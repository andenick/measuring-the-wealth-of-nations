"""V03_ES1302 — NSW/EC Moos range check + registry benchmark check.

Refactored 2026-05-24 per Decision 0002.
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL
from utils.registry_validator import get_reference_values, get_tolerance_class
from utils.series import BenchmarkValidator

def run():
    df = pd.read_csv(DATA_FINAL / "ES1302.csv")
    df = df[df["series_id"] == "ES1302-A"]
    in_range = bool(df["value"].between(-0.20, 0.20).all())

    bench = BenchmarkValidator(
        series_id="ES1302",
        tolerance_class=get_tolerance_class("ES1302", default="share_series"),
        benchmarks=get_reference_values("ES1302"),
        subseries_filter="ES1302-A",
    ).run(DATA_FINAL / "ES1302.csv")

    rule_pass = in_range and len(df) > 0
    status = "PASS" if (rule_pass and bench["status"] == "PASS") else "FAIL"
    result = {
        "series_id": "ES1302",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": get_tolerance_class("ES1302", default="share_series"),
        "status": status,
        "n_pass": bench["n_pass"] + (1 if rule_pass else 0),
        "n_fail": bench["n_fail"] + (0 if rule_pass else 1),
        "n_missing": bench["n_missing"],
        "range_check": {"expected": [-0.20, 0.20], "actual": [float(df["value"].min()), float(df["value"].max())]},
        "benchmarks": bench.get("benchmarks", {}),
    }
    write_validation_result("ES1302", result)
    print(f"    [V03_ES1302] status={status} range=[{df['value'].min():.4f}, {df['value'].max():.4f}]; bench={bench['n_pass']}/{bench['n_pass']+bench['n_fail']+bench['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
