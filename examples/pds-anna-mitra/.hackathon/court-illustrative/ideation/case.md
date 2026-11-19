# CASE — Ideation Trial: Anna-Mitra Dual-Channel Solution

## Question on Trial
Does the proposed solution, **Anna-Mitra Dual-Channel** (combining pre-travel IVR/SMS quota transparency with a cryptographically tamper-evident offline counter ledger), solve the PDS Fair Price Shop crisis for real users within civic, statutory, and operational constraints?

## Candidate Solution Under Review
1. **Pre-Travel Citizen Channel:** Free missed-call / IVR in regional languages (Kannada/Hindi) reachable via basic keypad phones. Beneficiaries hear whether the monthly foodgrain shipment has physically unloaded at their registered FPS and their exact Central NFSA entitlement (PMGKAY 35 kg AAY / 5 kg PHH free through Dec 2028) alongside active state add-on policies.
2. **Counter Outage Channel:** A lightweight dealer verification companion running locally on counter terminals during ePOS cellular/server timeouts. Uses an **HMAC-SHA256 signature and SHA-256 hash-chained append-only SQLite ledger** with physical printed receipts, allowing genuine beneficiaries to receive grain offline without queue stalls or audit ambiguity.
3. **Legal Boundary:** Explicitly distinguishes technical integrity of local receipts from statutory government transaction clearance.
