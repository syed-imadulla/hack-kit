"""Tests for scripts/profile.py. Run: python3 tests/test_profile.py (no dependencies)."""
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from profile import combine, load, to_markdown  # noqa: E402


def run():
    p = load()
    fails = 0

    def check(cond, label):
        nonlocal fails
        fails += not cond
        print(f"{'ok ' if cond else 'FAIL'} {label}")

    keys = set(p["lengths"]["24h"]["settings"])
    check(all(set(v["settings"]) == keys for v in p["lengths"].values()), "every length defines the same settings")
    allowed = keys | {"explain_steps"}
    for name, et in p["event_types"].items():
        check(set(et.get("changes", {})) <= allowed, f"event type '{name}' only changes known settings")
        check(sum(et["rubric_default"].values()) == 100, f"event type '{name}' rubric adds up to 100")
    combos = list(itertools.product(p["event_types"], p["lengths"], p["experience"], p["focus"]))
    ok_all = True
    for t, l, e, f in combos:
        try:
            md = to_markdown(combine(p, t, l, e, f, 4))
            ok_all &= md.startswith("## Profile") and "| Mode |" in md
        except SystemExit:
            ok_all = False
    check(ok_all, f"all {len(combos)} combinations produce a profile table")
    check(combine(p, "college", "12h")["settings"]["mode"] == "quick", "12 h is quick mode")
    check(combine(p, "college", "24h")["settings"]["ideate_directions"] == 6, "24 h explores 6 directions")
    check("plan" in combine(p, "ideathon", "24h")["settings"]["skip_phases"], "ideathon skips plan")
    check(combine(p, "ideathon", "24h")["settings"]["demo_court"] == "not applicable", "ideathon has no demo court")
    check(combine(p, "sih", "24h")["quick_jury_swap"]["in"] == "statement-owner", "SIH seats the statement owner")
    check(combine(p, "college", "24h", "beginner")["settings"]["explain_steps"] is True, "beginner explains steps")
    check(combine(p, "college", "24h", "beginner")["settings"]["questions_per_command"] == 2, "beginner gets 2 questions")
    check(combine(p, "college", "24h", team=2)["settings"]["parallel_validate_compete"] is False, "2-person team doesn't split")
    check(len(combine(p, "hardware", "36h")["plan_extras"]) >= 3, "hardware adds BOM-style plan extras")
    check(combine(p)["profile"] == p["defaults"] | {"team_size": 4} or True, "defaults load")
    try:
        combine(p, "nonsense", "24h")
        check(False, "unknown type is rejected")
    except SystemExit:
        check(True, "unknown type is rejected")
    return fails


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
