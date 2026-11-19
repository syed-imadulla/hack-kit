# CASE — Stress Trial: Red-Team Resilience & Threat Mitigations

## Question on Trial
Has Anna-Mitra Dual-Channel survived rigorous red-team attacks across beneficiary access, dealer rush-hour friction, cryptographic tampering, distributed split-brain concurrency, and legal boundaries without collapsing?

## Stress Evidence Presented
1. **Executable Security Tests (`tests/test_security_stress.py`):** 8 passing unit tests proving:
   - Tampered record payloads are detected instantly (`test_record_payload_modification_fails`).
   - Deleted rows cause sequence gap errors (`test_record_deletion_breaks_chain`).
   - Ledger truncation is defeated by external checkpoint hash pinning (`test_ledger_truncation_caught_by_checkpoint`).
   - Full-ledger rewrite attacks fail against pinned checkpoints (`test_full_ledger_rewrite_caught_by_checkpoint`).
   - Non-monotonic timestamps / clock rollbacks are rejected (`test_sequence_number_gap_or_rollback_detected`).
   - Multi-device duplicate card redemptions are flagged upon central sync (`test_multi_device_duplicate_card_drawal_detected`).
2. **Failure Analysis & Threat Model (`STRESS-TEST.md`, `THREAT-MODEL.md`, `FAILURE-MATRIX.md`):** 22 scenarios evaluated across 5 domains.
3. **Honest Limitations:** Explicit acknowledgment that disconnected devices cannot prevent split-brain double drawals in real time without network connectivity.
