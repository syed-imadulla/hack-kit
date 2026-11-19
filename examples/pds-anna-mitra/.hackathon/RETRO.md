# RETRO — Civic & Public Service AI Hackathon

> Summary: Post-hackathon retrospective · Clear quotas before you walk; verified grain when the network drops. · Generated 2026-11-19 18:02

## 1. Executive summary
- **Event:** Civic & Public Service AI Hackathon
- **Final Core Status:** v2
- **Trial Verdicts:** demo-1: FAIL
- **Demo Delivery:** 9/9 built; 6 tested live (6 [V], 0 [T]); 3 mocked/simulated; 8 shown in run

## 2. Original goals versus actual outcomes
| Goal | Intended (Brief / Plan) | Actual Outcome (Demo / Verdict) | Status |
|---|---|---|---|
| Solve primary user problem | S1: Fair Price Shop quota uncertainty, wasted trips, and… | Anna-Mitra Dual-Channel (Pre-travel IVR/SMS +… | Not proven: latest trial demo-1 was FAIL |
| Deliver functional demo | Fully tested MVP journey | 6/9 tested (3 mocked) | Partial [V] |
| Validate killer assumptions | All 'collapses' assumptions tested | 3 'collapses' assumptions left untested | Incomplete |

## 3. Idea evolution
- **Initial Concept:** Problem: S1: Fair Price Shop quota uncertainty, wasted trips, and ePOS outage queues.
- **Pivots & Refinements:** Select PDS quota transparency & outage resilience as problem; Strictly decouple Central NFSA (PMGKAY through 2028) from state…
- **Rejected Alternatives:** Generic farmer price advisory (crowded, lacks operational friction); Hardcoding Karnataka Anna Bhagya rice quotas as permanent central entitlements; Claiming "blockchain-grade" legal authorization for local offline overrides
- **Inside-Core Adjustments:** None recorded.

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
| Offline SQLite Cryptographic Ledger | Build | Built | ✅ Tested [V] | Shown | Real |
| Statutory Entitlement Rules Engine | Build | Built | ✅ Tested [V] | Shown | Real |
| Two-Tap Dealer POS Dispense Flow | Build | Built | ✅ Tested [V] | Shown | Real |
| Tamper Audit & Rollback Detection | Build | Built | ✅ Tested [V] | Shown | Real |
| Split-Brain Duplicate Drawal… | Build | Built | ✅ Tested [V] | Shown | Real |
| Regional Audio Voice Simulator | Build | Built | ✅ Tested [V] | Shown | Real |
| Telecom Inbound Cloud IVR Trunk | Build | Built | ⚠️ Untested | Shown | ⚠ Mocked |
| Aadhaar Biometric Fingerprint Hardware | Cut | Built | ⚠️ Untested | Not shown | ⚠ Mocked |
| Physical ESC/POS Thermal Slip Printer | Cut | Built | ⚠️ Untested | Shown | ⚠ Mocked |

## 6. Team execution analysis
- **Critical Path:** T3 → T4 → T6 → T8 → T10 → T11 (16.0 h)
- **Workload Distribution:** lead: 12.0 h · backend: 7.5 h · voice: 5.5 h · frontend: 5.0 h
- ⚠ Critical path is 16 h of 18 h to code freeze (89%): tight. Start the path first, and pick what to mock if it slips.

## 7. Jury and demo feedback
- **demo-1 (FAIL):**
  - Actual end user: Block more than one dispense per card per month and cap at quota, then play real Kannada audio of stock status and quota to 5 villagers on keypad phones and count trips saved
  - Least-digital user: Add once-per-card-per-month and quota-cap checks, relabel the voice line as text-only, then run a real Kannada audio/IVR or missed-call SMS trial with 5 elderly keypad-phone users.
  - Front-line worker: Before printing a receipt, block a second dispense of the same card in the same month and any quantity above the entitlement. Add [V] tests for both, and relabel the voice line as text-only.

## 8. Biggest mistakes
- **[Open risk] Killer assumption(s) "Wasted trips to Fair Price Shops are primarily…", "Beneficiaries with basic keypad phones will dial…" were never tested.** → *Consequence:* The idea's premise is still unproven. No recorded trial was capped by this, so it is a risk, not a proven cause of any verdict. *(Evidence: ASSUMPTIONS.md)*
- **[Direct Cause] Demo Day Court (demo-1) decided FAIL (NOT GUILTY 0 · GUILTY 7 · INSUFFICIENT EVIDENCE 0).** → *Consequence:* Jurors' reasons: I keypad-phone Kenchaiah. The IVR is mocked and the 'Kannada voice' only prints text, so…; Kenchaiah gets nothing tested: IVR mocked, Kannada voice prints text only yet labelled… *(Evidence: court/demo-1/votes-raw.json)*
- **[Correlation] Tight execution schedule recorded during planning: Critical path is 16 h of 18 h to code freeze (89%): tight. Start the…** → *Consequence:* Little buffer was left for bugs. The files don't show whether this affected the result. *(Evidence: PLAN.md workload warnings)*

## 9. Lessons learned
Each lesson is an `[AI]` reading of the evidence named next to it. No evidence, no lesson.
- **Test the premise before building on it:** the 'collapses' assumptions were still untested at the end. *(Evidence: ASSUMPTIONS.md)*
- **Judge the demo by what runs, not by what's planned:** the Demo Day Court failed the built product. *(Evidence: court/ demo trial)*
- **Leave slack on the critical path:** the plan check warned the schedule was tight or overloaded. *(Evidence: PLAN.md plan check)*

## 10. Top three improvements for the next hackathon
1. **Test killer assumptions in phase 6:** Run the experiment cards (calls, venue interviews) before /hack:lock; don't carry an untested 'collapses' assumption into the demo.
2. **Rebalance the plan early:** Act on the plan check's warnings during /hack:plan, not after code freeze.
3. **Keep evidence labels current:** Update [V]/[T] labels whenever an experiment finishes. *(general practice, not from this project's data)*
