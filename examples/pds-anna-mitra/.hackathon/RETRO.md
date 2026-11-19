# RETRO — Civic & Public Service AI Hackathon

> Summary: Post-hackathon retrospective · Clear quotas before you walk; verified grain when the network drops. · Generated 2026-11-19 21:40

## 1. Executive summary
- **Event:** Civic & Public Service AI Hackathon
- **Final Core Status:** v2
- **Trial Verdicts:** compete: REVISE, demo: REVISE, ideation: REVISE, improve: REVISE, pick-s1-pds: REVISE, stress: REVISE, validate: REVISE
- **Demo Delivery:** 9/9 built; 6 tested live (6 [V], 0 [T]); 3 mocked/simulated; 8 shown in run

## 2. Original goals versus actual outcomes
| Goal | Intended (Brief / Plan) | Actual Outcome (Demo / Verdict) | Status |
|---|---|---|---|
| Solve primary user problem | S1: Fair Price Shop quota uncertainty, wasted trip | Anna-Mitra Dual-Channel (Pre-travel IVR/SMS + Tamp | Achieved (Core) |
| Deliver functional demo | Fully tested MVP journey | 6/9 tested (3 mocked) | Partial [T] |
| Validate killer assumptions | All 'collapses' assumptions tested | 3 'collapses' assumptions left untested | Incomplete [V] |

## 3. Idea evolution
- **Initial Concept:** Problem: S1: Fair Price Shop quota uncertainty, wasted trips, and ePOS outage queues.
- **Pivots & Refinements:** Select PDS quota transparency & outage resilience as problem; Strictly decouple Central NFSA (PMGKAY through 2028) from st
- **Rejected Alternatives:** Generic farmer price advisory (crowded, lacks operational fr; Hardcoding Karnataka Anna Bhagya rice quotas as permanent ce; Claiming "blockchain-grade" legal authorization for local of
- **Inside-Core Adjustments:** Maintained core journey without scope drift.

## 4. Assumption and evidence analysis
- **Total Assumptions:** 17 (9 validated, 4 open, 4 testing, 0 rejected)
- **Evidence Breakdown:** [V] 2 · [T] 7 · [AI] 5 · [?] 3
- **Killer ('collapses') Risk:** 3 untested 'collapses' assumptions remained.

## 5. Planned versus delivered features
Summary metrics:
- **Planned to build:** 7 · **Planned to mock:** 0 · **Planned to cut:** 2
- **Actually built:** 9 of 9 · **Not implemented (unbuilt):** 0 of 9
- **Tested live:** 6 of 9 (6 [V], 0 [T]) · **Untested:** 3 of 9
- **Mocked / simulated:** 3 of 9 · **Real implementation:** 6 of 9
- **Shown in demo:** 8 of 9 (8 full, 0 partial/text) · **Not shown:** 1 of 9

| Feature | Planned | Implementation | Tested | Demo Presentation | Mock Status |
|---|---|---|---|---|---|
| Offline SQLite Cryptographic Ledger | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Statutory Entitlement Rules Engine | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Two-Tap Dealer POS Dispense Flow | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Tamper Audit & Rollback Detection | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Split-Brain Duplicate Drawal Reconc | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Regional Audio Voice Simulator | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Telecom Inbound Cloud IVR Trunk | Build | Built | ⚠️ Untested | Shown | ⚠ Mocked |
| Aadhaar Biometric Fingerprint Hardw | Cut | Built | ⚠️ Untested | Not shown | ⚠ Mocked |
| Physical ESC/POS Thermal Slip Print | Cut | Built | ⚠️ Untested | Shown | ⚠ Mocked |

## 6. Team execution analysis
- **Critical Path:** T3 → T4 → T6 → T8 → T10 → T11 (16.0 h)
- **Workload Distribution:** lead: 12.0 h · backend: 7.5 h · voice: 5.5 h · frontend: 5.0 h
- ⚠ Critical path is 16 h of 18 h to code freeze (89%): tight. Start the path first, and pick what to mock if it slips.

## 7. Jury and demo feedback
- **compete (REVISE):**
  - The 'already exists' researcher: Clearly document Level 1 (zero-integration kiosk/IVR) as an independent operating mode
  - Government clerk: Include an explicit soft-cap warning in the counter UI when offline transactions hit 8%
  - The front-line worker: Store the complete audit log in SQLite even if the thermal printer runs out of paper
- **demo (REVISE):**
  - The sceptic: Package the audit tool as a one-tap Android inspector companion app
  - Government clerk: Print the words 'CENTRAL NFSA FREE' in bold capital letters on the physical thermal slip
  - The least-digital user: Promote caller-ID matching so if dialed from registered phone, pressing hash confirms their card immediately
- **ideation (REVISE):**
  - The actual end user: Make truck arrival confirmation automatic via SMS delivery receipt from the godown truck driver
  - The least-digital user: Use concise, slow-paced spoken Kannada with repetition and SMS backup
  - The front-line worker: Add automatic card-level monthly disbursement lock so offline double drawals are impossible
- **improve (REVISE):**
  - Government clerk: Print the words 'CENTRAL NFSA FREE' in bold capital letters on the physical thermal slip
  - The least-digital user: Promote caller-ID matching so if dialed from registered phone, pressing hash confirms their card immediately
  - The builder: Configure SQLite PRAGMA synchronous = NORMAL and batch sync commits
- **pick-s1-pds (REVISE):**
  - The actual end user: Tell me if the grain has physically unloaded before I walk 2 kilometres
  - The least-digital user: Make sure checking quota does not require a smartphone or English text
  - The front-line worker: Give dealers a safe offline buffer log that food inspectors can audit
- **stress (REVISE):**
  - The safety and ethics reviewer: Send end-of-day summary hash checkpoint via one-way SMS ping whenever a single bar of cellular signal appears
  - Government clerk: Display the Food Inspector's direct emergency phone number on the screen when the 10% limit is reached
  - The least-digital user: Zero menu trees: user simply enters 12 digits and immediately hears their quota without pressing 1 for this or 2 for that
- **validate (REVISE):**
  - The actual end user: Provide automated SMS receipt alongside spoken Kannada prompt
  - The front-line worker: Keep counter offline interaction under 2 taps and provide clear visual offline status
  - The sceptic: Maintain honest [?] labels into the final pitch; never claim field adoption without data

## 8. Biggest mistakes
- **[Direct Cause] Killer assumption(s) "Wasted trips to Fair Price Shops are pri...", "Beneficiaries with basic keypad phones w..." remained unvalidated ([?] / [AI]) at trial.** → *Consequence:* Hack Court procedural rules strictly cap the verdict to REVISE (a solution cannot pass with unresolved collapses assumptions). *(Evidence: tally.py capping rule + ASSUMPTIONS.md)*
- **[Correlation] Tight execution schedule recorded during planning: Critical path is 16 h of 18 h to code freeze (89%): tight. S.** → *Consequence:* Workload utilization was high, reducing buffer for unexpected bugs, though all scheduled critical path items completed. *(Evidence: PLAN.md workload warnings)*

## 9. Lessons learned
- **Evidence beats confidence:** Jurors and judges immediately detect when a team claims a feature is tested when it was merely mocked.
- **Run the code first:** The Demo Day Court failure ladder forced transparency before judging, preventing embarrassing live failures.
- **Test riskiest assumptions early:** If the idea collapses when a premise is false, spend the first 30 minutes verifying it before building.

## 10. Top three improvements for the next hackathon
1. **Verify killers in Phase 6:** Complete telephone/venue interviews before locking the plan; never carry untested 'collapses' assumptions into the demo.
2. **Synchronize pitch slides with the demo ladder:** Ensure any simulated element is explicitly disclosed.
3. **Balance team workload at planning:** Reallocate tasks from overloaded members during /hack:plan to ensure buffer for integration.
