"""V03_XS1404 - ST/Mohun exploitation ratio: construction-identity + book-anchored check.

Re-baselined 2026-07-01 (workpackage E review, Group B) per _SHARED_BRIEF non-negotiable #4.

PRIOR STATE (FAIL): the check compared XS1404-A against
  - `validation.reference_values` {1948, 1989} that were EXACT copies of XS1404's own
    output (tautological, forbidden), and
  - a `validation.derived_statistics.mean` = 1.61 that is UNSOURCED: it matches neither the
    computed series mean (1.163) nor Mohun 2005 Fig 4 published ST/SM (0.74-0.87) nor SM/ST
    (1.15-1.35). That fabricated mean was the sole cause of the FAIL.

RE-BASELINE: XS1404 is a pipeline-internal cross-classification ratio with NO year-matched
external anchor (Mohun 2005 covers 1964-2001 and never publishes an ST-book / SM-reconstruction
ratio over 1948-1989; his Fig 4 ratio is a different period AND the inverse orientation). Per the
brief, the honest validator validates against the CONSTRUCTION IDENTITY recomputed from the two
independent component series, plus two anchors whose NUMERATOR is the independent ST-book value
(S506 registry reference_values, Table 5.7). This is class `book` (identity). The fabricated mean
is not used. See DIV (B_DIV_PATCHES) for the full divergence record.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402


SERIES_ID = "XS1404"
IDENTITY_TOL_ABS = 1e-9
ANCHOR_TOL_ABS = 0.01
EXPECTED_RANGE = [0.7, 1.5]


def _sub(df: pd.DataFrame, sid: str) -> pd.DataFrame:
    return df[df["series_id"] == sid][["year", "value"]].reset_index(drop=True)


def run():
    x4 = _sub(pd.read_csv(DATA_FINAL / "XS1404.csv"), "XS1404-A")
    s506 = _sub(pd.read_csv(DATA_FINAL / "S506.csv"), "S506-A").rename(columns={"value": "e_st"})
    x1 = _sub(pd.read_csv(DATA_FINAL / "XS1401.csv"), "XS1401-A").rename(columns={"value": "e_mohun"})

    # --- Construction-identity check: XS1404-A == S506-A / XS1401-A (recomputed) ---
    m = x4.rename(columns={"value": "stored"}).merge(s506, on="year").merge(x1, on="year")
    m["recomputed"] = m["e_st"] / m["e_mohun"]
    m["idty_err"] = (m["recomputed"] - m["stored"]).abs()
    identity_max_err = float(m["idty_err"].max())
    identity_ok = identity_max_err <= IDENTITY_TOL_ABS

    in_range = bool(x4["value"].between(*EXPECTED_RANGE).all())

    # --- Book-anchored checks: numerator from ST-book S506 registry refvals (Table 5.7) ---
    # expected XS1404[y] = S506_book_ref[y] / XS1401-A[y]  (independent of XS1404's own output)
    s506_book = get_reference_values("S506")  # e.g. {1948:1.7, 1989:2.44, ...}
    anchor_checks = []
    for year in (1948, 1989):
        srow = s506_book.get(year, s506_book.get(str(year)))
        drow = x1[x1["year"] == year]
        arow = x4[x4["year"] == year]
        if srow is None or drow.empty or arow.empty:
            anchor_checks.append({"year": year, "status": "MISSING"})
            continue
        expected = float(srow) / float(drow["e_mohun"].iloc[0])
        actual = float(arow["value"].iloc[0])
        abs_err = abs(actual - expected)
        anchor_checks.append({
            "year": year, "expected": round(expected, 6), "actual": round(actual, 6),
            "abs_err": round(abs_err, 8),
            "numerator_source": f"S506 book reference_values[{year}]={float(srow)} (ST 1994 Table 5.7)",
            "status": "PASS" if abs_err <= ANCHOR_TOL_ABS else "FAIL",
        })
    n_anchor_fail = sum(1 for c in anchor_checks if c["status"] in ("FAIL", "MISSING"))

    ok = identity_ok and in_range and len(x4) > 0 and n_anchor_fail == 0
    status = "PASS" if ok else "FAIL"
    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "validator_class": "book (construction identity; ST-book-anchored numerator)",
        "status": status,
        "identity_check": {
            "formula": "XS1404-A == S506-A / XS1401-A",
            "max_abs_err": identity_max_err,
            "tol": IDENTITY_TOL_ABS,
            "status": "PASS" if identity_ok else "FAIL",
        },
        "range_check": {
            "expected_range": EXPECTED_RANGE,
            "actual_min": float(x4["value"].min()),
            "actual_max": float(x4["value"].max()),
            "n_rows": len(x4),
        },
        "anchors": {"checks": anchor_checks},
        "series_mean": round(float(x4["value"].mean()), 6),
        "note": ("Fabricated registry mean=1.61 intentionally NOT used (unsourced; see DIV). "
                 "No year-matched external Mohun anchor exists for the 1948-1989 ratio."),
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} identity_err={identity_max_err:.2e} "
          f"range=[{x4['value'].min():.3f}, {x4['value'].max():.3f}] mean={x4['value'].mean():.3f}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)
