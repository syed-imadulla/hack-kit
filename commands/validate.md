---
description: Prove the problem is real — sourced numbers, real complaints, a local example, UNVERIFIED flags, and a 5-minute venue interview script
argument-hint: "[--quick]"
---

# /hack:validate

Follow the `hack-kit` skill rules. Read STATE.md, BRIEF.md, PICK-VERDICT.md and USERS.md first.

Arguments: $ARGUMENTS

## Goal
Three layers of evidence, so no judge can say "is this even a problem?"

## Step 1 — Research (if web tools are available)
Find and **open** each source (don't cite from snippets alone):
1. **Numbers:** scale and severity from government data, research papers, reputed news, official reports. Prefer the country/region of the event.
2. **Real voices:** complaints from news stories, consumer forums, app reviews of existing solutions, social posts. Paraphrase; short quotes only.
3. **Local example:** one concrete story or place near the event (a named hospital, district, market...).

If web tools aren't available, say so, list what to look up, and mark claims `UNVERIFIED`.

## Step 2 — Evidence table
Use `${CLAUDE_PLUGIN_ROOT}/templates/evidence.md`:

| # | Claim | Number / quote (short) | Source (link) | Date | Strength (strong/medium/weak) | Status |

Status = VERIFIED (opened and read) / UNVERIFIED. Flag any number the team already planned to use that has no source.

## Step 3 — Venue interview script
Write a 5-minute script for mentors, attendees, staff or anyone at the venue who matches a user type. Use Mom-Test rules: ask about their past behaviour, not opinions about your idea.
- "Tell me about the last time you [faced the problem]."
- "What did you do? How long did it take?"
- "What have you tried to fix it? Why did it fail?"
- "What's the most annoying part?"
- Only at the end: show the one-line idea, ask "What would stop you from using this?"
Add a **notes table**: person type | what they said | does it support / weaken our idea.

## Step 4 — Wait for real chats
Ask (AskUserQuestion): "Have you talked to anyone yet?" Options: "Add notes now", "Going to talk now — I'll run /hack:validate again", "Skip — no one available". If they add notes, put them in the notes table and mark which assumptions they confirm or break.

## Step 5 — Save
Write `.hackathon/EVIDENCE.md`: the 3 strongest facts for the pitch (with links), the full table, the script, the notes, and **"Assumptions still unproven"**. Update STATE.md.

Say: **Next: `/hack:compete`** (or `/hack:stress` if compete is done).
