"""S03 - Generate VALIDATION_REPORT.json scaffold.

Aggregates results from V## validators into a single report per series.
Validators write per-series JSON into data/intermediate/validation/{S###}.json
when they run. This script reads those and rolls them up.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "series_registry.json"
VAL_DIR = ROOT / "data" / "intermediate" / "validation"
REPORT = ROOT / "VALIDATION_REPORT.json"


def load_per_series_results() -> dict[str, dict]:
    if not VAL_DIR.is_dir():
        return {}
    results: dict[str, dict] = {}
    for f in VAL_DIR.glob("*.json"):
        try:
            results[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
    return results


def run() -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    series_ids = list(reg.get("series", {}).keys())
    per_series = load_per_series_results()

    rollup = {sid: {"status": "not_run"} for sid in series_ids}
    for sid, res in per_series.items():
        if sid in rollup:
            rollup[sid] = res

    by_status: dict[str, int] = {}
    for r in rollup.values():
        by_status[r.get("status", "not_run")] = by_status.get(r.get("status", "not_run"), 0) + 1

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "registry_version": reg.get("version"),
        "series_count": len(series_ids),
        "by_status": by_status,
        "results": rollup,
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"    [S03] Validation report: {len(series_ids)} series; status counts = {by_status}")
    return report


if __name__ == "__main__":
    run()
