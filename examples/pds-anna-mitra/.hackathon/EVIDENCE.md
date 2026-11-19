# EVIDENCE — PDS Anna-Mitra Source & Evidence Register

> Summary: Comprehensive source register classifying statutory citations, competitor benchmarks, technical estimates, simulated jury feedback, and unverified field hypotheses.

All claims in this project are strictly labeled following the Hack Kit evidence schema:
- `[V]` **Verified:** Official statutory publications, gazette orders, or observed deterministic prototype test runs.
- `[T]` **Team Estimate:** Direct measurements, code benchmarks, or engineering estimates produced by the project team.
- `[AI]` **Simulated:** Perspectives produced by simulated Hack Court jurors or LLM analysis tools.
- `[?]` **Unverified:** Hypotheses, unconfirmed field assumptions, or missing data requiring empirical validation.

---

## 1. Statutory & Regulatory Framework [V]

| Citation ID | Source / Document | Statutory Provision / Factual Finding | Label |
|---|---|---|---|
| `STAT-NFSA-01` | National Food Security Act, 2013 (Gazette of India, Sep 10, 2013) | Section 3(1) & Schedule I: Antyodaya Anna Yojana (AAY) households entitled to 35 kg foodgrains per household per month. Priority Households (PHH) entitled to 5 kg foodgrains per person per month. | `[V]` |
| `STAT-NFSA-02` | NFSA 2013, Section 10(1) | Identification of eligible households: State Governments identify beneficiaries under AAY and PHH guidelines within central coverage ceilings. PHH eligibility is distinct from legacy BPL survey lists. | `[V]` |
| `STAT-PMGKAY-03`| Cabinet Committee on Economic Affairs (CCEA) Decision (Nov 2023 / Jan 2024 notification) | Pradhan Mantri Garib Kalyan Anna Yojana (PMGKAY) extended for 5 years: provides free foodgrains to AAY and PHH beneficiaries from 1 Jan 2024 through **31 December 2028**. | `[V]` |
| `STAT-NPHH-04`  | State Food & Civil Supplies Rules | Non-Priority Households (NPHH / APL) have zero central NFSA grain entitlement, but may access state-specific subsidized or non-subsidized commodities where enacted by state rules. | `[V]` |
| `STAT-STATE-05` | Karnataka 2026–27 Food & Civil Supplies Scheme Guidelines | State add-on benefits (e.g., additional rice allocation, DBT cash transfer in lieu of grains when central/open-market procurement is constrained, subsidized sugar/oil) are policy- and date-specific, subject to budget availability. | `[V]` |
| `STAT-EPOS-06`  | Central PDS ePOS Operational Guidelines (NIC & Dept of Food & Public Distribution) | State operational exception rules: Fair Price Shops are permitted an offline exception quota (typically capped at 5–10% of monthly allocation) for documented biometric or connectivity failures, requiring manual exception registers and post-facto audit. | `[V]` |
| `STAT-COMP-07`  | NIC Mera Ration App (Google Play Store Release & DFPD Documentation) | Official government citizen app: displays registered members, monthly NFSA quota, and FPS locator; requires Android 7.0+, mobile data, and literacy in English/Hindi/regional script. | `[V]` |
| `STAT-COMP-08`  | Annavitran Portal (`annavitran.nic.in`) & Karnataka Ahara (`ahara.kar.nic.in`) | Authoritative public web dashboards tracking monthly grain allocation and ePOS transactions at state, district, and FPS levels. | `[V]` |

---

## 2. Technical Measurements & Benchmarks [T]

| Metric ID | Component | Measured Value | Observation Method | Label |
|---|---|---|---|---|
| `TECH-SQL-01` | Local Entitlement Calculation | < 1.5 ms per lookup | Benchmark run across 1,000 synthetic card records in SQLite (`pds_counter.py`). | `[T]` |
| `TECH-HMAC-02`| HMAC-SHA256 Receipt Generation | < 0.8 ms per transaction | Benchmark on Python 3.10 standard library `hashlib` & `hmac`. | `[T]` |
| `TECH-CHAIN-03`| Hash-Chain Audit Verification | < 12 ms per 100 receipts | `verify_chain.py` full-ledger cryptographic scan. | `[T]` |
| `TECH-STOR-04`| SQLite Append Overhead | ~1.2 KB per signed receipt record | SQLite database size on disk with indexes. | `[T]` |
| `TECH-CONFL-05`| Multi-Device Conflict Detection | 100% duplicate card drawals flagged upon sync | `EXP-04` / `test_security_stress.py`: central reconciler flags concurrent offline drawals without ledger corruption. | `[T]` |
| `TECH-CLOCK-06`| Clock Manipulation Rejection | 100% non-monotonic timestamps or backdated sequence numbers blocked | `test_security_stress.py`: sequence number monotonicity strictly enforced (`seq = prev_seq + 1`). | `[T]` |
| `TECH-ANCH-07` | External Checkpoint Pinning | Full-ledger rewrite caught immediately | `test_security_stress.py`: hash mismatch between local root and pinned external hash flag detected. | `[T]` |
| `TECH-IVR-08`  | Telephony Inbound Cost Model | ~₹0.30–₹0.50 per 30-second call | Standard cloud telephony per-minute inbound PRI/SIP trunk commercial rates. | `[T]` |
| `TECH-TRUNC-09`| Ledger Truncation Detection | 100% truncated rows detected | `test_security_stress.py`: final ledger hash mismatch against pinned external anchor. | `[T]` |
| `TECH-TAMPR-10`| Record Modification Detection | 100% payload tampering caught | `test_security_stress.py`: recomputed SHA-256 hash breaks HMAC signature verification. | `[T]` |
| `TECH-KEYROT-11`| Key Ring Rotation Support | 100% multi-version key rings verified | `test_security_stress.py`: historical receipts verify against retired keys, new receipts verify against active key. | `[T]` |
| `TECH-TSROLL-12`| Independent Clock Rollback Detection | 100% backdated timestamps caught | `test_security_stress.py`: catches clock manipulation independently of sequence counter. | `[T]` |
| `TECH-FUTTS-13` | Future Timestamp Horizon Bounding | 100% dates beyond year 2030 blocked | `test_security_stress.py` & `test_pds_counter.py`: prevents clock poisoning DoS. | `[T]` |
| `TECH-INPUT-14` | Negative Commodity Input Rejection | 100% negative quantities rejected | `test_pds_counter.py`: enforces non-negative commodity amounts. | `[T]` |

---

## 3. Simulated Analysis & Jury Feedback [AI]

| Item ID | Source | Perspective / Finding | Label |
|---|---|---|---|
| `SIM-JURY-01` | Hack Court (Civic Sceptic Juror) | A smartphone app with truck GPS tracking will fail because transport contracts lack public APIs and target citizens lack connectivity. | `[AI]` |
| `SIM-JURY-02` | Hack Court (Municipal Front-Line Worker) | Overburdened Fair Price Shop dealers will reject tools requiring additional data entry during peak rush hours. | `[AI]` |
| `SIM-JURY-03` | Hack Court (Government Clerk Juror) | Offline digital receipts without central synchronization or physical dealer countersignatures have zero statutory evidentiary weight. | `[AI]` |
| `SIM-SPLIT-04`| Hack Court (Systems Engineer Juror) | Disconnected offline terminals cannot prevent split-brain double drawals in real time; conflict detection must occur at central sync. | `[AI]` |
| `SIM-COMP-05` | Hack Court (Already Exists Researcher) | Differentiating Anna-Mitra on keypad phone voice and offline exception logging clearly separates it from Mera Ration without duplicating core portals. | `[AI]` |
| `SIM-IMPRV-06`| Hack Court (Improvement Trial Jury) | 12 civic jurors commended 2-tap UI, zero-PII IVR, and decoupled NFSA rules; capped at REVISE due to 3 open collapses. | `[AI]` |

---

## 4. Unverified Hypotheses & Field Assumptions [?]

| Hypothesis ID | Assumption | Why It Is Unverified | Required Field Validation | Label |
|---|---|---|---|---|
| `HYP-TRUCK-01`| PDS grain supply trucks arrive at Fair Price Shops between the 1st and 10th of each calendar month. | Actual delivery schedules vary widely by taluk, road conditions, and FCI godown buffer levels. | `EXP-01` (Proposed): Audit logistics drop sheets across 20 Fair Price Shops in one taluk. | `[?]` |
| `HYP-DEALER-02`| Fair Price Shop dealers are motivated to use an offline digital assistant rather than fallback paper registers during ePOS outages. | Dealers may prefer paper registers or turning beneficiaries away to avoid perceived liability or device clutter. | `EXP-03` (Proposed): Interview 5 Fair Price Shop operators on ePOS downtime protocols. | `[?]` |
| `HYP-PHONE-03`| Over 60% of rural PDS beneficiaries in the target taluk have access to at least a basic keypad phone for SMS/missed-call checks. | Household phone access is unevenly distributed among elderly women and migrant labourers. | `EXP-02` (Proposed): Survey 50 beneficiaries at 3 Fair Price Shops. | `[?]` |
| `HYP-OUTAGE-04`| Cellular/server ePOS authentication failures exceed 15% of transaction attempts during peak morning hours. | Network uptime telemetry is not publicly released by state ePOS vendors. | Request ePOS server error logs or observe live counter sessions during peak week. | `[?]` |
