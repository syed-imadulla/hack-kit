---
description: Think as every real user and stakeholder — today's journey, worst step, refusals, adoption triggers; write POV, How-Might-We, job story, persona and motto
argument-hint: "[--quick]"
---

# /hack:users

Follow the `hack-kit` skill rules. Read STATE.md, BRIEF.md, STATEMENTS.md and PICK-VERDICT.md first.

Arguments: $ARGUMENTS

## Step 1 — Ask
AskUserQuestion:
- Who are the real users? Offer your best list (end user, least-digital user, front-line operator, professional/decider, manager/owner, family/helper) as multiSelect; let them add.
- Does anyone on the team have personal experience with this problem? (They can type it.)

## Step 2 — Stakeholder views
For each user/stakeholder, using `${CLAUDE_PLUGIN_ROOT}/templates/pov.md`:
- **Today:** what they do step by step (be concrete: time, place, device, language).
- **Worst step:** where time, money, dignity or safety is lost.
- **What they'd refuse:** new app, typing, extra work, sharing data, losing authority...
- **What makes them adopt:** saves time *for them*, no new skills, someone they trust asks them to.
- **Their device and channel:** smartphone/keypad/shared phone/none; WhatsApp/call/SMS/counter.
- **Their power:** can they block this? (e.g. the doctor, the clerk, the admin)

## Step 3 — Write
- **POV statement:** "[User] needs a way to [need] because [insight]."
- **3–5 How-Might-We statements.**
- **Job story:** "When [situation], I want to [motivation], so I can [outcome]."
- **Main persona** with a name and a short day-in-the-life (5–8 lines), like "Ramesh uncle, 58, diabetic, keypad phone, Kannada".
- **Contrast motto** (one line, memorable): e.g. "Patients wait 2 hours to get 2 minutes. We make those 2 hours count."
- **Who is left out today, and how our idea must include them** (no smartphone → family phone, call, staff entry).

## Step 4 — Save
Write `.hackathon/USERS.md`. Update STATE.md. Ask the team (AskUserQuestion) to pick the motto from 2–3 options or type their own.

Say: **Next: `/hack:validate`** (can run in parallel with `/hack:compete`).
