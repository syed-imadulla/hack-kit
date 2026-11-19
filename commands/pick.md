---
description: "Phase 3 · Score statements on the rubric, apply red flags, put the top 2–3 on trial, and let the captain pick one"
argument-hint: "[--quick] [--no-trial]"
---

# /hack:pick — Choose the statement worth your weekend

> **Phase 3 of 12** · Reads: `BRIEF.md`, `STATEMENTS.md` · Writes: `PICK.md`, `court/` · Next: `/hack:users`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md` and `STATEMENTS.md`.

## Goal
Pick the one statement where a **real problem**, the **rubric** and the **team's ability to build** overlap. Base the pick on evidence and a trial, not on gut feeling.

## Steps

### 1. Score
Using `templates/scoring.md`, score every remaining statement 1–5 on each criterion:

| Criterion | Default weight |
|---|---|
| Problem is real and painful (evidence) | ×3 |
| Clear real end user we can reach or understand | ×2 |
| Fits the top rubric items | ×3 |
| Room for a smarter angle | ×2 |
| One complete journey buildable in time by this team | ×3 |
| Demo-able, with a wow moment | ×2 |
| Data available or easy to mock honestly | ×1 |
| Team interest or domain access (someone to call) | ×1 |

Adjust the weights to the real rubric and show the weights you used. Rank the statements by total.

### 2. Red flags
Flag any statement that:
- needs hardware the team doesn't have;
- needs private data the team can't get;
- needs real-world validation that's impossible in the time;
- is safety-critical with no possible human check;
- is already solved well by a free government or major app;
- the team knows nothing about and has no one to ask.

For each flag, say whether it lowers the score or removes the statement.

### 3. Shortlist
Ask (AskUserQuestion) to confirm the shortlist: the top 3 (top 2 in quick mode), or the team's own choice. For each statement on the shortlist, write a **one-paragraph candidate idea** based on its smarter angle.

### 4. Trial
Unless `--no-trial` was passed, run the `hack-court` skill once per candidate.
- **On trial:** "Is this problem worth solving, and can this idea solve it here, in this time, for its real users?"
- Use quick mode if `--quick` was passed or STATE.md says quick.
- Before starting, tell the user the cost: about 15 subagent calls per full trial, about 9 per quick trial.

### 5. Recommend and decide
| Candidate | Score | Verdict | Weakest rating | Best fix |

Recommend one candidate with 3 reasons. Then the **captain decides** (AskUserQuestion, with the candidates as options).

## Output
- Write `.hackathon/PICK.md`: the scores, red flags, links to each trial in `court/`, the final pick and why, and the fixes to carry forward.
- In STATE.md: tick "pick", and set the chosen statement and the candidate idea.

## Finish
Give 3 lines: the pick, its verdict, and the top fix.
**Next → `/hack:users`.**
