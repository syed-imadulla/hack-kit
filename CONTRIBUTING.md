# Contributing

Thanks for helping make Hack Kit better. The most useful contributions come from real hackathons. If you used it at an event, tell us what worked and what didn't.

## Ways to help
- **Field reports:** open an issue with the event, which commands you used, what helped and what slowed you down.
- **Jurors:** suggest a new juror lens, or a better question for an existing one, in `skills/hack-court/jurors.json`. Jurors must judge the problem or the solution, never business viability.
- **Templates:** keep them short. Each template has the same name as the file it produces.
- **Examples:** add a worked example under `examples/<idea-name>/.hackathon/`. Label sample verdicts as samples.

## Rules for command files
Every file in `commands/` follows the same layout:

```
---
description: "Phase N · what it does"
argument-hint: "..."
---
# /hack:<name> — <short title>
> **Phase N of 12** · Reads: … · Writes: … · Next: …
Arguments: $ARGUMENTS
## Before you start
## Goal
## Steps
## Output
## Finish
```

Write in simple everyday English, with short lines and tables for comparisons.

## Testing a change locally
```
/plugin marketplace add ./hack-kit
/plugin install hack@hack-kit
```
Run `/hack:help`, then try `/hack:start` → `/hack:pick --quick` on an old problem statement.

Check the plugin structure with:
```
claude plugin validate .
```

Check the PDF compiler with:
```
python3 scripts/compile.py examples/opd-saathi/.hackathon
```

## Website and skill zip
- The website lives in `docs/` (`index.html`, `assets/style.css`, `assets/app.js`). Keep it self-contained: no CDNs, no external fonts, no trackers. The page's Content Security Policy blocks them anyway.
- After editing `claude-ai/hack-kit/SKILL.md`, rebuild the download with `./scripts/build_skill_zip.sh`.
- Preview locally with `python3 -m http.server -d docs 8000`, then open http://localhost:8000.
