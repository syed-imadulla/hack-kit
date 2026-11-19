---
description: "Phase 11 · Plan the MVP as one complete journey with a wow moment: build/mock/cut, stack, roles, timeline, 90-second demo, AI test cases"
argument-hint: "[--quick]"
---

# /hack:plan — One journey, built for real

> **Phase 11 of 14** · Reads: `BRIEF.md`, `CORE.md` · Writes: `PLAN.md` · Next: `/hack:verify`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md` and `CORE.md`. If CORE.md isn't locked, suggest running `/hack:lock` first, except on the starter path, where this command does the lock (see "Starter path" below).


Profile settings used: `plan_depth`, plan extras, team size, `skip_phases` (ideathons skip this) (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
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

### 5. Team-aware tasks
1. **Team table:** each member, their skills, and the hours they can really work until code freeze (sleep counts). Prefill from BRIEF.md.
2. **Task table:** break the Build items into tasks of 4 h or less: ID, owner, skills needed, hours, depends on. Put the riskiest integration (for example, the AI call inside the main flow) **early**.
3. **Check it:**
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/plan_check.py" .hackathon/PLAN.md
   ```
   It reports the critical path, each person's load, skill gaps, integration checkpoints and whether the critical path fits before code freeze. Paste its output under `## Plan check`. Without Python, do the same checks by hand.
4. **Fix what it flags,** in this order: move tasks off overloaded people → pair a skill gap with someone who has the skill → mock or cut tasks on the critical path → move integration points earlier. Ask the captain (AskUserQuestion) before cutting anything in the demo journey.
5. **Plan extras from the profile:** for AI/ML, the data source, a baseline vs model comparison and an evaluation metric; for hardware, a bill of materials (in hand vs needed), substitutes and a simulation fallback.

### 6. Timeline and freezes
- An hour-by-hour timeline derived from the task table, with integration checkpoints marked.
- Freeze times: features, code, deck, and the backup demo recording.
- In `/hack:status`, the task table's Status column shows progress.

### 7. 90-second demo script
Hook (the problem in one line, plus a number) → persona → live journey → wow moment → safety or human check → impact (marked as targets) → the motto.
Add a **backup plan**: a recorded video, seeded data and an offline mode.

### 8. Failure scenarios
From STRESS.md, give each failure (no internet, API down, wrong AI answer, user gives up) a fallback and a backup demo path.

### 9. AI test cases
Write 8–12 inputs with the expected behaviour for each. Include a regional language, unclear input, wrong input, a safety-critical input and empty input. At least one test should expect a hand-over to a human.

## Starter path (STATE.md → Profile → Path: starter)
`/hack:validate`, `/hack:stress` and `/hack:lock` are folded in here. Do these **before step 1**, in about 15 minutes:
1. **Riskiest assumptions (validate, short):** list the top 3 in `ASSUMPTIONS.md` with a kill test each (collapses · weakens · minor). For the top "collapses" one, write one 30-minute experiment card (who to ask, what to ask, pass/fail rule). Never mark it validated without `[V]` or `[T]` evidence.
2. **Quick stress check:** role-play 3 people in 2 lines each: the least-digital user, the front-line worker, and the sceptic. Note each one's biggest doubt and the change it suggests. Write them to `STRESS.md` under `## Short version (starter path)`.
3. **Lock:** fill in `CORE.md` from `templates/core.md` (problem, main user, journey, motto, what's built vs mocked). Show it and ask the captain: **"Lock this idea?"** (Lock · Change one thing first). Warn in one line if a "collapses" assumption is still untested. Then mark lock done in STATE.md.

Then continue with steps 1–9 using the profile's `plan_depth` (light on the starter path: skip the architecture diagram unless asked, keep the task table short).

## Output
Write `.hackathon/PLAN.md` from `templates/plan.md`. Tick "plan" in STATE.md and set the freeze times.

## Finish
Give 3 lines: the journey, the wow moment and the code freeze time.
**Next → `/hack:verify`.** It puts the solution on trial. On the starter path: build, then **`/hack:pitch`** (and `/hack:verify --demo` after building if there's time).
