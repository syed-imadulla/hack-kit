> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:pitch — Say it so judges remember it

> **Phase 13 of 14** · Reads: everything · Writes: `PITCH.md` · Next: `/hack:ship`

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md`, `EVIDENCE.md`, `COMPETE.md`, `CORE.md`, `PLAN.md` and `VERDICT.md`. On the starter path, `EVIDENCE.md` and `VERDICT.md` usually don't exist: use `ASSUMPTIONS.md`, `STRESS.md` and the pick trial instead, and don't treat the missing files as a problem.


Profile settings used: `pitch_depth`, `drill_questions` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
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
- What did you actually build, and what is mocked? Take this answer from the DEMO.md ladder if it exists. If not, mark it *"(plan: update after /hack:verify --demo)"*, because what was planned is rarely what gets built.
- How does the least-digital user use it?

## Starter path (STATE.md → Profile → Path: starter)
This is the last of the 5 commands. Keep the pitch short (the profile's `pitch_depth`) and offer the drill once at the end: "Want to practise with simulated judges? `/hack:pitch --drill`". Many first-time teams skip `/hack:verify`, so take the built-vs-mocked answer from `DEMO.md` if it exists, and otherwise mark it *"(plan: update after building)"*.

## Output
Write `.hackathon/PITCH.md` from `templates/pitch.md`. Tick "pitch" in STATE.md.

## Finish
Give the one-line pitch and the slide count.
**Next → `/hack:ship`.** It compiles everything into one PDF. On the starter path this is optional.

---

## Drill mode: `/hack:pitch --drill`

Live practice with a simulated judging panel. Run it after the deck outline exists, and again after `/hack:verify --demo`. The number of questions comes from the profile (`drill_questions`).

### R1. Build the panel
Pick 3 simulated judges from the rubric in BRIEF.md: one for each of the top 3 weighted criteria (for example, a domain expert for Problem, a technical judge for Feasibility, an impact judge for Impact). For SIH and corporate profiles, the statement owner is always one of them. Say once: *"Simulated judges: practice, not a prediction of real scores."*

### R2. Build the question bank (hardest first)
Draw questions from:
- the prosecution's points and the GUILTY or INSUFFICIENT EVIDENCE reasons in the latest verdicts;
- open "collapses" and "weakens" assumptions;
- the closest competitor ("How is this different from X?");
- every mocked feature, every target number and every claim in the deck;
- the five standard questions in step 5 above.

### R3. Ask, one question at a time
For each question:
1. A judge asks it, in character. Wait for the team's typed answer. **Never write the team's answer for them.**
2. Score it 1–5 on four things:
   - **clarity:** a direct answer in the first sentence;
   - **evidence:** uses `[V]` or `[T]` facts, not hopes;
   - **honesty:** admits mocks, targets and unknowns;
   - **length:** 30 seconds spoken, about 75 words or fewer.
3. Show a **stronger answer**, built only from facts in `.hackathon/` files. If a strong answer needs a fact the team doesn't have, say "you need: <fact>" instead of inventing it.

Allow "skip" and "repeat". Stop early if the team asks.

### R4. Pitch vs product check
Compare every claim in PITCH.md and the deck outline with DEMO.md's feature ladder (or PLAN.md if there's no demo check yet):

| Claim | Backed by | Status |
|---|---|---|

Status is ✅ tested, ⚠️ built but untested, ❌ planned or mocked but described as working. Every ❌ must be reworded ("we will…", "mocked in this demo") or removed. **A strong pitch can't make up for an unbuilt feature.**

### R5. Timing check
Count the words in the 90-second demo script (about 150 spoken words per minute). Mark any section that runs long.

### Output (drill mode)
Add a `## Drill <n>` section to `.hackathon/PITCH.md`:
- the questions, a one-line summary of each answer, the scores, and the stronger answers;
- average scores, plus the 3 answers to rehearse again;
- the pitch vs product table and the timing check.

### Finish (drill mode)
Give 3 lines: the average score, the weakest topic, and the claims you must reword.
**Next →** rehearse the 3 weakest answers out loud, then `/hack:pitch --drill` again, or `/hack:ship`.
