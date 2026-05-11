#!/usr/bin/env python3
"""M00 - Apply All Adjustments: discovers and runs M01+ scripts in order.

Reads ADJUSTMENT_MANIFEST.json for pending adjustments, then discovers and
executes M01-M99 scripts. Outputs adjusted data to data/adjusted-final-data/.

Outputs:
  - data/adjusted-final-data/ (adjusted series CSVs)
  - config/ADJUSTMENT_MANIFEST.json (updated with execution results)
Dependencies: V00 should complete first (validate before adjusting)
"""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import CONFIG, ADJUSTED, SCRIPTS_MANUAL, ensure_dirs


def _load_manifest():
    manifest_path = CONFIG / "ADJUSTMENT_MANIFEST.json"
    if not manifest_path.exists():
        return {"version": "1.0", "adjustments": [], "pending": []}
    with open(manifest_path, encoding="utf-8") as f:
        return json.load(f)


def run_all(series_filter=None):
    """Discover and execute every M01-M99 adjustment script."""
    ensure_dirs()
    ADJUSTED.mkdir(parents=True, exist_ok=True)

    manifest = _load_manifest()
    pending = [p for p in manifest.get("pending", []) if p.get("status") == "READY"]

    if not pending:
        print("    No READY adjustments in manifest. Skipping M## phase.")
        return []

    scripts = sorted(SCRIPTS_MANUAL.glob("M[0-9][0-9]_*.py"))
    scripts = [s for s in scripts if s.name != "M00_apply_adjustments.py"]

    if not scripts:
        print(f"    {len(pending)} pending adjustment(s) but no M01+ scripts found.")
        return []

    results = []
    for script in scripts:
        module_name = script.stem
        spec = importlib.util.spec_from_file_location(module_name, script)
        mod = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(mod)
            result = mod.adjust(series_filter=series_filter)
        except Exception as exc:
            result = {
                "script": module_name,
                "status": "fail",
                "message": f"Unhandled error: {exc}",
            }

        results.append(result)
        status = result.get("status", "?")
        print(f"    {module_name}: {status.upper()}")

    return results


if __name__ == "__main__":
    run_all()
