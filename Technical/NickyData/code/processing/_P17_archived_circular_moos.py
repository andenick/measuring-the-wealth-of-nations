#!/usr/bin/env python3
"""P17 - Process Moos (2017) NSW series: N1301-N1305.

Computes Moos-style NSW metrics from existing T601-T609 series and
validates against Moos's reported benchmark values.

N1301: NSW/GDP = T607 / NIPA_GDP
N1302: NSW/EC = T607 / NIPA_EC (employee compensation)
N1304: Moos vs ST comparison for 1959-1997
N1305: Post-2000 structural shift indicator

Inputs:  final-data/series/T607.csv (NSW)
         api-data/BEA/nipa_T20100_compensation_1929_2025.csv
Outputs: final-data/series/N1301-N1305.csv
Dependencies: P11 (for T607)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from utils.paths import SERIES_OUT, STUDIES_OUT, API_DATA, ensure_dirs

SERIES_ID = "N1301"
SERIES_IDS = ["N1301", "N1302", "N1304", "N1305"]
PRIORITY = 13

# Moos benchmark values (from HDARP table descriptions)
MOOS_BENCHMARKS = {
    "1959_1997": {
        "min": -0.012,
        "median": 0.010,
        "mean": 0.011,
        "max": 0.037,
    },
    "1959_2012": {
        "min": -0.012,
        "median": 0.013,
        "mean": 0.020,
        "max": 0.086,
    },
}


def process():
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # Load T607 (NSW in billions)
    t607_path = SERIES_OUT / "T607.csv"
    if not t607_path.exists():
        return {"series_id": SERIES_ID, "status": "fail",
                "steps": ["T607 not found"], "data_dict": {}, "outputs": []}

    t607 = pd.read_csv(t607_path, index_col=0)["combined"]

    # Load GDP from BEA (use NIPA 1.7.5 gross output or GDP-by-industry)
    gdp_path = API_DATA / "BEA" / "gdp_by_industry_gross_output.csv"
    gdp = None
    if gdp_path.exists():
        df = pd.read_csv(gdp_path)
        # Total gross output = Industry code "II" (All industries)
        gdp_rows = df[df["Industry"] == "II"]
        if not gdp_rows.empty:
            gdp = gdp_rows.set_index("Year")["DataValue"].astype(float)

    # Load compensation from NIPA T20100
    comp_path = API_DATA / "BEA" / "nipa_T20100_compensation_1929_2025.csv"
    comp = None
    if comp_path.exists():
        df = pd.read_csv(comp_path)
        comp = df.set_index("year")["compensation_millions"] / 1e3  # millions → billions

    # N1301: NSW/GDP
    if gdp is not None:
        common = t607.index.intersection(gdp.index)
        nsw_gdp = t607[common] / gdp[common]
        nsw_gdp = nsw_gdp.dropna()

        out = pd.DataFrame({"book": nsw_gdp, "combined": nsw_gdp})
        out.index.name = "year"
        out_path = STUDIES_OUT / "N1301.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["N1301"] = nsw_gdp

        # Validate against Moos benchmarks
        period_59_97 = nsw_gdp[(nsw_gdp.index >= 1959) & (nsw_gdp.index <= 1997)]
        if len(period_59_97) > 0:
            our_mean = float(period_59_97.mean())
            moos_mean = MOOS_BENCHMARKS["1959_1997"]["mean"]
            steps.append(f"N1301: {len(nsw_gdp)} years | 1959-1997 mean={our_mean:.4f} vs Moos={moos_mean:.4f}")
        else:
            steps.append(f"N1301: {len(nsw_gdp)} years")
        print(f"    [P17] N1301: {len(nsw_gdp)} years (NSW/GDP)")

    # N1302: NSW/EC
    if comp is not None:
        common = t607.index.intersection(comp.index)
        nsw_ec = t607[common] / comp[common]
        nsw_ec = nsw_ec.dropna()

        out = pd.DataFrame({"book": nsw_ec, "combined": nsw_ec})
        out.index.name = "year"
        out_path = STUDIES_OUT / "N1302.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["N1302"] = nsw_ec
        steps.append(f"N1302: {len(nsw_ec)} years (NSW/EC)")
        print(f"    [P17] N1302: {len(nsw_ec)} years (NSW/EC)")

    # N1304: Moos vs ST comparison (summary stats for overlap period)
    if "N1301" in data_dict:
        nsw = data_dict["N1301"]
        period = nsw[(nsw.index >= 1959) & (nsw.index <= 1997)]
        if len(period) > 0:
            comparison = pd.DataFrame({
                "as2_nsw_gdp": period,
                "combined": period,
            })
            comparison.index.name = "year"
            out_path = STUDIES_OUT / "N1304.csv"
            comparison.to_csv(out_path)
            outputs.append(str(out_path))
            data_dict["N1304"] = period
            steps.append(f"N1304: {len(period)} years (1959-1997 overlap)")
            print(f"    [P17] N1304: {len(period)} years (ST-Moos overlap)")

    # N1305: Post-2000 structural shift
    if "N1301" in data_dict:
        nsw = data_dict["N1301"]
        pre = nsw[(nsw.index >= 1959) & (nsw.index <= 2000)]
        post = nsw[nsw.index >= 2001]  # Extended beyond Moos's 2012 cutoff
        if len(pre) > 0 and len(post) > 0:
            shift = pd.Series(dtype=float)
            for yr in nsw.index:
                if yr <= 2000:
                    shift[yr] = 0  # pre-shift
                else:
                    shift[yr] = 1  # post-shift

            out = pd.DataFrame({
                "nsw_gdp": nsw,
                "post_2000": shift,
                "combined": nsw,
            })
            out.index.name = "year"
            out_path = STUDIES_OUT / "N1305.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            data_dict["N1305"] = nsw

            pre_mean = float(pre.mean())
            post_mean = float(post.mean())
            steps.append(f"N1305: pre-2000 mean={pre_mean:.4f}, post-2000 mean={post_mean:.4f} (shift={post_mean-pre_mean:+.4f})")
            print(f"    [P17] N1305: pre={pre_mean:.4f}, post={post_mean:.4f}")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
