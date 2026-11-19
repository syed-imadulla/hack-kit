#!/usr/bin/env python3
"""Check a team's .hackathon/ folder for common problems. No dependencies.

Usage: python3 lint_project.py [.hackathon]

Checks: STATE.md schema version · broken Markdown tables · unlabelled numbers in key files ·
"collapses" assumptions still open · claims marked validated without [V]/[T] evidence ·
DEMO.md mock disclosures that aren't true yet.
Prints warnings; exit code 1 only if a file is unreadable or a table is broken.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check import table_ok  # noqa: E402


def main():
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".hackathon")
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}")
    errors, warnings = 0, []
    for f in sorted(folder.glob("*.md")):
        if f.name.startswith(("FINAL", "BRIEF")):
            continue
        text = f.read_text(encoding="utf-8")
        bad = table_ok(text)
        if bad:
            errors += 1
            print(f"✗ {f.name}: broken table row(s): {bad[0]}")
    for f in sorted(folder.glob("*.md")):
        if f.name.startswith(("FINAL", "BRIEF")):
            continue
        text = f.read_text(encoding="utf-8")
        pend = re.findall(r"^## Pending from ([^\n]+)", text, re.M)
        if pend:
            warnings.append(f"{f.name}: {len(pend)} pending section(s) not merged ({', '.join(pend)}): run /hack:status --merge")
        if re.search(r"^.*\bCONFLICT\b", text, re.M) and f.name != "STATE.md":
            warnings.append(f"{f.name}: unresolved CONFLICT marker")
    state = folder / "STATE.md"
    if state.exists() and "Schema version: 2" not in state.read_text(encoding="utf-8"):
        warnings.append("STATE.md is schema 1: run any /hack: command to upgrade it")
    a = folder / "ASSUMPTIONS.md"
    if a.exists():
        rows = [r for r in a.read_text(encoding="utf-8").splitlines() if r.startswith("| ") and "collapses" in r]
        open_c = [r for r in rows if re.search(r"\| (open|testing) \|", r) and ("[?]" in r or "[AI]" in r)]
        if open_c:
            warnings.append(f'{len(open_c)} "collapses" assumption(s) still untested: pass --open-collapses {len(open_c)} to tally.py')
        for r in a.read_text(encoding="utf-8").splitlines():
            if r.startswith("| ") and "| validated |" in r and "[V]" not in r and "[T]" not in r:
                warnings.append(f"Validated without [V]/[T] evidence: {r[:70]}…")
    d = folder / "DEMO.md"
    if d.exists():
        sec = d.read_text(encoding="utf-8").split("## What we'll say about mocks", 1)
        if len(sec) == 2:
            for r in sec[1].splitlines():
                cells = [c.strip() for c in r.strip("|").split("|")]
                if r.startswith("| ") and len(cells) >= 3 and re.match(r"(no|❌|not yet)", cells[-1], re.I):
                    warnings.append(f"DEMO.md: mock disclosure not true yet (fix it or reword it): {cells[0][:60]}")
    for name in ("CORE.md", "PITCH.md", "SUMMARY.md"):
        p = folder / name
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if re.search(r"(Problem|Innovation|Feasibility|Impact|Presentation|Technical|Business)\b[^|%.]{0,12}\d+\s?%", line):
                continue  # rubric weights, not claims
            if re.search(r"\b\d+(\.\d+)?\s?%", line) and not re.search(r"\[(V|T|AI|\?)\]|\(target\)|target|\]\(http", line, re.I):
                warnings.append(f"{name}: number without a label or source: {line.strip()[:70]}")
    for w in warnings:
        print(f"! {w}")
    print(f"{'OK' if not errors else str(errors) + ' error(s)'} · {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
