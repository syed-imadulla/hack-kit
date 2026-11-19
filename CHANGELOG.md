# Changelog

## 0.3.1 — 2026-11-19
### Changed
- The website's juror ring is now interactive: drag or swipe to spin it with momentum, tilt it up and down, hold to fan the cards out, tap a card to flip it. Arrow keys spin it, and Enter flips the front card. Auto-spin pauses when the ring is off-screen.
- Author, copyright and credits are now **Syed Imadulla** (LICENSE, plugin manifest, README, website, example).

## 0.3.0 — 2026-11-19
### Added
- Project website in `docs/` (GitHub Pages): an interactive 12-phase flow, a 3D demo courtroom trial, a `.hackathon/` folder preview, install tabs with copy buttons, flip cards for the 13 rules, a 24 h timeline and an FAQ.
  - Self-contained: no external scripts, fonts or trackers. A strict Content Security Policy blocks inline scripts and outbound connections.
  - Respects reduced-motion settings; keyboard and screen-reader friendly.
- `docs/downloads/hack-kit-skill.zip`: a ready-to-upload Claude app skill.
- `scripts/build_skill_zip.sh` to rebuild that zip.

## 0.2.0 — 2026-11-19
### Added
- `/hack:help`: a command map and quick start.
- Templates for `STATEMENTS`, `STRESS` and `SUMMARY`.
- `docs/GUIDE.md`: the full hackathon playbook (before, during and after the event).
- A fallback for finding the plugin when `${CLAUDE_PLUGIN_ROOT}` isn't expanded.
- PDF output now has page numbers and a date on the cover.
- `CONTRIBUTING.md` and this changelog.

### Changed
- Every command now uses the same layout: phase banner, Before you start, Goal, Steps, Output, Finish.
- Each template has the same name as the file it produces (`users.md` → `USERS.md`, and so on).
- `PICK-VERDICT.md` is renamed to `PICK.md`.
- Every output file starts with a title and a `> Summary:` line.
- Rewrote the README with a flow diagram, a quick start and an FAQ.

## 0.1.0 — 2026-11-19
- First release: 14 `/hack:` commands, the problem-focused trial (`hack-court`), templates, the PDF compiler, the claude.ai version and the OPD Saathi example.
