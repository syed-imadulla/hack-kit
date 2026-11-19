# SUMMARY — PDS Anna-Mitra

> Clear quotas before you walk; verified grain when the network drops.

| | |
|---|---|
| Event / track | Civic & Public Service AI Hackathon · Public Distribution & Food Security |
| Team | Civic AI Systems (Lead, Backend, Voice, Frontend) |
| Latest decision | REVISE (capped by 3 open collapses assumptions) · NG 12 · G 0 · IE 0 · Rubric estimate: 84/100 |
| Idea | CORE v2 · Dual-channel civic integrity bridge (Zero-PII Voice + Offline POS Cryptographic Ledger) |

## Problem
Over 800 million citizens rely on the National Food Security Act (NFSA), yet rural beneficiaries frequently walk 3–8 km to Fair Price Shops only to find foodgrains have not arrived, or stand in 50-meter queues stalled by ePOS server outages. In the chaos of manual overrides, vulnerable families lose daily wages and suffer arbitrary quota deductions with zero auditable proof.

## Solution
A dual-channel civic integrity bridge operating alongside existing Fair Price Shop infrastructure:
1. **Beneficiary Channel**: A toll-free voice dialogue line that reads statutory NFSA PMGKAY allocations and stock arrival status in spoken Kannada and Hindi with zero PII, accessible from any basic ₹800 keypad phone.
2. **Dealer Channel**: A lightweight offline cryptographic engine on ePOS terminals executing two-tap transactions in under 15 milliseconds using SHA-256 hash-chaining, HMAC-SHA256 signatures with key rotation, monotonic clock validation, and daily checkpoint pinning to detect ledger tampering.

## Journey
1. Kenchaiah dials toll-free number from basic phone at 6:30 AM before leaving home.
2. Hears exact quota in Kannada: "November quota: 20 kg rice free under PMGKAY, 1 kg dal at ₹25, stock arrived today 8:15 AM."
3. Travels to shop; dealer terminal is offline due to cellular timeout.
4. Dealer selects card, taps `[Dispense Standard Entitlement]` in 12 milliseconds.
5. Terminal prints tamper-evident offline voucher with HMAC signature and sequence hash.
6. Food Inspector runs `verify-chain` to mathematically verify ledger integrity, while central sync flags any multi-shop duplicate drawals.

## What's built vs mocked
| Built | Mocked |
|---|---|
| Genuine SQLite3 WAL database, deterministic NFSA PMGKAY rules engine, Two-tap counter CLI (`pds_counter.py`), SHA-256 hash chaining, HMAC-SHA256 signing with key rotation, monotonic clock rollback checks, `verify-chain` audit CLI, multi-terminal split-brain conflict reconciler, regional Kannada & Hindi dialogue generator | Inbound telecom PRI/SIP trunk line, physical ESC/POS thermal slip printer hardware, Aadhaar biometric fingerprint sensor hardware |

## Top ratings
| Item | /10 | Why |
|---|---|---|
| Problem is real | 9 | Affects millions of BPL households; verified NFSA statutory baseline [V] |
| Safe | 9 | Zero PII announced; zero biometric data stored; human dealer confirms identity [V] |
| Buildable and demo-able | 10 | 28 automated unit & integration tests passing with 0 failures [V] |
| Differentiated | 8 | Operates on basic keypad phones and disconnected ePOS hardware where smartphone apps fail [V] |

## Open field assumptions (collapses)
| Assumption | Label | Status |
|---|---|---|
| Wasted trips are primarily caused by stock delivery lag rather than shop opening hours | `[?]` | testing (EXP-01 proposed) |
| Beneficiaries with basic keypad phones will dial an IVR number before traveling | `[?]` | testing (EXP-02 proposed) |
| Fair Price Shop dealers will accept a 2-tap offline logging workflow during outages | `[?]` | testing (EXP-03 proposed) |

## Next steps
1. Run 15-household voice dialer field trial in Magadi Taluk (EXP-02).
2. Deploy Level 1 non-intrusive companion pilot with 5 Fair Price Shops.
3. Integrate closing hash checkpoints into Taluk Tahsildar daily SMS dashboard.
