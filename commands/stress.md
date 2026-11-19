---
description: "Phase 8 · Role-play the domain expert, front-line worker, least-digital user, sceptic and admin to attack the chosen idea, and draft CORE v1"
argument-hint: "[--quick]"
---

# /hack:stress — Attack it before the judges do

> **Phase 8 of 14** · Reads: `IDEAS.md`, `EVIDENCE.md`, `COMPETE.md`, `ASSUMPTIONS.md` · Writes: `STRESS.md`, draft `CORE.md` · Next: `/hack:improve`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `USERS.md`, `IDEAS.md`, `EVIDENCE.md`, `COMPETE.md` and `ASSUMPTIONS.md`.


Profile settings used: `mode` (questions per role), `explain_steps` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Stand in for the domain expert you don't have, and find every weakness in the chosen idea. This command **finds and ranks** the problems. `/hack:improve` then fixes them with the team.

## Steps

### 1. Draft CORE v1
From the chosen idea in IDEAS.md, write a draft `CORE.md` (from `templates/core.md`, `Version: v1`, marked DRAFT): the motto, the user, the end-to-end journey step by step, who does what, where AI is used and where humans decide.

### 2. Role-play the attacks
Play each role in turn, with 4–6 hard questions each (2–3 in quick mode). Label each attack `[V]`, `[T]` or `[AI]`, depending on what it's based on.

| Role | Typical attack |
|---|---|
| Senior domain expert | "That's not how it works in real life…"; rules, authority, liability |
| Front-line worker | Extra work, rush hour, failure cases |
| Least-digital user | "I can't read, type or use this." |
| Sceptical judge | "Why not just use X?" "Where's the evidence?" "What if the AI is wrong?" |
| Admin or systems owner | Integration, data, privacy, cost of change |

### 3. Failure scenarios
In one line each: what happens with **no internet**, an **API down**, a **wrong AI answer**, or a **user who gives up halfway**? Is there a fallback?

### 4. Doubt table
| # | Doubt | Raised by | Label | Severity | Smallest fix that keeps the core | Changes core? |

Rules for proposed fixes:
- Removing a feature beats adding one.
- A human check, a fixed rule or a fallback beats "better AI".
- A fix that changes the problem, the main user or the motto is marked **Y** (DRIFT).

### 5. New assumptions
Add every doubt that's really an untested belief to `ASSUMPTIONS.md` (source "stress"), with a kill test.

### 6. Real-people check
Suggest showing the top 3 doubts to 2–3 real people: a mentor, someone who works in the field, or a family member in that job. If the team adds their answers (`[T]`), update the table.

## Output
- `.hackathon/STRESS.md` from `templates/stress.md`.
- Draft `CORE.md` v1.
- Updated `ASSUMPTIONS.md`.
- Tick "stress" in STATE.md.

## Finish
Give 3 lines: the number of doubts (high, medium, low), the biggest one, and the number of new assumptions.
**Next → `/hack:improve`.** It turns these doubts into a better CORE v2, with the team's approval.
