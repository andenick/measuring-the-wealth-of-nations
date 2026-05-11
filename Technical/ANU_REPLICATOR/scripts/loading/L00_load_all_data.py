#!/usr/bin/env python3
"""L00 - Load All Data: discovers and runs all L## scripts in order.

Outputs:
  - data/parsed-raw/LOAD_LOG.json (run log with per-script results)
Dependencies: None (orchestrator — runs L01-L14 in filename order)
"""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import RAW_DATA, SCRIPTS_LOADING, ensure_dirs
from lib.reporting.console_reporter import print_load_summary


def run_all(series_filter=None):
    """Discover and execute every L01-L99 loader, returning combined results."""
    ensure_dirs()
    scripts = sorted(SCRIPTS_LOADING.glob("L[0-9][0-9]_*.py"))
    scripts = [s for s in scripts if s.name != "L00_load_all_data.py"]

    results = []
    for script in scripts:
        module_name = script.stem
        spec = importlib.util.spec_from_file_location(module_name, script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Support both SERIES_ID (single) and SERIES_IDS (list)
        if series_filter:
            mod_ids = getattr(mod, "SERIES_IDS", None) or []
            if hasattr(mod, "SERIES_ID"):
                mod_ids = mod_ids + [mod.SERIES_ID]
            if mod_ids and not any(sid in series_filter for sid in mod_ids):
                continue

        try:
            result = mod.load()
        except Exception as exc:
            result = {
                "series_id": getattr(mod, "SERIES_ID", module_name),
                "status": "fail",
                "message": f"Unhandled error: {exc}",
                "outputs": [],
            }
        results.append(result)

    log = {
        "run_date": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }
    log_path = RAW_DATA / "LOAD_LOG.json"
    log_path.write_text(json.dumps(log, indent=2, default=str))

    print_load_summary(results)
    return results


if __name__ == "__main__":
    run_all()
