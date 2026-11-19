# Hack Kit Worked Examples

This directory contains real-world and reference examples created using the [Hack Kit](https://github.com/syed-imadulla/hack-kit) framework across multiple hackathon profiles.

---

## Available Examples

### 1. [PDS Anna-Mitra](pds-anna-mitra/README.md)
- **Track**: Public Distribution & Food Security (Civic & Public Service)
- **Profile**: Civic Profile · 24-hour hackathon · Full mode (all 14 phases)
- **Concept**: A dual-channel civic integrity bridge providing pre-travel voice quota transparency on basic keypad phones and tamper-evident offline cryptographic transaction logging during network outages.
- **Key Features Demonstrated**:
  - Full 14-phase workflow execution from initial flawed idea (*RationTrack* app) to hardened architecture v2.
  - Decoupled statutory Central NFSA PMGKAY (free through 2028: 35 kg AAY / 5 kg PHH member) from dynamic state add-ons (Karnataka 2026-27).
  - Genuine working SQLite3 WAL database with SHA-256 hash chaining, HMAC-SHA256 signatures, key rotation, and independent clock rollback detection.
  - Multi-terminal split-brain reconciliation detecting duplicate card drawals across disconnected shops.
  - 32 automated unit & integration tests (`tests/test_pds_counter.py` and `tests/test_security_stress.py`).
  - Strict evidence labeling (`[V]`, `[T]`, `[AI]`, `[?]`) and assumption registers.
  - **One real Demo Day Court** (`court/demo-1/`, separate juror subagents): **FAIL 0–7**. It caught a repeat-dispense bug and a 500 kg "free" receipt; the fix and 4 tests were added afterwards.
  - 7 earlier trials kept in `court-illustrative/` as format examples only: their votes were written in one pass, not by separate jurors.
  - 11 hand-written extra notes in `.hackathon/extras/` (not produced by Hack Kit).
  - Automated post-hackathon retrospective (`/hack:retro`).

### 2. [OPD Saathi](opd-saathi/README.md)
- **Track**: Healthcare OPD Patient Experience
- **Profile**: Healthcare Profile · In-person hospital wait-time reduction
- **Concept**: A patient-facing voice check-in front desk for government hospital OPDs that starts doctor-approved basic tests while patients wait, eliminating wasted return trips.

### 3. [Test Run Certificates](test-run-certificates/README.md)
- **Track**: Citizen Services & Certificates
- **Profile**: Social Good Hack · Full 14-phase trial
- **Concept**: Document pre-check for village CSC/e-Seva operators to prevent rejection of income and caste certificate applications.
- **Includes**: the real trial records from Hack Kit's own end-to-end test runs (separate juror subagents), a small prototype, and a Demo Day Court that failed it 0–7.

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
