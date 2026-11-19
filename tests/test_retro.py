"""Tests for scripts/retro.py using standard unittest.

Run: python3 -m unittest discover -s tests
Or:  python3 tests/test_retro.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from merge import table_ok  # noqa: E402
from retro import (  # noqa: E402
    analyze_assumptions,
    analyze_court_trials,
    analyze_demo_ladder,
    analyze_pitch_drill,
    find_causal_connections,
    generate_retro_markdown,
)

ROOT = HERE.parent
CERT_EXAMPLE = ROOT / "examples" / "test-run-certificates" / ".hackathon"
OPD_EXAMPLE = ROOT / "examples" / "opd-saathi" / ".hackathon"


class TestRetro(unittest.TestCase):
    def test_complete_project_generates_all_10_sections(self):
        md = generate_retro_markdown(CERT_EXAMPLE)
        self.assertTrue(md.startswith("# RETRO — Mock Social Good Hack"))
        for sec_num in range(1, 11):
            self.assertIn(f"## {sec_num}.", md, f"Section {sec_num} should be present")

    def test_complete_project_tables_well_formed(self):
        md = generate_retro_markdown(CERT_EXAMPLE)
        bad_tables = table_ok(md)
        self.assertFalse(bad_tables, f"Generated RETRO.md has broken table rows: {bad_tables}")

    def test_incomplete_project_runs_gracefully(self):
        # opd-saathi has no DEMO.md, PLAN.md, or court/ trials (uses top-level VERDICT.md)
        md = generate_retro_markdown(OPD_EXAMPLE)
        self.assertTrue(md.startswith("# RETRO — OPD Saathi"))
        self.assertIn("## 1. Executive summary", md)
        self.assertIn("solution-trial: PASS", md)
        self.assertIn("No DEMO.md ladder available", md)
        self.assertIn("Task planning tables not available", md)
        bad_tables = table_ok(md)
        self.assertFalse(bad_tables, "Incomplete project tables must also be well-formed")

    def test_assumptions_analysis(self):
        assumptions_md = (CERT_EXAMPLE / "ASSUMPTIONS.md").read_text(encoding="utf-8")
        stats = analyze_assumptions(assumptions_md)
        self.assertIsNotNone(stats)
        self.assertEqual(stats["total"], 10)
        self.assertEqual(stats["collapses_total"], 2)
        self.assertEqual(stats["collapses_untested"], 2)
        self.assertEqual(stats["labels"]["[?]"], 2)
        self.assertEqual(stats["labels"]["[AI]"], 8)

    def test_demo_ladder_analysis_certificates(self):
        demo_md = (CERT_EXAMPLE / "DEMO.md").read_text(encoding="utf-8")
        stats = analyze_demo_ladder(demo_md)
        self.assertIsNotNone(stats)
        self.assertEqual(stats["total_features"], 9)
        self.assertEqual(stats["planned_build"], 8)
        self.assertEqual(stats["planned_mock"], 1)
        self.assertEqual(stats["planned_cut"], 0)
        self.assertEqual(stats["built"], 7)
        self.assertEqual(stats["not_implemented"], 1)
        self.assertEqual(stats["tested"], 7)
        self.assertEqual(stats["tested_v"], 7)
        self.assertEqual(stats["untested"], 2)
        self.assertEqual(stats["shown"], 7)
        self.assertEqual(stats["shown_full"], 5)
        self.assertEqual(stats["shown_partial"], 2)
        self.assertEqual(stats["not_shown"], 2)
        self.assertEqual(stats["mocked"], 3)
        self.assertEqual(stats["unmocked"], 6)

    def test_feature_ladder_combination_rules(self):
        # Test synthetic markdown with independent non-mutually-exclusive statuses
        synthetic_demo = """# DEMO Test

## Feature ladder
| Feature | Planned | Built (where) | Tested (how, result) | Shown in demo run | Mocked → disclosed in pitch? |
|---|---|---|---|---|---|
| F1 Built Untested Shown | Build | `app/f1.py` | Not tested | Yes | n/a |
| F2 Built Tested NotShown | Build | `app/f2.py` | [V] passes unit suite | No (CLI only) | unmocked |
| F3 Built Tested Shown Mocked | Build | `app/f3.py (text)` | [V] correct text | Partly | **TTS Mocked**: disclose |
| F4 Unbuilt Untested NotMocked | Build | **Not built**: deferred | — | No | Will build next |
| F5 PlannedMock Unbuilt NotShown | Mock | — | — | Planned as clip | Disclosed in plan ✓ |
"""
        stats = analyze_demo_ladder(synthetic_demo)
        self.assertEqual(stats["total_features"], 5)
        self.assertEqual(stats["planned_build"], 4)
        self.assertEqual(stats["planned_mock"], 1)
        self.assertEqual(stats["built"], 3)  # F1, F2, F3
        self.assertEqual(stats["not_implemented"], 1)  # F4 (F5 was planned mock)
        self.assertEqual(stats["tested"], 2)  # F2, F3
        self.assertEqual(stats["untested"], 3)  # F1, F4, F5
        self.assertEqual(stats["shown"], 2)  # F1 (full), F3 (partly)
        self.assertEqual(stats["not_shown"], 3)  # F2, F4, F5
        self.assertEqual(stats["mocked"], 2)  # F3 (TTS mocked), F5 (Planned mock)
        self.assertEqual(stats["unmocked"], 3)  # F1, F2, F4

    def test_court_trials_analysis(self):
        trials = analyze_court_trials(CERT_EXAMPLE / "court", open_collapses=2)
        trial_names = {t["name"] for t in trials}
        self.assertIn("demo-1", trial_names)
        self.assertIn("improve-r1", trial_names)
        self.assertIn("verify", trial_names)
        demo_trial = next(t for t in trials if t["name"] == "demo-1")
        self.assertEqual(demo_trial["decision"], "FAIL")
        improve_trial = next(t for t in trials if t["name"] == "improve-r1")
        self.assertEqual(improve_trial["decision"], "REVISE")
        verify_trial = next(t for t in trials if t["name"] == "verify")
        self.assertEqual(verify_trial["decision"], "INCONCLUSIVE")

    def test_court_trials_fallback_to_verdict_file(self):
        # opd-saathi has a single top-level VERDICT.md
        trials = analyze_court_trials(OPD_EXAMPLE / "court", verdict_path=OPD_EXAMPLE / "VERDICT.md")
        self.assertEqual(len(trials), 1)
        self.assertEqual(trials[0]["name"], "solution-trial")
        self.assertEqual(trials[0]["decision"], "PASS")

    def test_pitch_drill_analysis(self):
        pitch_md = (CERT_EXAMPLE / "PITCH.md").read_text(encoding="utf-8")
        stats = analyze_pitch_drill(pitch_md)
        self.assertIsNotNone(stats)
        self.assertEqual(stats["avg_honesty"], 1.75)
        self.assertGreaterEqual(len(stats["false_claims"]), 1)

    def test_causal_connections_rigor_and_tags(self):
        assumptions = analyze_assumptions((CERT_EXAMPLE / "ASSUMPTIONS.md").read_text(encoding="utf-8"))
        demo = analyze_demo_ladder((CERT_EXAMPLE / "DEMO.md").read_text(encoding="utf-8"))
        pitch_stats = analyze_pitch_drill((CERT_EXAMPLE / "PITCH.md").read_text(encoding="utf-8"))
        trials = analyze_court_trials(CERT_EXAMPLE / "court", open_collapses=2)

        # Mock plan_res with warning
        plan_res = {
            "critical_path": ["T1", "T2"],
            "critical_hours": 14.0,
            "load": {"a": 10.5, "b": 7.0},
            "warnings": ["Critical path is 14 h of 18 h to code freeze (78%): tight. Start the path first."]
        }

        connections = find_causal_connections(assumptions, demo, plan_res, trials, pitch_stats)
        categories = {c["category"] for c in connections}

        # Must distinguish Direct Cause from Contributing Factor / Correlation
        self.assertIn("[Direct Cause]", categories)
        self.assertIn("[Contributing Factor]", categories)

        for conn in connections:
            self.assertIn("category", conn)
            self.assertIn("finding", conn)
            self.assertIn("consequence", conn)
            self.assertIn("evidence", conn)
            # Ensure categories use exact bracketed tag
            self.assertTrue(conn["category"].startswith("[") and conn["category"].endswith("]"))

    def test_team_feedback_inclusion(self):
        md = generate_retro_markdown(CERT_EXAMPLE, feedback="Judges loved the regional language voice demo.")
        self.assertIn("## Team notes & feedback [T]", md)
        self.assertIn("Judges loved the regional language voice demo.", md)

    def test_write_flag_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / ".hackathon"
            shutil.copytree(CERT_EXAMPLE, dst)
            retro_file = dst / "RETRO.md"
            if retro_file.exists():
                retro_file.unlink()
            self.assertFalse(retro_file.exists())

            # Generate with write flag
            cmd = f"{sys.executable} {ROOT / 'scripts' / 'retro.py'} {dst} --write"
            code = os.system(cmd)
            self.assertEqual(code, 0)
            self.assertTrue(retro_file.is_file())
            content = retro_file.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("# RETRO — "))

    def test_json_output_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / ".hackathon"
            shutil.copytree(CERT_EXAMPLE, dst)
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "retro.py"), str(dst), "--json"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            data = json.loads(r.stdout)
            self.assertIn("assumptions", data)
            self.assertIn("demo", data)
            self.assertIn("trials", data)

    def test_cli_help(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "retro.py"), "--help"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("usage:", r.stdout.lower())
        self.assertIn("retrospective", r.stdout.lower())


class TestRetroHonesty(unittest.TestCase):
    """v1.2.2: retro may only report what the project files show."""

    def test_no_stock_mistakes_or_lessons_for_empty_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "STATE.md").write_text("# STATE — Empty\n\nSchema version: 2\n", encoding="utf-8")
            md = generate_retro_markdown(folder)
        self.assertNotIn("Writing pitch claims before running the demo check", md)
        self.assertNotIn("Evidence beats confidence", md)
        self.assertIn("No mistakes could be identified", md)
        self.assertIn("Not enough recorded evidence to draw lessons", md)
        self.assertEqual(md.count("general practice, not from this project's data"), 3)

    def test_demo_fail_uses_real_counts(self):
        md = generate_retro_markdown(CERT_EXAMPLE)
        self.assertIn("NOT GUILTY 0 · GUILTY 7 · INSUFFICIENT EVIDENCE 0", md)
        self.assertNotIn("due to simulated components", md)

    def test_open_collapses_without_capped_trial_is_a_risk_not_a_cause(self):
        assumptions = {"items": [{"assumption": "Users will call", "is_collapses": True, "status": "open"}]}
        trials = [{"name": "verify", "decision": "FAIL", "criticisms": [], "counts": (2, 9, 1), "capped": False, "reasons": []}]
        conns = find_causal_connections(assumptions, None, None, trials, None)
        self.assertEqual(conns[0]["category"], "[Open risk]")
        trials[0].update(decision="REVISE", capped=True)
        conns = find_causal_connections(assumptions, None, None, trials, None)
        self.assertEqual(conns[0]["category"], "[Direct Cause]")

    def test_no_mid_word_truncation(self):
        from retro import short
        self.assertEqual(short("Record real Kannada TTS clips for each flag and play one", 40), "Record real Kannada TTS clips for each…")
        self.assertEqual(short("short text", 40), "short text")

    def test_unbuilt_feature_is_not_called_real(self):
        md = generate_retro_markdown(CERT_EXAMPLE)
        row = next(l for l in md.splitlines() if l.startswith("| Watched scan folder"))
        self.assertNotIn("Real", row)

    def test_missing_honesty_score_is_not_invented(self):
        trials = []
        drill = {"avg_score": None, "avg_honesty": None, "false_claims": ["Built: watcher"]}
        conns = find_causal_connections(None, None, None, trials, drill)
        self.assertNotIn("1.75", conns[0]["consequence"])
        self.assertIn("No drill honesty score", conns[0]["consequence"])

    def test_starter_project_without_trial(self):
        """A starter-path project: plan done, no trial, assumptions table without its heading."""
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp)
            (f / "STATE.md").write_text("# STATE\n\n> Summary: x · next: <command>\n\n| # | Phase | Status | When | Notes |\n|---|---|---|---|---|\n| 11 | plan | done | | |\n| 13 | pitch | next | | |\n", encoding="utf-8")
            (f / "ASSUMPTIONS.md").write_text("# A\n\n| # | Assumption | Kill test | Evidence | Status |\n|---|---|---|---|---|\n| 1 | Warden refills | collapses | [?] | open |\n", encoding="utf-8")
            (f / "PLAN.md").write_text("# PLAN\n\n## Team\n| Member | Skills | Hours available |\n|---|---|---|\n| a | x | 5 |\n\nHours until code freeze: 10\n\n## Tasks\n| ID | Task | Owner | Skills needed | Hours | Depends on | Status |\n|---|---|---|---|---|---|---|\n| T1 | Build | a | x | 2 | — | todo |\n", encoding="utf-8")
            md = generate_retro_markdown(f)
        self.assertNotIn("<command>", md)
        self.assertNotIn("before /hack:plan or /hack:verify were run", md)
        self.assertIn("Warden refills", md)


def run():
    suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(c) for c in (TestRetro, TestRetroHonesty)])
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return len(res.failures) + len(res.errors)


if __name__ == "__main__":
    unittest.main()
