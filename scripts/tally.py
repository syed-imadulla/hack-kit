#!/usr/bin/env python3
"""Count Hack Court juror votes reliably.

Usage:
  python3 tally.py <votes.json> [--expected 12] [--open-collapses N] [--json]

--open-collapses N: how many "collapses" assumptions in ASSUMPTIONS.md are still open
(evidence [?] or [AI]). If N > 0, a PASS becomes REVISE: never pass an idea whose
killer assumptions are untested.

votes.json is a JSON list of juror replies (raw, as received). Each valid reply looks like:
  {"juror": "...", "vote": "GUILTY" | "NOT GUILTY" | "INSUFFICIENT EVIDENCE",
   "confidence": 1-10, "evidence_strength": "strong|medium|weak|none",
   "reason": "...", "weakest_assumption": "...", "missing_info": "...",
   "fix": {"change": "...", "impact": "high|medium|low", "effort": "high|medium|low"}}

Invalid or duplicate replies are reported and left out of the count. Nothing is invented.
The judge's decision rule (see skills/hack-court/SKILL.md):
  INCONCLUSIVE  fewer than 2/3 of expected jurors gave valid votes, or
                INSUFFICIENT EVIDENCE votes are MORE than 1/3 of valid votes
  FAIL          GUILTY votes outnumber NOT GUILTY votes
  PASS          NOT GUILTY is at least 75% of ALL valid votes (abstentions count against a pass)
                and fewer than half of the votes rest on weak or no evidence
  REVISE        anything else
"""
import json
import sys

VOTES = {"GUILTY", "NOT GUILTY", "INSUFFICIENT EVIDENCE"}
LEVELS = {"high", "medium", "low"}
STRENGTH = {"strong", "medium", "weak", "none"}
# Harmless wording differences jurors often use. Mapped in memory only;
# votes-raw.json is never edited.
SYNONYMS = {"moderate": "medium", "med": "medium", "mid": "medium",
            "not guilty": "NOT GUILTY", "guilty": "GUILTY",
            "insufficient evidence": "INSUFFICIENT EVIDENCE"}


def normalize(reply):
    """Return a copy with case, spaces and common synonyms fixed (vote, strength, fix levels)."""
    if not isinstance(reply, dict):
        return reply
    r = dict(reply)

    def norm(v, upper=False):
        if not isinstance(v, str):
            return v
        k = " ".join(v.strip().replace("_", " ").split()).lower()
        k = SYNONYMS.get(k, k)
        return k.upper() if upper else k

    r["vote"] = norm(r.get("vote"), upper=True)
    r["evidence_strength"] = norm(r.get("evidence_strength"))
    if isinstance(r.get("fix"), dict):
        f = dict(r["fix"])
        f["impact"], f["effort"] = norm(f.get("impact")), norm(f.get("effort"))
        r["fix"] = f
    return r


def check(reply):
    """Return a list of problems with one juror reply (empty list = valid)."""
    p = []
    if not isinstance(reply, dict):
        return ["not a JSON object"]
    if not isinstance(reply.get("juror"), str) or not reply["juror"].strip():
        p.append("missing juror name")
    if reply.get("vote") not in VOTES:
        p.append("vote must be GUILTY, NOT GUILTY or INSUFFICIENT EVIDENCE")
    c = reply.get("confidence")
    if not isinstance(c, int) or isinstance(c, bool) or not 1 <= c <= 10:
        p.append("confidence must be a whole number 1-10")
    if reply.get("evidence_strength") not in STRENGTH:
        p.append("evidence_strength must be strong, medium, weak or none")
    for k in ("reason", "weakest_assumption", "missing_info"):
        if not isinstance(reply.get(k), str):
            p.append(f"missing {k}")
    fix = reply.get("fix")
    if not isinstance(fix, dict) or not isinstance(fix.get("change"), str) \
            or fix.get("impact") not in LEVELS or fix.get("effort") not in LEVELS:
        p.append("fix must have change, impact (high/medium/low) and effort (high/medium/low)")
    return p


def tally(replies, expected=12, open_collapses=0):
    valid, invalid, seen = [], [], set()
    for i, r in enumerate(replies):
        r = normalize(r)
        probs = check(r)
        name = r.get("juror", f"#{i + 1}") if isinstance(r, dict) else f"#{i + 1}"
        if not probs and name.strip().lower() in seen:
            probs = ["duplicate juror"]
        if probs:
            invalid.append({"index": i + 1, "juror": name, "problems": probs})
        else:
            seen.add(name.strip().lower())
            valid.append(r)

    g = sum(1 for r in valid if r["vote"] == "GUILTY")
    ng = sum(1 for r in valid if r["vote"] == "NOT GUILTY")
    ie = sum(1 for r in valid if r["vote"] == "INSUFFICIENT EVIDENCE")
    decisive = g + ng
    n = len(valid)
    avg_conf = round(sum(r["confidence"] for r in valid) / n, 1) if n else None
    weak = sum(1 for r in valid if r["evidence_strength"] in ("weak", "none"))

    if n < (2 * expected) / 3 or (n and ie * 3 > n):
        decision = "INCONCLUSIVE"
    elif g > ng:
        decision = "FAIL"
    elif n and ng / n >= 0.75 and weak * 2 < n:
        decision = "PASS"
    else:
        decision = "REVISE"
    capped = False
    if decision == "PASS" and open_collapses > 0:
        decision, capped = "REVISE", True

    fixes = {}
    for r in valid:
        f = r["fix"]
        fixes.setdefault(f["impact"], []).append({"juror": r["juror"], "change": f["change"], "effort": f["effort"]})

    return {
        "expected": expected, "received_valid": n, "invalid": invalid,
        "not_guilty": ng, "guilty": g, "insufficient_evidence": ie,
        "average_confidence": avg_conf, "weak_or_no_evidence_votes": weak,
        "decision": decision, "capped_by_open_collapses": capped, "fixes_by_impact": fixes,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    expected, open_c = 12, 0
    if "--expected" in sys.argv:
        expected = int(sys.argv[sys.argv.index("--expected") + 1])
    if "--open-collapses" in sys.argv:
        open_c = int(sys.argv[sys.argv.index("--open-collapses") + 1])
    args = [a for a in args if not a.isdigit()]
    with open(args[0], encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        sys.exit("votes.json must be a JSON list of juror replies")
    res = tally(data, expected, open_c)
    if "--json" in sys.argv:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return
    print(f"Valid votes: {res['received_valid']} of {expected} expected")
    print(f"NOT GUILTY {res['not_guilty']} · GUILTY {res['guilty']} · INSUFFICIENT EVIDENCE {res['insufficient_evidence']}")
    print(f"Average confidence: {res['average_confidence']}/10 (not a probability of success)")
    print(f"Votes with weak or no evidence: {res['weak_or_no_evidence_votes']}")
    print(f"Judge's decision by rule: {res['decision']}")
    if res["capped_by_open_collapses"]:
        print(f"  (PASS by votes, capped to REVISE: {open_c} \"collapses\" assumption(s) still untested. Run those experiments first.)")
    for bad in res["invalid"]:
        action = "ignored (this juror already has a valid vote)" if bad["problems"] == ["duplicate juror"] else "re-run this juror"
        print(f"  ! Invalid reply {bad['index']} ({bad['juror']}): {'; '.join(bad['problems'])} → {action}")


if __name__ == "__main__":
    main()
