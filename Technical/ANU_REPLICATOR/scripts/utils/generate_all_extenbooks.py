#!/usr/bin/env python3
"""Generate Extenbook Excel workbooks for all processed series.

Reads processing results and the series registry to produce 4-sheet
Excel workbooks (Data, Provenance, Research, Construction) per series.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.config_loader import load_registry
from lib.formats.extenbook_writer import write_extenbook
from lib.paths import EXTENBOOKS, LOGS


def main():
    registry = load_registry()

    # Read the most recent process log to get data_dicts
    log_path = LOGS / "PROCESS_LOG.json"
    if not log_path.exists():
        print("  No PROCESS_LOG.json found. Run the pipeline first.")
        return

    with open(log_path, encoding="utf-8") as f:
        process_log = json.load(f)

    results = process_log.get("results", [])
    written = 0

    for result in results:
        sid = result.get("series_id")
        if not sid or sid not in registry.get("series", {}):
            continue
        data_dict = result.get("data_dict")
        if not data_dict:
            continue

        research_path = Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "research" / f"{sid}_research.json"
        research_data = None
        if research_path.exists():
            with open(research_path, encoding="utf-8") as f:
                research_data = json.load(f)

        out = write_extenbook(data_dict, registry, research_data, sid, EXTENBOOKS)
        print(f"  [extenbook] {sid} -> {out.name}")
        written += 1

    print(f"\n  {written} extenbooks written to {EXTENBOOKS}")


if __name__ == "__main__":
    main()
