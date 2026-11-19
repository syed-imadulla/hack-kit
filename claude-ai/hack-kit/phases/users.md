> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:users — Think as every real user

> **Phase 4 of 14** · Reads: `BRIEF.md`, `PICK.md` · Writes: `USERS.md`, `ASSUMPTIONS.md` · Next: `/hack:ideate`

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md`, `STATEMENTS.md` and `PICK.md`.


Profile settings used: `questions_per_command`, `explain_steps` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
See the problem through the eyes of everyone it touches, especially the person most likely to be left out.

## Steps

### 1. Ask
Use AskUserQuestion:
- **Who are the real users?** (multiSelect, prefilled with your best guesses: end user, least-digital user, front-line operator, professional or decider, manager or owner, family or helper.)
- **Does anyone on the team have personal experience with this problem?** (Free text.)

### 2. One card per user
| Field | What to write |
|---|---|
| Today, step by step | Concrete details: time, place, device, language |
| Worst step | Where time, money, dignity or safety is lost |
| What they'd refuse | A new app, typing, extra work, sharing data, losing authority |
| What makes them adopt | It saves *them* time, needs no new skills, or someone they trust asks them to |
| Device and channel | Smartphone, keypad phone, shared phone or none; WhatsApp, call, SMS or counter |
| Power to block it | Yes or no, and how |
| Evidence | Label each line `[V]`, `[T]`, `[AI]` or `[?]`. Personas are `[AI]` unless the team has met such people |

### 3. Write the framing
- **POV:** "[User] needs a way to [need] because [insight]."
- **How might we…:** 3–5 statements.
- **Job story:** "When [situation], I want to [motivation], so I can [outcome]."
- **Persona:** name, age, place, device and language, plus a day in their life in 5–8 lines.
- **Who is left out today,** and how the idea must include them (for example: no smartphone → family phone, a normal call, or entry by staff).
- **Contrast motto:** 2–3 options, each built as a pain in numbers plus what changes.

### 4. Pick the motto
Ask (AskUserQuestion) which motto to use, or let the team type their own.

## Output
- `.hackathon/USERS.md` from `templates/users.md`.
- Add every untested belief about users (devices, language, willingness, who decides) to `ASSUMPTIONS.md` (source "users"), with a kill test.
- In STATE.md, tick "users" and set the motto.

## Finish
Give 3 lines: the persona, the POV and the motto.
**Next → `/hack:ideate`.** It explores different ways to solve the problem for this user.
