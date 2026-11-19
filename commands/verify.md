---
description: "Phase 12 · Put the planned solution on trial with Hack Court 2.0 and check rubric, mistakes, claims and assumptions. With --demo: Demo Day Court on the built product"
argument-hint: "[--quick] [--demo]"
---

# /hack:verify — Put the solution on trial

> **Phase 12 of 14** · Reads: `BRIEF.md`, `EVIDENCE.md`, `COMPETE.md`, `CORE.md`, `PLAN.md`, `ASSUMPTIONS.md` · Writes: `VERDICT.md`, `court/` · Next: `/hack:pitch` (or `/hack:improve`)

Arguments: $ARGUMENTS

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md` and the files above.


Profile settings used: `verify_jury`, `demo_court`, quick-jury swap (from STATE.md → Profile; older projects use the Full/Quick table in the skill).
## Goal
Find out, before the judges do, whether the planned solution really solves the problem, and what to fix in the time left.

## Steps

### 1. Trial
Run the `hack-court` skill.
- **Evidence pack:** the CORE.md journey, the PLAN.md MVP scope (built vs mocked, labelled `[T]`), the top `[V]` and `[T]` facts from EVIDENCE.md, the closest competitor and honest difference from COMPETE.md, and the top 3 open assumptions.
- **On trial:** "Does this solution, as planned, solve the real problem for its real users?"
- Use quick mode if `--quick` was passed or STATE.md says quick. Tell the user the cost before starting.

### 2. Rubric check
| Criterion | Weight | Score /10 | Why | One thing that raises it |

Score like a strict judge would. Show the weighted total out of 100, and say plainly that it's an estimate, not a prediction.

### 3. Mistakes check
Mark each item in the skill's "Mistakes to block" table ✅, ⚠️ or ❌, with one line each.

### 4. Claims check
List every number and claim in CORE.md and PLAN.md and mark each one:
- `[V]` with a link, or `[T]`;
- `(target)`;
- ❌ unlabelled, or `[AI]` presented as a fact.

Every ❌ must end up sourced, relabelled as a target or an estimate, or removed.

### 5. Assumptions check
If the decision is INCONCLUSIVE or capped, the next experiment comes **before** more building or pitching.

List the open "collapses" and "weakens" assumptions. For each one, say whether the demo depends on it, and what the team should say if a judge asks.

## Output
Write `.hackathon/VERDICT.md`: the decision and ratings (with a link to the trial in `court/`), the rubric table, the mistakes table, the claims table and the assumptions check. Tick "verify" in STATE.md.

## Finish
Give 3 lines: the decision, the rubric total and the top remaining risk.
**Next:**
- **PASS** → `/hack:pitch`, then `/hack:verify --demo` once the product is built.
- **REVISE or FAIL** → `/hack:improve` (only inside-the-core changes once CORE is locked), then `/hack:pitch`.
- **INCONCLUSIVE** → `/hack:assumptions` and the next experiment.

---

## Demo mode: `/hack:verify --demo` (Demo Day Court)

Run this **after building**, ideally 4–6 hours before code freeze, and again after fixes. It judges the product as it will actually be demoed, not the plan. Skip it for ideathons (profile: `demo_court: not applicable`).

**Golden rule:** a feature counts as *tested* only if it was **run** and the result was seen. Code existing is not evidence. Anything you run and observe is `[V]` (measured); the team's word is `[T]`.

### D1. Feature ladder
From PLAN.md (Build / Mock / Cut and the demo journey), list every feature in the demo journey:

| Feature | Planned | Built (where) | Tested (how, result) | Shown in demo run | Mocked → disclosed in pitch? |
|---|---|---|---|---|---|

- **Built:** point to the file, endpoint or screen. Look in the repo: read the code, list the routes.
- **Tested:** if you can run it, do it (start the app, call the endpoint, run the script on the seeded data, run the test suite) and paste the command plus one line of output. If you can't run it, ask the team to run it and record their answer as `[T]`.
- A mocked feature is fine **only if** the pitch says it's mocked.

### D2. Demo walk
Walk the 90-second demo script step by step, as it will be shown:

| # | Step | Expected | Actual | Pass? | Time |
|---|---|---|---|---|---|

Then a **failure drill** on the riskiest step: no internet, a missing API key, a slow or wrong AI answer. Does the planned fallback actually work? Is the backup video recorded?

### D3. AI test cases
Run the AI test cases from PLAN.md that can be run, and record the actual behaviour next to the expected one. Count passes. Any safety case that fails (a wrong answer with no human check) is a P0.

### D3b. Disclosure check (before the trial)
Write the draft "What we'll say about mocks" lines, then check each one against the ladder **as it is right now**:
- A line may only say what exists. If the voice clip isn't recorded yet, the line says "voice is not built yet; text only", not "voice is pre-recorded".
- Every mocked or not-built feature in the demo journey needs a line. Every line needs a ladder row.
- Mark lines that depend on a fix ("true once fix 2 is done"), and re-check them after the fixes.

A disclosure that overstates what exists is a P0: judges treat it as a false claim, even when the mock itself would have been fine.

### D4. Demo Day Court
Run the `hack-court` skill with:
- **On trial:** "Does the built product, as it will be demoed, honestly prove that it solves the real problem for its real users?"
- **Evidence pack:** the feature ladder, demo walk and failure-drill results, AI test results, the mock disclosures, and the top 3 open assumptions. Use the labels from D1 and D2: measured runs `[V]`, team reports `[T]`.
- **Jury size:** the profile's `demo_court` (quick 7 or full 12). The engineer and the sceptic matter most here. Jurors are told: *"Count a feature as working only if the ladder shows it tested."*
- Pass `--open-collapses` to the vote counter as usual.

### D5. Fix list for the hours left
Merge the jurors' `fix` fields with your own: a fix named by 3+ jurors goes to the top. Rank the fixes by impact on the demo ÷ hours, and keep only what fits before code freeze (from STATE.md). For everything else, decide what to **say** in the pitch (for example, "the SMS step is mocked; here's why"). Ask the captain (AskUserQuestion) which fixes to do.

### Output (demo mode)
- `.hackathon/DEMO.md` from `templates/demo.md`: ladder, walk, failure drill, AI tests, verdict link, fix list, what to say about mocks.
- Trial records in `court/demo-<n>/`.
- In STATE.md, log "demo check <n>: <decision>, <x>/<y> steps passing".
- If PITCH.md exists, update its "built vs mocked" answer and slide claims to match the ladder, and list what changed.

### Finish (demo mode)
Give 3 lines: steps passing (x of y), the decision, and the one fix to do next.
**Next →** fix, then `/hack:verify --demo` again, or `/hack:pitch --drill`.
