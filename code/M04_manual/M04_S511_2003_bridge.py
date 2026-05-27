"""M04_S511 — BLS CES 2003 Overhaul Bridge Application (per-series wrapper).

S511 (Productive Labor Share Lp/L) is a direct ratio of two CES
super-sector employment counts:

  numerator   : productive production workers
                (mining/logging + construction + manufacturing)
                = CES1000000006 + CES2000000006 + CES3000000006
  denominator : total private all-employees
                = CES0500000001

For a *ratio*, the 2003 overhaul cancels exactly to the extent that the
multiplicative factor is common across numerator and denominator
super-sectors. Because BLS applies the QCEW NAICS-basis benchmark
per-industry (different sectors get different factors per the June 2003
BLS benchmark article), the ratio is *not* invariant. However, the
cached BLS API vintage is post-overhaul back-revised, so the cached
ratio is internally consistent across 2003 (any residual is dominated
by genuine sectoral cyclical divergence).

v1.1 applies a documented null bridge (factor=1.0). Wiring in place for
v1.2 when originally-published per-sector factors can be sourced.

See M04_bls_ces_2003_bridge.py for the master rationale.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL, ROOT  # noqa: E402

SERIES_ID = "S511"
BRIDGE_YEAR = 2003
FACTORS_JSON = ROOT / "data" / "adjusted-final-data" / "bls_ces_2003_bridge_factors.json"
RELEVANT_CES = [
    "CES0500000001",  # denominator: total private all-employees
    "CES1000000006",  # numerator: mining/logging production workers
    "CES2000000006",  # numerator: construction production workers
    "CES3000000006",  # numerator: manufacturing production workers
]


def load_factors() -> dict:
    if not FACTORS_JSON.exists():
        raise FileNotFoundError(
            f"Bridge factors not found at {FACTORS_JSON}. "
            f"Run M04_bls_ces_2003_bridge.py first."
        )
    return json.loads(FACTORS_JSON.read_text(encoding="utf-8"))


def apply_bridge_to_ratio(
    numerator: pd.Series, denominator: pd.Series,
    num_factor: float, den_factor: float,
) -> pd.Series:
    """Apply per-leg bridge factors then recompute the ratio.

    In v1.1 both factors == 1.0 ⇒ identity. Wired for v1.2.
    """
    bridge_factor = num_factor / den_factor  # net ratio adjustment
    out = (numerator / denominator).copy()
    out.loc[out.index >= BRIDGE_YEAR] = out.loc[out.index >= BRIDGE_YEAR] * bridge_factor
    return out


def verify() -> dict:
    payload = load_factors()
    factors_for_series = {
        k: v for k, v in payload["factors"].items() if k in RELEVANT_CES
    }
    assert factors_for_series, f"No relevant CES factors found for {SERIES_ID}"

    csv_path = DATA_FINAL / f"{SERIES_ID}.csv"
    n_post_2003 = None
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        ext = df[df["series_id"] == f"{SERIES_ID}-EXT"]
        if not ext.empty:
            n_post_2003 = int((ext["year"] >= BRIDGE_YEAR).sum())

    # Net ratio adjustment (illustrative — all 1.0 in v1.1)
    num_factors = [
        v["bridge_factor_post_2003"]
        for k, v in factors_for_series.items()
        if k != "CES0500000001"
    ]
    den_factor = factors_for_series["CES0500000001"]["bridge_factor_post_2003"]
    avg_num_factor = sum(num_factors) / len(num_factors)
    net_ratio_factor = avg_num_factor / den_factor

    summary = {
        "series_id": SERIES_ID,
        "bridge_year": BRIDGE_YEAR,
        "relevant_ces_series": RELEVANT_CES,
        "factors": {k: v["bridge_factor_post_2003"] for k, v in factors_for_series.items()},
        "avg_numerator_factor": avg_num_factor,
        "denominator_factor": den_factor,
        "net_ratio_adjustment": net_ratio_factor,
        "bridge_is_null_v1_1": net_ratio_factor == 1.0,
        "ext_rows_post_2003_on_disk": n_post_2003,
        "v1_3_followup": payload.get("v1_3_followup", payload.get("v1_2_followup", "n/a")),
    }
    print(f"[M04_{SERIES_ID}_2003_bridge] factors: {summary['factors']}")
    print(
        f"[M04_{SERIES_ID}_2003_bridge] net ratio adjustment: {net_ratio_factor:.6f}  "
        f"(null={summary['bridge_is_null_v1_1']}); ext rows >=2003: {n_post_2003}"
    )
    return summary


if __name__ == "__main__":
    verify()
