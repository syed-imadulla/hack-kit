# ASSUMPTIONS — Certificate pre-check (S2)

> Summary: 8 open · 2 testing · 0 validated · 0 rejected · 2 "collapses" still open

## Test-first list
1. Document problems cause most rejections (collapses)
2. CSC operators will add a pre-check step (collapses)
3. Document photos can be checked reliably enough (weakens)

## All assumptions
| # | Assumption | Importance | Team confidence | Evidence (label) | Kill test | How to test | Pass if / fail if | Status | Updated | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Document problems cause most rejections (vs Tahsildar verification, eligibility) | critical | medium | [?] (no public data found) | collapses | Experiment 1 | Pass: 6+ of 10 are document issues · Fail: most are verification/eligibility | testing | 10:20 | court pick-s2 |
| 2 | CSC operators will add a pre-check step | critical | low | [?] | collapses | Experiment 2 | Pass: 2 of 3 say yes · Fail: 2 of 3 say no | testing | 10:20 | court pick-s2 |
| 3 | Document photos can be checked reliably enough | high | medium | [AI] | weakens | Run 10 sample documents through the checker | Pass: 8 of 10 correct flags · Fail: under 6 | open | 10:20 | pick |
| 4 | Applicants learn of rejection only after days, not at the counter | medium | medium | [AI] | weakens | Ask operators how long status takes | Pass: several days typical | open | 10:30 | users |
| 5 | Farm labourers lack standard income proof, causing rejections | high | medium | [AI] | weakens | Open the Karnataka income certificate checklist; ask an operator | Pass: self-declaration rules are unclear or often rejected | open | 10:30 | users |
| 6 | Applicants will call the checklist line before their first trip | high | low | [AI] | weakens | Ask 5 students at the venue if they would | Pass: 3 of 5 say yes and know when they need one | open | 10:45 | ideate |
| 7 | Name matching works across Kannada/English spellings | high | medium | [AI] | weakens | Test 10 name pairs | Pass: 9 of 10 correct | open | 10:45 | ideate |
| 8 | Many applicants lack the needed documents in DigiLocker | high | medium | [AI] | weakens | Ask 5 students whether their parents' documents are in DigiLocker | Pass: 3 of 5 say no | open | 11:10 | compete |
| 9 | Applicants can name the purpose even if not the certificate | medium | high | [AI] | weakens | Ask 5 students what they'd say | Pass: 4 of 5 name the purpose | open | 11:20 | stress |
| 10 | The check runs in under 30 s on existing scans | high | medium | [AI] | weakens | Time it on the prototype | Pass: under 30 s for 5 documents | open | 11:20 | stress |

- Kill test: **collapses** (the idea fails if this is false) · weakens · minor.
- Status: open · testing · validated (needs `[V]` or `[T]`) · rejected.
- Source: where it came from (users, ideate, stress, court <case>, team).

## Status history
| Date time | # | From → to | Evidence added | By |
|---|---|---|---|---|
| Day 1 11:00 | 1 | open → testing | Experiment 1 planned; no public rejection data found | Team |
| Day 1 11:00 | 2 | open → testing | Experiment 2 planned | Team |
