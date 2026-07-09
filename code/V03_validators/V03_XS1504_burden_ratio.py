"""V03_XS1504 — Validate Mohun (2013) burden ratio Lu/Lp range + benchmark check.

Refactored 2026-05-24 per Decision 0002.
D4 REBUILD (2026-07-02): ratio now derived from Mohun's OWN published shares
(XS1503) over 1964-2010; benchmarks 1964=0.724, 2003=0.961, 2010=0.905 are
EXTERNAL Mohun anchors (non-tautological). Default tol -> share_series. Structural
range check [0.5, 2.0] retained. ST/Mohun comparison recorded in DIV-058.
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
    df = pd.read_csv(DATA_FINAL / "XS1504.csv")
    df = df[df["series_id"] == "XS1504-A"]
    in_range = bool(df["value"].between(0.5, 2.0).all())

    bench = BenchmarkValidator(
        series_id="XS1504",
        tolerance_class=get_tolerance_class("XS1504", default="share_series"),
        benchmarks=get_reference_values("XS1504"),
        subseries_filter="XS1504-A",
    ).run(DATA_FINAL / "XS1504.csv")

    rule_pass = in_range and len(df) > 0
    status = "PASS" if (rule_pass and bench["status"] == "PASS") else "FAIL"
    result = {
        "series_id": "XS1504",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": get_tolerance_class("XS1504", default="share_series"),
        "status": status,
        "n_pass": bench["n_pass"] + (1 if rule_pass else 0),
        "n_fail": bench["n_fail"] + (0 if rule_pass else 1),
        "n_missing": bench["n_missing"],
        "range_check": {"expected": [0.5, 2.0], "actual_min": float(df["value"].min()), "actual_max": float(df["value"].max())},
        "benchmarks": bench.get("benchmarks", {}),
    }
    write_validation_result("XS1504", result)
    print(f"    [V03_XS1504] status={status} range=[{df['value'].min():.4f}, {df['value'].max():.4f}]; bench={bench['n_pass']}/{bench['n_pass']+bench['n_fail']+bench['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
