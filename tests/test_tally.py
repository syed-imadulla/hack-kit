"""Tests for scripts/tally.py.

Run: python3 -m unittest discover -s tests
Or:  python3 tests/test_tally.py
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from tally import tally  # noqa: E402


def load(name):
    with open(os.path.join(HERE, "fixtures", f"votes-{name}.json"), encoding="utf-8") as fh:
        return json.load(fh)


class TestTally(unittest.TestCase):
    # --- 8 Fixture Decision Tests ---
    def test_fixture_votes_pass(self):
        self.assertEqual(tally(load("pass"), 12)["decision"], "PASS")

    def test_fixture_votes_revise(self):
        self.assertEqual(tally(load("revise"), 12)["decision"], "REVISE")

    def test_fixture_votes_fail(self):
        self.assertEqual(tally(load("fail"), 12)["decision"], "FAIL")

    def test_fixture_votes_inconclusive(self):
        self.assertEqual(tally(load("inconclusive"), 12)["decision"], "INCONCLUSIVE")

    def test_fixture_votes_weak(self):
        self.assertEqual(tally(load("weak"), 12)["decision"], "REVISE")

    def test_fixture_votes_invalid(self):
        self.assertEqual(tally(load("invalid"), 12)["decision"], "PASS")

    def test_fixture_votes_quick_two_abstain(self):
        self.assertEqual(tally(load("quick-two-abstain"), 6)["decision"], "REVISE")

    def test_fixture_votes_quick_snippets_only(self):
        self.assertEqual(tally(load("quick-snippets-only"), 6)["decision"], "INCONCLUSIVE")

    # --- 10 Detailed Rule & Edge Case Tests ---
    def test_invalid_fixture_keeps_only_8_valid_votes(self):
        bad = tally(load("invalid"), 12)
        self.assertEqual(bad["received_valid"], 8)

    def test_invalid_fixture_reports_4_bad_replies(self):
        bad = tally(load("invalid"), 12)
        self.assertEqual(len(bad["invalid"]), 4)

    def test_duplicate_juror_detected(self):
        bad = tally(load("invalid"), 12)
        self.assertTrue(any("duplicate juror" in i["problems"] for i in bad["invalid"]))

    def test_too_few_votes_is_inconclusive(self):
        self.assertEqual(tally(load("pass")[:7], 12)["decision"], "INCONCLUSIVE")

    def test_quick_jury_of_6_counts_against_6(self):
        self.assertEqual(tally(load("pass")[:6], 6)["decision"], "PASS")

    def test_no_votes_gives_no_average(self):
        self.assertIsNone(tally([], 12)["average_confidence"])

    def test_pass_capped_to_revise_while_collapses_open(self):
        self.assertEqual(tally(load("pass"), 12, open_collapses=2)["decision"], "REVISE")

    def test_cap_never_makes_verdict_more_lenient(self):
        self.assertEqual(tally(load("fail"), 12, open_collapses=2)["decision"], "FAIL")

    def test_synonyms_normalized_not_rejected(self):
        normalized = [dict(v, evidence_strength="Moderate", vote=" guilty ") for v in load("fail")]
        self.assertEqual(tally(normalized, 12)["decision"], "FAIL")

    def test_unknown_wording_still_rejected(self):
        unknown = [dict(v, evidence_strength="kinda") for v in load("pass")]
        self.assertEqual(tally(unknown, 12)["decision"], "INCONCLUSIVE")

    # --- Additional Edge Cases ---
    def test_fix_categorization_by_impact(self):
        res = tally(load("pass"), 12)
        self.assertIn("fixes_by_impact", res)
        for impact in res["fixes_by_impact"]:
            self.assertIn(impact, {"high", "medium", "low"})

    def test_vote_counts_breakdown(self):
        res = tally(load("pass"), 12)
        self.assertEqual(res["not_guilty"], 10)
        self.assertEqual(res["guilty"], 2)
        self.assertEqual(res["insufficient_evidence"], 0)


def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTally)
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return len(res.failures) + len(res.errors)


if __name__ == "__main__":
    unittest.main()
