# VERDICT — OPD Saathi solution (illustrative sample)

> Summary: PASS · NOT GUILTY 9 · GUILTY 2 · INSUFFICIENT EVIDENCE 1 · 12 of 12 valid votes

> This is an **illustrative sample** of the output format, not the result of a real trial run.

**DECISION: PASS**
On trial: "Does this solution, as planned, solve the real problem for its real users?"
Jury: healthcare seats · full 12
Average confidence: 7.1/10 (how sure jurors were, not a probability of success)

> Simulated jurors are perspectives, not real users or experts. Use this verdict to decide what to test and fix, not as proof.

## Votes (sample)
| # | Juror | Vote | Conf | Evidence | Reason |
|---|---|---|---|---|---|
| 1 | Actual end user | NOT GUILTY | 8 | medium | Voice check-in in my language while I wait anyway |
| 2 | Least-digital user | NOT GUILTY | 7 | medium | A normal phone call works; counter entry if no phone |
| 3 | Front-line worker | GUILTY | 6 | weak | Vitals entry by token adds a step in rush hour |
| 4 | Senior doctor | NOT GUILTY | 7 | medium | I approve every test; the case sheet stays mine |
| 5 | Hospital administrator | INSUFFICIENT EVIDENCE | 5 | none | Can't tell if it fits our software without an integration plan |
| 10 | Engineer | NOT GUILTY | 8 | strong | One journey is buildable; ABDM mocked |
| … | … | … | … | … | … |

## Contradictions between jurors
| Jurors | Disagreement | Evidence favours |
|---|---|---|
| Front-line worker vs senior doctor | Extra step for nurses vs time saved for doctors | Unclear: needs timing on the prototype |

## Ratings /10 (sample)
| Item | Score | Why (labels) |
|---|---|---|
| Problem is real | 9 | [T] doctor's estimate, [V] wait-time studies |
| Problem matters | 9 | [V] large OPD volumes |
| Solution fits the root cause | 8 | Uses waiting time [AI] |
| Works for real users | 7 | Call path added; voice untested [?] |
| Fits existing systems | 7 | Level 0 works; integration plan missing |
| Safe | 8 | Rules engine, doctor approval |
| Buildable and demo-able | 7 | One journey, mocked ABDM |
| Different from what exists | 7 | Voice + approved tests while waiting |

## What's genuinely strong
1. Uses the waiting time instead of adding new steps for patients [AI]
2. The doctor stays in charge of every test [T]

## Weakest assumption
Patients can describe symptoms by voice in a noisy OPD — [?] — kill test: collapses

## What we're overlooking
- Nurse workload in rush hour (contradiction above)

## An alternative approach (same problem, same user)
- A volunteer at the counter enters check-in details for patients without phones

## Ranked improvements
| # | Change | Impact | Effort | Priority | Raised by | Inside the core? | How to check it worked |
|---|---|---|---|---|---|---|---|
| 1 | Demo the phone-call path, not only WhatsApp | high | low | P0 | Least-digital user | yes | Judges see a keypad-phone check-in |
| 2 | Time vitals entry and show nurse time saved | high | medium | P1 | Front-line worker | yes | Under 30 s per entry |
| 3 | Label all impact numbers as pilot targets | medium | low | P1 | Sceptic | yes | No unlabelled numbers in the deck |

## Next experiment (30 min)
Test: 3 people describe a symptom by voice in Kannada on a normal call.
PASS if: 2 of 3 transcripts keep their exact words.
FAIL if: fewer than 2.

## If I were your team…
Lead the demo with Ramesh uncle's phone call, not the dashboard.

**Next →** continue to `/hack:pitch`
