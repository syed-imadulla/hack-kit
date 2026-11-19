# IDEAS — Repeat visits for government certificates

> Summary: 13 ideas from 6 directions + constraint removal · chosen: "Ready-to-submit" check on the operator's existing scans + a spoken Kannada checklist before the first trip (combination of process + access shift) · riskiest assumption: document problems cause most rejections

## Root cause
| Why? | Answer | Label |
|---|---|---|
| 1 | People make repeat trips for certificates | [T] statement |
| 2 | Applications get rejected and must be filed again from scratch | [V] Odisha e-District FAQ |
| 3 | Documents are missing, unreadable, invalid or mismatched (among other reasons) | [V] guide, low reliability |
| 4 | Applicants and operators don't know the exact checklist and rules for each certificate | [AI] |
| 5 | Checklists are scattered, differ by state and certificate, and nobody checks before submission | [AI] |

- **Today's workaround:** ask the operator or a relative; guess; re-apply after rejection.
- **Who suffers most often:** first-time applicants (students needing scholarship certificates).
- **Who suffers the worst consequences:** farm labourers without standard income proof, who face repeated rejections and missed deadlines.

## Directions explored
| Direction | Idea | What makes it different |
|---|---|---|
| User shift | 1. Operator-side "ready-to-submit" check on the scans they already make | Serves the operator, who has the power to block it |
| User shift | 2. Help for the verifying clerk: auto-summary of each file's gaps | Serves the officer, not the applicant |
| Process shift | 3. Check *before* submission instead of finding out 10 days later | Moves the failure point earlier |
| Process shift | 4. Correction instead of re-application (policy proposal) | Changes the rule; not buildable in 24 h |
| Access shift | 5. Missed-call or WhatsApp voice line: say the certificate type, hear the exact checklist in Kannada | Works before the first trip, on any phone |
| Access shift | 6. A printed or SMS "what to bring" slip from the operator | No tech for the applicant |
| Integration shift | 7. Pull existing documents from DigiLocker instead of re-scanning | Uses an existing system |
| Integration shift | 8. Match the name across Aadhaar, ration card and certificates automatically | Catches the top mismatch reason |
| Prevention shift | 9. A school/college certificate camp before scholarship season | Prevents the rush |
| Prevention shift | 10. Remind people when a certificate is about to expire | Avoids last-minute applications |
| Technology shift | 11. A document classifier + OCR for name and date checks | Tech adds value only for the mismatch check |
| Constraint removal | 12. "No AI": a laminated checklist card per certificate at every CSC | Shows most value is in the checklist itself |
| Combination | 13. Spoken checklist line (5) **+** operator scan check (1, 8) | Fixes both "didn't know what to bring" and "brought the wrong thing" |

Constraint removal notes: with **no AI**, a good checklist (12) already solves a lot, so AI must earn its place on the mismatch check. With **no app**, ideas 5 and 6 work. **Solving 10% well** means the income certificate only, in one state.

## Scores (weights from the rubric: user value ×3, originality ×3, rubric fit ×2, buildable ×3, evidence ×1)
| # | Idea | Direction | User value | Originality | Rubric fit | Buildable | Evidence | Biggest risk | Total |
|---|---|---|---|---|---|---|---|---|---|
| 13 | Spoken checklist line + operator scan check | Combination | 5 | 4 | 5 | 3 | 3 | Two parts to build | 49 |
| 1 | Operator ready-to-submit check (obvious-ish) | User shift | 4 | 3 | 4 | 4 | 3 | Operator adoption | 44 |
| 5 | Spoken checklist line | Access shift | 4 | 3 | 4 | 5 | 2 | Doesn't catch wrong documents | 44 |
| 7 | DigiLocker pull | Integration | 4 | 3 | 3 | 1 | 2 | Needs DigiLocker partner access | 31 |
| 12 | Laminated checklist card (no AI) | Constraint removal | 3 | 1 | 2 | 5 | 3 | Low innovation | 31 |
| — | New online application portal (obvious) | Technology | 2 | 1 | 2 | 3 | 2 | Already exists in every state | 24 |

## Chosen idea
**"One trip": spoken checklist + ready-to-submit check.** Before the first trip, the applicant gives a missed call, says "income certificate", and hears the exact checklist in Kannada. At the counter, the operator runs the scans they already made through a 30-second check (right type, readable, name matches across documents, date valid) and reads out what's missing. It flags only, never blocks, and the operator decides.

Why:
1. It fixes both causes, "didn't know" and "brought the wrong thing".
2. It works for the least-digital user through a call and the operator.
3. It uses the operator's existing scans, answering the front-line juror's objection.

Chosen by: captain A · Day 1 10:45 IST (test run)

## Rejected ideas (and why)
| Idea | Why not now |
|---|---|
| 4 Correction instead of re-application | A policy change; not buildable |
| 7 DigiLocker pull | Partner access impossible in 24 h; roadmap |
| 2 Clerk summary | The applicant still makes the trip |
| New portal | Already exists; judges will have seen it many times |
| 12 Laminated card | Low innovation, but a fallback if the AI fails |

## Key assumptions of the chosen idea
| Assumption | Label | Kill test |
|---|---|---|
| Document problems cause most rejections | [?] | collapses |
| Operators will run a 30-second check on existing scans | [?] | collapses |
| Applicants will call before their first trip | [AI] | weakens |
| Name matching works across Kannada/English spellings | [AI] | weakens |
