"""V03_S201 — Validate GFP/GDP ratio range + registry benchmark check.

Refactored 2026-05-24 per Decision 0002 — augmented with registry-sourced
benchmark check.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S201.csv")
    df = df[df["series_id"] == "S201-A"]
    in_range = bool(df["value"].between(0.6, 1.0).all())

    bench = BenchmarkValidator(
        series_id="S201",
        tolerance_class=get_tolerance_class("S201", default="share_series"),
        benchmarks=get_reference_values("S201"),
        subseries_filter="S201-A",
    ).run(DATA_FINAL / "S201.csv")

    rule_pass = in_range and len(df) > 0
    status = "PASS" if (rule_pass and bench["status"] == "PASS") else "FAIL"
    result = {
        "series_id": "S201",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": get_tolerance_class("S201", default="share_series"),
        "status": status,
        "n_pass": bench["n_pass"] + (1 if rule_pass else 0),
        "n_fail": bench["n_fail"] + (0 if rule_pass else 1),
        "n_missing": bench["n_missing"],
        "checks": {
            "GFP_GDP_range_expected": [0.6, 1.0],
            "actual_range": [float(df["value"].min()), float(df["value"].max())],
            "v_1948": float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None,
            "v_1989": float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None,
        },
        "benchmarks": bench.get("benchmarks", {}),
    }
    write_validation_result("S201", result)
    print(f"    [V03_S201] status={status} GFP/GDP range=[{df['value'].min():.3f}, {df['value'].max():.3f}]; bench={bench['n_pass']}/{bench['n_pass']+bench['n_fail']+bench['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
