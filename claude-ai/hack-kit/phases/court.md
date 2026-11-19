> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:court — Put anything on trial

## Before you start
Load the `hack-court` skill (`court.md`). This command works with or without a `.hackathon/` folder.

## Steps

### 1. What's on trial?
Work it out from the arguments. If there are none, ask (AskUserQuestion):
- **The current idea** (CORE.md)
- **A new feature or fix**
- **The pitch** (PITCH.md)
- **Something else** (type it)

### 2. Evidence pack
Build it from the relevant `.hackathon/` files plus anything the user said, keeping every claim's evidence label. If there's no `.hackathon/` folder, ask for 3–5 lines covering the problem, the users and the solution, and label everything the user says `[T]`.

### 3. The question on trial
| On trial | Question |
|---|---|
| Idea or solution | "Does this solve a real problem for its real users?" |
| Feature or fix | "Does this make the solution better for real users without drifting from the core?" |
| Pitch | "Does this pitch prove the problem is real and the solution solves it, to a judge who has already seen 30 pitches?" |

### 4. Run the trial
Run the full trial, or the quick one if `--quick` was passed. Tell the user the cost first: about 15 subagent calls for a full trial, about 9 for a quick one.

## Output
Save to `.hackathon/court/<slug>/`, or to `./court/<slug>/` if there's no `.hackathon/` folder. Show the decision and suggest the next step: REVISE or FAIL → `/hack:improve`; INCONCLUSIVE → `/hack:assumptions`.
