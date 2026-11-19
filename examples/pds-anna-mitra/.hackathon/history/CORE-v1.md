# PDS Anna-Mitra — Core Architecture v1 (Pre-Stress Baseline)

> **Historical Snapshot**: Archived prior to Phase 8/9 Stress Testing and Architectural Hardening.
> **Date**: 2026-11-03
> **Status**: Superseded by `ARCHITECTURE-V2.md`

---

## 1. Concept Summary (v1)

Anna-Mitra v1 was conceived in Phase 5 as a dual-channel transparency bridge:
1. **Beneficiary Channel**: Automated interactive phone line (IVR) + push SMS alerts to let rural ration card holders check monthly quota entitlements and verify shop grain arrivals before traveling.
2. **Dealer Channel**: Offline-capable SQLite transaction ledger with HMAC-SHA256 digital signatures on POS hardware, creating cryptographically signed local receipt codes for beneficiary audit.

---

## 2. Component Design (v1)

```
[Beneficiary Phone] ---> (PSTN/GSM) ---> [Twilio/Exotel IVR Gateway]
                                                    |
                                         (HTTPS Query / API)
                                                    v
                                      [Central Cloud Server]
                                                    ^
                                                    | (Sync when online)
[FPS ePOS Counter] ---> [Local SQLite DB + HMAC Log]
```

### 2.1 Beneficiary Flow (v1)
- Beneficiary dialed toll-free number.
- Prompt 1: Select language (1: Kannada, 2: Hindi, 3: English).
- Prompt 2: Enter 12-digit Ration Card number via DTMF keypad.
- Prompt 3: Enter 4-digit PIN for beneficiary privacy.
- Prompt 4: Main Menu (1: Current Quota, 2: Shop Stock Status, 3: Past Receipts, 4: Report Grievance).
- SMS sent with full transaction summary.

### 2.2 Dealer Counter Flow (v1)
- Multi-step form on POS tablet:
  1. Scan or enter Ration Card number.
  2. Select member identity from household list.
  3. Enter weighed quantities (Rice kg, Wheat kg, Sugar kg, Dal kg).
  4. Review summary screen.
  5. Click "Confirm & Sign".
  6. SQLite record created with `HMAC-SHA256(secret_key, receipt_data)`.
  7. Print paper slip with receipt hash.

### 2.3 Cryptographic Assumptions (v1)
- Assumed single static secret key per ePOS terminal (`SECRET_KEY`).
- Assumed sequential ID integrity prevents all tampering.
- Claimed offline transaction signing prevents fraudulent duplicate drawals across shops.

---

## 3. Vulnerabilities and Deficiencies Identified in Phase 8

1. **Beneficiary Usability & Inclusivity**:
   - 4-digit PIN required literacy and memory; failed for elderly beneficiaries and shared household phones.
   - Multi-level IVR hierarchy caused call abandonment on 2G/unstable cellular signals.
   - Push SMS delivery failed in deep rural areas with intermittent connectivity.
2. **Dealer Counter Friction**:
   - 5-step transaction flow took 75–90 seconds per customer; dealers refused workflow during peak morning rush.
3. **Cryptographic & Distributed Gaps**:
   - Static key lacked rotation mechanisms (`key_version`).
   - SQLite hash chain did not independently verify timestamp ordering against clock rollback.
   - Claim that offline signing "prevents duplicate drawals" was mathematically false in distributed split-brain topologies without live central locking.
4. **Data Freshness / Stock Claims**:
   - Stock arrival notifications relied on unverified depot dispatch data, risking false trips if dealer had not actually unloaded grain.
