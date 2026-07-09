"""V03_XS004 — productivity must rise over book period (Marxian q* growth).

Refactored 2026-05-24 per Decision 0002 — augmented with registry-sourced
benchmark check.
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
    df = pd.read_csv(DATA_FINAL / "XS004.csv")
    df = df[df["series_id"] == "XS004-A"].sort_values("year")
    first_v = float(df.iloc[0]["value"])
    last_v  = float(df.iloc[-1]["value"])
    rising = last_v > first_v
    growth_pct = (last_v / first_v - 1) * 100

    bench = BenchmarkValidator(
        series_id="XS004",
        tolerance_class=get_tolerance_class("XS004", default="share_series"),
        benchmarks=get_reference_values("XS004"),
        subseries_filter="XS004-A",
    ).run(DATA_FINAL / "XS004.csv")

    rule_pass = rising and len(df) >= 10
    status = "PASS" if (rule_pass and bench["status"] == "PASS") else "FAIL"
    result = {
        "series_id": "XS004",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": get_tolerance_class("XS004", default="share_series"),
        "status": status,
        "n_pass": bench["n_pass"] + (1 if rule_pass else 0),
        "n_fail": bench["n_fail"] + (0 if rule_pass else 1),
        "n_missing": bench["n_missing"],
        "trend_check": {"first_value": first_v, "last_value": last_v,
                        "growth_pct": growth_pct, "rising": rising,
                        "n_years": len(df)},
        "benchmarks": bench.get("benchmarks", {}),
    }
    write_validation_result("XS004", result)
    print(f"    [V03_XS004] status={status} q*: {df.iloc[0]['year']}={first_v:.2f} -> {df.iloc[-1]['year']}={last_v:.2f} ({growth_pct:+.1f}%); bench={bench['n_pass']}/{bench['n_pass']+bench['n_fail']+bench['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
