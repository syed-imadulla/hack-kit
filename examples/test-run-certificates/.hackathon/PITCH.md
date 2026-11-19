# PITCH — One trip

> Summary: "Find out what's wrong with your certificate application before you submit, not 21 days later." · 6 slides · 4-min pitch

## One-liners
- **One-line pitch:** One trip tells certificate applicants what's missing before they submit, spoken in Kannada at the counter.
- **Opening line (Problem 25% + Innovation 25%):** "In Odisha, a rejected certificate application can't be revived. You start again. We move the moment of truth from 21 days later to the counter."
- **Motto:** One trip, not three.

## Deck outline (stay within the slide limit)
| # | Headline (full sentence) | 3–5 short items | Visual | Source line |
|---|---|---|---|---|
| 1 | A rejected application means starting again, and losing weeks | Lakshmi, 19 · scholarship deadline · 21 days | Persona + timeline | Odisha e-District FAQ; tumkur.nic.in |
| 2 | Applicants only find out what was wrong after the rejection | Status after review · English guides · repeat trips | Before/after timeline | CitizenNest (low reliability) |
| 3 | One trip checks documents at the counter, before submission | Existing scans · 30 s target · spoken Kannada · never "approved" | Operator screen mock | — |
| 4 | Live: a name mismatch caught and explained aloud | Clean / blurry / mismatch | Demo | — |
| 5 | Built safely: the operator decides, nothing is stored | Flags only · log · Aadhaar masked · fallbacks | Architecture | — |
| 6 | What we tested, what we haven't, and what's next | Experiment results · eligibility warning · DigiLocker L1 | Assumptions table | — |

Rules: no heavy text · readable fonts · only [V]/[T] claims stated as facts · "under 30 s" shown as a target.

## Form answers
| Question | Word limit | Answer |
|---|---|---|
| What problem are you solving? | 150 | Certificate applications for income, caste and residence are often rejected for document problems, and a rejected application must be filed again from scratch (Odisha e-District FAQ). In Karnataka an income certificate can take up to 21 days in person, so one missing paper can cost a student a scholarship deadline. Applicants learn what was wrong only after the rejection, usually in English and online. We help the people who rely on a CSC operator, and who can't read the rejection reason, find out at the counter, before submission. |
| What is innovative? | 150 | Checklists already exist; what doesn't exist is a check at the moment of submission, spoken in the applicant's language. One trip runs on the scans the operator already makes, flags missing, unreadable or mismatched documents in under 30 seconds (target), and plays a Kannada explanation. It never approves anything: the operator decides, every flag is logged, and scans are never stored. |

## Judge Q&A
| Question | Answer (2–3 lines) |
|---|---|
| How many rejections are document problems? | We found no public data. We asked operators (experiment 1): [result]. If it's low, our eligibility warning covers the next biggest cause. |
| What if the AI is wrong? | It only flags; the operator confirms every flag. It never says "approved". Wrong flags are logged so we can measure them. |
| Doesn't DigiLocker solve this? | For documents already in DigiLocker, partly. Self-declarations and new documents aren't there, and we add DigiLocker fetch as level 1. |
| Why would operators use it? | It runs on the folder they already save scans to: no extra clicks. Fewer angry repeat customers. Experiment 2: [result]. |
| What did you build vs mock? | Built: folder watcher, checks, operator screen, Kannada TTS, flag log. Mocked: the missed-call line and SMS. |
| How does a person who can't read use it? | The operator plays the Kannada sentence aloud; before the visit, a missed call reads the checklist. |
| What about privacy? | Scans are processed in memory and never stored; Aadhaar numbers are masked on screen and in logs. |
| Isn't this just OCR? | The OCR is a commodity. The difference is when the check happens (before submission) and who it serves (non-readers, through the operator). |
