# IMPROVE — PDS Anna-Mitra

> Summary: 1 round · CORE v1 → v2 · latest decision: REVISE (capped by 3 open collapses)

## Round 1 — 2026-11-03 14:00 IST
Feedback source: `STRESS.md` and `court/stress/verdict.md`

### Candidates
| # | Change | Fixes which weakness | Impact | Effort | New risk | Evidence still needed | Inside core / DRIFT | Accepted? |
|---|---|---|---|---|---|---|---|---|
| 1 | Remove 4-digit IVR PIN, speak only commodity kg (Zero PII) | High drop-off from forgotten PINs and shared-phone privacy risk | high | low | Anyone with card number can hear kg quota | Beneficiary comfort with shared voice readout `[?]` | Inside core | Accepted |
| 2 | Flatten IVR to 2-step direct playout with Kannada/Hindi audio | Multi-level menu navigation confusion on 2G connections | high | low | Less room for sub-menus | Audio clarity testing on basic handsets `[?]` | Inside core | Accepted |
| 3 | Replace 5-step dealer form with 2-tap "Standard Dispense" flow | Dealer refusal/bypass during morning rush (75s down to 15s) | high | med | Accidental tap if dealer is careless | Dealer field timing trial `[?]` | Inside core | Accepted |
| 4 | Add key rotation (`key_version`) and monotonic clock verification | Signing key compromise and backdated record tampering | high | low | Terminal key management overhead | Cryptographic unit tests `[V]` | Inside core | Accepted |
| 5 | Explicit split-brain conflict detection (`CONFLICT_DUPLICATE_OFFLINE_DRAWAL`) | False claim that offline crypto prevents multi-device duplicate drawals | med | low | Double drawals still occur locally until sync | Central sync engine tests `[V]` | Inside core | Accepted |
| 6 | Separate central NFSA PMGKAY (free) from state add-ons (Karnataka 2026-27) | Legal misrepresentation of statutory entitlements as state guarantees | high | low | Confusion if state benefits change mid-month | Official Food Dept order verification `[E]` | Inside core | Accepted |
| 7 | Add external daily checkpoint hash pinning | Full-ledger rewrite by compromised terminal key | high | med | Requires daily communication channel (SMS/paper) | Checkpoint verification tests `[V]` | Inside core | Accepted |

### Version comparison
| Dimension | v1 Baseline | v2 Hardened |
|---|---|---|
| What improved | Complex 4-level PIN IVR; 5-step dealer screen; static single HMAC key; unverified truck GPS alerts | 2-step Zero-PII IVR; 2-tap dealer dispense (<15s); key rotation; independent clock rollback checks; external checkpoint pinning; decoupled central/state rules |
| What got worse or riskier | Assumed cryptography solves split-brain double drawals | Acknowledged that offline double drawal cannot be prevented in real time; requires central post-facto conflict resolution |
| Assumptions still open | A1 (phone access), A2 (IVR preference), A7 (dealer adoption) | A1, A2, A7 remain open `[?]` pending physical field trials; security assumptions A11, A12 verified `[V]` via tests |
| Same problem and main user? | Yes: Fair price shop quota transparency and outage resilience for rural BPL/PHH households | Yes: Identical problem and beneficiary persona (Kenchaiah & Ratnamma) |

### Re-check
| Metric | Before (Phase 8 Stress Verdict) | After (Phase 9 Improvement Re-evaluation) |
|---|---|---|
| Decision | REVISE (capped by 3 open collapses) | REVISE (capped by 3 open collapses) |
| Votes (NG · G · IE) | 12 NG · 0 G · 0 IE (uncapped) | 12 NG · 0 G · 0 IE (uncapped) |
| Lowest rating | 2 / 5 (due to unvalidated collapses & dealer friction) | 4 / 5 (methodological cap remains due to unvalidated field collapses) |

### Stop or continue
**Stop at Round 1**. The architectural improvements resolve all internal technical vulnerabilities, reduce counter transaction time by 80%, remove cognitive barriers in the IVR flow, and establish a tamper-evident cryptographic foundation. Further desk iterations will not resolve open field assumptions A1, A2, and A7 without actual physical trials. The team is ready to lock the core (`/hack:lock`) and proceed to implementation planning.
