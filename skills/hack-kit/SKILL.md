---
name: hack-kit
description: Shared rules for every /hack: command. Use at a hackathon when problem statements or themes are given and a team needs to pick a problem, explore ideas, test assumptions, challenge and improve the solution, plan the MVP and prepare the pitch. Think deeper. Challenge harder. Build smarter.
---

# Hack Kit — shared rules

**Think deeper. Challenge harder. Build smarter.**

Hack Kit takes a team from "here are the problem statements" to a well-explored, evidence-labelled, challenged, improved and buildable idea, an MVP plan, a pitch and one final PDF. Every `/hack:` command follows these rules. Read this file once per session, before running any command.

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
| Juror list and domain seats | `<plugin>/skills/hack-court/jurors.json` |
| Trial rules | `<plugin>/skills/hack-court/SKILL.md` |
| Vote counter | `<plugin>/scripts/tally.py` |
| Event profiles | `<plugin>/skills/hack-kit/profiles.json` · `<plugin>/scripts/profile.py` |
| Plan checker | `<plugin>/scripts/plan_check.py` |
| Project linter | `<plugin>/scripts/lint_project.py` |
| PDF compiler | `<plugin>/scripts/compile.py` |

---

## 2. State lives in `.hackathon/`

- All work is saved in a `.hackathon/` folder in the current project. Never keep an important decision only in chat.
- **Before** a command: read `.hackathon/STATE.md` and only the files listed under "Reads". Don't load everything.
- **Summary first:** for each file you only need for context, read the title and `> Summary:` line plus the sections you actually use. Read a whole file only when you are rewriting it. Trials get only their evidence pack, never whole files.
- **After** a command: update `STATE.md`: the phase table, the decisions log (including what was rejected and why), pending items, "Last updated" and the next command.
- Never delete a team's content. When a file is replaced by a new version, move the old one to `.hackathon/history/<NAME>-v<n>.md` first.
- If `.hackathon/` doesn't exist and the command isn't `/hack:start`, `/hack:help` or `/hack:court`, say so and offer to run `/hack:start`.
- Each output file comes from the template with the same name (for example, `CORE.md` comes from `templates/core.md`).

### File map

| Phase | Command | Reads | Writes | Template |
|---|---|---|---|---|
| 1 | `/hack:start` | — | `BRIEF.md`, `STATE.md` | brief, state |
| 2 | `/hack:decode` | BRIEF | `STATEMENTS.md` | statements |
| 3 | `/hack:pick` | BRIEF, STATEMENTS | `PICK.md`, `court/` | scoring, verdict |
| 4 | `/hack:users` | BRIEF, PICK | `USERS.md`, `ASSUMPTIONS.md` | users, assumptions |
| 5 | `/hack:ideate` | BRIEF, PICK, USERS | `IDEAS.md`, `ASSUMPTIONS.md` | ideas |
| 6 | `/hack:validate` | IDEAS, USERS, ASSUMPTIONS | `EVIDENCE.md`, `ASSUMPTIONS.md` | evidence |
| 7 | `/hack:compete` | IDEAS, USERS | `COMPETE.md` | compete |
| 8 | `/hack:stress` | IDEAS, EVIDENCE, COMPETE, ASSUMPTIONS | `STRESS.md`, draft `CORE.md` | stress, core |
| 9 | `/hack:improve` | CORE, latest verdict or STRESS, ASSUMPTIONS | `IMPROVE.md`, `CORE.md` (new version) | improve |
| 10 | `/hack:lock` | all above | `CORE.md` (locked) | core |
| 11 | `/hack:plan` | BRIEF, CORE | `PLAN.md` | plan |
| 12 | `/hack:verify` | BRIEF, EVIDENCE, COMPETE, CORE, PLAN, ASSUMPTIONS | `VERDICT.md`, `court/` | verdict |
| 12b | `/hack:verify --demo` | PLAN, CORE, the built product | `DEMO.md`, `court/demo-<n>/` | demo |
| 13 | `/hack:pitch` | everything | `PITCH.md` | pitch |
| 14 | `/hack:ship` | everything | `SUMMARY.md`, `FINAL.md/.html/.pdf` | summary |
| any | `/hack:assumptions` | ASSUMPTIONS, EVIDENCE | `ASSUMPTIONS.md` | assumptions |
| any | `/hack:court <thing>` | as needed | `court/<case>/` | verdict |
| any | `/hack:status`, `/hack:help` | STATE | — | — |
| post | `/hack:retro` | everything | `RETRO.md` | retro |

`/hack:improve` can also run after any trial (`/hack:pick`, `/hack:verify`, `/hack:court`). Phases 6 and 7 can run in parallel on different teammates' machines (see section 9).

### STATE.md schema (version 2)
`STATE.md` must contain: `Schema version: 2`, `Last updated` (date, time and time zone), the event table, the mode and event length, a phase table (each phase: done / skipped / next / not started), a decisions log (time, decision, why, by, and what was rejected), the locked items, pending items, and the current version of `CORE.md`.

### Upgrading older projects
If `STATE.md` has no `Schema version` line, it's a v1 project. Upgrade it in place:
1. Copy the old file to `.hackathon/history/STATE-v1.md`.
2. Add the missing sections from `templates/state.md`. Keep every existing value and log entry.
3. If `PICK-VERDICT.md` exists and `PICK.md` doesn't, copy it to `PICK.md`.
4. If there's no `ASSUMPTIONS.md`, create it from `templates/assumptions.md` and seed it from `USERS.md`, `STRESS.md` and `CORE.md` if they exist.
5. Log "Upgraded to schema 2" in the decisions log, and tell the user in one line.

### File conventions
- Every output file starts with a title line (`# CORE — <idea name>`) and a one-line `> Summary:` under it.
- Sources go inline as `[short name](link)`, with the date the source was published or read.
- Targets carry `(target)`. Mocked parts carry `(mocked)`.
- Dates and times include the time zone.

---

## 3. Evidence labels

Every claim that matters (a number, a user behaviour, a fact about a competitor, an assumption) carries one label:

| Label | Means | Example |
|---|---|---|
| `[V]` | **Verified.** A source Claude opened and read (link + date), or a result the team measured | `[V] 111 min average OPD wait ([study](link), 2023)` |
| `[T]` | **Team-provided.** The team said it or typed venue notes | `[T] 3 of 4 patients we met had keypad phones` |
| `[AI]` | **AI inference.** Claude's reasoning or estimate. Never presented as fact | `[AI] Nurses probably spend 2 min per check-in` |
| `[?]` | **Unknown.** Needed, but nobody knows yet | `[?] Will the hospital allow WhatsApp?` |

Rules:
- A search-result snippet you didn't open is `[AI]` (write "snippet, not opened"). It becomes `[V]` only after you open the page.
- Only `[V]` and `[T]` can support a "validated" status. `[AI]` can suggest; it can't prove.
- A label only goes up (`[?]` → `[AI]` → `[T]`/`[V]`) when new evidence is added, and the log says what was added.
- Never invent interviews, quotes, test results or juror votes.
- In decks and form answers, drop the labels but keep only `[V]` and `[T]` claims as facts. Present `[AI]` items as estimates or targets.

---

## 4. Asking questions

- When the team's answer changes the result, **ask**. Use the AskUserQuestion tool with 2–4 short options (the user can always type their own answer).
- Ask at most 4 questions at once (2 in quick mode), and ask **before** the expensive step.
- Prefill options from `.hackathon/` files, so the team mostly just confirms.
- If the team says "you decide", decide, and write the reason in the STATE.md decisions log.
- If AskUserQuestion isn't available, ask in plain text with numbered options.

---

## 5. The 17 principles

1. **Read the brief like a judge.** Rubric weights decide everything. Score against the real rubric, not your own taste.
2. **Pick a problem, not a technology.** "We want to use AI" is not a problem.
3. **Think as every real user:** the end user, the least-digital user (elderly, keypad phone, regional language), front-line staff, the professional, and the manager or owner.
4. **Prove it's real** with sourced numbers, real complaints, a local example and quick chats at the venue.
5. **Check what already exists** and position the idea honestly. "Nobody has done this" is almost always false.
6. **Stress-test in place of a domain expert.** Role-play the expert and the sceptic, then confirm with 2–3 real people.
7. **Lock the core.** The problem, the main user, the core journey and the motto are protected after lock. Solution details can still improve through `/hack:improve`.
8. **Fit with existing systems.** No new hardware, nothing the customer doesn't already have.
9. **Keep it simple for the user:** no app download, no typing, works on the simplest device they have.
10. **AI suggests, humans decide.** Safety-critical checks use fixed rules, not AI. Every AI step has a human check and a fallback.
11. **One complete journey for the MVP,** with one wow moment. Every feature needs a reason. Mock the rest and label it.
12. **No unsourced numbers.** Every number is labelled. Targets are labelled as targets.
13. **Simple, everyday English.** Short sentences. Explain it the way you'd tell a friend.
14. **Evidence before confidence.** Label every claim. A confident AI answer is still `[AI]`.
15. **Test the riskiest assumption first.** If it being false would collapse the idea, test it before anything else.
16. **Different technology isn't innovation.** Differentiate by what's better *for the user*, not by which model you used.
17. **Keep the decision history.** Record what was chosen, what was rejected, and why.

---

## 6. The judging rule

Hack Kit judges **whether the problem is real and whether the solution truly solves it for real users**. It does **not** judge business viability, market size, revenue or investor appeal. Business points appear only in `/hack:pitch`, and only if the rubric asks for them.

---

## 7. Event profiles, modes and the time guard

### Profiles (v1.1)
`/hack:start` sets a profile: **event type** (college, SIH/government, AI/ML, ideathon, hardware, corporate) · **length** (12h, 24h, 36h, 48h+) · **team size and experience** (beginner, mixed, advanced) · **judging focus** (balanced, technical, innovation-impact, business). It runs:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/profile.py" --type <t> --length <l> --experience <e> --focus <f> --team <n>
```
and pastes the output into STATE.md under `## Profile`. **Every command reads its numbers from that table**: how many ideas, trials, jurors, experiments and improve rounds; plan and pitch depth; which phases to skip; whether to explain each step. If STATE.md has no Profile (older projects), use the Full/Quick tables below.

- Beginner teams: explain each step in 2 plain lines first, define terms the first time, and ask at most 2 questions.
- Skipped phases are marked `skipped (profile: <type>)` in the phase table. The team can still run them.
- `--quick` on any command always means the quick column below, whatever the profile says.
- The focus changes scoring weights only. **Hack Court never judges business viability**, whatever the focus.

### Modes
**Quick** is on when `--quick` is passed, or when the profile says `mode: quick` (12 h events).

| | Full | Quick |
|---|---|---|
| Output length | normal | about half |
| Questions per command | up to 4 | up to 2 |
| Jurors per trial | 12 | 7 |
| Points per side | 5 | 3 |
| Web research | yes | only for top claims |

### Time guard: what the new thinking steps cost
| Step | Full (24 h+) | Quick or 12 h event |
|---|---|---|
| `/hack:ideate` | 6 directions × 2 ideas + constraint removal (~15 min) | 3 directions × 1 idea, no combinations (~5 min) |
| `/hack:assumptions` | all assumptions, kill test on each | top 5 only |
| `/hack:validate` experiments | up to 3 experiment cards | 1 card (the riskiest assumption) |
| `/hack:improve` | up to 2 rounds, quick re-trial each round | 1 round, re-trial only if the team asks |
| Trials in `/hack:pick` | up to 3 | up to 2, or `--no-trial` |

If time left (STATE.md) is less than the planned time for the remaining thinking phases, say so and offer the quick version of the next command.

### Time guide
| Event length | Phases 1–10 (idea locked) | Phases 11–13 |
|---|---|---|
| 12 h | ~45 min (quick) | ~30 min |
| 24 h | 80–100 min | ~40 min |
| 36 h | ~2.5 h | ~1 h |
| 48 h+ | ~3.5 h (more real validation) | ~1.5 h |

---

## 8. Mistakes to block

Warn the team **as soon as** you see one of these:

| # | Mistake | Why it hurts |
|---|---|---|
| 1 | A solution looking for a problem; a tech-first idea | Judges ask "who needs this?" |
| 2 | The user needs a new app, new hardware, or has to type a lot | Real users won't adopt it |
| 3 | The least-digital user is ignored | Excludes the people who suffer most |
| 4 | AI makes a safety-critical decision alone | Unsafe, and judges catch it |
| 5 | "No competitors" | Shows no research was done |
| 6 | Numbers without labels, or targets shown as results | Credibility loss |
| 7 | Feature creep after lock; drifting from the problem or main user | Half-built demo, muddled pitch |
| 8 | MVP has many half-features instead of one full journey | Nothing works end to end |
| 9 | Demo depends on live internet or APIs with no backup recording | Demo-day failure |
| 10 | Slides with heavy text, or more slides than the limit | Lost marks on presentation |
| 11 | Treating `[AI]` claims or AI juror votes as proof | False confidence |
| 12 | Only one idea ever considered | The obvious idea is what most teams build |

---

## 9. Parallel work

- **One owner per file.** When teammates run `/hack:validate` and `/hack:compete` on different machines, each writes only its own file (`EVIDENCE.md` or `COMPETE.md`).
- **Shared files get pending sections.** Updates to `ASSUMPTIONS.md` (and anything meant for STATE.md) go at the end, under `## Pending from <name> — <time>`. Never edit someone else's table rows directly.
- **Only the captain's machine updates `STATE.md`,** and merges pending sections with `/hack:status --merge`. That moves each pending row into the main table, removes duplicates, keeps both versions of a row the two people changed differently (marked `CONFLICT`) for the captain to choose, and logs the merge.
- **Sync through git:** pull before starting a command and push right after it. If git reports a conflict in a `.hackathon/` file, keep both versions inside the file, mark the block `CONFLICT`, and run `/hack:status --merge`.
- `/hack:status` and `scripts/lint_project.py` flag pending sections that haven't been merged, and `CONFLICT` markers.

---

## 10. Honesty

- Open every source you cite. If a fetch fails, say so and don't guess what the page says.
- Label mocked parts as mocked, and never claim results that haven't been measured.
- If research tools aren't available, say so and mark the claims `[?]` or `[AI]`.
- Simulated jurors, experts and users are perspectives, not real people. Say so whenever their output is shown.

---

## 11. Writing style

- Simple Indian English is fine. Short lines. Use tables for comparisons.
- Avoid buzzwords like "revolutionary", "seamless", "leverage" and "cutting-edge".
- End every command with a short summary of 3–5 lines, then **Next → `/hack:<command>`**.
