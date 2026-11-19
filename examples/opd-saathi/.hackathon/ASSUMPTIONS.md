# ASSUMPTIONS — OPD Saathi

> Summary: 4 open · 1 testing · 1 validated · 1 rejected · 1 "collapses" still open (illustrative sample)

## Test-first list
1. Patients can describe symptoms by voice in a noisy OPD (collapses)
2. Hospitals allow WhatsApp or calls for check-in (weakens)
3. Doctors will approve suggested tests within 15 minutes (weakens)

## All assumptions
| # | Assumption | Importance | Team confidence | Evidence (label) | Kill test | How to test | Pass if / fail if | Status | Updated | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Patients can describe symptoms by voice in a noisy OPD | critical | medium | [?] | collapses | 3 people describe a symptom by voice in Kannada | Pass: 2 of 3 transcripts keep their words · Fail: fewer | testing | 18:30 | ideate |
| 2 | Hospitals allow WhatsApp or calls for check-in | high | low | [?] | weakens | Ask a hospital admin or mentor | Pass: allowed or pilot possible · Fail: banned | open | 17:35 | ideate |
| 3 | Doctors will approve suggested tests within 15 minutes | high | medium | [AI] | weakens | Ask 2 doctors how they'd use it | Pass: both say yes · Fail: both say no | open | 17:35 | ideate |
| 4 | Many patients return the same day only to show reports | high | high | [T] doctor's estimate | weakens | Ask an OPD nurse | Pass: confirms a large share | validated | 17:50 | users |
| 5 | Patients have smartphones | medium | low | [T] | minor | — | — | rejected | 17:20 | users |
| 6 | Nurses can enter vitals by token in rush hour | high | medium | [AI] | weakens | Time one entry on the prototype | Pass: under 30 seconds | open | 18:05 | stress |
| 7 | Audio can be deleted within 72 hours by policy | medium | medium | [AI] | minor | Check the DPDP Act guidance | Pass: allowed | open | 18:05 | stress |

- Kill test: **collapses** · weakens · minor.
- Status: open · testing · validated (needs `[V]` or `[T]`) · rejected.

## Status history
| Date time | # | From → to | Evidence added | By |
|---|---|---|---|---|
| 2026-11-19 17:20 | 5 | open → rejected | [T] many patients use keypad or family phones; design for calls instead | Team |
| 2026-11-19 17:50 | 4 | open → validated | [T] doctor sister's estimate | Team |
| 2026-11-19 18:30 | 1 | open → testing | Experiment 1 planned | Team |
