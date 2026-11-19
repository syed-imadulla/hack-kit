# CASE — Validation Trial: Anna-Mitra Dual-Channel Foundation

## Question on Trial
Has the validation phase established a realistic operational, technical, and regulatory foundation for Anna-Mitra Dual-Channel, or do unresolved assumptions and risks require another pivot before building?

## Context & Evidence Presented
1. **Critical Assumptions:** The three collapses assumptions (A1: truck arrival root cause; A2: keypad voice dial-in adoption; A7: dealer offline software acceptance) have been mapped to structured experiment cards (`EXP-01`, `EXP-02`, `EXP-03`). They are honestly labeled as `[?] PROPOSED` rather than fabricated as completed.
2. **Technical Correction on Offline Duplicates:** The system explicitly acknowledges that disconnected offline devices *cannot* prevent multi-location split-brain double drawals in real time. It implements an asynchronous conflict detection and audit reconciliation architecture (`EXP-04` / `[T]`).
3. **Statutory & Regulatory Alignment:** Central NFSA PMGKAY (free 35 kg AAY / 5 kg PHH through 31 Dec 2028) is verified (`[V]`) and decoupled from variable state add-ons. State 5–10% offline exception quotas are modeled.
4. **Security & Cryptographic Hardening:** Hash-chaining is augmented with monotonic sequence numbers, external checkpoint hash pinning, and Aadhaar masking.
