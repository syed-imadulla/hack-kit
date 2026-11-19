# COMPETE — One trip (certificate pre-check)

> Summary: closest competitor: Seva Sindhu + DigiLocker (state portal) · our honest difference: we check documents **before** submission and explain gaps aloud in Kannada; portals only show the rejection reason **after** about 7–21 days

## Existing solutions
| # | Name | Type | What it does | Link | Still active? |
|---|---|---|---|---|---|
| 1 | Seva Sindhu / Nadakacheri | Government portal | Apply for and track certificates; shows the rejection reason after review | sevasindhu.karnataka.gov.in | Yes [AI] (guides, not opened) |
| 2 | DigiLocker integration | Government | Fetches existing certificates and IDs; Karnataka reportedly mandating DigiLocker storage for all certificates | [Elets, Oct 2026](https://egov.eletsonline.com/?p=107175) (fetch failed → [AI]) | Expanding [AI] |
| 3 | Doorstep delivery (Janasevaka-style) | Government | Agents collect documents at home and apply | GKToday snippet | Yes [AI] |
| 4 | Paid private agents (e.g. NammaDocs) | Private | File on Seva Sindhu for a fee (search snippet shows Rs 600 vs a ~Rs 35 portal fee) | jadudesk.pages.dev snippet | Yes [AI] |
| 5 | CitizenNest-style guides | Websites | Explain rejection reasons and checklists in English | citizennest.com (opened) | Yes [V] |
| 6 | Today's workaround | Workaround | Ask the operator or a relative; guess; re-apply | — | — |

## What exists, what it fails to solve, what remains
- **Exists:** online application, status tracking, DigiLocker for already-issued documents, doorstep agents, English guides.
- **Fails to solve (for the user):** nobody checks the documents **before** submission, and the reason arrives only after rejection, days later. Guides are in English and aimed at people who read.
- **Opportunity left:** a check at the moment of submission, spoken in Kannada, using the scans the operator already makes.

## Differentiation statement (user value, not technology)
"Today, you find out what was wrong after about 7–21 days, and then you start again. One trip tells you at the counter, in your language, before you submit."

> Different technology isn't innovation. Our OCR isn't the difference; *the moment* of the check is.

## Gap table
| What matters to the user | Our idea | Seva Sindhu portal | DigiLocker | Private agent | Today's workaround |
|---|---|---|---|---|---|
| Knows what's missing before submitting | Yes | No | Partly (only for docs already in DigiLocker) | Partly | No |
| Works without an app or reading | Yes (operator + call) | No | No | Yes | Partly |
| In Kannada, spoken | Yes | Partly (Kannada UI, not spoken) | No | Partly | Yes |
| Cost to the applicant | Free | ~Rs 35 fee | Free | Rs 600+ [AI] | Bus fare per trip |
| Fits the existing system | Yes (in front of the portal) | — | Yes | Yes | — |
| Human check on AI | Yes (flags only) | n/a | n/a | n/a | n/a |

Yes / Partly / No / Not found.
*Not found = not seen in public material, not proof it doesn't exist.*

## Closest competitor and honest difference
**DigiLocker integration.** If every document is already in DigiLocker, mismatches drop. Our honest difference: many applicants (farm labourers, first-time students) don't have the right documents in DigiLocker yet [AI], and self-declarations and income proof aren't there.

## Where we are weaker
- No data on how often rejections happen ([?]).
- No access to the real portal; we sit outside it.
- If Karnataka's DigiLocker push succeeds, part of the problem shrinks.

## Coexistence levels
- Level 0: standalone checklist line + operator check on scans (no integration).
- Level 1: fetch documents from DigiLocker with the citizen's consent.
- Level 2: export a "ready-to-submit" summary the operator attaches.
- Level 3: built into Seva Sindhu as a pre-submission step (by agreement).

## Positioning line
For first-time and low-literacy applicants who lose trips to rejected certificate applications, One trip is a counter-side pre-check that tells them what's missing before they submit. Unlike the state portal, which explains rejections days later, we explain gaps on the spot, aloud, in Kannada.
