---
description: Freeze the core — motto, positioning, persona story, end-to-end journey, who does what, USPs, AI-vs-rules split and human-check table
argument-hint: ""
---

# /hack:lock

Follow the `hack-kit` skill rules. Read STATE.md, USERS.md, EVIDENCE.md, COMPETE.md, STRESS.md and the draft CORE.md first.

Arguments: $ARGUMENTS

## Build CORE.md
Use `${CLAUDE_PLUGIN_ROOT}/templates/core.md`. It must contain:

1. **Name + motto** (one line each).
2. **Positioning line** (from COMPETE.md).
3. **The problem in 2 lines** with the strongest sourced number.
4. **Persona story:** the main persona's journey before vs after, 6–10 short lines.
5. **End-to-end journey:** numbered steps; for each step — who acts, channel/device, what the system does, what the human decides.
6. **Who does what:** table of each role and their exact actions (and what they never have to do).
7. **USPs:** 4–6, each tied to a user pain (not to a technology).
8. **AI vs rules vs humans:**
   | Step | AI does | Fixed rules do | Human decides | If AI fails |
   Safety-critical decisions → rules + human, never AI alone.
9. **Inclusion:** how the least-digital user is covered.
10. **Fit with existing systems:** levels 0–3.
11. **Privacy basics:** what data, how long kept, who sees it.
12. **Out of scope** (things we are deliberately not doing).

## Check against the mistakes list
Run the "Mistakes to block" list from the skill. Fix or flag anything that fails.

## Confirm and freeze
Show a 10-line summary. Ask (AskUserQuestion): "Lock this core?" — "Lock it", "Change something first", "Run a quick trial first (/hack:court --quick)".

When locked:
- Add `LOCKED: <timestamp>` at the top of CORE.md.
- In STATE.md set phase = locked, and add the rule: **"After lock, changes go inside the core. No new features without the captain's OK."**

From now on, if any later command or teammate proposes something that changes the motto, main user or main journey, warn: **"This drifts from the locked core."**

Say: **Next: `/hack:plan`.**
