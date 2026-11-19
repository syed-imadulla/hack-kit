#!/usr/bin/env python3
"""Compile a Hack Kit .hackathon/ folder into FINAL.md, FINAL.html and (if possible) FINAL.pdf.

Usage: python3 compile.py [.hackathon] [--md-only]

PDF is attempted with, in order: pandoc (with a PDF engine), Chromium/Chrome headless,
Playwright (python). If none works, open FINAL.html in a browser and Print -> Save as PDF.
"""
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ORDER = [
    ("SUMMARY.md", "Executive summary"),
    ("BRIEF.md", "Brief and rubric"),
    ("STATEMENTS.md", "Problem statements decoded"),
    ("PICK-VERDICT.md", "Pick and trial"),
    ("USERS.md", "Users and stakeholders"),
    ("EVIDENCE.md", "Evidence"),
    ("COMPETE.md", "Existing solutions and gap"),
    ("STRESS.md", "Stress test"),
    ("CORE.md", "Locked core"),
    ("PLAN.md", "MVP plan"),
    ("VERDICT.md", "Solution trial and checks"),
    ("PITCH.md", "Pitch and judge Q&A"),
]

CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font-family: -apple-system, 'Segoe UI', Inter, Roboto, Arial, sans-serif; color:#1b1b1b;
       font-size: 11pt; line-height: 1.5; max-width: 900px; margin: 0 auto; padding: 24px; }
h1 { font-size: 22pt; border-bottom: 3px solid #f5c400; padding-bottom: 6px; margin-top: 0; }
h2 { font-size: 15pt; margin-top: 22px; color:#111; }
h3 { font-size: 12.5pt; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5pt; }
th, td { border: 1px solid #ccc; padding: 5px 7px; vertical-align: top; text-align: left; }
th { background: #f6f3e6; }
code, pre { background: #f4f4f4; border-radius: 4px; font-size: 9pt; }
pre { padding: 10px; overflow-x: auto; white-space: pre-wrap; }
blockquote { border-left: 4px solid #f5c400; margin: 8px 0; padding: 4px 12px; color:#444; background:#fffbea; }
.cover { text-align:center; padding: 120px 0 60px; }
.cover h1 { border: none; font-size: 34pt; }
.cover p { color:#555; }
.section { page-break-before: always; }
.toc li { margin: 3px 0; }
"""


def first_heading(text, fallback):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def read_state_title(folder: Path):
    st = folder / "STATE.md"
    if not st.exists():
        return "Hackathon Idea Pack", ""
    t = st.read_text(encoding="utf-8")
    event = re.search(r"\|\s*Event\s*\|\s*([^|]*)\|", t)
    motto = re.search(r"\|\s*Motto\s*\|\s*([^|]*)\|", t)
    ev = event.group(1).strip() if event and event.group(1).strip() else "Hackathon Idea Pack"
    mo = motto.group(1).strip() if motto else ""
    return ev, mo


def build_markdown(folder: Path):
    parts, toc = [], []
    for fname, label in ORDER:
        p = folder / fname
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8").strip()
        toc.append((fname, label))
        parts.append((fname, label, text))
    return parts, toc


def md_to_html(md_text):
    try:
        import markdown  # type: ignore
        return markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    except Exception:
        pass
    if shutil.which("pandoc"):
        r = subprocess.run(["pandoc", "-f", "gfm", "-t", "html"], input=md_text,
                           capture_output=True, text=True)
        if r.returncode == 0:
            return r.stdout
    return "<pre>" + html.escape(md_text) + "</pre>"


def try_pdf(html_path: Path, pdf_path: Path, md_path: Path):
    # 1. Chromium / Chrome headless
    for exe in ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        path = shutil.which(exe) or (exe if os.path.exists(exe) else None)
        if not path:
            continue
        r = subprocess.run([path, "--headless", "--disable-gpu", "--no-sandbox",
                            "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
                            html_path.resolve().as_uri()], capture_output=True, text=True)
        if pdf_path.exists() and pdf_path.stat().st_size > 1000:
            return f"Chrome ({exe})"
    # 2. Playwright (python)
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(html_path.resolve().as_uri())
            pg.pdf(path=str(pdf_path), format="A4", print_background=True,
                   margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
            b.close()
        if pdf_path.exists():
            return "Playwright"
    except Exception:
        pass
    # 3. pandoc with a PDF engine
    if shutil.which("pandoc"):
        for engine in ["wkhtmltopdf", "weasyprint", "xelatex", "pdflatex"]:
            if shutil.which(engine):
                r = subprocess.run(["pandoc", str(md_path), "-f", "gfm", "-o", str(pdf_path),
                                    f"--pdf-engine={engine}"], capture_output=True, text=True)
                if r.returncode == 0 and pdf_path.exists():
                    return f"pandoc + {engine}"
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    md_only = "--md-only" in sys.argv
    folder = Path(args[0] if args else ".hackathon")
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}. Run /hack:start first.")

    parts, toc = build_markdown(folder)
    if not parts:
        sys.exit("No Hack Kit files found to compile.")

    event, motto = read_state_title(folder)

    # FINAL.md
    md_out = [f"# {event}", ""]
    if motto:
        md_out += [f"> {motto}", ""]
    md_out += ["## Contents", ""] + [f"{i}. {label}" for i, (_, label) in enumerate(toc, 1)] + [""]
    for fname, label, text in parts:
        md_out += ['<div style="page-break-after:always"></div>', "", text, ""]
    md_path = folder / "FINAL.md"
    md_path.write_text("\n".join(md_out), encoding="utf-8")

    # FINAL.html
    body = [f'<div class="cover"><h1>{html.escape(event)}</h1>']
    if motto:
        body.append(f"<p><em>{html.escape(motto)}</em></p>")
    body.append("<p>Idea Pack · compiled with Hack Kit</p></div>")
    body.append('<h2>Contents</h2><ol class="toc">' +
                "".join(f"<li>{html.escape(label)}</li>" for _, label in toc) + "</ol>")
    for fname, label, text in parts:
        body.append(f'<div class="section">{md_to_html(text)}</div>')
    html_doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{html.escape(event)}</title>"
                f"<style>{CSS}</style></head><body>{''.join(body)}</body></html>")
    html_path = folder / "FINAL.html"
    html_path.write_text(html_doc, encoding="utf-8")

    print(f"Wrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"Sections: {', '.join(label for _, label in toc)}")

    if md_only:
        return
    pdf_path = folder / "FINAL.pdf"
    if pdf_path.exists():
        pdf_path.unlink()
    how = try_pdf(html_path, pdf_path, md_path)
    if how:
        print(f"Wrote {pdf_path} (via {how})")
    else:
        print("Could not make a PDF automatically. Open FINAL.html in a browser and use Print -> Save as PDF.")


if __name__ == "__main__":
    main()
