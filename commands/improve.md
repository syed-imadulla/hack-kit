---
description: "Phase 9 · Turn trial or stress-test feedback into a better version of the idea — with reasons, a no-drift guardrail, team approval and a quick re-check"
argument-hint: "[--quick] [--no-retrial]"
---

# /hack:improve — Challenge harder, then make it better

> **Phase 9 of 14** · Reads: `CORE.md`, the latest verdict or `STRESS.md`, `ASSUMPTIONS.md` · Writes: `IMPROVE.md`, new version of `CORE.md` · Next: `/hack:lock` (or continue after a later trial)

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `CORE.md` and `ASSUMPTIONS.md`, plus the newest feedback source:
- the newest `court/*/verdict.md` (from `/hack:verify`, `/hack:court` or `/hack:pick`), or
- `STRESS.md`, if there's been no trial since the stress test.

If CORE.md doesn't exist yet, suggest `/hack:stress` first. This command can run after any trial, not only as phase 9.


Profile settings used: `improve_rounds`, `improve_retrial` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Criticism is only useful if it makes the idea better. This command turns feedback into a **revised version**, explains every change, and checks that the team hasn't drifted from the problem it set out to solve.

## The guardrail (never break it)
These stay fixed: **the problem, the main user, and the motto's promise**. After lock, the **core journey** is fixed too.
- An improvement that changes any of them is marked **DRIFT**. It's only applied if the captain explicitly approves, and that's logged.
- Prefer removing or simplifying over adding. Prefer a human check, a fixed rule or a fallback over "better AI".

## Steps

### 1. Collect the improvement candidates
From the feedback source, take the ranked improvements, the weakest assumption, "what we're overlooking" and the alternative approach. Remove duplicates, and keep the top 5 (top 3 in quick mode).

### 2. Draft each change
| # | Change | Fixes which weakness | Impact | Effort | New risk it adds | Evidence still needed | Inside the core / DRIFT |

Write each change concretely: what changes in the journey, in who does what, or in the MVP.

### 3. The team decides
Ask (AskUserQuestion, multiSelect) which changes to accept. Ask about every DRIFT change separately, with the warning: "This changes the problem, the user or the core journey."

### 4. Make the new version
1. Copy the current `CORE.md` to `.hackathon/history/CORE-v<n>.md`.
2. Apply only the accepted changes. Raise the version number at the top of CORE.md (`Version: v<n+1>`).
3. Add any new assumptions to `ASSUMPTIONS.md`, and mark the ones the changes resolved.

### 5. Compare versions
| | v<n> | v<n+1> |
|---|---|---|
| What improved | | |
| What got worse or riskier | | |
| Assumptions still open | | |
| Same problem and main user? | yes / no | |

### 6. Re-check
Unless `--no-retrial` was passed, run a **quick trial** of the new version with the `hack-court` skill (7 jurors), and compare the decision and ratings with the previous solution trial. If there's no earlier solution trial (the usual case right after `/hack:stress`), this re-trial is the first one: compare its weakest points with the stress doubts instead. In quick mode, re-try only if the team asks.

### 7. Stop rule
Stop and suggest moving on when any of these is true:
- the decision is PASS;
- 2 improvement rounds are done (1 in quick mode);
- the time guard in the skill says there's no time for another round;
- the remaining fixes are low impact;
- the remaining P0 items are experiments, not design changes. Another round can't fix an untested assumption, so send the team to `/hack:validate`.

Otherwise, offer one more round.

## Output
- `.hackathon/IMPROVE.md` from `templates/improve.md`. Add a new `## Round <n>` section each time; never overwrite an earlier round.
- The new version of `CORE.md`, with the old one in `history/`.
- In STATE.md: tick "improve", set "CORE version", and log accepted and rejected changes with reasons.

## Finish
Give 3 lines: the version change (v1 → v2), the top change and why, and the new decision.
**Next → `/hack:lock`.** If this ran after `/hack:verify`, carry on to `/hack:pitch`.
