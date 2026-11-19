# DEMO — PDS Anna-Mitra (Demo Day Check 1)

> Summary: 5 of 5 demo steps passing · 5 of 5 automated test cases passing · decision: REVISE (capped by 3 open field collapses) · 2 h to code freeze

## Feature ladder
| Feature | Planned | Built (where) | Tested (how, result) | Shown in demo run | Mocked → disclosed in pitch? |
|---|---|---|---|---|---|
| Offline SQLite Cryptographic Ledger | Yes | `app/crypto_core.py`, `app/pds_counter.py` | 28 automated tests in `tests/test_pds_counter.py` and `tests/test_security_stress.py` [V] | Yes | Real (genuine SQLite3 WAL DB) |
| Statutory Entitlement Rules Engine | Yes | `app/pds_counter.py` (`calculate_entitlements`) | Tested across AAY (35 kg free), PHH (5 kg/member free), NPHH (0 kg central) [V] | Yes | Real (deterministic Python engine) |
| Two-Tap Dealer POS Dispense Flow | Yes | `app/pds_counter.py` (`dispense`) | Benchmark < 15ms execution; receipt formatted [V] | Yes | Real CLI counter |
| Tamper Audit & Rollback Detection | Yes | `app/pds_counter.py` (`verify-chain`) | Verified payload tamper, deletion, truncation, clock rollback [V] | Yes | Real (`verify-chain` CLI) |
| Split-Brain Duplicate Drawal Reconciliation | Yes | `app/pds_counter.py` (`reconcile`) | Multi-database reconciliation flags `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` [V] | Yes | Real (`reconcile` CLI) |
| Regional Audio Voice Simulator | Yes | `app/pds_counter.py` (`ivr-simulate`) | Kannada & Hindi scripts tested; zero PII confirmed [V] | Yes | Real (local audio synthesizer text) |
| Telecom Inbound Cloud IVR Trunk | Yes | Mocked | Simulated via CLI dialogue generator `[AI]` | Yes | Disclosed in pitch: mocked PRI line |
| Aadhaar Biometric Fingerprint Hardware | Cut | Mocked | Hardware biometric sensor out of 24h scope `[AI]` | No | Disclosed in pitch: mocked sensor |
| Physical ESC/POS Thermal Slip Printer | Cut | Mocked | Terminal ASCII receipt slip rendered `[AI]` | Yes | Disclosed in pitch: mocked thermal roll |

Labels: `[V]` = run and observed by automated tests · `[T]` = reported by team · `[AI]` = simulated interface.

## Demo walk
| # | Step | Expected | Actual | Pass? | Time |
|---|---|---|---|---|---|
| 1 | Kenchaiah pre-travel voice check (`ivr-simulate KA-BLR-PHH-1002 --lang kn`) | Spoken Kannada text: "November quota: 20 kg rice free, stock arrived today 8:15 AM." | Output matches statutory PMGKAY formula; Zero PII announced | PASS | 0:15 |
| 2 | Outage happens; Dealer 2-tap dispense (`dispense KA-BLR-PHH-1002`) | < 15ms SQLite transaction; prints formatted receipt with HMAC signature and hash | Receipt generated with sequence #1, valid signature, 20 kg free rice, ₹25 dal | PASS | 0:25 |
| 3 | Food Inspector runs integrity audit (`verify-chain`) | Inspects entire database; verifies hash chain and monotonic timestamps | Output: `✓ INTEGRITY VERIFIED: Chain verified successfully` | PASS | 0:15 |
| 4 | Red-Team Tamper Drill: Alter SQLite database via SQL `UPDATE` | `verify-chain` detects payload tampering immediately with exact row index | Output: `✗ TAMPER DETECTED: Tampered record payload at row 1: hash mismatch` | PASS | 0:20 |
| 5 | Split-brain offline duplicate check (`reconcile shop_a.db shop_b.db`) | Flags card drawing rations at two disconnected offline shops in same month | Output: `⚠ SPLIT-BRAIN DUPLICATE DRAWAL CONFLICTS DETECTED: Card KA-BLR-PHH-1002` | PASS | 0:15 |

## Failure drill
| Failure | What happened | Fallback worked? |
|---|---|---|
| Complete Network Outage | System operated 100% offline using local SQLite database and cached household cards | Yes: Zero external network queries required during transaction |
| Database Corruption / Restart | Process killed mid-session; database reopened on restart; WAL journal recovered cleanly | Yes: `test_persistence_across_restart` passes [V] |
| Clock Rollback Attempt | Dealer tries to backdate a transaction to an earlier timestamp | Yes: Blocked with `Clock rollback violation` error [V] |
| SD Card Storage Wear | Normal SQLite sync mode configured (`PRAGMA synchronous = NORMAL`) | Yes: High-throughput batch writes without storage thrashing |
| Backup Video Recorded | Pre-recorded 90-second terminal walkthrough MP4 recorded at Hour 17 | Yes: Verified playable offline |

## AI test cases
| # | Input | Expected | Actual | Pass? |
|---|---|---|---|---|
| 1 | AAY Household (3 members) | 35.0 kg free rice, ₹0 central cost, 1.0 kg dal @ ₹25 | 35.0 kg rice, ₹0 cost, 1 kg dal @ ₹25 | PASS |
| 2 | PHH Household (4 members) | 20.0 kg free rice (4 x 5kg), ₹680 DBT cash, 1.0 kg dal @ ₹25 | 20.0 kg rice, ₹0 cost, ₹680 DBT, 1 kg dal | PASS |
| 3 | PHH Single-member card | 5.0 kg free rice (1 x 5kg), 1.0 kg dal @ ₹25 | 5.0 kg rice, ₹0 cost, 1 kg dal | PASS |
| 4 | NPHH Non-priority card | 0.0 kg central rice (no PMGKAY entitlement) | 0.0 kg central rice, ₹0 cost | PASS |
| 5 | Kannada Voice Dialect | Pure regional number pronunciation ("ಇಪ್ಪತ್ತು ಕಿಲೋಗ್ರಾಂ — ಉಚಿತ") | Accurate spoken Kannada translation string | PASS |

## Demo Day Court
Decision: **REVISE (capped by 3 open collapses assumptions)** · NOT GUILTY 12 · GUILTY 0 · INSUFFICIENT EVIDENCE 0 · see `court/demo/verdict.md`

## Fix list (fits before code freeze)
| # | Fix | Demo impact | Hours | Owner | Do it? |
|---|---|---|---|---|---|
| 1 | Add colorized ANSI green/red highlights to `verify-chain` CLI | High visual impact for judges during live tamper drill | 0.5 | Frontend | Done |
| 2 | Format terminal thermal receipt slip with double-width headers | Improves readability on demo projector | 0.5 | Frontend | Done |
| 3 | Provide pre-scripted `demo_tamper.sh` shell runner for the live pitch | Eliminates risk of typos during 90-second live presentation | 0.5 | Lead | Done |

## What we'll say about mocks
| Line we'll say | Ladder row | True now? |
|---|---|---|
| "The offline SQLite cryptographic ledger and tamper verification CLI run genuinely on local hardware." | Row 1 & 4: Cryptographic Ledger & Audit CLI | True now [V] |
| "The statutory entitlement engine calculates official NFSA PMGKAY allocations deterministically." | Row 2: Entitlement Rules Engine | True now [V] |
| "The telecom telephony PRI trunk and physical thermal printer are simulated on the console for this demo." | Row 7 & 9: Telecom IVR & Thermal Printer | True now (clearly disclosed) |
| "Aadhaar biometric hardware is out of scope for our 24h prototype; offline transactions use card IDs." | Row 8: Aadhaar Biometric Scan | True now (clearly disclosed) |
