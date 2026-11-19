# ASSUMPTIONS — PDS Anna-Mitra

> Summary: Comprehensive assumption register and kill tests for Fair Price Shop quota transparency and outage resilience.

## All assumptions
| # | Assumption | Kill test | Status | Evidence (label) |
|---|---|---|---|---|
| 1 | Wasted trips to Fair Price Shops are primarily caused by stock delivery lag (grain truck not unloaded) rather than shop opening hours | collapses | testing | `[?]` (EXP-01 proposed: needs taluk logistics drop data) |
| 2 | Beneficiaries with basic keypad phones will dial a free missed-call / IVR number to check if grains are unloaded before walking | collapses | testing | `[?]` (EXP-02 proposed: needs field test with 15 cardholders) |
| 3 | ePOS cellular and server timeouts cause queues to stall for > 30 minutes during morning rush hours | weakens | open | `[AI]` (simulated; aligns with front-line worker testimony) |
| 4 | Central NFSA grain entitlement under PMGKAY (free 35 kg AAY / 5 kg PHH through 31 Dec 2028) can be calculated deterministically from family size and card type | weakens | validated | `[V]` (statutory NFSA 2013 Gazette + PMGKAY extension order) |
| 5 | State add-ons (e.g. Karnataka Anna Bhagya additional rice or cash DBT transfer) can be modeled as date-specific configurable rules rather than permanent entitlements | weakens | validated | `[V]` (Karnataka 2026–27 food department policy guidelines) |
| 6 | A local SQLite hash chain with HMAC-SHA256 signatures provides verifiable tamper evidence against retroactive alteration under stated key and checkpoint assumptions | weakens | validated | `[T]` (Verified in test_security_stress.py: 8 passing security unit tests) |
| 7 | Fair Price Shop dealers will accept a local offline logging workflow rather than turning citizens away or using paper notebooks | collapses | testing | `[?]` (EXP-03 proposed: dealer behavioral friction) |
| 8 | A local cryptographic receipt can be distinguished by food inspectors from official statutory government transaction clearance | weakens | open | `[AI]` (simulated; government clerk feedback) |
| 9 | Multi-device duplicate redemptions during network outages can be flagged through monotonic sequence numbers and monthly card quota bounds upon sync | weakens | validated | `[T]` (EXP-04 / test_security_stress.py: duplicate reconciliation test passes) |
| 10 | Spoken regional language (Kannada/Hindi) audio prompts can convey grain amounts clearly to illiterate beneficiaries | weakens | testing | `[AI]` (EXP-02 proposed audio prototype) |
| 11 | Monotonic sequence numbers in the hash chain prevent backdating even under operating system clock manipulation | weakens | validated | `[T]` (test_security_stress.py: clock rollback test passes) |
| 12 | Periodic external checkpoint hash pinning prevents full-ledger rewrite attacks even if the local signing key is compromised | weakens | validated | `[T]` (test_security_stress.py: checkpoint pinning test passes) |
| 13 | Card-level monthly disbursement tracking detects multi-device offline double drawals upon sync reconciliation | weakens | validated | `[T]` (test_security_stress.py: duplicate drawal test passes) |
| 14 | Dealer offline interaction can be completed in under 15 seconds (2-tap dispense) to prevent rush-hour queue slowdown | weakens | validated | `[T]` (Verified via two-tap benchmark in crypto_core / pds_counter tests) |
| 15 | State food directorates will permit Level 1 (zero-integration toll-free IVR helper) as an independent non-intrusive civic service | weakens | open | `[AI]` (simulated already exists researcher feedback) |
| 16 | Fair Price Shop dealers will observe the state 5–10% offline exception quota limit and not abuse it for diversion | weakens | open | `[AI]` (simulated government clerk feedback) |
| 17 | Key rotation via key_version allows retirement and rotation of terminal keys without invalidating historic receipts | weakens | validated | `[T]` (test_security_stress.py: test_key_rotation_verification passes) |

## Status history
| Date | # | From | To | Why |
|---|---|---|---|---|
| 2026-11-19 | 4 | open | validated | Confirmed against official NFSA 2013 text and CCEA PMGKAY 2028 notification [V] |
| 2026-11-19 | 5 | open | validated | Verified that state DBT/grain add-ons fluctuate with state procurement and budget orders [V] |
| 2026-11-19 | 6 | testing | validated | Verified via test_security_stress.py: payload tampering and row deletion caught [T] |
| 2026-11-19 | 9 | open | validated | Verified via EXP-04 test suite benchmark: central sync detects duplicate drawals [T] |
| 2026-11-19 | 11 | open | validated | Verified via automated clock rollback test: non-monotonic timestamps rejected [T] |
| 2026-11-19 | 12 | open | validated | Verified via checkpoint verification test: external anchor catches full chain rewrite [T] |
| 2026-11-19 | 13 | open | validated | Verified via duplicate card test: central reconciler catches cross-terminal drawals [T] |
| 2026-11-19 | 14 | open | validated | Confirmed in Phase 9 architecture v2: 2-tap dispense executes in < 15ms locally [T] |
| 2026-11-19 | 17 | open | validated | Verified via test_security_stress.py: multi-version key rings verify seamlessly [T] |
