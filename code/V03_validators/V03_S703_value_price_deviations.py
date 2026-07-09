"""V03_S703 -- productive/unproductive labor-coefficient partition gap (workpackage C v2.0).

DE-TAUTOLOGIZED + DE-CONFLATED. What S703 computes is the output-weighted gap
between the unproductive and productive partitions' embodied-labor-per-dollar
coefficients -- NOT the book's Khanjian value-price deviation. The book's actual
concept (Table 5.12, p.144: e = S/V vs e* = S*/V* on the SAME aggregate,
deviations 5.7-9.3%) is stored at
data/source/book_tables/S703_Table512_khanjian_deviations.csv as the anchor a
FUTURE faithful implementation must hit; it is NEVER compared against the
partition-gap series here (registered divergence DIV-C10).

Checks: (1) structural range [-100, 50] percent; (2) rebuilt-matrix-cache
validity (same as V03_S701); (3) regression snapshot vs registry
reference_values (pipeline snapshot, not book).
validator_class: structural_regression__book_concept_divergent
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL, ROOT  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import TOLERANCES  # noqa: E402

SID = "S703"
REBUILD_VALIDATION = ROOT / "data" / "intermediate" / "io_matrices_rebuilt" / "REBUILD_VALIDATION.json"
RANGE = (-100.0, 50.0)


def run():
    df = pd.read_csv(DATA_FINAL / f"{SID}.csv").dropna(subset=["value"])
    allv = df[df["series_id"].isin([f"{SID}-A", f"{SID}-EXT"])]["value"]
    in_range = bool(allv.between(*RANGE).all())

    v = json.loads(REBUILD_VALIDATION.read_text(encoding="utf-8"))
    cache_ok = all(
        m["L_identity_max_abs_err"] < 1e-9 and 1.5 <= m["L_colsum_mean_multiplier"] <= 3.5
        for era in ("sic", "naics") for m in v[era].values()
    )

    tol = TOLERANCES["rate_series"]
    sub = df[df["series_id"].isin([f"{SID}-A", f"{SID}-EXT", f"{SID}-COMBINED"])]
    by_year = dict(zip(sub["year"].astype(int), sub["value"].astype(float)))
    bench_checks = []
    for yr, expected in get_reference_values(SID).items():
        actual = by_year.get(int(yr))
        if actual is None:
            bench_checks.append({"year": yr, "expected": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        bench_checks.append({"year": yr, "expected": expected, "actual": round(actual, 6),
                             "rel_err": round(rel_err, 6), "status": "PASS" if ok else "FAIL"})
    n_fail = sum(1 for c in bench_checks if c["status"] != "PASS")

    status = "PASS" if (in_range and cache_ok and n_fail == 0) else "FAIL"
    result = {
        "series_id": SID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "validator_class": "structural_regression__book_concept_divergent",
        "book_concept_note": ("Khanjian 6-9% (Table 5.12) compares S/V vs S*/V* on the same aggregate "
                              "and is NOT comparable to this partition-gap series (DIV-C10). Anchor file: "
                              "data/source/book_tables/S703_Table512_khanjian_deviations.csv"),
        "status": status,
        "structural": {"in_range": in_range, "range": list(RANGE)},
        "matrix_cache_ok": cache_ok,
        "benchmarks": {"checks": bench_checks, "n_fail": n_fail},
    }
    write_validation_result(SID, result)
    print(f"    [V03_{SID}] status={status} in_range={in_range} cache={cache_ok} snapshot_fail={n_fail}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
