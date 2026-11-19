# PDS Anna-Mitra — Architectural Improvements & Simplifications (Phase 9)

> **Context**: Generated in response to Phase 8 Stress Testing (`STRESS-TEST.md`, `THREAT-MODEL.md`, `FAILURE-MATRIX.md`).
> **Goal**: Eliminate fragile assumptions, reduce operator friction, harden cryptographic defenses, and remove non-essential complexity.

---

## 1. Summary of Changes (v1 -> v2)

| Subsystem | v1 Baseline (Fragile) | v2 Hardened (Production-Grade Prototype) | Justification & Stress Scenario |
|:---|:---|:---|:---|
| **Beneficiary IVR Flow** | 4-step nested menu with 4-digit PIN, English default option | 2-step flattened flow: Auto-detect language or 1-tap select, immediate slow spoken quota readback | SC-BEN-01, SC-BEN-04: Eliminates cognitive load, prevents call drops on 2G |
| **Shared Phone Privacy** | Spoke full beneficiary name, address, and Aadhaar on speaker | Speaks *only* commodity quantities (`rice_kg`, `wheat_kg`); suppresses PII | SC-BEN-02: Protects vulnerable women and elderly using neighbor/shared village phones |
| **Stock Fallback Handling** | Guaranteed truck arrival alerts based on depot dispatch | Clear freshness timestamp: if stock not unloaded, states "Stock not confirmed by dealer — last known update X days ago" | SC-BEN-05: Prevents wasted trips caused by phantom stock |
| **Dealer Counter Workflow** | 5-step form taking 75–90s per customer | 2-tap "Standard Dispense" workflow taking < 15s per customer | SC-DLR-01: Aligns with dealer incentive to clear 200+ morning queues |
| **Cryptographic Keys** | Single static symmetric key (`SECRET_KEY`) | Versioned key ring (`key_version`, e.g., `v1`, `v2`) with rotation support | SC-SEC-04: Key compromise mitigation without ledger invalidation |
| **Ledger Integrity** | Hash chain verifying only sequence number + hash | Three independent layers: (1) Hash chain, (2) HMAC signatures, (3) Monotonic timestamp validation | SC-SEC-01, SC-SEC-06: Catches clock rollback even if sequence numbers are sequential |
| **Checkpoints** | Local device hash comparison only | External checkpoint pinning: daily root hash published/pinned off-device | SC-SEC-05: Defeats full-ledger rewrite attacks |
| **Split-Brain Double Drawals** | Claimed offline cryptography prevents duplicate drawals | Explicit `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` reconciliation record flagged upon central sync | SC-DIST-01: Mathematically honest acknowledgment of offline CAP theorem limits |
| **Entitlement Scope** | Blended central + state into one hardcoded number | Strictly decoupled: Central NFSA (PMGKAY free through 2028) vs Configurable State add-on (Karnataka 2026–27) | Policy Compliance: Prevents illegal misrepresentation of statutory central entitlements |

---

## 2. Detailed Subsystem Improvements

### 2.1 Beneficiary IVR Simplification

```
[Incoming Call from Beneficiary]
             |
             v
 [Step 1: Language Select / Auto-detect]
 "Press 1 for Kannada / ಕನ್ನಡಕ್ಕೆ 1 ಒತ್ತಿರಿ, Press 2 for Hindi / हिंदी के लिए 2 दबाएं"
             |
             v
 [Step 2: Enter 12-digit Ration Card Number]
 (If dialed from registered mobile, press # to confirm current number)
             |
             v
 [Instant Spoken Response — No Menu Navigation]
 "Ration Card 1002.
  November Quota:
  Rice: Twenty Kilograms. Free.
  Wheat: Zero Kilograms.
  State Dal: One Kilogram.
  Shop Status: Stock arrived today morning at 8:15 AM.
  Press 1 to hear again. Thank you."
```

#### Privacy Safeguard on Shared Phones
- The system never pronounces the family head's name, caste, address, or Aadhaar numbers over the phone.
- Only the entitlement amounts for that card number are read out.
- Prevents embarrassment or targeted exploitation in rural community settings where multiple households use a single shopkeeper's or neighbor's handset.

#### Stale Stock Warning
- If the central sync shows the Fair Price Shop has not reported stock confirmation within 72 hours of expected cycle:
  > *"Shop stock has not been verified by the dealer for November. Please call your local panchayat or FPS dealer before traveling."*

---

### 2.2 Dealer Counter UI/UX: The "Two-Tap" Guarantee

Field failure scenario `SC-DLR-01` showed that any workflow adding more than 20 seconds per transaction causes dealers to bypass the digital terminal and revert to paper records.

#### Improved 2-Tap Flow:
1. **Tap 1: Select Card / Scan QR**:
   - Terminal loads offline household profile from local SQLite cache.
   - Screen displays calculated statutory quota:
     `KA-BLR-PHH-1002 (4 members) -> 20.0 kg Rice [PMGKAY Free] + 1.0 kg Dal [State Configurable]`.
2. **Tap 2: Dispense Standard & Sign**:
   - Green button: `[Dispense Standard Entitlement & Print]`.
   - SQLite transaction executes atomically within 12 milliseconds:
     - Fetches current `prev_hash`.
     - Increments sequence number `seq`.
     - Validates local system clock against last record timestamp.
     - Computes SHA-256 receipt hash.
     - Signs receipt with active HMAC key (`key_version`).
     - Appends to `transactions` table.
     - Outputs receipt payload to thermal printer / digital ledger.
3. **Exception Flow (Non-standard / Partial)**:
   - Only if beneficiary lacks money for paid state add-ons or takes partial grain does dealer tap `[Custom Amount]`. 90%+ transactions follow standard 2-tap path.

---

### 2.3 Cryptographic Hardening & Integrity Model

We formally decouple the security architecture into three distinct layers:

```
+-------------------------------------------------------------------------+
| Layer 3: External Checkpoint Pinning (Defeats Full Ledger Rewrite)      |
| Daily/Hourly Root Hash pinned to Central Server or Block Storage       |
+-------------------------------------------------------------------------+
                                    ^
                                    | (Validates tail hash)
+-------------------------------------------------------------------------+
| Layer 2: Authenticated Symmetric Signatures (HMAC-SHA256)               |
| Proves possession of hardware terminal secret key (supports rotation)   |
+-------------------------------------------------------------------------+
                                    ^
                                    | (Signs cryptographic digest)
+-------------------------------------------------------------------------+
| Layer 1: Cryptographic Hash Chain (SHA-256 + Sequence + Monotonic Time)  |
| Guarantees tamper-evidence: prev_hash links + strict timestamp order     |
+-------------------------------------------------------------------------+
```

1. **Independent Timestamp Rollback Detection**:
   - In v1, sequence numbers were checked, but an attacker with database access could backdate an entry while maintaining sequential IDs.
   - In v2, `verify_chain()` explicitly verifies:
     `assert current_timestamp >= previous_timestamp`.
     Any clock manipulation or backdated record injection raises an immediate `Clock rollback detected` violation.
2. **Key Rotation (`key_version`)**:
   - Each receipt records the signing key version used (e.g. `key_version: "v1"`).
   - In v2, verification accepts a dictionary `keys_map = {"v1": "...", "v2": "..."}`.
   - When a key is retired or rotated due to periodic policy, old historical records remain cryptographically verifiable against their respective version keys.
3. **Split-Brain Conflict Resolution**:
   - Under disconnected offline operations, Terminal A (Shop 1) and Terminal B (Shop 2) cannot communicate in real time.
   - If a beneficiary draws their quota at Shop 1 (Offline) and subsequently travels to Shop 2 (Offline) and draws again, both terminals produce locally valid signed receipts.
   - Anna-Mitra v2 abandons the impossible claim of real-time offline duplicate prevention. Instead, the central sync engine (`reconcile_batch_logs()`) flags this condition:
     `status: "CONFLICT_DUPLICATE_OFFLINE_DRAWAL"`.
     Both transactions are recorded in the central audit ledger for administrative review and recovery, while alerting the taluk food inspector.

---

### 2.4 State Add-on Configurator

- Central PMGKAY foodgrain (free through 31 Dec 2028: 35 kg for AAY; 5 kg/member for PHH) is hardcoded as statutory baseline.
- State-specific additions (e.g. Karnataka Anna Bhagya additional rice or cash DBT transfer, subsidized pulses/oil) are isolated in a dynamic configuration schema:
  ```json
  {
    "state_code": "KA",
    "effective_date": "2026-11-01",
    "scheme_name": "Karnataka Anna Bhagya & Essential Add-ons 2026-27",
    "rules": {
      "PHH": {
        "dbt_cash_per_member_inr": 170.0,
        "additional_grain_kg": 0.0,
        "subsidized_dal_kg": 1.0,
        "subsidized_dal_price_inr": 25.0
      },
      "AAY": {
        "dbt_cash_per_household_inr": 0.0,
        "additional_grain_kg": 0.0,
        "subsidized_dal_kg": 1.0,
        "subsidized_dal_price_inr": 25.0
      }
    }
  }
  ```
- This configuration is versioned and verifiable independently, ensuring zero distortion of central statutory mandates.
