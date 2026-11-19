> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:lock — Freeze the core

> **Phase 10 of 14** · Reads: `USERS.md`, `IDEAS.md`, `EVIDENCE.md`, `COMPETE.md`, `IMPROVE.md`, `ASSUMPTIONS.md`, `CORE.md` · Writes: `CORE.md` (locked) · Next: `/hack:plan`

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md` and the files above.


Profile settings used: `explain_steps` (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
One clear idea the whole team can repeat word for word. From here on, the team builds instead of rethinking.

**What lock means:** the **problem, the main user, the core journey and the motto** are protected. Solution details (a screen, a channel, a fallback) can still improve through `/hack:improve`, as long as every change is logged and nothing drifts.

## Steps

### 1. Complete CORE.md
Fill every section of `templates/core.md`, keeping the current version number:

1. Name and motto
2. Positioning line
3. The problem in 2 lines, with the strongest `[V]` or `[T]` fact
4. Persona story, before vs after
5. End-to-end journey: for each step, who acts, the channel, what the system does and what the human decides
6. Who does what, and what each role never has to do
7. 4–6 USPs, each tied to a user pain and to what's better than existing options (not to a technology)
8. AI vs rules vs humans: safety-critical steps use rules plus a human, never AI alone
9. Inclusion of the least-digital user
10. Fit with existing systems (L0–L3)
11. Privacy basics
12. Out of scope
13. Open assumptions (from ASSUMPTIONS.md, with their status)

### 2. Checks before locking
- **Mistakes check:** go through the "Mistakes to block" table in the skill. Fix anything that fails, or flag it.
- **Assumption check:** if any "collapses" assumption is still open, warn: "You're locking on an untested belief: <assumption>." Suggest the experiment card from `/hack:validate`, or lock anyway with the risk logged.
- **History check:** make sure IDEAS.md records the rejected ideas, and IMPROVE.md the rejected changes.

### 3. Confirm
Show a 10-line summary, then ask (AskUserQuestion):
- **Lock it**
- **Change something first**
- **Run a quick trial first** (`/hack:court --quick`)

### 4. Freeze
Once the team confirms:
- Put `> LOCKED: <date time, time zone> · Version v<n>` at the top of CORE.md.
- In STATE.md: tick "lock", fill the **Locked** section (problem, main user, core journey, motto), set "Core locked at", and log it.

## Starter path, when plan is skipped (ideathons)
On an ideathon's starter path there's no `/hack:plan`, so the short validate and stress steps happen here, **before step 1**:
1. List the top 3 assumptions in `ASSUMPTIONS.md` with a kill test each, and one 30-minute experiment card for the top "collapses" one.
2. Role-play the least-digital user, the front-line worker and the sceptic in 2 lines each; write their doubts to `STRESS.md` under `## Short version (starter path)`.
Then lock as normal.

## Output
- `.hackathon/CORE.md`, complete and marked LOCKED. The previous draft goes to `history/` only if its content changed.
- In STATE.md: the Locked section, "Core locked at", phase 10 ticked, and the decision logged.

## After lock
If any later command or teammate proposes a change to the problem, the main user, the core journey or the motto, warn: **"This drifts from the locked core. Captain's OK needed."** Other improvements go through `/hack:improve`.

## Finish
Give the motto, the journey in 5 steps, and any open "collapses" assumptions.
**Next → `/hack:plan`** (or **`/hack:pitch`** if the profile skips plan).
