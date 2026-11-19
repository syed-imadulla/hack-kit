# Demo Day Court 1 — One Trip (CSC document pre-check, Karnataka)

ON TRIAL: "Does the built product, as it will be demoed, honestly prove that it solves the real problem for its real users?"
GUILTY = it does not. NOT GUILTY = it does. INSUFFICIENT EVIDENCE = can't tell from this pack.

Count a feature as working only if the ladder shows it tested ([V] measured or [T] team-run). Code existing is not evidence. A mocked feature is fine only if it's disclosed.

PROBLEM [T]: Applicants for income certificates at Karnataka CSC centres make repeat trips because documents are missing, unreadable, too old or have mismatched names. Rejected applications can't be revived; Karnataka income certificate can take up to 21 days.
USERS: applicant (e.g. Lakshmi, 19, scholarship deadline), CSC operator, Tahsildar office clerk.

FEATURE LADDER (all [V] = run and observed):
- Checklist (income certificate only): built, tested.
- Readability check: built, tested on blurry scan — BUT document reading (OCR) is MOCKED as JSON files.
- Name match: "Laxmi Kumari" vs "Lakshmi K" passes [V]; Kannada-script vs English-script name is flagged for operator instead of matched [V]. Transliteration not built.
- Date rule (365 days): tested, 2023 proof flagged.
- Kannada voice: MOCKED (text printed, no audio).
- Missed-call callback: MOCKED (planned recorded clip, not yet recorded).
- Folder watcher: NOT BUILT (operator runs the script by hand).
- Flag log: built, 3 rows written, no Aadhaar number stored. Aadhaar masked on screen.
- Never says "approved"; says "looks complete (operator decides)".

DEMO WALK: 3 of 6 steps pass; 2 manual/mocked; missed-call clip missing. Check time 0.01 s.
AI TESTS: 6 of 10 pass, 1 partial; fails: Kannada-script match (safe failure — human checks), random photo silently ignored, unsupported certificate type not handed over.
FAILURE DRILL: works offline only because online parts are mocked; backup video not recorded.
PLANNED MOCK DISCLOSURE: "Document reading is simulated; check rules, masking and log are real. Voice is pre-recorded. Missed call is a recorded clip."

OPEN "COLLAPSES" ASSUMPTIONS (2): (1) document problems cause most rejections — experiment phoning operators not yet done [?]; (2) CSC operators will add a pre-check step [?].
CLOSEST COMPETITOR: operators' own manual checklists / printed tick list; DigiLocker (fetch, not pre-check).
FIX LIST (fits before freeze): backup video, pre-generated TTS clips, unknown-document message, checklist hand-over, folder watcher if time.
