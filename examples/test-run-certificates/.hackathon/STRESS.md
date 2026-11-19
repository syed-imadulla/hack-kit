# STRESS — One trip

> Summary: 14 doubts raised (4 high, 6 medium, 4 low) · biggest open doubt: whether documents cause most rejections · 2 new assumptions

## Draft idea (before fixes)
See CORE.md v1: a missed-call Kannada checklist, plus a 30-second operator check on existing scans. It flags, never blocks, and the operator decides.

## Attacks
### Senior domain expert (Tahsildar office clerk, simulated)
1. [AI] "Most of our rejections are field verification: income declared doesn't match the village accountant's report. Your tool can't see that." (high)
2. [AI] "Self-declarations are judged, not checked. A pre-check can't tell if the declared income is believable." (medium)
3. [AI] "Who's liable if your tool says 'all clear' and we reject?" (medium)
4. [AI] "Checklists change by notification; who updates yours?" (medium)

### Front-line worker (CSC operator, simulated)
5. [AI] "My scans are PDFs from the scanner software; where do they go?" (medium)
6. [AI] "If it's slow at rush hour, I'll stop using it." (high)
7. [AI] "Customers will blame me if your tool was wrong." (medium)

### Least-digital user (simulated)
8. [AI] "I don't know the certificate's name. I just know the college asked for 'the income paper'." (medium)
9. [AI] "A missed call costs nothing, but will a machine voice call me back? I might not pick up an unknown number." (low)

### Sceptical judge (simulated)
10. [?] "Where's your data that documents cause rejections?" (high)
11. [AI] "Karnataka is pushing DigiLocker. Won't this be obsolete?" (medium)
12. [AI] "Isn't this just a checklist with OCR?" (low)

### Admin or systems owner (simulated)
13. [AI] "Aadhaar images on your server is a privacy problem." (high → covered by in-memory processing, but must be shown)
14. [AI] "You can't be on our portal, so how do operators trust it?" (low)

## Failure scenarios
| Scenario | What happens | Fallback |
|---|---|---|
| No internet | Check can't run | Offline checklist card + manual tick list on screen |
| API down (speech/OCR) | No classification or voice | Text checklist; operator ticks manually |
| Wrong AI answer | False "all clear" or false flag | Flag-only design; the operator confirms every flag; show confidence |
| User gives up halfway | Missed call not returned | SMS the checklist link to a family member's number |

## Doubt table
| # | Doubt | Raised by | Label | Severity | Smallest fix that keeps the core | Changes core? |
|---|---|---|---|---|---|---|
| 1 | Field verification causes many rejections; out of reach | Domain expert | [AI] | high | Say so openly; scope claims to "document-caused rejections"; check "income proof matches declared income" consistency | N |
| 6 | Too slow at rush hour | Operator | [AI] | high | A drag-and-drop folder of existing scans; target under 30 s; manual-tick fallback | N |
| 10 | No rejection data | Judge | [?] | high | Run experiment 1; present it as a hypothesis | N |
| 13 | Aadhaar privacy | Admin | [AI] | high | In-memory only; mask numbers; show this in the demo | N |
| 8 | Applicant doesn't know the certificate name | Least-digital user | [AI] | medium | Ask "What is it for?" (scholarship, job, scheme) and map it to the certificate | N |
| 4 | Checklists change | Domain expert | [AI] | medium | Checklist as a config file with a "last checked" date | N |
| 7 | Blame when the tool is wrong | Operator | [AI] | medium | Wording: "possible issue, please check", never "approved" | N |
| 11 | DigiLocker makes it obsolete | Judge | [AI] | medium | L1: fetch from DigiLocker when available; the check still covers self-declarations and new documents | N |
| 12 | "Just OCR" | Judge | [AI] | low | Pitch the moment and the spoken explanation, not the OCR | N |

(Fixes are applied with the team in `/hack:improve`.)

## New assumptions added
| Assumption | Kill test |
|---|---|
| Applicants can name the purpose ("for scholarship") even if not the certificate | weakens |
| The check runs in under 30 s on existing scans | weakens |

## Real-people check
| Person | Doubt shown | What they said | Effect |
|---|---|---|---|
| *(none — test run)* | | | |
