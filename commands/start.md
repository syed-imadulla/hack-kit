---
description: "Phase 1 · Set up the hackathon project and read the brief like a judge: rubric, limits, team, time"
argument-hint: "[event name or brief link] [--quick]"
---

# /hack:start — Read the brief like a judge

> **Phase 1 of 12** · Reads: — · Writes: `BRIEF.md`, `STATE.md` · Next: `/hack:decode`

Arguments: $ARGUMENTS

## Before you start
Load the shared rules from the `hack-kit` skill (`${CLAUDE_PLUGIN_ROOT}/skills/hack-kit/SKILL.md`).

If `.hackathon/STATE.md` already exists, show the current phase and ask:
- **Continue this event** → stop here and suggest `/hack:status`.
- **Start a new event** → rename the old folder to `.hackathon-old-<YYYYMMDD-HHMM>/`, then continue.

## Goal
Capture everything about the event that decides what wins, before anyone falls in love with an idea.

## Steps

### 1. Collect the brief
If the arguments contain a link, fetch it with WebFetch. If the user attached or pasted the brief, read that. Pull out the rubric, the rules and the deliverables, show what you found, and ask the user to confirm it.

### 2. Ask what's missing
Use AskUserQuestion (at most 4 per round). Prefill options wherever you can.

| Topic | What to capture |
|---|---|
| Event | name, organiser, track or theme |
| Rubric | criteria and weights. If unknown, use the default (Problem 25 · Innovation 20 · Feasibility 20 · Impact 20 · Presentation 15) and mark it `ASSUMED` |
| Deliverables | slide limit, video, repo, form questions with word limits, demo length |
| Time | now, submission deadline, judging time (with time zone) |
| Team | names, roles, skills (frontend, backend, AI, design, pitch, domain) |
| Sponsor tech | required or bonus tools and APIs |
| Rules | pre-built code, data, APIs, team size |

### 3. Write down what judges will reward
Translate the top 3 rubric items into plain words, and say what each one means for choosing an idea. For example: "Feasibility 25% → pick something one journey can prove in 24 h."

### 4. Set the plan
- **Mode:** `quick` if `--quick` was passed or the whole event is under 12 h, otherwise `full`.
- **Captain:** the final decider. Ask if it isn't clear.
- **Freeze times:** idea freeze ≈ 1.5 h after statements are released; code freeze 3–4 h before judging.

## Output
- `.hackathon/BRIEF.md` from `templates/brief.md`.
- `.hackathon/STATE.md` from `templates/state.md`. Tick "start".
- Create the folder `.hackathon/court/`.

## Finish
Give a 5-line summary: event, top 3 rubric items, deliverables, time left, mode.
**Next → `/hack:decode`.** Paste the problem statements when they're out.
