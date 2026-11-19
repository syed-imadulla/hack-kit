<div align="center">

# 🏁 Hack Kit

### Think deeper. Challenge harder. Build smarter.

A Claude Code plugin that takes your hackathon team from *"here are the problem statements"* to a tested idea, an MVP plan, a pitch and one final PDF.

[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-D97757)](https://docs.claude.com/en/docs/claude-code/plugins)
[![Version](https://img.shields.io/badge/version-1.3.0-blue)](CHANGELOG.md)
[![Checks](https://github.com/syed-imadulla/hack-kit/actions/workflows/check.yml/badge.svg)](https://github.com/syed-imadulla/hack-kit/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

### 🌐 [See it in action →](https://syed-imadulla.github.io/hack-kit/)

</div>

---

## Why

Most teams lose in the first two hours: they pick the problem that sounds cool, build the first idea everyone else builds, and treat guesses as facts. Hack Kit turns those hours into a guided process. Each `/hack:` command asks the few questions that matter, saves the answers in `.hackathon/`, and tells you what to run next. Along the way it puts your idea **on trial** in front of AI jurors, so you find the weak spots before the judges do.

> ⚖️ It judges whether the problem is real and whether your solution solves it for real users. Never business viability.

## Install

Inside Claude Code:

```bash
/plugin marketplace add syed-imadulla/hack-kit
/plugin install hack@hack-kit
/hack:help
```

Updating? `/plugin marketplace update hack-kit`. Old projects upgrade automatically ([MIGRATION.md](MIGRATION.md)).

## 🌱 First hackathon? Five commands

```
/hack:start → /hack:pick → /hack:ideate → /hack:plan → /hack:pitch     (then /hack:ship for the PDF)
```

| Command | Does |
|---|---|
| `/hack:start` | Reads the brief like a judge and sets your event profile |
| `/hack:pick` | Decodes every statement, then picks the problem with one quick trial |
| `/hack:ideate` | Who the users are, 3 directions, who already does it; the team picks |
| `/hack:plan` | Riskiest assumptions, a quick stress check, **locks the idea**, then the build plan |
| `/hack:pitch` | Deck outline and judge Q&A; practise with `--drill` |

This starter path is the default for first-time teams. Nothing is dropped: the other phases run as short versions inside these commands, and `/hack:status --path full` opens all 14 phases anytime.

## All commands (full path)

| | Command | Does |
|---|---|---|
| **Find** | `/hack:start` · `/hack:decode` · `/hack:pick` ⚖️ | Brief and profile · decode statements · choose the problem |
| **Shape** | `/hack:users` · `/hack:ideate` · `/hack:validate` · `/hack:compete` | Real users · 6 solution directions · evidence and experiments · what exists |
| | `/hack:stress` · `/hack:improve` · `/hack:lock` 🔒 | Attack the idea · make it better · freeze the core |
| **Build** | `/hack:plan` · `/hack:verify` ⚖️ · `/hack:pitch` · `/hack:ship` | Team-aware MVP plan · trial · pitch · one PDF |
| **Anytime** | `/hack:assumptions` · `/hack:court` ⚖️ · `/hack:status` · `/hack:help` · `/hack:retro` | Assumptions · try anything · where are we · help · lessons after the event |

Useful flags: `--quick` (faster, 7 jurors) · `/hack:verify --demo` (judge what you actually built) · `/hack:pitch --drill` (practise with simulated judges) · `/hack:status --merge` (combine teammates' work).

## How Hack Court works

A prosecution and a defense argue from a labelled evidence pack. Then 12 jurors (7 in quick mode), each a **separate** AI run, vote GUILTY, NOT GUILTY or INSUFFICIENT EVIDENCE. `scripts/tally.py` counts the votes:

| Decision | When |
|---|---|
| **PASS** | NOT GUILTY ≥ 75%, with solid evidence and no untested "collapses" assumption |
| **REVISE** | Anything in between |
| **FAIL** | GUILTY outnumbers NOT GUILTY |
| **INCONCLUSIVE** | Too few valid votes, or too many say "insufficient evidence" |

Every claim is labelled `[V]` verified · `[T]` from the team · `[AI]` inference · `[?]` unknown. Only `[V]` and `[T]` count as proof. The verdict is advice; **the captain decides.**

## Tested, honestly

Each release was run end to end with real juror runs, and every run found problems that were then fixed. One real Demo Day Court failed a prototype 0–7 and caught two bugs a made-up jury had missed. See the [test report](docs/TEST-RUN.md) and [examples](examples/).

## No Claude Code?

- **Claude app:** upload [`hack-kit-skill.zip`](docs/downloads/hack-kit-skill.zip) under Settings → Capabilities → Skills, then type `hack start`.
- **Any chat AI:** paste [`claude-ai/PROMPT.md`](claude-ai/PROMPT.md) as your first message.

## Learn more

- [Guide](docs/GUIDE.md): timeline, team tips, the 17 rules, the jurors, saved files and FAQ
- [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Examples](examples/)

---

Built by **[Syed Imadulla](https://github.com/syed-imadulla)**. Trial format inspired by [alexyc9381/court-skill](https://github.com/alexyc9381/court-skill) (MIT); phase flow inspired by GSD. Open source under the **[MIT License](LICENSE)**.

<sub>© 2026 Syed Imadulla · Made for hackers who want to solve real problems.</sub>
