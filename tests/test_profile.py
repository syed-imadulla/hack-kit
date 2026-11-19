"""Tests for scripts/profile.py.

Run: python3 -m unittest discover -s tests
Or:  python3 tests/test_profile.py
"""
import itertools
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from profile import combine, load, to_markdown  # noqa: E402


class TestProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles_data = load()

    def test_lengths_define_same_settings_keys(self):
        p = self.profiles_data
        keys = set(p["lengths"]["24h"]["settings"])
        for length_name, length_cfg in p["lengths"].items():
            self.assertEqual(set(length_cfg["settings"]), keys, f"length '{length_name}' should define the same settings")

    def test_event_type_college_settings_and_rubric(self):
        p = self.profiles_data
        allowed = set(p["lengths"]["24h"]["settings"]) | {"explain_steps"}
        et = p["event_types"]["college"]
        self.assertTrue(set(et.get("changes", {})) <= allowed)
        self.assertEqual(sum(et["rubric_default"].values()), 100)

    def test_event_type_sih_settings_and_rubric(self):
        p = self.profiles_data
        allowed = set(p["lengths"]["24h"]["settings"]) | {"explain_steps"}
        et = p["event_types"]["sih"]
        self.assertTrue(set(et.get("changes", {})) <= allowed)
        self.assertEqual(sum(et["rubric_default"].values()), 100)

    def test_event_type_aiml_settings_and_rubric(self):
        p = self.profiles_data
        allowed = set(p["lengths"]["24h"]["settings"]) | {"explain_steps"}
        et = p["event_types"]["ai-ml"]
        self.assertTrue(set(et.get("changes", {})) <= allowed)
        self.assertEqual(sum(et["rubric_default"].values()), 100)

    def test_event_type_ideathon_settings_and_rubric(self):
        p = self.profiles_data
        allowed = set(p["lengths"]["24h"]["settings"]) | {"explain_steps"}
        et = p["event_types"]["ideathon"]
        self.assertTrue(set(et.get("changes", {})) <= allowed)
        self.assertEqual(sum(et["rubric_default"].values()), 100)

    def test_event_type_hardware_settings_and_rubric(self):
        p = self.profiles_data
        allowed = set(p["lengths"]["24h"]["settings"]) | {"explain_steps"}
        et = p["event_types"]["hardware"]
        self.assertTrue(set(et.get("changes", {})) <= allowed)
        self.assertEqual(sum(et["rubric_default"].values()), 100)

    def test_event_type_corporate_settings_and_rubric(self):
        p = self.profiles_data
        allowed = set(p["lengths"]["24h"]["settings"]) | {"explain_steps"}
        et = p["event_types"]["corporate"]
        self.assertTrue(set(et.get("changes", {})) <= allowed)
        self.assertEqual(sum(et["rubric_default"].values()), 100)

    def test_all_288_combinations_produce_profile_table(self):
        p = self.profiles_data
        combos = list(itertools.product(p["event_types"], p["lengths"], p["experience"], p["focus"]))
        self.assertEqual(len(combos), 288)
        for t, l, e, f in combos:
            res = combine(p, t, l, e, f, 4)
            md = to_markdown(res)
            self.assertTrue(md.startswith("## Profile"))
            self.assertIn("| Mode |", md)

    def test_12h_is_quick_mode(self):
        p = self.profiles_data
        self.assertEqual(combine(p, "college", "12h")["settings"]["mode"], "quick")

    def test_24h_explores_6_directions(self):
        p = self.profiles_data
        self.assertEqual(combine(p, "college", "24h")["settings"]["ideate_directions"], 6)

    def test_ideathon_skips_plan(self):
        p = self.profiles_data
        self.assertIn("plan", combine(p, "ideathon", "24h")["settings"]["skip_phases"])

    def test_ideathon_has_no_demo_court(self):
        p = self.profiles_data
        self.assertEqual(combine(p, "ideathon", "24h")["settings"]["demo_court"], "not applicable")

    def test_sih_seats_statement_owner(self):
        p = self.profiles_data
        self.assertEqual(combine(p, "sih", "24h")["quick_jury_swap"]["in"], "statement-owner")

    def test_beginner_explains_steps(self):
        p = self.profiles_data
        self.assertTrue(combine(p, "college", "24h", "beginner")["settings"]["explain_steps"])

    def test_beginner_gets_2_questions(self):
        p = self.profiles_data
        self.assertEqual(combine(p, "college", "24h", "beginner")["settings"]["questions_per_command"], 2)

    def test_2_person_team_does_not_split(self):
        p = self.profiles_data
        self.assertFalse(combine(p, "college", "24h", team=2)["settings"]["parallel_validate_compete"])

    def test_hardware_adds_bom_plan_extras(self):
        p = self.profiles_data
        self.assertGreaterEqual(len(combine(p, "hardware", "36h")["plan_extras"]), 3)

    def test_defaults_load(self):
        p = self.profiles_data
        self.assertEqual(combine(p)["profile"]["event_type"], p["defaults"]["event_type"])
        self.assertEqual(combine(p)["profile"]["length"], p["defaults"]["length"])

    def test_unknown_type_is_rejected(self):
        p = self.profiles_data
        with self.assertRaises(SystemExit):
            combine(p, "nonsense", "24h")

    def test_unknown_length_is_rejected(self):
        p = self.profiles_data
        with self.assertRaises(SystemExit):
            combine(p, "college", "99h")

    def test_unknown_experience_is_rejected(self):
        p = self.profiles_data
        with self.assertRaises(SystemExit):
            combine(p, "college", "24h", "expert")

    def test_unknown_focus_is_rejected(self):
        p = self.profiles_data
        with self.assertRaises(SystemExit):
            combine(p, "college", "24h", "mixed", "random")

    def test_invalid_team_size_rejected(self):
        p = self.profiles_data
        with self.assertRaises(SystemExit):
            combine(p, "college", "24h", team="not-a-number")

    def test_json_output_structure(self):
        p = self.profiles_data
        r = combine(p, "college", "24h", "mixed", "balanced", 4)
        self.assertIn("profile", r)
        self.assertIn("settings", r)
        self.assertIn("rubric_default", r)
        self.assertIn("scoring_weights", r)


def run():
    suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(c) for c in (TestProfile, TestStarterPath)])
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return len(res.failures) + len(res.errors)


class TestStarterPath(unittest.TestCase):
    """v1.3: the starter path for first-time teams."""

    @classmethod
    def setUpClass(cls):
        cls.p = load()

    def test_beginners_get_starter_by_default(self):
        r = combine(self.p, experience="beginner")
        self.assertEqual(r["path"]["name"], "starter")
        self.assertEqual(r["path"]["commands"], ["start", "pick", "ideate", "plan", "pitch"])

    def test_others_get_full_by_default(self):
        for exp in ("mixed", "advanced"):
            self.assertEqual(combine(self.p, experience=exp)["path"]["name"], "full")

    def test_explicit_path_wins(self):
        self.assertEqual(combine(self.p, experience="beginner", path="full")["path"]["name"], "full")
        self.assertEqual(combine(self.p, experience="advanced", path="starter")["path"]["name"], "starter")

    def test_every_phase_is_run_folded_or_explained(self):
        full = self.p["paths"]["full"]["commands"]
        for et in self.p["event_types"]:
            for length in self.p["lengths"]:
                r = combine(self.p, event_type=et, length=length, path="starter")
                pa = r["path"]
                self.assertLessEqual(len(pa["commands"]), 5)
                for ph in full:
                    covered = ph in pa["commands"] or ph in pa["folded"] or ph in pa["skipped"] \
                        or ph == pa["optional_end"] or ph in self.p["event_types"][et].get("changes", {}).get("skip_phases", [])
                    self.assertTrue(covered, f"{et}/{length}: phase {ph} is lost")
                for into in pa["folded"].values():
                    self.assertIn(into, pa["commands"], f"{et}: folded into a command not on the path")

    def test_ideathon_starter_locks_in_lock(self):
        pa = combine(self.p, event_type="ideathon", path="starter")["path"]
        self.assertNotIn("plan", pa["commands"])
        self.assertIn("lock", pa["commands"])
        self.assertEqual(pa["folded"]["stress"], "lock")

    def test_starter_caps_never_raise_settings(self):
        for length in self.p["lengths"]:
            base = combine(self.p, length=length, path="full")["settings"]
            st = combine(self.p, length=length, path="starter")["settings"]
            for k in ("pick_trials", "ideate_directions", "questions_per_command", "drill_questions"):
                self.assertLessEqual(st[k], base[k], f"{length}: {k}")
            self.assertEqual(st["pick_jury"], 7)

    def test_markdown_lists_commands_and_folds(self):
        md = to_markdown(combine(self.p, experience="beginner"))
        self.assertIn("/hack:start → /hack:pick → /hack:ideate → /hack:plan → /hack:pitch", md)
        self.assertIn("decode → /hack:pick", md)
        self.assertIn("--path starter", md)

    def test_unknown_path_rejected(self):
        with self.assertRaises(SystemExit):
            combine(self.p, path="express")


if __name__ == "__main__":
    unittest.main()
