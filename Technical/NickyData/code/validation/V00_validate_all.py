#!/usr/bin/env python3
"""V00 - Validate All: discovers and runs V01-V08 scripts in order.

Outputs:
  - data/final-data/logs/VALIDATION_REPORT.json
Dependencies: P00 must complete (final series data must exist)
"""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import LOGS, SCRIPTS_VALIDATION, ensure_dirs


def run_validation(series_filter=None, chapter_filter=None):
    """Discover and execute every V01-V08 validator, returning combined results."""
    ensure_dirs()
    scripts = sorted(SCRIPTS_VALIDATION.glob("V[0-9][0-9]_*.py"))
    scripts = [s for s in scripts if s.name != "V00_validate_all.py"]

    results = []
    total_pass = 0
    total_fail = 0
    total_warn = 0
    total_skip = 0

    print(f"\n  Found {len(scripts)} validation scripts")
    print()

    for script in scripts:
        module_name = script.stem
        spec = importlib.util.spec_from_file_location(module_name, script)
        mod = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(mod)
            result = mod.validate(
                series_filter=series_filter,
                chapter_filter=chapter_filter,
            )
        except Exception as exc:
            result = {
                "validator": module_name,
                "status": "error",
                "message": f"Unhandled error: {exc}",
                "checks": [],
            }

        results.append(result)
        for check in result.get("checks", []):
            s = check.get("status", "")
            if s == "PASS":
                total_pass += 1
            elif s == "FAIL":
                total_fail += 1
            elif s == "WARN":
                total_warn += 1
            elif s == "SKIP":
                total_skip += 1

        status = result.get("status", "?")
        n_checks = len(result.get("checks", []))
        label = "PASS" if status == "pass" else status.upper()
        print(f"    {module_name}: {label} ({n_checks} checks)")

    # Write VALIDATION_REPORT.json
    report = {
        "version": "1.0.0",
        "project": "AS2",
        "generated": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_checks": total_pass + total_fail + total_warn + total_skip,
            "pass": total_pass,
            "fail": total_fail,
            "warn": total_warn,
            "skip": total_skip,
            "overall": "PASS" if total_fail == 0 else "FAIL",
        },
        "validators": results,
    }

    report_path = LOGS / "VALIDATION_REPORT.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)

    print()
    print(f"  Validation: {total_pass} PASS, {total_fail} FAIL, "
          f"{total_warn} WARN, {total_skip} SKIP")
    print(f"  Report: {report_path}")

    return report


if __name__ == "__main__":
    run_validation()
