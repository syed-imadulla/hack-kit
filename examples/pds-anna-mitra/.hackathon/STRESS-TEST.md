# STRESS-TEST — PDS Anna-Mitra Red-Team Scenarios & Vulnerability Assessment

> Summary: 22 concrete stress-test failure and attack scenarios across 5 operational domains, distinguishing executable technical tests [T] from simulated operational risks [AI].

---

## 1. Domain 1: Beneficiary Access & Telephony Failures

### Scenario 1.1: Shared Household Phone / Migrant Husband Custody
- **Attack / Failure:** The mobile number seeded on the ration card belongs to the migrant husband working 300 km away in Bengaluru. The mother attending the FPS has no personal phone.
- **Severity:** High · **Likelihood:** High `[?]` · **Detectability:** Easy
- **Impact:** If notifications are sent strictly as SMS push to the registered number, the person standing at the shop remains completely unnotified.
- **Mitigation (`[T]` Architectural):** Channel 1 is strictly designed as an **on-demand inbound pull IVR**: the beneficiary can dial the toll-free number from any borrowed village phone or neighbour's handset, enter the 12-digit Ration Card number, and hear their specific quota. Zero dependency on phone SIM ownership.
- **Residual Risk:** Illiterate beneficiaries may struggle to type a 12-digit number without assistance `[AI]`.

### Scenario 1.2: Rural Telecom Voice Quality & Codec Degradation
- **Attack / Failure:** In rural hamlets, 2G cellular voice suffers severe packet loss and jitter during monsoon storms, turning text-to-speech Kannada audio into unintelligible noise.
- **Severity:** High · **Likelihood:** Medium `[?]` · **Detectability:** Difficult
- **Impact:** Beneficiaries mishear grain availability or arrive expecting grain that hasn't unloaded.
- **Mitigation (`[AI]` UX):** The IVR script repeats key numbers twice in slow cadence (*"20 kilograms. I repeat: two-zero kilograms"*) and triggers a fallback SMS text to the calling number.
- **Residual Risk:** Background noise in village streets impairs listening comprehension `[?]`.

### Scenario 1.3: False Stock Arrival Signal (Premature Truck Departure Confirmation)
- **Attack / Failure:** Godown truck dispatch is marked "Delivered" when the truck leaves the FCI depot, but the truck breaks down on the state highway. Beneficiaries hear "Grain ready" and walk 3 km to a shuttered shop.
- **Severity:** High · **Likelihood:** Medium `[?]` · **Detectability:** Moderate
- **Impact:** Destroys citizen trust in Channel 1; beneficiary loses half a day's wages.
- **Mitigation (`[T]` Logic):** The system strictly enforces that "Stock Unloaded" status can only be triggered by the dealer counter terminal scanning the physical unload challan, *not* by godown departure events.
- **Residual Risk:** Collusion where a dealer confirms arrival before bags are offloaded `[AI]`.

### Scenario 1.4: Complete Village Cellular Outage (Tower Blackout)
- **Attack / Failure:** Power grid failure knocks out the local BSNL/Airtel cellular base station for 48 hours. Neither IVR nor SMS functions.
- **Severity:** Medium · **Likelihood:** Low `[?]` · **Detectability:** Easy
- **Impact:** Citizen pre-travel notification is completely offline.
- **Mitigation (`[AI]` Fallback):** Citizens revert to walking to the shop. However, Channel 2 (the offline counter ledger) ensures that *if* they walk, the counter continues distributing grain offline.
- **Residual Risk:** Pre-trip wasted walk cannot be eliminated during total cellular blackouts `[AI]`.

---

## 2. Domain 2: Fair Price Shop Dealer Operations & Counter Stress

### Scenario 2.1: Dealer Refusal / Walkout under Crowd Pressure
- **Attack / Failure:** 100 cardholders queue up on the 2nd of the month. When ePOS server timeouts occur, the dealer claims the software is broken and shuts the shop shutters to escape crowd anger.
- **Severity:** Critical · **Likelihood:** Medium `[AI]` · **Detectability:** Easy
- **Impact:** Beneficiaries turned away; public unrest.
- **Mitigation (`[AI]` Operations):** The counter UI provides a prominent, high-contrast **"OFFLINE EXCEPTION MODE ACTIVE"** banner that displays current state-approved exception quota percentage (e.g. *"5.2% of 10% used"*), giving the dealer legal confidence to continue distribution.
- **Residual Risk:** Human psychological panic under aggressive crowd agitation cannot be solved solely by software `[AI]`.

### Scenario 2.2: Terminal Power Failure Mid-Queue
- **Attack / Failure:** Grid power cuts during morning distribution; the ePOS device's worn lithium battery drops to 0% and shuts down mid-transaction.
- **Severity:** High · **Likelihood:** High `[?]` · **Detectability:** Easy
- **Impact:** Terminal dies while recording a grain issuance.
- **Mitigation (`[T]` Executed Test):** SQLite Write-Ahead Logging (WAL) mode guarantees atomic transactions. Uncommitted writes roll back cleanly; upon restart, the database integrity check passes and the last valid hash-chain state is restored without corruption.
- **Residual Risk:** Distribution stalls until power is restored or a power bank is connected `[T]`.

### Scenario 2.3: Multiple Beneficiaries Claiming the Same Ration Card
- **Attack / Failure:** Two estranged family members (or a dishonest neighbour holding a duplicate card photocopy) attempt to claim the family's 20 kg quota separately.
- **Severity:** High · **Likelihood:** Low `[?]` · **Detectability:** Easy
- **Impact:** Legitimate family members are left without foodgrains.
- **Mitigation (`[T]` Executed Test):** Local database enforces a strict unique constraint on `(card_id, year_month)`. Once Card #1042 has redeemed its monthly allotment, subsequent attempts on that terminal are immediately rejected with an alert: *"Quota already redeemed on 2026-11-03 at 10:14 AM"*.
- **Residual Risk:** If family members coordinate across two disconnected shops, split-brain duplicate risk occurs (see Domain 4) `[T]`.

---

## 3. Domain 3: Cryptographic Security & Ledger Tampering

### Scenario 3.1: Retroactive Record Alteration (Modifying Quantities in SQLite)
- **Attack:** Dealer opens the local SQLite database using a tool like `sqlite3` CLI and updates record #2 from 20 kg to 35 kg to cover up 15 kg of diverted rice.
- **Severity:** Critical · **Likelihood:** Medium `[T]` · **Detectability:** Immediate
- **Impact:** Black-market grain diversion.
- **Mitigation (`[T]` Executed Test):** `verify_chain()` recomputes the SHA-256 payload hash of every row. Altering row #2 breaks row #2's hash and invalidates the HMAC signature. Furthermore, row #3's `prev_hash` no longer matches row #2's hash, breaking the entire chain.
- **Test Evidence:** Executed in `test_record_payload_modification_fails` (Assert: PASS).

### Scenario 3.2: Record Deletion / Dropped Rows
- **Attack:** Dealer deletes record #3 from the database to hide that a favoured customer received grain without payment.
- **Severity:** Critical · **Likelihood:** Medium `[T]` · **Detectability:** Immediate
- **Impact:** Missing audit history.
- **Mitigation (`[T]` Executed Test):** Strict monotonic sequence numbers (`seq = prev_seq + 1`). Deleting row #3 causes row #4 (`seq=4`) to follow row #2 (`seq=2`), triggering immediate sequence gap failure. Furthermore, row #4's `prev_hash` does not match row #2's hash.
- **Test Evidence:** Executed in `test_record_deletion_breaks_chain` (Assert: PASS).

### Scenario 3.3: Ledger Truncation Attack
- **Attack:** Dealer deletes the final 10 transactions recorded during an afternoon offline session before the food inspector arrives.
- **Severity:** Critical · **Likelihood:** High `[T]` · **Detectability:** Immediate via Checkpoint Pinning
- **Impact:** Unrecorded offline transactions.
- **Mitigation (`[T]` Executed Test):** End-of-day summary hash checkpoints are physically printed on the thermal paper roll and/or sent via one-way SMS ping to the state server. When `verify_chain()` runs with `pinned_checkpoint_hash`, it verifies that the final hash of the database matches the external anchor. Truncated databases fail verification instantly.
- **Test Evidence:** Executed in `test_ledger_truncation_caught_by_checkpoint` (Assert: PASS).

### Scenario 3.4: Full-Ledger Rewrite Attack with Stolen Local Key
- **Attack:** An attacker extracts the HMAC secret key from terminal storage and uses an automated script to regenerate an entirely new, internally consistent 50-record ledger with forged card numbers.
- **Severity:** Critical · **Likelihood:** Low `[T]` · **Detectability:** Immediate via External Checkpoint Pinning
- **Impact:** Total ledger forgery.
- **Mitigation (`[T]` Executed Test):** Although an attacker holding the key can generate valid individual HMAC signatures, they cannot forge past external anchors. When verified against the pinned checkpoint hash from the previous morning or central server sync anchor, the re-generated chain fails verification.
- **Test Evidence:** Executed in `test_full_ledger_rewrite_caught_by_checkpoint` (Assert: PASS).

### Scenario 3.5: Operating System Clock Manipulation (Clock Rollback)
- **Attack:** Dealer sets device system clock back from November 28 to November 2 to backdate offline transactions and bypass monthly quota limits.
- **Severity:** High · **Likelihood:** Medium `[T]` · **Detectability:** Immediate
- **Impact:** Bypassing monthly quota resets.
- **Mitigation (`[T]` Executed Test):** The ledger enforces strictly monotonic sequence numbers (`seq = i + 1`) independent of clock time. Non-monotonic timestamps or backdated sequence insertions are rejected by the validator.
- **Test Evidence:** Executed in `test_sequence_number_gap_or_rollback_detected` (Assert: PASS).

### Scenario 3.6: Unauthorized Key Injection / Key Compromise
- **Attack:** Attacker signs records using an arbitrary or forged private key.
- **Severity:** Critical · **Likelihood:** Low `[T]` · **Detectability:** Immediate
- **Impact:** Rogue offline transactions.
- **Mitigation (`[T]` Executed Test):** The central verification auditor checks every HMAC against the officially registered dealer terminal key. Signatures generated with unauthorized keys fail HMAC verification.
- **Test Evidence:** Executed in `test_wrong_secret_key_fails_hmac` (Assert: PASS).

---

## 4. Domain 4: Distributed Systems & Reconciliation Edge Cases

### Scenario 4.1: Split-Brain Duplicate Drawal Across Two Disconnected Shops
- **Attack / Failure:** Beneficiary family Card #1042 draws 20 kg at Shop A while Shop A is offline. The family's son takes the physical card to Shop B in the neighbouring village, which is also offline, and claims another 20 kg.
- **Severity:** Critical · **Likelihood:** Medium `[AI]` · **Detectability:** Detected upon Central Sync
- **Impact:** 20 kg foodgrain double-drawal leakage.
- **Mitigation (`[T]` Executed Test & Architectural Limit):**
  - **Honest Boundary:** Disconnected offline devices *cannot* prevent this in real time without communication.
  - **Reconciliation Engine:** `reconcile_batch_logs()` sorts incoming batch logs deterministically by timestamp and card ID. The first transaction is accepted; the second is flagged as `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` for administrative recovery and dealer notification.
- **Test Evidence:** Executed in `test_multi_device_duplicate_card_drawal_detected` (Assert: PASS).

### Scenario 4.2: Duplicate Batch Uploads (Network Glitch during Sync)
- **Attack / Failure:** The dealer connects to cellular data and begins uploading 30 offline receipts. The network drops after 15 receipts; the dealer retries, uploading all 30 again.
- **Severity:** Medium · **Likelihood:** High `[T]` · **Detectability:** Immediate
- **Impact:** Duplicate transaction records on state servers.
- **Mitigation (`[T]` Database):** Every offline receipt carries a deterministic transaction UUID based on its SHA-256 hash. Ingestion uses idempotent `INSERT OR IGNORE` semantics. Duplicate batch transmissions produce zero duplicate entries.

### Scenario 4.3: Out-of-Order Batch Synchronization
- **Attack / Failure:** Day 3 batch receipts are uploaded *before* Day 2 receipts because Day 2's sync failed.
- **Severity:** Medium · **Likelihood:** Medium `[T]` · **Detectability:** Handled
- **Impact:** Hash chain appears broken if ingested naively.
- **Mitigation (`[T]` Architecture):** Central sync verifies the entire hash chain per-terminal *locally* before merging into the central relational database, preserving per-terminal chain ordering.

---

## 5. Domain 5: Legal, Privacy & Regulatory Edge Cases

### Scenario 5.1: Exceeding State 5–10% Offline Exception Threshold
- **Attack / Failure:** Dealer uses offline mode for 40% of their monthly transactions, violating the state's 5–10% exception limit circular.
- **Severity:** High · **Likelihood:** Medium `[AI]` · **Detectability:** Easy
- **Impact:** Dealer license suspended; audit dispute.
- **Mitigation (`[AI]` Software Guard):** The terminal tracks cumulative offline transaction share. At 8%, a prominent amber warning appears (*"Approaching 10% offline limit"*); at 10%, offline transactions require explicit supervisor override confirmation.

### Scenario 5.2: Plaintext Aadhaar Exposure on Local Storage
- **Attack / Failure:** The terminal database stores 12-digit Aadhaar numbers in plaintext, violating Section 29 of the Aadhaar Act.
- **Severity:** Critical · **Likelihood:** Medium `[V]` · **Detectability:** Immediate
- **Impact:** Legal penalty; privacy violation.
- **Mitigation (`[V]` Compliance):** Plaintext Aadhaar numbers are never stored on disk. All cardholder references use masked format (`XXXX XXXX 1234`) or the state Ration Card ID. Zero biometric templates are retained.

### Scenario 5.3: False Statutory Authority Reliance
- **Attack / Failure:** A citizen or dealer presents an Anna-Mitra printed offline receipt in court, claiming it constitutes official government foodgrain clearance.
- **Severity:** High · **Likelihood:** Medium `[AI]` · **Detectability:** Easy
- **Impact:** Legal dispute; misrepresentation of public authority.
- **Mitigation (`[V]` Disclaimers):** Every printed receipt and screen banner explicitly carries statutory watermark text: *"Cryptographic local audit record only. Statutory transaction clearance subject to State Food Directorate ePOS reconciliation."*
