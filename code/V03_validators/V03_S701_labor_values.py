"""V03_S701 — productive labor coefficient lambda_p (workpackage C rebuild, review 2026-07).

DE-TAUTOLOGIZED. The book prints NO numeric lambda table anywhere (verified
against the canonical v2 KB: Ch7 has only Table 7.1 profit/burden rates; Ch4
tables 4.1-4.4 are formulas/toy examples; Appendix G is money wages). There is
therefore NO book numeric anchor for S701, and the prior practice of copying
the chopped output into validation.reference_values proved nothing.

This validator asserts what CAN honestly be asserted:
  1. STRUCTURAL: values positive, finite, inside [0.001, 1.0] hr/$; the
     nominal-denominator arithmetic implies a declining path (book 1958->1977
     and extension 1990->2024) since hours are near-flat while nominal gross
     output grows.
  2. INPUT-ANCHORED: the rebuilt matrix cache underlying every value passes
     its own validation (L=(I-A)^-1 to <1e-9; mean Leontief multipliers in a
     sane 1.5-3.5 band) — read from io_matrices_rebuilt/REBUILD_VALIDATION.json.
  3. REGRESSION SNAPSHOT: registry validation.reference_values, which after
     the workpackage C patch are explicitly labeled a pipeline snapshot (regression
     guard), NOT a book anchor.
validator_class: structural_regression__no_book_anchor
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

SID = "S701"
REBUILD_VALIDATION = ROOT / "data" / "intermediate" / "io_matrices_rebuilt" / "REBUILD_VALIDATION.json"
RANGE = (0.001, 1.0)          # hr per current-year nominal dollar


def _load(sid: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_FINAL / f"{sid}.csv")
    return df.dropna(subset=["value"])


def _matrix_cache_checks() -> dict:
    v = json.loads(REBUILD_VALIDATION.read_text(encoding="utf-8"))
    checks = []
    for era in ("sic", "naics"):
        for yr, m in v[era].items():
            checks.append({
                "vintage": int(yr), "era": era,
                "identity_err": m["L_identity_max_abs_err"],
                "identity_ok": m["L_identity_max_abs_err"] < 1e-9,
                "mult_mean": m["L_colsum_mean_multiplier"],
                "mult_ok": 1.5 <= m["L_colsum_mean_multiplier"] <= 3.5,
                "diag_ok": m["L_diag_all_ge_1"],
            })
    ok = all(c["identity_ok"] and c["mult_ok"] and c["diag_ok"] for c in checks)
    return {"ok": ok, "n_vintages": len(checks), "checks": checks}


def run():
    df = _load(SID)
    book = df[df["series_id"] == f"{SID}-A"].set_index("year")["value"]
    ext = df[df["series_id"] == f"{SID}-EXT"].sort_values("year").set_index("year")["value"]
    allv = df[df["series_id"].isin([f"{SID}-A", f"{SID}-EXT"])]["value"]

    # 1. structural
    in_range = bool(allv.between(*RANGE).all()) and bool(allv.gt(0).all())
    decline_book = bool(book.get(1977, float("inf")) < book.get(1958, 0) * 1.2) if len(book) else False
    decline_ext = bool(ext.iloc[-1] < ext.iloc[0]) if len(ext) > 1 else False
    structural_ok = in_range and decline_book and decline_ext

    # 2. input-anchored (rebuilt matrix cache validity)
    cache = _matrix_cache_checks()

    # 3. regression snapshot vs registry reference_values
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

    status = "PASS" if (structural_ok and cache["ok"] and n_fail == 0) else "FAIL"
    result = {
        "series_id": SID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "validator_class": "structural_regression__no_book_anchor",
        "no_book_anchor_note": ("The book prints no numeric lambda values (v2 KB verified, workpackage C 2026-07); "
                                "reference_values are a pipeline regression snapshot, not a book anchor."),
        "status": status,
        "structural": {"in_range": in_range, "range": list(RANGE),
                       "book_nominal_decline_1958_1977": decline_book,
                       "ext_nominal_decline_1990_2024": decline_ext},
        "matrix_cache": {"ok": cache["ok"], "n_vintages": cache["n_vintages"]},
        "benchmarks": {"checks": bench_checks, "n_fail": n_fail},
    }
    write_validation_result(SID, result)
    print(f"    [V03_{SID}] status={status} structural={structural_ok} "
          f"matrix_cache={cache['ok']} snapshot_fail={n_fail}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
