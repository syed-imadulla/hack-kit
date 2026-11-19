# Illustrative trials (not real jury runs)

These 7 trials (pick, ideation, validate, compete, stress, improve, demo) were written while building the showcase. In each one, all 12 juror votes were written in a single pass by one model. They are **not** the output of 12 separate juror subagents, so they don't show how a real Hack Court behaves: 82 of 84 votes are NOT GUILTY, and almost every confidence is 8 or 9.

Read them only as examples of the file format. They are kept outside `court/` so `retro.py` and other tools don't count them as evidence.

The real trial for this project is `../court/demo-1/`: 2 lawyers and 7 jurors, each a separate subagent. It returned **FAIL, 0–7**, and found two bugs the illustrative "demo" trial missed.
