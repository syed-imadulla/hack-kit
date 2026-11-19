---
description: "Phase 10 · Put the solution on trial with a 12-juror court, then check it against the rubric, the mistakes list and every claim"
argument-hint: "[--quick]"
---

# /hack:verify — Put the solution on trial

> **Phase 10 of 12** · Reads: `BRIEF.md`, `EVIDENCE.md`, `COMPETE.md`, `CORE.md`, `PLAN.md` · Writes: `VERDICT.md`, `court/` · Next: `/hack:pitch`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md`, `EVIDENCE.md`, `COMPETE.md`, `CORE.md` and `PLAN.md`.

## Goal
Find out, before the judges do, whether the planned solution really solves the problem, and what to fix in the time left.

## Steps

### 1. Trial
Run the `hack-court` skill.
- **Case file:** the CORE.md journey, the PLAN.md MVP scope, and the top 3 facts from EVIDENCE.md.
- **On trial:** "Does this solution, as planned, solve the real problem for its real users?"
- Use quick mode if `--quick` was passed or STATE.md says quick. Tell the user the cost before starting.

### 2. Rubric check
| Criterion | Weight | Score /10 | Why | One thing that raises it |

Score like a strict judge would. Show the weighted total out of 100.

### 3. Mistakes check
Mark each item in the skill's "Mistakes to block" table ✅, ⚠️ or ❌, with one line each.

### 4. Claims check
List every number and claim in CORE.md and PLAN.md, and mark each one:
- sourced, with the link;
- `(target)`;
- ❌ unsourced.

Every ❌ must end up sourced, relabelled as a target, or removed.

### 5. Fix list
Merge the fixes from the trial, the rubric check and the mistakes check, and rank them by score gained ÷ effort. Mark each one "inside the core" or "changes the core".
Ask (AskUserQuestion, multiSelect) which fixes to apply, then apply them to CORE.md and PLAN.md. Once CORE.md is locked, apply only inside-the-core fixes unless the captain approves.

## Output
Write `.hackathon/VERDICT.md`: the verdict and ratings (with a link to the trial in `court/`), the rubric table, the mistakes table, the claims table and the fixes applied. Tick "verify" in STATE.md.

## Finish
Give 3 lines: the verdict, the rubric total and the top remaining risk.
**Next → `/hack:pitch`.**
