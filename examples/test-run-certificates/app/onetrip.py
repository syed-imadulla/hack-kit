#!/usr/bin/env python3
"""One trip — prototype counter check (test-run build). OCR is MOCKED: each scan is a JSON file
standing in for what the vision model would extract. Usage: python3 onetrip.py <scan-folder>"""
import json, re, sqlite3, sys, time
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

KN = {"missing": "ದಯವಿಟ್ಟು {doc} ತನ್ನಿ.", "unreadable": "{doc} ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ, ಮತ್ತೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ.",
      "name": "{doc} ನಲ್ಲಿ ಹೆಸರು ಬೇರೆ ಇದೆ, ದಯವಿಟ್ಟು ಪರಿಶೀಲಿಸಿ.", "old": "{doc} ಹಳೆಯದಾಗಿರಬಹುದು.",
      "ok": "ಎಲ್ಲಾ ದಾಖಲೆಗಳು ಸರಿಯಾಗಿ ಕಾಣುತ್ತಿವೆ. ಅರ್ಹತೆ ಮತ್ತು ತಹಸೀಲ್ದಾರ್ ನಿರ್ಧಾರವನ್ನು ಇಲ್ಲಿ ಪರಿಶೀಲಿಸಲಾಗಿಲ್ಲ."}

def norm(n):
    n = n.lower().replace("ksh", "x").replace("ee", "i")
    return re.sub(r"[^a-z ]", "", n).split()

def same_person(a, b):
    ta, tb = norm(a), norm(b)
    if not ta or not tb:
        return False
    first = SequenceMatcher(None, ta[0], tb[0]).ratio() >= 0.8
    rest_a, rest_b = ta[1:], tb[1:]
    initials_ok = all(any(y.startswith(x[0]) for y in rest_b) for x in rest_a) if rest_a and rest_b else True
    return first and initials_ok

def main(folder):
    t0 = time.time()
    cl = json.loads((Path(__file__).parent / "checklists/income_certificate.json").read_text())
    docs = [json.loads(p.read_text()) for p in sorted(Path(folder).glob("*.json"))]
    by = {d["doc_type"]: d for d in docs}
    flags = []
    for req in cl["required"]:
        d = by.get(req["type"])
        if not d:
            flags.append(("missing", req)); continue
        if not d.get("readable"):
            flags.append(("unreadable", req)); continue
        if "max_age_days" in req and d.get("date"):
            if (date.today() - date.fromisoformat(d["date"])).days > req["max_age_days"]:
                flags.append(("old", req))
    ref = by.get("aadhaar", {}).get("name", "")
    for req in cl["required"]:
        d = by.get(req["type"])
        if d and d.get("readable") and d.get("name") and req["type"] != "aadhaar" and not same_person(ref, d["name"]):
            flags.append(("name", req))
    print(f"Checklist: {cl['certificate']} (last checked {cl['last_checked']})")
    for kind, req in flags:
        print(f"  ⚠ possible issue, please check: {kind} — {req['type']}")
        print(f"    [TTS mocked] {KN[kind].format(doc=req['label_kn'])}")
    if not flags:
        print("  ✓ looks complete (operator decides)")
        print(f"    [TTS mocked] {KN['ok']}")
    a = by.get("aadhaar", {}).get("number")
    if a:
        print(f"  Aadhaar shown as: XXXX XXXX {a[-4:]}")
    db = sqlite3.connect(Path(__file__).parent / "flaglog.sqlite")
    db.execute("create table if not exists log(ts real, folder text, flags text)")
    db.execute("insert into log values(?,?,?)", (time.time(), str(folder), json.dumps([[k, r["type"]] for k, r in flags])))
    db.commit()
    print(f"  checked in {time.time() - t0:.2f} s · logged")

if __name__ == "__main__":
    main(sys.argv[1])
