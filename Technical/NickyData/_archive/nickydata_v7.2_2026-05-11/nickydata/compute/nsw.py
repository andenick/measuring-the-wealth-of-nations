"""T607 (NSW), T608 (NSW/V*), T609 (NSW/NI).

NSW = T605 + T606 - T604 (benefits + govt services - taxes).
"""

import pandas as pd
from .helpers import build_series, save_series, load_computed
from nickydata.fetch.bea_nipa import parse_line

DEPENDS_ON = ["taxes", "benefits", "variable_capital"]


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    t604 = load_computed("T604")
    t605 = load_computed("T605")
    t606 = load_computed("T606")
    t504 = load_computed("T504")

    results = {}

    # T607: NSW = benefits + services - taxes
    if not t604.empty and not t605.empty and not t606.empty:
        common = t604.index.intersection(t605.index).intersection(t606.index)
        nsw = t605[common] + t606[common] - t604[common]
        results["T607"] = build_series(nsw, pd.Series(dtype=float))

        # T608: NSW/V*
        if not t504.empty:
            common2 = nsw.index.intersection(t504.index)
            valid = common2[t504[common2] > 0]
            t608 = nsw[valid] / t504[valid]
            results["T608"] = build_series(t608, pd.Series(dtype=float))

        # T609: NSW/NI (National Income from NIPA)
        nipa_21 = data.get("nipa", {}).get("T20100", [])
        ni = parse_line(nipa_21, line_description="National income") / 1e3
        if not ni.empty:
            common3 = nsw.index.intersection(ni.index)
            valid3 = common3[ni[common3] > 0]
            t609 = nsw[valid3] / ni[valid3]
            results["T609"] = build_series(t609, pd.Series(dtype=float))

    for sid, df in results.items():
        save_series(sid, df)
        print(f"    {sid}: {len(df)} years")

    return results
