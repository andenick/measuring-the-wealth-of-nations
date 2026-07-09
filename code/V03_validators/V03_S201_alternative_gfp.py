"""V03_S201 — Validate the Marxian GFP*/GDP ratio.

DE-TAUTOLOGISED 2026-07 (review workpackage D). S201-A is the annual ratio
GFP* / orthodox GDP, where GFP* = this project's S503 (Marxian gross final
product) and GDP = BEA NIPA 1.7.5 line 1. There is NO book "Table 2.1"
(Chapter 2 is purely theoretical and prints no tables); the in-book analogue
is Figure 5.4 / Table 5.4 row "GFP*/GNP". The series is a DERIVED ratio, so
it is validated by two INDEPENDENT anchors — never against its own chopped
output (the previous `get_reference_values` benchmarks were verbatim copies of
S201's own chopped column, i.e. tautological):

  1. COMPONENT IDENTITY — recompute GFP*/GDP from the two upstream inputs
     (S503 final CSV and the NIPA GDP loader) and require S201-A == that ratio
     to floating tolerance. Neither input is S201's own output.

  2. BOOK ANCHOR — the numerator S503 (project GFP*) must equal the book's
     reconciled GFP* at the I-O benchmark years, taken from the KB v2
     benchmark reconciliation
     (Technical/book_digitization_v2/benchmark_reconciled.csv,
     variable_id GFP_star, basis Table 5.3 NIPA). This ties S201's numerator
     to the printed book, so the ratio is book-anchored end-to-end.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S201_alternative_gfp import load_nipa_aggregates  # noqa: E402
from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_tolerance_class  # noqa: E402

# Book GFP* (aggregate, $bn) at the six I-O benchmark years, reconciled in KB v2
# from ST 1994 Table 5.3 (NIPA basis). 1947 precedes the S201 1948-1989 span
# and is omitted. Source of record:
#   book_digitization_v2/benchmark_reconciled.csv
BOOK_GFP_STAR = {
    1958: 403.67,
    1963: 523.74,
    1967: 699.15,
    1972: 1014.08,
    1977: 1690.83,
}
BOOK_TOL_ABS = 0.5      # $0.5bn — book values carry two decimals
IDENTITY_TOL_ABS = 1e-6  # S201-A must equal recomputed S503/GDP


def run():
    df = pd.read_csv(DATA_FINAL / "S201.csv")
    df = df[df["series_id"] == "S201-A"][["year", "value"]]
    in_range = bool(df["value"].between(0.6, 1.0).all()) and len(df) > 0

    # --- Anchor 1: component identity S201-A == S503-A / GDP ------------------
    nipa = load_nipa_aggregates()[["year", "GDP"]]
    s503 = pd.read_csv(DATA_FINAL / "S503.csv")
    s503 = s503[s503["series_id"] == "S503-A"][["year", "value"]].rename(
        columns={"value": "GFP_star"})
    recomputed = s503.merge(nipa, on="year", how="inner")
    recomputed["ratio"] = recomputed["GFP_star"] / recomputed["GDP"]
    ident = df.merge(recomputed[["year", "ratio"]], on="year", how="inner")
    ident["abs_err"] = (ident["value"] - ident["ratio"]).abs()
    identity_max_err = float(ident["abs_err"].max()) if len(ident) else float("nan")
    identity_pass = bool(len(ident) >= 30 and identity_max_err <= IDENTITY_TOL_ABS)

    # --- Anchor 2: numerator S503 == book GFP* at benchmark years ------------
    book_checks = []
    s503_by_year = dict(zip(s503["year"].astype(int), s503["GFP_star"].astype(float)))
    for yr, book_val in sorted(BOOK_GFP_STAR.items()):
        actual = s503_by_year.get(yr)
        if actual is None:
            book_checks.append({"year": yr, "book_GFP_star": book_val,
                                "status": "MISSING"})
            continue
        abs_err = abs(actual - book_val)
        book_checks.append({
            "year": yr, "book_GFP_star": book_val,
            "project_S503": round(actual, 4), "abs_err": round(abs_err, 4),
            "status": "PASS" if abs_err <= BOOK_TOL_ABS else "FAIL",
        })
    n_book_pass = sum(1 for c in book_checks if c["status"] == "PASS")
    n_book_fail = sum(1 for c in book_checks if c["status"] == "FAIL")
    n_book_miss = sum(1 for c in book_checks if c["status"] == "MISSING")

    status = "PASS" if (in_range and identity_pass
                        and n_book_fail == 0 and n_book_miss == 0) else "FAIL"
    result = {
        "series_id": "S201",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": get_tolerance_class("S201", default="share_series"),
        "status": status,
        "n_pass": (1 if in_range else 0) + (1 if identity_pass else 0) + n_book_pass,
        "n_fail": (0 if in_range else 1) + (0 if identity_pass else 1) + n_book_fail,
        "n_missing": n_book_miss,
        "checks": {
            "GFP_GDP_range_expected": [0.6, 1.0],
            "actual_range": [float(df["value"].min()), float(df["value"].max())],
            "v_1948": float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None,
            "v_1989": float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None,
        },
        "component_identity": {
            "definition": "S201-A == S503-A / NIPA_1.7.5_GDP",
            "compared_years": int(len(ident)),
            "max_abs_err": identity_max_err,
            "status": "PASS" if identity_pass else "FAIL",
        },
        "book_anchor": {
            "definition": "numerator S503-A == book GFP* (benchmark_reconciled.csv, Table 5.3)",
            "checks": book_checks,
        },
    }
    write_validation_result("S201", result)
    print(f"    [V03_S201] status={status} range=[{df['value'].min():.3f},{df['value'].max():.3f}] "
          f"identity_max_err={identity_max_err:.2e} book_anchor={n_book_pass}/{len(book_checks)}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
