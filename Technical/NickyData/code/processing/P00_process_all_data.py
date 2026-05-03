#!/usr/bin/env python3
"""P00 - Process All Data: discovers and runs all P## scripts in PRIORITY order.

Outputs:
  - data/logs/PROCESS_LOG.json (structured run log)
  - data/reports/REPLICATION_REPORT.md (human-readable report)
Dependencies: None (orchestrator — runs P01-P15 sorted by PRIORITY attribute)
"""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import FINAL_DATA, LOGS, REPORTS, ensure_dirs
from utils.config_loader import load_registry
from utils.reporting.console_reporter import print_process_summary
from utils.formats.report_generator import generate_replication_report

SCRIPTS_DIR = Path(__file__).resolve().parent


def run_all(series_filter=None):
    """Discover and execute every P01-P99 processor, returning combined results."""
    ensure_dirs()
    registry = load_registry()

    scripts = sorted(SCRIPTS_DIR.glob("P[0-9][0-9]_*.py"))
    scripts = [s for s in scripts if s.name != "P00_process_all_data.py"]

    # Load all modules first, then sort by PRIORITY attribute
    modules = []
    for script in scripts:
        module_name = script.stem
        spec = importlib.util.spec_from_file_location(module_name, script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        modules.append((script, mod))

    modules.sort(key=lambda x: (getattr(x[1], "PRIORITY", 50), x[0].name))

    results = []
    for script, mod in modules:
        # Support both SERIES_ID (single) and SERIES_IDS (list)
        if series_filter:
            mod_ids = getattr(mod, "SERIES_IDS", None) or []
            if hasattr(mod, "SERIES_ID"):
                mod_ids = mod_ids + [mod.SERIES_ID]
            if mod_ids and not any(sid in series_filter for sid in mod_ids):
                continue

        try:
            result = mod.process()
        except Exception as e:
            result = {
                "series_id": getattr(mod, "SERIES_ID", module_name),
                "status": "fail",
                "error": str(e),
                "steps": [],
                "outputs": [],
            }
        results.append(result)

    log = {
        "run_date": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": "1.0.0",
        "series_filter": series_filter,
        "total_series": len(results),
        "passed": sum(1 for r in results if r.get("status") == "ok"),
        "warnings": sum(1 for r in results if r.get("status") == "warn"),
        "failed": sum(1 for r in results if r.get("status") == "fail"),
        "results": results,
    }
    log_path = LOGS / "PROCESS_LOG.json"
    log_path.write_text(json.dumps(log, indent=2, default=str))

    report_path = REPORTS / "REPLICATION_REPORT.md"
    generate_replication_report(results, report_path)

    print_process_summary(results)
    return results


if __name__ == "__main__":
    filter_ids = sys.argv[1:] if len(sys.argv) > 1 else None
    run_all(series_filter=filter_ids)
