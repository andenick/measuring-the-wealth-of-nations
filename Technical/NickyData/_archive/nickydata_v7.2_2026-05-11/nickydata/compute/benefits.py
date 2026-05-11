"""T605 (benefits to workers) and T606 (govt services to workers).

T605: Government social benefits from NIPA 3.12.
T606: Appendix N 3-group methodology from NIPA 3.16.
  Group I (income_security): 100% to workers
  Group II (education, health, transport): × annual labor_share
  Group III (defense, safety): 0%
"""

import pandas as pd
from .helpers import build_series, save_series
from nickydata.fetch.bea_nipa import parse_line

DEPENDS_ON = []


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    results = {}

    nipa_312 = data.get("nipa", {}).get("T31200", [])
    nipa_316 = data.get("nipa", {}).get("T31600", [])
    nipa_21 = data.get("nipa", {}).get("T20100", [])

    # T605: Social benefits
    benefits = parse_line(nipa_312, line_description="Government social benefits") / 1e3
    if benefits.empty:
        benefits = parse_line(nipa_312, line_number=1) / 1e3
    if not benefits.empty:
        results["T605"] = build_series(benefits, pd.Series(dtype=float))

    # T606: 3-group methodology
    nsw_groups = methodology.get("nsw_expenditure_groups", {})
    g1_lines = nsw_groups.get("group_1_direct", {}).get("nipa_3_16_lines", {})
    g2_lines = nsw_groups.get("group_2_labor_share", {}).get("nipa_3_16_lines", {})

    # Labor share
    ec = parse_line(nipa_21, line_description="Compensation of employees") / 1e3
    pi = parse_line(nipa_21, line_description="Personal income") / 1e3
    common_ls = ec.index.intersection(pi.index)
    labor_share = ec[common_ls] / pi[common_ls]

    if nipa_316:
        t606 = pd.Series(dtype=float)

        # Parse each line from 3.16
        g1_total = pd.Series(0.0, dtype=float)
        g2_total = pd.Series(0.0, dtype=float)

        for name, ln in g1_lines.items():
            s = parse_line(nipa_316, line_number=ln) / 1e3
            if not s.empty:
                g1_total = g1_total.add(s, fill_value=0)

        for name, ln in g2_lines.items():
            s = parse_line(nipa_316, line_number=ln) / 1e3
            if not s.empty:
                g2_total = g2_total.add(s, fill_value=0)

        # Allocate
        common = g1_total.index.intersection(g2_total.index).intersection(labor_share.index)
        for yr in common:
            ls = labor_share.get(yr, 0.60)
            t606[yr] = g1_total.get(yr, 0) * 1.0 + g2_total.get(yr, 0) * ls

        if not t606.empty:
            results["T606"] = build_series(t606, pd.Series(dtype=float))

    for sid, df in results.items():
        save_series(sid, df)
        print(f"    {sid}: {len(df)} years")

    return results
