# STATE — OPD Saathi (example)

> Summary: Acharya The Big Hack · phase 10 lock done · next: /hack:plan

Schema version: 2
Last updated: 2026-11-19 18:30 IST

| Field | Value |
|---|---|
| Event | OPD Saathi (example) |
| Track | Healthcare AI Agents |
| Event length | 24 h |
| Mode | full |
| Captain (final decider) | Team lead |
| Chosen statement | Long OPD waits; patients get only a few minutes with the doctor |
| Chosen idea | Voice check-in + doctor-approved basic tests while patients wait |
| Motto | Patients wait 2 hours to get 2 minutes. OPD Saathi makes those 2 hours count. |
| CORE version | v2 |
| Core locked at | 2026-11-19 18:25 IST |

## Phases
| # | Phase | Status | When | Notes |
|---|---|---|---|---|
| 1 | start | done | 16:40 | |
| 2 | decode | done | 16:50 | |
| 3 | pick (trial) | done | 17:05 | |
| 4 | users | done | 17:20 | |
| 5 | ideate | done | 17:35 | access shift chosen |
| 6 | validate | done | 17:50 | 1 experiment planned |
| 7 | compete | done | 17:55 | |
| 8 | stress | done | 18:05 | |
| 9 | improve | done | 18:20 | v1 → v2 |
| 10 | lock | done | 18:25 | |
| 11 | plan | next | | |
| 12 | verify (trial) | not started | | |
| 13 | pitch | not started | | |
| 14 | ship | not started | | |

## Decisions log
| Time | Decision | Why | Rejected (and why) | By |
|---|---|---|---|---|
| 17:35 | Access-shift idea: voice check-in | Least-digital patients can use a normal call | Kiosk (new hardware), patient app (needs install) | Captain |
| 18:20 | Any authorised doctor on duty approves AI test suggestions | Matches how authority works in OPDs | Head-of-department sign-off (unrealistic) | Captain |
| 18:20 | Doctor picks follow-up in one tap | Respects clinical judgement | Automatic 2-day calls | Captain |

## Locked
- Problem: long OPD waits with little doctor time, and same-day returns just to show reports
- Main user: OPD patients, including those with keypad phones
- Core journey: token → voice check-in → vitals → rules → doctor-approved tests → smart queue → doctor → voice explanation
- Motto: Patients wait 2 hours to get 2 minutes. OPD Saathi makes those 2 hours count.

## Pending
- [ ] Run experiment 1 (Kannada voice check-in with 3 people)

## Rules
- After lock, the problem, main user, core journey and motto don't change without the captain's OK. Solution details can still improve through `/hack:improve`.

## Next command
/hack:plan
