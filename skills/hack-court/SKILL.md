---
name: hack-court
description: Run a courtroom trial on a hackathon problem statement, idea, feature or pitch. Prosecution and defense argue, 12 independent juror subagents vote, a judge gives a verdict with ratings and fixes. Judges whether the problem is real and the solution truly solves it — never business viability. Used by /hack:pick, /hack:verify and /hack:court.
---

# Hack Court — problem-focused trial

## What is on trial
One question only: **"Does this solve a real problem for its real users, as described?"**

- **GUILTY** = it does *not* solve a real problem for its real users as described.
- **NOT GUILTY** = it does.
- Never judge revenue, market size, pricing, business model or investor appeal. If a juror or lawyer brings these up, drop that point.

The juror list is in `${CLAUDE_PLUGIN_ROOT}/skills/hack-court/jurors.json` and the verdict template in `${CLAUDE_PLUGIN_ROOT}/templates/verdict.md`. If `${CLAUDE_PLUGIN_ROOT}` isn't expanded, find the plugin root as described in section 1 of the `hack-kit` skill. Read the juror list before starting.

## Modes
| Mode | Jurors | Points per side | When |
|---|---|---|---|
| Full | 12 | 5 | default |
| Quick | 6 (`"quick": true` jurors) | 3 | `--quick`, or low time/usage |

Trying several statements (in `/hack:pick`)? Run one trial per shortlisted item, max 3. In quick mode, run max 2.

## Step 1 — Case file (you, the clerk)
Write `case.md` (≈120 words, plain words):
- **Problem:** who suffers, what, how often, evidence (with source or `UNVERIFIED`).
- **Real users:** end user, least-digital user, operator.
- **Proposed solution:** what it does, step by step, in 3–5 lines.
- **Constraints:** time left, team skills, rubric top items, existing systems.

Save to `.hackathon/court/<case-slug>/case.md` (or `./court/<case-slug>/` if there is no `.hackathon/`). Build it only from `.hackathon/` files and what the user said. Don't add facts.

## Step 2 — Prosecution and defense
Launch two subagents **in parallel** using the Agent/Task tool (use the `hack-prosecutor` and `hack-defender` agents if available, else general-purpose with the prompts below). Give each only the case file.

- **Prosecution:** "Make the strongest case that this does NOT solve a real problem for its real users. Give exactly N numbered points. Each point: claim (1 line) + why it matters to a real user (1 line). Attack the problem's reality, the fit to the root cause, exclusion of users, safety, existing alternatives, and buildability. Do not use business, revenue or market arguments."
- **Defense:** "Make the strongest case that this DOES solve a real problem for its real users. Give exactly N numbered points, same format. No business, revenue or market arguments."

Save them as `prosecution.md` and `defense.md`.

## Step 3 — Jury (independent)
For each juror in the active list, launch **a separate subagent** (use the `hack-juror` agent if available). Launch them in parallel, in batches of up to 6. Each juror gets **only**: their persona (name, lens, asks), the case file, the prosecution and the defense. They must not see other jurors' votes.

Juror prompt:
```
You are juror #{id}: {name}.
Your lens: {lens}
Questions you care about: {asks}

Read the case, the prosecution and the defense below.
GUILTY means: "It does not solve a real problem for its real users as described."
Do NOT consider revenue, market size, pricing or investors.

Reply with ONLY one JSON object, nothing else:
{"juror": "{name}", "vote": "GUILTY" or "NOT GUILTY", "confidence": 1-10, "reason": "<max 30 words, from your lens>", "fix": "<one concrete change that would win or keep your vote, max 25 words>"}

CASE: ...
PROSECUTION: ...
DEFENSE: ...
```

Collect every reply. Parse the JSON.
- If a reply is not valid JSON, or a juror fails, **re-run only that juror** (max 2 retries).
- If it still fails, mark it `NO VOTE` and say so. **Never invent a vote.**

Save all raw votes to `votes.json`.

## Step 4 — Judge (you)
Use only the real votes.

1. Count: GUILTY x / NOT GUILTY y (out of the votes received). Average confidence.
2. Verdict: majority wins. Tie → `HUNG JURY` (treat as "fix before moving on").
3. Ratings out of 10 for the 8 items in `jurors.json → ratings`. Base each on the jurors whose lens covers it, plus the arguments. Show one short reason per rating.
4. Top 3 reasons it fails (from GUILTY reasons and prosecution points that went unanswered).
5. Top 3 fixes (from juror `fix` fields; merge duplicates; prefer fixes **inside the core idea**, don't change the idea).
6. **Quick venue check:** one test the team can do in the next 30 minutes at the venue (talk to 3 people, try the flow on a keypad phone, time a step...), with a clear pass/fail rule.
7. One line: **"If I were your team…"**

## Step 5 — Output
Write `.hackathon/court/<case-slug>/verdict.md` using `${CLAUDE_PLUGIN_ROOT}/templates/verdict.md`, and show the user:

```
VERDICT: NOT GUILTY (9 of 12, avg confidence 7.4/10)

| # | Juror | Vote | Conf | Reason |
...

Ratings /10
Problem is real ........ 9  — sourced wait-time data, 3 venue chats
...

Top 3 reasons it could fail
Top 3 fixes
Quick venue check (30 min): ...  PASS if ..., FAIL if ...
If I were your team: ...
```

## Rules
- Jurors must be independent subagents. If the Agent tool is unavailable (e.g. claude.ai), simulate the jury in one pass and print a clear note: "Simulated jury — less independent than subagents."
- A full trial costs about 15 subagent calls. Tell the user before running more than one full trial in a row; suggest `--quick`.
- The verdict is advice, not a decision. The team captain decides.
