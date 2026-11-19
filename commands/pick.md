---
description: Score problem statements against the rubric, apply red flags, then put the top 2–3 on trial to pick one
argument-hint: "[--quick] [--no-trial]"
---

# /hack:pick

Follow the `hack-kit` skill rules. Read STATE.md, BRIEF.md and STATEMENTS.md first.

Arguments: $ARGUMENTS

## Step 1 — Score
Use `${CLAUDE_PLUGIN_ROOT}/templates/scoring.md`. Score every remaining statement 1–5 on:

| Criterion | Default weight | Notes |
|---|---|---|
| Problem is real & painful (evidence) | 3 | |
| Clear real end user we can reach/understand | 2 | |
| Fits top rubric items | 3 | use BRIEF.md weights |
| Room for a smarter angle (not the obvious idea) | 2 | |
| One complete journey buildable in time by this team | 3 | match team skills |
| Demo-able with a wow moment | 2 | |
| Data available or easy to mock honestly | 1 | |
| Team interest / domain access (someone to call) | 1 | |

Adjust weights to the real rubric and show the weights used. Show a ranked table with total score.

## Step 2 — Red flags
Mark any statement with: needs hardware we don't have; needs private data we can't get; needs real-world validation impossible in time; safety-critical with no human-check possible; already solved well by a free government/major app; team has zero knowledge and no one to ask. A red flag drops the score or removes it — say which.

## Step 3 — Shortlist
Ask the team (AskUserQuestion) to confirm the shortlist: top 3 (top 2 in quick mode), or their own choice. For each shortlisted statement, write a **one-paragraph candidate idea** (the smarter angle from STATEMENTS.md).

## Step 4 — Trial
Unless `--no-trial`, run the `hack-court` skill (`${CLAUDE_PLUGIN_ROOT}/skills/hack-court/SKILL.md`) once per shortlisted candidate. The question on trial: **"Is this problem worth solving, and can this idea solve it here, in this time, for its real users?"** Use quick mode if `--quick` or STATE.md says quick. Tell the user how many subagent calls this will take before starting (≈15 per full trial, ≈9 per quick trial).

## Step 5 — Recommend and decide
Show a comparison table: candidate | score | verdict (x/12) | weakest rating | best fix. Recommend one with 3 reasons. Then ask the captain to make the final pick (AskUserQuestion with the candidates as options).

## Step 6 — Save
Write `.hackathon/PICK-VERDICT.md`: scores, red flags, trial summaries (link to `.hackathon/court/...`), the final pick, why, and fixes to carry forward. Update STATE.md (phase = picked; chosen statement; candidate idea).

Say: **Next: `/hack:users`.**
