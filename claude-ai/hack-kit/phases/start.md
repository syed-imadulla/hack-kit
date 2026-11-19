> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:start — Read the brief like a judge

> **Phase 1 of 14** · Reads: — · Writes: `BRIEF.md`, `STATE.md` · Next: `/hack:decode`

## Before you start
Load the shared rules from the `hack-kit` skill (`SKILL.md`).

If `.hackathon/STATE.md` already exists:
- If it has no `Schema version` line, it's an older project. Upgrade it as described in section 2 of the skill, tell the user in one line, then suggest `/hack:status`.
- Otherwise, show the current phase and ask:
  - **Continue this event** → stop here and suggest `/hack:status`.
  - **Start a new event** → rename the old folder to `.hackathon-old-<YYYYMMDD-HHMM>/`, then continue.

## Goal
Capture everything about the event that decides what wins, before anyone falls in love with an idea.

## Steps

### 1. Collect the brief
If the arguments contain a link, fetch it with WebFetch. If the user attached or pasted the brief, read that. Pull out the rubric, rules and deliverables, show what you found, and ask the user to confirm it.

### 2. Ask what's missing
Use AskUserQuestion (at most 4 per round), prefilled wherever possible. Don't ask what the brief already answers.

| Topic | What to capture |
|---|---|
| Event type | college · SIH / government statements · AI/ML · startup ideathon (no build) · hardware · corporate |
| Event length | 12 h · 24 h · 36 h · 48 h+ (and online, offline or hybrid) |
| Team | size, and experience: mostly first-timers · mixed · experienced |
| Judging focus | balanced · technical feasibility · innovation and impact · business (pitch only) |
| Path | **starter** (5 commands, recommended for a first hackathon) · **full** (all 14 phases). Default: starter for mostly first-timers, full otherwise |
| Event | name, organiser, track or theme, **domain** (healthcare, agriculture, education, finance, civic, climate, other) |
| Rubric | criteria and weights. If unknown, use the event type's default rubric from the profile and mark it `ASSUMED` |
| Deliverables | slide limit, video, repo, form questions with word limits, demo length |
| Time | now, submission deadline, judging time (with time zone) |
| Team members | names, roles, skills (frontend, backend, AI, design, pitch, domain), hours each can work |
| Resources | sponsor tech or required APIs, hardware, datasets, cloud credits |
| Rules | pre-built code allowed, data, team size |

### 3. Write down what judges will reward
Translate the top 3 rubric items into plain words and say what each means for choosing an idea. For example: "Feasibility 25% → pick something one journey can prove in 24 h."

### 4. Set the profile
Ask the first four rows of the table first (type, length, team, focus): one AskUserQuestion round, prefilled from the brief. Then ask the path in one question:
- **Starter path (Recommended for first-timers):** 5 commands: start → pick → ideate → plan → pitch. The other phases are folded in as short versions. One trial, about 9 agent runs.
- **Full path:** all 14 phases, more trials, deeper checks.

Put the recommended option first: starter if the team is mostly first-timers, full otherwise. Then run:
```bash
python3 "<plugin>/scripts/profile.py" --type <t> --length <l> --experience <e> --focus <f> --team <n> --path <starter|full>
```
Show the table in one screen and ask: **"Use this plan?"** (Yes · Change something). If Python isn't available, build the same table by hand from `profiles.json` (length first, then event type, experience and focus).

### 5. Set the plan
- **Mode and depth:** from the profile (`--quick` forces quick).
- **Time guard:** idea locked within the profile's target; code freeze 3–4 h before judging (not used for ideathons).
- **Captain:** the final decider. Ask if it isn't clear.

## Output
- `.hackathon/BRIEF.md` from `templates/brief.md`.
- `.hackathon/STATE.md` from `templates/state.md` (schema version 2): fill in the event table, paste the profile under `## Profile`, mark the profile's skipped phases as `skipped (profile)` and, on the starter path, each folded phase as `folded → /hack:<command>`, set phase 1 to done, and set "Last updated".
- `.hackathon/ASSUMPTIONS.md` from `templates/assumptions.md` (empty for now).
- The folders `.hackathon/court/` and `.hackathon/history/`.

## Finish
Give a 5-line summary: event and profile, top 3 rubric items, deliverables, time left, target time to lock the idea.
On the starter path, add one line: "Your 5 commands: start ✓ → pick → ideate → plan → pitch."
**Next → `/hack:decode`** (full path) or **`/hack:pick`** (starter path: it decodes the statements first). Paste the problem statements when they're out.
