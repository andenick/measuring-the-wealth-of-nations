"""T513 (r* = S*/K*) and T514 (r*_adj = r*/TCU).

K* = K_total × IO productive ratio.
K_total from BEA Fixed Assets Table 4.1.
TCU from FRED.
"""

import pandas as pd
from .helpers import build_series, save_series, load_computed, interpolate_annual
from nickydata.fetch.bea_fixed_assets import parse_total_k

DEPENDS_ON = ["exploitation"]


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    s_star = load_computed("T505")
    results = {}

    # Load K from Fixed Assets
    fa_records = data.get("fixed_assets", [])
    if not fa_records:
        return results

    k_total_mn = parse_total_k(fa_records, min_year=1947)
    k_total_bn = k_total_mn / 1e3  # millions -> billions

    # K* = K × productive ratio (from IO benchmarks)
    io_data = data.get("io", {})
    prod_ratios = {}
    productive = set(methodology["sector_classification"]["productive_naics"])
    trading = set(methodology["sector_classification"]["trading_naics"])

    for year, io in io_data.items():
        use_records = io.get("use", [])
        if not use_records:
            continue
        from nickydata.fetch.bea_io import parse_use_matrix
        _, go = parse_use_matrix(use_records)
        if go.empty:
            continue
        go_pt = sum(go.get(c, 0) for c in go.index if c in productive | trading)
        go_total = go.sum()
        if go_total > 0:
            prod_ratios[year] = go_pt / go_total

    if prod_ratios:
        ratio_annual = interpolate_annual(prod_ratios)
    else:
        ratio_annual = pd.Series(0.55, index=k_total_bn.index)

    avg_ratio = ratio_annual.mean()
    k_star = pd.Series(dtype=float)
    for yr in k_total_bn.index:
        r = ratio_annual.get(yr, avg_ratio)
        k_star[yr] = k_total_bn[yr] * r

    # r* = S*/K*
    if not s_star.empty:
        common = s_star.index.intersection(k_star.index)
        valid = common[k_star[common] > 0]
        r_star = s_star[valid] / k_star[valid]
        results["T513"] = build_series(r_star, pd.Series(dtype=float))

        # r*_adj = r*/TCU
        tcu = data.get("tcu", pd.Series(dtype=float))
        if not tcu.empty:
            tcu_ratio = tcu / 100  # percent -> ratio
            common2 = r_star.index.intersection(tcu_ratio.index)
            r_adj = r_star[common2] / tcu_ratio[common2]
            results["T514"] = build_series(r_adj, pd.Series(dtype=float))

    for sid, df in results.items():
        save_series(sid, df)
        print(f"    {sid}: {len(df)} years")

    return results
