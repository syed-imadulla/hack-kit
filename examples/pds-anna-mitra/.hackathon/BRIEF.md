# BRIEF — PDS Anna-Mitra

> Civic & Public Service AI Hackathon · Public Distribution & Food Security · Submission Brief

---

## 1. Executive Summary

- **Project Name**: PDS Anna-Mitra
- **One-Line Pitch**: A dual-channel civic integrity bridge for India's Public Distribution System: pre-travel voice quota transparency on basic keypad phones, and tamper-evident offline cryptographic transaction logging during network outages.
- **Motto**: Clear quotas before you walk; verified grain when the network drops.
- **Track**: Public Distribution & Food Security
- **Team**: Civic AI Systems (Lead, Backend, Voice, Frontend)
- **Status**: Working prototype verified by 28 automated tests; ready for Level 1 field pilot.

---

## 2. Problem Statement & Ground Evidence

Over 800 million citizens depend on the National Food Security Act (NFSA) for basic subsistence. Yet in rural India, beneficiaries face two chronic bottlenecks:
1. **Pre-travel Information Asymmetry**: Vulnerable families walk 3–8 km to remote Fair Price Shops only to find foodgrains have not arrived or the dealer is closed, losing ₹300–₹400 in daily agricultural wages.
2. **Counter Outage Paralysis**: ePOS cellular and server timeouts stall queues for hours. When dealers resort to manual overrides, lack of auditable records enables arbitrary quota cuts, phantom transactions, and zero paper trails.

---

## 3. The Anna-Mitra Dual-Channel Solution

Anna-Mitra introduces an inclusive dual-channel architecture that operates alongside existing government infrastructure without demanding smartphones or hardware replacement:

### Channel 1: Beneficiary Voice Transparency (Basic Phone)
- Toll-free inbound voice line accessible from any ₹800 feature phone over standard PSTN/GSM.
- Flattens interaction to a 2-step flow: citizen enters their 12-digit card number and immediately hears their monthly quota spoken slowly in regional languages (Kannada & Hindi).
- **Zero-PII Privacy Protection**: Suppresses family names, caste, and Aadhaar numbers over audio; announces only commodity kilogram amounts, protecting privacy on shared village handsets.
- **Stale Stock Warnings**: Explicitly states when grain stock was verified by the dealer, warning citizens if stock information is stale.

### Channel 2: Dealer Offline Cryptographic Ledger (ePOS Terminal)
- Lightweight SQLite3 database running with Write-Ahead Logging (WAL) and synchronous normal commits.
- **Two-Tap Counter Dispense**: Transaction completes locally in under 15 milliseconds, displaying calculated statutory quota and printing an auditable thermal slip.
- **Three-Layer Cryptographic Audit**:
  1. *SHA-256 Hash Chaining*: Every record links deterministically to the previous record's hash.
  2. *HMAC-SHA256 Signatures*: Signed using terminal hardware keys with multi-version key rotation support (`key_version`).
  3. *Independent Clock Rollback Checks*: Rejects backdated transaction insertions independently of sequence counters.
- **Daily External Checkpoint Pinning**: Daily closing hashes are published or pinned externally (via SMS/paper roll), defeating full-ledger rewrite attacks even under terminal key compromise.
- **Transparent Split-Brain Reconciliation**: Disconnected terminals cannot mathematically prevent concurrent double drawals in real time under the CAP theorem; Anna-Mitra's central sync engine detects and flags `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` for administrative recovery upon batch sync.

---

## 4. Policy & Statutory Decoupling

Anna-Mitra strictly decouples statutory central mandates from state budgetary additions:
- **Central NFSA PMGKAY (Statutory Baseline)**: Flat 35 kg foodgrain per household for Antyodaya Anna Yojana (AAY); 5 kg per member for Priority Households (PHH). Gazetted by the Government of India as 100% free through 31 December 2028.
- **State Add-ons (Karnataka 2026-27)**: Configurable add-on parameters specifying cash DBT transfers (₹170/member in lieu of extra rice) and subsidized essential commodities (1 kg Tur Dal at ₹25).
- Receipts prominently display `CENTRAL NFSA FREE` to legally prevent corrupt dealers from charging illegal handling fees for central grain.

---

## 5. Technical Deliverables & Test Verification

The codebase includes genuine, runnable, thoroughly tested software:
- `app/crypto_core.py`: Cryptographic hash-chaining, HMAC signing, key rotation, and multi-device conflict resolution.
- `app/pds_counter.py`: Complete CLI prototype with `init-db`, `quota`, `dispense`, `verify-chain`, `checkpoint`, `reconcile`, and `ivr-simulate` commands.
- `tests/test_security_stress.py`: 14 automated unit tests verifying payload tamper detection, row deletion breaks, truncation catches, full rewrite blocks, clock rollback detection, future timestamp horizon checks, and key rotation.
- `tests/test_pds_counter.py`: 14 integration tests verifying end-to-end transaction recording, persistence across restarts, quota accuracy, input validation (negative numbers, future timestamps, SQL injection), and split-brain conflict detection.
- **Total Test Suite**: 28 automated tests passing with 0 failures (`Ran 28 tests in 0.016s · OK`).

---

## 6. Honest Disclosures & Open Assumptions

In accordance with Hack Kit scientific integrity principles:
- **Mocked Components**: We explicitly disclose that the live telecom telephony PRI trunk, physical ESC/POS thermal printer hardware, and Aadhaar biometric fingerprint sensor are simulated via local console interfaces for this 24-hour hackathon.
- **Open Field Assumptions**: The three critical collapses assumptions (A1: stock arrival lag vs opening hours, A2: keypad phone voice adoption, A7: dealer willingness to operate offline workflow) remain tracked as open unvalidated hypotheses `[?]` awaiting physical pilot deployment in Magadi Taluk.
