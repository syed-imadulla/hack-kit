---
description: Find existing apps, portals, research and past hackathon projects; build an honest gap table and show how the idea fits alongside existing systems
argument-hint: "[--quick]"
---

# /hack:compete

Follow the `hack-kit` skill rules. Read STATE.md, PICK-VERDICT.md and USERS.md first.

Arguments: $ARGUMENTS

## Step 1 — Ask
AskUserQuestion: "Any competitor or existing system you already know?" (they can type names) and "Which existing system must we work alongside?" (e.g. hospital software, government portal, ERP, school app — offer best guesses).

## Step 2 — Search (open every source)
Look for:
- Commercial products and startups (incl. ones that shut down — why?).
- Government portals and public schemes.
- Big-company pilots.
- Research papers / prototypes.
- Past hackathon projects (Devpost, GitHub, college fests).
- The **workaround** people use today (WhatsApp, paper, phone calls).

Aim for 6–10 entries (3–5 in quick mode). Never say "no competitors".

## Step 3 — Gap table
Use `${CLAUDE_PLUGIN_ROOT}/templates/gap-table.md`. Rows = the 5–7 things that matter **to the real user** (e.g. works without app, regional voice, works for least-digital user, human check, fits existing system, cost to user). Columns = competitors + our idea. Use Yes / Partly / No / Not found. Add the note: *"Not found = not seen in public material, not proof it doesn't exist."*

## Step 4 — Positioning
- **Closest competitor** and the honest difference in one line.
- **Where we are weaker** (be honest — judges respect this).
- **Coexistence:** how our idea works *alongside* existing systems in levels:
  - Level 0: standalone, zero integration (e.g. only a token number).
  - Level 1: uses an existing ID or QR scheme.
  - Level 2: exports a standard format (FHIR, CSV, API).
  - Level 3: full integration by agreement.
- **Positioning line:** "For [user] who [problem], [name] is a [category] that [key benefit]. Unlike [closest], we [difference]."

## Step 5 — Save
Write `.hackathon/COMPETE.md`. Update STATE.md. If a competitor already does exactly the idea, warn clearly and suggest 2 angles that keep the core (different user, different step, different channel).

Say: **Next: `/hack:stress`.**
