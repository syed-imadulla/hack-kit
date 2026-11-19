---
name: hack-kit
description: Shared rules for every /hack: command. Use at a hackathon when problem statements or themes are given and a team needs to pick one, understand real users, validate, design a simple feasible solution, plan the MVP and prepare the pitch.
---

# Hack Kit — shared rules

Hack Kit takes a team from "here are the problem statements" to "locked, validated, buildable idea + MVP plan + pitch + one final PDF". Every `/hack:` command follows these rules. Read this file once per session, before running any command.

---

## 1. Finding the plugin files

Plugin files are under `${CLAUDE_PLUGIN_ROOT}`. If that text shows up unexpanded, or the path doesn't exist, find the root once and reuse it for the rest of the session:

```bash
dirname "$(dirname "$(dirname "$(find ~/.claude -path '*skills/hack-court/jurors.json' 2>/dev/null | head -1)")")"
```

In this file and in the commands, `<plugin>` means that root.

| What | Where |
|---|---|
| Templates | `<plugin>/templates/<name>.md` |
| Juror list | `<plugin>/skills/hack-court/jurors.json` |
| Trial rules | `<plugin>/skills/hack-court/SKILL.md` |
| PDF compiler | `<plugin>/scripts/compile.py` |

---

## 2. State lives in `.hackathon/`

- All work is saved in a `.hackathon/` folder in the current project. Never keep an important decision only in chat.
- **Before** a command: read `.hackathon/STATE.md` and the files listed under "Reads".
- **After** a command: update `STATE.md` (phase checklist, decisions log, next command).
- If `.hackathon/` doesn't exist and the command isn't `/hack:start`, `/hack:help` or `/hack:court`, say so and offer to run `/hack:start`.
- Each output file is built from the template with the same name (for example, `CORE.md` comes from `templates/core.md`).

### File map

| Phase | Command | Reads | Writes | Template |
|---|---|---|---|---|
| 1 | `/hack:start` | — | `BRIEF.md`, `STATE.md` | brief, state |
| 2 | `/hack:decode` | BRIEF | `STATEMENTS.md` | statements |
| 3 | `/hack:pick` | BRIEF, STATEMENTS | `PICK.md` + `court/` | scoring, verdict |
| 4 | `/hack:users` | BRIEF, PICK | `USERS.md` | users |
| 5 | `/hack:validate` | PICK, USERS | `EVIDENCE.md` | evidence |
| 6 | `/hack:compete` | PICK, USERS | `COMPETE.md` | compete |
| 7 | `/hack:stress` | USERS, EVIDENCE, COMPETE | `STRESS.md`, draft `CORE.md` | stress, core |
| 8 | `/hack:lock` | all above | `CORE.md` (locked) | core |
| 9 | `/hack:plan` | BRIEF, CORE | `PLAN.md` | plan |
| 10 | `/hack:verify` | BRIEF, EVIDENCE, COMPETE, CORE, PLAN | `VERDICT.md` + `court/` | verdict |
| 11 | `/hack:pitch` | everything | `PITCH.md` | pitch |
| 12 | `/hack:ship` | everything | `SUMMARY.md`, `FINAL.md/.html/.pdf` | summary |
| — | `/hack:status`, `/hack:help`, `/hack:court` | STATE | `court/<case>/` | verdict |

Phases 5 and 6 can run in parallel on different teammates' machines. Merge their files into the shared repo afterwards.

### File conventions
- Every output file starts with a title line (`# CORE — <idea name>`) and a one-line `> Summary:` under it.
- Sources go inline as `[short name](link)`. Unchecked claims carry the tag `UNVERIFIED`.
- Targets carry the tag `(target)`. Mocked parts carry the tag `(mocked)`.
- Dates and times include the time zone.

---

## 3. Asking questions

- When the team's answer changes the result, **ask**. Use the AskUserQuestion tool with 2–4 short options (the user can always type their own answer).
- Ask at most 4 questions at once, and ask **before** the expensive step.
- Prefill options from `.hackathon/` files, so the team mostly just confirms.
- If the team says "you decide", decide, and write the reason in the STATE.md decisions log.
- If AskUserQuestion isn't available, ask in plain text with numbered options.

---

## 4. The 13 principles

1. **Read the brief like a judge.** Rubric weights decide everything. Score against the real rubric, not your own taste.
2. **Pick a problem, not a technology.** "We want to use AI" is not a problem.
3. **Think as every real user:** the end user, the least-digital user (elderly, keypad phone, regional language), front-line staff, the professional, and the manager or owner.
4. **Prove it's real** with sourced numbers, real complaints, a local example and quick chats at the venue.
5. **Check what already exists** and position the idea honestly. "Nobody has done this" is almost always false.
6. **Stress-test in place of a domain expert.** Role-play the expert and the sceptic, then confirm with 2–3 real people.
7. **Lock the core:** motto, persona, journey, USPs. After lock, fixes go *inside* the core. No new ideas.
8. **Fit with existing systems.** No new hardware, nothing the customer doesn't already have. Work alongside their current software and process.
9. **Keep it simple for the user:** no app download, no typing, works on the simplest device they have.
10. **AI suggests, humans decide.** Safety-critical checks use fixed rules, not AI. Every AI step has a human check and a fallback.
11. **One complete journey for the MVP,** with one wow moment. Mock the rest and label it as mocked.
12. **No unsourced numbers.** Every number has a link or is marked `UNVERIFIED`. Targets are labelled as targets.
13. **Simple, everyday English.** Short sentences. Explain it the way you'd tell a friend.

---

## 5. The judging rule

Hack Kit judges **whether the problem is real and whether the solution truly solves it for real users**. It does **not** judge business viability, market size, revenue or investor appeal. Business points appear only in `/hack:pitch`, and only if the rubric asks for them.

---

## 6. Modes

| | Full | Quick |
|---|---|---|
| Turned on by | default | `--quick` in arguments, or under 12 h for the whole event (STATE.md) |
| Output length | normal | about half |
| Questions per command | up to 4 | up to 2 |
| Jurors per trial | 12 | 6 |
| Points per side | 5 | 3 |
| Web research | yes | only for top claims |

### Time guide
| Event length | Phases 1–8 (idea locked) | Phases 9–11 |
|---|---|---|
| 24 h | 60–80 min | ~40 min |
| 36 h | ~2 h | ~1 h |
| 48 h+ | ~3 h (more real validation) | ~1.5 h |

---

## 7. Mistakes to block

Warn the team **as soon as** you see one of these:

| # | Mistake | Why it hurts |
|---|---|---|
| 1 | A solution looking for a problem; a tech-first idea | Judges ask "who needs this?" |
| 2 | The user needs a new app, new hardware, or has to type a lot | Real users won't adopt it |
| 3 | The least-digital user is ignored | Excludes the people who suffer most |
| 4 | AI makes a safety-critical decision alone | Unsafe, and judges catch it |
| 5 | "No competitors" | Shows no research was done |
| 6 | Numbers without sources, or targets shown as results | Credibility loss |
| 7 | Feature creep after lock; drifting from the motto | Half-built demo, muddled pitch |
| 8 | MVP has many half-features instead of one full journey | Nothing works end to end |
| 9 | Demo depends on live internet or APIs with no backup recording | Demo-day failure |
| 10 | Slides with heavy text, or more slides than the limit | Lost marks on presentation |

---

## 8. Honesty

- Open every source you cite. If a fetch fails, say so and don't guess what the page says.
- Label mocked parts as mocked, and never claim results that haven't been measured.
- If research tools aren't available, say so and mark the claims `UNVERIFIED`.
- Never invent juror votes, interview notes or quotes.

---

## 9. Writing style

- Simple Indian English is fine. Short lines. Use tables for comparisons.
- Avoid buzzwords like "revolutionary", "seamless", "leverage" and "cutting-edge".
- End every command with a short summary of 3–5 lines, then **Next → `/hack:<command>`**.
