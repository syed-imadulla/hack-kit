# Hack Kit v1.0 — first end-to-end test run

> Summary: the full 14-phase flow was run on a mock 24 h hackathon with 3 problem statements, using 48 real subagent calls for the courts. It worked end to end and produced a 34-page Idea Pack. It also found 11 problems, and all 11 are fixed in v1.0.1.

**Date:** 19 Nov 2026 · **Run by:** Claude, following the command files exactly, playing the team and captain · **Project:** [`examples/test-run-certificates`](../examples/test-run-certificates/.hackathon)

## Set-up
- **Event:** mock 24 h college hackathon, social-good track. Rubric: Problem 25, Innovation 25, Feasibility 20, Impact 20, Presentation 10.
- **Team:** 4 people (backend, frontend, AI/speech, design/pitch), with sponsor credits for Indian-language speech.
- **Statements:** S1 farm prices (agriculture) · S2 repeat visits for government certificates (civic) · S3 reading levels (education).
- **Real research:** 7 web searches and 6 sources opened (one fetch failed and was labelled `[AI]`).
- **Courts:** 3 quick trials in `/hack:pick` (one rerun after a fix), 1 quick re-trial in `/hack:improve`, 1 full 12-juror trial in `/hack:verify`. Each juror was a separate subagent that read only the case files.

## What happened
| Phase | Result |
|---|---|
| decode | 3 statements decoded; the smarter angle for S2 was a pre-submission document check |
| pick | Round 1 (snippets only): **INCONCLUSIVE**, with 5 of 6 jurors saying insufficient evidence. After opening 2 sources per statement: **S2 REVISE, S1 REVISE** → captain picked S2 |
| users | Persona Lakshmi, 19, needing an income certificate for a scholarship; motto "One trip, not three." |
| ideate | 13 ideas from 6 directions + constraint removal; chose a combination: spoken checklist before the visit + operator check on existing scans |
| validate | 3 `[V]` facts; **no public data on rejection causes** → 2 experiment cards (phone 3 operators) |
| compete | Closest: Seva Sindhu + DigiLocker; difference = *when* the check happens and spoken Kannada |
| stress | 14 doubts, 4 failure scenarios, CORE v1 |
| improve | 7 inside-core fixes → CORE v2; re-trial votes went from NG 4 · IE 2 to **NG 5 · IE 1**; PASS by votes, **capped to REVISE** while 2 killer assumptions are untested |
| lock | Locked with the risk logged |
| plan | One journey, 3 seeded scan sets, 10 AI test cases, failure fallbacks |
| verify | Full jury: **NG 5 · G 0 · IE 7 → INCONCLUSIVE**: "run experiment 1 first". 4 jurors independently proposed an **eligibility warning**, a real improvement the team hadn't thought of |
| pitch, ship | 6-slide outline, form answers, 8 judge Q&As; FINAL.pdf (34 pages) and BRIEF.pdf (15 pages) |

## Time and cost
| | |
|---|---|
| Machine time (Claude working, no waiting for people) | ~19 minutes for all 14 phases |
| Estimated team time (answering ~15 questions + reading outputs) | ~75–90 minutes to lock, within the guide's 80–100 min for 24 h |
| Real-world experiments | +30 minutes (phone 3 operators), not done in the test |
| Subagent calls | 48 (pick 26 including the rerun, improve 8, verify 14) |

## Problems found and fixed
| # | Problem found | Evidence from the run | Fix in v1.0.1 |
|---|---|---|---|
| 1 | **Pick trials ran on unopened search snippets** | 5 of 6 jurors voted INSUFFICIENT EVIDENCE | `/hack:pick` now has an **evidence boost**: open the 2 strongest sources per shortlisted statement before the trial. Unopened snippets are explicitly `[AI]` |
| 2 | **Decision rule too strict for small juries** | 4 NG + 2 IE (zero GUILTY) gave INCONCLUSIVE | INCONCLUSIVE only when abstentions are **more than** 1/3 |
| 3 | **PASS ignored abstentions** | PASS was computed only from decisive votes | PASS needs NOT GUILTY from 75% of **all** valid votes |
| 4 | **PASS possible with untested killer assumptions** | Improve re-trial passed by votes with 2 "collapses" assumptions at `[?]` | **Mandatory cap:** PASS → REVISE while any "collapses" assumption is untested (`tally.py --open-collapses`) |
| 5 | **Domain seat duplicated the end user** | "Citizen at the counter" and "Small farmer" answered almost exactly like "Actual end user" | Domain seats are now experts the jury lacks (clerk, policy officer, NGO advocate; agronomist, trader, FPO leader; …). A check blocks duplicates |
| 6 | **Quick jury more lenient than the full jury** | Quick re-trial NG 5/6 vs full trial NG 5/12; the missing seats were the evidence-focused ones | The **sceptic** now always sits on the quick jury (7 seats) |
| 7 | **Verify's evidence pack had no competitors** | The researcher juror said "no prior-art scan in the case" | Evidence packs include the closest competitor and honest difference from COMPETE.md |
| 8 | **Lawyers labelled the team's own plans `[V]`** | Defense cited the built/mocked list as verified | Plans, scope and build status are always `[T]`; added to the agent rules |
| 9 | **Improve had no baseline right after stress** | The only earlier trial was about the problem, not the solution | Improve compares with the stress doubts when there's no earlier solution trial, and **stops when the remaining P0s are experiments** |
| 10 | **Idea Pack too long to share** | FINAL.pdf was 34 pages | New **brief pack** (`compile.py --brief`): about 10–15 pages for mentors and judges |
| 11 | **No way to check a team's files mid-event** | A broken table only showed up when I checked by hand | New `scripts/lint_project.py`, run by `/hack:status` |

The two real juror vote sets from this run are now test fixtures (`tests/fixtures/votes-quick-*.json`), so these decision cases are checked on every push.

## What worked well
- **Evidence labels changed outcomes.** The same idea went from INCONCLUSIVE to REVISE once real sources were opened. The jury rewarded evidence, not confidence.
- **Ideation broadened the idea.** The chosen idea, a voice checklist plus a check on existing scans, wasn't the obvious "new portal" idea, and the "no AI" constraint exposed what the AI actually had to add.
- **The court produced a new idea.** The eligibility warning came from 4 independent jurors, not from the team.
- **Honesty held.** No interviews were invented. Experiment observations stayed empty, and the full jury refused to pass an idea built on untested assumptions.
- **The guardrails held.** No improvement drifted from the problem or the user; every fix was marked "inside the core".

## Limits of this test
- No real people. The tester played the captain and answered every question, and no venue interviews or experiments were run.
- The Claude Code interface itself (slash-command loading, AskUserQuestion pop-ups) wasn't exercised. The command files were followed by hand, and the subagents were general-purpose agents given the plugin's agent instructions.
- One problem domain was fully tested (civic). Agriculture got a quick trial; healthcare is covered by the OPD Saathi example.

## Next
Run the same flow with a real team at a real event, measuring time to lock, assumptions found, how often the verdict changes after `/hack:improve`, and whether the demo worked. Then decide what v1.1 should be.
