---
description: "Phase 9 · Plan the MVP as one complete journey with a wow moment: build/mock/cut, stack, roles, timeline, 90-second demo, AI test cases"
argument-hint: "[--quick]"
---

# /hack:plan — One journey, built for real

> **Phase 9 of 12** · Reads: `BRIEF.md`, `CORE.md` · Writes: `PLAN.md` · Next: `/hack:verify`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md` and `CORE.md`. If CORE.md isn't locked, suggest running `/hack:lock` first.

## Goal
Plan an MVP that works end to end for one journey, with one moment the judges remember, and a plan that fits the hours left.

## Steps

### 1. Ask
Use AskUserQuestion, prefilled from BRIEF.md and STATE.md:
- **What's the team fastest in?** For example: Next.js + FastAPI, Streamlit, Flutter, no-code, or "you decide".
- **Hours left until code freeze.**
- **Any sponsor API that must be used.**
- **Confirm who does frontend, backend, AI and pitch.**

### 2. Scope
- **The journey:** the one end-to-end path from CORE.md that shows the whole value.
- **The wow moment:** the 10 seconds judges will remember.
- **Build / Mock / Cut:** sort every CORE.md feature into one of these:
  - **Build:** made real.
  - **Mock:** faked, and labelled "(mocked)".
  - **Cut:** left for the roadmap.

  Build only what the demo journey needs.

### 3. Stack
| Layer | Tool | Why this one | Fallback |

Keep the stack small. Use the simplest channel for users that fits CORE.md, and fixed rules (not AI) for safety checks.

### 4. Architecture
Describe it in layers: who uses it → the brain → AI services → data and existing systems. Include a Mermaid `flowchart` block.

### 5. Timeline and roles
- An hour-by-hour plan up to code freeze, with checkpoints.
- Each teammate's tasks.
- Freeze times: features, code, deck, and the backup demo recording.

### 6. 90-second demo script
Hook (the problem in one line, plus a number) → persona → live journey → wow moment → safety or human check → impact (marked as targets) → the motto.
Add a **backup plan**: a recorded video, seeded data and an offline mode.

### 7. AI test cases
Write 8–12 inputs with the expected behaviour for each. Include a regional language, unclear input, wrong input, a safety-critical input and empty input. At least one test should expect a hand-over to a human.

## Output
Write `.hackathon/PLAN.md` from `templates/plan.md`. Tick "plan" in STATE.md and set the freeze times.

## Finish
Give 3 lines: the journey, the wow moment and the code freeze time.
**Next → `/hack:verify`.** It puts the solution on trial.
