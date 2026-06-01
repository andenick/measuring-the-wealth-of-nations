"""V03_S608 — Validate NSW/V* ratio: identity round-trip + registry benchmarks.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
Upgraded from identity-only to also check year-by-year reference values.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_validation_result  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import TOLERANCES  # noqa: E402


SERIES_ID = "S608"


def run():
    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s608 = pd.read_csv(DATA_FINAL / "S608.csv")
    s607 = s607[s607["series_id"] == "S607-A"][["year", "value"]].rename(columns={"value": "NSW"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    s608_a = s608[s608["series_id"] == "S608-A"][["year", "value"]].rename(columns={"value": "ratio"})

    overlap = s607.merge(s504, on="year").merge(s608_a, on="year")
    overlap["implied"] = overlap["NSW"] / overlap["V_star"]
    overlap["abs_err"] = (overlap["implied"] - overlap["ratio"]).abs()

    max_err = float(overlap["abs_err"].max()) if len(overlap) else None
    identity_pass = (max_err is None or max_err < 1e-6)

    # Registry benchmark check (per Decision 0002)
    benchmarks = get_reference_values(SERIES_ID)
    by_year = dict(zip(s608_a["year"].astype(int), s608_a["ratio"].astype(float)))
    tol = TOLERANCES["rate_series"]
    bench_checks = []
    for yr, expected in benchmarks.items():
        actual = by_year.get(yr)
        if actual is None:
            bench_checks.append({"year": yr, "expected": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        bench_checks.append({
            "year": yr, "expected": expected, "actual": round(actual, 6),
            "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
            "status": "PASS" if ok else "FAIL",
        })
    n_bench_pass = sum(1 for c in bench_checks if c["status"] == "PASS")
    n_bench_fail = sum(1 for c in bench_checks if c["status"] == "FAIL")
    n_bench_miss = sum(1 for c in bench_checks if c["status"] == "MISSING")

    status = "PASS" if (identity_pass and n_bench_fail == 0 and n_bench_miss == 0) else "FAIL"

    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "rel_tol": tol["rel"], "abs_tol": tol["abs"],
        "status": status,
        "n_pass": n_bench_pass,
        "n_fail": n_bench_fail,
        "n_missing": n_bench_miss,
        "identity_check": {
            "identity": "S608 = S607 / S504 (NSW / V*)",
            "compared_years": len(overlap),
            "max_abs_err": max_err,
            "status": "PASS" if identity_pass else "FAIL",
        },
        "benchmarks": {"checks": bench_checks},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} identity_max_err={max_err} bench_pass={n_bench_pass}/{n_bench_pass+n_bench_fail+n_bench_miss}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
