---
description: Build the deck outline within the slide limit, the one-line pitch, form answers for the most-weighted questions, and judge Q&A
argument-hint: "[slide limit] [--quick]"
---

# /hack:pitch

Follow the `hack-kit` skill rules. Read STATE.md, BRIEF.md, EVIDENCE.md, COMPETE.md, CORE.md, PLAN.md and VERDICT.md first.

Arguments: $ARGUMENTS

## Step 1 — Ask
AskUserQuestion: slide limit (prefill from BRIEF.md; default 7), format (PPT/PDF/Google Slides/none), form questions to answer (paste them), pitch length (2/3/5 min).

## Step 2 — One-liners
- **One-line pitch** (≤20 words).
- **Opening line** for the most-weighted rubric item (e.g. an innovation line if Innovation is highest).
- **Motto** (from CORE.md).

## Step 3 — Deck outline
Use `${CLAUDE_PLUGIN_ROOT}/templates/deck-outline.md`. Stay **exactly within** the slide limit. For each slide: title (a full-sentence headline), 3–5 short items max, the visual (diagram, table, timeline, screenshot), and the source line. Default 7-slide flow:
1. Hook + team name + track (the waiting-room moment).
2. Problem with evidence (numbered sources).
3. Solution in one line + 3 cards + "how we compare" table.
4. How it works / AI agents + human checks + rules-not-AI.
5. Persona journey end-to-end + USPs.
6. Tech stack / architecture (clean diagram, MVP tags).
7. Impact (labelled targets) + pilot plan + motto.
Rules: no heavy text, big readable fonts, every number sourced or labelled as a target, no slide over the limit.

## Step 4 — Form answers
If form questions were given, answer each within its word limit. Lead each answer with the strongest point for that question. Simple English.

## Step 5 — Judge Q&A
12–15 likely questions (from the trial's prosecution points and GUILTY reasons, the rubric, and competitors) with 2–3 line answers. Include: "What if the AI is wrong?", "Who already does this?", "Why would [operator] use it?", "What did you actually build vs mock?", "How does the least-digital user use it?"

## Step 6 — Save
Write `.hackathon/PITCH.md`. Update STATE.md.

Say: **Next: `/hack:ship`** (compiles everything into one PDF).
