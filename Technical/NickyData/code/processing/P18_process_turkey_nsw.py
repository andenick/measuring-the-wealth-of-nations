#!/usr/bin/env python3
"""P18 - Process Karabacak & Tonak (2022) Turkey NSW from fiscal data.

Uses TurkStat HDARP-extracted labor share (Table 20.37, 1980-2006) combined
with SBB budget shares and World Bank fiscal data to compute Turkey NSW.

Methodology (standard Shaikh-Tonak):
  NSW = Benefits_labor - Taxes_labor
  Benefits_labor = social_security + LS * (transfers - social_security)
  Taxes_labor = LS * tax_revenues
  LS = compensation_of_employees / GDP (from TurkStat national accounts)

Outputs: N1601 (labor share), N1602 (NSW/GDP ratio)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from utils.paths import STUDIES_OUT, PARSED_RAW, INPUTS, ensure_dirs

SERIES_ID = "N1601"
SERIES_IDS = ["N1601", "N1602"]
PRIORITY = 14

TURKEY_DIR = INPUTS / "ExternalSources" / "Turkey2022"


def process():
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    sbb_path = PARSED_RAW / "turkey_sbb_consolidated.csv"
    wbf_path = PARSED_RAW / "turkey_worldbank_fiscal.csv"
    ts_path = PARSED_RAW / "turkstat_compensation_labor_share_1980_2006.csv"

    sbb = pd.read_csv(sbb_path, index_col=0) if sbb_path.exists() else pd.DataFrame()
    wbf = pd.read_csv(wbf_path, index_col=0) if wbf_path.exists() else pd.DataFrame()

    # Load TurkStat HDARP labor share (primary source)
    if ts_path.exists():
        ts_df = pd.read_csv(ts_path, skiprows=2, index_col=0)
        turkstat_ls = ts_df["labor_share_pct"] / 100.0
    else:
        turkstat_ls = pd.Series(dtype=float)

    if turkstat_ls.empty and sbb.empty:
        steps.append("No Turkish data — run L18 first")
        print("    [P18] N1601/N1602: data_unavailable")
        return {"series_id": SERIES_ID, "status": "data_unavailable",
                "steps": steps, "data_dict": {}, "outputs": []}

    # Load FRED Turkey labor share (Penn World Table, 1980-2019) for extension
    fred_path = PARSED_RAW / "turkey_fred_labor_share_1980_2019.csv"
    fred_ls = pd.Series(dtype=float)
    if fred_path.exists():
        fred_df = pd.read_csv(fred_path, index_col="year")
        if "labor_share_fred" in fred_df.columns:
            fred_ls = fred_df["labor_share_fred"]

    # N1601: Labor share — TurkStat (1980-2006) + FRED extension (2007-2019)
    labor_share = pd.Series(dtype=float)
    for yr in range(1980, 2020):
        if yr in turkstat_ls.index:
            labor_share[yr] = turkstat_ls[yr]
        elif yr > 2006 and yr in fred_ls.index:
            # Growth-rate splice at 2006 to preserve TurkStat level
            if 2006 in turkstat_ls.index and 2006 in fred_ls.index and fred_ls[2006] > 0:
                labor_share[yr] = turkstat_ls[2006] * (fred_ls[yr] / fred_ls[2006])
    labor_share = labor_share.sort_index()

    if len(labor_share) > 0:
        out_df = pd.DataFrame({"book": labor_share, "combined": labor_share})
        out_df.index.name = "year"
        out_df.to_csv(STUDIES_OUT / "N1601.csv")
        data_dict["N1601"] = labor_share
        outputs.append(str(STUDIES_OUT / "N1601.csv"))
        steps.append(f"N1601: {len(labor_share)} years (TurkStat Table 20.37, {labor_share.index.min()}-{labor_share.index.max()})")
        print(f"    [P18] N1601: {len(labor_share)} years (labor share, TurkStat HDARP)")

    # N1602: NSW/GDP from SBB budget shares + real labor share
    nsw_gdp = pd.Series(dtype=float)

    if not sbb.empty:
        for yr in sbb.index:
            if yr < 1980 or yr > 2019:
                continue
            ls = labor_share.get(yr, np.nan)
            if np.isnan(ls):
                continue

            sg = sbb.loc[yr].get("Sosyal Güvenlik", 0) or 0
            transfers = sbb.loc[yr].get("Transfer", 0) or 0
            tax_rev = sbb.loc[yr].get("Vergi Gelirleri", 0) or 0

            benefit_labor_share = sg + ls * (transfers - sg)
            tax_labor_share = ls * tax_rev
            nsw_share = benefit_labor_share - tax_labor_share

            if not wbf.empty and yr in wbf.index:
                exp_gdp = wbf.loc[yr].get("govt_expenditure_pct_gdp", np.nan)
                if not np.isnan(exp_gdp):
                    nsw_gdp[yr] = (nsw_share / 100.0) * (exp_gdp / 100.0)

    # Fallback: World Bank-only for years not covered by SBB
    if not wbf.empty:
        for yr in wbf.index:
            if yr in nsw_gdp.index or yr < 1980 or yr > 2019:
                continue
            ls = labor_share.get(yr, np.nan)
            if np.isnan(ls):
                continue

            tax_pct = wbf.loc[yr].get("tax_revenue_pct_gdp", np.nan)
            exp_pct = wbf.loc[yr].get("govt_expenditure_pct_gdp", np.nan)
            if np.isnan(tax_pct) or np.isnan(exp_pct):
                continue

            benefit_pct = np.nan  # WB fallback removed (no paper citation for 0.35 scalar; DEC-012)
            tax_labor_pct = tax_pct * ls
            nsw_gdp[yr] = (benefit_pct - tax_labor_pct) / 100.0

    nsw_gdp = nsw_gdp.sort_index()

    if len(nsw_gdp) > 0:
        out_df = pd.DataFrame({"book": nsw_gdp, "combined": nsw_gdp})
        out_df.index.name = "year"
        out_df.to_csv(STUDIES_OUT / "N1602.csv")
        data_dict["N1602"] = nsw_gdp
        outputs.append(str(STUDIES_OUT / "N1602.csv"))
        mean_nsw = float(nsw_gdp.mean())
        all_neg = bool((nsw_gdp < 0).all())
        steps.append(f"N1602: {len(nsw_gdp)} years, mean={mean_nsw:.4f}, all_neg={all_neg}")
        print(f"    [P18] N1602: {len(nsw_gdp)} years (mean={mean_nsw:.4f})")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "data_unavailable",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
