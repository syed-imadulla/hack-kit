# USERS — PDS Anna-Mitra User Profiles & Personas

> Summary: Stakeholder personas, constraints, and operational journeys for PDS Fair Price Shop transparency.

---

## 1. Primary Personas

### Persona 1: Lakshmi (Beneficiary & Household Head)
- **Age:** 48
- **Occupation:** Agricultural daily-wage labourer
- **Location:** Semi-rural taluk, Karnataka
- **Household:** 4 registered members on Ration Card (Self, husband, 2 children)
- **Card Category:** PHH (Priority Household under NFSA)
- **Technology Profile:** Basic keypad feature phone; intermittent voice reception; does not use mobile data apps or English text `[?]`.
- **Pain Points:**
  - Loses half a day's wages (₹250–₹300) every time she walks 2.5 km to the Fair Price Shop only to find the truck hasn't unloaded yet.
  - Doesn't know why some months she receives 20 kg (5 kg × 4 members under central NFSA) while other months additional state grain or DBT cash was promised under state schemes.
  - Anxious when the biometric sensor rejects her thumbprint due to worn friction ridges from manual farm labour.
- **Simulated Quote [AI]:**
  > *"I don't mind waiting 20 minutes if I get the grain. What hurts is walking 2 kilometres in the sun, waiting an hour, and being told the server is down or the grain hasn't come. I lose a day of harvesting work for nothing."*

---

### Persona 2: Basavaraj (Fair Price Shop Dealer / Operator)
- **Age:** 42
- **Role:** Sole operator of FPS No. 42 (servicing ~450 ration cards)
- **Hardware:** Government-issued Android ePOS terminal with integrated thermal printer and optical fingerprint scanner; single 4G SIM.
- **Operating Reality:**
  - 100+ beneficiaries queue up in the first week of every month during morning hours (7:30 AM – 11:00 AM) before going to work.
  - When the cellular tower experiences latency or the state food server times out, the queue stalls.
  - If he issues grain manually on paper, he risks audit deductions or accusations of black-market grain diversion during monthly inspection.
- **Simulated Quote [AI]:**
  > *"People think I am hoarding the rice. When the machine shows 'Server Timeout (Error 504)', what am I supposed to do? If I distribute on a notebook, the Food Inspector flags a stock deficit and suspends my license. If I tell them to come tomorrow, the crowd gets furious."*

---

### Persona 3: Ramesh (Food & Civil Supplies Inspector)
- **Age:** 51
- **Role:** Taluk Food Inspector auditing 55 Fair Price Shops
- **Responsibilities:**
  - Reconciling physical grain stocks against ePOS electronic closing balances at month-end.
  - Approving dealer commission allocations based on verified transaction counts.
- **Audit Constraints:**
  - Deeply sceptical of manual paper registers because historical PDS leakage occurred via fictitious paper entries.
  - Requires tamper-evident proof that any offline transaction genuinely corresponds to an eligible cardholder who collected their grain, without duplicate drawals elsewhere.
- **Simulated Quote [AI]:**
  > *"The rules say 100% biometric ePOS authentication. I know rural network towers fail. But if a dealer claims they gave out 40 bags offline on a paper ledger, how do I prove those were real families and not diverted to private flour mills? I need verifiable proof."*

---

## 2. Current vs. Desired Journey

```
CURRENT PAINFUL JOURNEY
[Beneficiary walks 2.5 km] ──▶ [Shop closed / No truck] ──▶ [Wasted Trip / Lost ₹300 wage]
         │
         ▼ (If shop open)
[Joins 40-person queue] ──▶ [ePOS Server Times Out] ──▶ [Dealer stalls queue] ──▶ [Turned away]

DESIRED INTENDED JOURNEY
[Free missed call / IVR check from home] ──▶ [Spoken Kannada: "FPS #42 grain unloaded; your quota is 20 kg free NFSA"]
         │
         ▼ (Travels with certainty)
[Direct to counter] ──▶ [ePOS Server down?] ──▶ [Local Tamper-Evident HMAC Offline Receipt logged & printed] ──▶ [Grain issued; 0 wasted trips]
```
