# Hack Kit 🏁

**From "here are the problem statements" to a locked, validated, buildable hackathon idea, MVP plan, pitch and one final PDF.**

Hack Kit is a Claude Code plugin with `/hack:` commands. Each step asks your team the questions that matter, saves its work in a `.hackathon/` folder, and tells you the next command. At two key points it puts your idea **on trial** in front of 12 independent AI jurors.

> Hack Kit judges **whether the problem is real and whether your solution truly solves it for real users**. It does **not** judge business viability, revenue or market size.

Built by Team Udaan from what we learned making *OPD Saathi* (see `examples/`).

---

## Install

### Claude Code (recommended)
```
/plugin marketplace add syed-imadulla/hack-kit
/plugin install hack@hack-kit
```
Restart Claude Code if the commands don't show up. Type `/hack:` to see them.

**Manual install:** clone the repo and run `/plugin marketplace add ./hack-kit`, then `/plugin install hack@hack-kit`.

### claude.ai (for teammates without Claude Code)
1. Zip the folder `claude-ai/hack-kit/` (the zip must contain `hack-kit/SKILL.md`).
2. In claude.ai: **Settings → Capabilities → Skills → Upload skill**.
3. In a chat, type `hack start` or paste your problem statements.

No skills? Paste `claude-ai/PROMPT.md` into any chat.

---

## Commands

| # | Command | What it does | Saves |
|---|---|---|---|
| 1 | `/hack:start` | Sets up the project; reads the brief like a judge (rubric, limits, team, time) | BRIEF.md, STATE.md |
| 2 | `/hack:decode` | Decodes every statement: real problem, real user, hidden constraints, obvious idea vs smarter angle | STATEMENTS.md |
| 3 | `/hack:pick` | Rubric-weighted scoring + red flags, then **trial** of the top 2–3; captain picks | PICK-VERDICT.md |
| 4 | `/hack:users` | Thinks as every real user; POV, How-Might-We, persona, motto | USERS.md |
| 5 | `/hack:validate` | Sourced facts, real complaints, venue interview script | EVIDENCE.md |
| 6 | `/hack:compete` | Existing solutions, gap table, fit with existing systems | COMPETE.md |
| 7 | `/hack:stress` | Role-plays the domain expert and sceptic; smallest fixes inside the core | STRESS.md |
| 8 | `/hack:lock` | Freezes motto, journey, USPs, AI-vs-rules-vs-humans | CORE.md |
| 9 | `/hack:plan` | One-journey MVP, build/mock/cut, stack, roles, 90-sec demo, AI tests | PLAN.md |
| 10 | `/hack:verify` | **Trial** of the solution + rubric score + mistakes and claims check | VERDICT.md |
| 11 | `/hack:pitch` | Deck outline within the slide limit, form answers, judge Q&A | PITCH.md |
| 12 | `/hack:ship` | Compiles everything into one document | FINAL.md / .html / .pdf |
| — | `/hack:status` | Where you are, what's locked, time left, next command | — |
| — | `/hack:court <thing>` | Put anything on trial: an idea, a feature, a pitch | court/… |

Add `--quick` to any command for a faster version (6 jurors, shorter outputs).

---

## The trial ⚖️

Used in `/hack:pick`, `/hack:verify` and `/hack:court`.

1. **Case file:** about 120 words on the problem, users, solution and constraints.
2. **Prosecution:** the strongest case that it does **not** solve a real problem for real users (5 points).
3. **Defense:** the strongest case that it **does** (5 points).
4. **Jury:** 12 jurors, each a **separate subagent** who can't see the others, vote GUILTY / NOT GUILTY with confidence 1–10, a reason and a fix.
5. **Judge:** uses only real votes (never invents any), and gives ratings /10, the top 3 fail reasons, the top 3 fixes, a 30-minute venue check and "If I were your team…".

**The jury:** actual end user · least-digital user · front-line worker · domain professional · today's-workaround user · root-cause analyst · "already exists" researcher · safety & ethics reviewer · systems person · engineer · statement-owner judge · sceptic. No investors or accountants.

**Ratings:** problem is real · problem matters · fits root cause · works for real users · fits existing systems · safe · buildable & demo-able · different from what exists.

---

## How to use it at a hackathon

### Before the event
- Fix roles: captain (final decider), builder(s), researcher, pitcher.
- Freeze your default stack so you don't debate it on the day.
- Each person lists 10 real frustrations they've seen. Real problems beat invented ones.
- Line up 2–3 people you can call (a doctor, farmer, teacher, shopkeeper…).
- Install Hack Kit and do a 15-minute dry run with an old problem statement.

### During the event
| Time after statements | Do |
|---|---|
| 0:00 | `/hack:start` (or do it before statements are out) |
| 0:05 | `/hack:decode` |
| 0:20 | `/hack:pick` → captain decides |
| 0:35 | `/hack:users` |
| 0:45 | `/hack:validate` ‖ `/hack:compete` (split the team) + venue chats |
| 1:10 | `/hack:stress` |
| ~1:30 | `/hack:lock` → **idea freeze** |
| then | `/hack:plan` → `/hack:verify` → build |
| before judging | `/hack:pitch` → `/hack:ship` |

**Code freeze** 3–4 hours before judging. Record a backup demo video.

### Team use
- One person runs the commands in the shared repo, so `.hackathon/` is the single source of truth. Commit it to git so everyone sees the same state.
- Others work in parallel: one on `/hack:validate`, one on `/hack:compete`, one talking to people at the venue.
- The captain makes the final call. The verdict is advice, not a decision.

### Honesty rules
- Open every source you cite. If it can't be opened, it's `UNVERIFIED`.
- Label mocked parts as mocked in the demo.
- Never show targets as results.

---

## Limits
- A full trial uses about **15 subagent calls**; quick mode about 9. Use `--quick` when time or usage is short.
- Research steps need web search and fetch access. Without them, Hack Kit marks claims `UNVERIFIED`.
- The PDF step needs Python 3, plus Chrome/Chromium, Playwright or pandoc with a PDF engine. Otherwise, open `FINAL.html` and use Print → Save as PDF.
- The claude.ai version simulates the jury in one chat, so it's less independent.

---

## Repo layout
```
hack-kit/
├── .claude-plugin/     plugin.json + marketplace.json
├── commands/           one file per /hack: command
├── agents/             hack-juror, hack-prosecutor, hack-defender
├── skills/
│   ├── hack-kit/       shared rules (SKILL.md)
│   └── hack-court/     trial protocol (SKILL.md) + jurors.json
├── templates/          state, brief, scoring, POV, evidence, gap table, core, plan, verdict, deck outline
├── scripts/compile.py  builds FINAL.md / FINAL.html / FINAL.pdf
├── prompts/            copy-ready prompts for teammates
├── claude-ai/          one-chat skill + one-paste prompt
└── examples/           OPD Saathi sample
```

## Credits
The trial format was inspired by court-style review skills, such as [alexyc9381/court-skill](https://github.com/alexyc9381/court-skill) (MIT), and adapted to judge problems and solutions instead of business viability. The phase structure was inspired by spec-driven workflows like GSD.

## License
MIT
