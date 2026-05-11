"""T515 (Lp), T516 (Lu), T511 (Lp/L), T512 (V*/W).

Computes from FRED PAYEMS (total nonfarm) + BLS CES (production workers)
+ IO productive employment ratios.

Lp = production workers in productive sectors (BLS CES, adjusted by IO ratio)
Lu = total employment - Lp
Lp/L = productive labor share
V*/W = productive wage share (computed after V* is available)
"""

import pandas as pd
from .helpers import load_methodology, build_series, save_series, load_computed

DEPENDS_ON = []


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    results = {}

    # Total employment from PAYEMS
    payems = data.get("payems", pd.Series(dtype=float))
    if payems.empty:
        return results

    # BLS production workers (total private)
    bls_ratios = data.get("bls_ratios", pd.DataFrame())
    employment = data.get("employment", pd.DataFrame())

    # Production workers: use manufacturing ratio as anchor, apply IO adjustment
    prod_workers = pd.Series(dtype=float)
    if "manufacturing" in bls_ratios.columns:
        mfg_ratio = bls_ratios["manufacturing"]
    else:
        mfg_ratio = pd.Series(0.68, index=payems.index)

    # Approximate Lp: PAYEMS × IO productive employment ratio
    # For now use a stable ratio calibrated from the methodology
    # Book shows Lp/L declining from 0.57 (1948) to 0.36 (1989)
    # IO productive output ratio ≈ 0.55 for NAICS era
    # The employment ratio is lower because productive sectors are more capital-intensive

    # Use employment sector data to subtract trade + FIRE
    if not employment.empty:
        total = payems.copy()
        trade = employment.get("trade", pd.Series(0, index=total.index))
        fire = employment.get("fire", pd.Series(0, index=total.index))

        # "Roughly productive" = total - trade - FIRE
        # Then apply production worker fraction (~0.65)
        common = total.index
        for s in [trade, fire]:
            if not s.empty:
                common = common.intersection(s.dropna().index)

        productive_universe = total[common]
        if not trade.empty:
            productive_universe = productive_universe - trade.reindex(common).fillna(0)
        if not fire.empty:
            productive_universe = productive_universe - fire.reindex(common).fillna(0)

        prod_fraction = methodology.get("parameters", {}).get("production_worker_fraction", 0.65)
        prod_workers = productive_universe * prod_fraction
    else:
        prod_workers = payems * 0.35  # rough approximation

    lp = prod_workers
    lu = payems - lp
    lp_l = lp / payems

    results["T515"] = build_series(lp, pd.Series(dtype=float))
    results["T516"] = build_series(lu, pd.Series(dtype=float))
    results["T511"] = build_series(lp_l, pd.Series(dtype=float))

    # T512 (V*/W) computed later when V* is available
    # For now, derive from Lp/L using the book's relationship:
    ec_p_ratio = methodology.get("parameters", {}).get("ec_p_ec_avg_ratio", 0.95)
    t512 = lp_l * ec_p_ratio
    results["T512"] = build_series(t512, pd.Series(dtype=float))

    for sid, df in results.items():
        save_series(sid, df)
        print(f"    {sid}: {len(df)} years")

    return results
