"""M04_S512 — Manual Adjustment Documentation: 1990-1997 Log-Linear Bridge.

This is a documentation-only / verification script. The actual bridge logic
is implemented inside `P02_processors/P02_S512_productive_wage_share.py` as
the S512-INTERP subseries; this file exists to (a) satisfy the Anu Framework
v12.0 M04 manual-adjustment-script discoverability requirement and (b) provide
a standalone verifier that re-derives the interpolated values from the
published endpoints and asserts equality with the values stored in
`data/final/S512.csv`.

ADJUSTMENT
----------
Type             : log-linear interpolation (SIC->NAICS classification bridge)
Affected years   : 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997
Affected subseries: S512-INTERP, S512-COMBINED (for years 1990-1997)
Anchor LHS       : S512-A[1989]    (book Table 5.7 T512A = 0.36)
Anchor RHS       : S512-EXT[1998]  (BEA NIPA 6.2D productive share, level-spliced)
Method           : v(t) = exp( ln(v0) + (t - t0)/(t1 - t0) * (ln(v1) - ln(v0)) )

RATIONALE
---------
BEA NIPA Table 6.2D (Compensation of Employees by Industry, NAICS basis) begins
1998. The productive-wage-share V*/W cannot be reconstructed from a single
modern source for 1990-1997 because the Marxian productive/unproductive
partition requires industry-level compensation detail that is unavailable on a
NAICS basis pre-1998 and not directly comparable on the SIC pre-2002 vintage.

Rather than leave NaN in S512-COMBINED across 1990-1997, we interpolate
log-linearly between the last book observation (1989, V*/W = 0.36) and the
first level-spliced BEA observation (1998). Log-linear (not linear) is the
right choice because V*/W is a positive bounded ratio and the underlying
productive/total ratio is closer to multiplicative than additive over an 8-year
span. This matches the precedent set by M04_S501, M04_S502, M04_S503 (see
BUILD_NARRATIVE.md Stage 5 cohort 3).

HONESTY
-------
These 8 values are NOT directly observed. They are model-implied estimates
under a smooth-growth assumption. They:
  * Carry stage="extension_bridge" (not "extension")
  * Live in a dedicated S512-INTERP subseries
  * Have provenance strings that begin with "Log-linear interpolation"
  * Are documented here and in the S512 DPR/EPR Methodology sections

DOWNSTREAM USE CAUTION: S504-EXT is derived as S512-EXT * W, so S512-INTERP
1990-1997 propagates into S504-INTERP 1990-1997 (also marked as interpolated).

VERIFICATION (executable):
  Run `python Technical/code/M04_manual/M04_S512_1990_1997_bridge.py` --
  re-derives interp values from (1989, 1998) endpoints and asserts equality
  with the on-disk S512-INTERP rows.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S512"
BOOK_LAST_YEAR = 1989
EXT_FIRST_YEAR = 1998
INTERP_YEARS = list(range(1990, 1998))


def _log_linear_bridge(v0: float, v1: float, y0: int, y1: int) -> pd.DataFrame:
    n = y1 - y0
    log0, log1 = np.log(v0), np.log(v1)
    rows = []
    for k in range(1, n):
        frac = k / n
        rows.append({"year": y0 + k, "value": float(np.exp(log0 + frac * (log1 - log0)))})
    return pd.DataFrame(rows)


def verify() -> dict:
    csv = DATA_FINAL / f"{SERIES_ID}.csv"
    if not csv.exists():
        raise FileNotFoundError(f"{csv} not found; run P02_S512 first")
    df = pd.read_csv(csv)

    a = df[df["series_id"] == "S512-A"]
    ext = df[df["series_id"] == "S512-EXT"]
    interp = df[df["series_id"] == "S512-INTERP"]

    if a.empty or ext.empty:
        raise RuntimeError("S512-A or S512-EXT missing; P02 incomplete")
    if interp.empty:
        raise RuntimeError("S512-INTERP missing; P02 has not yet been updated with bridge")

    v0 = float(a.loc[a["year"] == BOOK_LAST_YEAR, "value"].iloc[0])
    v1 = float(ext.loc[ext["year"] == EXT_FIRST_YEAR, "value"].iloc[0])
    expected = _log_linear_bridge(v0, v1, BOOK_LAST_YEAR, EXT_FIRST_YEAR)

    merged = interp[["year", "value"]].merge(expected, on="year", suffixes=("_disk", "_recompute"))
    merged["abs_diff"] = (merged["value_disk"] - merged["value_recompute"]).abs()
    max_diff = float(merged["abs_diff"].max())

    print(f"[M04_S512] book(1989)={v0:.4f} | EXT(1998)={v1:.4f}")
    print(f"[M04_S512] interpolated rows: {len(interp)}; max recompute diff: {max_diff:.2e}")
    for _, r in merged.iterrows():
        print(f"          {int(r['year'])}: disk={r['value_disk']:.4f}  recompute={r['value_recompute']:.4f}")

    assert max_diff < 1e-6, f"S512-INTERP mismatch: max diff {max_diff}"
    print("[M04_S512] VERIFY PASS")

    return {
        "v0_1989": v0,
        "v1_1998": v1,
        "n_interp": int(len(interp)),
        "max_recompute_diff": max_diff,
        "sample": {int(r["year"]): float(r["value_disk"]) for _, r in merged.iterrows()},
    }


if __name__ == "__main__":
    diag = verify()
    print(f"[M04_S512] sample 1991={diag['sample'].get(1991):.4f}, 1995={diag['sample'].get(1995):.4f}")
