---
description: Decode every problem statement on the spot — real problem, real end user, hidden constraints, data, obvious idea vs smarter angle
argument-hint: "[paste statements or file path] [--quick]"
---

# /hack:decode

Follow the `hack-kit` skill rules. Read `.hackathon/STATE.md` and `.hackathon/BRIEF.md` first.

Arguments: $ARGUMENTS

## Goal
Turn each raw problem statement into something the team truly understands in 2 minutes.

## Steps
1. Get the statements: from arguments, a file path, an image, or ask the user to paste them. Also ask: "Did the organiser say anything verbally (hints, favourites, sponsor interest)?"
2. For **each** statement, write (keep each to ~12 lines; quick mode ~6):
   - **In one line:** the problem in plain words.
   - **Who posted it and why:** the organiser/sponsor and what they likely want.
   - **Real end user:** who suffers it daily. **Operator:** who would run the solution. **Least-digital user:** who could be left out.
   - **Where it happens:** setting (rural/urban, hospital/farm/office...), devices people actually have, language, connectivity.
   - **Hidden constraints:** offline, regional languages, privacy laws, existing government/company systems, approvals, safety.
   - **Root cause guess:** why this problem exists (ask "why" 3 times).
   - **Data situation:** what data exists, is it public, what must be mocked.
   - **Obvious idea** (what 70% of teams will build) vs **smarter angle** (a different user, a different step, a no-app channel, fitting into an existing system).
   - **What a 24/36 h MVP could show.**
   - **Unknowns to check** (questions for mentors/organisers).
3. If research tools are available, do 1–2 quick searches per statement to check the problem's reality and the biggest existing solution. Link sources. Mark anything unchecked as `UNVERIFIED`. Skip searches in quick mode unless asked.
4. Add a summary table: statement | one-line problem | end user | obvious idea | smarter angle | biggest unknown.
5. Save to `.hackathon/STATEMENTS.md`. Update STATE.md.
6. Ask (AskUserQuestion): "Any statements to drop right now?" (multiSelect) — record drops with reasons.
7. Say: **Next: `/hack:pick`** (scores the statements and puts the top ones on trial).
