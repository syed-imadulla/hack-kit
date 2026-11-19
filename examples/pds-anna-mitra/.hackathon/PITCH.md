# PITCH — PDS Anna-Mitra

> Summary: A dual-channel civic integrity bridge for India's Public Distribution System: pre-travel voice quota checks on basic keypad phones, and tamper-evident offline cryptographic transaction logging during network outages · 7 slides · 3-min pitch.

## One-liners
- **One-line pitch:** A dual-channel civic integrity bridge for PDS: pre-travel voice quota transparency on basic keypad phones, and tamper-evident offline cryptographic transaction logging during network outages.
- **Opening line:** "Over 800 million citizens depend on the National Food Security Act, but in rural India, families walk miles only to find empty shops or stalled ePOS servers."
- **Motto:** Clear quotas before you walk; verified grain when the network drops.

## Deck outline (stay within the slide limit)

| # | Headline (full sentence) | 3–5 short items | Visual | Source line |
|---|---|---|---|---|
| 1 | PDS Anna-Mitra: Food security transparency that works before you walk and when the network drops | Track: Public Distribution & Food Security · Team: Civic AI Systems · Motto | Rural ration queue at sunrise | `STATE.md` |
| 2 | Millions walk blindly to Fair Price Shops only to face empty stock or stalled ePOS queues | 3–8 km wasted round-trips · 50m morning queues · ePOS server timeouts · Zero paper trail during outages | Split screen: long queue vs basic phone | `USERS.md`, `EVIDENCE.md` [1] |
| 3 | Anna-Mitra bridges transparency through a dual-channel architecture without requiring smartphones | Channel 1: Toll-free regional voice line (Zero PII) · Channel 2: Two-tap offline POS cryptographic ledger (<15s) | Two-channel architecture diagram | `ARCHITECTURE-V2.md` |
| 4 | Offline transactions are secured by hash-chaining, HMAC signatures, and daily checkpoint pinning | SHA-256 chain links · HMAC signing with key rotation · Monotonic clock rollback checks · External checkpoint pinning | Cryptographic 3-layer security diagram | `app/crypto_core.py` [V] |
| 5 | Kenchaiah gets verified grain in 12 seconds instead of losing a ₹350 daily wage | Pre-travel Kannada voice call · Two-tap counter dispense · Clear paper slip separating free central grain from state dal | Persona before/after journey table | `CORE.md` |
| 6 | A genuine working prototype verified by 19 automated tests and transparent disclosures | Genuine SQLite3 WAL database · 19 passing tests · Disclosed mocks: telecom PRI trunk and biometric sensor | Live terminal split-screen + test output | `DEMO.md` [V] |
| 7 | Zero new hardware, sustainable economics, and a clear 4-tier rollout pathway | Level 0 standalone today → Level 3 statutory integration · Pennies per voice call · Clear quotas before you walk | Phased roadmap & impact metrics | `CORE.md`, `STATEMENTS.md` |

## Form answers
| Question | Word limit | Answer |
|---|---|---|
| What problem does your project solve? | 100 words | Over 800 million Indians rely on NFSA foodgrains, yet rural beneficiaries frequently walk miles only to find grain trucks haven't arrived, or wait hours in queues stalled by ePOS server timeouts. During outages, manual distribution creates quota cuts and zero auditable records. |
| Describe your technical solution and innovation | 150 words | Anna-Mitra operates a dual-channel bridge: (1) A toll-free voice dialogue line that reads statutory NFSA PMGKAY allocations and verified stock arrivals in spoken Kannada and Hindi with zero PII. (2) A lightweight offline cryptographic engine on ePOS terminals that executes two-tap transactions in under 15ms using SHA-256 hash-chaining, HMAC signatures with key rotation, monotonic clock validation, and daily checkpoint pinning to prevent ledger tampering. |
| What is the social and economic impact? | 100 words | Prevents lost daily agricultural wages (₹300–₹400/day) for millions of vulnerable households, eliminates arbitrary short-distribution of grain, and provides food inspectors with automated mathematical proof of offline shop records without requiring expensive proprietary hardware. |

## Judge Q&A
| Question | Answer (2–3 lines) |
|---|---|
| "Why not build a smartphone app with GPS tracking of grain trucks?" | Over 70% [AI] of rural BPL cardholders do not own smartphones, and transport contractors lack public telemetry APIs. A smartphone app gatekeeps the very people who need transparency most. Anna-Mitra works on any ₹800 keypad phone. |
| "How do you prevent a beneficiary from drawing rations at two disconnected shops offline?" | Under the CAP theorem, two disconnected offline devices cannot prevent concurrent drawals in real time. We are mathematically honest: Anna-Mitra's central sync engine detects and flags `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` for administrative recovery upon upload. |
| "Can a corrupt dealer rewrite the SQLite database and re-sign the records?" | Local hash-chaining detects edits and deletions. If a rogue dealer steals the terminal key and attempts a full-ledger rewrite, they are caught because daily closing hashes are pinned externally to the central cloud or district dashboard. |
| "Is your local offline receipt an official government clearance?" | No. We explicitly distinguish local technical integrity from statutory government clearance. Our receipt is an auditable evidentiary artifact for food inspectors, operating within state 5–10% [V] emergency offline exception quotas. |

## Drill 1 (from `/hack:pitch --drill`)
| # | Judge | Question | Answer (summary) | Clarity | Evidence | Honesty | Length | Stronger answer |
|---|---|---|---|---|---|---|---|---|
| 1 | Civic Tech Sceptic | How do you know beneficiaries will call an IVR instead of just walking? | We honestly track this as an open assumption `[?]` (A2) requiring field trials; but our 2-step Zero-PII design removes menu confusion. | 9/10 | 8/10 | 10/10 | 25s | "We don't claim field proof yet. That's why EXP-02 is designed as a 15-household pilot before state rollout." |
| 2 | Systems Architect | What happens when local ePOS clocks drift without network time? | System enforces strict monotonicity: $T_i \ge T_{i-1}$, and flags clock drift deltas exceeding 1 hour against external checkpoints. | 9/10 | 9/10 | 10/10 | 20s | Solid; highlighted in ADR DEC-05. |
| 3 | Government Bureaucrat | Does this violate central PMGKAY free foodgrain guidelines? | Absolutely not. We strictly decoupled central PMGKAY (100% free [V] through 2028) from state add-ons; receipts print 'CENTRAL FREE' explicitly. | 10/10 | 10/10 | 10/10 | 20s | Exact match with Gazette and CCEA notification. |
| 4 | Security Reviewer | What prevents key theft and backdating? | Key rotation (`key_version`) isolates compromise, and independent monotonic timestamp validation catches backdated records even if sequence IDs match. | 9/10 | 10/10 | 10/10 | 22s | Verified by unit tests in `test_security_stress.py`. |

### Pitch vs product
| Claim | Backed by | Status |
|---|---|---|
| "Runs genuinely offline in SQLite with < 15ms latency" | `app/pds_counter.py` benchmark | Verified `[V]` |
| "Detects record tampering, row deletion, and clock rollback" | `tests/test_security_stress.py` (10 tests) | Verified `[V]` |
| "Decouples Central NFSA PMGKAY free foodgrain from State add-ons" | Statutory Gazette & `calculate_entitlements()` | Verified `[V]` |
| "Flags split-brain duplicate card disbursements upon sync" | `reconcile_batch_logs()` in `crypto_core.py` | Verified `[V]` |
| "Telephony PRI trunk and hardware biometric sensor are simulated" | Feature ladder disclosures in `DEMO.md` | Disclosed `[AI]` |

### Rehearse again
1. Keep the 90-second demo walk strictly under 1:30. Let the terminal speak for itself during the tamper drill.
2. Emphasize the CAP theorem honesty when explaining offline duplicate drawal conflict detection.
3. Pronounce the Kannada dialogue clearly during Slide 5: *"ಅಕ್ಕಿ: ಇಪ್ಪತ್ತು ಕಿಲೋಗ್ರಾಂ — ಉಚಿತ"*.
