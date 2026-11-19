---
description: Put the locked solution and MVP plan on trial (12-juror court), then check it against the rubric and the mistakes list
argument-hint: "[--quick]"
---

# /hack:verify

Follow the `hack-kit` skill rules. Read STATE.md, BRIEF.md, EVIDENCE.md, COMPETE.md, CORE.md and PLAN.md first.

Arguments: $ARGUMENTS

## Step 1 — Trial
Run the `hack-court` skill (`${CLAUDE_PLUGIN_ROOT}/skills/hack-court/SKILL.md`) on the solution. Case file = CORE.md journey + PLAN.md MVP scope + key evidence. Question on trial: **"Does this solution, as planned, solve the real problem for its real users?"** Use quick mode if `--quick` or STATE.md says quick. Tell the user the subagent cost first.

## Step 2 — Rubric check
For each rubric item in BRIEF.md (with weight): score 1–10 as a strict judge would, one-line reason, and one thing that would raise it. Show the weighted total out of 100.

## Step 3 — Mistakes check
Go through "Mistakes to block" in the skill. Mark each ✅ / ⚠️ / ❌ with one line.

## Step 4 — Claims check
List every number and claim in CORE.md and PLAN.md. Mark: sourced (link) / target (labelled) / ❌ unsourced. Every ❌ must be sourced, labelled as a target, or removed.

## Step 5 — Fixes
Merge fixes from the trial, rubric and mistakes into one list, ranked by (impact on score) ÷ (effort). Mark each "inside the core" or "changes the core". Ask (AskUserQuestion, multiSelect) which to apply. Apply accepted ones to CORE.md / PLAN.md (if CORE.md is locked, only inside-the-core fixes, unless the captain approves).

## Step 6 — Save
Write `.hackathon/VERDICT.md`: verdict summary + ratings (link to court folder), rubric table, mistakes table, claims table, applied fixes. Update STATE.md.

Say: **Next: `/hack:pitch`.**
