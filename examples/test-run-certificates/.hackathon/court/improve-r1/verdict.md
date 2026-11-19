# VERDICT — One trip, CORE v2 (quick re-trial)

> Summary: REVISE (PASS by votes, capped) · NOT GUILTY 5 · GUILTY 0 · INSUFFICIENT EVIDENCE 1 · 6 of 6 valid votes

**DECISION: REVISE**: PASS by votes, capped because 2 "collapses" assumptions are untested
On trial: "Does this solve a real problem for its real users?"
Jury: civic seats (Government clerk in the quick seat) · quick 6
Average confidence: 5.3/10 (not a probability of success)

> Simulated jurors are perspectives, not real users or experts.

## Votes
| # | Juror | Vote | Conf | Evidence | Reason |
|---|---|---|---|---|---|
| 1 | Actual end user | NOT GUILTY | 6 | medium | 21-day restart after rejection is real [V]; checklist before travel helps |
| 2 | Least-digital user | NOT GUILTY | 6 | medium | Missed call + spoken Kannada; no app, typing or English |
| 3 | Front-line worker | INSUFFICIENT EVIDENCE | 5 | weak | Still an extra step; speed and failure behaviour untested |
| 4 | Government clerk | NOT GUILTY | 5 | medium | Advisory, operator decides; adds a step, untested |
| 6 | Root-cause analyst | NOT GUILTY | 5 | weak | Hits upstream causes; document share is [?] |
| 10 | Engineer | NOT GUILTY | 5 | medium | One journey fits in 22 h; telephony and Kannada OCR are demo risks |

## Contradictions between jurors
| Jurors | Disagreement | Evidence favours |
|---|---|---|
| Front-line worker vs government clerk | "Extra step at rush hour" vs "advisory, fine" | Unresolved: needs a timed counter trial |

## Weakest assumption
Document problems cause most rejections — [?] — kill test: collapses (raised by 3 of 6 jurors)

## Ranked improvements
| # | Change | Impact | Effort | Priority | Raised by | Inside the core? | How to check it worked |
|---|---|---|---|---|---|---|---|
| 1 | Tally real rejection reasons with 3–5 operators | high | low | P0 | Root-cause, end user | yes (experiment) | 6+ of 10 document-caused |
| 2 | Auto-run on the operator's existing scan folder | high | medium | P1 | Front-line worker | yes | Zero extra clicks |
| 3 | Test the voice flow with 5 elderly Kannada speakers, spoken input | high | low | P1 | Least-digital user | yes | 4 of 5 complete it |
| 4 | Seeded scan sets + recorded call for the demo | high | low | P1 | Engineer | yes | Demo runs offline |
| 5 | Log flags + operator decisions | medium | low | P2 | Government clerk | yes | Log visible in demo |

## Next experiment (30 min)
Test: phone 3 Nadakacheri/CSC operators; tally their last 10 rejections by reason.
PASS if: 6+ of 10 are document issues for at least 2 operators.
FAIL if: most are field verification or eligibility.

## If I were your team…
Make that phone call before you write a line of OCR code.

**Next →** `/hack:lock` (with the risk logged), or run the experiment first
