# SUMMARY — OPD Saathi

> Patients wait 2 hours to get 2 minutes. OPD Saathi makes those 2 hours count.

| | |
|---|---|
| Event / track | Acharya The Big Hack · Healthcare AI Agents |
| Team | Udaan (4) |
| Verdict | NOT GUILTY 9/12 (illustrative sample) |

## Problem
Patients wait hours in hospital OPDs, then get only a few minutes with the doctor. Many return the same day only to show reports.

## Solution
A patient-facing AI front desk that hospitals deploy in their OPD. Patients check in by voice on WhatsApp or a normal call, in their own language. Doctor-approved basic tests start while they wait, and reports are reviewed the same day.

## Journey
1. Token at the counter (unchanged)
2. Voice check-in; the patient's exact words are kept
3. Nurse enters vitals; fixed red-flag rules run (not AI)
4. AI suggests basic tests; an authorised doctor approves
5. Smart queue → doctor examines → prescription explained by voice

## What's built vs mocked
| Built | Mocked |
|---|---|
| WhatsApp/voice check-in, rules engine, shared OPD screen, smart queue | ABDM / FHIR export, hospital software link |

## Next steps
1. Build the phone-call path first
2. Record a backup demo
3. Rehearse "what if the AI is wrong?"
