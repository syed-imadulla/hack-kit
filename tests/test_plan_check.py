"""Tests for scripts/plan_check.py. Run: python3 tests/test_plan_check.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from plan_check import check, to_md  # noqa: E402

TEAM = """## Team
| Member | Skills | Hours available |
|---|---|---|
| A | backend, python | 14 |
| B | frontend, react | 14 |
| C | ai, python, speech | 14 |
| D | design, pitch | 12 |

Hours until code freeze: 18
"""

GOOD = TEAM + """
## Tasks
| ID | Task | Owner | Skills needed | Hours | Depends on | Status |
|---|---|---|---|---|---|---|
| T1 | Folder watcher | A | backend | 3 | — | todo |
| T2 | Operator screen | B | frontend | 4 | — | todo |
| T3 | Vision extraction | C | ai | 4 | — | todo |
| T4 | Check engine | A | backend | 4 | T1, T3 | todo |
| T5 | Wire screen to engine | B | frontend | 3 | T2, T4 | todo |
| T6 | Kannada TTS | C | speech | 3 | T4 | todo |
| T7 | Deck | D | pitch | 6 | — | todo |
| T8 | Seeded scans | D | design | 2 | — | todo |
"""

OVER = TEAM.replace("| 14 |\n| B", "| 6 |\n| B", 1) + GOOD[len(TEAM):]
LOOP = TEAM + """
## Tasks
| ID | Task | Owner | Skills needed | Hours | Depends on | Status |
|---|---|---|---|---|---|---|
| T1 | A | A | backend | 2 | T2 | todo |
| T2 | B | B | frontend | 2 | T1 | todo |
"""
GAP = TEAM + """
## Tasks
| ID | Task | Owner | Skills needed | Hours | Depends on | Status |
|---|---|---|---|---|---|---|
| T1 | Train model | D | ai | 5 | — | todo |
| T2 | Something | | backend | 2 | T9 | todo |
"""
TIGHT = TEAM.replace("Hours until code freeze: 18", "Hours until code freeze: 10") + GOOD[len(TEAM):]


def run():
    fails = 0

    def ok(c, label):
        nonlocal fails
        fails += not c
        print(f"{'ok ' if c else 'FAIL'} {label}")
    g = check(GOOD)
    ok(not g["errors"], "good plan has no errors")
    ok(g["critical_path"] == ["T3", "T4", "T5"], f"critical path T3→T4→T5 ({g['critical_path']})")
    ok(g["critical_hours"] == 11, "critical path is 11 h")
    ok("T4" in g["integration_points"] and "T5" in g["integration_points"], "integration points found")
    ok(not any("Overload" in w for w in g["warnings"]), "no overload in good plan")
    ok(any("Overload: a" in w for w in check(OVER)["warnings"]), "overload detected")
    ok(any("loop" in e.lower() for e in check(LOOP)["errors"]), "dependency loop detected")
    gp = check(GAP)
    ok(any("may lack ai" in w for w in gp["warnings"]), "skill gap detected")
    ok(any("no owner" in w for w in gp["warnings"]), "unassigned task detected")
    ok(any("unknown task T9" in e for e in gp["errors"]), "unknown dependency detected")
    ok(any("tight" in w or "no slack" in w for w in check(TIGHT)["warnings"]), "critical path vs freeze checked")
    shared = GOOD.replace("| T8 | Seeded scans | D | design | 2 | — | todo |", "| T8 | Seeded scans | D, A | design | 2 | — | todo |")
    ok(not any("T8" in w and "lack" in w for w in check(shared)["warnings"]), "shared task: any owner's skill counts")
    maybe = GOOD.replace("| T7 | Deck | D | pitch | 6 | — | todo |", "| T7 | Deck | D | pitch | 6 | — | maybe |")
    mc = check(maybe)
    ok("T7" in mc["conditional"] and mc["load"].get("d", 0) == 2, "maybe tasks aren't counted in load")
    ok(any("spare" in w for w in check(OVER)["warnings"]), "overload suggests who has spare hours")
    ok(check("no tables here")["errors"], "missing task table is an error")
    ok(to_md(g).startswith("## Plan check"), "markdown output")
    return fails


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
