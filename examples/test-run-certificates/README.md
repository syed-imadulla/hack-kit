# Example: test run — "One trip" (certificate pre-check)

The complete `.hackathon/` folder from Hack Kit's end-to-end test runs: a mock 24 h hackathon, 3 problem statements, and the full 14-phase flow (v1.0), then the v1.1 features on the same project: event profile, team-aware plan, a small prototype, Demo Day Court and a pitch drill.

- Every file the kit produces, from `BRIEF.md` to `PITCH.md`.
- `court/` holds the **real** trial records: evidence packs, prosecution and defense, and the raw juror votes from separate subagents for 5 trials. That includes the snippets-only round that led to the evidence-boost fix.
- Sources marked `[V]` were opened during the run. No interviews were invented, so the experiment observations are empty.

- **v1.1 additions:** `STATE.md → ## Profile`, the plan check at the end of `PLAN.md`, `DEMO.md` (feature ladder, AI tests, disclosure table), `court/demo-1/` (2 lawyers + 7 jurors, 7–0 FAIL), and `## Drill 1` in `PITCH.md`.
- `app/` is the prototype the demo court judged: `python3 app/onetrip.py app/scans/mismatch`. OCR and voice are mocked, and the demo files say so.

Read the report: [`docs/TEST-RUN.md`](../../docs/TEST-RUN.md).

Compile it yourself:
```bash
python3 scripts/compile.py examples/test-run-certificates/.hackathon --brief
```
