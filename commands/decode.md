---
description: "Phase 2 · Decode every problem statement on the spot: real problem, real user, hidden constraints, obvious idea vs smarter angle"
argument-hint: "[statements text or file path] [--quick]"
---

# /hack:decode — Understand every statement in 2 minutes

> **Phase 2 of 14** · Reads: `BRIEF.md` · Writes: `STATEMENTS.md` · Next: `/hack:pick`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md` and `BRIEF.md`.


Profile settings used: `decode_research`, `questions_per_command`, `explain_steps` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Turn each raw problem statement into something the whole team understands, and spot the angle the other 70% of teams will miss.

## Steps

### 1. Get the statements
Take them from the arguments, a file path, an image, or ask the user to paste them. Also ask whether the organiser said anything out loud: hints, favourite topics, sponsor interest.

### 2. Decode each statement
For **each** statement, fill in this card (about 12 lines; about 6 in quick mode):

| Field | What to write |
|---|---|
| In one line | The problem in plain words |
| Who posted it and why | The organiser or sponsor, and what they probably want |
| Real end user | Who suffers this every day |
| How bad, how often, how many | Severity, frequency and the affected population, each labelled `[V]`, `[T]`, `[AI]` or `[?]` |
| Operator | Who would run the solution day to day |
| Least-digital user | Who could be left out (elderly, keypad phone, regional language) |
| Where it happens | Setting, the devices people really have, language, connectivity |
| Hidden constraints | Offline, languages, privacy laws, existing systems, approvals, safety |
| Root cause guess | Ask "why" 3 times |
| Data situation | What exists, whether it's public, what must be mocked |
| Obvious idea | What most teams will build |
| Smarter angle | A different user, a different step, a no-app channel, or fitting into an existing system (`/hack:ideate` explores this properly later) |
| 24/36 h MVP | What one journey could show |
| Unknowns | Questions to ask mentors or organisers |

### 3. Quick reality check
If web tools are available, run 1–2 searches per statement: is the problem real, and what's the biggest existing solution? Link the sources and mark anything unchecked `UNVERIFIED`. In quick mode, skip this unless the user asks for it.

### 4. Summary table
| # | Statement | One-line problem | End user | Obvious idea | Smarter angle | Biggest unknown |

### 5. Drop the obvious misfits
Ask (AskUserQuestion, multiSelect): "Drop any statements right now?" Record each drop with its reason.

## Output
Write `.hackathon/STATEMENTS.md` from `templates/statements.md`. Tick "decode" in STATE.md.

## Finish
Give a 3-line summary with the number of statements and the 2 that look strongest.
**Next → `/hack:pick`.** It scores the statements and puts the best ones on trial.
