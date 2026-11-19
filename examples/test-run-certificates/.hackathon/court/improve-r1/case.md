CASE: One trip — certificate pre-check, CORE v2
QUESTION ON TRIAL: Does this solve a real problem for its real users?
PROBLEM: Applicants for income/caste/residence certificates get rejected and must apply again from scratch, costing trips and weeks.
REAL USERS: end user = first-time or low-literacy applicant (e.g. student needing an income certificate for a scholarship) · least-digital user = elderly person who depends on the CSC operator · operator = CSC / Nadakacheri operator
SOLUTION: (1) Missed call: the system asks what the certificate is for, maps it to the certificate, reads the exact checklist aloud in Kannada, and SMSes it to a family number. (2) At the counter, the operator drags the scans they already made into a one-screen check (under 30 s): document type, readability, name match across documents, date validity, income proof vs declared band. It says "looks complete" or "possible issue, please check", never "approved", with a Kannada sentence to read aloud. The operator decides; it never blocks. Scans in memory only, Aadhaar masked. Honest scope: document-caused rejections only, not field verification or eligibility.
CONSTRAINTS: 22 h left; team = backend, frontend, AI/speech, design; no portal integration; checklist hand-entered for the Karnataka income certificate.
EVIDENCE (labelled):
  [V] Odisha e-District FAQ: rejected applications can't be revived; apply again (official, opened 19 Nov 2026)
  [V] Tumakuru district page: Karnataka income certificate "after 21 days" in person; needs income, age, address and ID proof (official, opened 19 Nov 2026)
  [V] Seva Sindhu rejection statuses include unreadable, invalid, mismatch, incomplete, Tahsildar rejection, not eligible (low-reliability guide, no frequencies)
  [?] Share of rejections caused by documents: no public data found
  [?] Operator willingness: experiments planned, not yet run
  [AI] Karnataka pushing DigiLocker storage for certificates (fetch failed)
KEY ASSUMPTIONS: [?] documents cause most rejections (collapses) · [?] operators will run the check (collapses) · [AI] check runs in under 30 s
