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
Run the same flow with a real team at a real event, measuring time to lock, assumptions found, how often the verdict changes after `/hack:improve`, and whether the demo worked. v1.1 was then built and tested; see below.

---

# Hack Kit v1.1 — test run of the new features

> Summary: the v1.1 features were run on the same project. A small prototype was built so the Demo Day Court had something real to judge: 2 lawyers and 7 jurors as separate subagents (9 calls). The verdict was a unanimous FAIL, and every juror named the same problem the kit should have caught first. That led to 4 fixes, all in v1.1.0.

## What was run
| Feature | How | Result |
|---|---|---|
| Event profile | `profile.py --type college --length 24h --experience mixed --focus balanced --team 4` | `## Profile` added to STATE.md |
| Plan check | 4 members, 14 tasks, 18 h to freeze | Critical path T3→T4→T5→T7→T12, 14 of 18 h ("tight"); load a 10.5 · b 7 · c 9 · d 8.5 h; 1 conditional task |
| Prototype | `app/onetrip.py`: checklist, name match, date rule, Aadhaar masking, flag log; OCR and voice mocked | Clean, blurry and mismatch scan sets behaved as expected (0.01 s per check) |
| AI test cases | 10 cases from PLAN.md, all run | 6 pass, 1 partial, 3 fail (Kannada script flagged instead of matched, random photo ignored, unsupported certificate not handed over) |
| Demo Day Court | Quick 7 with the government-clerk civic seat, `--open-collapses 2` | **FAIL**, 0 NG · 7 G · 0 IE, average confidence 6.9 |
| Pitch drill | 4 questions from a 3-judge panel; Claude played the team | Honesty averaged 1.75 of 5; the pitch vs product check found a false "built" line |

## Problems found and fixed
1. **Overstated mock disclosure.** The draft said "voice is pre-recorded" and "the missed call is a recorded clip". Neither existed yet. All 7 jurors caught it. → New step D3b, a disclosure check in `/hack:verify --demo`; a "True now?" column in DEMO.md; `lint_project.py` warns on untrue lines.
2. **Pitch written before building.** PITCH.md listed the folder watcher and TTS as built. → `/hack:pitch` takes the built-vs-mocked answer from DEMO.md, or marks it as the plan; demo mode updates PITCH.md.
3. **Votes rejected over wording.** Jurors wrote "moderate" instead of "medium", and all 7 votes were invalid. → `tally.py` maps harmless synonyms in memory (the raw file stays unedited); unknown words are still rejected. 2 new tests.
4. **Linter false positive** on "Problem judge (25%)". → Rubric-weight lines are recognised more broadly.

Earlier in v1.1 development, `plan_check.py` testing also fixed 4 gaps: a false skill gap on shared tasks, no hint for overload, conditional tasks counted, and no "tight" warning.

## What worked well
- The feature ladder made the gap between planned and built obvious within minutes.
- Running the AI test cases found 3 real failures that a read-through of the code would have missed.
- The jurors' `fix` fields agreed, so the fix list ranked itself.
- The court judged the *problem* too: 6 of 7 jurors said the operator-phone experiment still had to come first.

## Limits
- Same limits as v1.0: no real team; Claude played the captain and the team in the drill.
- The prototype was built in the workspace, not by a hackathon team, and OCR and voice were mocked.

---

# v1.2.2 review — a real Demo Day Court on the PDS example

> Summary: the PDS Anna-Mitra example shipped with 7 trials whose 84 votes were written in one pass (82 NOT GUILTY). The reviewer ran the prototype, found 2 bugs, and ran a real quick Demo Day Court with separate subagents. It returned FAIL 0–7.

| What | Result |
|---|---|
| Prototype run | Quota, offline dispense, verify-chain and tamper drill all worked [V]; dispense takes under 2 ms [V] |
| Bug 1 | The same card could be dispensed 20 times in one month at one shop [V] |
| Bug 2 | `--custom-rice 500` printed a 500 kg "100% FREE" receipt, 25× the quota [V] |
| Mislabels | Voice line called "Real" but prints text only; backup video claimed but missing |
| Demo Day Court 1 | Quick 7 with the government-clerk seat, `--open-collapses 3` → **FAIL**, 0 NG · 7 G · 0 IE, confidence 7.9 |
| After the trial | Monthly entitlement guard added; 4 tests; both bugs now rejected. Not re-tried. |

**Lesson for the kit:** one model writing all 12 votes produces confident, uniform agreement and misses what running the product reveals. Hack Court only works when each juror is a separate run and the evidence comes from actually running the product.
