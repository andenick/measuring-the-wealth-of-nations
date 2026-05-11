#!/usr/bin/env python3
"""P21 - Independent Moos (2017) NSW derivation from BEA NIPA tables.

Implements Moos's methodology directly from NIPA data rather than
deriving from our own NSW series (which would be circular).

NSW = (E1 + E2*LS) - (T1 + T2*LS)
where:
  E1 = direct social benefits to persons (NIPA T3.12)
  E2 = mixed public goods allocated by labor share (NIPA T3.16)
  T1 = social insurance contributions (NIPA T3.7)
  T2 = personal current taxes allocated by labor share (NIPA T3.1)
  LS = employee compensation / personal income (NIPA T2.1)

Outputs: N1301-N1305 in studies/series/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from utils.paths import STUDIES_OUT, PARSED_RAW, ensure_dirs

SERIES_ID = "N1301"
PRIORITY = 13


def process():
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # Load parsed NIPA data from L17
    def _load(name):
        p = PARSED_RAW / f"moos_{name}.csv"
        if p.exists():
            return pd.read_csv(p, index_col=0)
        return pd.DataFrame()

    pi = _load("personal_income")
    gdp_df = _load("gdp")
    benefits = _load("social_benefits")
    govt_con = _load("govt_consumption")
    soc_ins = _load("social_insurance")
    govt_acc = _load("govt_accounts")

    if pi.empty or gdp_df.empty or benefits.empty:
        steps.append("Missing NIPA data — run L17 first")
        print("    [P21] FAIL: missing parsed NIPA data")
        return {"series_id": SERIES_ID, "status": "fail", "steps": steps,
                "data_dict": {}, "outputs": []}

    # Restrict to 1959-2024 (Moos starts at 1959)
    years = range(1959, 2025)

    # Labor Share: LS = Employee Compensation / Personal Income
    ls = pi["employee_compensation"] / pi["personal_income"]
    ls = ls.reindex([y for y in years if y in ls.index])

    # GDP
    gdp = gdp_df["gdp"].reindex([y for y in years if y in gdp_df.index])

    # E1: Direct social benefits to persons (NIPA T3.12 line 1)
    e1 = benefits["total_social_benefits"].reindex(ls.index)

    # E2: Government consumption by function (T3.16) — loaded but NOT included
    # in the standard Moos/Shaikh-Tonak NSW formula. Moos (2017) defines NSW as
    # direct transfers minus taxes, without government consumption expenditure.
    # Kept for potential sensitivity analysis (alpha parameter in A03).
    if not govt_con.empty:
        e2_cols = ["education", "health", "transportation"]
        available = [c for c in e2_cols if c in govt_con.columns]
        if available:
            e2 = govt_con[available].sum(axis=1).reindex(ls.index)
        else:
            e2 = pd.Series(0, index=ls.index)
    else:
        e2 = pd.Series(0, index=ls.index)

    # T1: Social insurance contributions (NIPA T3.7 line 1)
    if not soc_ins.empty:
        t1 = soc_ins["total_social_insurance"].reindex(ls.index)
    else:
        t1 = pd.Series(0, index=ls.index)

    # T2: Personal current taxes (NIPA T3.1 line 3)
    if not govt_acc.empty and "personal_current_taxes" in govt_acc.columns:
        t2 = govt_acc["personal_current_taxes"].reindex(ls.index)
    else:
        t2 = pd.Series(0, index=ls.index)

    # Compute NSW using Moos methodology
    common = ls.dropna().index.intersection(gdp.dropna().index)
    common = common.intersection(e1.dropna().index)

    # Standard Moos/ST formula: benefits = E1 only (direct transfers to persons)
    # E2 (govt consumption) excluded per Moos (2017) methodology
    total_benefits = e1[common]
    total_taxes = t1.reindex(common).fillna(0) + t2.reindex(common).fillna(0) * ls[common]
    nsw = total_benefits - total_taxes
    nsw_gdp = nsw / gdp[common]
    nsw_ec = nsw / pi["employee_compensation"].reindex(common)

    steps.append(f"NSW computed: {len(common)} years ({common.min()}-{common.max()})")
    steps.append(f"  LS range: {ls[common].min():.3f}-{ls[common].max():.3f}")
    steps.append(f"  NSW/GDP mean: {nsw_gdp.mean():.4f}")

    # N1301: NSW/GDP
    out = pd.DataFrame({"book": nsw_gdp, "combined": nsw_gdp})
    out.index.name = "year"
    out.to_csv(STUDIES_OUT / "N1301.csv")
    data_dict["N1301"] = nsw_gdp
    outputs.append(str(STUDIES_OUT / "N1301.csv"))
    print(f"    [P21] N1301: {len(nsw_gdp)} years (NSW/GDP, independent NIPA)")

    # N1302: NSW/EC
    out = pd.DataFrame({"book": nsw_ec, "combined": nsw_ec})
    out.index.name = "year"
    out.to_csv(STUDIES_OUT / "N1302.csv")
    data_dict["N1302"] = nsw_ec
    outputs.append(str(STUDIES_OUT / "N1302.csv"))
    print(f"    [P21] N1302: {len(nsw_ec)} years (NSW/EC)")

    # N1304: 1959-1997 overlap validation
    overlap = nsw_gdp[(nsw_gdp.index >= 1959) & (nsw_gdp.index <= 1997)]
    if len(overlap) > 0:
        out = pd.DataFrame({"book": overlap, "combined": overlap})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1304.csv")
        data_dict["N1304"] = overlap
        outputs.append(str(STUDIES_OUT / "N1304.csv"))

        moos_mean = 0.011
        our_mean = float(overlap.mean())
        steps.append(f"  Moos Table 1 validation (1959-1997): our mean={our_mean:.4f} vs Moos={moos_mean}")
        print(f"    [P21] N1304: {len(overlap)} years (overlap, mean={our_mean:.4f} vs Moos={moos_mean})")

    # N1305: Post-2000 structural shift
    pre = nsw_gdp[nsw_gdp.index <= 2000]
    post = nsw_gdp[nsw_gdp.index > 2000]
    if len(pre) > 0 and len(post) > 0:
        shift_series = nsw_gdp.copy()
        out = pd.DataFrame({
            "nsw_gdp": shift_series,
            "post_2000": (shift_series.index > 2000).astype(int),
            "combined": shift_series,
        })
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1305.csv")
        data_dict["N1305"] = shift_series
        outputs.append(str(STUDIES_OUT / "N1305.csv"))

        shift = float(post.mean()) - float(pre.mean())
        steps.append(f"  Structural shift: pre={float(pre.mean()):.4f}, post={float(post.mean()):.4f}, shift={shift:+.4f}")
        print(f"    [P21] N1305: shift={shift:+.4f} (Moos reports +0.030)")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
