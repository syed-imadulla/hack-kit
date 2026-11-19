---
description: "Anytime · Track what the team believes but hasn't proven; run the kill test and plan how to test the riskiest assumptions first"
argument-hint: "[add <assumption>] [--quick]"
---

# /hack:assumptions — What are we assuming?

> **Anytime** · Reads: `ASSUMPTIONS.md`, `EVIDENCE.md` · Writes: `ASSUMPTIONS.md` · Next: `/hack:validate` (to test the top one)

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `ASSUMPTIONS.md` and `EVIDENCE.md`. If `ASSUMPTIONS.md` doesn't exist, create it from `templates/assumptions.md` and seed it from `USERS.md`, `IDEAS.md`, `STRESS.md`, `CORE.md` and any trial verdicts that exist.

## Goal
Teams build on beliefs nobody has tested: "farmers have smartphones", "nurses will use it", "the API is free". This command makes those beliefs visible and ranks which to test first.

## Steps

### 1. Collect
- If the arguments start with `add`, add that assumption.
- Otherwise, scan the files above for anything stated without `[V]` or `[T]` evidence: claims about user behaviour, access, data, technology, cost to the user, adoption, existing systems or rules.
- Merge duplicates. Never delete an assumption; mark it rejected instead.

### 2. Rate each assumption
| Field | Values |
|---|---|
| Importance | critical / high / medium / low |
| Confidence (team's) | high / medium / low |
| Evidence | label + link or note (`[V]`, `[T]`, `[AI]`, `[?]`) |
| **Kill test** | "If this is false, does the idea collapse?" → **collapses** / weakens / minor |
| How to test | the fastest real check (talk to 3 people, try it on a keypad phone, call the API, read the rule) |
| Pass if / fail if | a clear rule |
| Status | open / testing / validated / rejected |

### 3. Rank
Order by kill test first (collapses → weakens → minor), then importance, then lowest confidence. The top 3 open ones are the **test-first list**. Quick mode: rate and rank only the top 5.

### 4. Status rules (strict)
- **Validated** only when the evidence is `[V]` or `[T]`, and the team has typed real observations or a source has been opened.
- **Rejected** when the evidence contradicts it. Then flag every file that depends on it (IDEAS, CORE, PLAN) and suggest `/hack:improve`.
- The AI can never mark something validated on its own reasoning.

### 5. Ask
Ask (AskUserQuestion): "Any results to add?"
- **Add results now:** update the status, the evidence and the date.
- **Test the top one:** go to `/hack:validate`, which builds an experiment card for it.
- **Not now.**

## Output
Write `.hackathon/ASSUMPTIONS.md`, keeping the history (status changes are dated). In STATE.md, put the test-first list under Pending.

## Finish
Show:
- counts: open, testing, validated, rejected;
- how many "collapses" assumptions are still open;
- the test-first list.

**Next → `/hack:validate`** to test the top one.
