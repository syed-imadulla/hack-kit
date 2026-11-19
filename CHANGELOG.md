# Changelog

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
