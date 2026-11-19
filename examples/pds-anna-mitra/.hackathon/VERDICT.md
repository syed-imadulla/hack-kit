# VERDICT — PDS Anna-Mitra (Final Showcase Review)

> Summary: REVISE (capped by open collapses assumptions) · NOT GUILTY 12 · GUILTY 0 · INSUFFICIENT EVIDENCE 0 · 12 of 12 valid votes · Rubric estimate: 84/100

**DECISION: REVISE (capped by 3 open collapses assumptions).**
On trial: "Does PDS Anna-Mitra, as implemented and verified, solve the real problem for its real users under operational constraints without unverified claims?"
Jury: Civic domain seats (full 12)
Average confidence: 9.1 / 10

> Simulated jurors are perspectives, not real users or government officials. Use this verdict to decide what to test and fix, not as proof.

*Procedural note:* All 12 jurors voted NOT GUILTY, unanimous in praising the technical execution: 28 automated tests passing with zero failures, genuine local SQLite WAL transactions in under 15ms, deterministic calculation of free central NFSA PMGKAY grain, real tamper detection via hash chaining and HMAC signing, honest disclosures of mocked telephony and biometric sensors, and transparent handling of distributed split-brain double drawals. Under Hack Court rules, because the three critical collapses assumptions (A1, A2, A7) remain open in the field (`[?]`), the procedural decision is capped at **REVISE** until physical field deployment.

## Votes
| # | Juror | Vote | Conf | Evidence | Reason |
|---|---|---|---|---|---|
| 1 | The safety and ethics reviewer | NOT GUILTY | 9 | strong | Zero PII announced; no biometric data stored locally; preserves citizen privacy on shared phones |
| 2 | The sceptic | NOT GUILTY | 9 | strong | Live tamper drill is genuine: SQLite SQL updates fail verify-chain instantly with exact row index |
| 3 | Government clerk | NOT GUILTY | 9 | strong | Clean legal decoupling: central PMGKAY free grain separated from state add-ons; prevents illegal charges |
| 4 | The front-line worker | NOT GUILTY | 9 | strong | Two-tap dispense executes in < 15ms locally; realistic speed for morning queue pressure |
| 5 | The least-digital user | NOT GUILTY | 9 | strong | Spoken Kannada numbers are clear, slow, and easy to understand without any mobile app or internet |
| 6 | The budget holder | NOT GUILTY | 9 | strong | Cost model is completely sustainable: zero new POS hardware and pennies per voice query |
| 7 | The domain expert | NOT GUILTY | 9 | strong | 28 passing tests verify statutory compliance with NFSA PMGKAY free foodgrain through 31 Dec 2028 |
| 8 | The builder | NOT GUILTY | 10 | strong | Clean code architecture. Standard library cryptography, WAL mode SQLite, and comprehensive test coverage |
| 9 | The data protection advocate | NOT GUILTY | 9 | strong | Truthful disclosure of mocks: explicitly disclosed simulated telephony PRI and biometric hardware |
| 10 | The systems architect | NOT GUILTY | 9 | strong | Multi-terminal reconciliation engine accurately detects split-brain duplicate card disbursements upon sync |
| 11 | The maintenance engineer | NOT GUILTY | 9 | strong | The verify-chain command outputs human-readable diagnostic messages with zero complex dependency overhead |
| 12 | The devil's advocate | NOT GUILTY | 9 | strong | Retaining the three open collapses assumptions with [?] labels preserves scientific integrity |

## Ratings /10
| Item | Score | Why (labels) |
|---|---|---|
| Problem is real | 9 | NFSA statutory rules verified [V]; queue friction and outage delays documented [V] |
| Problem matters | 9 | Food security touches 800M+ citizens; lost daily wage is ₹350/day [V] |
| Solution fits root cause | 8 | Fixes pre-travel information gap and counter queue stall without smartphone gatekeeping |
| Works for real users | 7 | Keypad phone voice fit is strong; dealer rush-hour adoption remains open [?] |
| Fits existing systems | 9 | Operates standalone (Level 0) without requiring immediate government IT clearance |
| Safe | 9 | Zero PII in voice stream, zero biometrics stored, tamper-evident audit trail |
| Buildable and demo-able | 10 | Fully functional CLI prototype, 28 passing automated tests, live tamper drill [V] |
| Different from what exists | 8 | Voice-first and offline-first vs smartphone apps that fail in rural dead zones [V] |

## What's genuinely strong
1. **Verifiable Technical Execution**: A genuinely working SQLite3 database with HMAC-SHA256 signatures and SHA-256 hash chaining, verified by 28 automated unit & integration tests (`tests/test_pds_counter.py` and `tests/test_security_stress.py`).
2. **Honest Distributed Systems Boundary**: Acknowledging that offline terminals cannot prevent split-brain double drawals in real time under the CAP theorem, and resolving them via asynchronous conflict detection upon central sync (`CONFLICT_DUPLICATE_OFFLINE_DRAWAL`).
3. **Strict Policy Compliance**: Legally decoupling statutory central NFSA PMGKAY free foodgrains (through 31 Dec 2028: 35 kg AAY / 5 kg PHH member) from dynamic state add-ons (Karnataka 2026-27), ensuring citizens cannot be misled or overcharged.
4. **Methodological Realism**: Keeping the three critical collapses assumptions (A1, A2, A7) strictly labeled as open `[?]` awaiting physical field deployment, refusing to fabricate simulated surveys as field proof.
