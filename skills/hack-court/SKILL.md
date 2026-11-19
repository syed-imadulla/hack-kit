---
name: hack-court
description: Run Hack Court 2.0 on a hackathon problem, idea, feature or pitch. Prosecution and defense argue from a labelled evidence pack, 12 independent juror subagents (with domain seats) vote GUILTY, NOT GUILTY or INSUFFICIENT EVIDENCE, and a judge gives PASS, REVISE, FAIL or INCONCLUSIVE with ranked improvements and the next experiment. Judges whether the problem is real and the solution truly solves it, never business viability. Used by /hack:pick, /hack:verify, /hack:improve and /hack:court.
---

# Hack Court 2.0 — problem-focused trial

## What's on trial
One question: **"Does this solve a real problem for its real users, as described?"** (Commands adapt the wording. `/hack:pick`, for example, asks whether a problem is worth solving here.)

| Juror vote | Means |
|---|---|
| **NOT GUILTY** | It does solve a real problem for its real users. |
| **GUILTY** | It does not solve a real problem for its real users. |
| **INSUFFICIENT EVIDENCE** | From this juror's lens, the evidence pack doesn't allow a decision. The juror must say what's missing. |

Never judge revenue, market size, pricing, business model or investor appeal. If a lawyer or juror brings these up, drop that point.

Read `${CLAUDE_PLUGIN_ROOT}/skills/hack-court/jurors.json` (jurors, domain seats, vote format) and `${CLAUDE_PLUGIN_ROOT}/templates/verdict.md` before starting. If `${CLAUDE_PLUGIN_ROOT}` isn't expanded, find the plugin root as described in section 1 of the `hack-kit` skill.

## Modes
| Mode | Jurors | Points per side | When |
|---|---|---|---|
| Full | 12 | 5 | default |
| Quick | 6 (the `"quick": true` seats) | 3 | `--quick`, quick mode in STATE.md, or low time or usage |

Before starting, tell the user the cost: about 15 subagent calls for a full trial, about 9 for a quick one.

---

## Step 1 — Evidence pack (you, the clerk)
Write `case.md` in `.hackathon/court/<case-slug>/`, or in `./court/<case-slug>/` if there's no `.hackathon/`. Keep it to about 200 words:

```
CASE: <one line>
QUESTION ON TRIAL: <question>
PROBLEM: who suffers, what, how often
REAL USERS: end user · least-digital user · operator
SOLUTION: 3–5 lines, step by step
CONSTRAINTS: time left, team skills, top rubric items, existing systems
EVIDENCE (labelled):
  [V] … (source, date)
  [T] …
  [AI] …
  [?] …
KEY ASSUMPTIONS: top 3 from ASSUMPTIONS.md, with labels
```
Build it only from `.hackathon/` files and what the user said. Don't add facts, and keep every claim's label exactly as it is in the source file.

## Step 2 — Domain seats
Look up the domain in BRIEF.md or STATEMENTS.md. If it matches a key in `domain_seats.domains` (healthcare, agriculture, education, finance, civic, climate), swap the three seats listed in `domain_seats.replaces` for that domain's three jurors. The first domain juror takes the quick-mode seat. If the domain isn't listed, or is unclear, keep the universal jurors and say so in the verdict.

## Step 3 — Prosecution and defense
Launch two subagents **in parallel** (the `hack-prosecutor` and `hack-defender` agents if available, otherwise general-purpose agents with the agent files' instructions). Each gets only `case.md` and N, the number of points.

- **Prosecution:** the strongest honest case that it does NOT solve a real problem for its real users.
- **Defense:** the strongest honest case that it DOES.
- Every point carries an evidence label, and any new source they cite includes a link. No business arguments.

Save them as `prosecution.md` and `defense.md`.

## Step 4 — Jury (independent)
Launch **one subagent per juror** (the `hack-juror` agent if available), in parallel batches of up to 6. Each juror gets **only** their persona (name, lens, asks), `case.md`, `prosecution.md` and `defense.md`. Jurors never see each other's votes.

Juror prompt:
```
You are juror #{n}: {name}.
Your lens: {lens}
Questions you care about: {asks}

Read the case, the prosecution and the defense.
Claims are labelled: [V] verified source, [T] team-provided, [AI] AI inference, [?] unknown.
Weigh [V] and [T] much more than [AI]. Treat [?] as unknown, never as true.

Vote GUILTY if it does not solve a real problem for its real users,
NOT GUILTY if it does, or INSUFFICIENT EVIDENCE if you can't decide from your lens.
Ignore revenue, market size, pricing and investors.

Reply with ONLY one JSON object:
{"juror": "{name}", "vote": "GUILTY" | "NOT GUILTY" | "INSUFFICIENT EVIDENCE",
 "confidence": 1-10, "evidence_strength": "strong" | "medium" | "weak" | "none",
 "reason": "<max 30 words>", "weakest_assumption": "<max 20 words>",
 "missing_info": "<max 20 words or 'none'>",
 "fix": {"change": "<max 25 words>", "impact": "high" | "medium" | "low", "effort": "high" | "medium" | "low"}}
```

### Collecting the votes
1. Save every raw reply, as received, to `votes-raw.json`, a JSON list. **Never edit this file afterwards.**
2. Count with the script:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tally.py" .hackathon/court/<case>/votes-raw.json --expected <12 or 6>
   ```
3. Re-run only the jurors the script reports as invalid, up to 2 retries each. Append the new replies to `votes-raw.json`. If a juror has a valid reply and a later invalid one, the valid one stands.
4. If a juror still fails, record it as `NO VOTE`. **Never invent a vote.** The script counts only the valid votes it received.
5. Log the retries in `trial-log.md`: juror, attempt number, problem.

If Python isn't available, apply the same checks and decision rules by hand, and say so in the verdict.

## Step 5 — Judge (you)
Use only the valid votes.

1. **Count:** NOT GUILTY, GUILTY and INSUFFICIENT EVIDENCE, out of the valid votes received. Average confidence.
2. **Contradiction check:** list where jurors disagree (for example, "end user says easy, least-digital user says impossible") and which side the evidence supports. Unresolved contradictions go into "What we're overlooking".
3. **Decision** (the script applies the same rule):
   | Decision | Rule |
   |---|---|
   | **INCONCLUSIVE** | Fewer than 2/3 of jurors gave valid votes, or INSUFFICIENT EVIDENCE is 1/3 or more of valid votes |
   | **FAIL** | GUILTY outnumbers NOT GUILTY |
   | **PASS** | NOT GUILTY is at least 75% of decisive votes, and fewer than half of votes rest on weak or no evidence |
   | **REVISE** | Anything else |

   You may move the decision **one step stricter** (PASS → REVISE, or REVISE → FAIL) if a safety risk or a critical `[?]` assumption is unresolved. Say why. Never move it in the lenient direction.
4. **Ratings out of 10** for the 8 items in `jurors.json → ratings`, each with a one-line reason. Lower any rating that rests mostly on `[AI]` or `[?]` claims.
5. **The improvement sections:**
   - **What's genuinely strong:** 2–3 points, with evidence labels.
   - **Weakest assumption:** the one most jurors flagged. Run the kill test: if it's false, does the idea collapse?
   - **What we're overlooking:** a missed opportunity or an unresolved contradiction.
   - **An alternative approach:** a different way to solve the *same* problem for the *same* user.
   - **Ranked improvements:** merge the juror fixes, remove duplicates, and rank by impact ÷ effort. Columns: # · change · impact · effort · priority (P0/P1/P2) · raised by · inside the core? · how to check it worked.
   - **Next experiment:** one test the team can do in the next 30 minutes, with a clear pass/fail rule.
6. **One line:** "If I were your team…"

## Step 6 — Output
Write `verdict.md` from `templates/verdict.md` and show the user:

```
DECISION: REVISE   (NOT GUILTY 8 · GUILTY 2 · INSUFFICIENT EVIDENCE 2 · 12 of 12 valid · avg confidence 6.9/10)
Simulated jurors: perspectives, not real users or experts. Confidence is not a probability of success.

| # | Juror | Vote | Conf | Evidence | Reason |
…
Contradictions · Ratings · Strong · Weakest assumption · Overlooking · Alternative
Ranked improvements · Next experiment · If I were your team…
Next → /hack:improve
```

Suggest the next step based on the decision: PASS → continue; REVISE → `/hack:improve`; FAIL → `/hack:improve` or reconsider (the captain decides); INCONCLUSIVE → `/hack:assumptions` and the next experiment.

Also update `ASSUMPTIONS.md`: add each juror's `weakest_assumption` that isn't already listed, labelled `[AI]` with the source "court <case>".

## Rules
- Jurors must be independent subagents. If the Agent tool isn't available (for example, in the Claude app), simulate the jury in one pass and print: "Simulated jury in one chat — less independent than the Claude Code version."
- The verdict is advice, not a decision. **The captain decides.**
- Never present juror votes as proof that real users accept the idea.
- Demo Day Court (a trial of the built product) is planned for v1.1.
