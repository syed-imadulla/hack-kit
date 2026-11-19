# PDS Anna-Mitra — Architecture Decision Log (ADR)

> **Project**: PDS Anna-Mitra (NFSA Quota Transparency & Outage Resilience)  
> **Repository**: `examples/pds-anna-mitra/.hackathon/DECISION-LOG.md`  
> **Status**: Living Architectural Record (Phases 5 through 9)

---

## Decision Index

- [DEC-01: IVR PIN Removal in Favor of Zero-PII Voice Delivery](#dec-01-ivr-pin-removal-in-favor-of-zero-pii-voice-delivery)
- [DEC-02: Dealer Workflow Reduction to 2-Tap Dispense Pattern](#dec-02-dealer-workflow-reduction-to-2-tap-dispense-pattern)
- [DEC-03: Decoupling Central NFSA PMGKAY from State Add-on Configurator](#dec-03-decoupling-central-nfsa-pmgkay-from-state-add-on-configurator)
- [DEC-04: Split-Brain Duplicate Drawal: Conflict Detection Over Impossible Prevention](#dec-04-split-brain-duplicate-drawal-conflict-detection-over-impossible-prevention)
- [DEC-05: Rejection of "Immutable SQLite" in Favor of Tamper-Evident Checkpoint Pinning](#dec-05-rejection-of-immutable-sqlite-in-favor-of-tamper-evident-checkpoint-pinning)
- [DEC-06: Cryptographic Key Rotation with Versioned Key Identifiers](#dec-06-cryptographic-key-rotation-with-versioned-key-identifiers)

---

### DEC-01: IVR PIN Removal in Favor of Zero-PII Voice Delivery

- **Date**: 2026-11-03
- **Status**: Accepted (Replaces v1 PIN prompt)
- **Context**: In Phase 5 (v1), the IVR required beneficiaries to enter a 4-digit secret PIN before hearing their quota, intended to preserve privacy.
- **Problem**: In rural Karnataka field contexts (and general low-literacy environments), beneficiaries frequently forget PINs or share them with shop owners, relatives, or middlemen. Additionally, elderly citizens struggled with DTMF numeric entry on noisy cellular connections.
- **Options Considered**:
  1. *Retain 4-digit PIN*: Secure against casual eavesdropping; high failure rate for rural elderly.
  2. *OTP via SMS*: Requires two handsets or multitasking on basic feature phone; SMS delivery unreliable in rural dead zones.
  3. *Zero-PII Open Query (Selected)*: Caller inputs 12-digit Ration Card number (or presses # if calling from registered phone); system speaks **only** commodity quantities (`rice_kg: 20`, `dal_kg: 1`) without announcing personal names, caste, address, or Aadhaar numbers.
- **Decision**: Adopt Option 3. Since ration entitlement formulas are publicly determined by law and card category (AAY vs PHH member count), hearing the kilogram entitlement discloses no private biometric or personal data.
- **Consequences**: Drastically cuts call duration by 60%, prevents dropped calls, and allows illiterate beneficiaries to have a trusted neighbor dial on their behalf without exposing sensitive personal identifiers.

---

### DEC-02: Dealer Workflow Reduction to 2-Tap Dispense Pattern

- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: Stress test scenario `SC-DLR-01` revealed that during the first week of every month, an FPS dealer serves 150–300 beneficiaries per day. Morning queues stretch 50+ meters.
- **Problem**: The v1 dealer interface required 5 distinct form screens: card entry, member selection, weighing inputs for 4 separate commodities, review confirmation, and signing. Total interaction took 75–90 seconds per customer. Dealers stated they would boycott the system.
- **Decision**: Implement a **Two-Tap Dispense Flow**:
  - Tap 1: Select Card / Scan barcode (loads cached entitlement).
  - Tap 2: Tap green `[Dispense Standard Entitlement & Print]` button.
  - Generates receipt, hashes payload, signs HMAC, updates SQLite in under 15 milliseconds.
- **Consequences**: Reduces counter transaction time to < 15 seconds. For the 5–10% of households taking partial rations, a secondary `[Custom Quantity]` button is available, but the happy path default minimizes dealer friction.

---

### DEC-03: Decoupling Central NFSA PMGKAY from State Add-on Configurator

- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: Hackathon projects frequently blend central and state food schemes into a single hardcoded number (e.g. claiming "All citizens get 10 kg rice free in Karnataka").
- **Problem**: Under the National Food Security Act (NFSA) 2013, the Government of India provides PMGKAY foodgrains 100% free through 31 December 2028 (35 kg/AAY household, 5 kg/PHH member). State additions (such as Karnataka's Anna Bhagya DBT cash transfers of ₹170/person or supplemental pulses/oil) are state budgetary policies subject to change, procurement availability, and executive orders. Blending them distorts statutory legal rights and misinforms citizens.
- **Decision**: Isolate the entitlement calculator into two decoupled sub-engines:
  1. `calculate_central_nfsa_quota()`: Hardcoded statutory rules (AAY 35 kg, PHH 5 kg/member, free).
  2. `calculate_state_addon_quota(config_json, effective_date)`: Dynamic configuration specifying cash DBT vs grain add-ons and subsidized commodities.
- **Consequences**: Clean legal compliance, clear receipt breakdowns, and easily portable to other Indian states (e.g., Tamil Nadu, Odisha, Uttar Pradesh) simply by swapping the state JSON configuration.

---

### DEC-04: Split-Brain Duplicate Drawal: Conflict Detection Over Impossible Prevention

- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: Reviewers asked whether Anna-Mitra's offline cryptography prevents a beneficiary from collecting ration at Shop A (offline) and immediately traveling to Shop B (offline) to collect a second time under One Nation One Ration Card (ONORC).
- **Problem**: Under the CAP theorem, two partition-isolated distributed nodes without network connectivity cannot achieve mutual consensus or locking. Claiming offline cryptography "prevents" double drawals is mathematically false and academically dishonest.
- **Decision**: Explicitly acknowledge that real-time offline double drawal prevention is impossible across disconnected shops. Implement **asynchronous conflict detection upon central reconciliation**:
  - Central sync engine flags `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` whenever two receipts with the same `card_id` and overlapping month/year are synced from different terminal IDs.
  - Both signed receipts are preserved in the central audit ledger for administrative recovery and disciplinary action.
- **Consequences**: Maintains technical and academic honesty. Positions Anna-Mitra as an auditable accountability system rather than making false claims of distributed magic.

---

### DEC-05: Rejection of "Immutable SQLite" in Favor of Tamper-Evident Checkpoint Pinning

- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: Early documentation described SQLite database as "immutable".
- **Problem**: SQLite is an ordinary file format; any entity with root or terminal file access can rewrite SQLite tables, re-execute hashing, and overwrite records if they control the database file.
- **Decision**: Strike all references to "immutable database". Adopt the rigorous definition:
  - **Tamper-Evident Local Hash Chain**: Internal record modifications break `prev_hash` pointers.
  - **HMAC Signatures**: Modification without terminal secret key fails signature check.
  - **External Daily Checkpoint Pinning**: The terminal's closing receipt hash $H_n$ is pinned daily to a central cloud server, local bank branch, or municipal office via SMS/USSD/paper log. A dealer attempting a full-ledger rewrite is caught because their synthesized historical chain does not match the previously pinned checkpoint hash.
- **Consequences**: Accurate, legally defensible security claims that hold up under rigorous technical audit.

---

### DEC-06: Cryptographic Key Rotation with Versioned Key Identifiers

- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: In production operations, symmetric HMAC keys must be rotated periodically (e.g. annually or after terminal servicing).
- **Problem**: If a static key is rotated, historical receipts signed with older keys would fail verification unless the system supports multi-version key rings.
- **Decision**: Include `key_version` in the receipt schema and hash calculation. The verification function accepts a dictionary `keys_map = {"v1": key1, "v2": key2}` and verifies each record against its designated key.
- **Consequences**: Seamless key lifecycle management with zero invalidation of historic audit trails.
