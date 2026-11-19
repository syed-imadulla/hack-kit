# DEMO — PDS Anna-Mitra (Demo Day Check 1)

> Summary: 5 of 5 demo steps passing · 5 of 5 AI test cases passing · Demo Day Court 1: **FAIL** (0 NG · 7 G · 0 IE, separate juror subagents) · fix 1 applied and tested afterwards · 2 h to code freeze

## Feature ladder
| Feature | Planned | Built (where) | Tested (how, result) | Shown in demo run | Mocked → disclosed in pitch? |
|---|---|---|---|---|---|
| Offline SQLite Cryptographic Ledger | Yes | `app/crypto_core.py`, `app/pds_counter.py` | 28 automated tests at Demo Day Court 1; 32 after fix 1 (`tests/test_pds_counter.py`, `tests/test_security_stress.py`) [V] | Yes | Real (genuine SQLite3 WAL DB) |
| Statutory Entitlement Rules Engine | Yes | `app/pds_counter.py` (`calculate_entitlements`) | Tested across AAY (35 kg free), PHH (5 kg/member free), NPHH (0 kg central) [V] | Yes | Real (deterministic Python engine) |
| Two-Tap Dealer POS Dispense Flow | Yes | `app/pds_counter.py` (`dispense`) | Benchmark < 15ms execution; receipt formatted [V] | Yes | Real CLI counter |
| Tamper Audit & Rollback Detection | Yes | `app/pds_counter.py` (`verify-chain`) | Verified payload tamper, deletion, truncation, clock rollback [V] | Yes | Real (`verify-chain` CLI) |
| Split-Brain Duplicate Drawal Reconciliation | Yes | `app/pds_counter.py` (`reconcile`) | Multi-database reconciliation flags `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` [V] | Yes | Real (`reconcile` CLI) |
| Regional Audio Voice Simulator | Yes | `app/pds_counter.py` (`ivr-simulate`) | Kannada & Hindi scripts tested; zero PII confirmed [V] | Yes (as printed text) | **Text only: no audio is produced.** Disclose as "spoken script, shown as text" |
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
| Backup Video Recorded | DEMO.md originally claimed an MP4 "verified playable", but no video file exists in this example [?] | Not verified: record it or drop the claim |

## AI test cases
| # | Input | Expected | Actual | Pass? |
|---|---|---|---|---|
| 1 | AAY Household (3 members) | 35.0 kg free rice, ₹0 central cost, 1.0 kg dal @ ₹25 | 35.0 kg rice, ₹0 cost, 1 kg dal @ ₹25 | PASS |
| 2 | PHH Household (4 members) | 20.0 kg free rice (4 x 5kg), ₹680 DBT cash, 1.0 kg dal @ ₹25 | 20.0 kg rice, ₹0 cost, ₹680 DBT, 1 kg dal | PASS |
| 3 | PHH Single-member card | 5.0 kg free rice (1 x 5kg), 1.0 kg dal @ ₹25 | 5.0 kg rice, ₹0 cost, 1 kg dal | PASS |
| 4 | NPHH Non-priority card | 0.0 kg central rice (no PMGKAY entitlement) | 0.0 kg central rice, ₹0 cost | PASS |
| 5 | Kannada Voice Dialect | Pure regional number pronunciation ("ಇಪ್ಪತ್ತು ಕಿಲೋಗ್ರಾಂ — ಉಚಿತ") | Accurate spoken Kannada translation string | PASS |

## Demo Day Court
Decision: **FAIL** · NOT GUILTY 0 · GUILTY 7 · INSUFFICIENT EVIDENCE 0 · quick 7 (civic seat: government clerk), separate juror subagents, `--open-collapses 3` · see `court/demo-1/verdict.md`

Why (all 7 jurors): the reviewer's own testing found the counter accepted 20 repeat dispenses of one card in a month and printed a 500 kg "100% FREE" receipt, while the disclosure said "the rules are real". 6 of 7 also flagged the open "collapses" assumptions and the voice line labelled "Real" though it prints text only.

> The earlier 12–0 NOT GUILTY "demo" trial is kept in `court-illustrative/demo/`. Its votes were written in one pass, not by separate jurors, and it missed both bugs.

## Fix list (fits before code freeze)
| # | Fix | Demo impact | Hours | Owner | Do it? |
|---|---|---|---|---|---|
| 1 | Add colorized ANSI green/red highlights to `verify-chain` CLI | High visual impact for judges during live tamper drill | 0.5 | Frontend | Done |
| 2 | Format terminal thermal receipt slip with double-width headers | Improves readability on demo projector | 0.5 | Frontend | Done |
| 3 | Provide pre-scripted `demo_tamper.sh` shell runner for the live pitch | Eliminates risk of typos during 90-second live presentation | 0.5 | Lead | Done |
| 4 | **From Demo Day Court 1:** block more than the monthly entitlement per card (repeat or oversized dispense) | Rules claim becomes true; demo can show the rejection live | 0.5 | Backend | **Done after the trial** [V]: 4 new tests; repeat and 500 kg dispenses now rejected |
| 5 | Relabel the voice line as text-only | Disclosure matches the ladder | 0.1 | Pitch | Done |
| 6 | Record the backup video or remove the claim | No unverifiable claim | 1 | Lead | Open |
| 7 | Test A1/A2 with 5–10 beneficiaries and dealers | Problem stops being only [T] | field | Team | Open (named by 6 of 7 jurors) |

A re-trial after fix 4 has not been run. Run `/hack:verify --demo` again before claiming it passes.

## What we'll say about mocks
| Line we'll say | Ladder row | True now? |
|---|---|---|
| "The offline SQLite cryptographic ledger and tamper verification CLI run genuinely on local hardware." | Row 1 & 4: Cryptographic Ledger & Audit CLI | True now [V] |
| "The statutory entitlement engine calculates official NFSA PMGKAY allocations deterministically." | Row 2: Entitlement Rules Engine | True now [V] |
| "A card can't draw more than its monthly entitlement at this shop." | Row 3: Two-tap dispense | yes: true since fix 4 [V]; it was false at Demo Day Court 1 |
| "The Kannada voice line is a spoken script, shown as text in this demo." | Row 6: Regional voice | yes [V] |
| "A backup video of the demo is ready." | Failure drill | no (no video file exists) |
| "The telecom telephony PRI trunk and physical thermal printer are simulated on the console for this demo." | Row 7 & 9: Telecom IVR & Thermal Printer | True now (clearly disclosed) |
| "Aadhaar biometric hardware is out of scope for our 24h prototype; offline transactions use card IDs." | Row 8: Aadhaar Biometric Scan | True now (clearly disclosed) |
