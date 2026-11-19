> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:ideate — Think deeper before you commit

> **Phase 5 of 14** · Reads: `BRIEF.md`, `PICK.md`, `USERS.md` · Writes: `IDEAS.md`, `ASSUMPTIONS.md` · Next: `/hack:validate`

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`, `BRIEF.md`, `PICK.md` and `USERS.md`. If `PICK.md` is missing, suggest `/hack:pick` first.


Profile settings used: `ideate_directions`, `ideas_per_direction`, `constraint_removal`, scoring weights (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Most teams build the first idea they think of. This command makes the team look at **genuinely different ways** to solve the same problem for the same user, then choose with the trade-offs in plain view.

**Rules for this command**
- Generate *directions*, not 50 random ideas. Every idea must say which direction it comes from and how it differs.
- The problem and the main user from `PICK.md` and `USERS.md` stay fixed.
- The AI shows the trade-offs, and **the team picks**. Never choose the most impressive-sounding idea on the team's behalf.

## Steps

### 1. Root cause in one screen
- **Five Whys:** from the symptom down to a cause the team could act on.
- **Today's workaround:** what people do now, and why it isn't enough.
- **Where it hurts most:** who suffers most often, and who suffers the worst consequences.

Label each line `[V]`, `[T]`, `[AI]` or `[?]`.

### 2. Explore the 6 directions
For each direction, write **2 ideas** (1 in quick mode), each in 2 lines: what it is, and why it's different.

| Direction | Question |
|---|---|
| **User shift** | What if we solve it for an overlooked user (the least-digital user, the operator, the family member)? |
| **Process shift** | What if we fix one broken step instead of the whole system? |
| **Access shift** | What if we make an existing service reachable (voice, regional language, no app, a normal call)? |
| **Integration shift** | What if we connect systems that already exist instead of building a new one? |
| **Prevention shift** | What if we stop the problem before it happens? |
| **Technology shift** | Where does technology add real value here, not just novelty? |

Quick mode: use only the 3 directions most likely to fit the rubric.

### 3. Constraint removal (skip in quick mode)
Answer each question in one line:
- What does a solution look like with **no AI**? With **no app**? With **no internet**?
- What if we solve only **10% of the problem, exceptionally well**?
- What would **another industry** do? (Airlines for queues, banks for verification, food delivery for tracking.)
- **Reverse brainstorm:** how would we make this problem *worse*? Then flip each answer.

Turn the best 1–2 answers into ideas, tagged "constraint removal".

### 4. Combine
Suggest up to 2 combinations that are stronger together, such as an access shift plus a process shift. Skip in quick mode.

### 5. Score the trade-offs
Score each idea 1–5. Weight the scores by the rubric in BRIEF.md and show the weights you used.

| # | Idea | Direction | User value | Originality | Rubric fit | Buildable in time | Evidence available | Biggest risk | Total |

- **Different technology isn't innovation.** An idea that only swaps in a newer model scores low on originality.
- Mark the obvious idea (the one most teams will build) with "(obvious)". It's allowed, but the team should see the alternatives next to it.

### 6. The team picks
Show the top 3 with a 2-line case for each, then ask (AskUserQuestion):
- **Pick one** (the options are the top 3).
- **Combine two.**
- **Let me type my own.**

Then ask for the captain's confirmation.

### 7. Record
- In `IDEAS.md` (from `templates/ideas.md`), record **every idea, the scores, the choice, and why each other idea was rejected**.
- For the chosen idea, list its **key assumptions** (what must be true for it to work). Add them to `ASSUMPTIONS.md`, labelled `[AI]` or `[T]`, with the source "ideate".

## Output
- `.hackathon/IDEAS.md`.
- Updated `.hackathon/ASSUMPTIONS.md`.
- In STATE.md: set "Chosen idea", tick "ideate", and log the decision with the rejected ideas.

## Finish
Give 3 lines: the chosen idea, the direction it came from, and its riskiest assumption.
**Next → `/hack:validate`** (test the riskiest assumption). It can run in parallel with `/hack:compete`.
