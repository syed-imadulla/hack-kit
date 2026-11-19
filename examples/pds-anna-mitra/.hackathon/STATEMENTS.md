# STATEMENTS — Problem Selection & Decode

> Summary: Problem statement selection and deconstruction for Public Distribution System Fair Price Shop resilience.

## 1. Candidate Problem Statements

### S1: Fair Price Shop Quota Uncertainty & ePOS Outage Queue Stall (Selected)
- **Problem Statement:** Beneficiaries under the Public Distribution System (PDS) face wasted trips, long queues, and quota confusion at Fair Price Shops (FPS) because grain truck deliveries arrive unpredictably, central vs state entitlements are poorly understood, and ePOS biometric/cellular timeouts stall distribution lines.
- **Why Selected:** Affects millions of daily-wage households; combines information asymmetry (citizens walking to closed shops) with engineering failure (network-dependent ePOS machines stalling queues); clear tension between statutory rules and frontline operations.

### S2: One Nation One Ration Card (ONORC) Portability Friction for Migrant Workers
- **Problem Statement:** Inter-state and intra-state seasonal migrant labourers struggle to claim partial monthly grain entitlements at destination fair price shops due to dealer unfamiliarity with biometric portability guidelines and fear of local quota depletion.
- **Why Deprioritized:** Complex multi-state godown allocation rules and inter-state reconciliation infrastructure make building a testable local prototype in a 24-hour hackathon unrealistic without live state API access.

### S3: PDS Subsidized Pulse and Kerosene Leakage at Dealer Level
- **Problem Statement:** Discrepancies between physical stock of non-grain items (pulses, sugar, kerosene) received at the FPS and distributed quantities lead to disputes between vigilance committees and dealers.
- **Why Deprioritized:** Narrower scope; overlaps with basic retail inventory management without addressing the core beneficiary journey of food security.

---

## 2. Deep Dive: Deconstructing Statement S1

### 2.1 The Two Parallel Failures
1. **The Pre-Trip Information Gap:**
   - Beneficiaries walk or take shared autos to Fair Price Shops without knowing if:
     - The current month's grain delivery has physically arrived and been unloaded.
     - The shop is open today.
     - Their exact entitlement under Central NFSA (PMGKAY free grain through Dec 2028) vs the currently active state add-on scheme.
   - Result: Wasted trips, lost wages (half-day daily wage loss for agricultural labourers).
2. **The Counter Outage Stall:**
   - ePOS terminals require real-time cellular data to connect to state PDS servers and the central Aadhaar authentication gateway.
   - When server latency exceeds threshold or cellular towers flap, transactions fail.
   - Dealers either:
     - Stall the queue indefinitely while tempers flare,
     - Turn beneficiaries away,
     - Or resort to manual paper registers (which state auditors view with suspicion of diversion).

### 2.2 Root Causes vs. Symptoms

| Observed Symptom | Surface Diagnosis | Actual Root Cause (Evidence-Backed) |
|---|---|---|
| Crowds waiting outside closed FPS on the 3rd of the month. | "Dealers are lazy or hoard grains." | Logistics delivery lag: Godown truck schedules are unannounced; stock arrives in batches throughout the 1st–10th `[?]` (needs taluk audit). |
| Beneficiary argues with dealer over whether they get 25 kg or 35 kg. | "Beneficiaries don't understand math." | Opacity between Central NFSA (5 kg/member for PHH) and state add-on policy shifts (cash DBT vs grain add-on) `[V]`. |
| Queue frozen for 45 minutes inside the shop. | "ePOS machine is broken." | Cellular tower congestion and central authentication server timeouts under synchronous blocking architecture `[?]`. |
| Dealers turn people away rather than give manual grain. | "Dealers are unhelpful." | Dealers fear reconciliation penalties: unverified manual paper register entries risk being flagged as diversion during food inspection audits `[AI]`. |

### 2.3 Regulatory & Operational Boundaries

1. **Central Statutory Entitlements [V]:**
   - Central NFSA provides 35 kg fixed for AAY households and 5 kg per person for PHH households.
   - PMGKAY makes this grain free of cost through 31 December 2028.
   - PHH eligibility is determined by State Governments under Section 10, distinct from historical BPL surveys.
2. **State Policy Discretion [V]:**
   - States (e.g. Karnataka 2026–27) may add supplemental rice, pulses, sugar, or cash-transfer DBT.
   - These are variable, date-dependent, and constrained by annual fiscal allocations.
3. **Cryptographic & Technical Bounds [T]:**
   - An offline ledger using HMAC-SHA256 signatures and SHA-256 hash chaining can guarantee local tamper evidence against retroactive alteration.
   - It does **not** provide statutory government authorization. Statutory clearance legally requires central state ePOS server acceptance.
