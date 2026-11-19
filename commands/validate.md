---
description: "Phase 5 · Prove the problem is real: sourced numbers, real complaints, a local example, and a 5-minute venue interview script"
argument-hint: "[--quick]"
---

# /hack:validate — Prove it's real

> **Phase 5 of 12** · Reads: `PICK.md`, `USERS.md` · Writes: `EVIDENCE.md` · Next: `/hack:compete`

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md`, `PICK.md` and `USERS.md`.

## Goal
Collect three layers of evidence, so no judge can ask "is this even a problem?"

## Steps

### 1. Research (open every source)
| Layer | Look for |
|---|---|
| Numbers | Scale and severity from government data, research papers, official reports and reputed news. Prefer the event's own country or region. |
| Real voices | Complaints in news stories, consumer forums, app reviews of existing solutions and social posts. Paraphrase them, with short quotes only. |
| Local example | One concrete place or story near the event: a named hospital, district or market. |

If web tools aren't available, say so, list what to look up, and mark the claims `UNVERIFIED`.

### 2. Evidence table
| # | Claim | Number or short quote | Source | Date | Strength | Status |

- Strength is strong, medium or weak.
- Status is `VERIFIED` (opened and read) or `UNVERIFIED`.
- Flag any number the team was planning to use that has no source.

### 3. Venue interview script (5 minutes, Mom-Test style)
Ask about people's past behaviour, not their opinion of the idea:
1. "Tell me about the last time you [faced the problem]."
2. "What did you do? How long did it take?"
3. "What have you tried to fix it? Why didn't it work?"
4. "What's the most annoying part?"
5. At the very end, share the one-line idea and ask: "What would stop you from using this?"

### 4. Real chats
Ask (AskUserQuestion) whether they've talked to anyone yet:
- **Add notes now** → fill in the notes table and mark which assumptions are confirmed or broken.
- **Going to talk now** → tell them to run `/hack:validate` again afterwards.
- **Nobody available** → record it as a risk.

## Output
Write `.hackathon/EVIDENCE.md` from `templates/evidence.md`, with the top 3 facts for the pitch first. Tick "validate" in STATE.md.

## Finish
Give 3 lines: how many facts are verified, how many are unverified, and the strongest fact.
**Next → `/hack:compete`**, or `/hack:stress` if compete is already done.
