"""T601-T604: Taxes on workers.

T601 = personal income taxes × labor_share
T602 = social insurance contributions (100% from workers)
T603 = indirect taxes × worker consumption share
T604 = T601 + T602 + T603 (identity)

labor_share = EC/PI from NIPA 2.1.
"""

import pandas as pd
from .helpers import build_series, save_series
from nickydata.fetch.bea_nipa import parse_line

DEPENDS_ON = []


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    results = {}

    nipa_21 = data.get("nipa", {}).get("T20100", [])
    nipa_31 = data.get("nipa", {}).get("T30100", [])
    nipa_37 = data.get("nipa", {}).get("T30700", [])

    # Labor share: EC/PI
    ec = parse_line(nipa_21, line_description="Compensation of employees") / 1e3
    pi = parse_line(nipa_21, line_description="Personal income") / 1e3
    common_ls = ec.index.intersection(pi.index)
    labor_share = ec[common_ls] / pi[common_ls]

    # T601: Personal taxes × labor_share
    personal_taxes = parse_line(nipa_31, line_description="Personal current taxes") / 1e3
    if not personal_taxes.empty:
        common = personal_taxes.index.intersection(labor_share.index)
        t601 = personal_taxes[common] * labor_share[common]
        results["T601"] = build_series(t601, pd.Series(dtype=float))

    # T602: Social insurance contributions (100% from workers)
    social_ins = parse_line(nipa_37, line_number=1) / 1e3  # total
    if social_ins.empty:
        social_ins = parse_line(nipa_31, line_description="Contributions for government social insurance") / 1e3
    if not social_ins.empty:
        results["T602"] = build_series(social_ins, pd.Series(dtype=float))

    # T603: Indirect taxes × consumption share (approximate with labor_share)
    indirect = parse_line(nipa_31, line_description="Taxes on production and imports") / 1e3
    if not indirect.empty:
        common = indirect.index.intersection(labor_share.index)
        t603 = indirect[common] * labor_share[common] * 0.8  # workers bear ~80% via consumption
        results["T603"] = build_series(t603, pd.Series(dtype=float))

    # T604: Sum
    if "T601" in results and "T602" in results and "T603" in results:
        t601_v = results["T601"]["value"]
        t602_v = results["T602"]["value"]
        t603_v = results["T603"]["value"]
        common = t601_v.index.intersection(t602_v.index).intersection(t603_v.index)
        t604 = t601_v[common] + t602_v[common] + t603_v[common]
        results["T604"] = build_series(t604, pd.Series(dtype=float))

    for sid, df in results.items():
        save_series(sid, df)
        print(f"    {sid}: {len(df)} years")

    return results
