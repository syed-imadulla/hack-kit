---
description: Compile everything in .hackathon/ into one final document — FINAL.md, FINAL.html and FINAL.pdf
argument-hint: "[pdf|md|both]"
---

# /hack:ship

Follow the `hack-kit` skill rules. Read STATE.md first.

Arguments: $ARGUMENTS

## Step 1 — Check completeness
List which files exist in `.hackathon/`. If CORE.md, PLAN.md or PITCH.md is missing, warn and ask (AskUserQuestion): "Compile anyway" / "Run the missing command first".

## Step 2 — Ask format
If not given in arguments, ask: PDF, Markdown, or both (default both).

## Step 3 — Executive summary
Write `.hackathon/SUMMARY.md` (one page): name, motto, problem (2 lines + top number with source), solution (3 lines), journey (5 steps), verdict (x/12, top ratings), MVP scope (built vs mocked), team and roles, next steps.

## Step 4 — Compile
Run:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/compile.py" .hackathon
```
The script joins the files in this order: SUMMARY, BRIEF, STATEMENTS, PICK-VERDICT, USERS, EVIDENCE, COMPETE, STRESS, CORE, PLAN, VERDICT, PITCH — skipping missing ones — into `.hackathon/FINAL.md` and `.hackathon/FINAL.html`, then tries to make `.hackathon/FINAL.pdf` (pandoc → Chromium/Chrome headless → Playwright). If no PDF tool works, it says so; then tell the user to open FINAL.html in a browser and Print → Save as PDF.

If python3 is missing, build FINAL.md yourself by concatenating the files in that order with a page-break line (`<div style="page-break-after:always"></div>`) between them.

## Step 5 — Check
Open/inspect the result: page count, every section present, no broken tables. Fix and re-run if needed.

## Step 6 — Finish
Update STATE.md (phase = shipped). Tell the user where the files are, and the 3 things to do next (e.g. build the demo journey, record backup video, rehearse Q&A).
