> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:help — How to use Hack Kit

Show this, then add one line with the next command based on `.hackathon/STATE.md` if the file exists:

```
HACK KIT  ·  Think deeper. Challenge harder. Build smarter.

 FIRST HACKATHON?  Starter path, 5 commands:
   /hack:start → /hack:pick → /hack:ideate → /hack:plan → /hack:pitch
   (decode, users, compete, validate, stress and lock are folded in;
    /hack:ship for the PDF is optional)

 FULL PATH (14 phases)

 FIND IT             SHAPE IT              BUILD & SELL IT
 1 /hack:start       4 /hack:users         11 /hack:plan
 2 /hack:decode      5 /hack:ideate  💡    12 /hack:verify  ⚖️
 3 /hack:pick  ⚖️     6 /hack:validate      13 /hack:pitch
                     7 /hack:compete       14 /hack:ship  → FINAL.pdf
                     8 /hack:stress
                     9 /hack:improve ↺
                    10 /hack:lock  🔒

 ANYTIME   /hack:assumptions · /hack:court <thing> ⚖️ · /hack:status · /hack:help · /hack:retro
 FLAGS     --quick   faster: 7 jurors, fewer ideas, 1 improve round
           /hack:verify --demo   Demo Day Court on what you built
           /hack:pitch --drill   simulated judges, hard-question practice
           /hack:status --merge  captain merges teammates' pending work
           /hack:status --path full|starter  switch path, nothing is lost
 PROFILE   /hack:start sets event type, length, team experience, focus and
           path; every command reads it from STATE.md

 💡 = explore different solution directions     ↺ = improve loop after any trial
 ⚖️ = Hack Court: PASS · REVISE · FAIL · INCONCLUSIVE
 🔒 = protects problem, user, journey and motto; details can still improve
 Labels: [V] verified · [T] team-provided · [AI] AI inference · [?] unknown
```

If STATE.md says the path is **starter**, show this quick start:
1. Before the statements are out: `/hack:start` (pick the starter path).
2. When they're out: `/hack:pick`. It decodes the statements, then picks the problem with one quick trial.
3. `/hack:ideate`: who the users are, 3 directions, who already does it, then the team picks.
4. `/hack:plan`: the riskiest assumptions, a quick stress check, lock the idea, then the build plan.
5. Build, then `/hack:pitch` (and `/hack:pitch --drill` to practise). `/hack:ship` makes the PDF.

Otherwise, show the full quick start:
1. Before the statements are out: run `/hack:start` and fill in the brief.
2. When they're out: `/hack:decode` → `/hack:pick` (choose the problem).
3. `/hack:users` → `/hack:ideate` (choose the idea).
4. Split the team: one person on `/hack:validate`, one on `/hack:compete`, one testing the riskiest assumption with real people.
5. `/hack:stress` → `/hack:improve` → `/hack:lock`, at about 1.5 h for a 24 h event.
6. `/hack:plan` → `/hack:verify` → build → `/hack:verify --demo` → `/hack:pitch` → `/hack:pitch --drill` → `/hack:ship`.
7. Post-hackathon: `/hack:retro` (extract lessons, analyze execution vs goals, and set top 3 improvements).
