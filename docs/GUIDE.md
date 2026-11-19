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

---

# Reference

## The 17 rules every command follows
1. Read the brief like a judge, because rubric weights decide everything.
2. Pick a problem, not a technology.
3. Think as every real user, especially the least-digital one.
4. Prove it's real with sources, real complaints and venue chats.
5. Check what already exists. "No competitors" is never true.
6. Stress-test in place of a domain expert, then confirm with real people.
7. Lock the core (problem, user, journey, motto). Details can still improve.
8. Fit with existing systems. No new hardware.
9. No app, no typing, the simplest device.
10. AI suggests, humans decide. Safety checks use fixed rules.
11. One complete journey for the MVP. Every feature needs a reason.
12. No unlabelled numbers. Targets are labelled as targets.
13. Simple, everyday English.
14. **Evidence before confidence.** A confident AI answer is still `[AI]`.
15. **Test the riskiest assumption first.**
16. **Different technology isn't innovation.** Differentiate by user value.
17. **Keep the decision history.** Record what was rejected, and why.

## The 12 jurors
★ = sits on the quick jury of 7.

| # | Juror | Asks |
|---|---|---|
| 1 ★ | Actual end user | Would I use this on a busy day? |
| 2 ★ | Least-digital user | Can I use it without an app, typing or English? |
| 3 ★ | Front-line worker | Does this add work for me or remove it? |
| 4 ★ | Domain professional | Does it respect how the work really happens? |
| 5 | Today's-workaround user | Why switch from WhatsApp or paper? |
| 6 ★ | Root-cause analyst | Does it fix the cause or only a symptom? |
| 7 | "Already exists" researcher | What's honestly different? |
| 8 | Safety & ethics reviewer | What's the worst that can go wrong? |
| 9 | Systems person | Does it fit what we already run? |
| 10 ★ | Engineer | Can it be built and demoed in time? |
| 11 | Statement-owner judge | Does it answer what was asked? |
| 12 ★ | Sceptic | Does this really matter, and to how many people? |

**Domain seats:** for healthcare, agriculture, education, finance, civic and climate problems, seats 4, 5 and 9 become three domain jurors. For healthcare, that's a senior doctor, a hospital administrator and a patient privacy officer. The jury stays at 12, so the cost doesn't change.

No investors and no accountants, on purpose. Simulated jurors are perspectives, not real experts, and confidence isn't a probability of success.

## What gets saved
Everything is saved in `.hackathon/` in your project. Commit it so the whole team works from the same state. The starter path writes fewer files; short versions go under `## Short version (starter path)`.

```
.hackathon/
├── STATE.md        schema v2: phases, decisions (incl. rejected), locked items
├── BRIEF.md        rubric, limits, team, time
├── STATEMENTS.md   every statement decoded
├── PICK.md         chosen problem + trial
├── USERS.md        stakeholder views, persona, motto
├── IDEAS.md        💡 directions explored, scores, rejected ideas
├── ASSUMPTIONS.md  what you're assuming, kill test, status
├── EVIDENCE.md     labelled evidence, experiment cards
├── COMPETE.md      what exists + differentiation
├── STRESS.md       doubts + failure scenarios
├── IMPROVE.md      ↺ improvement rounds, v1 → v2
├── CORE.md         🔒 the locked idea (versioned)
├── PLAN.md         MVP, demo script, fallbacks
├── VERDICT.md      solution trial + rubric estimate
├── DEMO.md         Demo Day check: planned → built → tested → shown
├── RETRO.md        after the event
├── PITCH.md        deck + Q&A
├── SUMMARY.md      one page
├── FINAL.pdf       📄 everything
├── history/        earlier versions, never deleted
└── court/          full trial records + raw votes
```

## FAQ
<details>
<summary><b>How long does it take?</b></summary>

About 80–100 minutes to a locked idea for a 24-hour event, and about 45 minutes in quick mode for a 12-hour one. The time guard shrinks the new thinking steps when time is short.
</details>

<details>
<summary><b>How much usage does a trial cost?</b></summary>

A full trial uses about 15 subagent calls (2 lawyers + 12 jurors + retries). Quick mode uses about 10. `/hack:improve` runs one quick re-trial per round.
</details>

<details>
<summary><b>Will it pick the idea for us?</b></summary>

No. `/hack:ideate` shows the trade-offs and the captain decides. The AI never picks the most impressive-sounding idea for you.
</details>

<details>
<summary><b>Can we trust the verdict?</b></summary>

Use it to decide what to test and fix, not as proof. Jurors are simulated perspectives, confidence isn't a probability, and only `[V]` and `[T]` evidence counts as real. Real validation comes from the experiments you run.
</details>

<details>
<summary><b>Does it need web access?</b></summary>

The research steps work best with web search. Without it, Hack Kit still runs, but labels claims `[?]` or `[AI]` and tells you what to look up.
</details>

<details>
<summary><b>What do I need for the PDF?</b></summary>

Python 3, plus Chrome/Chromium, Playwright or pandoc. Otherwise, open `FINAL.html` and use **Print → Save as PDF**.
</details>

<details>
<summary><b>Why no business or market judging?</b></summary>

At the idea stage, judges reward a real problem that's clearly solved. If your rubric asks for business points, `/hack:pitch` covers them.
</details>

## Repo layout
```
hack-kit/
├── .claude-plugin/     plugin.json · marketplace.json
├── .github/workflows/  checks on every push
├── commands/           19 /hack: commands
├── agents/             hack-juror · hack-prosecutor · hack-defender
├── skills/
│   ├── hack-kit/       shared rules (the source of truth)
│   └── hack-court/     trial protocol + jurors.json (with domain seats)
├── templates/          one template per output file
├── scripts/            tally · profile · plan_check · merge · retro · compile · lint_project · check · build_claude_ai
├── tests/              unit tests and vote fixtures
├── claude-ai/          generated Claude app skill + one-paste prompt
├── prompts/            copy-ready prompts
├── docs/               website · GUIDE.md · TEST-RUN.md · skill zip · internal/
└── examples/           test run (complete) · PDS Anna-Mitra · OPD Saathi sample
```

