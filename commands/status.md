---
description: "Show where the team is: phase checklist, what's locked, latest verdict, time to freezes, open risks, next command"
argument-hint: ""
---

# /hack:status — Where are we?

Arguments: $ARGUMENTS

Read `.hackathon/STATE.md` and list the files in `.hackathon/`. If nothing is there, say: "No hackathon set up here. Run `/hack:start`."

Show the following in under 15 lines:

```
Event   <name> · <track> · <mode> · captain <name>
Pick    <chosen statement>
Motto   <motto>
Core    🔒 locked <time>  |  ✏️ not locked

✅ start  ✅ decode  ✅ pick  ⏳ users  ⬜ validate  ⬜ compete
⬜ stress ⬜ lock    ⬜ plan  ⬜ verify ⬜ pitch     ⬜ ship

Verdict  <x>/12 · lowest rating: <item> <n>/10
Time     idea freeze in <h:mm> · code freeze in <h:mm> · submission in <h:mm>
Risks    <n> UNVERIFIED claims · <n> fixes not applied · missing: <files>

Next → /hack:<command> — <why, in one line>
```

Work out the times by comparing against the current time. If a freeze is overdue, put **OVERDUE** next to it.
