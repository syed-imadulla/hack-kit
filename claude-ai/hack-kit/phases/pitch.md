> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:pitch — Say it so judges remember it

> **Phase 13 of 14** · Reads: everything · Writes: `PITCH.md` · Next: `/hack:ship`

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md`, `EVIDENCE.md`, `COMPETE.md`, `CORE.md`, `PLAN.md` and `VERDICT.md`.

## Goal
A pitch that proves the problem is real and the solution works, in the format and limits the event demands.

## Steps

### 1. Ask
Use AskUserQuestion, prefilled from BRIEF.md:
- Slide limit (default 7) and format (PPT, PDF, Google Slides or none).
- Pitch length (2, 3 or 5 minutes).
- Form questions to answer (paste them, with word limits).

### 2. One-liners
- **One-line pitch** (20 words or fewer).
- **Opening line** aimed at the most heavily weighted rubric item.
- **Motto** (from CORE.md).

### 3. Deck outline
Use `templates/pitch.md`. Stay **exactly within** the slide limit. For each slide, give a full-sentence headline, 3–5 short items, the visual and a source line.

Default 7-slide flow:
1. Hook, team name and track
2. Problem with evidence (numbered sources)
3. The solution in one line, 3 cards and a "how we compare" table
4. How it works: AI agents, human checks, and rules instead of AI for safety
5. The persona's journey end to end, plus the USPs
6. Tech stack and architecture (a clean diagram with MVP tags)
7. Impact (marked as targets), the pilot plan and the motto

Rules: no heavy text, readable fonts. Only `[V]` and `[T]` claims are stated as facts; `[AI]` items become estimates or targets. Drop the labels on the slides, but keep the sources.

### 4. Form answers
Answer each form question within its word limit. Lead with the strongest point for that question, in simple English.

### 5. Judge Q&A
Write 12–15 likely questions with answers of 2–3 lines. Draw them from the prosecution's points, the GUILTY reasons, the rubric and the competitors. Always include:
- What if the AI is wrong?
- Who already does this?
- Why would [operator] use it?
- What did you actually build, and what is mocked?
- How does the least-digital user use it?

## Output
Write `.hackathon/PITCH.md` from `templates/pitch.md`. Tick "pitch" in STATE.md.

## Finish
Give the one-line pitch and the slide count.
**Next → `/hack:ship`.** It compiles everything into one PDF.
