---
description: Put anything on trial at any time — an idea, a feature, a fix, a pitch — with prosecution, defense, a 12-juror jury and a judge's verdict
argument-hint: "<what to put on trial> [--quick]"
---

# /hack:court

Run the `hack-court` skill (`${CLAUDE_PLUGIN_ROOT}/skills/hack-court/SKILL.md`).

Arguments: $ARGUMENTS

1. Work out what is on trial from the arguments. If empty, ask (AskUserQuestion): "The locked idea (CORE.md)", "A new feature or fix", "The pitch/deck (PITCH.md)", "Something else (type it)".
2. Build the case file from `.hackathon/` files where relevant plus what the user said. If there's no `.hackathon/` folder, ask the user for a 3–5 line description of the problem, users and solution.
3. Adapt the question on trial:
   - Idea/solution: "Does this solve a real problem for its real users?"
   - Feature/fix: "Does this feature make the solution better for real users without drifting from the core?"
   - Pitch: "Does this pitch prove the problem is real and the solution solves it, to a judge who has seen 30 pitches?"
4. Run the full trial (quick if `--quick`). Tell the user the subagent cost before starting.
5. Save to `.hackathon/court/<slug>/` (or `./court/<slug>/` if no `.hackathon/`). Show the verdict.
