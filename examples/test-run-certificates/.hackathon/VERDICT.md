# VERDICT — One trip, planned MVP (full trial)

> Summary: INCONCLUSIVE · NOT GUILTY 5 · GUILTY 0 · INSUFFICIENT EVIDENCE 7 · 12 of 12 valid votes · rubric estimate 68/100

**DECISION: INCONCLUSIVE.** The jury won't decide until experiment 1 runs. Nobody voted GUILTY.
On trial: "Does this solution, as planned, solve the real problem for its real users?"
Jury: civic seats (Government clerk, Policy officer, Citizen advocate in seats 4, 5, 9) · full 12
Average confidence: 5.5/10 (how sure jurors were, not a probability of success)

> Simulated jurors are perspectives, not real users or experts. Use this verdict to decide what to test and fix, not as proof.

## Votes
| # | Juror | Vote | Conf | Evidence | Reason |
|---|---|---|---|---|---|
| 1 | Actual end user | INSUFFICIENT EVIDENCE | 5 | weak | Real pain [V]; unknown whether documents cause most rejections |
| 2 | Least-digital user | NOT GUILTY | 5 | medium | No app, typing or English; the pre-visit call is mocked |
| 3 | Front-line worker | INSUFFICIENT EVIDENCE | 5 | weak | Few taps, but speed and false flags untested |
| 4 | Government clerk | INSUFFICIENT EVIDENCE | 6 | weak | Logging helps; operator uptake untested |
| 5 | Policy officer | NOT GUILTY | 5 | medium | Advisory, needs no portal; fits the rules |
| 6 | Root-cause analyst | INSUFFICIENT EVIDENCE | 6 | weak | Eligibility and Tahsildar causes untouched |
| 7 | "Already exists" researcher | INSUFFICIENT EVIDENCE | 5 | weak | Checklists exist; no prior-art scan in the case |
| 8 | Safety and ethics reviewer | NOT GUILTY | 5 | medium | Human decides, logged, masked; false-confidence risk |
| 9 | Citizen advocate (NGO) | INSUFFICIENT EVIDENCE | 6 | weak | Outreach before the visit is mocked |
| 10 | Engineer | NOT GUILTY | 6 | medium | Buildable in 22 h; name matching is the demo risk |
| 11 | Statement-owner judge | NOT GUILTY | 6 | medium | Answers the statement directly |
| 12 | Sceptic | INSUFFICIENT EVIDENCE | 6 | weak | Both killer assumptions are [?] |

No vote or invalid: none. Raw votes: `court/verify/votes-raw.json`.

## Contradictions between jurors
| Jurors | Disagreement | Evidence favours |
|---|---|---|
| Researcher vs citizen advocate | "Drop the pre-visit call (duplicates existing lists)" vs "make the pre-visit call real" | Advocate: existing lists are English and online [V-guide]; the call reaches non-readers. Keep it, but in L1 |
| Least-digital user vs front-line worker | "Fits me" vs "untested at rush hour" | Both right; experiment 2 decides |

## Ratings /10
| Item | Score | Why (labels) |
|---|---|---|
| Problem is real | 8 | Rejection means starting again [V], 21 days [V] |
| Problem matters | 6 | Frequency unknown [?] |
| Solution fits the root cause | 5 | Covers document causes only; eligibility untouched |
| Works for real users | 6 | Least-digital fit good; operator uptake [?] |
| Fits existing systems | 7 | In front of the portal, no integration |
| Safe | 8 | Flags only, logged, masked |
| Buildable and demo-able | 7 | One journey; name matching risky [AI] |
| Different from what exists | 5 | Checklists exist; the moment and the voice are the difference |

## What's genuinely strong
1. The cost of a rejection is verified [V]: start again, up to 21 days.
2. Safety design: the operator decides, nothing says "approved", scans aren't stored.

## Weakest assumption
Document problems cause most rejections — [?] — kill test: **collapses** (named by 9 of 12 jurors)

## What we're overlooking
- **Eligibility:** 4 jurors independently suggested warning about likely ineligibility (an income limit for the purpose) before submission. This is a rejection cause the document check can't catch.
- No prior-art scan of existing pre-check tools was given to the jury.

## An alternative approach (same problem, same user)
- A purpose-first "Am I eligible, and what do I bring?" voice line, with the counter check as an add-on.

## Ranked improvements
| # | Change | Impact | Effort | Priority | Raised by | Inside the core? | How to check it worked |
|---|---|---|---|---|---|---|---|
| 1 | Run experiment 1 (operators tally rejection reasons) | high | low | P0 | 9 jurors | yes | 6+ of 10 document-caused |
| 2 | Run experiment 2 (timed counter run, false flags) | high | low | P0 | Front-line worker, clerk | yes | Under 30 s, few false flags |
| 3 | Rules-based eligibility warning (income limit by purpose) | high | medium | P1 | Root-cause, end user, advocate, sceptic | yes (adds a check, same user and journey) | Warns on a test case over the limit |
| 4 | Say aloud: "eligibility and the Tahsildar's decision aren't checked" | high | low | P1 | Safety reviewer | yes | Spoken in the demo |
| 5 | Pre-test on real sample scans; cache TTS; backup video | high | low | P1 | Engineer | yes | Demo runs offline |

## Next experiment (30 min)
Test: phone 3 Nadakacheri/CSC operators; tally their last 10 rejections by reason.
PASS if: 6+ of 10 are document issues for at least 2 operators.
FAIL if: most are eligibility or Tahsildar decisions → pivot the core check to the eligibility warning.

## If I were your team…
Make the three phone calls now. The answer decides whether you build a document checker or an eligibility checker.

## Rubric estimate (strict judge; an estimate, not a prediction)
| Criterion | Weight | Score /10 | Why | One thing that raises it |
|---|---|---|---|---|
| Problem understanding | 25 | 7 | Cost of rejection verified | Real rejection-cause data |
| Innovation | 25 | 6 | Moment + voice; checklists exist | Eligibility + document check together |
| Feasibility | 20 | 8 | One honest journey | Real scans pre-tested |
| Impact | 20 | 6 | Frequency unknown | Experiment 1 numbers |
| Presentation | 10 | 7 | Clear persona | Live mismatch caught on stage |
| **Total** | | **68/100** | | |

## Mistakes check
✅ problem-first · ✅ no app · ✅ least-digital user · ✅ AI never decides · ✅ competitors named · ✅ numbers labelled · ✅ no drift · ✅ one journey · ✅ backup demo planned · ⚠️ slides not made yet · ⚠️ #11: two "collapses" assumptions still `[?]`; don't present the jury as proof · ✅ more than one idea considered

## Claims check
| Claim | Status |
|---|---|
| Rejection means starting again (Odisha) | [V] |
| 21 days (Karnataka in person) | [V] |
| "Under 30 s" | [AI]: present as a target |
| "Catches most rejections" | ❌ unsupported: removed; say "catches document-caused rejections" |

**Next →** `/hack:assumptions` and experiment 1, then continue to `/hack:pitch`
