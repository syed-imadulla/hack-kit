# Demo Day Court 1 — PDS Anna-Mitra (offline ration-shop counter)

ON TRIAL: "Does the built product, as it will be demoed, honestly prove that it solves the real problem for its real users?"
GUILTY = it does not. NOT GUILTY = it does. INSUFFICIENT EVIDENCE = can't tell from this pack.

Count a feature as working only if the ladder shows it tested ([V] measured or [T] team-run). Code existing is not evidence. A mocked feature is fine only if it's disclosed.

PROBLEM [T]: Ration-card holders in rural Karnataka make wasted trips to Fair Price Shops: stock hasn't arrived, the ePOS/biometric network is down, or they don't know their free quota and get overcharged.
USERS: beneficiary (e.g. Kenchaiah, keypad phone, Kannada), shop dealer, taluk food inspector.

FEATURE LADDER (all [V] = run and observed by the reviewer on 19 Nov 2026):
- Entitlement engine: PHH card with 4 members → 20 kg rice free, dal 1 kg at Rs 25 [V]. Matches NFSA 5 kg/member.
- Offline 2-tap dispense: works with no network; signed receipt printed [V]; record time median 0.04 ms, max 1.6 ms over 20 runs [V].
- Tamper audit: editing a stored transaction is caught by verify-chain ("hash mismatch at row 1") [V].
- 28 automated tests pass [V].
- Kannada voice line: Kannada TEXT script printed; no audio is produced [V]. DEMO.md calls it "Real (local audio synthesizer text)".
- Phone IVR line: MOCKED (no telephony), disclosed.
- Biometric scanner and thermal printer: MOCKED (terminal receipt), disclosed.
- FOUND IN TESTING [V]: the same card can be dispensed again and again in the same month at the same shop: 20 repeat dispenses of the same card were all accepted. Only cross-shop duplicates are flagged afterwards by "reconcile".
- FOUND IN TESTING [V]: dispense with --custom-rice 500 printed a receipt for 500 kg rice "100% FREE" (25x the quota); no limit check.
- Backup demo video: DEMO.md says recorded and "verified playable", but no video file exists in the project [?].

DEMO WALK (team's DEMO.md): 5 of 5 steps pass [V reproduced: quota, dispense, verify-chain, tamper drill].
OPEN "COLLAPSES" ASSUMPTIONS (3) [?]: A1 wasted trips are mainly caused by stock-arrival lag; A2 keypad-phone users will dial an IVR before travelling; A7 dealers will adopt the offline counter.
CLOSEST EXISTING: state "Mera Ration" app, Ahara portal (Karnataka), paper registers during outages.
PLANNED MOCK DISCLOSURE: "Telephony, biometric scanner and thermal printer are mocked; ledger, rules and audit are real."
