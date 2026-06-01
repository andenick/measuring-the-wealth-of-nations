r"""
DPR Status Sync
================

Syncs each DPR file's `**Status**:` header line with the canonical
`status` field in series_registry.json.

Behavior per DPR
----------------
* Parse first line in the file that matches the regex
  ``^(?:- )?\*\*Status\*\*:\s*`?([A-Za-z0-9_]+)`?``.
* If the parsed status equals the registry status: skip (already correct).
* If different: rewrite that single line in place, preserving the original
  bullet style (``- **Status**: `value` ...`` vs ``**Status**: value ...``)
  and any trailing annotation (text in parens or after the value token).
* If no Status line exists at all: insert ``**Status**: <value>`` directly
  after the title block (line that starts with ``# `` plus one blank).

Constraints
-----------
* series_registry.json is read-only.
* Only DPR files in Technical/docs/series/ may be modified.
* All other content of each DPR is preserved byte-for-byte.

Usage
-----
    python Technical/code/utils/dpr_status_sync.py
        [--dry-run]
        [--registry PATH]
        [--series-dir PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = PROJECT_ROOT / "Technical" / "series_registry.json"
DEFAULT_SERIES_DIR = PROJECT_ROOT / "Technical" / "docs" / "series"

# Captures: optional bullet, the status token (with or without backticks),
# and any trailing annotation we want to preserve.
STATUS_LINE_RE = re.compile(
    r"^(?P<prefix>(?:-\s+)?\*\*Status\*\*:\s*)"
    r"(?P<backtick_open>`?)"
    r"(?P<value>[A-Za-z0-9_]+)"
    r"(?P<backtick_close>`?)"
    r"(?P<trailing>.*)$"
)


def load_registry(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def sync_dpr(dpr_path: Path, target_status: str) -> str:
    """Returns one of: 'already-correct', 'synced', 'inserted', 'skipped'."""
    text = dpr_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=False)
    newline_terminated = text.endswith("\n")

    # Try to find an existing parseable status line.
    for idx, line in enumerate(lines):
        m = STATUS_LINE_RE.match(line)
        if not m:
            continue
        current = m.group("value")
        if current == target_status:
            return "already-correct"
        # Rewrite this single line, preserving prefix/backticks/trailing.
        new_line = (
            m.group("prefix")
            + m.group("backtick_open")
            + target_status
            + m.group("backtick_close")
            + m.group("trailing")
        )
        lines[idx] = new_line
        new_text = "\n".join(lines) + ("\n" if newline_terminated else "")
        dpr_path.write_text(new_text, encoding="utf-8")
        return "synced"

    # No status line found anywhere. Insert one after the first title block.
    insert_at = None
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            # Insert after the title line and any single trailing blank line.
            insert_at = idx + 1
            # If the next line is blank, insert after the blank so layout is:
            #   # Title
            #
            #   **Status**: ...
            #
            if insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            break
    if insert_at is None:
        # File has no title heading; refuse to guess.
        return "skipped"

    new_status_line = f"**Status**: {target_status}"
    new_block = [new_status_line, ""]
    lines[insert_at:insert_at] = new_block
    new_text = "\n".join(lines) + ("\n" if newline_terminated else "")
    dpr_path.write_text(new_text, encoding="utf-8")
    return "inserted"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--series-dir", type=Path, default=DEFAULT_SERIES_DIR)
    parser.add_argument("--dry-run", action="store_true",
                        help="Report intended actions without writing.")
    args = parser.parse_args(argv)

    registry = load_registry(args.registry)
    series = registry.get("series", {})
    if not series:
        print("ERROR: registry has no 'series' section", file=sys.stderr)
        return 2

    counts = {"already-correct": 0, "synced": 0, "inserted": 0,
              "skipped": 0, "missing-dpr": 0, "missing-status-in-registry": 0}
    detail = []

    for sid in sorted(series):
        entry = series[sid]
        target = entry.get("status")
        if not target:
            counts["missing-status-in-registry"] += 1
            detail.append((sid, "missing-status-in-registry", None))
            continue
        dpr_path = args.series_dir / f"{sid}_DPR.md"
        if not dpr_path.exists():
            counts["missing-dpr"] += 1
            detail.append((sid, "missing-dpr", target))
            continue
        if args.dry_run:
            # Read-only probe.
            text = dpr_path.read_text(encoding="utf-8")
            found = None
            for line in text.splitlines():
                m = STATUS_LINE_RE.match(line)
                if m:
                    found = m.group("value")
                    break
            if found is None:
                outcome = "inserted"
            elif found == target:
                outcome = "already-correct"
            else:
                outcome = "synced"
        else:
            outcome = sync_dpr(dpr_path, target)
        counts[outcome] += 1
        if outcome not in ("already-correct",):
            detail.append((sid, outcome, target))

    print("DPR Status Sync Summary")
    print("=" * 60)
    print(f"  already-correct:           {counts['already-correct']}")
    print(f"  synced (rewritten):        {counts['synced']}")
    print(f"  inserted (new line):       {counts['inserted']}")
    print(f"  skipped (no title block):  {counts['skipped']}")
    print(f"  missing-dpr file:          {counts['missing-dpr']}")
    print(f"  missing-status in reg:     {counts['missing-status-in-registry']}")
    print()
    if detail:
        print("Detail (non-no-op rows):")
        for sid, outcome, target in detail:
            print(f"  {sid:<8} {outcome:<28} -> {target}")
    if args.dry_run:
        print("\n[dry-run] no files were modified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
