# Changelog

## 1.2.0 — 2026-11-19 · "Prove it"
Post-hackathon learning, deterministic merging, standardized test infrastructure, verified causal retrospective, and complete 14-phase real-world civic showcase.

### Added
- **`/hack:retro` & `scripts/retro.py`:** Post-hackathon retrospective system that parses the completed `.hackathon/` project and connects the dots across phases. Features multi-dimensional feature reporting (planned, built, tested, mocked, shown, not implemented) without mutual exclusion bugs, and rigorous causal analysis distinguishing directly evidenced causes from contributing factors and correlations. Writes `RETRO.md`.
- **`templates/retro.md`:** 10-section retrospective template with executive summary, goals vs outcomes, idea evolution, assumptions analysis, delivered features ladder, jury feedback, and actionable improvements.
- **`scripts/merge.py`:** Deterministic, transactional parser for merging teammate `## Pending from <name>` sections. Validates table structures, appends new rows with attribution, skips exact duplicates, tags conflicting rows with `CONFLICT` annotations, and guarantees zero data loss and idempotency. Integrated directly with `/hack:status --merge`.
- **Real-World Showcase (`examples/pds-anna-mitra/`):** Full 14-phase demonstration for Public Distribution System (PDS) quota transparency and outage resilience. Demonstrates statutory NFSA PMGKAY decoupling, genuine SQLite3 WAL database, 2-tap dispense (<15ms), SHA-256 hash-chaining, HMAC signatures with key rotation, independent monotonic clock validation, split-brain duplicate conflict detection, and 28 passing unit & integration tests.
- **Standard unittest discovery:** All test suites migrated to standard `unittest.TestCase` format, supporting `python3 -m unittest discover -s tests` with 87 granular unit tests across tallying, profiles, planning DAGs, merging, and retrospectives.

### Changed
- CLI scripts (`lint_project.py`, `compile.py`, `profile.py`, `onetrip.py`) now support `-h`/`--help` and provide clean, friendly guidance instead of unhandled tracebacks on missing arguments.
- `compile.py` compiles `DEMO.md` and `RETRO.md` when present in `.hackathon/`.
- 19 commands total (14 phases + 5 anytime/post-event commands).

## 1.1.0 — 2026-11-19 · "Build smarter"
The kit now adapts to your event and checks what you actually built, not just what you planned.

### Added
- **Event profiles.** `/hack:start` asks the event type (college, SIH, AI/ML, ideathon, hardware, corporate), length (12 h, 24 h, 36 h, 48 h+), team experience and judging focus. `scripts/profile.py` turns that into a `## Profile` table in STATE.md, and every phase command reads its settings: questions asked, research depth, jury size, ideation width, plan depth, drill length. Ideathons skip the plan phase and the demo court; SIH swaps the statement owner onto the quick jury.
- **Beginner mode.** Fewer questions per step and a one-line "why" for each step.
- **Team-aware `/hack:plan`.** A team table (skills, hours) and a task table (owner, skills, hours, dependencies, status). `scripts/plan_check.py` finds the critical path, overload and spare hours, skill gaps, integration points, dependency loops and whether the plan fits before code freeze. Tasks marked `maybe` are tracked but not counted. Plans also get failure scenarios and AI test cases.
- **`/hack:verify --demo` (Demo Day Court).** Planned → built → tested → shown: a feature ladder where a feature counts only if it was run, a timed demo walk, a failure drill, the AI test cases, a **disclosure check** (each "this is mocked" line must match what exists now), a trial of the built product, and a fix list ranked by juror agreement. Writes `DEMO.md` and updates the pitch's built-vs-mocked answer.
- **`/hack:pitch --drill`.** A simulated panel of 3 judges built from your rubric asks one hard question at a time. It never writes your answers; it scores clarity, evidence, honesty and length, shows a stronger answer from your own files, and checks every pitch claim against `DEMO.md`.
- **Safe parallel work.** One owner per file; teammates write `## Pending from <name>` sections and only the captain merges with `/hack:status --merge`. Conflicts are marked, never overwritten.
- **Lighter context.** Commands read each file's summary line first and open the rest only when needed.

### Changed
- `tally.py` accepts harmless wording differences ("Moderate", " guilty ") instead of rejecting the vote. Unknown words are still rejected; the raw votes file is never edited.
- `lint_project.py` warns about mock disclosures in DEMO.md that aren't true yet, and no longer flags rubric weights such as "Problem judge (25%)".
- The test-run example now includes the v1.1 run: profile, plan check, prototype, Demo Day Court and drill.

## 1.0.1 — 2026-11-19 · test-run fixes
All 11 problems found in the first end-to-end test run ([docs/TEST-RUN.md](docs/TEST-RUN.md)) are fixed.

- `/hack:pick` adds an **evidence boost**: open the 2 strongest sources per shortlisted statement before the trial. Unopened search snippets are `[AI]`.
- Decision rule: INCONCLUSIVE only when abstentions are **more than** 1/3; PASS needs 75% NOT GUILTY of **all** valid votes; a PASS is **capped to REVISE** while a "collapses" assumption is untested (`tally.py --open-collapses`).
- Domain seats no longer duplicate the end user (civic: clerk, policy officer, NGO advocate; agriculture: agronomist, trader, FPO leader; education: literacy specialist, parent, school admin; finance: compliance, fraud analyst, literacy trainer; climate: field scientist, local authority, response volunteer).
- The sceptic always sits on the quick jury (7 seats).
- Evidence packs include existing solutions; the team's own plans are always `[T]`.
- `/hack:improve` compares with the stress doubts when there's no earlier solution trial, and stops when the remaining P0s are experiments.
- New brief pack (`compile.py --brief`) and `scripts/lint_project.py` (run by `/hack:status`).
- New example: `examples/test-run-certificates`, the full test project with real trial records. Its votes are now test fixtures.

## 1.0.0 — 2026-11-19 · "Think deeper"
**Think deeper. Challenge harder. Build smarter.** Shaped by independent reviews of v0.3.

### Added
- **`/hack:ideate`** (phase 5): explores 6 solution directions (user, process, access, integration, prevention and technology shift), constraint removal and combinations. Scores the trade-offs, lets the team pick, and logs rejected ideas.
- **`/hack:improve`** (phase 9, and after any trial): turns feedback into a revised CORE version, with a reason for each change, a no-drift guardrail, team approval, a version comparison, a quick re-trial and a stop rule.
- **`/hack:assumptions`** (anytime) and a living `ASSUMPTIONS.md`: importance, confidence, evidence, kill test, how to test, pass/fail rule, and dated status history.
- **Evidence labels** everywhere: `[V]` verified, `[T]` team-provided, `[AI]` inference, `[?]` unknown. Only `[V]` and `[T]` can validate.
- **Hack Court 2.0:**
  - labelled evidence packs;
  - a third juror vote, INSUFFICIENT EVIDENCE, plus evidence strength, weakest assumption, missing info, and fixes rated for impact and effort;
  - PASS / REVISE / FAIL / INCONCLUSIVE decisions;
  - a contradiction check and ranked improvements;
  - domain seats for healthcare, agriculture, education, finance, civic and climate (the jury stays at 12);
  - raw votes saved unedited, and retries logged.
- `scripts/tally.py`: checks juror replies and applies the decision rule, with tests in `tests/`.
- **Experiment cards** in `/hack:validate`: hypothesis, who, procedure, pass/fail, and observations from the team only.
- **Time guard:** quick mode and 12 h events shrink the new thinking steps automatically.
- `scripts/check.py` and GitHub Actions: manifests, command structure, templates, jury, vote counter, PDF build, app-skill sync and website safety.
- `scripts/build_claude_ai.py`: the Claude app skill is now **generated** from the plugin, including every phase's full instructions, the templates and the court rules.
- Templates for `PICK`, `IDEAS`, `IMPROVE` and `ASSUMPTIONS`. `MIGRATION.md`.

### Changed
- 14 phases and 18 commands. `/hack:pick` now chooses the **problem**; `/hack:ideate` chooses the idea.
- `STATE.md` schema 2: last updated, event length, a phase table, a decisions log with rejected options, locked items, pending items and CORE version. Older projects upgrade automatically.
- Lock protects the problem, main user, core journey and motto. Details can still improve through `/hack:improve`.
- `/hack:stress` finds and ranks doubts and failure scenarios; fixes are applied in `/hack:improve`.
- `/hack:compete` adds a differentiation statement based on user value ("different technology isn't innovation").
- Principles 14–17: evidence before confidence, riskiest assumption first, technology isn't innovation, keep the decision history.
- The README, website, guide, one-paste prompt and example were updated for v1.0.

### Removed
- `scripts/build_skill_zip.sh` (replaced by `scripts/build_claude_ai.py`).

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
