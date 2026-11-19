#!/usr/bin/env python3
"""Hack Kit repository checks. No dependencies beyond Python 3.8+.

Run:  python3 scripts/check.py
Exit code 0 = all checks passed, 1 = something failed (details printed).
"""
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASES = ["start", "decode", "pick", "users", "ideate", "validate", "compete", "stress",
          "improve", "lock", "plan", "verify", "pitch", "ship"]
ANYTIME = ["assumptions", "court", "status", "help"]
STANDARD = ["## Before you start", "## Goal", "## Steps", "## Output", "## Finish"]

failures = []


def ok(cond, label):
    print(("  ok   " if cond else "  FAIL ") + label)
    if not cond:
        failures.append(label)
    return cond


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict((k.strip(), v.strip().strip('"')) for k, _, v in
                (line.partition(":") for line in m.group(1).splitlines())) if m else {}


def check_manifests():
    print("Plugin manifests")
    plugin = json.loads(read(".claude-plugin/plugin.json"))
    market = json.loads(read(".claude-plugin/marketplace.json"))
    ok(plugin.get("name") == "hack", "plugin name is 'hack' (commands are /hack:…)")
    entry = next((p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")), None)
    ok(entry is not None, "marketplace lists the plugin")
    ok(entry and entry.get("version") == plugin.get("version") == market.get("metadata", {}).get("version"),
       f"versions match ({plugin.get('version')})")
    ok(plugin.get("author", {}).get("name") == "Syed Imadulla", "author is Syed Imadulla")
    return plugin["version"]


def check_commands():
    print("Commands")
    files = {f.stem: f.read_text(encoding="utf-8") for f in (ROOT / "commands").glob("*.md")}
    ok(sorted(files) == sorted(PHASES + ANYTIME), f"exactly {len(PHASES + ANYTIME)} commands: {', '.join(sorted(files))}")
    for n, name in enumerate(PHASES, 1):
        t = files.get(name, "")
        fm = frontmatter(t)
        ok(fm.get("description", "").startswith(f"Phase {n} · "), f"{name}: description says Phase {n}")
        ok(f"**Phase {n} of {len(PHASES)}**" in t, f"{name}: banner says Phase {n} of {len(PHASES)}")
        ok(all(s in t for s in STANDARD), f"{name}: has the standard sections")
        ok("$ARGUMENTS" in t, f"{name}: passes $ARGUMENTS")
    t = files.get("assumptions", "")
    ok(all(s in t for s in STANDARD), "assumptions: has the standard sections")
    for name in ANYTIME:
        ok("description" in frontmatter(files.get(name, "")), f"{name}: has a description")
    mentioned = set()
    for rel in ["README.md", "docs/index.html", "docs/GUIDE.md", "skills/hack-kit/SKILL.md", "skills/hack-court/SKILL.md"] + \
               [f"commands/{n}.md" for n in files]:
        mentioned |= set(re.findall(r"/hack:([a-z-]+)", read(rel)))
    unknown = sorted(mentioned - set(files))
    ok(not unknown, f"every /hack: command mentioned exists{' (unknown: ' + ', '.join(unknown) + ')' if unknown else ''}")
    readme = read("README.md")
    missing = [n for n in files if f"/hack:{n}" not in readme]
    ok(not missing, f"README mentions every command{' (missing: ' + ', '.join(missing) + ')' if missing else ''}")


def check_templates():
    print("Templates")
    skill = read("skills/hack-kit/SKILL.md")
    outputs = set(re.findall(r"`([A-Z][A-Z-]+)\.md`", skill)) - {"FINAL", "STATE-v1", "PICK-VERDICT"}
    templates = {f.stem for f in (ROOT / "templates").glob("*.md")}
    missing = sorted(o for o in outputs if o.lower() not in templates)
    ok(not missing, f"every output file has a template{' (missing: ' + ', '.join(missing) + ')' if missing else ''}")
    for f in sorted((ROOT / "templates").glob("*.md")):
        first = f.read_text(encoding="utf-8").splitlines()[0]
        ok(first.startswith("# "), f"templates/{f.name}: starts with a title")
    state = read("templates/state.md")
    ok("Schema version: 2" in state and "Last updated:" in state, "STATE template has schema version and last updated")
    ok(all(f"| {p}" in state for p in PHASES), "STATE template lists all 14 phases")


def check_jurors():
    print("Jury")
    j = json.loads(read("skills/hack-court/jurors.json"))
    jur = j["jurors"]
    keys = [x["key"] for x in jur]
    ok(len(jur) == 12 and len(set(keys)) == 12, "12 jurors with unique keys")
    ok(sum(x["quick"] for x in jur) == 7, "7 quick-mode jurors")
    ok(next(x for x in jur if x["key"] == "sceptic")["quick"], "the sceptic sits on the quick jury")
    ok(all(x.get("name") and x.get("lens") and len(x.get("asks", [])) >= 2 for x in jur), "every juror has name, lens and questions")
    ok(len(j["ratings"]) == 8, "8 rating items")
    rep = j["domain_seats"]["replaces"]
    ok(len(rep) == 3 and all(k in keys for k in rep), "domain seats replace 3 existing jurors")
    ok(any(next(x for x in jur if x["key"] == k)["quick"] for k in rep), "one replaced seat is a quick-mode seat")
    banned = ("end user", "citizen at the counter", "small farmer", "first-time", "affected community")
    for d, seats in j["domain_seats"]["domains"].items():
        ok(len(seats) == 3 and all(s.get("name") and s.get("lens") and s.get("asks") for s in seats), f"domain '{d}' has 3 complete jurors")
        dup = [s["name"] for s in seats if any(b in s["name"].lower() for b in banned)]
        ok(not dup, f"domain '{d}' doesn't duplicate the end user{' (' + ', '.join(dup) + ')' if dup else ''}")
    ok(set(j["votes"]) == {"GUILTY", "NOT GUILTY", "INSUFFICIENT EVIDENCE"}, "three vote options defined")
    agent = read("agents/hack-juror.md")
    ok("INSUFFICIENT EVIDENCE" in agent and "evidence_strength" in agent, "juror agent uses the v2 vote format")


def check_tally():
    print("Scripts and tests")
    for name in ("test_tally.py", "test_profile.py", "test_plan_check.py"):
        r = subprocess.run([sys.executable, str(ROOT / "tests" / name)], capture_output=True, text=True)
        ok(r.returncode == 0, f"tests/{name} passes")
        if r.returncode:
            print(r.stdout + r.stderr)
    prof = json.loads(read("skills/hack-kit/profiles.json"))
    ok(set(prof["event_types"]) == {"college", "sih", "ai-ml", "ideathon", "hardware", "corporate"}, "6 event types defined")
    ok(set(prof["lengths"]) == {"12h", "24h", "36h", "48h+"}, "4 event lengths defined")
    skip = {p for et in prof["event_types"].values() for p in et.get("changes", {}).get("skip_phases", [])}
    ok(skip <= set(PHASES), "profiles only skip real phases")
    cmds = "".join(read(f"commands/{n}.md") for n in PHASES)
    ok(cmds.count("Profile settings used") >= 12, "phase commands say which profile settings they use")
    ok("--demo" in read("commands/verify.md") and "--drill" in read("commands/pitch.md"), "demo and drill modes documented")


def table_ok(md):
    """Every Markdown table row has the same number of cells as its header."""
    bad = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
            cols = lines[i].count("|")
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                if lines[j].replace("\\|", "").count("|") != cols:
                    bad.append(lines[j][:60])
                j += 1
            i = j
        else:
            i += 1
    return bad


def check_compile():
    print("PDF compiler (on the example)")
    ex = ROOT / "examples" / "opd-saathi" / ".hackathon"
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp) / ".hackathon"
        dst.mkdir()
        for f in ex.glob("*.md"):
            (dst / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "compile.py"), str(dst), "--md-only"],
                           capture_output=True, text=True)
        ok(r.returncode == 0, "compile.py runs")
        final = (dst / "FINAL.md").read_text(encoding="utf-8") if (dst / "FINAL.md").exists() else ""
        html = (dst / "FINAL.html").read_text(encoding="utf-8") if (dst / "FINAL.html").exists() else ""
        ok(bool(final) and bool(html), "FINAL.md and FINAL.html written")
        for f in sorted(ex.glob("*.md")):
            if f.name == "STATE.md":
                continue
            title = f.read_text(encoding="utf-8").splitlines()[0]
            ok(title in final, f"FINAL includes {f.name}")
        order = [m for m in re.findall(r'\("([A-Z-]+\.md)"', read("scripts/compile.py"))]
        positions = [final.find(Path(ex / n).read_text(encoding="utf-8").splitlines()[0]) for n in order if (ex / n).exists()]
        ok(positions == sorted(positions), "sections appear in the right order")
        bad = table_ok(final)
        ok(not bad, f"all Markdown tables are well formed{' (bad rows: ' + '; '.join(bad[:3]) + ')' if bad else ''}")
        empty = re.findall(r"^## [^\n]+\n+(?=## |\Z)", final, re.M)
        ok(not empty, f"no empty sections in the example{' (' + str(len(empty)) + ' empty)' if empty else ''}")
    for f in sorted((ROOT / "templates").glob("*.md")):
        bad = table_ok(f.read_text(encoding="utf-8"))
        ok(not bad, f"templates/{f.name}: tables well formed")


def check_app_skill():
    print("Claude app skill")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_claude_ai.py"), "--check"], capture_output=True, text=True)
    ok(r.returncode == 0, "claude-ai/hack-kit and the download zip are generated from the current plugin")
    z = ROOT / "docs" / "downloads" / "hack-kit-skill.zip"
    with zipfile.ZipFile(z) as zf:
        names = zf.namelist()
    ok("hack-kit/SKILL.md" in names and all(n.startswith("hack-kit/") for n in names), "zip has hack-kit/SKILL.md at the top")


def check_website(version):
    print("Website")
    html = read("docs/index.html")
    ok('http-equiv="Content-Security-Policy"' in html and "script-src 'self'" in html, "strict Content Security Policy present")
    ok(not re.search(r"<script(?![^>]*\bsrc=)[^>]*>", html), "no inline scripts")
    ok(' style="' not in html, "no inline style attributes")
    ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
    loaded = [u for u in re.findall(r'<(?:script|link|img|iframe)[^>]+(?:src|href)="(https?://[^"]+)"', html)]
    ok(not loaded, "loads nothing from outside the repo")
    ok(all(u.startswith("https://github.com/syed-imadulla") for u in ext), "external links only point to the GitHub repo")
    ok("Think deeper. Challenge harder. Build smarter." in html, "tagline on the website")
    js = read("docs/assets/app.js")
    ok(not re.search(r"\beval\(|innerHTML|new Function|document\.write|fetch\(|XMLHttpRequest", js), "no risky JavaScript APIs")
    ok(read("README.md").count("Think deeper. Challenge harder. Build smarter.") >= 1, "tagline in the README")
    ok(f"version-{version}-" in read("README.md"), "README version badge matches the plugin")


def main():
    version = check_manifests()
    check_commands()
    check_templates()
    check_jurors()
    check_tally()
    check_compile()
    check_app_skill()
    check_website(version)
    print()
    if failures:
        print(f"{len(failures)} check(s) failed.")
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
