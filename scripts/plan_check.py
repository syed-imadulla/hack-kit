#!/usr/bin/env python3
"""Check the task plan in PLAN.md: critical path, overload, skills, dependencies, freeze fit.

Usage: python3 plan_check.py [.hackathon/PLAN.md] [--json]

Reads two tables from PLAN.md:
  ## Team    | Member | Skills | Hours available |
  ## Tasks   | ID | Task | Owner | Skills needed | Hours | Depends on | Status |
and the line "Hours until code freeze: N" (optional).

Prints a Markdown "## Plan check" section to paste into PLAN.md. Nothing is invented: if a table is
missing or malformed, it says so.
"""
import json
import re
import sys
from pathlib import Path


def table_after(md, heading):
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", md, re.M)
    if not m:
        return None
    rows, started = [], False
    for line in md[m.end():].splitlines():
        if line.startswith("## "):
            break
        if line.startswith("|"):
            started = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            rows.append(cells)
        elif started and line.strip() == "":
            break
    if not rows:
        return None
    head = [h.lower() for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[1:] if any(r)]


def num(x):
    m = re.search(r"\d+(\.\d+)?", x or "")
    return float(m.group()) if m else 0.0


def split(x):
    return [s.strip().lower() for s in re.split(r"[,;/·]| and ", x or "") if s.strip() and s.strip() not in ("—", "-", "none")]


def check(md):
    team = table_after(md, "Team")
    tasks = table_after(md, "Tasks")
    out = {"errors": [], "warnings": [], "critical_path": [], "critical_hours": 0, "load": {}, "integration_points": []}
    if not tasks:
        out["errors"].append("No '## Tasks' table found (columns: ID | Task | Owner | Skills needed | Hours | Depends on | Status).")
        return out
    all_t = {r.get("id", "").strip(): r for r in tasks if r.get("id", "").strip()}
    # "maybe" tasks are conditional: listed, but not counted in load or the critical path
    t = {i: r for i, r in all_t.items() if r.get("status", "").strip().lower() != "maybe"}
    out["conditional"] = [i for i in all_t if i not in t]
    members = {}
    for r in team or []:
        members[r.get("member", "").strip().lower()] = {"skills": split(r.get("skills", "")), "hours": num(r.get("hours available", ""))}
    if not team:
        out["warnings"].append("No '## Team' table: can't check overload or skills.")

    # dependencies
    deps = {i: [d.strip() for d in re.split(r"[,; ]+", r.get("depends on", "")) if d.strip() and d.strip() not in ("—", "-")] for i, r in t.items()}
    for i, ds in deps.items():
        for d in ds:
            if d not in all_t:
                out["errors"].append(f"{i} depends on unknown task {d}.")
            elif d not in t:
                out["warnings"].append(f"{i} depends on conditional task {d}: decide {d} before starting {i}.")
    state = {}

    def visit(i, stack):
        if state.get(i) == 1:
            out["errors"].append("Dependency loop: " + " → ".join(stack + [i]))
            return
        if state.get(i) == 2:
            return
        state[i] = 1
        for d in deps.get(i, []):
            if d in t:
                visit(d, stack + [i])
        state[i] = 2
    for i in t:
        visit(i, [])
    if any(e.startswith("Dependency loop") for e in out["errors"]):
        return out

    # critical path (longest by hours)
    memo = {}

    def longest(i):
        if i in memo:
            return memo[i]
        best = (0.0, [])
        for d in deps.get(i, []):
            if d in t:
                h, p = longest(d)
                if h > best[0]:
                    best = (h, p)
        memo[i] = (best[0] + num(t[i].get("hours")), best[1] + [i])
        return memo[i]
    if t:
        hours, path = max((longest(i) for i in t), key=lambda x: x[0])
        out["critical_path"], out["critical_hours"] = path, hours

    # load, skills, unassigned
    for i, r in t.items():
        owner = r.get("owner", "").strip().lower()
        if not owner or owner in ("—", "-", "?"):
            out["warnings"].append(f"{i} ({r.get('task', '')}) has no owner.")
            continue
        owners = split(owner)
        for o in owners:
            out["load"][o] = out["load"].get(o, 0) + num(r.get("hours")) / max(1, len(owners))
            if members and o not in members:
                out["warnings"].append(f"{i}: owner '{o}' isn't in the Team table.")
        if members and all(o in members for o in owners):
            need = split(r.get("skills needed", ""))
            have = [h for o in owners for h in members[o]["skills"]]  # shared task: any owner's skill counts
            missing = [n for n in need if not any(n in h or h in n for h in have)]
            if missing:
                out["warnings"].append(f"{i}: {', '.join(owners)} may lack {', '.join(missing)}. Pair with someone who has it, or reassign.")
    for o, h in out["load"].items():
        cap = members.get(o, {}).get("hours", 0)
        if cap and h > 0.85 * cap:
            spare = sorted(((members[m]["hours"] - out["load"].get(m, 0), m) for m in members if m != o), reverse=True)
            hint = ", ".join(f"{m} has {s:g} h spare" for s, m in spare[:2] if s > 0)
            out["warnings"].append(f"Overload: {o} has {h:g} h of tasks for {cap:g} h available ({h / cap:.0%}). Move or cut a task" + (f" ({hint})." if hint else "."))
    idle = [m for m, v in members.items() if v["hours"] and out["load"].get(m, 0) < 0.4 * v["hours"]]
    for m in idle:
        out["warnings"].append(f"Underused: {m} has {out['load'].get(m, 0):g} h of tasks for {members[m]['hours']:g} h available.")

    # integration points: tasks depending on work by 2+ different owners
    for i, ds in deps.items():
        owners = {t[d].get("owner", "").strip().lower() for d in ds if d in t}
        if len(owners) >= 2:
            out["integration_points"].append(i)

    m = re.search(r"Hours until code freeze:\s*(\d+(\.\d+)?)", md)
    if m:
        freeze = float(m.group(1))
        out["hours_to_freeze"] = freeze
        share = out["critical_hours"] / freeze if freeze else 0
        if share >= 0.9:
            out["warnings"].append(f"Critical path is {out['critical_hours']:g} h of {freeze:g} h to code freeze ({share:.0%}): no slack. Cut or mock something on the path.")
        elif share >= 0.7:
            out["warnings"].append(f"Critical path is {out['critical_hours']:g} h of {freeze:g} h to code freeze ({share:.0%}): tight. Start the path first, and pick what to mock if it slips.")
    return out


def to_md(r):
    lines = ["## Plan check", ""]
    for e in r["errors"]:
        lines.append(f"- ✗ {e}")
    if r["critical_path"]:
        f = f" of {r['hours_to_freeze']:g} h to code freeze" if "hours_to_freeze" in r else ""
        lines.append(f"- **Critical path:** {' → '.join(r['critical_path'])} ({r['critical_hours']:g} h{f}). Any delay here delays the demo.")
    if r["load"]:
        lines.append("- **Load:** " + " · ".join(f"{o} {h:g} h" for o, h in sorted(r["load"].items())))
    if r["integration_points"]:
        lines.append(f"- **Integration checkpoints:** {', '.join(r['integration_points'])}. Test these joins early, not at the end.")
    if r.get("conditional"):
        lines.append(f"- **Conditional (status maybe, not counted):** {', '.join(r['conditional'])}")
    for w in r["warnings"]:
        lines.append(f"- ⚠ {w}")
    if not r["errors"] and not r["warnings"]:
        lines.append("- ✓ No overload, skill gaps or dependency problems found.")
    return "\n".join(lines)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = Path(args[0] if args else ".hackathon/PLAN.md")
    if not path.exists():
        sys.exit(f"Not found: {path}")
    r = check(path.read_text(encoding="utf-8"))
    print(json.dumps(r, indent=2) if "--json" in sys.argv else to_md(r))
    sys.exit(1 if r["errors"] else 0)


if __name__ == "__main__":
    main()
