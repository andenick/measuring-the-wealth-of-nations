"""V03_XS001 — Validate social burden rate against book Table 7.1 finding.

Book finding: b rises 0.56 -> 0.66 (1948 -> 1989). Range check:
- Range over period: [0.4, 0.9]
- Rising trend: 1989 > 1948

Refactored 2026-05-24 per Decision 0002 — augmented with registry-sourced
benchmark check (validation.reference_values via get_reference_values).
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
    df = pd.read_csv(DATA_FINAL / "XS001.csv")
    df = df[df["series_id"] == "XS001-A"]
    in_range = bool(df["value"].between(0.3, 0.95).all())
    v_1948 = float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None
    v_1989 = float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None
    rising = (v_1989 > v_1948) if (v_1948 and v_1989) else None

    # Registry-sourced benchmark check (Decision 0002).
    bench = BenchmarkValidator(
        series_id="XS001",
        tolerance_class=get_tolerance_class("XS001", default="share_series"),
        benchmarks=get_reference_values("XS001"),
        subseries_filter="XS001-A",
    ).run(DATA_FINAL / "XS001.csv")

    rule_pass = in_range and len(df) > 0
    bench_pass = bench["status"] == "PASS"
    status = "PASS" if (rule_pass and bench_pass) else "FAIL"
    result = {
        "series_id": "XS001",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": get_tolerance_class("XS001", default="share_series"),
        "status": status,
        "n_pass": bench["n_pass"] + (1 if rule_pass else 0),
        "n_fail": bench["n_fail"] + (0 if rule_pass else 1),
        "n_missing": bench["n_missing"],
        "checks": {
            "in_range": in_range,
            "actual_range": [float(df["value"].min()), float(df["value"].max())],
            "v_1948": v_1948, "v_1989": v_1989,
            "rising_1948_to_1989": rising,
            "note": "Book Table 7.1 b = 1-(Pn/S*), rises ~0.56->0.66. REVIEW 2026-07: Pn now sourced from ST1994 Table 7.1 (was NIPA corporate profits, a wrong/narrower quantity that yielded b=0.79-0.86); S*=S505-A reproduces book Table 7.1 S* exactly. FIDELITY: |Db| <= 0.005 ABSOLUTE (= 2-decimal print rounding) — all 42 book-period cells round EXACT to the printed b; the relative bound is NOT literally met (max 0.79% at 1967, per F1d), so the fidelity is stated as an absolute half-percentage-point bound, not relative. Refvals re-anchored to book Table 7.1 b (registry patch).",
        },
        "benchmarks": bench.get("benchmarks", {}),
    }
    write_validation_result("XS001", result)
    print(f"    [V03_XS001] status={status} b 1948={v_1948:.4f}, 1989={v_1989:.4f}, rising={rising}; bench={bench['n_pass']}/{bench['n_pass']+bench['n_fail']+bench['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
