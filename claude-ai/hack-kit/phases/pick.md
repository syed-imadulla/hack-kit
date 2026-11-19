> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:pick — Choose the problem worth your weekend

> **Phase 3 of 14** · Reads: `BRIEF.md`, `STATEMENTS.md` · Writes: `PICK.md`, `court/` · Next: `/hack:users`

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md` and `STATEMENTS.md`. If `STATEMENTS.md` is missing: on the starter path, do the short decode below first; on the full path, suggest `/hack:decode`.


Profile settings used: `pick_trials`, `pick_jury`, `sources_to_open`, scoring weights, quick-jury swap (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Pick the **problem** where real pain, the rubric and the team's ability to build overlap. Base the pick on evidence and a trial, not gut feeling. The solution comes later, in `/hack:ideate`. Here you only need a rough direction to show the problem *can* be solved in the time.

## Steps

### 1. Score
Using `templates/scoring.md`, score every remaining statement 1–5 on each criterion:

| Criterion | Default weight |
|---|---|
| Problem is real and painful (evidence label strength) | ×3 |
| Clear real end user we can reach or understand | ×2 |
| Fits the top rubric items | ×3 |
| Room for different solution directions (not just one obvious app) | ×2 |
| One complete journey buildable in time by this team | ×3 |
| Demo-able, with a wow moment | ×2 |
| Data available or easy to mock honestly | ×1 |
| Team interest or domain access (someone to call) | ×1 |

Adjust the weights to the real rubric and show the weights used. Rank by total. Show how sure each score is: a score that rests on `[AI]` or `[?]` claims gets a "low certainty" mark.

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
Ask (AskUserQuestion) to confirm the shortlist: the top 3 (top 2 in quick mode), or the team's own choice. For each, write a **one-paragraph case**: the problem, the user, and one rough direction (from the smarter angle in STATEMENTS.md).

### 4. Evidence boost (before the trial)
For each shortlisted statement, **open the 2 strongest sources** behind its "problem is real" claim, preferring official or research sources, and relabel those claims `[V]`. Leave everything else as `[AI]` or `[?]`. Skip this only if web tools aren't available, and say so.

Why: in testing, a jury given only unopened search snippets voted INSUFFICIENT EVIDENCE almost unanimously. Ten minutes of opening sources turned that into a decision.

### 5. Trial
Unless `--no-trial` was passed, run the `hack-court` skill once per shortlisted statement.
- **On trial:** "Is this problem real and worth solving here, and can this team solve it for its real users in the time?"
- Use quick mode if `--quick` was passed or STATE.md says quick. Tell the user the cost first.

### 6. Recommend and decide
| Statement | Score | Certainty | Decision (PASS/REVISE/FAIL/INCONCLUSIVE) | Weakest assumption | Best fix |

Recommend one with 3 reasons. Then the **captain decides** (AskUserQuestion, with the statements as options).

## Starter path (STATE.md → Profile → Path: starter)
`/hack:decode` is folded in here. If `STATEMENTS.md` doesn't exist yet, do a **short decode** first, then continue with step 1:
- For each statement, one row: real problem in plain words · who suffers most · least-digital user · one hidden constraint · how often or how bad (label `[V]`/`[T]`/`[AI]`/`[?]`).
- No web research unless the team asks; mark gaps `[?]`.
- Write it to `STATEMENTS.md` under `## Short decode (starter path)`.

Then run steps 1–6 as normal with the profile's settings: one trial with a quick jury of 7. Tell the team the cost first (about 9 agent runs).

## Output
- `.hackathon/PICK.md`: scores and weights, red flags, links to each trial in `court/`, the final pick and why, the rejected statements and why, and the assumptions to carry forward.
- Add the trial's weakest assumptions to `ASSUMPTIONS.md`.
- In STATE.md: tick "pick", set the chosen statement, and log the decision with the rejected options.

## Finish
Give 3 lines: the chosen problem, its decision, and the riskiest assumption.
**Next → `/hack:users`** (full path) or **`/hack:ideate`** (starter path: it covers users too).
