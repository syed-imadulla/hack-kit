# Demo Day Court 1 — verdict

Jury: quick 7 (end user, least-digital user, front-line worker, government clerk [civic seat], root-cause analyst, engineer, sceptic) · each a separate subagent that saw only case.md, prosecution.md and defense.md · raw votes in votes-raw.json (unedited)
Count: `tally.py votes-raw.json --expected 7 --open-collapses 3` → NG 0 · G 7 · IE 0 · average confidence 7.9/10 · weak-evidence votes 0
**Decision: FAIL** (G > NG). Advice, not a decision: the captain decides.

Evidence came from the reviewer running the prototype on 19 Nov 2026 (v1.2.2 review), not from the team's own DEMO.md alone.

## Why (named by 5+ jurors)
1. The rules claim was false: 20 repeat dispenses of one card in a month were accepted, and a 500 kg "100% FREE" receipt was printed (7 of 7).
2. The problem link is unproven: A1, A2 and A7 are open "collapses" assumptions (6 of 7).
3. The Kannada voice line prints text but was labelled "Real"; the backup video doesn't exist (6 of 7).

## Fix list from the jury (merged)
| # | Fix | Jurors | Status |
|---|---|---|---|
| 1 | One dispense per card per month, capped at the entitlement | 7 | Done after the trial: 4 tests added, CLI rejects both cases [V] |
| 2 | Relabel the voice line as text-only | 6 | Done in DEMO.md |
| 3 | Validate A1/A2 with beneficiaries and dealers | 5 | Open |
| 4 | Record or drop the backup video | 3 | Open |
| 5 | Show an export to the Ahara record format | 1 | Open |

Not re-tried after fix 1.
