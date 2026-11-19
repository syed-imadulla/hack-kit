> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:retro — Learn from this hackathon

> **Post-event / Anytime** · Reads: `BRIEF.md`, `STATE.md`, `ASSUMPTIONS.md`, `EVIDENCE.md`, `PLAN.md`, `DEMO.md`, `PITCH.md`, `court/` · Writes: `RETRO.md` · Next: Apply lessons to next hackathon

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md` and check which project files exist. If no `.hackathon/` directory exists, tell the user to run `/hack:start` or point to a valid hackathon project.

Profile settings used: `event_type`, `length`, `experience`, `focus` (from STATE.md → Profile).

## Goal
Extract honest, measurable engineering and design lessons from the hackathon. Don't just summarize files: connect the dots between what was assumed, what was planned, what was built, what the jury criticized, and how the demo actually functioned.

## Steps

### 1. Collect and parse project state
Run the retrospective engine:
```bash
python3 "<plugin>/scripts/retro.py" .hackathon --write
```
If Python isn't available, follow `templates/retro.md` and analyze the existing files directly.

### 2. Connect the dots (Causal analysis)
Look for evidence-backed relationships across phases:
- **Untested assumptions vs. demo cracks:** Did an unvalidated assumption (e.g. `[?]` or `[AI]`) lead to a demo failure or failure-drill weakness?
- **Planning overload vs. incomplete features:** Did a member with >85% task allocation in `PLAN.md` cause unbuilt features, delayed joins, or late code freezes?
- **Mock disclosure vs. pitch honesty:** Did early deck drafts claim functionality that was merely mocked or untested?
- **Unaddressed jury criticisms:** Did multiple jurors across trials flag the same weakness without the team addressing it?

### 3. Ask for team feedback
Use AskUserQuestion (optional, 2 questions max):
1. **Live judging feedback:** What did the real judges ask or criticize during presentation?
2. **Biggest team surprise:** What broke that the team didn't anticipate?
Record answers with label `[T]`. Never invent judge questions or team reactions.

### 4. Distinguish evidence levels
- `[V]`: Verified runs, timing benchmarks, test suite pass rates, and recorded trial decisions.
- `[T]`: Notes typed by the team, live judge feedback, self-reported hours.
- `[AI]`: Identified patterns, causal connection proposals, recommended future improvements.
- `[?]`: Unknown or unrecorded outcomes.

### 5. Prioritize top 3 improvements
Identify the 3 highest-leverage practices to adopt in the next event:
1. One upstream discovery improvement (Phase 1–6).
2. One execution / demo verification improvement (Phase 11–12).
3. One pitch / disclosure alignment improvement (Phase 13).

## Output
Write `.hackathon/RETRO.md` from `templates/retro.md`. In `STATE.md`, log "retrospective completed: 3 lessons recorded" in the Decisions log and update "Last updated".

## Finish
Give a 4-line summary: goals achieved vs missed, total assumptions validated vs open, biggest demo failure or risk caught, and the #1 improvement for next time.
