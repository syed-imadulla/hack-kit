CASE: S2 — repeat visits for government certificates
QUESTION ON TRIAL: Is this problem real and worth solving here, and can this team solve it for its real users in the time?
PROBLEM: Citizens applying for income, caste and residence certificates often get rejected for missing or mismatched documents and must apply and visit again.
REAL USERS: end user = low-literacy citizen (student, farmer) · least-digital user = elderly person who depends on the CSC operator · operator = CSC / e-Mitra / Seva Sindhu operator
SOLUTION (rough direction): Before submission, the citizen or operator photographs each document; the tool checks document type, name match with Aadhaar, date validity and the state's checklist, and explains what's missing in Kannada or Hindi.
CONSTRAINTS: 23 h left; team = backend, frontend, AI (LLM + speech), design/pitch; rubric top items Problem 25, Innovation 25, Feasibility 20; state e-District portals differ and can't be integrated in 24 h.
EVIDENCE (labelled):
  [V] Odisha's official e-District FAQ: a rejected application can't be revived. "You will have to apply again after completing the documents procedure." (edistrictapp.odisha.gov.in/fr/faq, opened 19 Nov 2026)
  [V] An independent guide (CitizenNest, low reliability, no frequency data) lists Seva Sindhu rejection statuses: document not readable, invalid document, details mismatch, incomplete application, rejected by Tahsildar (field verification), not eligible. For income certificates: declared income not matching proof, missing agricultural income documents. (opened 19 Nov 2026)
  [AI] Several of these causes (unreadable or invalid documents, mismatches, missing documents) are catchable before submission; Tahsildar field verification and eligibility are not
  [?] Share of rejections caused by documents vs officer discretion
  [?] Whether CSC operators would add a pre-check step
KEY ASSUMPTIONS: [?] document problems cause most rejections · [?] operators will use a pre-check · [AI] document photos can be checked reliably by AI
