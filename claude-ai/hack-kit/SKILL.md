---
name: hack-kit
description: Use at a hackathon when problem statements or themes are given on the spot and a team wants to pick one, think as real users, validate, stress-test, put the idea on trial with a 12-juror court, plan the MVP and pitch, and get one final document. One-chat version of the Hack Kit Claude Code plugin; responds to "hack start", "hack decode", "hack pick" and the other phase names.
---

# Hack Kit (claude.ai one-chat version)

This is the chat version of the Hack Kit plugin. The team types a phase name ("hack start", "hack pick", "hack verify"...) or just pastes problem statements. Keep a running **Idea Pack** in the conversation, and if the session can make documents, keep it in one doc that you update after every phase.

## Shared rules
1. Read the brief like a judge — rubric weights decide everything.
2. Pick a problem, not a technology.
3. Think as every real user: end user, least-digital user, front-line operator, professional, manager.
4. Prove it's real: sourced numbers (open the source), real complaints, a local example, venue chats.
5. Check what already exists; never say "no competitors".
6. Stress-test by role-playing the domain expert and the sceptic, then confirm with real people.
7. Lock the core; after lock, fixes go inside the core.
8. Fit with existing systems; no new hardware.
9. Keep it simple for users: no app, no typing, simplest device.
10. AI suggests, humans decide; safety checks are fixed rules.
11. MVP = one complete journey + one wow moment; mock the rest and label it.
12. No unsourced numbers; targets labelled as targets.
13. Simple everyday English.

**Judge only whether the problem is real and the solution truly solves it for real users — never business viability, revenue or market size.**

Ask questions with the ask-user / multiple-choice tool if available (max 4 at a time); otherwise ask in plain text with numbered options. If the team is in a hurry or says "quick", use quick mode (shorter outputs, 6 jurors, 3 points per side).

## Phases
| Say | What you do | Idea Pack section |
|---|---|---|
| hack start | Ask event, rubric + weights, deliverables + limits, time left, team skills, sponsor tech. List "what judges will reward". | Brief |
| hack decode | For each statement: one-line problem, who posted it, real end user, operator, least-digital user, setting, hidden constraints, root cause, data, obvious idea vs smarter angle, MVP possibility, unknowns. Summary table. | Statements |
| hack pick | Weighted scoring table (problem real ×3, clear user ×2, fits rubric ×3, smarter angle ×2, buildable ×3, demo wow ×2, data ×1, team fit ×1), red flags, shortlist 2–3, **trial each**, recommend, captain picks. | Pick |
| hack users | Each stakeholder: today, worst step, refusals, adoption trigger, device, power to block. POV, 3–5 HMW, job story, persona, contrast motto. | Users |
| hack validate | 3 strongest sourced facts, evidence table (VERIFIED/UNVERIFIED), real voices, local example, 5-min Mom-Test venue script, notes table, unproven assumptions. | Evidence |
| hack compete | 6–10 existing solutions incl. government portals, past hackathon projects, today's workaround. Gap table (Yes/Partly/No/Not found), closest competitor, where we're weaker, coexistence levels 0–3, positioning line. | Compete |
| hack stress | Role-play domain expert, front-line worker, least-digital user, sceptical judge, admin. Fix table: doubt, who, severity, smallest fix inside the core, changes core Y/N. Team accepts fixes. | Stress |
| hack lock | Name, motto, positioning, problem + number, persona before/after, end-to-end journey table, who does what, 4–6 USPs, AI vs rules vs humans table, inclusion, systems fit, privacy, out of scope. Confirm → LOCKED. | Core |
| hack plan | One journey + wow moment, build/mock/cut, stack with why + fallback, layered architecture (Mermaid), hour plan, freeze times, 90-sec demo script, backup plan, 8–12 AI test cases. | Plan |
| hack verify | **Trial the solution**, rubric score /100, mistakes check, claims check (sourced/target/unsourced), ranked fixes. | Verdict |
| hack pitch | One-line pitch, opening line, deck outline within slide limit (default 7), form answers, 12–15 judge Q&A. | Pitch |
| hack ship | One-page summary + the full Idea Pack as one document (export to PDF if the session can). | Final |
| hack status | Phase checklist, what's locked, next phase. | — |
| hack help | List all phases and the quick start. | — |
| hack court <thing> | Trial anything. | — |

## The trial (simulated jury in one chat)
Print first: *"Simulated jury in one chat — less independent than the Claude Code version, which uses separate subagents."*

1. **Case file** (~120 words): problem, real users, solution, constraints.
2. **Prosecution:** 5 points (3 in quick) that it does NOT solve a real problem for its real users. No business arguments.
3. **Defense:** 5 points (3 in quick) that it does. No business arguments.
4. **Jury:** voice each juror separately, judging only from their own lens, and give each a JSON line:
   `{"juror": "...", "vote": "GUILTY|NOT GUILTY", "confidence": 1-10, "reason": "...", "fix": "..."}`
   Jurors (quick mode = ★ only):
   1. ★ Actual end user
   2. ★ Least-digital user (elderly, keypad phone, regional language)
   3. ★ Front-line worker who operates it
   4. ★ Domain professional (match to statement)
   5. Person using today's workaround
   6. ★ Root-cause analyst
   7. "Already exists" researcher
   8. Safety and ethics reviewer
   9. Systems person (fit with existing systems)
   10. ★ Engineer (buildable and demo-able in time)
   11. Statement-owner judge (answers what was asked?)
   12. Sceptic (does it really matter, to how many?)

   GUILTY = "It does not solve a real problem for its real users as described."
5. **Judge:** count votes (tie = HUNG JURY), average confidence, ratings /10 (problem real, problem matters, fits root cause, works for real users, fits existing systems, safe, buildable/demo-able, different), top 3 fail reasons, top 3 fixes inside the core, a 30-minute venue check with pass/fail, and "If I were your team…".

## Mistakes to block (warn immediately)
Tech-first idea · new app/hardware/typing needed · least-digital user ignored · AI deciding safety alone · "no competitors" · unsourced numbers or targets shown as results · feature creep after lock · many half-features instead of one journey · demo with no offline backup · heavy-text slides or over the slide limit.
