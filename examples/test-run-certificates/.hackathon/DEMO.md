# DEMO — One Trip (Demo Day check 1)

> Summary: 3 of 6 demo steps passing (2 manual or mocked) · 6 of 10 AI tests passing (1 partial) · decision: FAIL · 18 h to code freeze (test run: prototype built in the workspace, not by a real team)

## Feature ladder
| Feature | Planned | Built (where) | Tested (how, result) | Shown in demo run | Mocked → disclosed in pitch? |
|---|---|---|---|---|---|
| Checklist per purpose | Build | `app/checklists/income_certificate.json` | [V] loaded on every run; only income certificate exists | Yes | n/a |
| Watched scan folder + auto-run | Build | **Not built**: script takes a folder path | Not tested | No (run by hand) | Must say "run by the operator" or build it |
| Document type + readability check | Build | `onetrip.py` reads `readable` flag | [V] `scans/blurry` → "unreadable — ration_card" | Yes | **Vision OCR mocked as JSON**: must disclose |
| Name match (Kannada/English) | Build | `same_person()` fuzzy + initials | [V] "Laxmi Kumari" ≈ "Lakshmi K" passes; Kannada script vs English **flagged, not matched** | Partly | Transliteration not built: disclose |
| Date validity rule | Build | `max_age_days 365` | [V] 2023 income proof → "old — income_proof" | Yes | n/a |
| Spoken Kannada (TTS) | Build | Text only, `[TTS mocked]` | [V] correct Kannada sentence printed | Text only | **Mocked**: disclose or pre-record clips |
| Missed-call callback | Mock | — | — | Planned as clip | Disclosed in plan ✓ |
| Flag log | Build | `flaglog.sqlite` | [V] 3 rows written; no Aadhaar number stored | Yes | n/a |
| Aadhaar masking | Build | `onetrip.py` | [V] shown as `XXXX XXXX 9012` | Yes | n/a |

Labels: [V] = run and observed by Claude · [T] = reported by the team. Code existing is not evidence.

## Demo walk
| # | Step | Expected | Actual | Pass? | Time |
|---|---|---|---|---|---|
| 1 | Missed-call clip | Clip plays | Not recorded yet | ❌ | — |
| 2 | Scans land in folder, check auto-runs | Auto-run | Operator runs `python3 onetrip.py scans/mismatch` | ⚠ manual | — |
| 3 | Mismatch caught | Missing income proof + name flag | [V] both flags shown | ✅ | 0.01 s |
| 4 | Kannada read aloud | Audio | [V] text only (`[TTS mocked]`) | ⚠ mocked | — |
| 5 | "Never says approved" | Operator decides | [V] "looks complete (operator decides)" + Tahsildar line | ✅ | — |
| 6 | Clean set passes | "Looks complete" | [V] | ✅ | 0.01 s |

## Failure drill
| Failure | What happened | Fallback worked? |
|---|---|---|
| No internet | Everything runs locally (OCR mocked) | ✅ trivially, but only because the online parts are mocked |
| API key missing / API down | No API used yet | n/a until vision/TTS are wired |
| Slow or wrong AI answer | Wrong name match → flag for operator, never auto-fail | ✅ safe direction |
| Backup video recorded? | No | ❌ T12 still todo |

## AI test cases
| # | Input | Expected | Actual | Pass? |
|---|---|---|---|---|
| 1 | Clean set | "Looks complete" | [V] looks complete | ✅ |
| 2 | Blurry ration card | "Not readable" | [V] unreadable — ration_card | ✅ |
| 3 | "Lakshmi K" vs "Laxmi Kumari" | Not auto-failed | [V] passes | ✅ |
| 4 | Kannada vs English script | Transliterated match | [V] flagged as name difference | ❌ (safe: human checks) |
| 5 | Income proof from 2023 | "May be too old" | [V] old — income_proof | ✅ |
| 6 | Missing income proof | "Missing" | [V] missing — income_proof | ✅ |
| 7 | Random photo | "Not a recognised document" | [V] silently ignored | ❌ |
| 8 | Aadhaar visible | Masked on screen and log | [V] masked; log stores no number | ✅ |
| 9 | Unsupported certificate | "Checklist not available" | [V] argument ignored, income checklist used | ❌ |
| 10 | Empty folder | "No scans found" | [V] no crash; lists 3 missing | ⚠ partial |

## Demo Day Court
Decision: **FAIL** · NG 0 · G 7 · IE 0 (quick 7, 2 collapses open) · see `court/demo-1/verdict.md`

## Fix list (fits before code freeze)
| # | Fix | Demo impact | Hours | Owner | Do it? |
|---|---|---|---|---|---|
| 1 | Record backup video (T12) | Demo survives any failure | 1 | D | Yes |
| 2 | Pre-generate 3 Kannada TTS clips | Step 4 becomes real audio | 1 | C | Yes |
| 3 | "Not a recognised document" for unknown types | Test 7 passes | 0.5 | A | Yes |
| 4 | "Checklist not available" hand-over | Test 9 passes, safety story | 0.5 | A | Yes |
| 5 | Folder watcher (watchdog) | Step 2 automatic | 2 | A | If time |

## What we'll say about mocks
Each line must match the ladder as it is now (D3b). Mark lines that are only true after a fix.

| Line we'll say | Ladder row | True now? |
|---|---|---|
| Document reading is simulated in this demo; the check rules, masking and log are real | Readability check | yes |
| Voice is pre-recorded Kannada | Spoken Kannada | no (text only until fix 2) |
| The missed call is a recorded clip | Missed-call callback | no (clip not recorded) |
| The operator runs the check; auto-watch is next | Folder watcher | yes |
