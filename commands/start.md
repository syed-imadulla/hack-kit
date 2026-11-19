---
description: Set up a hackathon project and read the brief like a judge (rubric, rules, deliverables, team, time)
argument-hint: "[event name] [--quick]"
---

# /hack:start

Follow the shared rules in the `hack-kit` skill (`${CLAUDE_PLUGIN_ROOT}/skills/hack-kit/SKILL.md`). Read it now if it isn't loaded.

Arguments: $ARGUMENTS

## Goal
Create `.hackathon/` and capture everything about the event that will decide what wins.

## Steps
1. If `.hackathon/STATE.md` already exists, show the current phase and ask: continue, or start a new event (rename old folder to `.hackathon-old-<date>/`)?
2. Create `.hackathon/` and `.hackathon/court/`.
3. Ask the team (AskUserQuestion, max 4 at a time; let them paste text or attach the brief):
   - Event name, organiser, track(s) or theme.
   - **Judging rubric and weights.** If they don't know, ask them to paste the brief/website text; if still unknown, use a default (Problem 25, Innovation 20, Feasibility 20, Impact 20, Presentation 15) and mark it `ASSUMED`.
   - Deliverables and limits: slides (max count?), video, repo, form questions, demo length, deadline with time zone.
   - Time left until submission / judging.
   - Team: names, roles, skills (frontend, backend, AI, design, pitch, domain).
   - Sponsor tech or required tools (bonus points?).
   - Rules: allowed pre-built code, data, APIs, team size.
4. If they gave a link to the brief, fetch it with WebFetch and extract the rubric, rules and deliverables. Show what you extracted and ask them to confirm.
5. Write `.hackathon/BRIEF.md` using `${CLAUDE_PLUGIN_ROOT}/templates/brief.md`. Add a **"What judges will reward"** section: the top 3 rubric items in plain words and what that means for idea choice.
6. Write `.hackathon/STATE.md` using `${CLAUDE_PLUGIN_ROOT}/templates/state.md`. Set mode (`quick` if `--quick` or under 12 h total), the planned freeze times (idea freeze ≈ 1.5 h after statements; code freeze 3–4 h before judging), and the captain (the final decider).
7. Show a 5-line summary and say: **Next: `/hack:decode` — paste the problem statements.**
