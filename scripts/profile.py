#!/usr/bin/env python3
"""Combine a Hack Kit event profile into one table of effective settings.

Usage:
  python3 profile.py [--type college|sih|ai-ml|ideathon|hardware|corporate]
                     [--length 12h|24h|36h|48h+] [--experience beginner|mixed|advanced]
                     [--focus balanced|technical|innovation-impact|business] [--team N]
                     [--path auto|full|starter] [--json]

Missing options use the defaults in skills/hack-kit/profiles.json. Output is a Markdown block
for STATE.md ("## Profile"), or JSON with --json. Order: length → event type → experience → focus → path.
--path auto (the default) picks the starter path for beginner teams and the full path otherwise.
"""
import json
import sys
from pathlib import Path

_BASE = Path(__file__).resolve().parent.parent
# Repo layout (skills/hack-kit/profiles.json) or portable skill layout (<skill>/profiles.json next to scripts/)
PROFILES = next((c for c in (_BASE / "skills" / "hack-kit" / "profiles.json", _BASE / "profiles.json") if c.exists()),
                _BASE / "skills" / "hack-kit" / "profiles.json")


def load():
    return json.loads(PROFILES.read_text(encoding="utf-8"))


def resolve_path(p, path, experience):
    path = path or p["defaults"].get("path", "auto")
    if path == "auto":
        return "starter" if experience == "beginner" else "full"
    if path not in p["paths"]:
        raise SystemExit(f"Unknown path '{path}'. Choose from: auto, {', '.join(p['paths'])}")
    return path


def apply_path(p, path, s):
    """Return (commands, folded, skipped) for the path, and change settings s in place."""
    spec = p["paths"][path]
    if path == "full":
        cmds = [c for c in spec["commands"] if c not in s.get("skip_phases", [])]
        return cmds, {}, {}
    plan_skipped = "plan" in s.get("skip_phases", [])
    cmds = list(spec["commands_if_plan_skipped"] if plan_skipped else spec["commands"])
    folded = dict(spec["folded"])
    if plan_skipped:  # ideathons: the lock (with a short stress check) happens in /hack:lock instead
        folded = {k: ("lock" if v == "plan" and k != "lock" else v) for k, v in folded.items() if k != "lock"}
    for k, cap in spec["caps"].items():
        if isinstance(s.get(k), (int, float)) and not isinstance(s.get(k), bool):
            s[k] = min(s[k], cap)
    s.update(spec["changes"])
    all_phases = p["paths"]["full"]["commands"]
    s["skip_phases"] = sorted(set(all_phases) - set(cmds) - {spec.get("optional_end")})
    return cmds, folded, dict(spec["skipped"])


def combine(p, event_type=None, length=None, experience=None, focus=None, team=None, path=None):
    d = p["defaults"]
    event_type, length = event_type or d["event_type"], length or d["length"]
    experience, focus = experience or d["experience"], focus or d["focus"]
    try:
        team = int(team if team is not None else d["team_size"])
    except (ValueError, TypeError):
        raise SystemExit(f"Invalid --team value '{team}'. Team size must be an integer (e.g. --team 4).")
    for key, group in (("event type", (event_type, p["event_types"])), ("length", (length, p["lengths"])),
                       ("experience", (experience, p["experience"])), ("focus", (focus, p["focus"]))):
        if group[0] not in group[1]:
            raise SystemExit(f"Unknown {key} '{group[0]}'. Choose from: {', '.join(group[1])}")

    s = dict(p["lengths"][length]["settings"])
    et = p["event_types"][event_type]
    for k, v in et.get("changes", {}).items():
        if k == "skip_phases":
            s[k] = sorted(set(s.get(k, [])) | set(v))
        else:
            s[k] = v
    s.update(p["experience"][experience].get("changes", {}))
    s.setdefault("explain_steps", False)

    # Small teams: fewer parallel phases and lighter plans.
    if team <= 2:
        s["parallel_validate_compete"] = False
        s["plan_depth"] = "light" if s.get("plan_depth") != "deep" else "standard"
    else:
        s["parallel_validate_compete"] = True

    path = resolve_path(p, path, experience)
    commands, folded, skipped = apply_path(p, path, s)
    s["path"] = path

    notes = list(et.get("notes", [])) + list(p["experience"][experience].get("notes", [])) + \
        list(p["focus"][focus].get("notes", [])) + list(p["paths"][path].get("notes", []))
    return {
        "profile": {"event_type": event_type, "length": length, "experience": experience,
                    "focus": focus, "team_size": team, "path": path},
        "path": {"name": path, "label": p["paths"][path]["label"], "commands": commands,
                 "optional_end": p["paths"][path].get("optional_end"), "folded": folded, "skipped": skipped},
        "labels": {"event_type": et["label"], "length": p["lengths"][length]["label"],
                   "experience": p["experience"][experience]["label"], "focus": p["focus"][focus]["label"]},
        "settings": s,
        "rubric_default": et["rubric_default"],
        "scoring_weights": p["focus"][focus]["weights"],
        "plan_extras": et.get("plan_extras", []),
        "quick_jury_swap": et.get("quick_jury_swap"),
        "notes": notes,
    }


def to_markdown(r):
    pr, lb, s = r["profile"], r["labels"], r["settings"]
    pa = r["path"]
    cmd_line = " → ".join(f"/hack:{c}" for c in pa["commands"])
    if pa.get("optional_end"):
        cmd_line += f" (then /hack:{pa['optional_end']} for the PDF)"
    rows = [
        ("Path", pa["label"]), ("Commands, in order", cmd_line),
    ]
    if pa["folded"]:
        by_cmd = {}
        for phase, into in pa["folded"].items():
            by_cmd.setdefault(into, []).append(phase)
        rows.append(("Folded in (short versions)", " · ".join(f"{', '.join(v)} → /hack:{k}" for k, v in by_cmd.items())))
    rows += [
        ("Mode", s["mode"]), ("Questions per command", s["questions_per_command"]),
        ("Explain each step (beginner)", "yes" if s.get("explain_steps") else "no"),
        ("Decode research", s["decode_research"]), ("Sources to open per key claim", s["sources_to_open"]),
        ("Pick: trials · jury", f'{s["pick_trials"]} · {s["pick_jury"]} jurors'),
        ("Ideate: directions × ideas", f'{s["ideate_directions"]} × {s["ideas_per_direction"]}'
         + (" + constraint removal" if s["constraint_removal"] else "")),
        ("Validate: experiments", s["validate_experiments"]),
        ("Improve: rounds · re-trial", f'{s["improve_rounds"]} · {s["improve_retrial"]}'),
        ("Verify jury · Demo Day Court", f'{s["verify_jury"]} jurors · {s["demo_court"]}'),
        ("Plan depth", s["plan_depth"]), ("Pitch depth · drill questions", f'{s["pitch_depth"]} · {s["drill_questions"]}'),
        ("Validate ‖ compete in parallel", "yes" if s["parallel_validate_compete"] else "no (small team)"),
        ("Skip phases", ", ".join(x for x in s["skip_phases"] if x not in pa["folded"]) or "none"),
        ("Target: idea locked within", f'{s["lock_target_minutes"]} min'),
    ]
    out = ["## Profile", "",
           f'**{lb["event_type"]}** · {lb["length"]} · team of {pr["team_size"]} · {lb["experience"]} · focus: {lb["focus"]}',
           f'`--type {pr["event_type"]} --length {pr["length"]} --experience {pr["experience"]} --focus {pr["focus"]} --team {pr["team_size"]} --path {pr["path"]}`',
           "", "| Setting | Value |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in rows]
    w = r["scoring_weights"]
    out += ["", "Scoring weights (pick/ideate): " + " · ".join(f"{k} ×{v}" for k, v in w.items())]
    if r["quick_jury_swap"]:
        out += [f'Quick jury: seat **{r["quick_jury_swap"]["in"]}** instead of {r["quick_jury_swap"]["out"]}.']
    if r["plan_extras"]:
        out += ["Plan extras: " + "; ".join(r["plan_extras"]) + "."]
    if r["notes"]:
        out += ["", "Notes:"] + [f"- {n}" for n in r["notes"]]
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(__doc__.strip())
        sys.exit(0)

    def opt(name):
        if name in args:
            idx = args.index(name)
            if idx + 1 < len(args) and not args[idx + 1].startswith("--"):
                return args[idx + 1]
            raise SystemExit(f"Missing value for option '{name}'.")
        return None
    r = combine(load(), opt("--type"), opt("--length"), opt("--experience"), opt("--focus"), opt("--team"),
                opt("--path"))
    print(json.dumps(r, indent=2, ensure_ascii=False) if "--json" in args else to_markdown(r))


if __name__ == "__main__":
    main()
