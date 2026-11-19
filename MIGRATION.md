# Migrating to Hack Kit 1.0

> Summary: update the plugin. Existing `.hackathon/` projects keep working and upgrade themselves on the next command. Nothing is deleted.

## 1. Update the plugin

In Claude Code:
```
/plugin marketplace update hack-kit
/plugin install hack@hack-kit
```
Restart Claude Code if the new commands (`/hack:ideate`, `/hack:improve`, `/hack:assumptions`) don't show up.

**Claude app users:** download the new `hack-kit-skill.zip` from the website or `docs/downloads/`, remove the old Hack Kit skill under **Settings → Capabilities → Skills**, and upload the new one.

## 2. What happens to an existing project

The next `/hack:start` or `/hack:status` (or any command) notices that `STATE.md` has no `Schema version` line and upgrades it:

1. The old file is copied to `.hackathon/history/STATE-v1.md`.
2. The missing schema 2 sections are added: last updated, event length, phase table, decisions log columns, locked items, pending items, CORE version. Every existing value and log entry is kept.
3. If you have `PICK-VERDICT.md` (from 0.1) and no `PICK.md`, it's copied to `PICK.md`.
4. A new `ASSUMPTIONS.md` is created and seeded from `USERS.md`, `STRESS.md` and `CORE.md`.
5. The upgrade is logged in the decisions log.

## 3. Phase numbers changed

| 0.x | 1.0 |
|---|---|
| 1 start · 2 decode · 3 pick · 4 users | same |
| — | **5 ideate** (new) |
| 5 validate · 6 compete · 7 stress | 6 validate · 7 compete · 8 stress |
| — | **9 improve** (new) |
| 8 lock · 9 plan · 10 verify · 11 pitch · 12 ship | 10 lock · 11 plan · 12 verify · 13 pitch · 14 ship |
| — | **assumptions** (anytime, new) |

**Mid-event?** You don't have to go back.
- If you've already locked, run `/hack:assumptions` once to see what's untested, and use `/hack:improve` after your next trial.
- If you haven't locked yet and have time, run `/hack:ideate` before `/hack:stress`. It takes about 15 minutes (5 in quick mode).

## 4. Trial results look different

Old verdicts said GUILTY or NOT GUILTY with a count. New verdicts add a third juror vote (INSUFFICIENT EVIDENCE) and a decision: **PASS / REVISE / FAIL / INCONCLUSIVE**. Old trial folders in `court/` are left as they are.

## 5. Evidence labels

Old files used `UNVERIFIED`. New files use `[V]`, `[T]`, `[AI]` and `[?]`. Old files don't need changing: when a command reads them, it treats `UNVERIFIED` as `[?]`, and sourced numbers as `[V]` only after it reopens the source.
