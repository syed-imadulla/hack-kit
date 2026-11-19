---
name: hack-kit
description: Use at a hackathon when problem statements or themes are given and a team needs to pick one, understand real users, validate, design a simple feasible solution, plan the MVP, and prepare the pitch. Shared rules for every /hack: command.
---

# Hack Kit — shared rules

Hack Kit takes a team from "here are the problem statements" to "locked, validated, buildable idea + MVP plan + pitch + one final PDF". Every `/hack:` command follows these rules.

## 1. State lives in `.hackathon/`
- All work is saved in a `.hackathon/` folder in the current project. Never keep important decisions only in chat.
- Before doing anything, read `.hackathon/STATE.md` (if it exists) and the files the command needs.
- After finishing, update `STATE.md`: current phase, what was decided, what is locked, and the next command.
- If `.hackathon/` does not exist and the command is not `/hack:start`, tell the user to run `/hack:start` first (or offer to run it).
- Templates are in `${CLAUDE_PLUGIN_ROOT}/templates/`. Copy their structure, fill them in.

## 2. Ask, don't assume
- When the team's answer changes the result, ask. Use the AskUserQuestion tool with 2–4 short options (the user can always type their own).
- Ask at most 4 questions at a time. Ask before the expensive step, not after.
- If the team says "you decide", decide, and write the reason in STATE.md.

## 3. The 13 principles
1. **Read the brief like a judge.** Rubric weights decide everything. Score against the real rubric, not your taste.
2. **Pick a problem, not a technology.** "We want to use AI" is not a problem.
3. **Think as every real user:** the end user, the least-digital user (elderly, keypad phone, regional language), front-line staff, the professional, the manager/owner.
4. **Prove it's real.** Sourced numbers, real complaints, a local example, quick chats at the venue.
5. **Check what already exists** and position honestly. "Nobody has done this" is almost always false.
6. **Stress-test in place of a domain expert.** Role-play the expert and the sceptic, then confirm with 2–3 real people.
7. **Lock the core.** Motto, persona, journey, USPs. After lock, fixes go *inside* the core. No new ideas.
8. **Fit with existing systems.** No new hardware, nothing the customer doesn't already have. Work alongside their current software and process.
9. **Keep it simple for the user.** No app download, no typing, works on the simplest device they have.
10. **AI suggests, humans decide.** Safety-critical checks use fixed rules, not AI. Every AI step has a human check and a fallback.
11. **One complete journey for the MVP** with one wow moment. Mock the rest and label it as mocked.
12. **No unsourced numbers.** Every number has a link or is marked `UNVERIFIED`. Targets are labelled as targets.
13. **Simple, everyday English.** Short sentences. Explain like you are telling a friend.

## 4. Judging rule (important)
Hack Kit judges **whether the problem is real and whether the solution truly solves it for real users**. It does **not** judge business viability, market size, revenue or investor appeal. Business points may appear in the pitch only if the rubric asks for them.

## 5. Command order
| Phase | Command | Output |
|---|---|---|
| 1 | `/hack:start` | BRIEF.md, STATE.md |
| 2 | `/hack:decode` | STATEMENTS.md |
| 3 | `/hack:pick` | PICK-VERDICT.md (with trial) |
| 4 | `/hack:users` | USERS.md |
| 5 | `/hack:validate` | EVIDENCE.md |
| 6 | `/hack:compete` | COMPETE.md |
| 7 | `/hack:stress` | STRESS.md (+ CORE.md draft) |
| 8 | `/hack:lock` | CORE.md (locked) |
| 9 | `/hack:plan` | PLAN.md |
| 10 | `/hack:verify` | VERDICT.md (with trial) |
| 11 | `/hack:pitch` | PITCH.md |
| 12 | `/hack:ship` | FINAL.md / FINAL.html / FINAL.pdf |
| any | `/hack:status`, `/hack:court` | — |

Phases 5 and 6 can run in parallel by different teammates.

## 6. `--quick` mode
If the command arguments contain `--quick`, or time left (from BRIEF.md) is under 12 hours for the whole event, use quick mode: shorter outputs, fewer questions, 6 jurors instead of 12, 3 points per side instead of 5.

## 7. Time guide
| Event length | Phases 1–8 (idea locked) | Phases 9–11 |
|---|---|---|
| 24 h | ~60–80 min | ~40 min |
| 36 h | ~2 h | ~1 h |
| 48 h+ | ~3 h (more real validation) | ~1.5 h |

## 8. Mistakes to block
Warn the team immediately if you see any of these:
- Solution looking for a problem; tech-first idea.
- User needs a new app, new hardware, or must type a lot.
- Ignoring the least-digital user.
- AI making a safety-critical decision alone.
- "No competitors".
- Numbers without sources, or targets shown as results.
- Feature creep after lock; drifting away from the motto.
- MVP has many half-features instead of one full journey.
- Demo depends on live internet/API with no fallback recording.
- Slides with heavy text; more slides than the limit.

## 9. Honesty
- Open every source you cite. If a fetch fails, say so; do not guess what it says.
- Label mocked parts as mocked. Never claim results you haven't measured.
- If research tools are unavailable, say so and mark claims `UNVERIFIED`.

## 10. Writing style
Simple Indian English is fine. Short lines. Tables for comparisons. No buzzwords ("revolutionary", "seamless", "leverage", "cutting-edge"). Every output file starts with a 3-line summary.
