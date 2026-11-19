# Hack Kit Worked Examples

This directory contains real-world and reference examples created using the [Hack Kit](https://github.com/imadulla/hack-kit) framework across multiple hackathon profiles.

---

## Available Examples

### 1. [PDS Anna-Mitra](file:///home/syed-imadulla/Desktop/hack-kit/examples/pds-anna-mitra/README.md)
- **Track**: Public Distribution & Food Security (Civic & Public Service)
- **Profile**: Civic Profile · 24-hour hackathon · Full mode (all 14 phases)
- **Concept**: A dual-channel civic integrity bridge providing pre-travel voice quota transparency on basic keypad phones and tamper-evident offline cryptographic transaction logging during network outages.
- **Key Features Demonstrated**:
  - Full 14-phase workflow execution from initial flawed idea (*RationTrack* app) to hardened architecture v2.
  - Decoupled statutory Central NFSA PMGKAY (free through 2028: 35 kg AAY / 5 kg PHH member) from dynamic state add-ons (Karnataka 2026-27).
  - Genuine working SQLite3 WAL database with SHA-256 hash chaining, HMAC-SHA256 signatures, key rotation, and independent clock rollback detection.
  - Multi-terminal split-brain reconciliation detecting duplicate card drawals across disconnected shops.
  - 28 automated unit & integration tests (`tests/test_pds_counter.py` and `tests/test_security_stress.py`).
  - Strict evidence labeling (`[V]`, `[T]`, `[AI]`, `[?]`), assumption registers, and 7 Hack Court verdicts capped by open collapses assumptions.
  - Automated post-hackathon retrospective (`/hack:retro`).

### 2. [OPD Saathi](file:///home/syed-imadulla/Desktop/hack-kit/examples/opd-saathi/README.md)
- **Track**: Healthcare OPD Patient Experience
- **Profile**: Healthcare Profile · In-person hospital wait-time reduction
- **Concept**: A patient-facing voice check-in front desk for government hospital OPDs that starts doctor-approved basic tests while patients wait, eliminating wasted return trips.

### 3. [Test Run Certificates](file:///home/syed-imadulla/Desktop/hack-kit/examples/test-run-certificates/README.md)
- **Track**: Citizen Services & Certificates
- **Profile**: Social Good Hack · Full 14-phase trial
- **Concept**: Document pre-check for village CSC/e-Seva operators to prevent rejection of income and caste certificate applications.

---

## Running the Examples

Each example includes its own `.hackathon/` directory tracking the project's state, decisions, and Hack Court trials. To inspect or lint any example:

```bash
# Run Hack Kit project linter
python3 scripts/lint_project.py examples/pds-anna-mitra/.hackathon

# Check task plans
python3 scripts/plan_check.py examples/pds-anna-mitra/.hackathon/PLAN.md

# Run automated tests
python3 -m unittest discover -s examples/pds-anna-mitra/tests
```
