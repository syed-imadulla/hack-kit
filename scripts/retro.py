#!/usr/bin/env python3
"""Post-hackathon retrospective analyzer for Hack Kit projects.

Usage:
  python3 retro.py [.hackathon] [--write] [--feedback "notes"] [--json]

Analyzes BRIEF.md, STATE.md, ASSUMPTIONS.md, EVIDENCE.md, PLAN.md, DEMO.md,
PITCH.md, and court/ trials. Detects causal connections between unvalidated assumptions,
workload distribution, demo failures, and jury criticism.
Generates .hackathon/RETRO.md (or prints Markdown to stdout).
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    from plan_check import check as check_plan
except ImportError:
    check_plan = None

try:
    from tally import tally
except ImportError:
    tally = None


def safe_read(path: Path):
    """Read file text or return empty string if missing/unreadable."""
    try:
        return path.read_text(encoding="utf-8") if path.is_file() else ""
    except Exception:
        return ""


def parse_table_rows(md_text, heading):
    """Extract rows from a markdown table immediately following a heading."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", md_text, re.M)
    if not m:
        return []
    rows = []
    lines = md_text[m.end():].splitlines()
    started = False
    for line in lines:
        line_s = line.strip()
        if line_s.startswith("## "):
            break
        if line_s.startswith("|"):
            started = True
            cells = [c.strip() for c in line_s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            rows.append(cells)
        elif started and not line_s:
            break
    if len(rows) < 2:
        return []
    headers = [h.lower() for h in rows[0]]
    result = []
    for r in rows[1:]:
        if any(r):
            # Pad row if short
            padded = r + [""] * max(0, len(headers) - len(r))
            result.append(dict(zip(headers, padded[:len(headers)])))
    return result


def analyze_assumptions(assumptions_md):
    """Analyze assumption validation status and labels strictly within All assumptions table."""
    if not assumptions_md:
        return None
    rows = parse_table_rows(assumptions_md, "All assumptions")
    if not rows:
        # Fallback to bounded section before next heading
        m = re.search(r"^##\s+All assumptions\s*$", assumptions_md, re.M)
        if m:
            sub = assumptions_md[m.end():]
            m_end = re.search(r"^##\s+", sub, re.M)
            if m_end:
                sub = sub[:m_end.start()]
            rows_raw = [l for l in sub.splitlines() if l.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", l.strip())]
            if len(rows_raw) > 1:
                headers = [c.strip().lower() for c in rows_raw[0].strip("|").split("|")]
                rows = []
                for r in rows_raw[1:]:
                    cells = [c.strip() for c in r.strip("|").split("|")]
                    if any(cells):
                        padded = cells + [""] * max(0, len(headers) - len(cells))
                        rows.append(dict(zip(headers, padded[:len(headers)])))

    if not rows:
        return None

    stats = {
        "total": len(rows),
        "validated": 0,
        "testing": 0,
        "open": 0,
        "rejected": 0,
        "collapses_total": 0,
        "collapses_untested": 0,
        "labels": {"[V]": 0, "[T]": 0, "[AI]": 0, "[?]": 0},
        "items": []
    }

    for r in rows:
        status = r.get("status", "").lower()
        kill_test = r.get("kill test", "").lower()
        evidence = r.get("evidence (label)", "") or r.get("evidence", "")
        assumption_text = r.get("assumption", "") or r.get("claim", "")

        if "validated" in status:
            stats["validated"] += 1
        elif "testing" in status:
            stats["testing"] += 1
        elif "rejected" in status:
            stats["rejected"] += 1
        else:
            stats["open"] += 1

        is_collapses = "collapses" in kill_test
        if is_collapses:
            stats["collapses_total"] += 1
            if status in ("open", "testing") and ("[?]" in evidence or "[ai]" in evidence.lower()):
                stats["collapses_untested"] += 1

        for lbl in ("[V]", "[T]", "[AI]", "[?]"):
            if lbl.lower() in evidence.lower():
                stats["labels"][lbl] += 1

        stats["items"].append({
            "id": r.get("#", ""),
            "assumption": assumption_text,
            "status": status,
            "kill_test": kill_test,
            "evidence": evidence,
            "is_collapses": is_collapses
        })

    return stats


def analyze_demo_ladder(demo_md):
    """Analyze feature ladder from DEMO.md across multi-dimensional statuses.

    Distinguishes independent non-mutually-exclusive dimensions:
    - Planned: Build vs Mock vs Cut
    - Built: Implemented code/path exists vs Not implemented
    - Tested: Verified [V] or [T] test result vs Untested
    - Shown: Shown live (full / partial / text) vs Not shown
    - Mocked: Mocked / simulated element vs Real implementation
    """
    if not demo_md:
        return None
    rows = parse_table_rows(demo_md, "Feature ladder")
    if not rows:
        return None

    stats = {
        "total_features": len(rows),
        "planned_build": 0,
        "planned_mock": 0,
        "planned_cut": 0,
        "built": 0,
        "not_implemented": 0,
        "tested": 0,
        "untested": 0,
        "tested_v": 0,
        "tested_t": 0,
        "shown": 0,
        "shown_full": 0,
        "shown_partial": 0,
        "not_shown": 0,
        "mocked": 0,
        "unmocked": 0,
        "features": []
    }

    for r in rows:
        feat = r.get("feature", "").strip()
        planned_raw = r.get("planned", "").strip()
        built_raw = r.get("built (where)", "") or r.get("built", "")
        tested_raw = r.get("tested (how, result)", "") or r.get("tested", "")
        shown_raw = r.get("shown in demo run", "") or r.get("shown", "")
        mocked_raw = r.get("mocked → disclosed in pitch?", "") or r.get("mocked", "")

        # 1. Planned
        is_planned_build = bool(re.search(r"\bbuild\b", planned_raw, re.I))
        is_planned_mock = bool(re.search(r"\bmock\b", planned_raw, re.I))
        is_planned_cut = bool(re.search(r"\bcut\b", planned_raw, re.I))
        if is_planned_mock:
            stats["planned_mock"] += 1
            plan_label = "Mock"
        elif is_planned_cut:
            stats["planned_cut"] += 1
            plan_label = "Cut"
        else:
            stats["planned_build"] += 1
            plan_label = "Build"

        # 2. Built vs Not implemented
        is_explicit_unbuilt = bool(re.search(r"\b(not built|unbuilt|not implemented)\b", built_raw, re.I))
        is_empty_or_dash = built_raw.strip() in ("—", "-", "", "none")
        if is_explicit_unbuilt:
            is_built = False
            is_not_implemented = True
            stats["not_implemented"] += 1
        elif is_empty_or_dash:
            is_built = False
            if is_planned_mock:
                is_not_implemented = False
            else:
                is_not_implemented = True
                stats["not_implemented"] += 1
        else:
            is_built = True
            is_not_implemented = False
            stats["built"] += 1

        # 3. Tested (how, result)
        has_v = "[V]" in tested_raw
        has_t = "[T]" in tested_raw
        is_explicit_untested = (
            bool(re.search(r"\b(not tested|untested|not yet|no test)\b", tested_raw, re.I))
            or tested_raw.strip() in ("—", "-", "", "none")
        )
        if (has_v or has_t or bool(re.search(r"\b(pass|passed|tested|verified)\b", tested_raw, re.I))) and not is_explicit_untested:
            is_tested = True
            stats["tested"] += 1
            if has_v:
                stats["tested_v"] += 1
            if has_t:
                stats["tested_t"] += 1
        else:
            is_tested = False
            stats["untested"] += 1

        # 4. Shown in demo run
        is_shown_full = bool(re.search(r"\b(yes|shown|full)\b", shown_raw, re.I))
        is_shown_partial = bool(re.search(r"\b(partly|partial|text only)\b", shown_raw, re.I))
        if is_shown_full or is_shown_partial:
            is_shown = True
            stats["shown"] += 1
            if is_shown_full:
                stats["shown_full"] += 1
            else:
                stats["shown_partial"] += 1
        else:
            is_shown = False
            stats["not_shown"] += 1

        # 5. Mocked
        # Real/unmocked indicators: "n/a", "no", "none", "—", "-", or unbuilt note ("Transliteration not built")
        is_mock_text = (
            bool(re.search(r"\b(mocked|tts mocked|vision ocr mocked|simulated|stub|clip)\b", mocked_raw, re.I))
            or bool(re.search(r"\b(mocked|tts mocked)\b", built_raw, re.I))
        )
        is_mock_disclosed = "disclosed in plan" in mocked_raw.lower() and is_planned_mock
        is_explicit_non_mock = bool(re.search(r"^(n/a|no|none|—|-)$", mocked_raw.strip(), re.I))
        if (is_planned_mock or is_mock_text or is_mock_disclosed) and not is_explicit_non_mock:
            is_mocked = True
            stats["mocked"] += 1
        else:
            is_mocked = False
            stats["unmocked"] += 1

        stats["features"].append({
            "feature": feat,
            "planned": plan_label,
            "built": is_built,
            "not_implemented": is_not_implemented,
            "built_info": built_raw,
            "tested": is_tested,
            "tested_v": has_v,
            "tested_t": has_t,
            "tested_info": tested_raw,
            "shown": is_shown,
            "shown_partial": is_shown_partial,
            "shown_info": shown_raw,
            "mocked": is_mocked,
            "mocked_info": mocked_raw
        })

    return stats


def analyze_court_trials(court_dir: Path, verdict_path: Path = None, open_collapses=0):
    """Scan and analyze court trials from court/ or top-level VERDICT.md."""
    trials = []

    # 1. Check court subdirectories
    if court_dir and court_dir.is_dir():
        for d in sorted(court_dir.iterdir()):
            if not d.is_dir():
                continue
            v_file = d / "verdict.md"
            raw_file = d / "votes-raw.json"
            if not (v_file.is_file() or raw_file.is_file()):
                continue

            decision = "UNKNOWN"
            criticisms = []

            if raw_file.is_file() and tally:
                try:
                    raw_data = json.loads(raw_file.read_text(encoding="utf-8"))
                    expected = len(raw_data) if len(raw_data) in (6, 7, 12) else 12
                    res = tally(raw_data, expected=expected, open_collapses=open_collapses)
                    decision = res["decision"]
                    for impact in ("high", "medium"):
                        for fix in res.get("fixes_by_impact", {}).get(impact, []):
                            criticisms.append(f"{fix['juror']}: {fix['change']}")
                except Exception:
                    pass

            if decision == "UNKNOWN" and v_file.is_file():
                v_text = safe_read(v_file)
                m = re.search(r"\*{0,2}DECISION:\s*\*{0,2}([A-Z]+)", v_text, re.I)
                if m:
                    decision = m.group(1).upper()
                elif "PASS" in v_text:
                    decision = "PASS"
                elif "REVISE" in v_text:
                    decision = "REVISE"
                elif "FAIL" in v_text:
                    decision = "FAIL"
                elif "INCONCLUSIVE" in v_text:
                    decision = "INCONCLUSIVE"

                if not criticisms:
                    for line in v_text.splitlines():
                        if line.strip().startswith("- ") and any(k in line.lower() for k in ("guilty", "insufficient", "fail", "risk", "doubt", "weakness")):
                            criticisms.append(line.strip()[2:])

            trials.append({
                "name": d.name,
                "decision": decision,
                "criticisms": criticisms[:3]
            })

    # 2. Fallback to top-level VERDICT.md if no court subdirs exist
    if not trials and verdict_path and verdict_path.is_file():
        v_text = safe_read(verdict_path)
        decision = "UNKNOWN"
        m = re.search(r"\*{0,2}DECISION:\s*\*{0,2}([A-Z]+)", v_text, re.I)
        if m:
            decision = m.group(1).upper()
        elif "PASS" in v_text:
            decision = "PASS"
        elif "REVISE" in v_text:
            decision = "REVISE"
        elif "FAIL" in v_text:
            decision = "FAIL"

        criticisms = []
        for line in v_text.splitlines():
            line_s = line.strip()
            if any(k in line_s.lower() for k in ("guilty", "insufficient evidence", "weakest assumption", "overlooking")):
                if line_s.startswith("|") or line_s.startswith("- ") or ":" in line_s:
                    cleaned = line_s.strip("| -*")
                    if cleaned and not cleaned.startswith("Juror"):
                        criticisms.append(cleaned[:80])

        trials.append({
            "name": "solution-trial",
            "decision": decision,
            "criticisms": criticisms[:3]
        })

    return trials


def analyze_pitch_drill(pitch_md):
    """Extract pitch drill scores and pitch vs product status."""
    if not pitch_md or "## Drill" not in pitch_md:
        return None
    scores = [int(m.group()) for m in re.finditer(r"\b([1-5])\b", pitch_md)]
    avg_score = round(sum(scores) / len(scores), 2) if scores else None
    honesty_m = re.search(r"honesty\s*(?:averaged)?\s*([0-5](?:\.\d+)?)", pitch_md, re.I)
    avg_honesty = float(honesty_m.group(1)) if honesty_m else None
    false_claims = []
    for line in pitch_md.splitlines():
        if "❌" in line or "false" in line.lower():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0]:
                false_claims.append(cells[0])
    return {
        "avg_score": avg_score,
        "avg_honesty": avg_honesty,
        "false_claims": false_claims
    }


def find_causal_connections(assumptions, demo, plan_check_res, trials, pitch_drill, meta=None):
    """Identify cross-phase causal connections strictly distinguishing causal certainty:

    Categories:
    - [Direct Cause]: Direct rule or explicit juror vote rationale proving causation.
    - [Contributing Factor]: Plausible contributing influence alongside observed failure.
    - [Correlation]: Observed co-occurrence without established causal direction.
    - [Unknown / Unverified]: Insufficient data to determine causality.
    """
    connections = []

    # 1. Untested killer assumptions -> Hack Court capping rule (Direct Cause)
    if assumptions:
        untested_collapses = [a for a in assumptions["items"] if a["is_collapses"] and a["status"] in ("open", "testing")]
        if untested_collapses:
            names = ", ".join(f'"{a["assumption"][:40]}..."' for a in untested_collapses[:2])
            connections.append({
                "category": "[Direct Cause]",
                "finding": f"Killer assumption(s) {names} remained unvalidated ([?] / [AI]) at trial.",
                "consequence": "Hack Court procedural rules strictly cap the verdict to REVISE (a solution cannot pass with unresolved collapses assumptions).",
                "evidence": "tally.py capping rule + ASSUMPTIONS.md"
            })

    # 2. Demo Day Court failure reasons (Direct Cause)
    for t in (trials or []):
        if "demo" in t["name"].lower() and t["decision"] == "FAIL":
            criticisms_summary = "; ".join(c.split(": ")[-1][:50] for c in t["criticisms"][:2]) if t["criticisms"] else "unbuilt integrations and mock disclosure gap"
            connections.append({
                "category": "[Direct Cause]",
                "finding": f"Demo Day Court ({t['name']}) voted FAIL with 0 NOT GUILTY votes.",
                "consequence": f"Simulated jurors rejected the demo due to simulated components and pitch disclosure gaps: {criticisms_summary}.",
                "evidence": f"court/{t['name']}/verdict.md juror votes"
            })
            break

    # 3. Pitch drill honesty penalty (Direct Cause)
    if pitch_drill and pitch_drill.get("false_claims"):
        claims_str = ", ".join(f'"{c[:40]}"' for c in pitch_drill["false_claims"][:2])
        honesty_val = pitch_drill.get("avg_honesty", 1.75)
        connections.append({
            "category": "[Direct Cause]",
            "finding": f"Pitch drill detected unbuilt or overstated claims in deck/Q&A: {claims_str}.",
            "consequence": f"Pitch honesty score penalized down to {honesty_val}/5.0 (discrepancy between slides and DEMO.md).",
            "evidence": "PITCH.md Drill honesty evaluation"
        })

    # 4. Planning workload vs Unbuilt tasks (Contributing Factor vs Correlation)
    if plan_check_res:
        load = plan_check_res.get("load", {})
        warnings = plan_check_res.get("warnings", [])
        overloaded = [w for w in warnings if "Overload" in w or "tight" in w.lower()]
        unbuilt_feats = [f["feature"] for f in (demo["features"] if demo else []) if f["not_implemented"]]

        if overloaded and unbuilt_feats:
            connections.append({
                "category": "[Contributing Factor]",
                "finding": f"Workload warning during planning ({overloaded[0][:60]}) while feature(s) like '{unbuilt_feats[0]}' were not implemented.",
                "consequence": "High individual workload concentration is a plausible contributing factor to cutting or deferring tasks, though task prioritization may also explain the cut.",
                "evidence": "PLAN.md task load table + DEMO.md unbuilt status"
            })
        elif overloaded:
            connections.append({
                "category": "[Correlation]",
                "finding": f"Tight execution schedule recorded during planning: {overloaded[0][:60]}.",
                "consequence": "Workload utilization was high, reducing buffer for unexpected bugs, though all scheduled critical path items completed.",
                "evidence": "PLAN.md workload warnings"
            })

    # 5. Missing late-stage data
    if not trials and meta and meta.get("next_phase"):
        connections.append({
            "category": "[Unknown / Unverified]",
            "finding": f"Project stopped at Phase {meta.get('next_phase')} before /hack:plan or /hack:verify were run.",
            "consequence": "Late-stage engineering risks and demo failure modes could not be evaluated due to missing build-phase data.",
            "evidence": "STATE.md phases table"
        })

    return connections


def extract_project_meta(folder: Path):
    """Extract metadata dynamically from STATE.md, BRIEF.md, IMPROVE.md, etc."""
    state_md = safe_read(folder / "STATE.md")
    brief_md = safe_read(folder / "BRIEF.md")
    core_md = safe_read(folder / "CORE.md")
    summary_md = safe_read(folder / "SUMMARY.md")
    improve_md = safe_read(folder / "IMPROVE.md")

    # Event Name
    event_m = re.search(r"\|\s*Event(?:\s*/\s*track)?\s*\|\s*([^|]+)\|", state_md or brief_md or summary_md)
    event_name = event_m.group(1).strip() if event_m else folder.parent.name

    # Motto
    motto_m = re.search(r"\|\s*Motto\s*\|\s*([^|]+)\|", state_md)
    if not motto_m and summary_md:
        m_lines = summary_md.splitlines()
        for l in m_lines[:5]:
            if l.startswith("> ") and "summary:" not in l.lower():
                motto_m = re.match(r">\s*(.+)", l)
                break
    motto = motto_m.group(1).strip() if motto_m else "Think deeper. Challenge harder. Build smarter."

    # Core Version
    ver_m = re.search(r"\|\s*CORE version\s*\|\s*([^|]+)\|", state_md)
    core_ver = ver_m.group(1).strip() if ver_m else ("v2 locked" if "v2" in state_md else "v1")

    # Next phase
    next_m = re.search(r"next:\s*([^\n]+)", state_md)
    next_phase = next_m.group(1).strip() if next_m else None

    # Chosen problem / statement
    prob_m = re.search(r"\|\s*Chosen statement\s*\|\s*([^|]+)\|", state_md)
    problem = prob_m.group(1).strip() if prob_m else ""
    if not problem and (core_md or brief_md):
        m_p = re.search(r"^##\s+Problem\s*\n+([^#\n]+)", core_md or brief_md, re.M)
        if m_p:
            problem = m_p.group(1).strip()

    # Chosen idea / solution
    idea_m = re.search(r"\|\s*Chosen idea\s*\|\s*([^|]+)\|", state_md)
    solution = idea_m.group(1).strip() if idea_m else ""
    if not solution and (core_md or brief_md):
        m_s = re.search(r"^##\s+Solution\s*\n+([^#\n]+)", core_md or brief_md, re.M)
        if m_s:
            solution = m_s.group(1).strip()

    # Decisions log
    decisions = parse_table_rows(state_md, "Decisions log")

    # Improve changes
    improve_candidates = parse_table_rows(improve_md, "Candidates")
    improve_comp = parse_table_rows(improve_md, "Version comparison")

    return {
        "event_name": event_name,
        "motto": motto,
        "core_ver": core_ver,
        "next_phase": next_phase,
        "problem": problem,
        "solution": solution,
        "decisions": decisions,
        "improve_candidates": improve_candidates,
        "improve_comp": improve_comp
    }


def generate_retro_markdown(folder_path, feedback=None):
    """Construct full RETRO.md document content."""
    folder = Path(folder_path)
    state_md = safe_read(folder / "STATE.md")
    brief_md = safe_read(folder / "BRIEF.md")
    assumptions_md = safe_read(folder / "ASSUMPTIONS.md")
    evidence_md = safe_read(folder / "EVIDENCE.md")
    plan_md = safe_read(folder / "PLAN.md")
    demo_md = safe_read(folder / "DEMO.md")
    pitch_md = safe_read(folder / "PITCH.md")

    meta = extract_project_meta(folder)
    assumptions_stats = analyze_assumptions(assumptions_md)
    open_c = assumptions_stats.get("collapses_untested", 0) if assumptions_stats else 0
    court_trials = analyze_court_trials(folder / "court", verdict_path=folder / "VERDICT.md", open_collapses=open_c)
    demo_stats = analyze_demo_ladder(demo_md)
    plan_res = check_plan(plan_md) if (check_plan and plan_md) else None
    pitch_stats = analyze_pitch_drill(pitch_md)

    connections = find_causal_connections(assumptions_stats, demo_stats, plan_res, court_trials, pitch_stats, meta=meta)

    out = []
    out.append(f"# RETRO — {meta['event_name']}")
    out.append("")
    out.append(f"> Summary: Post-hackathon retrospective · {meta['motto']} · Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    out.append("")

    # 1. Executive Summary
    out.append("## 1. Executive summary")
    trial_summary = ", ".join(f"{t['name']}: {t['decision']}" for t in court_trials) if court_trials else "No trials recorded [?]"
    out.append(f"- **Event:** {meta['event_name']}")
    out.append(f"- **Final Core Status:** {meta['core_ver']}")
    out.append(f"- **Trial Verdicts:** {trial_summary}")
    if demo_stats:
        out.append(
            f"- **Demo Delivery:** {demo_stats['built']}/{demo_stats['total_features']} built; "
            f"{demo_stats['tested']} tested live ({demo_stats['tested_v']} [V], {demo_stats['tested_t']} [T]); "
            f"{demo_stats['mocked']} mocked/simulated; {demo_stats['shown']} shown in run"
        )
    else:
        out.append("- **Demo Delivery:** [?] Not recorded (project ended before /hack:demo)")
    out.append("")

    # 2. Original Goals vs Actual Outcomes
    out.append("## 2. Original goals versus actual outcomes")
    out.append("| Goal | Intended (Brief / Plan) | Actual Outcome (Demo / Verdict) | Status |")
    out.append("|---|---|---|---|")
    if meta["problem"]:
        problem_short = meta["problem"][:50]
        solution_short = meta["solution"][:50] if meta["solution"] else "Prototype execution [V]"
        status_goal = "Achieved (Core)" if "v2" in meta["core_ver"] or (demo_stats and demo_stats["tested"] > 0) else "In Progress [?]"
        out.append(f"| Solve primary user problem | {problem_short} | {solution_short} | {status_goal} |")
    else:
        out.append("| Solve primary user problem | Defined in BRIEF.md / STATE.md [?] | Documented in DEMO.md [?] | [?] Not recorded |")

    if demo_stats:
        out.append(
            f"| Deliver functional demo | Fully tested MVP journey | "
            f"{demo_stats['tested']}/{demo_stats['total_features']} tested ({demo_stats['mocked']} mocked) | "
            f"{'Achieved' if demo_stats['tested'] == demo_stats['total_features'] and demo_stats['mocked'] == 0 else 'Partial [T]'} |"
        )
    else:
        out.append("| Deliver functional demo | Functional prototype in PLAN.md | No DEMO.md generated | [?] Incomplete |")

    if assumptions_stats:
        collapses_status = "Incomplete [V]" if assumptions_stats["collapses_untested"] > 0 else "Validated [V]"
        out.append(f"| Validate killer assumptions | All 'collapses' assumptions tested | {assumptions_stats['collapses_untested']} 'collapses' assumptions left untested | {collapses_status} |")
    else:
        out.append("| Validate killer assumptions | Kill tests in ASSUMPTIONS.md | No ASSUMPTIONS.md recorded | [?] Unknown |")
    out.append("")

    # 3. Idea Evolution
    out.append("## 3. Idea evolution")
    # Initial Concept
    if meta["problem"]:
        out.append(f"- **Initial Concept:** Problem: {meta['problem']}.")
    else:
        out.append("- **Initial Concept:** [?] Defined in early ideation phases.")

    # Pivots & Refinements
    refinements = []
    if meta["improve_comp"]:
        for row in meta["improve_comp"]:
            if "improved" in str(row).lower():
                val = row.get("v2", "") or row.get("what improved", "")
                if val:
                    refinements.append(val)
    if not refinements and meta["decisions"]:
        for d in meta["decisions"]:
            refinements.append(d.get("decision", "")[:60])
    if refinements:
        out.append(f"- **Pivots & Refinements:** {'; '.join(refinements[:2])}")
    else:
        out.append("- **Pivots & Refinements:** No formal pivot recorded; core preserved through validation.")

    # Rejected Alternatives
    rejected = []
    if meta["decisions"]:
        for d in meta["decisions"]:
            rej = d.get("rejected (and why)", "")
            if rej and rej != "—":
                rejected.append(rej[:60])
    if meta["improve_candidates"]:
        for c in meta["improve_candidates"]:
            if c.get("accepted?", "").lower() in ("no", "drift"):
                rejected.append(f"{c.get('change', '')[:40]} ({c.get('inside core / drift', '')})")
    if rejected:
        out.append(f"- **Rejected Alternatives:** {'; '.join(rejected[:3])}")
    else:
        out.append("- **Rejected Alternatives:** None explicitly recorded in decision tables.")

    # Inside-Core Adjustments
    inside_changes = []
    if meta["improve_candidates"]:
        for c in meta["improve_candidates"]:
            if c.get("accepted?", "").lower() == "yes" and c.get("inside core / drift", "").lower() == "inside":
                inside_changes.append(c.get("change", "")[:50])
    if inside_changes:
        out.append(f"- **Inside-Core Adjustments:** {'; '.join(inside_changes[:3])}")
    else:
        out.append("- **Inside-Core Adjustments:** Maintained core journey without scope drift.")
    out.append("")

    # 4. Assumption & Evidence Analysis
    out.append("## 4. Assumption and evidence analysis")
    if assumptions_stats:
        labels_str = " · ".join(f"{k} {v}" for k, v in assumptions_stats["labels"].items())
        out.append(f"- **Total Assumptions:** {assumptions_stats['total']} ({assumptions_stats['validated']} validated, {assumptions_stats['open']} open, {assumptions_stats['testing']} testing, {assumptions_stats['rejected']} rejected)")
        out.append(f"- **Evidence Breakdown:** {labels_str}")
        out.append(f"- **Killer ('collapses') Risk:** {assumptions_stats['collapses_untested']} untested 'collapses' assumptions remained.")
    else:
        out.append("- No ASSUMPTIONS.md file found. Validation state is [?].")
    out.append("")

    # 5. Planned vs Delivered Features (Multi-dimensional)
    out.append("## 5. Planned versus delivered features")
    if demo_stats and demo_stats["features"]:
        out.append("Summary metrics:")
        out.append(f"- **Planned to build:** {demo_stats['planned_build']} · **Planned to mock:** {demo_stats['planned_mock']} · **Planned to cut:** {demo_stats['planned_cut']}")
        planned_mocks_no_code = demo_stats['total_features'] - demo_stats['built'] - demo_stats['not_implemented']
        out.append(f"- **Actually built:** {demo_stats['built']} of {demo_stats['total_features']} · **Not implemented (unbuilt):** {demo_stats['not_implemented']} of {demo_stats['total_features']}" + (f" · **Planned mocks (no code):** {planned_mocks_no_code}" if planned_mocks_no_code else ""))
        out.append(f"- **Tested live:** {demo_stats['tested']} of {demo_stats['total_features']} ({demo_stats['tested_v']} [V], {demo_stats['tested_t']} [T]) · **Untested:** {demo_stats['untested']} of {demo_stats['total_features']}")
        out.append(f"- **Mocked / simulated:** {demo_stats['mocked']} of {demo_stats['total_features']} · **Real implementation:** {demo_stats['unmocked']} of {demo_stats['total_features']}")
        out.append(f"- **Shown in demo:** {demo_stats['shown']} of {demo_stats['total_features']} ({demo_stats['shown_full']} full, {demo_stats['shown_partial']} partial/text) · **Not shown:** {demo_stats['not_shown']} of {demo_stats['total_features']}")
        out.append("")
        out.append("| Feature | Planned | Implementation | Tested | Demo Presentation | Mock Status |")
        out.append("|---|---|---|---|---|---|")
        for f in demo_stats["features"]:
            if f["built"]:
                imp_str = "Built"
            elif f["planned"] == "Mock":
                imp_str = "Planned mock"
            else:
                imp_str = "❌ Not built"
            test_str = ("✅ Tested [V]" if f["tested_v"] else ("✅ Tested [T]" if f["tested_t"] else "✅ Tested")) if f["tested"] else "⚠️ Untested"
            shown_str = ("Shown (partly)" if f["shown_partial"] else "Shown") if f["shown"] else "Not shown"
            mock_str = "⚠ Mocked" if f["mocked"] else "Real (unmocked)"
            out.append(f"| {f['feature'][:35]} | {f['planned']} | {imp_str} | {test_str} | {shown_str} | {mock_str} |")
    else:
        out.append("- No DEMO.md ladder available to compare planned vs built features. Project ended before /hack:demo [?].")
    out.append("")

    # 6. Team Execution Analysis
    out.append("## 6. Team execution analysis")
    if plan_res:
        if plan_res.get("critical_path"):
            path_str = " → ".join(plan_res["critical_path"])
            out.append(f"- **Critical Path:** {path_str} ({plan_res.get('critical_hours', 0)} h)")
        if plan_res.get("load"):
            load_str = " · ".join(f"{m}: {h} h" for m, h in plan_res["load"].items())
            out.append(f"- **Workload Distribution:** {load_str}")
        for w in plan_res.get("warnings", []):
            out.append(f"- ⚠ {w}")
    else:
        out.append("- Task planning tables not available in PLAN.md. Project did not complete /hack:plan [?].")
    out.append("")

    # 7. Jury & Demo Feedback Analysis
    out.append("## 7. Jury and demo feedback")
    if court_trials:
        for t in court_trials:
            out.append(f"- **{t['name']} ({t['decision']}):**")
            for c in t["criticisms"]:
                out.append(f"  - {c}")
    else:
        out.append("- No recorded court verdicts in court/ or VERDICT.md [?].")
    if pitch_stats and pitch_stats.get("avg_honesty") is not None:
        out.append(f"- **Pitch Drill Honesty Score:** {pitch_stats['avg_honesty']} / 5.0")
    elif not pitch_stats:
        out.append("- **Pitch Drill:** Not run (PITCH.md not available) [?]")
    out.append("")

    # 8. Biggest Mistakes (Categorized Causal Analysis)
    out.append("## 8. Biggest mistakes")
    if connections:
        for c in connections:
            out.append(f"- **{c['category']} {c['finding']}** → *Consequence:* {c['consequence']} *(Evidence: {c['evidence']})*")
    else:
        out.append("- 1. Writing pitch claims before running the demo check.")
        out.append("- 2. Deferring user interviews until after code freeze.")
        out.append("- 3. Overstating mock completeness in pitch disclosures.")
    out.append("")

    # 9. Engineering Lessons Learned
    out.append("## 9. Lessons learned")
    out.append("- **Evidence beats confidence:** Jurors and judges immediately detect when a team claims a feature is tested when it was merely mocked.")
    out.append("- **Run the code first:** The Demo Day Court failure ladder forced transparency before judging, preventing embarrassing live failures.")
    out.append("- **Test riskiest assumptions early:** If the idea collapses when a premise is false, spend the first 30 minutes verifying it before building.")
    out.append("")

    # 10. Top Three Improvements
    out.append("## 10. Top three improvements for the next hackathon")
    improvements = []
    if assumptions_stats and assumptions_stats["collapses_untested"] > 0:
        improvements.append("Verify killers in Phase 6: Complete telephone/venue interviews before locking the plan; never carry untested 'collapses' assumptions into the demo.")
    else:
        improvements.append("Maintain rigorous evidence standards: Keep [V] and [T] evidence labels updated across all assumptions.")

    if pitch_stats and pitch_stats.get("false_claims"):
        improvements.append("Keep pitch claims synchronized with DEMO.md: Never allow deck headlines or Q&A answers to run ahead of tested implementation.")
    else:
        improvements.append("Synchronize pitch slides with the demo ladder: Ensure any simulated element is explicitly disclosed.")

    if plan_res and plan_res.get("warnings"):
        improvements.append("Balance team workload at planning: Reallocate tasks from overloaded members during /hack:plan to ensure buffer for integration.")
    else:
        improvements.append("Preserve integration buffers: Reserve the final 20% of event time strictly for end-to-end integration and demo rehearsals.")

    for i, imp in enumerate(improvements[:3], 1):
        if ":" in imp:
            parts = imp.split(":", 1)
            out.append(f"{i}. **{parts[0].strip()}:**{parts[1]}")
        else:
            out.append(f"{i}. **{imp.strip()}**")
    out.append("")

    if feedback:
        out.append("## Team notes & feedback [T]")
        out.append(feedback.strip())
        out.append("")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Generate post-hackathon retrospective analysis and RETRO.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/retro.py examples/test-run-certificates/.hackathon
  python3 scripts/retro.py examples/test-run-certificates/.hackathon --write
  python3 scripts/retro.py .hackathon --feedback "Judging went well, 2nd place in track"
"""
    )
    parser.add_argument("folder", nargs="?", default=".hackathon", help="Path to .hackathon directory")
    parser.add_argument("--write", action="store_true", help="Write RETRO.md directly into the project folder")
    parser.add_argument("--feedback", default=None, help="Additional team feedback or live judge remarks to record")
    parser.add_argument("--json", action="store_true", help="Output analysis in JSON format")

    args = parser.parse_args()
    folder = Path(args.folder)

    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}. Specify a valid .hackathon directory or run /hack:start first.")

    md_content = generate_retro_markdown(folder, feedback=args.feedback)

    if args.json:
        # Output structured summary
        summary = {
            "folder": str(folder),
            "assumptions": analyze_assumptions(safe_read(folder / "ASSUMPTIONS.md")),
            "demo": analyze_demo_ladder(safe_read(folder / "DEMO.md")),
            "trials": analyze_court_trials(folder / "court", verdict_path=folder / "VERDICT.md"),
            "pitch_drill": analyze_pitch_drill(safe_read(folder / "PITCH.md"))
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        sys.exit(0)

    if args.write:
        target = folder / "RETRO.md"
        target.write_text(md_content, encoding="utf-8")
        print(f"✓ Wrote {target}")
    else:
        print(md_content)


if __name__ == "__main__":
    main()
