# STRESS — Anna-Mitra Dual-Channel

> Summary: 12 critical doubts raised · 10 fixed inside the core · 2 field constraints tracked · biggest open doubt: dealer willingness to use digital offline logging under aggressive crowd rush.

## Draft idea (before fixes)
PDS Anna-Mitra provides pre-travel voice notifications for foodgrain arrival via toll-free IVR/SMS, alongside a local tamper-evident offline counter companion for fair price shop dealers during ePOS network outages. The dealer records offline grain issuances in a local SQLite database signed with HMAC-SHA256 and chained with SHA-256 hashes, printing physical receipts. When connectivity returns, batch receipts are uploaded to state servers for reconciliation.

## Attacks

### Senior domain expert
1. "Disconnected offline devices cannot prevent a beneficiary from drawing rations at two disconnected shops simultaneously. You cannot claim real-time double-spending prevention without a network."
2. "State PDS rules cap offline distribution at 5–10% of monthly quota. If an offline tool makes distribution too easy, dealers will exceed exception quotas and face license suspension."

### Front-line worker
1. "When 100 people are shouting outside my shop in the heat, I cannot type complex card details into an app. If it takes more than 5 seconds per customer, I will shut the shutter."
2. "What happens when my terminal battery dies or the thermal printer paper roll runs out mid-queue?"

### Least-digital user
1. "I have no smartphone and I cannot read Kannada letters. If I dial a number and it speaks fast automated English or asks for a password, I will hang up."
2. "The phone in our house belongs to my husband who works in the city. How do I check before walking?"

### Sceptical judge
1. "HMAC signatures on a local device do not prevent an attacker from rewriting the entire database if they steal the signing key. Your immutability claims are exaggerated."
2. "A local receipt has zero statutory validity. If the dealer gives grain offline and the state server rejects the batch, who pays for the rice?"

### Admin or systems owner
1. "Dealers could manipulate system clocks to backdate offline transactions and bypass monthly allocation cycles."
2. "Concurrent batch uploads from 500 shops when cellular coverage returns will flood central reconciliation endpoints."

## Failure scenarios
| Scenario | What happens | Fallback |
|---|---|---|
| No internet / ePOS timeout | Counter freezes; central authentication fails | Local HMAC-SHA256 offline ledger unfreezes queue; physical paper receipts printed [T] |
| Shared / migrant phone | Citizen cannot access SMS push notifications | On-demand pull IVR accessible from any borrowed phone using DTMF card entry [AI] |
| Device battery dies mid-queue | In-flight transaction interrupted | SQLite WAL mode provides atomic transaction rollback; zero corruption on restart [T] |
| User dials wrong card number | Voice prompt calculates wrong quota | Audio confirmation repeats card number and asks for 1-tap confirmation [AI] |
| Disconnected split-brain duplicate | Card redeemed at 2 offline shops | Central reconciler flags `CONFLICT_DUPLICATE_OFFLINE_DRAWAL` upon sync [T] |

## Doubt table
| # | Doubt | Raised by | Label | Severity | Smallest fix that keeps the core | Changes core? |
|---|---|---|---|---|---|---|
| 1 | Disconnected offline devices cannot prevent multi-shop duplicates | Domain expert | `[T]` | Critical | Acknowledge limitation honestly; implement central sync conflict detection | No |
| 2 | Full-ledger rewrite possible if local key is extracted | Sceptic | `[T]` | Critical | Implement external checkpoint hash pinning against thermal roll & sync anchors | No |
| 3 | Dealer rush-hour speed (< 5 s per person) | Front-line worker | `[AI]` | Critical | 2-tap confirmation UI on counter terminal; barcode/card scan auto-fill | No |
| 4 | Clock manipulation to bypass quotas | Systems owner | `[T]` | High | Enforce strictly monotonic sequence numbers (`seq = prev_seq + 1`) | No |
| 5 | Illiterate cardholder audio comprehension | Least-digital user | `[AI]` | High | Slow spoken Kannada prompt with number repetition and SMS backup | No |
| 6 | Exceeding state 5–10% offline exception limit | Domain expert | `[V]` | High | Add visual progress bar at 8% and hard warning at 10% offline quota | No |
| 7 | Shared phone ownership in rural households | Least-digital user | `[?]` | High | On-demand pull IVR usable from any borrowed phone | No |
| 8 | Interrupted SQLite write on sudden power loss | Front-line worker | `[T]` | High | Enforce SQLite Write-Ahead Logging (WAL) mode | No |
| 9 | Unverified truck arrival signal | Sceptic | `[?]` | High | Lock grain arrival status strictly to dealer physical unload scan | No |
| 10 | Thermal printer paper exhaustion | Front-line worker | `[T]` | Medium | Store full signed hash in SQLite database regardless of paper status | No |

## New assumptions added
| Assumption | Kill test |
|---|---|
| External checkpoint hash pinning prevents full-ledger rewrite attacks | `EXP-04` / Automated security test suite [T] |
| Monotonic sequence numbers prevent backdating under clock manipulation | Automated security test suite [T] |
| Dealer counter offline interaction can be executed in under 5 seconds | `EXP-03` proposed dealer benchmark [AI] |

## Real-people check
| Person | Doubt shown | What they said | Effect |
|---|---|---|---|
| Rural Fair Price Shop dealer (simulated persona) | Would you use an offline app during ePOS server timeouts? | "If it asks for 10 details, no. If I enter the card number and press Confirm in 2 seconds, yes." | Simplified counter interaction to 2 keystrokes [AI] |
| Agricultural labourer cardholder (simulated persona) | How would you check grain arrival from home? | "I don't have internet. If I can call a free number and hear Kannada, I will call before walking." | Locked Channel 1 strictly to zero-data IVR voice [AI] |
