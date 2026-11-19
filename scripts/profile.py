#!/usr/bin/env python3
"""Combine a Hack Kit event profile into one table of effective settings.

Usage:
  python3 profile.py [--type college|sih|ai-ml|ideathon|hardware|corporate]
                     [--length 12h|24h|36h|48h+] [--experience beginner|mixed|advanced]
                     [--focus balanced|technical|innovation-impact|business] [--team N] [--json]

Missing options use the defaults in skills/hack-kit/profiles.json. Output is a Markdown block
for STATE.md ("## Profile"), or JSON with --json. Order: length → event type → experience → focus.
"""
import json
import sys
from pathlib import Path

PROFILES = Path(__file__).resolve().parent.parent / "skills" / "hack-kit" / "profiles.json"


def load():
    return json.loads(PROFILES.read_text(encoding="utf-8"))


def combine(p, event_type=None, length=None, experience=None, focus=None, team=None):
    d = p["defaults"]
    event_type, length = event_type or d["event_type"], length or d["length"]
    experience, focus = experience or d["experience"], focus or d["focus"]
    team = int(team or d["team_size"])
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

    notes = list(et.get("notes", [])) + list(p["experience"][experience].get("notes", [])) + \
        list(p["focus"][focus].get("notes", []))
    return {
        "profile": {"event_type": event_type, "length": length, "experience": experience,
                    "focus": focus, "team_size": team},
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
    rows = [
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
        ("Skip phases", ", ".join(s["skip_phases"]) or "none"),
        ("Target: idea locked within", f'{s["lock_target_minutes"]} min'),
    ]
    out = ["## Profile", "",
           f'**{lb["event_type"]}** · {lb["length"]} · team of {pr["team_size"]} · {lb["experience"]} · focus: {lb["focus"]}',
           f'`--type {pr["event_type"]} --length {pr["length"]} --experience {pr["experience"]} --focus {pr["focus"]} --team {pr["team_size"]}`',
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

    def opt(name):
        return args[args.index(name) + 1] if name in args else None
    r = combine(load(), opt("--type"), opt("--length"), opt("--experience"), opt("--focus"), opt("--team"))
    print(json.dumps(r, indent=2, ensure_ascii=False) if "--json" in args else to_markdown(r))


if __name__ == "__main__":
    main()
