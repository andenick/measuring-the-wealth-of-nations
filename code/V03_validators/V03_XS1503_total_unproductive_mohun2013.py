"""V03_XS1503 — Validate Mohun (2013) total unproductive employment share.

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from registry.
D4 REBUILD (2026-07-02): series is now a SHARE of total employment (Mohun Fig 1);
benchmarks 1964=0.420, 2003=0.490, 2010=0.475 are EXTERNAL Mohun anchors.
Adds the decomposition IDENTITY check XS1501-A + XS1502-A == XS1503-A at the
overlapping benchmark year 1964 (honest, non-tautological). Default tol -> share_series.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.registry_validator import get_reference_values, get_tolerance_class
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="XS1503",
    tolerance_class=get_tolerance_class("XS1503", default="share_series"),
    benchmarks=get_reference_values("XS1503"),
    subseries_filter="XS1503-A",
)


def _identity_check(tol: float = 2.0e-3) -> dict:
    """XS1501-A + XS1502-A == XS1503-A at years where all three exist.

    Mohun publishes total (Fig 1) and the two components (Figs 2-3) separately,
    all figure-read, so the identity is checked to a figure-rounding tolerance.
    Only 1964 has all three benchmark values.
    """
    def load(sid):
        df = pd.read_csv(DATA_FINAL / f"{sid}.csv")
        df = df[df["series_id"] == f"{sid}-A"]
        return dict(zip(df["year"].astype(int), df["value"].astype(float)))
    a, b, c = load("XS1501"), load("XS1502"), load("XS1503")
    years = sorted(set(a) & set(b) & set(c))
    checks = []
    for y in years:
        diff = abs(a[y] + b[y] - c[y])
        checks.append({"year": y, "sum_components": round(a[y] + b[y], 4),
                       "total": round(c[y], 4), "abs_diff": round(diff, 5),
                       "status": "PASS" if diff <= tol else "FAIL"})
    status = "PASS" if all(k["status"] == "PASS" for k in checks) and checks else \
             ("SKIP" if not checks else "FAIL")
    return {"status": status, "tol": tol, "checks": checks}


def run():
    result = VALIDATOR.run(DATA_FINAL / "XS1503.csv")
    ident = _identity_check()
    result["identity_check"] = ident
    if ident["status"] == "FAIL":
        result["status"] = "FAIL"
    print(f"    [V03_XS1503] status={result['status']} "
          f"bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']} "
          f"identity={ident['status']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
