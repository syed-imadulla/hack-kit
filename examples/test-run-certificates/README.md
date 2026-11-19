# Example: test run — "One trip" (certificate pre-check)

The complete `.hackathon/` folder from Hack Kit v1.0's first end-to-end test run: a mock 24 h hackathon, 3 problem statements, and the full 14-phase flow.

- Every file the kit produces, from `BRIEF.md` to `PITCH.md`.
- `court/` holds the **real** trial records: evidence packs, prosecution and defense, and the raw juror votes from separate subagents for 5 trials. That includes the snippets-only round that led to the evidence-boost fix.
- Sources marked `[V]` were opened during the run. No interviews were invented, so the experiment observations are empty.

Read the report: [`docs/TEST-RUN.md`](../../docs/TEST-RUN.md).

Compile it yourself:
```bash
python3 scripts/compile.py examples/test-run-certificates/.hackathon --brief
```
