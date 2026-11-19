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

## First hackathon? Take the starter path

If most of your team is new, choose the **starter path** in `/hack:start` (it's the default for first-timers):

| # | Command | What happens |
|---|---|---|
| 1 | `/hack:start` | Event profile, rubric, deadlines |
| 2 | `/hack:pick` | A short decode of every statement, then one quick trial to choose the problem |
| 3 | `/hack:ideate` | Users in 5 lines, 3 directions, who already does it, then the team picks |
| 4 | `/hack:plan` | Top 3 assumptions with one experiment, a 3-person stress check, **lock the idea**, then tasks and the demo script |
| 5 | `/hack:pitch` | Deck, judge Q&A, then `--drill` to practise |

For a 24 h event, aim to finish `/hack:plan` within about an hour of the statements coming out, then build. If you have time later, `/hack:verify --demo` checks what you built, and `/hack:status --path full` opens up the full 14 phases without losing anything.

---

## During the event

### Timeline (24 h event)
| After statements are released | Command | Who |
|---|---|---|
| 0:00 | `/hack:start`: event profile + brief (or before statements) | Captain |
| 0:05 | `/hack:decode` | Captain |
| 0:20 | `/hack:pick` → captain chooses the problem | Everyone |
| 0:35 | `/hack:users` | Captain + pitcher |
| 0:45 | `/hack:ideate` → captain chooses the idea | Everyone |
| 0:55 | `/hack:validate` ‖ `/hack:compete` ‖ test the riskiest assumption with real people | Split the team |
| 1:15 | `/hack:stress` → `/hack:improve` | Everyone |
| ~1:40 | `/hack:lock` → **idea freeze** 🔒 | Captain |
| 1:50 | `/hack:plan`: team table, tasks, plan check | Builders |
| 2:10 | `/hack:verify` (→ `/hack:improve` if REVISE) | Captain |
| 2:30 → code freeze | Build the one journey | Builders |
| 4–6 h before code freeze | `/hack:verify --demo` → fix what fits | Captain + builders |
| Code freeze (3–4 h before judging) | Record the backup demo | Builder |
| Before judging | `/hack:pitch` → `/hack:pitch --drill` → `/hack:ship` | Pitcher |
| After the event | `/hack:retro`: connect unvalidated assumptions to demo cracks, analyze load, and record top 3 improvements | Team |

Your event profile sets the depth. For a 12 h event, quick mode turns on automatically: fewer ideas, one improve round, and the idea is locked in about 45 minutes. For 36 h+, spend the extra time on real conversations and experiments. Ideathons skip the plan phase and the demo court. Beginner teams get fewer questions and a short "why" for each step.

### Working as a team
- Put `.hackathon/` in your shared git repo. It's the single source of truth.
- One person (the captain) runs the main commands and owns each file. Others run `/hack:validate` and `/hack:compete` on their own machines; their changes go into `## Pending from <name> — <time>` sections, and the captain runs `/hack:status --merge`. Nothing is overwritten; clashes are marked CONFLICT for the captain.
- Run `/hack:status` whenever someone asks "where are we?"
- The verdict is advice. **The captain decides.**

### Demo Day Court and the drill
- **`/hack:verify --demo`** checks the product as it will be shown. A feature counts only if it was run and the result was seen; code existing isn't enough. Every "this is mocked" line must match what exists now. In our test run, 7 of 7 jurors failed a demo whose disclosure said a voice clip was "pre-recorded" before anyone had recorded it.
- **`/hack:pitch --drill`** plays 3 judges from your rubric. Answer out loud in your own words; it scores you and shows a stronger answer built only from your files. It also checks every pitch claim against `DEMO.md`.

### Talking to people at the venue
Mentors, volunteers, other attendees and staff can all be users. Ask about their past, not their opinion of your idea:
- "Tell me about the last time you…"
- "What did you do? How long did it take?"
- "What have you tried? Why didn't it work?"

Write it down in `/hack:validate`. Three real conversations beat thirty AI guesses.

---

## Evidence labels

| Label | Means |
|---|---|
| `[V]` | Verified: a source that was opened and read, or a measured result |
| `[T]` | Team-provided: something you said, or venue notes you typed |
| `[AI]` | AI inference: a reasonable guess, never a fact |
| `[?]` | Unknown |

Only `[V]` and `[T]` can validate an assumption. In your deck, state only `[V]` and `[T]` claims as facts; present the rest as estimates or targets.

---

## Hack Court 2.0, explained

| Part | Who | What |
|---|---|---|
| Evidence pack | Clerk (main Claude) | ~200 words: problem, users, solution, constraints, labelled evidence, top assumptions |
| Prosecution | Subagent | Strongest case that it does **not** solve a real problem |
| Defense | Subagent | Strongest case that it **does** |
| Jury | 12 separate subagents (3 domain seats for known domains; 7 in quick mode, always including the sceptic) | GUILTY / NOT GUILTY / INSUFFICIENT EVIDENCE, with confidence, evidence strength, weakest assumption, missing info and a rated fix |
| Count | `scripts/tally.py` | Checks every reply and re-runs broken ones; counts only valid votes |
| Judge | Main Claude | PASS / REVISE / FAIL / INCONCLUSIVE, contradictions, ratings, ranked improvements, next experiment |

**GUILTY** means "it does not solve a real problem for its real users as described". Business viability is **never** judged.

### Reading a verdict
| Decision | What to do |
|---|---|
| **PASS** | Go. Apply the top P0 improvement if it's cheap. |
| **REVISE** | Run `/hack:improve`: accept the top changes, get CORE v2, re-check. If it says "capped", the votes passed but a killer assumption is untested: run that experiment first. |
| **FAIL** | Run `/hack:improve` once. If it still fails, the captain decides: rethink the idea in `/hack:ideate`, or pick the next problem. |
| **INCONCLUSIVE** | Not enough evidence. Run `/hack:assumptions`, do the next experiment, then trial again. |

Remember: jurors are simulated perspectives, and confidence isn't a probability of success.

---

## The improve loop

`/hack:improve` turns criticism into a better version:
1. It collects the top fixes from the latest verdict (or the stress test).
2. For each change, it shows which weakness it fixes, the new risk it adds, and the evidence still needed.
3. You accept or reject each change. Anything that changes the problem or main user is marked **DRIFT** and needs the captain's OK.
4. The old CORE goes to `history/`, the new version is compared side by side, and a quick trial re-checks it.
5. It stops at PASS, after 2 rounds, or when time runs out.

---

## After lock: staying on track
- Lock protects the problem, the main user, the core journey and the motto. Smaller improvements still go through `/hack:improve`, and get logged.
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
1. **Drifting from the core.** Fixing feedback by adding new ideas instead of improving the original. (`/hack:improve`'s guardrail exists because of this.)
2. **Adding hardware** (a kiosk) that most real sites don't have.
3. **Unrealistic approvals** that ignored how authority really works on the ground.
4. **Overclaiming:** numbers like "saves 133 staff-hours" with no source.
5. **Cost higher than price** in the business slide.
6. **Over the slide limit.**
7. **Diagrams that implied the wrong user** used a screen.

Hack Kit's rules exist because of these.
