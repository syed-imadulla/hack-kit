# CORE — OPD Saathi

> LOCKED (example)

## 1. Name and motto
**OPD Saathi.** Patients wait 2 hours to get 2 minutes. OPD Saathi makes those 2 hours count.

## 2. Positioning line
A patient-facing AI front desk that hospitals deploy in their OPD. It works alongside the hospital's own software, with no app and no new hardware.

## 3. Problem
Patients wait hours in hospital OPDs, then get only a few minutes with the doctor. Many come back the same day only to show reports.

## 4. Persona story — Ramesh uncle (58, diabetic, keypad phone, Kannada)
| Before | After |
|---|---|
| Waits from 8 am with no idea when his turn is | Gets token, checks in by voice call in Kannada |
| Explains symptoms in a rush in 2 minutes | His exact words are already on the doctor's screen, marked "patient-reported" |
| Sent for tests, waits again, comes back another day | Doctor-approved basic tests done while he waits; same-day review |
| Forgets medicine instructions | Prescription explained by voice in Kannada |

## 5. End-to-end journey
| # | Who acts | Channel | System does | Human decides |
|---|---|---|---|---|
| 1 | Patient | Counter | Normal token (unchanged) | — |
| 2 | Patient | WhatsApp QR or phone call | Voice check-in, keeps exact words | — |
| 3 | Nurse | Shared OPD screen | Vitals entered by token | Nurse |
| 4 | Rules engine | — | Hospital-approved red-flag rules (not AI) | Nurse clears alert |
| 5 | AI | — | Suggests basic tests with reasons | Authorised doctor approves/edits/rejects |
| 6 | System | — | Checks lab wait vs OPD wait; smart queue | — |
| 7 | Doctor | Case sheet | Examines, writes in hospital format | Doctor |
| 8 | Doctor → patient | One tap → voice | Follow-up choice; prescription explained | Doctor |

## 6. Who does what
| Role | Does | Never has to |
|---|---|---|
| Patient | Talks in own language | Download an app or type |
| Nurse | Enters vitals, clears alerts | Re-type patient history |
| Doctor | Approves tests, examines, writes case sheet | Accept AI output without review |

## 7. USPs
1. No app, no typing — WhatsApp voice or a normal call.
2. Patient's exact words kept, never rewritten.
3. Tests started while waiting, only after doctor approval.
4. Same-day report review, same doctor.
5. Danger checks are fixed rules, not AI.
6. Works standalone with only a token number.

## 8. AI vs rules vs humans
| Step | AI does | Fixed rules do | Human decides | If AI fails |
|---|---|---|---|---|
| Check-in | Understands speech | — | — | Nurse/counter entry |
| Red flags | — | Flags danger signs | Nurse clears | Rules still run |
| Tests | Suggests with reasons | — | Doctor approves | Normal OPD flow |

## 9. Inclusion
No phone → family phone or counter/nurse entry.

## 10. Fit with existing systems
Level 0 token only → Level 1 ABHA Scan & Share → Level 2 FHIR export → Level 3 hospital software agreement.

## 11. Privacy
Audio deleted within 72 h. The hospital record is the official one.

## 12. Out of scope
Diagnosis, prescribing, emergency triage, filling the case sheet.
