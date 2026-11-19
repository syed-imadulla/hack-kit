# CORE — One trip

> LOCKED: Day 1 11:40 IST · Version v2 · risk logged: 2 "collapses" assumptions untested

> Summary: a counter-side pre-check and spoken checklist so certificate applicants find out what's missing before they submit.

Version: v2

## 1. Name and motto
**One trip.** "One trip, not three."

## 2. Positioning line
For first-time and low-literacy applicants who lose trips to rejected certificate applications, One trip is a counter-side pre-check that tells them what's missing before they submit.

## 3. Problem (2 lines + strongest sourced number)
In Odisha, a rejected certificate application can't be revived; you apply again from scratch ([V] Odisha e-District FAQ). In Karnataka, an income certificate takes up to 21 days by the in-person route ([V] tumkur.nic.in), so a rejection costs weeks.

## 4. Persona story — before vs after
| Before | After |
|---|---|
| Lakshmi brings what her father thinks is needed | She gives a missed call, says "income certificate" and hears the exact list in Kannada |
| The operator uploads; she's rejected 10 days later | The operator's scans get a 30-second check: "income proof missing, father's name spelled differently" |
| She starts again and nearly misses the scholarship | She returns the next morning with the right paper; one submission |

## 5. End-to-end journey
| # | Who acts | Channel / device | System does | Human decides |
|---|---|---|---|---|
| 1 | Applicant | Missed call / WhatsApp voice | Calls back, asks **what it's for** (scholarship, job, scheme), maps that to the certificate, reads the checklist aloud in Kannada, and SMSes it to a family number | — |
| 2 | Applicant | CSC counter | — | Brings documents |
| 3 | Operator | Drag the existing scan folder (PDF/JPG) | In under 30 s: checks type, readability, name match across documents, date validity, and that the income proof matches the declared income band | — |
| 4 | System → operator | One screen | Shows "looks complete" or "possible issue, please check" per document, with a Kannada sentence to read aloud. Never says "approved" | Operator decides to submit or ask for more |
| 5 | Operator | Seva Sindhu (unchanged) | — | Submits |

## 6. Who does what
| Role | Does | Never has to |
|---|---|---|
| Applicant | Calls once, brings documents | Install an app, read or type |
| Operator | Clicks "check" on scans they already made | Re-photograph documents |
| Verifying officer | Nothing changes | Use a new system |

## 7. USPs (each tied to a user pain)
1. Find out before submitting, not days later.
2. Spoken Kannada: no reading needed.
3. Uses the operator's existing scans: no extra photos.
4. Flags only, never blocks: the operator stays in charge.
5. Honest scope: catches document-caused rejections, not field verification or eligibility.

## 8. AI vs rules vs humans
| Step | AI does | Fixed rules do | Human decides | If AI fails |
|---|---|---|---|---|
| Checklist | — | Checklist config file per certificate, with a "last checked" date | — | Printed card |
| Document type | Classifies the scan | — | Operator confirms | Operator ticks manually |
| Name match | Fuzzy match across scripts | Exact-match fallback | Operator confirms | Operator compares by eye |
| Date validity | Reads the date | Rule: income proof within 1 year | Operator | Manual |

## 9. Inclusion (least-digital user)
Spoken checklist on a missed call; the operator reads results aloud; no phone needed at the counter.

## 10. Fit with existing systems (levels 0–3)
L0 standalone · L1 DigiLocker fetch when the citizen consents (covers documents already there; we still check self-declarations and new documents) · L2 summary attached · L3 built into Seva Sindhu.

## 11. Privacy basics
Scans are processed in memory and never stored; Aadhaar numbers are masked on screen and in logs; nothing is sent to the portal by us. Shown live in the demo.

## 12. Out of scope
Approving applications, field verification, eligibility decisions, judging whether a self-declared income is believable, filing on the portal.

## 13. Open assumptions
| Assumption | Label | Kill test | Status |
|---|---|---|---|
| Document problems cause most rejections | [?] | collapses | testing (experiment 1) |
| Operators will run the check | [?] | collapses | testing (experiment 2) |
| Check runs in under 30 s on existing scans | [AI] | weakens | open |
| Applicants can name the purpose | [AI] | weakens | open |
