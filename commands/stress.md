---
description: Role-play the domain expert and a sceptical judge to attack the idea; propose the smallest fix for each weakness that keeps the core
argument-hint: "[--quick]"
---

# /hack:stress

Follow the `hack-kit` skill rules. Read STATE.md, USERS.md, EVIDENCE.md and COMPETE.md first.

Arguments: $ARGUMENTS

## Goal
Replace the missing domain expert. Find every weakness *before* the judges do — and fix it **inside** the core idea.

## Step 1 — Draft the idea
Write a draft of the idea in 8–10 lines: motto, user, the end-to-end journey step by step, who does what, where AI is used, where humans decide.

## Step 2 — Role-play attacks
Play each role in turn, 4–6 hard questions each (2–3 in quick mode):
1. **Senior domain expert** (match to statement: doctor, farmer, lawyer...): "That's not how it works in real life because…", rules, authority, liability.
2. **Front-line worker:** extra work, rush hour, failure cases.
3. **Least-digital user:** "I can't read/type/use this."
4. **Sceptical judge:** "Why not use X that exists?", "Show me evidence", "What if the AI is wrong?", "How is this different?"
5. **Admin / systems owner:** integration, data, privacy, cost of change.

## Step 3 — Fix table
| # | Doubt | Who raised it | Severity (high/med/low) | Smallest fix that keeps the core | Changes the core? (Y/N) |

Rules for fixes:
- Prefer removing a feature over adding one.
- Prefer a human check, a fixed rule or a fallback over "better AI".
- If a fix changes the core (motto, main user, main journey), mark it **Y** and warn: "This drifts from the idea."

## Step 4 — Team decides
Ask (AskUserQuestion, multiSelect): which fixes to accept. Ask separately about any **Y** fix.

Also suggest: "Show the top 3 doubts to 2–3 real people (mentor, someone in the field, family member who works there) and add what they say." If they add answers, update the table.

## Step 5 — Save
Write `.hackathon/STRESS.md` with the table and decisions. Write/refresh a **draft** `.hackathon/CORE.md` with accepted fixes applied. Update STATE.md.

Say: **Next: `/hack:lock`.**
