---
description: "Show where the team is: phase table, CORE version, latest decision, open assumptions, tasks, time to freezes, conflicts and the next command. With --merge: merge teammates' pending sections"
argument-hint: "[--merge]"
---

# /hack:status — Where are we?

Arguments: $ARGUMENTS

Read `.hackathon/STATE.md` and `ASSUMPTIONS.md`, and list the files in `.hackathon/`. If nothing is there, say: "No hackathon set up here. Run `/hack:start`."

If `STATE.md` has no `Schema version` line, upgrade it first (section 2 of the `hack-kit` skill) and say so in one line.

Show the following in under 18 lines:

```
Event    <name> · <track> · <length> · <mode> · captain <name>
Problem  <chosen statement>
Idea     <chosen idea> · CORE v<n> · 🔒 locked <time> | ✏️ not locked
Motto    <motto>

✅ start  ✅ decode  ✅ pick  ✅ users  ⏳ ideate  ⬜ validate  ⬜ compete
⬜ stress ⬜ improve ⬜ lock  ⬜ plan   ⬜ verify  ⬜ pitch     ⬜ ship

Decision   <latest trial>: <PASS/REVISE/FAIL/INCONCLUSIVE> · NG <x> · G <y> · IE <z> · lowest rating: <item> <n>/10
Assumptions <open> open · <validated> validated · <rejected> rejected · ⚠ <n> "collapses" still open
Evidence   [V] <n> · [T] <n> · [AI] <n> · [?] <n>
Time       idea freeze in <h:mm> · code freeze in <h:mm> · submission in <h:mm>
Risks      <unapplied fixes> · <missing files> · <conflicts>

Next → /hack:<command> — <why, in one line>
```

- If `PLAN.md` has a task table, add a line: `Tasks  <done>/<total> done · blocked: <ids> · critical path: <on track / late>`.

Work out the times from the current time. Mark any overdue freeze **OVERDUE**.
- Show skipped phases as ⏭ with their reason.
- **Conflicts:** flag `## Pending from <name>` sections in ASSUMPTIONS.md that haven't been merged, and files changed by more than one person since the last STATE update (if git is available).
- If time is short (by the time guard in the skill), suggest the quick version of the next command.
- If Python is available, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lint_project.py" .hackathon` and add its warnings (broken tables, untested "collapses" assumptions, unlabelled numbers) to **Risks**.

---

## `/hack:status --merge` (captain only)
1. `git pull` if this is a git repo.
2. Find every `## Pending from <name> — <time>` section in `.hackathon/*.md`, and every `CONFLICT` block.
3. For each pending row:
   - if it's new, append it to the main table;
   - if it duplicates an existing row, drop it and keep the better-labelled evidence;
   - if it changes a row differently from the main table, keep both, mark them `CONFLICT`, and ask the captain (AskUserQuestion) which to keep.
4. Remove the merged pending sections. Never delete a row nobody chose to drop.
5. Log in STATE.md: "merged <n> rows from <names>; <k> conflicts resolved", and update "Last updated".
6. Remind the captain to commit and push.
