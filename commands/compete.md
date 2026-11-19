---
description: "Phase 7 · Find what already exists, build an honest gap table, and show how the idea fits alongside existing systems"
argument-hint: "[--quick]"
---

# /hack:compete — Know what already exists

> **Phase 7 of 14** · Reads: `IDEAS.md`, `USERS.md` · Writes: `COMPETE.md` · Next: `/hack:stress`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `IDEAS.md` and `USERS.md`.


Profile settings used: `sources_to_open`, `questions_per_command` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Position the idea honestly against what exists, and show that it works **alongside** the systems people already use instead of replacing them.

## Steps

### 1. Ask
Use AskUserQuestion:
- **Any competitor or existing system you already know?** (Free text.)
- **Which existing system must we work alongside?** Prefill your best guesses: hospital software, a government portal, an ERP, a school app.

### 2. Search (open every source)
Aim for 6–10 entries (3–5 in quick mode) from:
- startups and products, including ones that shut down, and why;
- government portals and schemes;
- big-company pilots;
- research prototypes;
- past hackathon projects (Devpost, GitHub);
- **today's workaround**: WhatsApp, paper, phone calls.

For each entry, note the link, the date you checked it, and its biggest weakness *for the user*. Label findings `[V]` only if you opened the source.

Never write "no competitors".

### 3. Gap table
Rows are what matters **to the user**, not features. Columns are each competitor plus our idea. Each cell is Yes, Partly, No or Not found.
Add this note under the table: *"Not found = not seen in public material, not proof it doesn't exist."*

### 4. Differentiation
- **What already exists, what it fails to solve, and what opportunity remains:** one line each.
- **Differentiation statement,** based on user value. For example: "Existing systems digitise registration. We remove the effort for patients who can't use digital registration." Not "we use AI to revolutionise…".
- **Warning:** different technology isn't innovation. Swapping in an LLM isn't a difference unless the user gets something better.

### 5. Positioning
- **Closest competitor,** and the honest difference in one line.
- **Where we're weaker.** Be honest; judges respect it.
- **Coexistence levels:**
  - L0: standalone, with zero integration.
  - L1: uses an existing ID or QR scheme.
  - L2: exports a standard format (FHIR, CSV or an API).
  - L3: full integration, by agreement.
- **Positioning line:** "For [user] who [problem], [name] is a [category] that [benefit]. Unlike [closest], we [difference]."

### 6. Overlap alarm
If something already does exactly this idea, say so clearly and suggest 2 angles that keep the core: a different user, a different step, or a different channel.

## Output
Write `.hackathon/COMPETE.md` from `templates/compete.md`. Tick "compete" in STATE.md.

## Finish
Give 3 lines: the closest competitor, our honest difference, and the positioning line.
**Next → `/hack:stress`.**
