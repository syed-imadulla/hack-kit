# EXPERIMENTS — PDS Anna-Mitra Validation Experiment Cards

> Summary: Empirical test designs to validate the three critical collapses assumptions. Unperformed experiments are explicitly marked as PROPOSED.

---

## Experiment Card 1: Stock Arrival vs. Wasted Trips Audit

- **Card ID:** `EXP-01`
- **Status:** **PROPOSED** (Requires district food office permissions; not performed during hackathon)
- **Target Assumption:** Assumption 1 — *"Wasted trips to Fair Price Shops are primarily caused by stock delivery lag (unloaded grain) rather than shop opening hours."*
- **Hypothesis:** At least 50% of wasted beneficiary visits in the first 10 days of the month occur because the grain truck has not arrived or completed unloading at the shop, rather than dealer absenteeism.
- **Methodology:**
  1. Select 3 rural Fair Price Shops in a single taluk over the first 7 days of the monthly distribution cycle.
  2. Interview 60 beneficiaries exiting empty-handed outside the shops using a structured 3-question survey:
     - (a) Did you receive your monthly grain today?
     - (b) If not, what reason was given? (Stock not arrived / Machine server down / Dealer absent / Fingerprint rejected).
     - (c) How far did you travel to get here?
  3. Correlate survey responses with the wholesale FCI godown truck dispatch e-challans.
- **Sample Size:** 60 beneficiaries across 3 Fair Price Shops.
- **Success Threshold:** Delivery lag and stock unreadiness account for ≥ 40% of non-disbursement visits.
- **Failure Threshold (Kill Test Trigger):** Delivery lag accounts for < 20% of wasted visits (e.g. if dealer absenteeism or pure ePOS biometric rejection causes > 80% of failures).
- **Cost & Time:** ₹1,500 (field travel); 3 days field observation.
- **Limitations:** Self-reporting bias; dealers may alter operating behavior while observers are present.

---

## Experiment Card 2: Dialect IVR Comprehension & Adoption Test

- **Card ID:** `EXP-02`
- **Status:** **PROPOSED** (Simulated audio prototype ready; field user testing pending post-hackathon)
- **Target Assumption:** Assumption 2 — *"Beneficiaries with basic keypad phones will dial a free missed-call / IVR number to check if grains are unloaded before walking."*
- **Hypothesis:** At least 70% of low-literacy beneficiaries can listen to a 20-second automated spoken Kannada audio prompt and correctly state: (a) whether grain is available today, and (b) how many kilograms of free NFSA grain their family is entitled to.
- **Methodology:**
  1. Pre-record 3 realistic spoken Kannada audio prompts:
     - Prompt A: Shop 42 stocked; 4 members; 20 kg free NFSA rice.
     - Prompt B: Shop 42 NOT stocked yet; truck expected 4th Nov; do not travel yet.
     - Prompt C: Shop 42 stocked; AAY card; 35 kg free grain.
  2. Play audio samples over standard 2G cellular voice connection to 15 rural participants with basic keypad feature phones.
  3. Ask participants two comprehension questions: *"Is the shop ready today?"* and *"How many kilograms will you collect?"*
- **Sample Size:** 15 rural cardholders (8 women, 7 men; 10 holding basic keypad phones).
- **Success Threshold:** ≥ 11 of 15 (73%) correctly understand grain status and kilograms.
- **Failure Threshold (Kill Test Trigger):** ≤ 8 of 15 (53%) understand the audio prompt, or participants report that automated voice causes confusion.
- **Cost & Time:** ₹500 (telecom airtime); 4 hours testing.
- **Limitations:** Lab/simulated testing over phone does not replicate noisy village background environments.

---

## Experiment Card 3: Dealer Offline Queue Time & Usability Benchmark

- **Card ID:** `EXP-03`
- **Status:** **PROPOSED** (Benchmarked via synthetic CLI; live dealer field run pending)
- **Target Assumption:** Assumption 7 — *"Fair Price Shop dealers will accept a local offline logging workflow rather than turning citizens away or using paper notebooks."*
- **Hypothesis:** An offline cryptographic logging interface allows a Fair Price Shop dealer to authenticate and log a beneficiary's offline grain disbursement in under 8 seconds (< 3 physical interactions), maintaining queue velocity during network outages.
- **Methodology:**
  1. Set up the prototype terminal in offline mode (cellular disconnected).
  2. Simulate a queue of 10 consecutive cardholders presenting their 12-digit ration card IDs.
  3. Measure time from card entry to physical receipt printing and HMAC-SHA256 hash-chain commit.
  4. Collect dealer qualitative feedback on ease of use vs manual paper ledger.
- **Sample Size:** 2 Fair Price Shop operators running 20 simulated transactions each.
- **Success Threshold:** Average transaction logging time < 8.0 seconds per beneficiary; zero chain corruption; dealer confirms interface is faster than paper register.
- **Failure Threshold (Kill Test Trigger):** Average transaction logging time > 20 seconds; or dealers report that physical crowd pressure makes software interaction impractical.
- **Cost & Time:** ₹0 (local hardware); 2 hours testing.
- **Limitations:** Synthetic simulation cannot fully replicate crowd agitation during severe 2-hour server outages.

---

## Experiment Card 4: Multi-Device Duplicate Conflict Reconciliation Test

- **Card ID:** `EXP-04`
- **Status:** **EXECUTABLE BENCHMARK** (Implemented in project test suite `tests/test_pds_counter.py`)
- **Target Assumption:** Assumption 9 & Assumption 13 — *"Multi-device duplicate redemptions during network outages can be flagged through monotonic sequence numbers and monthly card quota bounds upon sync."*
- **Hypothesis:** When an identical ration card is redeemed at two disconnected offline counter terminals in the same calendar month, the central reconciliation engine detects the duplicate transaction upon synchronization and raises a `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` audit flag without ledger corruption.
- **Methodology:**
  1. Initialize two isolated offline SQLite databases (Terminal A and Terminal B) with identical starting card registries.
  2. Record a valid offline disbursement of 20 kg for Card #1042 on Terminal A.
  3. Record a simultaneous offline disbursement of 20 kg for Card #1042 on Terminal B.
  4. Ingest both batch logs into the central reconciliation script.
  5. Assert that the first transaction is accepted and the second is flagged as a duplicate conflict.
- **Sample Size:** 100 simulated concurrent transaction pairs across 5 simulated offline shops.
- **Success Threshold:** 100% of duplicate card disbursements flagged upon sync; zero silent quota double-drawals.
- **Failure Threshold:** Central ingestion accepts duplicate card disbursement without raising an audit flag.
- **Cost & Time:** ₹0; automated test execution in < 1 second.
- **Limitations:** Confirms algorithm correctness; does not address administrative recovery protocols once physical grain has left the shop.
