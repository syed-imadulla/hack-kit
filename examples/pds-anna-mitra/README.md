# PDS Anna-Mitra (Fair Price Shop Assistance & Outage-Resilient Verification)

> **Hack Kit v1.2 Real-World Showcase** · 24-hour Civic Hackathon Demonstration

This directory contains a complete, end-to-end, educational worked example built with [Hack Kit](https://github.com/imadulla/hack-kit). It demonstrates how a team moves from an ordinary, flawed hackathon concept (*"a smartphone app with GPS truck tracking and queue webcams"*) to a defensible, evidence-backed public-service solution through Hack Kit's 14 phases.

---

## 1. Domain & Statutory Framework

### 1.1 Central NFSA (2013) vs. State-Specific Schemes
Under the National Food Security Act (NFSA), 2013, Central statutory entitlements are clearly distinct from State schemes:

- **Central NFSA Entitlements (Extended under PMGKAY through 31 December 2028):**
  - **Antyodaya Anna Yojana (AAY):** Fixed at **35 kg foodgrains per household per month**, provided free of cost.
  - **Priority Households (PHH):** Fixed at **5 kg foodgrains per person per month**, provided free of cost.
  - *Distinction:* State governments identify eligible households under Section 10 of the NFSA based on state-specific criteria. Being Below Poverty Line (BPL) under an older survey is distinct from being an identified PHH beneficiary on the state NFSA ration card list.
- **State-Specific Add-Ons (Configurable, Date-Specific):**
  - States provide additional welfare benefits (e.g., additional rice/grains, fortified oil, sugar, pulses, or DBT cash-transfers in lieu of grains during procurement shortages).
  - These benefits vary across budget years, procurement availability, and cabinet orders (e.g., Karnataka's 2026–27 policy environment). They are modeled as configurable parameters, never hardcoded as permanent central statutory guarantees.
- **Non-Priority Households (NPHH):**
  - NPHH cardholders do not receive Central NFSA AAY/PHH subsidies, but individual state schemes may provide specific subsidized or unsubsidized commodities under separate state rules.

---

## 2. Technical Scope & Explicit Disclaimers

> [!IMPORTANT]
> **Legal & Administrative Disclaimer:**
> This repository contains an educational prototype and simulated hackathon artifacts. It is **not** an official government portal, and its outputs do **not** confer statutory entitlement or legal authorization. In real-world PDS operations, grain disbursement authorization rests exclusively with the relevant State Food & Civil Supplies Directorate and certified ePOS server infrastructure.

> [!NOTE]
> **Cryptographic Assumptions & Boundaries:**
> - The local ledger uses **HMAC-SHA256 signatures** and **SHA-256 hash chaining** (`prev_hash`).
> - This mechanism provides **tamper-evidence under stated key and external checkpoint assumptions**: any unauthorized modification of past records invalidates the hash chain and HMAC signatures.
> - It does **not** independently guarantee immutability, prevent a full-ledger rewrite by an attacker who controls the signing key (without external checkpoint pinning), or magically make SQLite append-only.
> - An offline receipt signed by this tool represents **cryptographic proof of local execution attempt**, not statutory government verification.

---

## 3. Directory Layout

- `.hackathon/`: Complete Hack Kit state and phase artifacts (Phases 1–14).
  - `STATE.md`: Real-time project tracking, phase progress, decisions log.
  - `EVIDENCE.md`: Source register classifying all data as `[V]`, `[T]`, `[AI]`, or `[?]`.
  - `STATEMENTS.md`, `PICK.md`, `USERS.md`, `IDEAS.md`, `ASSUMPTIONS.md`, `COMPETE.md`, `STRESS.md`, `IMPROVE.md`, `CORE.md`, `PLAN.md`, `DEMO.md`, `PITCH.md`, `BRIEF.md`, `RETRO.md`.
  - `court/`: Simulated Hack Court trials and Demo Day Court ballots.
- `app/`: Working Python prototype (`pds_counter.py`, `crypto_core.py`).
- `tests/`: Automated test suite testing quota math, offline logging, truncation, tampering detection, key rotation, non-monotonic clocks, and crash recovery (`test_pds_counter.py`, `test_security_stress.py`).

---

## 4. Quick Start & CLI Usage

### Running the Test Suite
```bash
python3 -m unittest discover -s examples/pds-anna-mitra/tests
# Ran 28 tests in 0.016s · OK
```

### Initializing the Offline Terminal Database
```bash
python3 examples/pds-anna-mitra/app/pds_counter.py init-db
```

### Calculating Statutory Entitlements (Zero PII)
```bash
python3 examples/pds-anna-mitra/app/pds_counter.py quota KA-BLR-PHH-1002
```

### Simulating Regional Audio Dialogue (Kannada & Hindi)
```bash
python3 examples/pds-anna-mitra/app/pds_counter.py ivr-simulate KA-BLR-PHH-1002 --lang kn
```

### Executing Fast Two-Tap Counter Dispense (<15ms)
```bash
python3 examples/pds-anna-mitra/app/pds_counter.py dispense KA-BLR-PHH-1002
```

### Auditing Database Ledger Integrity
```bash
python3 examples/pds-anna-mitra/app/pds_counter.py verify-chain
```

### Reconciling Multi-Terminal Logs & Flagging Conflicts
```bash
python3 examples/pds-anna-mitra/app/pds_counter.py reconcile shop_a.db shop_b.db
```
