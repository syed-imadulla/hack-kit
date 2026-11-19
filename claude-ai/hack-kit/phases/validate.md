> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:validate — Prove it's real

> **Phase 6 of 14** · Reads: `IDEAS.md`, `USERS.md`, `ASSUMPTIONS.md` · Writes: `EVIDENCE.md`, `ASSUMPTIONS.md` · Next: `/hack:compete`

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md`, `IDEAS.md`, `USERS.md` and `ASSUMPTIONS.md`.


Profile settings used: `validate_experiments`, `sources_to_open` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Collect three layers of evidence, so no judge can ask "is this even a problem?" Then design small real-world tests for the assumptions that could kill the idea.

## Steps

### 1. Research (open every source)
| Layer | Look for |
|---|---|
| Numbers | Scale and severity from government data, research papers, official reports and reputed news. Prefer the event's own country or region. |
| Real voices | Complaints in news stories, consumer forums, app reviews of existing solutions and social posts. Paraphrase them, with short quotes only. |
| Local example | One concrete place or story near the event. |

If web tools aren't available, say so, list what to look up, and mark the claims `[?]`. In quick mode, research only the top 3 claims.

### 2. Evidence table
| # | Claim | Label | Number or short quote | Source | Date | Reliability | Supports which assumption |

- Label: `[V]` only if the source was opened and read; otherwise `[AI]` or `[?]`.
- Reliability: high (official data, peer-reviewed), medium (reputed news, industry report), low (blog, forum, single anecdote).
- Flag any number the team was planning to use that isn't `[V]` or `[T]`.

### 3. Experiment cards
Take the test-first list from `ASSUMPTIONS.md`. Write up to 3 cards (1 in quick mode), starting with the "collapses" assumptions:

```
EXPERIMENT <n>: <assumption #>
Hypothesis:   <what we believe>
Who:          <which users, how many — e.g. 3 elderly patients at the venue>
Procedure:    <exact steps, under 30 minutes>
Pass if:      <clear rule>
Fail if:      <clear rule>
Observations: (team fills this in — never the AI)
Conclusion:   (after observations: validated / rejected / unclear)
```

### 4. Venue interview script (5 minutes, Mom-Test style)
Ask about people's past behaviour, not their opinion of the idea:
1. "Tell me about the last time you [faced the problem]."
2. "What did you do? How long did it take?"
3. "What have you tried to fix it? Why didn't it work?"
4. "What's the most annoying part?"
5. At the very end, share the one-line idea and ask: "What would stop you from using this?"

Note the difference between what people **say** they'd do and what they've actually **done**. Only past behaviour counts as strong evidence.

### 5. Real results
Ask (AskUserQuestion) whether they've talked to anyone or run an experiment yet:
- **Add results now** → fill in the observations (labelled `[T]`), write conclusions, and update the assumption statuses in `ASSUMPTIONS.md`.
- **Going to test now** → tell them to run `/hack:validate` again afterwards.
- **Nobody available** → record it as a risk, and keep the assumptions open.

Never fill in observations yourself, and never mark an assumption validated without them.

## Output
- `.hackathon/EVIDENCE.md` from `templates/evidence.md`, with the top 3 facts (`[V]` or `[T]` only) for the pitch first.
- Updated `ASSUMPTIONS.md`.
- Tick "validate" in STATE.md.

## Finish
Give 3 lines: the count of `[V]`, `[T]`, `[AI]` and `[?]` claims; the experiments planned or done; the strongest fact.
**Next → `/hack:compete`**, or `/hack:stress` if compete is already done.
