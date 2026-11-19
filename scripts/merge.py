#!/usr/bin/env python3
"""Safely merge teammate pending sections into main project files.

Usage:
  python3 merge.py [.hackathon] [--dry-run] [--file <filename>] [--json]

Scans for sections matching '## Pending from <name> [— <time>]' in .hackathon/*.md.
Validates table structures, merges non-conflicting rows, flags conflicts for captain
review, preserves teammate attribution, and maintains idempotency and atomic writes.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Identify table column delimiter pattern
DELIM_PATTERN = re.compile(r"^\|[\s:|-]+\|$")
PENDING_HEADING_PATTERN = re.compile(r"^##\s+Pending from\s+([^\n]+)", re.M)


def table_ok(md):
    """Check that every Markdown table row has the same number of cells as its header."""
    bad = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and DELIM_PATTERN.match(lines[i + 1].strip()):
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


def parse_attribution(raw_header):
    """Extract author and optional timestamp from a pending header line."""
    raw = raw_header.strip()
    # Match dividers like ' — ', ' – ', ' - '
    parts = re.split(r"\s+[—–-]\s+", raw, maxsplit=1)
    author = parts[0].strip()
    timestamp = parts[1].strip() if len(parts) > 1 else ""
    return author, timestamp


def parse_cells(row_str):
    """Split a markdown table row into stripped cell values."""
    raw = row_str.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [c.strip() for c in raw.split("|")]


def format_row(cells):
    """Format list of cell values into a markdown table row."""
    return "| " + " | ".join(cells) + " |"


def normalize_key(text):
    """Normalize text for fuzzy primary key matching."""
    t = text.lower().strip()
    # Remove leading numbering like '1.', '1)', '1 -'
    t = re.sub(r"^\d+[\.\)\-]\s*", "", t)
    # Remove extra spaces and punctuation
    t = re.sub(r"[^\w\s]", "", t)
    return " ".join(t.split())


def find_key_column_index(headers):
    """Determine the column index used as primary key for row matching."""
    norm_headers = [h.lower() for h in headers]
    # Priority column names
    candidates = ["assumption", "claim", "fact / claim", "name", "alternative / competitor",
                  "what matters to the user", "task", "question", "step", "feature"]
    for c in candidates:
        if c in norm_headers:
            return norm_headers.index(c)
    # If first column is ID-like (#, id), use 2nd column if available
    if len(norm_headers) > 1 and norm_headers[0] in ("#", "id", "no", "item"):
        return 1
    return 0


def is_sequential_id_table(headers, rows):
    """Check if table has a numeric ID column that follows 1, 2, 3... sequence."""
    if not headers or headers[0].lower() not in ("#", "id"):
        return False
    if not rows:
        return True
    ids = []
    for r in rows:
        cells = parse_cells(r)
        if cells and cells[0].isdigit():
            ids.append(int(cells[0]))
    return bool(ids) and ids == list(range(1, len(ids) + 1))


def process_file_content(content, filename):
    """
    Parse pending sections, merge into main tables, detect duplicates & conflicts.
    Returns (new_content, summary_dict, error_list).
    """
    errors = []
    # Structural check on original file
    bad_orig = table_ok(content)
    if bad_orig:
        errors.append(f"{filename}: broken table in existing content: {bad_orig[0]}")
        return content, {}, errors

    pending_matches = list(PENDING_HEADING_PATTERN.finditer(content))
    if not pending_matches:
        return content, {"pending_sections": 0, "added": 0, "conflicts": 0, "duplicates": 0}, []

    first_pending_pos = pending_matches[0].start()
    main_part = content[:first_pending_pos]
    pending_part = content[first_pending_pos:]

    # Parse pending sections
    sections = []
    for i, m in enumerate(pending_matches):
        start = m.start() - first_pending_pos
        end = (pending_matches[i + 1].start() - first_pending_pos) if i + 1 < len(pending_matches) else len(pending_part)
        sec_text = pending_part[start:end]
        author, timestamp = parse_attribution(m.group(1))
        lines = sec_text.splitlines()
        body_lines = lines[1:] if len(lines) > 1 else []
        sections.append({
            "author": author,
            "timestamp": timestamp,
            "raw_header": m.group(1),
            "body": "\n".join(body_lines).strip()
        })

    # Validate pending section table formatting
    for sec in sections:
        bad_pending = table_ok(sec["body"])
        if bad_pending:
            errors.append(f"{filename}: broken table in pending section from '{sec['author']}': {bad_pending[0]}")

    if errors:
        return content, {}, errors

    # Parse main tables from main_part
    main_lines = main_part.splitlines()
    table_ranges = []
    i = 0
    while i < len(main_lines):
        line = main_lines[i].strip()
        if line.startswith("|") and i + 1 < len(main_lines) and DELIM_PATTERN.match(main_lines[i + 1].strip()):
            start_idx = i
            header_line = main_lines[i]
            delim_line = main_lines[i + 1]
            i += 2
            row_indices = []
            while i < len(main_lines) and main_lines[i].strip().startswith("|"):
                row_indices.append(i)
                i += 1
            table_ranges.append({
                "header_idx": start_idx,
                "header_line": header_line,
                "delim_line": delim_line,
                "row_indices": row_indices,
                "headers": parse_cells(header_line),
                "cols": header_line.count("|")
            })
        else:
            i += 1

    added_count = 0
    conflicts_count = 0
    duplicates_count = 0
    skipped_items = []
    added_items = []
    conflict_items = []

    # Merge pending rows
    modified_lines = list(main_lines)
    for sec in sections:
        author = sec["author"]
        ts = sec["timestamp"]
        attr_label = f"{author} — {ts}" if ts else author

        body_lines = [l.strip() for l in sec["body"].splitlines() if l.strip()]
        pending_rows = []
        for l in body_lines:
            if l.startswith("|"):
                if DELIM_PATTERN.match(l):
                    continue
                cells = parse_cells(l)
                # Skip duplicate header line inside pending block
                if table_ranges and cells == table_ranges[0]["headers"]:
                    continue
                pending_rows.append(cells)

        if not pending_rows:
            continue

        if not table_ranges:
            errors.append(f"{filename}: has pending table rows from '{author}' but no target main table found.")
            return content, {}, errors

        # Target the primary table in the file (e.g. All assumptions, Evidence table)
        tbl = table_ranges[0]
        headers = tbl["headers"]
        key_col = find_key_column_index(headers)
        has_seq_id = is_sequential_id_table(headers, [modified_lines[idx] for idx in tbl["row_indices"]])

        for p_cells in pending_rows:
            if len(p_cells) != len(headers):
                errors.append(f"{filename}: row from '{author}' has {len(p_cells)} cells, expected {len(headers)}.")
                continue

            p_key = normalize_key(p_cells[key_col])

            # Check existing rows in table
            matched_idx = None
            is_exact_dup = False
            is_conflict = False

            existing_rows = [modified_lines[idx] for idx in tbl["row_indices"]]
            for r_idx, r_str in zip(tbl["row_indices"], existing_rows):
                r_cells = parse_cells(r_str)
                r_key = normalize_key(r_cells[key_col])
                if r_key == p_key:
                    matched_idx = r_idx
                    # Compare non-ID cells
                    comp_start = 1 if (has_seq_id and len(r_cells) > 1) else 0
                    if r_cells[comp_start:] == p_cells[comp_start:]:
                        is_exact_dup = True
                    else:
                        is_conflict = True
                    break

            if is_exact_dup:
                duplicates_count += 1
                skipped_items.append(f"{p_cells[key_col]} (exact duplicate from {attr_label})")
                continue

            if is_conflict:
                conflicts_count += 1
                # Format conflict row preserving attribution
                conflict_cells = list(p_cells)
                # Tag status or last cell with conflict annotation
                note_col = -1
                for candidate_name in ("notes", "source", "status", "reliability"):
                    if candidate_name in [h.lower() for h in headers]:
                        note_col = [h.lower() for h in headers].index(candidate_name)
                        break

                orig_note = conflict_cells[note_col]
                conflict_annotation = f"CONFLICT ({attr_label})"
                conflict_cells[note_col] = f"{orig_note} [{conflict_annotation}]" if orig_note else conflict_annotation

                # Preserve sequential ID if target has one
                if has_seq_id and matched_idx is not None:
                    conflict_cells[0] = parse_cells(modified_lines[matched_idx])[0]

                conflict_row_str = format_row(conflict_cells)
                # Insert directly after the matched conflicting row
                insert_pos = matched_idx + 1
                modified_lines.insert(insert_pos, conflict_row_str)
                # Adjust indices
                for t in table_ranges:
                    t["row_indices"] = [idx if idx < insert_pos else idx + 1 for idx in t["row_indices"]]
                tbl["row_indices"].append(insert_pos)
                tbl["row_indices"].sort()
                conflict_items.append(f"{p_cells[key_col]} (conflicts with main row; both preserved)")

            else:
                # Brand new row
                new_cells = list(p_cells)
                if has_seq_id:
                    next_id = len(tbl["row_indices"]) + 1
                    new_cells[0] = str(next_id)

                # Add attribution if table has source/updated/notes column
                norm_h = [h.lower() for h in headers]
                if "source" in norm_h:
                    s_idx = norm_h.index("source")
                    if not new_cells[s_idx] or new_cells[s_idx] in ("—", "-"):
                        new_cells[s_idx] = f"team ({author})"
                elif "updated" in norm_h:
                    u_idx = norm_h.index("updated")
                    if not new_cells[u_idx] or new_cells[u_idx] in ("—", "-"):
                        new_cells[u_idx] = ts or author

                new_row_str = format_row(new_cells)
                # Append to bottom of target table
                last_row_idx = tbl["row_indices"][-1] if tbl["row_indices"] else tbl["delim_line"]
                insert_pos = last_row_idx + 1
                modified_lines.insert(insert_pos, new_row_str)
                for t in table_ranges:
                    t["row_indices"] = [idx if idx < insert_pos else idx + 1 for idx in t["row_indices"]]
                tbl["row_indices"].append(insert_pos)
                tbl["row_indices"].sort()
                added_count += 1
                added_items.append(f"{new_cells[key_col]} (from {attr_label})")

    if errors:
        return content, {}, errors

    # Clean up trailing whitespace and remove the merged pending sections
    new_content = "\n".join(modified_lines).rstrip() + "\n"

    # Validate output
    bad_out = table_ok(new_content)
    if bad_out:
        errors.append(f"{filename}: merge resulted in broken table row: {bad_out[0]}")
        return content, {}, errors

    summary = {
        "pending_sections": len(sections),
        "added": added_count,
        "conflicts": conflicts_count,
        "duplicates": duplicates_count,
        "added_items": added_items,
        "conflict_items": conflict_items,
        "skipped_items": skipped_items,
        "authors": sorted(list(set(s["author"] for s in sections)))
    }
    return new_content, summary, []


def update_state_md(state_content, total_merged, total_conflicts, authors):
    """Append merge event to Decisions log in STATE.md and update timestamp."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    author_str = ", ".join(authors) if authors else "teammates"
    decision = f"Merged {total_merged} pending row(s) from {author_str}"
    why = f"Safe parallel merge via scripts/merge.py ({total_conflicts} conflict(s) flagged for review)"
    new_log_row = f"| {now_str} | {decision} | {why} | — | Captain |"

    lines = state_content.splitlines()
    new_lines = []
    in_decisions_table = False
    log_inserted = False

    for i, line in enumerate(lines):
        if line.startswith("Last updated:"):
            new_lines.append(f"Last updated: {now_str}")
            continue

        new_lines.append(line)

        if line.strip() == "## Decisions log":
            in_decisions_table = True
            continue

        if in_decisions_table and DELIM_PATTERN.match(line.strip()) and not log_inserted:
            new_lines.append(new_log_row)
            log_inserted = True
            continue

        if in_decisions_table and line.startswith("## ") and line.strip() != "## Decisions log":
            in_decisions_table = False

    return "\n".join(new_lines).rstrip() + "\n"


def merge_project(folder_path, dry_run=False, target_file=None):
    """
    Execute merge across project files with strict transactional validation.
    Returns (success: bool, report: dict).
    """
    folder = Path(folder_path)
    if not folder.is_dir():
        return False, {"error": f"Folder not found: {folder}. Run /hack:start first."}

    files_to_check = [folder / target_file] if target_file else sorted(folder.glob("*.md"))
    files_to_check = [f for f in files_to_check if f.is_file() and not f.name.startswith(("FINAL", "BRIEF")) and f.name != "STATE.md"]

    proposed_writes = {}
    file_summaries = {}
    all_errors = []
    total_added = 0
    total_conflicts = 0
    total_duplicates = 0
    all_authors = set()

    # Step 1 & 2: Parse and construct proposed changes in memory
    for f in files_to_check:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            all_errors.append(f"Cannot read {f.name}: {e}")
            continue

        if "## Pending from" not in content:
            continue

        new_content, summary, errors = process_file_content(content, f.name)
        if errors:
            all_errors.extend(errors)
        else:
            proposed_writes[f] = new_content
            file_summaries[f.name] = summary
            total_added += summary.get("added", 0)
            total_conflicts += summary.get("conflicts", 0)
            total_duplicates += summary.get("duplicates", 0)
            all_authors.update(summary.get("authors", []))

    # If errors occurred, abort transactionally
    if all_errors:
        return False, {"error": "Transactional validation failed. Original files remain untouched.", "details": all_errors}

    if not proposed_writes:
        return True, {"message": "No pending sections found to merge. Files are clean and up to date."}

    # Prepare STATE.md update if needed
    state_file = folder / "STATE.md"
    if state_file.is_file():
        try:
            state_text = state_file.read_text(encoding="utf-8")
            new_state = update_state_md(state_text, total_added, total_conflicts, sorted(list(all_authors)))
            proposed_writes[state_file] = new_state
            file_summaries["STATE.md"] = {"action": "Updated Last updated and recorded merge in Decisions log"}
        except Exception as e:
            return False, {"error": f"Failed preparing STATE.md update: {e}. No files written."}

    # If dry-run, stop before writing
    if dry_run:
        return True, {
            "dry_run": True,
            "total_added": total_added,
            "total_conflicts": total_conflicts,
            "total_duplicates": total_duplicates,
            "authors": sorted(list(all_authors)),
            "files": file_summaries
        }

    # Step 3: Atomic write phase (temporary files first)
    tmp_files = []
    try:
        for target_path, content in proposed_writes.items():
            tmp_path = target_path.with_suffix(".merge_tmp")
            tmp_path.write_text(content, encoding="utf-8")
            tmp_files.append((tmp_path, target_path))

        # Atomic replacement
        for tmp_path, target_path in tmp_files:
            os.replace(tmp_path, target_path)

    except Exception as e:
        # Cleanup temporary files
        for tmp_path, _ in tmp_files:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass
        return False, {"error": f"Atomic write failed: {e}. Merge aborted."}

    return True, {
        "success": True,
        "total_added": total_added,
        "total_conflicts": total_conflicts,
        "total_duplicates": total_duplicates,
        "authors": sorted(list(all_authors)),
        "files": file_summaries
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministically merge teammate pending sections into main Hack Kit tables.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/merge.py .hackathon --dry-run
  python3 scripts/merge.py .hackathon
  python3 scripts/merge.py .hackathon --file ASSUMPTIONS.md
"""
    )
    parser.add_argument("folder", nargs="?", default=".hackathon", help="Path to .hackathon directory (default: .hackathon)")
    parser.add_argument("--dry-run", action="store_true", help="Preview proposed merge actions without writing to disk")
    parser.add_argument("--file", dest="target_file", default=None, help="Merge pending sections in a specific file only")
    parser.add_argument("--json", action="store_true", help="Output merge report in JSON format")

    args = parser.parse_args()

    success, res = merge_project(args.folder, dry_run=args.dry_run, target_file=args.target_file)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if success else 1)

    if not success:
        print(f"✗ Merge failed: {res.get('error')}", file=sys.stderr)
        for d in res.get("details", []):
            print(f"  - {d}", file=sys.stderr)
        sys.exit(1)

    if "message" in res:
        print(f"✓ {res['message']}")
        sys.exit(0)

    mode = "[DRY RUN] " if res.get("dry_run") else ""
    print(f"✓ {mode}Merge completed successfully:")
    print(f"  Added rows: {res.get('total_added', 0)}")
    print(f"  Conflicts flagged: {res.get('total_conflicts', 0)}")
    print(f"  Duplicates skipped: {res.get('total_duplicates', 0)}")
    if res.get("authors"):
        print(f"  Teammates: {', '.join(res['authors'])}")

    for fname, details in res.get("files", {}).items():
        if "action" in details:
            print(f"  - {fname}: {details['action']}")
        else:
            print(f"  - {fname}: {details.get('added', 0)} added, {details.get('conflicts', 0)} conflicts, {details.get('duplicates', 0)} duplicates")
            for item in details.get("conflict_items", []):
                print(f"      ! {item}")
            for item in details.get("skipped_items", []):
                print(f"      - {item}")


if __name__ == "__main__":
    main()
