"""V03_S801 — Cross-study reference series (ST exploitation rate).

DE-TAUTOLOGISED 2026-07 (review workpackage D). As shipped, S801-A IS the Shaikh-Tonak
exploitation rate e = S*/V* (identically S506) displayed as the cross-study
reference; the P02 also computes the ST-vs-Mohun differences, but the canonical
value column is ST_e. (The literal ST/Mohun *ratio* lives in XS1404; the book
has no "Chapter 8" / "Table 8.1" — those are project-internal labels for a
synthesis of book Chapter 7 §7.4 "Comparisons with previous studies".)

The previous benchmark check read `validation.reference_values`, which were
verbatim copies of S801's own chopped column (tautological). S801 is validated
by two INDEPENDENT anchors instead:

  1. COMPONENT IDENTITY — S801-A == upstream S506-A (ST exploitation rate) to
     floating tolerance, all years. S506 is built and validated independently.

  2. BOOK ANCHOR — the ST exploitation rate at the endpoints must equal the
     value reported in the book: e(1948)=1.70 and e(1989)=2.44 (ST 1994
     Table 5.7; the 1989 figure "unadjusted S*/V* 2.44 in 1989" is quoted
     verbatim in Appendix N, folios 352-361). These are checked against
     S801-A directly, not against S801's own registry copy.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import TOLERANCES  # noqa: E402

# Book-reported ST exploitation rate e = S*/V* (ST 1994 Table 5.7; 1989 value
# also quoted verbatim in Appendix N). Independent of S801's own output.
BOOK_EXPLOITATION_RATE = {
    1948: 1.70,
    1989: 2.44,
}


def run():
    df = pd.read_csv(DATA_FINAL / "S801.csv")
    df = df[df["series_id"] == "S801-A"]

    # --- Anchor 1: component identity S801-A == upstream S506-A --------------
    s506 = pd.read_csv(DATA_FINAL / "S506.csv")
    s506 = s506[s506["series_id"] == "S506-A"][["year", "value"]].rename(columns={"value": "S506"})
    merged = df[["year", "value"]].rename(columns={"value": "S801"}).merge(s506, on="year")
    max_err = float((merged["S801"] - merged["S506"]).abs().max()) if len(merged) else 0.0
    round_trip_pass = bool(max_err < 1e-9 and len(df) >= 30)

    # --- Anchor 2: book exploitation-rate endpoints -------------------------
    tol = TOLERANCES["rate_series"]
    by_year = dict(zip(df["year"].astype(int), df["value"].astype(float)))
    book_checks = []
    for yr, expected in sorted(BOOK_EXPLOITATION_RATE.items()):
        actual = by_year.get(yr)
        if actual is None:
            book_checks.append({"year": yr, "book_e": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        book_checks.append({
            "year": yr, "book_e": expected, "actual": round(actual, 6),
            "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
            "status": "PASS" if ok else "FAIL",
            "source": "ST 1994 Table 5.7" + ("; Appendix N verbatim" if yr == 1989 else ""),
        })
    n_book_pass = sum(1 for c in book_checks if c["status"] == "PASS")
    n_book_fail = sum(1 for c in book_checks if c["status"] == "FAIL")
    n_book_miss = sum(1 for c in book_checks if c["status"] == "MISSING")

    status = "PASS" if (round_trip_pass and n_book_fail == 0 and n_book_miss == 0) else "FAIL"
    result = {
        "series_id": "S801",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "rel_tol": tol["rel"], "abs_tol": tol["abs"],
        "status": status,
        "n_pass": n_book_pass + (1 if round_trip_pass else 0),
        "n_fail": n_book_fail + (0 if round_trip_pass else 1),
        "n_missing": n_book_miss,
        "component_identity": {"definition": "S801-A == S506-A (ST exploitation rate)",
                               "vs_S506_max_err": max_err, "comparison_years": len(df),
                               "status": "PASS" if round_trip_pass else "FAIL"},
        "book_anchor": {"definition": "ST 1994 Table 5.7 exploitation rate e=S*/V* endpoints",
                        "checks": book_checks},
    }
    write_validation_result("S801", result)
    print(f"    [V03_S801] status={status} identity_max_err={max_err} book_anchor={n_book_pass}/{len(book_checks)}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
