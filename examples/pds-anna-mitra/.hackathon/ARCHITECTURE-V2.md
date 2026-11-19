# PDS Anna-Mitra — System Architecture Specification v2 (Hardened)

> **Document Version**: 2.0  
> **Status**: Approved for Core Lock & Phase Planning  
> **Target Platform**: Raspberry Pi / Linux-based ePOS Terminal + Central Cloud Sync Gateway  
> **Author**: Civic Systems Engineering Team

---

## 1. System Topology & Dual-Channel Overview

Anna-Mitra bridges statutory foodgrain transparency between vulnerable rural beneficiaries and Fair Price Shop (FPS) dealers operating under frequent network outages.

```
  +-----------------------------------------------------------------------------------+
  |                            BENEFICIARY CHANNEL (VOICE)                            |
  |                                                                                   |
  |  [Basic Feature Phone]                                                            |
  |          |                                                                        |
  |          | (PSTN / GSM Call to Toll-Free Number)                                  |
  |          v                                                                        |
  |  [Telecom IVR Gateway] (Simulated Exotel/Twilio API / Local Audio Simulator)      |
  |          |                                                                        |
  |          | (HTTPS Query: card_id)                                                 |
  |          v                                                                        |
  |  [Central Entitlement Service]                                                    |
  |    - Computes Central NFSA (PMGKAY free baseline)                                 |
  |    - Computes Karnataka 2026-27 State Add-on Rules (DBT / Subsidized Dal)         |
  |    - Looks up latest FPS Stock Delivery Confirmation Timestamp                    |
  |    - Returns JSON audio response payload (Kannada / Hindi audio generation)        |
  +-----------------------------------------------------------------------------------+

  +-----------------------------------------------------------------------------------+
  |                         DEALER COUNTER CHANNEL (OFFLINE POS)                      |
  |                                                                                   |
  |  [ePOS Terminal / POS Counter CLI]                                                |
  |    - Local SQLite 3 Database (WAL mode, fsync=ON)                                 |
  |    - Offline Household Cache (`cards.json` / `households` table)                  |
  |    - Two-Tap Dispense Interface (< 15 seconds per transaction)                     |
  |    - Cryptographic Engine (`crypto_core.py`):                                     |
  |        * SHA-256 Hash Chaining                                                    |
  |        * HMAC-SHA256 Transaction Signatures                                       |
  |        * Key Rotation Registry (`keys_map`, `key_version`)                        |
  |        * Independent Timestamp Monotonicity Enforcement                           |
  |    - Outputs Thermal Receipt Slip / Verification Code                             |
  |          |                                                                        |
  |          | (Periodic Batch Sync when connectivity returns: 4G/WiFi/USB-OTG)       |
  |          v                                                                        |
  |  [Central Reconciliation Service]                                                 |
  |    - Verifies Hash Chain against Registered Device Genesis Hash                   |
  |    - Verifies Signatures against Key Ring                                         |
  |    - Compares Tail Hash against Stored Checkpoints                                |
  |    - Detects Cross-Device Duplicate Drawals (`CONFLICT_DUPLICATE_OFFLINE_DRAWAL`) |
  |    - Updates Beneficiary Quota Ledger                                             |
  +-----------------------------------------------------------------------------------+
```

---

## 2. Data Models & Schemas

### 2.1 Household Profile (`beneficiary_cards`)
```sql
CREATE TABLE beneficiary_cards (
    card_id VARCHAR(32) PRIMARY KEY,     -- e.g., "KA-BLR-PHH-1002"
    scheme_type VARCHAR(8) NOT NULL,     -- "AAY" or "PHH" (Identified by State)
    member_count INTEGER NOT NULL,       -- Family members registered on card
    assigned_fps_id VARCHAR(32) NOT NULL,-- e.g., "FPS-42-BANGALORE-RURAL"
    registered_mobile VARCHAR(16),       -- Optional, for CLI auto-match
    last_sync_date TEXT NOT NULL
);
```

### 2.2 Offline Transaction Record (`offline_transactions`)
```sql
CREATE TABLE offline_transactions (
    seq INTEGER PRIMARY KEY,             -- Strictly increasing counter: 1, 2, 3...
    prev_hash VARCHAR(64) NOT NULL,      -- SHA-256 hash of previous transaction
    timestamp TEXT NOT NULL,             -- ISO 8601 UTC (must be >= previous record)
    card_id VARCHAR(32) NOT NULL,        -- Beneficiary card number
    items_json TEXT NOT NULL,            -- Sorted JSON string of dispensed items
    dealer_id VARCHAR(32) NOT NULL,      -- Unique terminal/shop identifier
    hash VARCHAR(64) NOT NULL,           -- SHA-256(prev_hash + seq + ts + card + items + dealer)
    signature VARCHAR(64) NOT NULL,      -- HMAC-SHA256(key_ring[key_version], hash)
    key_version VARCHAR(16) NOT NULL,    -- Key identifier, e.g., "v1", "v2"
    sync_status VARCHAR(16) DEFAULT 'PENDING'
);
```

### 2.3 Receipt Hash Calculation Specification
The receipt hash `H_i` is computed deterministically:
$$\text{Payload} = \text{prev\_hash} \parallel \text{seq} \parallel \text{timestamp} \parallel \text{card\_id} \parallel \text{canonical\_items\_json} \parallel \text{dealer\_id}$$
$$H_i = \text{SHA-256}(\text{Payload})$$
$$\text{Signature}_i = \text{HMAC-SHA256}(K_{\text{ver}}, H_i)$$

Where:
- $\parallel$ denotes string concatenation with pipe delimiter `|`.
- $\text{canonical\_items\_json}$ is serialized with keys sorted lexicographically and no redundant whitespace.
- $K_{\text{ver}}$ is the terminal HMAC key designated by `key_version`.

---

## 3. Entitlement Calculation Rules Engine

### 3.1 Central NFSA PMGKAY (Statutory Baseline)
Under the National Food Security Act (NFSA) 2013 and PMGKAY extension (gazetted through 31 December 2028):
- **Antyodaya Anna Yojana (AAY)**: Flat **35 kg foodgrain per household per month**. Distributed free of cost (\$0 / ₹0).
- **Priority Households (PHH)**: **5 kg foodgrain per individual member per month**. Distributed free of cost (\$0 / ₹0).
- Grain proportion in Karnataka typically dispenses 100% Rice, or Rice/Wheat split as per central allocation order.

### 3.2 State Add-on Configurator (Karnataka Context 2026–27)
- Identified by State Food & Civil Supplies Department.
- Modeled as dynamic configuration parameter:
  - Rice Top-up: 0 kg (or 5 kg if procurement allows).
  - DBT Cash Transfer: ₹170 per member per month in lieu of 5 kg additional rice (when grain procurement unavailable).
  - Subsidized Essential Commodities: 1 kg Tur Dal at ₹25/kg (subsidized rate).
- **Hard Rule**: The system strictly distinguishes NFSA PMGKAY free foodgrain from state add-ons on the screen and print slip. Dealers cannot charge money for central grain under any circumstance.

---

## 4. IVR Script Specification & Dialog Flow

### 4.1 Dialog State Table

| State ID | Audio Prompt (Kannada / Hindi / English) | Valid User Input | Next State | Error / Timeout Action |
|:---|:---|:---|:---|:---|
| `LANG_SELECT` | "ಕನ್ನಡಕ್ಕಾಗಿ 1 ಒತ್ತಿರಿ. हिंदी के लिए 2 दबाएँ." | `1` (Kannada), `2` (Hindi) | `CARD_INPUT` | Default to Kannada after 5s |
| `CARD_INPUT` | "ನಿಮ್ಮ 12 ಅಂಕಿಯ ರೇಷನ್ ಕಾರ್ಡ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ." / "अपना 12 अंकों का राशन कार्ड नंबर दर्ज करें." | 12 numeric digits | `QUOTA_PLAYOUT` | Repeat prompt (max 2 retries), then hang up |
| `QUOTA_PLAYOUT` | Spoken reading of entitlement (see 4.2) | `1` (Repeat), `9` (Stock status) | `REPEAT` / `STOCK_INFO` | Hang up gracefully after 10s |

### 4.2 Spoken Audio Output Template (Example)
> *"ರೇಷನ್ ಕಾರ್ಡ್ KA-BLR-PHH-1002. ನವೆಂಬರ್ ತಿಂಗಳ ಕೋಟಾ:*  
> *ಅಕ್ಕಿ: ಇಪ್ಪತ್ತು ಕಿಲೋಗ್ರಾಂ — ಉಚಿತ.*  
> *ಗೋಧಿ: ಸೊನ್ನೆ ಕಿಲೋಗ್ರಾಂ.*  
> *ತೊಗರಿ ಬೇಳೆ: ಒಂದು ಕಿಲೋಗ್ರಾಂ, ಬೆಲೆ ಇಪ್ಪತ್ತೈದು ರೂಪಾಯಿ.*  
> *ನ್ಯಾಯಬೆಲೆ ಅಂಗಡಿ ಮಾಹಿತಿ: ನವೆಂಬರ್ 3 ರಂದು ಬೆಳಿಗ್ಗೆ 8:15 ಕ್ಕೆ ಆಹಾರ ಧಾನ್ಯ ತಲುಪಿದೆ.*  
> *ಮತ್ತೊಮ್ಮೆ ಕೇಳಲು 1 ಒತ್ತಿರಿ. ಧನ್ಯವಾದಗಳು."*

*English Translation for Audit:*
> *"Ration card KA-BLR-PHH-1002. November quota:*  
> *Rice: Twenty kilograms — Free.*  
> *Wheat: Zero kilograms.*  
> *Toor Dal: One kilogram, price twenty-five rupees.*  
> *Fair price shop info: Foodgrain arrived on November 3 at 8:15 AM.*  
> *Press 1 to hear again. Thank you."*

---

## 5. Security & Cryptographic Guarantees

### 5.1 What Anna-Mitra Cryptography Guarantees
1. **Tamper-Evidence**: Any unauthorized modification, insertion, or deletion of local SQLite records breaks the SHA-256 `prev_hash` chain and invalidates the HMAC signature.
2. **Clock Rollback Detection**: Backdated transactions inserted with forged older timestamps are rejected during validation because timestamps must satisfy $T_i \ge T_{i-1}$.
3. **Key Rotation Lifecycle**: Historic receipts remain auditable after terminal secret key rotation using `key_version` lookup.
4. **Full-Ledger Rewrite Resistance**: By publishing periodic checkpoint hashes (e.g., daily closing hash $H_n$) to an offsite ledger or municipal dashboard, a rogue dealer cannot rewrite an entire historical database without mismatching the external checkpoint.

### 5.2 What Anna-Mitra Cryptography CANNOT Guarantee (Honest Disclosures)
1. **No Real-Time Distributed Double Drawal Prevention**: Disconnected offline POS terminals cannot lock records across multiple geographical locations simultaneously.
2. **No Physical Biometric Proof**: Local digital receipts prove a terminal transaction took place; they do not mathematically prove that the actual human beneficiary stood at the counter (requires biometric ePOS hardware or OTP).
3. **No Automatic Central Enforcement**: Offline receipts are evidentiary audit artifacts, not statutory government reconciliation clearances.

---

## 6. Implementation Status Matrix

| Component | Architecture Role | Hackathon Implementation Mode | Verification Method |
|:---|:---|:---|:---|
| `crypto_core.py` | Hash chain, HMAC sign, key rotate, verify, reconcile | **Fully Functional Python 3 Module** | Unit & stress tests (10 passing tests) |
| `pds_counter.py` | Dealer POS 2-tap CLI & receipt generator | **Fully Functional CLI Prototype** | Integration & simulated counter run |
| SQLite Ledger | Local offline transaction database | **Genuine Working SQLite3 Database** | ACID write, restart, tamper recovery tests |
| Entitlement Engine | NFSA PMGKAY + State add-on calculation | **Deterministic Python Rules Engine** | Unit tests against statutory cases |
| IVR Audio Service | Beneficiary voice quota readout | **Simulated IVR Synthesizer / Audio CLI** | Dialogue script test & Kannada text generator |
| Central Sync Gateway | Multi-device reconciliation & duplicate detection | **Functional Python Conflict Resolver** | Multi-device split-brain test |
| Biometric Scanner | Aadhaar fingerprint / iris match | **Mocked / Out of Scope for 24h Hackathon** | Explicitly labeled as simulated interface |
| Physical Thermal Printer | Hardware paper slip printing | **Console Receipt Formatter** | Formatted text receipt output |
