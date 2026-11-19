# CASE — Improvement Trial: Architecture v2 Hardening & Simplification

## Question on Trial
Has Anna-Mitra Architecture v2 successfully incorporated the findings of stress testing, eliminated fragile assumptions, simplified beneficiary and dealer workflows, hardened cryptographic protocols, and remained true to its core civic purpose without mission drift?

## Evidence Presented
1. **Removed Non-Essential Complexity (`IMPROVEMENTS.md`):**
   - Eliminated 4-digit IVR PINs that block elderly/low-literacy users; adopted Zero-PII open quota readout.
   - Replaced 5-step dealer screen with 2-tap "Standard Dispense" workflow reducing transaction time from 75s to <15s.
   - Dropped unverified truck GPS arrival alerts; added explicit data freshness timestamps.
2. **Cryptographic Hardening (`ARCHITECTURE-V2.md`, `app/crypto_core.py`, `tests/test_security_stress.py`):**
   - 10 passing unit tests verifying tamper detection, sequence gaps, external checkpoint pinning, independent monotonic clock rollback verification, and key rotation (`key_version`).
   - Mathematically honest acknowledgment that split-brain offline duplicate drawals cannot be prevented in real time; resolved via `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` upon central sync.
3. **Legal Compliance & Policy Accuracy (`DECISION-LOG.md`):**
   - NFSA PMGKAY free foodgrain (through 31 Dec 2028: 35 kg AAY / 5 kg PHH member) cleanly separated from dynamic Karnataka 2026-27 state add-ons (DBT / Subsidized Dal).
4. **Honest Assumption Tracking (`ASSUMPTIONS.md`):**
   - Field assumptions A1, A2, and A7 remain explicitly labeled as open unvalidated assumptions (`[?]`) awaiting physical pilot deployment.
