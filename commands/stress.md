---
description: "Phase 7 · Role-play the domain expert and a sceptical judge to attack the idea; find the smallest fix for each weakness that keeps the core"
argument-hint: "[--quick]"
---

# /hack:stress — Attack it before the judges do

> **Phase 7 of 12** · Reads: `USERS.md`, `EVIDENCE.md`, `COMPETE.md` · Writes: `STRESS.md`, draft `CORE.md` · Next: `/hack:lock`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `PICK.md`, `USERS.md`, `EVIDENCE.md` and `COMPETE.md`.

## Goal
Stand in for the domain expert you don't have. Find every weakness, and fix it **inside** the core idea.

## Steps

### 1. Draft the idea
In 8–10 lines: the motto, the user, the end-to-end journey step by step, who does what, where AI is used, and where humans decide.

### 2. Role-play the attacks
Play each role in turn, with 4–6 hard questions each (2–3 in quick mode):

| Role | Typical attack |
|---|---|
| Senior domain expert | "That's not how it works in real life…"; rules, authority, liability |
| Front-line worker | Extra work, rush hour, failure cases |
| Least-digital user | "I can't read, type or use this." |
| Sceptical judge | "Why not just use X?" "Where's the evidence?" "What if the AI is wrong?" |
| Admin or systems owner | Integration, data, privacy, cost of change |

### 3. Fix table
| # | Doubt | Raised by | Severity | Smallest fix that keeps the core | Changes core? |

Rules for fixes:
- Removing a feature beats adding one.
- A human check, a fixed rule or a fallback beats "better AI".
- If a fix changes the motto, the main user or the main journey, mark it **Y** and warn: "This drifts from the idea."

### 4. The team decides
- Ask (AskUserQuestion, multiSelect) which fixes to accept. Ask about every **Y** fix separately.
- Suggest showing the top 3 doubts to 2–3 real people: a mentor, someone who works in the field, or a family member in that job. If the team adds their answers, update the table.

## Output
- `.hackathon/STRESS.md` from `templates/stress.md`.
- A refreshed **draft** of `.hackathon/CORE.md` from `templates/core.md`, with the accepted fixes applied.
- Tick "stress" in STATE.md.

## Finish
Give 3 lines: the number of doubts, the number fixed, and the biggest one still open.
**Next → `/hack:lock`.**
