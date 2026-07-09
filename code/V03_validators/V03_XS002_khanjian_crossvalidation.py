"""V03_XS002 -- S*/V* at I-O benchmark years vs BOOK Table H.1 (workpackage C v2.0).

DE-TAUTOLOGIZED: previously the reference values were the series' own chopped
output. XS002-A reproduces ST's own money rate of surplus value S*/V* at the
I-O benchmark years, and the book PRINTS those values (Appendix H Table H.1,
= Appendix I Table I.1 Line 23). The anchor now comes from
data/source/book_tables/XS002_TableH1_SV_BENCHMARKS.csv (verbatim v2 KB
extraction). Tolerance: printed 2 dp -> abs 0.01.
validator_class: book
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL, ROOT  # noqa: E402

BOOK_CSV = ROOT / "data" / "source" / "book_tables" / "XS002_TableH1_SV_BENCHMARKS.csv"


def run():
    df = pd.read_csv(DATA_FINAL / "XS002.csv").dropna(subset=["value"])
    by_year = dict(zip(df["year"].astype(int), df["value"].astype(float)))
    book = pd.read_csv(BOOK_CSV, comment="#")
    checks = []
    for r in book.itertuples():
        actual = by_year.get(int(r.year))
        if actual is None:
            # XS002 carries only the five benchmark years 1958-1977; the
            # 1948/1989 book rows are context, not misses.
            continue
        ok = abs(actual - r.sv_star_book) <= 0.01 + 1e-9
        checks.append({"year": int(r.year), "book": r.sv_star_book,
                       "actual": round(actual, 4), "status": "PASS" if ok else "FAIL"})
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")
    status = "PASS" if (checks and n_fail == 0) else "FAIL"
    result = {
        "series_id": "XS002",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "validator_class": "book",
        "anchor": "S&T 1994 Appendix H Table H.1 S*/V* row (= Table I.1 Line 23), v2 KB verbatim",
        "status": status,
        "benchmarks": {"checks": checks, "n_fail": n_fail},
    }
    write_validation_result("XS002", result)
    print(f"    [V03_XS002] status={status} book_anchors={len(checks)-n_fail}/{len(checks)}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
