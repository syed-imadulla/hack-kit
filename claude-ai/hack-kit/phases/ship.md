> **Claude app note:** this file comes from the Hack Kit plugin. `.hackathon/<FILE>.md` means that section of the Idea Pack (or a real file if this session has file tools). Templates are in `templates/`. Where it says to launch subagents, simulate them one after another in this chat and say so. The plugin's Python scripts aren't included here: when a step says to run one, apply the same rules by hand.

# /hack:ship — One Idea Pack

> **Phase 14 of 14** · Reads: everything · Writes: `SUMMARY.md`, `FINAL.md`, `FINAL.html`, `FINAL.pdf` · Next: build and rehearse

## Before you start
Load the `hack-kit` skill rules. Read `.hackathon/STATE.md`.

## Goal
One document that tells the whole story: the problem, what was explored and rejected, the evidence, the challenges, the improvements, the locked idea, the plan and the pitch. Share it with mentors and teammates, or attach it to a submission.

## Steps

### 1. Check what's there
List the files in `.hackathon/`. If CORE.md, PLAN.md or PITCH.md is missing, ask (AskUserQuestion):
- **Compile anyway**
- **Run the missing command first**

### 2. Format
If the arguments don't say, ask:
- PDF, Markdown, or both (the default is both);
- **Full pack** (every file, often 25–35 pages) or **brief pack** (`--brief`: SUMMARY, CORE, ASSUMPTIONS, PLAN, VERDICT, PITCH, about 10 pages, best for mentors and judges). The default is both.

### 3. One-page summary
Write `.hackathon/SUMMARY.md` from `templates/summary.md`, covering:
- name and motto;
- the problem, with its top sourced number;
- the solution in 3 lines;
- the journey in 5 steps;
- the latest decision and top ratings;
- open "collapses" assumptions, if any;
- what's built and what's mocked;
- the team;
- next steps.

### 4. Compile
```bash
python3 "<plugin>/scripts/compile.py" .hackathon            # full pack → FINAL.*
python3 "<plugin>/scripts/compile.py" .hackathon --brief    # brief pack → BRIEF.*
# add --md-only for no PDF
```
If `${CLAUDE_PLUGIN_ROOT}` isn't set in the shell, use the plugin root found as described in the skill.

The script:
- joins SUMMARY, BRIEF, STATEMENTS, PICK, USERS, IDEAS, ASSUMPTIONS, EVIDENCE, COMPETE, STRESS, IMPROVE, CORE, PLAN, VERDICT, DEMO and PITCH, skipping any that are missing;
- adds a cover page and a table of contents;
- writes FINAL.md and FINAL.html;
- tries to make FINAL.pdf with Chrome/Chromium, then Playwright, then pandoc.

If no PDF tool works, tell the user to open FINAL.html in a browser and use **Print → Save as PDF**.
If Python is missing, build FINAL.md yourself by joining the files in that order, with a page-break line between them.

### 5. Check the result
Check the page count, that every section is there, and that no tables are broken. Fix anything wrong and run it again.

## Output
FINAL.md, FINAL.html and FINAL.pdf in `.hackathon/`. In STATE.md, tick "ship" and set the phase to shipped.

## Finish
Say where the files are, then list the 3 things to do next: build the demo journey, record the backup video, and rehearse the Q&A.
