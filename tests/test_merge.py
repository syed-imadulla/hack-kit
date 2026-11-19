"""Tests for scripts/merge.py using standard unittest.

Run: python3 -m unittest discover -s tests
Or:  python3 tests/test_merge.py
"""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from merge import merge_project, parse_attribution, process_file_content, table_ok  # noqa: E402

SAMPLE_ASSUMPTIONS = """# ASSUMPTIONS — Test Project

## All assumptions
| # | Assumption | Importance | Team confidence | Evidence (label) | Kill test | Status | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Users have smartphones | high | high | [V] survey | collapses | validated | Verified from Census |
| 2 | Internet is available | medium | medium | [AI] | weakens | open | Needs check |

## Status history
| Date | # | Change |
|---|---|---|
"""

SAMPLE_STATE = """# STATE — Test Project

Schema version: 2
Last updated: 2026-11-19 10:00

| Field | Value |
|---|---|
| Event | Test Hackathon |

## Decisions log
| Time | Decision | Why | Rejected (and why) | By |
|---|---|---|---|---|
| 10:00 | Chose problem | Best fit | Others | Captain |
"""

SAMPLE_NON_NUMERIC_ID = """# TASKS — Test Tasks

## Task table
| ID | Task | Owner | Status |
|---|---|---|---|
| T1 | Setup repo | Alice | done |
| T2 | Build prototype | Bob | in progress |
"""


class TestMerge(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.folder = Path(self.test_dir) / ".hackathon"
        self.folder.mkdir()
        (self.folder / "ASSUMPTIONS.md").write_text(SAMPLE_ASSUMPTIONS, encoding="utf-8")
        (self.folder / "STATE.md").write_text(SAMPLE_STATE, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_clean_merge_new_row(self):
        pending = (
            "\n## Pending from Alice — 11:30 IST\n"
            "| | Power outages happen often | high | low | [?] | collapses | open | Ask 3 shopkeepers |\n"
        )
        (self.folder / "ASSUMPTIONS.md").write_text(SAMPLE_ASSUMPTIONS + pending, encoding="utf-8")

        success, res = merge_project(self.folder)
        self.assertTrue(success, f"Merge failed: {res}")
        self.assertEqual(res["total_added"], 1)
        self.assertEqual(res["total_conflicts"], 0)
        self.assertEqual(res["total_duplicates"], 0)

        updated = (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8")
        self.assertNotIn("## Pending from Alice", updated)
        self.assertIn("| 3 | Power outages happen often |", updated)
        self.assertFalse(table_ok(updated), "Table in updated file should be well-formed")

    def test_exact_duplicate_skip(self):
        pending = (
            "\n## Pending from Bob — 12:00 IST\n"
            "| 1 | Users have smartphones | high | high | [V] survey | collapses | validated | Verified from Census |\n"
        )
        (self.folder / "ASSUMPTIONS.md").write_text(SAMPLE_ASSUMPTIONS + pending, encoding="utf-8")

        success, res = merge_project(self.folder)
        self.assertTrue(success)
        self.assertEqual(res["total_added"], 0)
        self.assertEqual(res["total_duplicates"], 1)
        self.assertEqual(res["total_conflicts"], 0)

        updated = (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8")
        self.assertNotIn("## Pending from Bob", updated)
        self.assertEqual(updated.count("Users have smartphones"), 1)

    def test_conflict_detection_and_preservation(self):
        pending = (
            "\n## Pending from Charlie — 13:00 IST\n"
            "| 2 | Internet is available | medium | high | [T] Tested at venue | collapses | validated | Fast wifi here |\n"
        )
        (self.folder / "ASSUMPTIONS.md").write_text(SAMPLE_ASSUMPTIONS + pending, encoding="utf-8")

        success, res = merge_project(self.folder)
        self.assertTrue(success)
        self.assertEqual(res["total_conflicts"], 1)
        self.assertEqual(res["total_added"], 0)

        updated = (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8")
        self.assertNotIn("## Pending from Charlie", updated)
        self.assertIn("Fast wifi here [CONFLICT (Charlie — 13:00 IST)]", updated)
        self.assertIn("Needs check", updated)
        self.assertIn("CONFLICT", updated)
        self.assertFalse(table_ok(updated))

    def test_idempotency_repeated_execution(self):
        pending = (
            "\n## Pending from Dana — 14:00 IST\n"
            "| | Battery life is sufficient | low | high | [V] tests | weakens | validated | 8 hours tested |\n"
        )
        (self.folder / "ASSUMPTIONS.md").write_text(SAMPLE_ASSUMPTIONS + pending, encoding="utf-8")

        s1, r1 = merge_project(self.folder)
        self.assertTrue(s1)
        self.assertEqual(r1["total_added"], 1)
        content_after_run1 = (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8")

        s2, r2 = merge_project(self.folder)
        self.assertTrue(s2)
        self.assertEqual(r2.get("total_added", 0), 0)
        content_after_run2 = (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8")

        self.assertEqual(content_after_run1, content_after_run2)

    def test_dry_run_does_not_modify_disk(self):
        pending = (
            "\n## Pending from Eve — 15:00 IST\n"
            "| | Offline sync works | high | medium | [AI] | collapses | open | Build prototype |\n"
        )
        orig_content = SAMPLE_ASSUMPTIONS + pending
        (self.folder / "ASSUMPTIONS.md").write_text(orig_content, encoding="utf-8")

        success, res = merge_project(self.folder, dry_run=True)
        self.assertTrue(success)
        self.assertTrue(res.get("dry_run"))
        self.assertEqual(res["total_added"], 1)

        current_content = (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8")
        self.assertEqual(orig_content, current_content)

    def test_malformed_markdown_transactional_abort(self):
        broken_pending = (
            "\n## Pending from Frank — 16:00 IST\n"
            "| Broken row | missing | cell | columns | here |\n"
        )
        orig_content = SAMPLE_ASSUMPTIONS + broken_pending
        (self.folder / "ASSUMPTIONS.md").write_text(orig_content, encoding="utf-8")

        success, res = merge_project(self.folder)
        self.assertFalse(success)
        self.assertIn("error", res)

        current_content = (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8")
        self.assertEqual(orig_content, current_content)

    def test_multi_file_transactional_abort(self):
        valid_pending = (
            "\n## Pending from Grace — 17:00 IST\n"
            "| | Valid assumption | high | high | [V] | weakens | validated | ok |\n"
        )
        (self.folder / "ASSUMPTIONS.md").write_text(SAMPLE_ASSUMPTIONS + valid_pending, encoding="utf-8")

        compete_content = (
            "# COMPETE\n\n## Existing solutions\n"
            "| # | Name | Type |\n|---|---|---|\n| 1 | CompA | App |\n"
            "\n## Pending from Heidi — 17:05\n| Broken | Row |\n"
        )
        (self.folder / "COMPETE.md").write_text(compete_content, encoding="utf-8")

        success, res = merge_project(self.folder)
        self.assertFalse(success, "Merge must abort across all files if one file fails validation")

        self.assertEqual((self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8"), SAMPLE_ASSUMPTIONS + valid_pending)
        self.assertEqual((self.folder / "COMPETE.md").read_text(encoding="utf-8"), compete_content)

    def test_state_md_updated_on_merge(self):
        pending = (
            "\n## Pending from Ian — 18:00 IST\n"
            "| | Cloud costs are low | low | high | [V] pricing | minor | validated | AWS tier |\n"
        )
        (self.folder / "ASSUMPTIONS.md").write_text(SAMPLE_ASSUMPTIONS + pending, encoding="utf-8")

        success, _ = merge_project(self.folder)
        self.assertTrue(success)

        state_text = (self.folder / "STATE.md").read_text(encoding="utf-8")
        self.assertIn("Merged 1 pending row(s) from Ian", state_text)
        self.assertNotIn("Last updated: 2026-11-19 10:00", state_text)

    def test_interrupted_write_rollback_safety(self):
        pending = (
            "\n## Pending from Jack — 19:00 IST\n"
            "| | Local caching works | low | low | [?] | minor | open | test |\n"
        )
        orig_content = SAMPLE_ASSUMPTIONS + pending
        (self.folder / "ASSUMPTIONS.md").write_text(orig_content, encoding="utf-8")

        # Simulate exception during os.replace
        with patch("os.replace", side_effect=OSError("Simulated disk error during replacement")):
            success, res = merge_project(self.folder)
            self.assertFalse(success)
            self.assertIn("error", res)

        # File must remain untouched and temporary files cleaned up
        self.assertEqual((self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8"), orig_content)
        tmp_files = list(self.folder.glob("*.merge_tmp"))
        self.assertEqual(len(tmp_files), 0, "All temporary merge files must be cleaned up on failure")

    def test_non_sequential_id_table_preserves_raw_ids(self):
        pending = (
            "\n## Pending from Karen — 20:00 IST\n"
            "| T3 | Deploy web app | Karen | todo |\n"
        )
        (self.folder / "TASKS.md").write_text(SAMPLE_NON_NUMERIC_ID + pending, encoding="utf-8")

        success, res = merge_project(self.folder, target_file="TASKS.md")
        self.assertTrue(success)
        self.assertEqual(res["total_added"], 1)

        updated = (self.folder / "TASKS.md").read_text(encoding="utf-8")
        self.assertIn("| T3 | Deploy web app | Karen | todo |", updated)

    def test_author_timestamp_parsing_variations(self):
        cases = [
            ("Alice — 14:00 IST", ("Alice", "14:00 IST")),
            ("Bob – 14:00", ("Bob", "14:00")),
            ("Charlie - 14:00", ("Charlie", "14:00")),
            ("Dana", ("Dana", "")),
            ("Eve, Frank — Day 1 15:30", ("Eve, Frank", "Day 1 15:30")),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_attribution(raw), expected)

    def test_merge_with_specific_file_filter(self):
        # File 1 has pending
        (self.folder / "ASSUMPTIONS.md").write_text(
            SAMPLE_ASSUMPTIONS + "\n## Pending from Alice\n| | Power check | low | low | [?] | minor | open | note |\n",
            encoding="utf-8"
        )
        # File 2 has pending
        (self.folder / "TASKS.md").write_text(
            SAMPLE_NON_NUMERIC_ID + "\n## Pending from Bob\n| T3 | Test task | Bob | todo |\n",
            encoding="utf-8"
        )

        # Merge ONLY TASKS.md
        success, res = merge_project(self.folder, target_file="TASKS.md")
        self.assertTrue(success)

        # TASKS.md should be merged
        self.assertNotIn("## Pending from Bob", (self.folder / "TASKS.md").read_text(encoding="utf-8"))
        # ASSUMPTIONS.md should NOT be merged
        self.assertIn("## Pending from Alice", (self.folder / "ASSUMPTIONS.md").read_text(encoding="utf-8"))


class TestNoDataLoss(unittest.TestCase):
    """Regression tests for v1.2.2: nothing a teammate writes may disappear."""

    DOC = """# ASSUMPTIONS

| # | Assumption | Status |
|---|---|---|
| 1 | Docs cause rejections | open |
| 2 | Operators add a step | open |

## Pending from Priya — 14:10
| # | Assumption | Status |
|---|---|---|
| 1 | Docs cause rejections | validated |
| 3 | Families keep papers | open |

Priya: called 3 operators, 2 said docs.
"""

    def test_free_text_notes_are_kept(self):
        out, summary, errs = process_file_content(self.DOC, "ASSUMPTIONS.md")
        self.assertEqual(errs, [])
        self.assertIn("called 3 operators, 2 said docs", out)
        self.assertEqual(summary["notes_kept"], 1)

    def test_added_rows_keep_attribution(self):
        out, _, _ = process_file_content(self.DOC, "ASSUMPTIONS.md")
        self.assertIn("### From Priya — 14:10", out)
        self.assertIn("Rows added: Families keep papers", out)

    def test_teammate_id_kept_when_free(self):
        out, _, _ = process_file_content(self.DOC, "ASSUMPTIONS.md")
        self.assertIn("| 3 | Families keep papers | open |", out)

    def test_clashing_id_gets_next_free_number(self):
        doc = self.DOC.replace("| 3 | Families keep papers", "| 2 | Families keep papers")
        out, _, _ = process_file_content(doc, "ASSUMPTIONS.md")
        self.assertIn("| 3 | Families keep papers | open |", out)

    def test_notes_only_section_is_kept(self):
        doc = self.DOC.split("## Pending")[0] + "## Pending from Ravi\nOperator at Tumkur CSC says rush is 10-12.\n"
        out, _, errs = process_file_content(doc, "ASSUMPTIONS.md")
        self.assertEqual(errs, [])
        self.assertIn("Operator at Tumkur CSC says rush is 10-12.", out)
        self.assertNotIn("## Pending from", out)


if __name__ == "__main__":
    unittest.main()
