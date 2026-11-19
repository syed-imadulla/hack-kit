# The Hack Kit hackathon guide

This is the playbook behind the commands. Read it once before your first event.

---

## Before the event (1 evening)

| Do | Why |
|---|---|
| Fix the roles: **captain** (final decider), builder(s), researcher, pitcher | No debates about who decides |
| Freeze your default stack | No stack fights on the day |
| Each person lists 10 real frustrations they've seen | Real problems beat invented ones |
| Line up 2–3 people you can call (a doctor, farmer, teacher, shopkeeper…) | Your stand-in domain experts |
| Install Hack Kit and do a 15-minute dry run on an old statement | Learn the flow before it counts |
| Prepare a deck skeleton in your slide tool | Saves an hour at the end |

---

## During the event

### Timeline (24 h event)
| After statements are released | Command | Who |
|---|---|---|
| 0:00 | `/hack:start` (or before statements) | Captain |
| 0:05 | `/hack:decode` | Captain |
| 0:20 | `/hack:pick` → captain decides | Everyone |
| 0:35 | `/hack:users` | Captain + pitcher |
| 0:45 | `/hack:validate` ‖ `/hack:compete` ‖ venue chats | Split the team |
| 1:10 | `/hack:stress` | Everyone |
| ~1:30 | `/hack:lock` → **idea freeze** 🔒 | Captain |
| 1:40 | `/hack:plan` | Builders |
| 2:00 | `/hack:verify` | Captain |
| 2:15 → code freeze | Build the one journey | Builders |
| Code freeze (3–4 h before judging) | Record the backup demo | Builder |
| Before judging | `/hack:pitch` → `/hack:ship` | Pitcher |

For a 36 h event, double the time for phases 1–8 and spend it on real conversations.

### Working as a team
- Put `.hackathon/` in your shared git repo. It's the single source of truth.
- One person runs the main commands. Others run `/hack:validate` and `/hack:compete` on their own machines and push the files.
- Run `/hack:status` whenever someone asks "where are we?"
- The verdict is advice. **The captain decides.**

### Talking to people at the venue
Mentors, volunteers, other attendees and staff can all be users. Ask about their past, not their opinion of your idea:
- "Tell me about the last time you…"
- "What did you do? How long did it take?"
- "What have you tried? Why didn't it work?"

Write it down in `/hack:validate`. Three real conversations beat thirty AI guesses.

---

## The trial, explained

| Part | Who | What |
|---|---|---|
| Case file | Clerk (main Claude) | ~120 words: problem, users, solution, constraints |
| Prosecution | Subagent | Strongest case that it does **not** solve a real problem |
| Defense | Subagent | Strongest case that it **does** |
| Jury | 12 separate subagents | GUILTY / NOT GUILTY, confidence, reason, fix |
| Judge | Main Claude | Counts only real votes, then gives ratings, fixes and a venue check |

**GUILTY** means "it does not solve a real problem for its real users as described". Business viability is **never** judged.

### Reading a verdict
| Result | What to do |
|---|---|
| NOT GUILTY with 9 or more votes | Go. Apply the top fix. |
| NOT GUILTY with 7–8 votes | Go, but fix the lowest rating first. |
| HUNG JURY (6–6) | Run the 30-minute venue check, then decide. |
| GUILTY | Read the top 3 reasons. Fix inside the core, or choose the next candidate. |

---

## After lock: staying on track
- Every new idea goes on a "later" list unless the captain approves it.
- Before adding a feature, ask: "Does the demo journey need this?"
- When a reviewer or mentor raises a doubt, fix it **inside** the core instead of switching ideas.

---

## Pitch rules that win
- Open with the problem and one sourced number, not your team intro.
- Show the persona's journey live. Keep the dashboard for the end.
- Say clearly what's mocked. Judges respect honesty and punish surprises.
- Label every impact number as a target until you've measured it.
- Stay within the slide limit.

---

## Mistakes we made (so you don't)
From building OPD Saathi:
1. **Drifting from the core.** Fixing feedback by adding new ideas instead of improving the original.
2. **Adding hardware** (a kiosk) that most real sites don't have.
3. **Unrealistic approvals** that ignored how authority really works on the ground.
4. **Overclaiming:** numbers like "saves 133 staff-hours" with no source.
5. **Cost higher than price** in the business slide.
6. **Over the slide limit.**
7. **Diagrams that implied the wrong user** used a screen.

Hack Kit's rules exist because of these.
