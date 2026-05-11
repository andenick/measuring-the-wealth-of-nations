"""A07 (social burden rate), A09 (unproductive exploitation), A10 (productivity).

Social burden: Eu_share = 1 - P+/S* where P+ = NNP - EC.
Exploitation: eu = (hu/hp)/(ecu/ecp) × (1 + e) - 1.
Productivity: q* = TP_real/Hp, y = GDP_real/H.
"""

import pandas as pd
from .helpers import build_series, save_series, load_computed
from nickydata.fetch.bea_nipa import parse_line

DEPENDS_ON = ["exploitation", "profit_rate"]


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    s_star = load_computed("T505")
    e_star = load_computed("T506")
    tp_star = load_computed("T501")
    t515 = load_computed("T515")
    results = {}

    # --- A07: Social burden rate ---
    nipa_21 = data.get("nipa", {}).get("T20100", [])
    nipa_gdp = data.get("nipa", {}).get("T10105", [])

    va_nnp = parse_line(nipa_gdp, line_description="Gross domestic product") / 1e3
    ec = parse_line(nipa_21, line_description="Compensation of employees") / 1e3

    if not va_nnp.empty and not ec.empty and not s_star.empty:
        common = va_nnp.index.intersection(ec.index).intersection(s_star.index)
        valid = common[s_star[common] > 0]
        p_plus = va_nnp[valid] - ec[valid]
        pps = p_plus / s_star[valid]
        eu_share = 1 - pps

        a07 = pd.DataFrame({"P_plus_over_S_star": pps, "Eu_share": eu_share})
        a07.index.name = "year"
        save_series("A07", a07)
        results["A07"] = a07
        print(f"    A07: {len(a07)} years (Eu_share range {eu_share.min():.3f}-{eu_share.max():.3f})")

    # --- A09: Unproductive exploitation rate ---
    if not e_star.empty:
        hu_hp = 0.99  # stable per Appendix I
        ecu_ecp = 1.01  # converged by 1989
        relative = hu_hp / ecu_ecp
        eu = relative * (1 + e_star) - 1
        eu_ep = eu / e_star

        a09 = pd.DataFrame({"ep": e_star, "eu": eu, "eu_ep": eu_ep})
        a09.index.name = "year"
        save_series("A09", a09)
        results["A09"] = a09
        print(f"    A09: {len(a09)} years")

    # --- A10: Marxian productivity ---
    deflator = data.get("gdp_deflator", pd.Series(dtype=float))
    payems = data.get("payems", pd.Series(dtype=float))

    if not tp_star.empty and not payems.empty and not deflator.empty:
        hours_per_worker = methodology["parameters"]["production_worker_hours_annual"]

        common = tp_star.index.intersection(payems.index).intersection(deflator.index)
        if not t515.empty:
            common = common.intersection(t515.index)

        q_star_vals = {}
        y_vals = {}

        for yr in common:
            py = deflator.get(yr, 100) / 100  # index to ratio
            if py <= 0:
                continue

            tp_real = tp_star[yr] / py
            lp = t515.get(yr, payems[yr] * 0.35)
            hp = lp * hours_per_worker / 1e6  # millions of hours

            if hp > 0:
                q_star_vals[yr] = tp_real / hp

            gdp_yr = va_nnp.get(yr, 0)
            h_total = payems[yr] * hours_per_worker / 1e6
            if h_total > 0 and gdp_yr > 0:
                y_vals[yr] = (gdp_yr / py) / h_total

        if q_star_vals:
            a10 = pd.DataFrame({"q_star": pd.Series(q_star_vals), "y_orthodox": pd.Series(y_vals)})
            a10.index.name = "year"
            save_series("A10", a10)
            results["A10"] = a10
            print(f"    A10: {len(a10)} years")

    return results
