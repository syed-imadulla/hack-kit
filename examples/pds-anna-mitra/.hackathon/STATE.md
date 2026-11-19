# STATE — PDS Anna-Mitra

> Summary: Civic & Public Service AI Hackathon · Phase 14 ship done · All 14 phases complete · Next: /hack:retro

Schema version: 2
Last updated: 2026-11-19 21:30 IST

| Field | Value |
|---|---|
| Event | Civic & Public Service AI Hackathon |
| Track | Public Distribution & Food Security |
| Event length | 24 h |
| Mode | full |
| Captain (final decider) | Team Lead (Captain) |
| Chosen statement | S1: Fair Price Shop quota uncertainty, wasted trips, and ePOS outage queues |
| Chosen idea | Anna-Mitra Dual-Channel (Pre-travel IVR/SMS + Tamper-Evident HMAC Offline Ledger) |
| Motto | Clear quotas before you walk; verified grain when the network drops. |
| CORE version | v2 |
| Core locked at | 2026-11-19 21:20 IST |

## Phases
| # | Phase | Status | When | Notes |
|---|---|---|---|---|
| 1 | start | done | 20:30 | Profile: civic, 24 h, mode: full |
| 2 | decode | done | 20:35 | Statutory NFSA vs state scheme bounds established |
| 3 | pick (trial) | done | 20:45 | S1 selected; illustrative verdict: REVISE (capped by 3 open collapses) |
| 4 | users | done | 20:48 | Personas: Lakshmi (beneficiary), Basavaraj (dealer), Ramesh (inspector) |
| 5 | ideate | done | 20:55 | 10 ideas evaluated; RationTrack app rejected; Dual-Channel selected |
| 6 | validate | done | 21:00 | 4 experiment cards created (EXP-01..04); illustrative verdict: REVISE (capped by 3 collapses) |
| 7 | compete | done | 21:05 | Benchmarked vs Mera Ration, Ahara, and paper registers; illustrative verdict: REVISE |
| 8 | stress | done | 21:10 | 22 failure scenarios analyzed; 8 security unit tests passing; illustrative verdict: REVISE |
| 9 | improve | done | 21:18 | Hardened to v2: 2-tap UI, zero-PII IVR, key rotation, clock checks; illustrative verdict: REVISE |
| 10 | lock | done | 21:20 | Core locked: problem, personas, journey, motto, non-negotiables |
| 11 | plan | done | 21:23 | Team workload balanced; critical path 16h / 18h to freeze verified |
| 12 | verify (trial) | done | 21:26 | Working prototype complete; 19 tests passing; illustrative verdict: REVISE (capped). Real Demo Day Court 1 (v1.2.2 review): FAIL 0–7; fix applied, 32 tests |
| 13 | pitch | done | 21:28 | Slide deck, Q&A drill, and pitch vs product verification complete |
| 14 | ship | done | 21:30 | Submission package complete: BRIEF, SUMMARY, VERDICT published |

## Decisions log
| Time | Decision | Why | Rejected (and why) | By |
|---|---|---|---|---|
| 20:30 | Select PDS quota transparency & outage resilience as problem | Affects vulnerable households daily; strong tension between central policy and ground reality | Generic farmer price advisory (crowded, lacks operational friction) | Captain |
| 20:35 | Strictly decouple Central NFSA (PMGKAY through 2028) from state add-ons | Avoids legally invalid claims of state entitlement guarantees | Hardcoding Karnataka Anna Bhagya rice quotas as permanent central entitlements | Captain |
| 20:35 | Clarify cryptographic boundary: HMAC + hash chaining gives tamper evidence, NOT statutory authority | Technical integrity of local records does not replace government ePOS clearance | Claiming "blockchain-grade" legal authorization for local offline overrides | Captain |
| 20:50 | Reject RationTrack mobile app (smartphones, webcams, GPS) | 70%+ of target AAY/PHH beneficiaries lack smartphones; grain trucks lack public GPS APIs; dealers won't fund webcams | Building an app-first MVP (hackathon anti-pattern that fails in the field) | Captain |
| 20:50 | Reject Web3 blockchain (Idea 7) and SmartCard NFC dongles (Idea 4) | Blockchains require continuous connectivity (anti-offline); smartcards require impossible 24h hardware logistics | Pursuing Web3 buzzwords over civic reality | Captain |
| 20:55 | Select Anna-Mitra Dual-Channel (Access shift IVR + Process shift HMAC ledger) | Solves both pre-travel wasted trips AND counter queue stalls without citizen hardware gatekeeping | Pure IVR (leaves counter stalled) and unsigned dealer app (unverifiable audit risk) | Captain |
| 21:00 | Clarify offline duplicate limitation: offline devices cannot prevent multi-location split-brain double drawals | Mathematical reality of disconnected nodes; conflict must be detected upon central sync | Claiming impossible local multi-device real-time consistency | Captain |
| 21:00 | Mark unperformed field experiments EXP-01, EXP-02, EXP-03 as PROPOSED | Preserves strict evidence integrity; avoids fabricating interviews or unperformed surveys | Claiming field validation without actual user testing | Captain |
| 21:05 | Formulate 4-tier coexistence model (Level 0 standalone to Level 3 statutory integration) | Enables non-intrusive companion rollout without requiring immediate ePOS firmware replacement | Demanding an immediate rip-and-replace of certified government hardware | Captain |
| 21:05 | Model state 5-10% offline exception quota limits directly in the architecture | Conforms to official government ePOS exception guidelines | Operating unregulated offline volumes that food inspectors will reject | Captain |
| 21:10 | Enforce monotonic sequence numbers and external checkpoint pinning | Defeats retroactive tampering, ledger truncation, and full rewrite attacks | Relying purely on local hash-chaining without external anchor pinning | Captain |
| 21:10 | Build executable security unit tests (`test_security_stress.py`) during stress phase | Backs stress mitigations with verifiable automated unit tests rather than prose | Making unverified security claims | Captain |
| 21:18 | Adopt 2-Tap Dispense Flow and Zero-PII IVR in Architecture v2 | Cuts dealer counter time to <15s and protects vulnerable beneficiaries on shared phones | 5-step dealer form and 4-digit IVR PINs (high friction / cognitive barriers) | Captain |
| 21:18 | Implement Key Rotation (`key_version`) and Monotonic Clock Rollback Checks | Defeats backdating and enables key retirement without historical invalidation | Single static key and blind sequence-only checking | Captain |
| 21:20 | Lock Core Architecture v2 in CORE.md | Fixes problem, personas, journey, motto, and non-negotiables before implementation | Permitting mid-hackathon scope creep or drifting back to naive mobile app | Captain |
| 21:23 | Plan 18-Hour Code Freeze with 16-Hour Critical Path | Provides a 2-hour safety buffer for verification, demo rehearsals, and video recording | Scheduling development up to the submission deadline | Captain |
| 21:26 | Deliver Fully Working CLI Prototype with 19 Automated Tests | Proves tamper-evident hash chaining, clock checks, and split-brain conflict detection | Delivering non-executable slides or mocked database wrappers | Captain |
| 21:28 | Complete 7-Slide Pitch Deck and Q&A Rehearsal Drill | Prepares team with rigorous, honest responses for tough judge inquiries | Overpromising unvalidated field metrics or hiding simulation limits | Captain |
| 21:30 | Ship Full Submission Brief and Verified Repository | All 14 phases successfully executed and audited under Hack Kit 2.0 methodology | Leaving project undocumented or skipping retrospective verification | Captain |

## Locked
- **Problem**: Fair Price Shop quota uncertainty, wasted trips, and ePOS outage queues.
- **Personas**: Kenchaiah & Ratnamma (rural beneficiaries), Basavaraj (FPS dealer), Ramesh (Food Inspector).
- **Core Journey**: 2-step Zero-PII IVR call + 2-tap offline HMAC receipt + central conflict reconciliation.
- **Motto**: Clear quotas before you walk; verified grain when the network drops.
- **Non-Negotiables**: Zero smartphone gatekeeping, Zero-PII voice privacy, <15s counter speed, 3-layer crypto audit, daily external checkpoint pinning, decoupled NFSA PMGKAY vs State add-ons, transparent CAP conflict detection.

## Pending
- [ ] Run post-hackathon retrospective (`/hack:retro`) to generate RETRO.md
- [ ] Complete final documentation and showcase verification audit

## Rules
- Distinguish verified statutory rules [V] from team hypotheses [T] and unverified field assumptions [?].
- Never claim local cryptographic verification equals official government transaction approval.
- Preserves all intermediate trial decisions, failure modes, and pivots.

## Next command
/hack:improve
