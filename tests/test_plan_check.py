"""Tests for scripts/plan_check.py.

Run: python3 -m unittest discover -s tests
Or:  python3 tests/test_plan_check.py
"""
import os
import sys
import unittest

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


class TestPlanCheck(unittest.TestCase):
    def test_good_plan_has_no_errors(self):
        g = check(GOOD)
        self.assertFalse(g["errors"])

    def test_critical_path_identification(self):
        g = check(GOOD)
        self.assertEqual(g["critical_path"], ["T3", "T4", "T5"])

    def test_critical_path_hours_calculation(self):
        g = check(GOOD)
        self.assertEqual(g["critical_hours"], 11)

    def test_integration_points_found(self):
        g = check(GOOD)
        self.assertIn("T4", g["integration_points"])
        self.assertIn("T5", g["integration_points"])

    def test_no_overload_in_good_plan(self):
        g = check(GOOD)
        self.assertFalse(any("Overload" in w for w in g["warnings"]))

    def test_overload_detected(self):
        o = check(OVER)
        self.assertTrue(any("Overload: a" in w for w in o["warnings"]))

    def test_overload_suggests_spare_hours(self):
        o = check(OVER)
        self.assertTrue(any("spare" in w for w in o["warnings"]))

    def test_dependency_loop_detected(self):
        l = check(LOOP)
        self.assertTrue(any("loop" in e.lower() for e in l["errors"]))

    def test_skill_gap_detected(self):
        gp = check(GAP)
        self.assertTrue(any("may lack ai" in w for w in gp["warnings"]))

    def test_unassigned_task_detected(self):
        gp = check(GAP)
        self.assertTrue(any("no owner" in w for w in gp["warnings"]))

    def test_unknown_dependency_detected(self):
        gp = check(GAP)
        self.assertTrue(any("unknown task T9" in e for e in gp["errors"]))

    def test_critical_path_vs_freeze_checked(self):
        t = check(TIGHT)
        self.assertTrue(any("tight" in w or "no slack" in w for w in t["warnings"]))

    def test_shared_task_any_owners_skill_counts(self):
        shared = GOOD.replace("| T8 | Seeded scans | D | design | 2 | — | todo |", "| T8 | Seeded scans | D, A | design | 2 | — | todo |")
        self.assertFalse(any("T8" in w and "lack" in w for w in check(shared)["warnings"]))

    def test_maybe_tasks_not_counted_in_load(self):
        maybe = GOOD.replace("| T7 | Deck | D | pitch | 6 | — | todo |", "| T7 | Deck | D | pitch | 6 | — | maybe |")
        mc = check(maybe)
        self.assertIn("T7", mc["conditional"])
        self.assertEqual(mc["load"].get("d", 0), 2)

    def test_missing_task_table_is_error(self):
        self.assertTrue(check("no tables here")["errors"])

    def test_markdown_output(self):
        g = check(GOOD)
        self.assertTrue(to_md(g).startswith("## Plan check"))

    def test_no_team_table_warning(self):
        tasks_only = GOOD[len(TEAM):]
        res = check(tasks_only)
        self.assertTrue(any("No '## Team' table" in w for w in res["warnings"]))


def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlanCheck)
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return len(res.failures) + len(res.errors)


if __name__ == "__main__":
    unittest.main()
