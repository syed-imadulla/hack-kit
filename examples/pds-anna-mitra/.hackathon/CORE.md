# CORE — PDS Anna-Mitra

> LOCKED: 2026-11-19 21:20 IST · Version v2 (Showcase)

> Summary: A dual-channel civic integrity bridge for PDS: pre-travel voice quota transparency on basic keypad phones, and tamper-evident offline cryptographic transaction logging during network outages.

Version: v2

## 1. Name and motto
**PDS Anna-Mitra.** Clear quotas before you walk; verified grain when the network drops.

## 2. Positioning line
A dual-channel civic integrity bridge for India's Public Distribution System (PDS). It operates alongside existing Fair Price Shop (FPS) infrastructure: basic phone voice guidance for rural beneficiaries, and an offline tamper-evident cryptographic receipt ledger for dealers when ePOS networks fail.

## 3. Problem
Over 800 million citizens rely on the National Food Security Act (NFSA), yet rural beneficiaries frequently walk 3–8 km to Fair Price Shops only to find foodgrains have not arrived, or stand in 50-meter queues stalled by ePOS server outages. In the chaos of manual overrides, vulnerable families lose daily wages and suffer arbitrary quota deductions with zero auditable proof.

## 4. Persona story — Kenchaiah & Ratnamma (Magadi Taluk, Karnataka, PHH Card, 4 members, basic phone)
| Before | After (Anna-Mitra v2) |
|---|---|
| Walks 4 km to Fair Price Shop at 7:00 AM; loses ₹350 daily agricultural wage | Dials free number from basic keypad phone at 6:30 AM |
| Finds grain truck has not arrived yet; told by dealer to "come back Friday" | Hears exact audio in Kannada: "November quota: Rice 20 kg free. Shop stock arrived today at 8:15 AM." |
| Terminal offline; dealer demands ₹100 cash for "handling" or gives only 15 kg rice | Stands at counter; dealer taps 2 buttons in 12 seconds; receives printed slip with HMAC receipt hash |
| Has no proof of short-distribution when complaining to village panchayat | Holds signed physical receipt with verifiable sequence number and hash |

## 5. End-to-end journey
| # | Who acts | Channel | System does | Human decides |
|---|---|---|---|---|
| 1 | Beneficiary | Basic Phone (Call) | Auto-detects language; prompts for 12-digit card number | Beneficiary dials |
| 2 | Rules engine | Audio IVR (Kannada/Hindi) | Speaks statutory PMGKAY quota (20 kg free) + state dal (1 kg, ₹25) + stock arrival time | — |
| 3 | Beneficiary | In-person at FPS | Presents card at counter during confirmed stock window | Beneficiary travels |
| 4 | Dealer | ePOS / Counter CLI | Tap 1: Selects card number; displays cached household entitlement | Dealer verifies identity |
| 5 | Dealer | ePOS / Counter CLI | Tap 2: Taps `[Dispense Standard Entitlement & Print]` | Dealer initiates |
| 6 | Crypto Engine | Local SQLite DB | Signs HMAC-SHA256, checks clock monotonicity, links hash chain, updates local ledger in <15ms | — |
| 7 | Hardware | Thermal Printer | Prints physical receipt with card ID, dispensed kg, and cryptographic receipt code | Beneficiary takes grain |
| 8 | Central Sync | Cloud Gateway (upon sync) | Verifies hash chain, validates signatures against key ring, flags duplicate drawals | Food Inspector reviews |

## 6. Who does what
| Role | Does | Never has to |
|---|---|---|
| Beneficiary | Dials toll-free number from basic phone, enters card number, listens in Kannada/Hindi | Download a smartphone app, remember a 4-digit PIN, or travel blindly |
| Dealer | Taps 2 buttons (<15 seconds per transaction), hands paper slip with hash | Manually calculate complex quotas or maintain duplicate paper registers |
| Food Inspector | Runs automated `verify-chain` CLI on terminal database; reviews reconciliation logs | Manually cross-check hundreds of illegible paper counterfoils |

## 7. USPs (Non-Negotiables)
1. **Zero Smartphone Gatekeeping**: Accessible to any citizen owning a basic ₹800 feature phone via standard voice telephony.
2. **Zero-PII Voice Privacy**: Never announces beneficiary names, caste, or Aadhaar on audio loudspeaker; reads out only commodity kilogram amounts.
3. **Two-Tap Dealer Counter Speed**: Standard dispense transaction completes in under 15 seconds, preventing queue bottlenecks.
4. **Three-Layer Cryptographic Audit**: SHA-256 hash-chaining + HMAC-SHA256 signatures + independent clock rollback detection.
5. **Full-Ledger Rewrite Resistance**: Daily external checkpoint pinning defeats retroactive ledger rewriting even under terminal key compromise.
6. **Strict Central vs State Decoupling**: Central NFSA PMGKAY free foodgrains (through 31 Dec 2028) strictly separated from dynamic state add-ons (Karnataka 2026-27).
7. **Transparent Failure Disclosures**: Disconnected terminals cannot prevent split-brain double drawals in real time; resolved via `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` upon central sync.

## 8. AI vs rules vs humans
| Step | AI / Automated Model | Fixed Deterministic Rules | Human Decides | If System Fails |
|---|---|---|---|---|
| Quota Lookup | Audio synthesis (TTS / recorded prompts) | Statutory NFSA PMGKAY formula (5 kg/PHH, 35 kg/AAY) | Beneficiary decides to visit shop | SMS fallback or physical notice |
| Outage Transaction | Hash calculation & HMAC signature | Sequential counter & monotonic clock verification | Dealer verifies citizen physical card | Emergency offline quota (10% ceiling [AI]) |
| Sync Reconciliation | Anomaly scoring on transaction intervals | Conflict flag on duplicate card redemption | Food Inspector audits duplicate drawal | Manual taluk administrative review |

## 9. Inclusion
- No phone in household → neighbor's phone used safely (Zero PII ensures no personal data leaked).
- Low literacy / non-English → spoken Kannada & Hindi audio prompts with slow repetition.
- Visually impaired → spoken voice feedback for quota; tactile embossed thermal paper slip.

## 10. Fit with existing systems (4-Tier Coexistence)
- **Level 0 (Standalone)**: Independent toll-free phone line + standalone offline counter CLI (zero government IT approval required).
- **Level 1 (Read-Only API)**: Central quota lookup pulls from public State Food Department web portal.
- **Level 2 (ePOS Companion)**: Anna-Mitra runs as background APK / daemon on existing certified Android ePOS terminals.
- **Level 3 (Statutory Integration)**: Full NIC/Annavitran backend integration with automated offline voucher clearance.

## 11. Privacy & Legal Boundaries
- No biometric Aadhaar numbers or scans are stored in the local offline database.
- Local cryptographic receipts prove terminal audit trail; they do **not** represent official statutory government clearance.
- Offline double drawals across disconnected shops are recorded and flagged for administrative recovery upon central sync.

## 12. Out of scope
- Real-time physical biometric scanning (Aadhaar iris/fingerprint match).
- Live GPS tracking of transport contractor trucks.
- Automatic banking DBT direct cash disbursement.
- Statutory policy changes to national food security quotas.

## 13. Open field assumptions (Methodological Realism)
| Assumption | Label | Kill test | Status |
|---|---|---|---|
| Wasted trips are primarily caused by stock delivery lag rather than shop opening hours | `[?]` | EXP-01: Taluk drop-off correlation | testing (proposed) |
| Beneficiaries with basic keypad phones will dial an IVR number before traveling | `[?]` | EXP-02: 15-household voice trial | testing (proposed) |
| Fair Price Shop dealers will accept a 2-tap offline logging workflow during outages | `[?]` | EXP-03: Dealer speed simulation | testing (proposed) |
