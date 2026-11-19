"""Tests for scripts/tally.py. Run: python3 tests/test_tally.py (no dependencies)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from tally import tally  # noqa: E402


def load(name):
    with open(os.path.join(HERE, "fixtures", f"votes-{name}.json"), encoding="utf-8") as fh:
        return json.load(fh)


def run():
    cases = [
        ("pass", 12, "PASS"),
        ("revise", 12, "REVISE"),
        ("fail", 12, "FAIL"),
        ("inconclusive", 12, "INCONCLUSIVE"),
        ("weak", 12, "REVISE"),
        ("invalid", 12, "PASS"),
    ]
    failures = 0
    for name, expected, want in cases:
        res = tally(load(name), expected)
        ok = res["decision"] == want
        failures += not ok
        print(f"{'ok ' if ok else 'FAIL'} votes-{name}: {res['decision']} (want {want})")
    bad = tally(load("invalid"), 12)
    checks = [
        (bad["received_valid"] == 8, "invalid fixture keeps only 8 valid votes"),
        (len(bad["invalid"]) == 4, "invalid fixture reports 4 bad replies"),
        (any("duplicate juror" in i["problems"] for i in bad["invalid"]), "duplicate juror detected"),
        (tally(load("pass")[:7], 12)["decision"] == "INCONCLUSIVE", "too few votes is INCONCLUSIVE"),
        (tally(load("pass")[:6], 6)["decision"] == "PASS", "quick jury of 6 counts against 6"),
        (tally([], 12)["average_confidence"] is None, "no votes gives no average"),
    ]
    for ok, label in checks:
        failures += not ok
        print(f"{'ok ' if ok else 'FAIL'} {label}")
    return failures


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
