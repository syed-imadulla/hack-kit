---
description: Plan the MVP as one complete journey with a wow moment — build / mock / cut, tech stack with reasons, roles, freeze times, 90-second demo script and AI test cases
argument-hint: "[--quick]"
---

# /hack:plan

Follow the `hack-kit` skill rules. Read STATE.md, BRIEF.md and CORE.md (must be LOCKED; if not, suggest `/hack:lock` first).

Arguments: $ARGUMENTS

## Step 1 — Ask
AskUserQuestion:
- Stack preferences / what the team is fastest in (offer: Next.js + FastAPI, Streamlit, Flutter, no-code, "you decide").
- Hours left until code freeze (prefill from STATE.md).
- Any sponsor API that must be used.
- Who is on frontend / backend / AI / pitch (confirm from BRIEF.md).

## Step 2 — MVP = one journey
- Pick the **one** end-to-end journey from CORE.md that shows the whole value.
- Name the **wow moment** (the 10 seconds judges will remember).
- **Build / Mock / Cut** table: every feature from CORE.md → Build (real), Mock (fake but labelled "mocked"), or Cut (roadmap). Build only what the demo journey needs.

## Step 3 — Tech stack
Table: layer | tool | why this one | fallback if it fails. Keep it small. Use the simplest channel for users (e.g. WhatsApp, phone call) when it fits CORE.md. Use fixed rules (not AI) for safety checks.

## Step 4 — Architecture
A simple layered description (Who uses it → The brain → AI services → Data & existing systems). Write a Mermaid diagram block for it.

## Step 5 — Timeline and roles
- Hour-by-hour plan up to code freeze (3–4 h before judging), with checkpoints.
- Each teammate's tasks.
- Freeze times: feature freeze, code freeze, deck freeze, demo recording.

## Step 6 — Demo script (90 seconds)
Script with time marks: hook (problem in one line + number) → persona → live journey → wow moment → safety/human check → impact (labelled as target) → close with motto. Include a **backup plan**: recorded video, seeded data, offline mode.

## Step 7 — AI test cases
8–12 test inputs including edge cases: regional language, unclear input, wrong input, safety-critical input, empty input. Expected behaviour for each (incl. "hand over to human").

## Step 8 — Save
Write `.hackathon/PLAN.md` using `${CLAUDE_PLUGIN_ROOT}/templates/plan.md`. Update STATE.md.

Say: **Next: `/hack:verify`** (puts the solution on trial).
