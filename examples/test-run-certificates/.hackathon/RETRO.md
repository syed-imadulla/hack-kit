# RETRO — Mock Social Good Hack (test run)

> Summary: Post-hackathon retrospective · One trip, not three. · Generated 2026-11-19 20:03

## 1. Executive summary
- **Event:** Mock Social Good Hack (test run)
- **Final Core Status:** v2
- **Trial Verdicts:** demo-1: FAIL, improve-r1: REVISE, pick-s1-farm-prices: REVISE, pick-s2-certificates: REVISE, verify: INCONCLUSIVE
- **Demo Delivery:** 7/9 built; 7 tested live (7 [V], 0 [T]); 3 mocked/simulated; 7 shown in run

## 2. Original goals versus actual outcomes
| Goal | Intended (Brief / Plan) | Actual Outcome (Demo / Verdict) | Status |
|---|---|---|---|
| Solve primary user problem | S2 repeat visits for certificates | One trip: spoken checklist + operator ready-to-sub | Achieved (Core) |
| Deliver functional demo | Fully tested MVP journey | 7/9 tested (3 mocked) | Partial [T] |
| Validate killer assumptions | All 'collapses' assumptions tested | 2 'collapses' assumptions left untested | Incomplete [V] |

## 3. Idea evolution
- **Initial Concept:** Problem: S2 repeat visits for certificates.
- **Pivots & Refinements:** Chose S2 (certificates); Chose idea 13 (spoken checklist + operator scan check)
- **Rejected Alternatives:** S1 farm prices (root cause may be debt/storage; existing ser; DigiLocker (no access), new portal (exists), policy change (; None rejected
- **Inside-Core Adjustments:** Maintained core journey without scope drift.

## 4. Assumption and evidence analysis
- **Total Assumptions:** 10 (0 validated, 8 open, 2 testing, 0 rejected)
- **Evidence Breakdown:** [V] 0 · [T] 0 · [AI] 8 · [?] 2
- **Killer ('collapses') Risk:** 2 untested 'collapses' assumptions remained.

## 5. Planned versus delivered features
Summary metrics:
- **Planned to build:** 8 · **Planned to mock:** 1 · **Planned to cut:** 0
- **Actually built:** 7 of 9 · **Not implemented (unbuilt):** 1 of 9 · **Planned mocks (no code):** 1
- **Tested live:** 7 of 9 (7 [V], 0 [T]) · **Untested:** 2 of 9
- **Mocked / simulated:** 3 of 9 · **Real implementation:** 6 of 9
- **Shown in demo:** 7 of 9 (5 full, 2 partial/text) · **Not shown:** 2 of 9

| Feature | Planned | Implementation | Tested | Demo Presentation | Mock Status |
|---|---|---|---|---|---|
| Checklist per purpose | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Watched scan folder + auto-run | Build | ❌ Not built | ⚠️ Untested | Not shown | Real (unmocked) |
| Document type + readability check | Build | Built | ✅ Tested [V] | Shown | ⚠ Mocked |
| Name match (Kannada/English) | Build | Built | ✅ Tested [V] | Shown (partly) | Real (unmocked) |
| Date validity rule | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Spoken Kannada (TTS) | Build | Built | ✅ Tested [V] | Shown (partly) | ⚠ Mocked |
| Missed-call callback | Mock | Planned mock | ⚠️ Untested | Not shown | ⚠ Mocked |
| Flag log | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |
| Aadhaar masking | Build | Built | ✅ Tested [V] | Shown | Real (unmocked) |

## 6. Team execution analysis
- **Critical Path:** T3 → T4 → T5 → T7 → T12 (14.0 h)
- **Workload Distribution:** d: 8.5 h · a: 10.5 h · c: 9.0 h · b: 7.0 h
- ⚠ Critical path is 14 h of 18 h to code freeze (78%): tight. Start the path first, and pick what to mock if it slips.

## 7. Jury and demo feedback
- **demo-1 (FAIL):**
  - Actual end user: Swap in real OCR (even Tesseract) for at least one live photographed document, and fix the disclosure so it says voice is printed text and the missed-call clip doesn't exist yet.
  - Least-digital user: Record real Kannada TTS clips for each flag and play one in the demo, then reword the disclosure so it matches what is actually mocked (voice and missed call are not built yet).
  - Front-line worker: Run real OCR on 3-5 real income-certificate scans live, show a clear message for unknown photos, and correct the mock disclosure to match what actually exists at freeze.
- **improve-r1 (REVISE):**
  - Actual end user: Lead with the missed-call Kannada checklist plus a family SMS; make the counter check add-on and say exactly which document to fix.
  - Least-digital user: Test the missed-call voice flow and operator read-aloud with five elderly Kannada speakers on keypad phones. Make spoken-answer input work, not only keypad menus.
  - Front-line worker: Auto-run the check on the scan folder the operator already saves to, so there is no drag step; if it fails, fall back to a printed checklist.
- **pick-s1-farm-prices (REVISE):**
  - Actual end user: Lead with today's fair price to bargain with the local trader at the farm gate; treat hold/sell and distant mandis as secondary, flag stale data.
  - Least-digital user: Use a free missed-call callback with a keypad menu fallback (press 1 for wheat), and let me hand the call over to a named FPO person.
  - Front-line worker: Add a simple staff view: flagged stale prices, a one-tap override to enter a local mandi rate, and a call log so farmers aren't misled.
- **pick-s2-certificates (REVISE):**
  - Actual end user: Interview 5-10 CSC operators and rejected applicants this week; count rejection causes and test the check flow with one operator at the counter.
  - Least-digital user: Speak the missing-document list aloud in the regional language and print or SMS a simple slip the family can read later.
  - Front-line worker: Use the documents the operator already scans for upload, give a one-screen pass/flag result in under 30 seconds, and fall back to a printed checklist when offline.
- **verify (INCONCLUSIVE):**
  - Actual end user: Run experiments 1 and 2 today with real operators and rejection records; also flag likely ineligibility (income over limit) before submission.
  - Least-digital user: Make one real missed-call checklist line in Kannada work, and let the operator replay the spoken flag with a simple 'bring this document' instruction.
  - Front-line worker: Run experiment 2 at a live counter: time each check, count false flags, and add a visible 'check unavailable, proceed manually' fallback.
- **Pitch Drill Honesty Score:** 1.75 / 5.0

## 8. Biggest mistakes
- **[Direct Cause] Killer assumption(s) "Document problems cause most rejections ...", "CSC operators will add a pre-check step..." remained unvalidated ([?] / [AI]) at trial.** → *Consequence:* Hack Court procedural rules strictly cap the verdict to REVISE (a solution cannot pass with unresolved collapses assumptions). *(Evidence: tally.py capping rule + ASSUMPTIONS.md)*
- **[Direct Cause] Demo Day Court (demo-1) voted FAIL with 0 NOT GUILTY votes.** → *Consequence:* Simulated jurors rejected the demo due to simulated components and pitch disclosure gaps: Swap in real OCR (even Tesseract) for at least one; Record real Kannada TTS clips for each flag and pl. *(Evidence: court/demo-1/verdict.md juror votes)*
- **[Direct Cause] Pitch drill detected unbuilt or overstated claims in deck/Q&A: "Q&A: "Built: folder watcher, operator sc".** → *Consequence:* Pitch honesty score penalized down to 1.75/5.0 (discrepancy between slides and DEMO.md). *(Evidence: PITCH.md Drill honesty evaluation)*
- **[Contributing Factor] Workload warning during planning (Critical path is 14 h of 18 h to code freeze (78%): tight. S) while feature(s) like 'Watched scan folder + auto-run' were not implemented.** → *Consequence:* High individual workload concentration is a plausible contributing factor to cutting or deferring tasks, though task prioritization may also explain the cut. *(Evidence: PLAN.md task load table + DEMO.md unbuilt status)*

## 9. Lessons learned
- **Evidence beats confidence:** Jurors and judges immediately detect when a team claims a feature is tested when it was merely mocked.
- **Run the code first:** The Demo Day Court failure ladder forced transparency before judging, preventing embarrassing live failures.
- **Test riskiest assumptions early:** If the idea collapses when a premise is false, spend the first 30 minutes verifying it before building.

## 10. Top three improvements for the next hackathon
1. **Verify killers in Phase 6:** Complete telephone/venue interviews before locking the plan; never carry untested 'collapses' assumptions into the demo.
2. **Keep pitch claims synchronized with DEMO.md:** Never allow deck headlines or Q&A answers to run ahead of tested implementation.
3. **Balance team workload at planning:** Reallocate tasks from overloaded members during /hack:plan to ensure buffer for integration.
