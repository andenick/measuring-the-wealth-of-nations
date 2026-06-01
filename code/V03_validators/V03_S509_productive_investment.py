"""V03_S509 — Validate Productive Investment (IG*) against registry benchmark.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
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


SERIES_ID = "S509"


def run():
    """Validate S509 against registry-supplied benchmark year(s)."""
    final_csv = DATA_FINAL / f"{SERIES_ID}.csv"
    df = pd.read_csv(final_csv)
    df = df[df["series_id"] == "S509-A"]

    benchmarks = get_reference_values(SERIES_ID)
    if not benchmarks:
        raise RuntimeError(f"No reference_values found for {SERIES_ID} in registry")

    # Use 1948 as the canonical round-trip benchmark when present; otherwise pick the
    # earliest available year. Tolerance: dollar_series abs_tol = 1.0; here we tighten
    # to 0.01 because S509 is a direct E.2 round-trip and any drift is digitization noise.
    benchmark_year = 1948 if 1948 in benchmarks else min(benchmarks)
    expected = benchmarks[benchmark_year]
    actual = float(df[df["year"] == benchmark_year]["value"].iloc[0])

    abs_err = abs(actual - expected)
    status = "PASS" if abs_err < 0.01 else "FAIL"

    result = {
        "series_id":       SERIES_ID,
        "run_at":          datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "dollar_series",
        "status":          status,
        "n_pass":          1 if status == "PASS" else 0,
        "n_fail":          0 if status == "PASS" else 1,
        "n_missing":       0,
        "range_check":     {"year": benchmark_year, "value": actual, "expected": expected,
                            "abs_err": abs_err,
                            "note": "Round-trip check against registry reference_values "
                                    "(E.2 row value)."},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_S509] status={status} val_{benchmark_year}={actual:.2f}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
