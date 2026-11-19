---
description: "Phase 8 · Freeze the core: motto, positioning, persona story, journey, who does what, USPs, and the AI-vs-rules-vs-humans split"
argument-hint: ""
---

# /hack:lock — Freeze the core

> **Phase 8 of 12** · Reads: all files so far · Writes: `CORE.md` (locked) · Next: `/hack:plan`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `USERS.md`, `EVIDENCE.md`, `COMPETE.md`, `STRESS.md` and the draft `CORE.md`.

## Goal
One clear, frozen idea that the whole team can repeat word for word. From here on, the team builds instead of rethinking.

## Steps

### 1. Complete CORE.md
Fill every section of `templates/core.md`:

1. Name and motto
2. Positioning line
3. The problem in 2 lines, with the strongest sourced number
4. Persona story, before vs after
5. End-to-end journey: for each step, who acts, the channel, what the system does and what the human decides
6. Who does what, and what each role never has to do
7. 4–6 USPs, each tied to a user pain (not to a technology)
8. AI vs rules vs humans: safety-critical steps use rules plus a human, never AI alone
9. Inclusion of the least-digital user
10. Fit with existing systems (L0–L3)
11. Privacy basics
12. Out of scope

### 2. Mistakes check
Go through the "Mistakes to block" table in the skill. Fix anything that fails, or flag it.

### 3. Confirm
Show a 10-line summary, then ask (AskUserQuestion):
- **Lock it**
- **Change something first**
- **Run a quick trial first** (`/hack:court --quick`)

### 4. Freeze
Once the team confirms:
- Replace the top line of CORE.md with `> LOCKED: <date time, time zone>`.
- In STATE.md: tick "lock", set "Core locked at", and log the decision.

## After lock
If any later command or teammate proposes a change to the motto, the main user or the main journey, warn: **"This drifts from the locked core. Captain's OK needed."**

## Finish
Give the motto and the journey in 5 steps.
**Next → `/hack:plan`.**
