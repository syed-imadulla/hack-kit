# CASE — Demo Day Trial: Verification of Working MVP & Truthful Disclosures

## Question on Trial
Has Anna-Mitra delivered a working, tested, and honestly disclosed MVP that fulfills its locked core promise under real-world constraints without unverified claims?

## Verification Evidence Presented
1. **Working Code & Test Suite (`app/pds_counter.py`, `app/crypto_core.py`, `tests/test_pds_counter.py`):**
   - 19 automated tests passing with 0 failures [V].
   - Genuine SQLite3 database running with WAL mode and local transaction commits in < 15ms.
   - Deterministic entitlement engine strictly adhering to NFSA PMGKAY (free foodgrain through 31 Dec 2028: 35 kg AAY / 5 kg PHH member).
   - Tamper-evident SHA-256 hash chaining + HMAC-SHA256 signature verification catching row edits, deletions, sequence breaks, and clock rollback.
   - Pinned checkpoint hash verification defeating full-ledger rewrites.
   - Multi-device split-brain reconciliation detecting duplicate card drawals across disconnected shops.
2. **Honest Mock Disclosures (`DEMO.md` Feature Ladder):**
   - Real components explicitly labeled: SQLite ledger, rules engine, two-tap CLI, verify-chain auditor, conflict reconciler, regional Kannada dialogue.
   - Mocked components clearly disclosed: Telecom telephony PRI trunk, physical thermal paper printer, Aadhaar biometric scanner.
3. **Open Field Collapses (`ASSUMPTIONS.md`):**
   - The three killer assumptions (A1: stock arrival lag, A2: IVR dial-in preference, A7: dealer adoption) remain unvalidated in the field and are marked `[?]`.
