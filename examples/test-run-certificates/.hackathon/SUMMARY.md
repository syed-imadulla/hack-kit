# SUMMARY — One trip

> One trip, not three.

| | |
|---|---|
| Event / track | Mock Social Good Hack (test run) · S2 certificates |
| Team | A (captain, backend), B (frontend), C (AI), D (design + pitch) |
| Latest decision | INCONCLUSIVE · NG 5 · G 0 · IE 7 (full trial) · rubric estimate 68/100 |
| Idea | CORE v2 · combination of process shift + access shift |

## Problem
A rejected certificate application must be filed again from scratch ([Odisha e-District FAQ](https://edistrictapp.odisha.gov.in/fr/faq)), and a Karnataka income certificate takes up to 21 days in person ([tumkur.nic.in](https://tumkur.nic.in/?p=25892)).

## Solution
A missed-call checklist by purpose, plus a 30-second (target) check on the operator's existing scans that flags missing, unreadable or mismatched documents and explains them aloud in Kannada. Flags only; the operator decides; nothing is stored.

## Journey
1. Missed call → checklist in Kannada (mocked)
2. Operator scans as usual into a watched folder
3. Check auto-runs: type, readability, name match, dates
4. Operator plays the Kannada explanation
5. One submission

## What's built vs mocked
| Built | Mocked |
|---|---|
| Folder watcher, checks, operator screen, Kannada TTS, flag log | Missed-call line, SMS |

## Top ratings
| Item | /10 |
|---|---|
| Problem is real | 8 |
| Safe | 8 |
| Buildable and demo-able | 7 |

## Open assumptions (collapses / weakens)
| Assumption | Status |
|---|---|
| Document problems cause most rejections | testing (experiment 1) |
| Operators will run the check | testing (experiment 2) |

## Next steps
1. Phone 3 operators (experiment 1)
2. Add the eligibility warning if experiment 1 fails
3. Pre-test real scans; record the backup demo
