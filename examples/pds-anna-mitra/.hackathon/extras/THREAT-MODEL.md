# THREAT-MODEL — PDS Anna-Mitra Security & Threat Analysis

> Summary: Comprehensive threat modeling identifying threat actors, protected assets, attack surfaces, single points of failure (SPOFs), and residual risks.

---

## 1. Threat Actors & Motivations

| Threat Actor | Motivation | Capabilities | Likely Attack Vectors |
|---|---|---|---|
| **Dishonest Fair Price Shop Dealer** | Financial gain via grain diversion to private flour mills; avoiding audit stock deductions. | Physical access to ePOS terminal; local OS filesystem access; authority over shop queues. | Modifying offline grain weights; deleting transaction rows; backdating offline transactions; claiming phantom cardholders. |
| **Opportunistic Beneficiary** | Obtaining duplicate rations or maximizing monthly grain drawals beyond statutory limits. | Physical ration card; access to multiple shops in border areas; family members with duplicate cards. | Attempting concurrent offline redemptions at two disconnected shops (split-brain exploit). |
| **Rogue Technician / Hardware Maintenance Staff** | Sabotaging audit data; extracting device secrets for dealer bribes. | Root/ADB access to terminal hardware; ability to copy SQLite files and extract configuration keys. | Extracting HMAC secret keys; flashing rogue firmware; attempting full-ledger regeneration. |
| **Telecom / Network Attacker** | Disrupting public services; eavesdropping on telephony lines. | Network interception on cellular PRI/SIP trunks; SMS spoofing. | Man-in-the-middle on sync uploads; SMS notification spoofing. |

---

## 2. Protected Assets

1. **Foodgrain Integrity:** Preventing unauthorized or unverified grain disbursements (diversion prevention).
2. **Citizen Entitlement Rights:** Ensuring vulnerable cardholders receive their exact statutory quota (PMGKAY 35 kg AAY / 5 kg PHH) without unauthorized dealer cuts.
3. **Audit History Integrity:** Maintaining an unforgeable, tamper-evident record of local offline transactions.
4. **Beneficiary Privacy:** Protecting personal identification numbers (Aadhaar, phone numbers) from plaintext exposure.
5. **State Audit Credibility:** Ensuring food inspectors can trust local digital records over unverified paper registers.

---

## 3. Attack Surfaces

```
[Citizen Keypad Phone] ──(PSTN / 2G Voice)──▶ [Cloud Telephony IVR Gateway]
                                                      │ (Public REST API)
                                                      ▼
[Fair Price Shop Counter Terminal] ────────▶ [Central State Sync Gateway]
  ├── (Local Touchscreen UI)                   │ (Database Ingestion)
  ├── (Local SQLite File on Flash Storage)     ▼
  └── (Local HMAC Secret Key in Storage)    [Central Audit Reconciliation DB]
```

1. **Local SQLite File (`pds_offline.db`):** Plain file stored on device flash. Directly vulnerable to raw SQL edits, truncation, or row deletion if an attacker has filesystem access.
2. **Local Cryptographic Key (`secret.key`):** Stored in terminal flash memory. If exported, allows generating valid HMAC signatures on arbitrary payloads.
3. **Inbound Telephony Voice API:** Vulnerable to automated dialer scraping or brute-force Ration Card entitlement lookups.
4. **Sync Ingestion Endpoint:** Vulnerable to replay attacks, duplicate batch submissions, or payload injection during network restoration.

---

## 4. Single Points of Failure (SPOFs)

| SPOF ID | Component | Failure Consequence | Architectural Mitigation |
|---|---|---|---|
| `SPOF-01` | **Local HMAC Key Custody on Terminal** | If the secret key is extracted from device storage, an attacker could sign forged individual records. | **Mitigation:** Hash chaining + external checkpoint pinning. A forged record cannot match past external anchors printed on paper or sent to state servers `[T]`. |
| `SPOF-02` | **Wholesale Truck Unload Status Diligence** | If the dealer or godown driver fails to confirm physical unloading, Channel 1 reports outdated "Stock En Route" status. | **Mitigation:** Dual-party confirmation: Wholesale depot driver triggers an automated dispatch SMS; dealer confirms unloading via 1-tap counter scan `[AI]`. |
| `SPOF-03` | **Central Reconciliation Ingestion Script** | If central sync crashes during large morning batch uploads, reconciliation queues back up. | **Mitigation:** Idempotent `INSERT OR IGNORE` batch processing with SQLite WAL mode; zero data loss on crash `[T]`. |

---

## 5. Residual Risks & Stated Boundaries

1. **Offline Split-Brain Reality:** Disconnected local devices cannot communicate in real time. Concurrent redemptions of the same card across two disconnected shops *will* succeed locally and can only be caught upon central sync `[T]`.
2. **Dealer Coercion / Physical Weighing Fraud:** Software cannot verify that the dealer physically poured exactly 20.0 kg of rice into the beneficiary's cloth sack. Physical weighing fraud requires vigilance committee monitoring `[AI]`.
3. **No Statutory Authority:** Local cryptographic signatures are evidence of local software execution integrity; they do *not* constitute statutory government transaction clearance `[V]`.
