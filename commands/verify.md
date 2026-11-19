---
description: "Phase 12 · Put the planned solution on trial with Hack Court 2.0, then check it against the rubric, the mistakes list, every claim and the open assumptions"
argument-hint: "[--quick]"
---

# /hack:verify — Put the solution on trial

> **Phase 12 of 14** · Reads: `BRIEF.md`, `EVIDENCE.md`, `COMPETE.md`, `CORE.md`, `PLAN.md`, `ASSUMPTIONS.md` · Writes: `VERDICT.md`, `court/` · Next: `/hack:pitch` (or `/hack:improve`)

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md` and the files above.

## Goal
Find out, before the judges do, whether the planned solution really solves the problem, and what to fix in the time left.

## Steps

### 1. Trial
Run the `hack-court` skill.
- **Evidence pack:** the CORE.md journey, the PLAN.md MVP scope (built vs mocked, labelled `[T]`), the top `[V]` and `[T]` facts from EVIDENCE.md, the closest competitor and honest difference from COMPETE.md, and the top 3 open assumptions.
- **On trial:** "Does this solution, as planned, solve the real problem for its real users?"
- Use quick mode if `--quick` was passed or STATE.md says quick. Tell the user the cost before starting.

### 2. Rubric check
| Criterion | Weight | Score /10 | Why | One thing that raises it |

Score like a strict judge would. Show the weighted total out of 100, and say plainly that it's an estimate, not a prediction.

### 3. Mistakes check
Mark each item in the skill's "Mistakes to block" table ✅, ⚠️ or ❌, with one line each.

### 4. Claims check
List every number and claim in CORE.md and PLAN.md and mark each one:
- `[V]` with a link, or `[T]`;
- `(target)`;
- ❌ unlabelled, or `[AI]` presented as a fact.

Every ❌ must end up sourced, relabelled as a target or an estimate, or removed.

### 5. Assumptions check
If the decision is INCONCLUSIVE or capped, the next experiment comes **before** more building or pitching.

List the open "collapses" and "weakens" assumptions. For each one, say whether the demo depends on it, and what the team should say if a judge asks.

## Output
Write `.hackathon/VERDICT.md`: the decision and ratings (with a link to the trial in `court/`), the rubric table, the mistakes table, the claims table and the assumptions check. Tick "verify" in STATE.md.

## Finish
Give 3 lines: the decision, the rubric total and the top remaining risk.
**Next:**
- **PASS** → `/hack:pitch`.
- **REVISE or FAIL** → `/hack:improve` (only inside-the-core changes once CORE is locked), then `/hack:pitch`.
- **INCONCLUSIVE** → `/hack:assumptions` and the next experiment.
