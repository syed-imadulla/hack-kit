# IMPROVE — One trip

> Summary: 1 round · CORE v1 → v2 · latest decision: REVISE (PASS by votes, capped while 2 "collapses" assumptions are untested)

## Round 1 — Day 1 11:30 IST
Feedback source: STRESS.md (no solution trial yet, so the pick trial is the only baseline)

### Candidates
| # | Change | Fixes which weakness | Impact | Effort | New risk | Evidence still needed | Inside core / DRIFT | Accepted? |
|---|---|---|---|---|---|---|---|---|
| 1 | Honest scope: "document-caused rejections only" + income-proof vs declared-band check | Field verification is out of reach | high | low | Smaller claim | Experiment 1 | inside | yes |
| 2 | Drag the existing scan folder; under 30 s; manual-tick fallback | Too slow at rush hour | high | medium | Scanner formats vary | Timing test | inside | yes |
| 3 | In-memory only, Aadhaar masked, shown in the demo | Privacy | high | low | — | — | inside | yes |
| 4 | Ask "what is it for?" and map it to the certificate | Applicant doesn't know the name | medium | low | Mapping errors | Ask 5 students | inside | yes |
| 5 | Checklist config with a "last checked" date | Checklists change | medium | low | — | — | inside | yes |
| 6 | "Possible issue, please check", never "approved" | Blame on the operator | medium | low | — | — | inside | yes |
| 7 | DigiLocker fetch when the citizen consents (L1) | DigiLocker makes it obsolete | medium | medium | Consent flow | — | inside | yes |

### Version comparison
| | v1 | v2 |
|---|---|---|
| What improved | — | Honest scope, faster operator flow, privacy shown, purpose-based checklist |
| What got worse or riskier | — | Smaller claim; depends on scanner file formats |
| Assumptions still open | 8 | 10 (2 added by stress) |
| Same problem and main user? | — | yes |

### Re-check (quick trial, civic seats: court/improve-r1)
| | Before (pick trial, problem-level) | After (solution, v2) |
|---|---|---|
| Decision | REVISE | REVISE (PASS by votes, capped: 2 untested "collapses" assumptions) |
| Votes (NG · G · IE) | 4 · 0 · 2 | 5 · 0 · 1 |
| Lowest rating | — | Works for real users (operator adoption untested) |

New suggestions from the re-trial, carried to `/hack:plan` (inside the core):
- Auto-run on the folder the operator already saves to, so there's no drag step (front-line worker)
- Log each flag and the operator's decision for accountability (government clerk)
- Demo on 3 seeded scan sets: clean, blurry, name mismatch (engineer)

### Stop or continue
Stop. The remaining P0 items are experiments 1 and 2 with real operators, not design changes. Another improve round can't fix an untested assumption.
