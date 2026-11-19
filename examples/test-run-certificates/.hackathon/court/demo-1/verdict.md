# Demo Day Court 1 — verdict

Jury: quick 7 (end user, least-digital user, front-line worker, government clerk [civic seat], root-cause analyst, engineer, sceptic) · separate subagents · raw votes in votes-raw.json (unedited)
Count: `tally.py votes-raw.json --expected 7 --open-collapses 2` → NG 0 · G 7 · IE 0 · average confidence 6.9/10 · weak-evidence votes 0
**Decision: FAIL** (G > NG). Advice, not a decision: the captain decides.

## Why (named by 5+ jurors)
1. The disclosure overstates what exists: "voice is pre-recorded" and "missed call is a recorded clip" are not true yet (7 of 7).
2. No real document goes end to end: OCR is mocked as JSON (7 of 7).
3. The problem cause is unproven: experiment 1 (phone operators) not done (6 of 7).

## Fix list from the jury (merged, ranked)
| # | Fix | Jurors | Hours |
|---|---|---|---|
| 1 | Reword the disclosure to match the ladder now | 7 | 0.1 |
| 2 | Run experiment 1: phone 3–5 operators | 5 | 1 |
| 3 | Real OCR (Tesseract kan+eng) on 1–3 real scans, JSON as disclosed fallback | 6 | 3 |
| 4 | Record Kannada TTS clips, missed-call clip, backup video | 3 | 2 |
| 5 | Clear message for unknown photos | 2 | 0.5 |
