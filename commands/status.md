---
description: Show the current phase, what's locked, time left, open risks and the next command
argument-hint: ""
---

# /hack:status

Read `.hackathon/STATE.md` and list the files in `.hackathon/`. If nothing exists, say "No hackathon set up here. Run `/hack:start`."

Show, in under 15 lines:
- Event, track, mode (full/quick), captain.
- Phase checklist (✅ done / ⏳ next / ⬜ not started) for: start, decode, pick, users, validate, compete, stress, lock, plan, verify, pitch, ship.
- Chosen statement and motto (if any).
- Locked? (timestamp)
- Latest verdict (x/12) and lowest rating.
- Time left to idea freeze / code freeze / submission (compare with the current time; say if a freeze is overdue).
- Open risks: UNVERIFIED claims count, unapplied fixes, missing files.
- **Next command** with one line on why.
