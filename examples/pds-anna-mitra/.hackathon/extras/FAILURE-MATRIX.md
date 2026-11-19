# FAILURE-MATRIX — PDS Anna-Mitra Comprehensive Failure & Risk Register

> Summary: Master risk matrix grading 22 failure and attack scenarios across Severity, Likelihood, Impact, Detectability, Mitigation, and Residual Risk.

---

## 1. Master Risk Matrix

| # | Failure / Attack Scenario | Domain | Severity | Likelihood | Detectability | Primary Architectural Mitigation | Residual Risk | Status |
|---|---|---|---|---|---|---|---|---|
| **1** | Beneficiary lacks phone / shared migrant phone | Access | High | High `[?]` | Easy | Inbound pull IVR accessible from any borrowed phone | Dialing assistance needed | Mitigated `[AI]` |
| **2** | 2G cellular voice codec degradation | Access | High | Med `[?]` | Moderate | Slow repetition of numbers + fallback SMS | Low village audio clarity | Mitigated `[AI]` |
| **3** | False truck arrival signal | Access | High | Med `[?]` | Moderate | Unload signal locked to dealer physical scan | Dealer driver collusion | Mitigated `[T]` |
| **4** | Total village cellular blackout | Access | Med | Low `[?]` | Easy | Offline counter ledger ensures distribution continues | Pre-trip walk not prevented | Operational limit |
| **5** | Dealer refuses workflow under crowd rush | Dealer | Critical | Med `[AI]` | Easy | High-visibility offline exception banner (< 2 taps) | Human panic / walkout | Mitigated `[AI]` |
| **6** | Terminal power failure mid-queue | Dealer | High | High `[?]` | Easy | SQLite Write-Ahead Logging (WAL) atomic rollback | Distribution paused | **Verified `[T]`** |
| **7** | Multiple claims on same card at same shop | Dealer | High | Low `[?]` | Immediate | Local unique constraint `(card_id, year_month)` | Coordinated split-brain | **Verified `[T]`** |
| **8** | Retroactive grain weight tampering in SQLite | Security | Critical | Med `[T]` | Immediate | SHA-256 payload hash + HMAC-SHA256 signature | None (chain breaks) | **Verified `[T]`** |
| **9** | Row deletion / dropped record attack | Security | Critical | Med `[T]` | Immediate | Monotonic sequence enforcement (`seq = i + 1`) | None (gap flags corruption) | **Verified `[T]`** |
| **10**| Ledger truncation attack | Security | Critical | High `[T]` | Immediate | External checkpoint hash pinning against physical roll | None (checkpoint mismatch) | **Verified `[T]`** |
| **11**| Full-ledger rewrite with stolen key | Security | Critical | Low `[T]` | Immediate | Historical checkpoint anchor verification | None (anchor mismatch) | **Verified `[T]`** |
| **12**| Clock rollback to bypass monthly quotas | Security | High | Med `[T]` | Immediate | Strictly monotonic sequence numbers independent of clock | None (sequence rollback rejected) | **Verified `[T]`** |
| **13**| Unauthorized HMAC key injection | Security | Critical | Low `[T]` | Immediate | Central verification against registered terminal keys | None (HMAC invalid) | **Verified `[T]`** |
| **14**| Split-brain duplicate drawal across 2 shops | Distributed| Critical | Med `[AI]` | Upon Sync | Central reconciliation flags `CONFLICT_DUPLICATE_OFFLINE` | Disconnected 24h window | **Verified `[T]`** |
| **15**| Duplicate batch uploads during sync retry | Distributed| Med | High `[T]` | Immediate | Idempotent `INSERT OR IGNORE` with transaction UUID | None (re-upload is no-op) | **Verified `[T]`** |
| **16**| Out-of-order batch synchronization | Distributed| Med | Med `[T]` | Handled | Per-terminal local chain verification before merge | None (ordered per terminal) | **Verified `[T]`** |
| **17**| Exceeding state 5–10% offline quota limit | Legal | High | Med `[AI]` | Easy | Automated UI warnings at 8%; hard block at 10% | Emergency supervisor override | Mitigated `[AI]` |
| **18**| Plaintext Aadhaar number exposure | Privacy | Critical | Med `[V]` | Immediate | Strict masking (`XXXX XXXX 1234`); 0 biometric storage | None (never written to disk) | **Verified `[V]`** |
| **19**| False statutory authority reliance | Legal | High | Med `[AI]` | Easy | Explicit statutory watermark on all receipts and screens | Legal misunderstanding | Mitigated `[V]` |
| **20**| Interrupted SQLite write on power pull | Security | High | High `[?]` | Immediate | SQLite WAL mode crash recovery | Unsaved last in-flight row | **Verified `[T]`** |
| **21**| Thermal printer paper roll exhaustion | Dealer | Med | High `[?]` | Immediate | Complete audit record retained in SQLite regardless of print | No physical paper for citizen | Mitigated `[T]` |
| **22**| Keypad DTMF entry errors by citizen | Access | Med | High `[?]` | Moderate | Audio confirmation step (*"You entered card 1042. Press 1 to confirm"*) | Abandoned phone calls | Mitigated `[AI]` |

---

## 2. Re-Assessment of the Three Critical Collapses Assumptions

1. **Assumption 1 (Stock Arrival vs. Wasted Trips):**
   - *Status:* Remains **`[?]` (Testing)**. If wasted trips are primarily caused by dealer absence rather than delivery truck lag, Channel 1's impact is reduced. Mitigation: Ensure dealer attendance is tied to shop open status.
2. **Assumption 2 (Keypad Phone IVR Adoption):**
   - *Status:* Remains **`[?]` (Testing)**. Illiterate cardholders may struggle with 12-digit DTMF keypad entry without family assistance. Mitigation: Simple DTMF confirmation + SMS backup.
3. **Assumption 3 / 7 (Dealer Offline Software Adoption):**
   - *Status:* Remains **`[?]` (Testing)**. If counter software requires more than 2 keystrokes, dealers under crowd rush will abandon it for paper. Mitigation: Single-tap confirmation workflow.
