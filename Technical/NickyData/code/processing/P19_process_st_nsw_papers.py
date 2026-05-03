#!/usr/bin/env python3
"""P19 - Process Shaikh-Tonak NSW papers: Ch11 (1987) + Ch12 (2002).

Both papers use the same framework as T601-T609 but for different periods.
We compute their reported metrics from our existing NSW series.

Ch11 (1987): N1101-N1103 — net transfer rate, benefit rate, tax rate (1952-1985)
Ch12 (2002): N1201-N1202 — NSW/GDP, NSW/EC (1952-1997)

Inputs:  final-data/series/T604.csv (total taxes)
         final-data/series/T605.csv (total benefits)
         final-data/series/T607.csv (NSW)
         api-data/BEA/nipa_T20100_compensation_1929_2025.csv
Outputs: final-data/series/N1101-N1103.csv, N1201-N1202.csv
Dependencies: P09, P10, P11
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, STUDIES_OUT, API_DATA, ensure_dirs

SERIES_ID = "N1101"
SERIES_IDS = ["N1101", "N1102", "N1103", "N1201", "N1202"]
PRIORITY = 13


def process():
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # Load existing NSW components
    t604 = t605 = t607 = comp = None
    for sid, var in [("T604", "t604"), ("T605", "t605"), ("T607", "t607")]:
        path = SERIES_OUT / f"{sid}.csv"
        if path.exists():
            locals()[var] = pd.read_csv(path, index_col=0)["combined"]

    t604 = pd.read_csv(SERIES_OUT / "T604.csv", index_col=0)["combined"] if (SERIES_OUT / "T604.csv").exists() else None
    t605 = pd.read_csv(SERIES_OUT / "T605.csv", index_col=0)["combined"] if (SERIES_OUT / "T605.csv").exists() else None
    t607 = pd.read_csv(SERIES_OUT / "T607.csv", index_col=0)["combined"] if (SERIES_OUT / "T607.csv").exists() else None

    # Load compensation
    comp_path = API_DATA / "BEA" / "nipa_T20100_compensation_1929_2025.csv"
    if comp_path.exists():
        df = pd.read_csv(comp_path)
        comp = df.set_index("year")["compensation_millions"] / 1e3  # → billions

    # === Ch11: Shaikh & Tonak (1987) 1952-1985 ===

    if t604 is not None and t605 is not None and comp is not None:
        # Restrict to 1952-1985 (paper's period)
        years = [y for y in range(1952, 1986)]

        # N1101: Net Transfer Rate = (Benefits - Taxes) / EC
        common = t605.index.intersection(t604.index).intersection(comp.index)
        common = [y for y in common if y in years]
        if common:
            net_transfer = (t605[common] - t604[common]) / comp[common]
            out = pd.DataFrame({"book": net_transfer, "combined": net_transfer})
            out.index.name = "year"
            (STUDIES_OUT / "N1101.csv").open("w").close()  # ensure exists
            out.to_csv(STUDIES_OUT / "N1101.csv")
            data_dict["N1101"] = net_transfer
            outputs.append(str(STUDIES_OUT / "N1101.csv"))
            steps.append(f"N1101: {len(net_transfer)} years (net transfer rate)")
            print(f"    [P19] N1101: {len(net_transfer)} years (net transfer rate)")

        # N1102: Social Benefit Rate = Benefits / EC
        if common:
            benefit_rate = t605[common] / comp[common]
            out = pd.DataFrame({"book": benefit_rate, "combined": benefit_rate})
            out.index.name = "year"
            out.to_csv(STUDIES_OUT / "N1102.csv")
            data_dict["N1102"] = benefit_rate
            outputs.append(str(STUDIES_OUT / "N1102.csv"))
            steps.append(f"N1102: {len(benefit_rate)} years (benefit rate)")
            print(f"    [P19] N1102: {len(benefit_rate)} years")

        # N1103: Social Tax Rate = Taxes / EC
        if common:
            tax_rate = t604[common] / comp[common]
            out = pd.DataFrame({"book": tax_rate, "combined": tax_rate})
            out.index.name = "year"
            out.to_csv(STUDIES_OUT / "N1103.csv")
            data_dict["N1103"] = tax_rate
            outputs.append(str(STUDIES_OUT / "N1103.csv"))
            steps.append(f"N1103: {len(tax_rate)} years (tax rate)")
            print(f"    [P19] N1103: {len(tax_rate)} years")

    # === Ch12: Shaikh & Tonak (2002) 1952-1997 ===

    if t607 is not None and comp is not None:
        years = [y for y in range(1952, 1998)]

        # N1201: NSW/GDP — use T201 orthodox GDP (available 1929-2025 from L14)
        t201_path = SERIES_OUT / "T201.csv"
        gdp = None
        if t201_path.exists():
            t201_df = pd.read_csv(t201_path, index_col=0)
            if "GDP" in t201_df.columns:
                gdp = t201_df["GDP"].dropna()
                gdp = gdp / 1e9 if gdp.max() > 1e6 else gdp

        if gdp is None:
            gdp_path = API_DATA / "BEA" / "gdp_by_industry_gross_output.csv"
            if gdp_path.exists():
                gdp_df = pd.read_csv(gdp_path)
                gdp_rows = gdp_df[gdp_df["Industry"] == "II"]
                if not gdp_rows.empty:
                    gdp = gdp_rows.set_index("Year")["DataValue"].astype(float)

        if gdp is not None:
            common = t607.index.intersection(gdp.index)
            common = [y for y in common if y in years]
            if common:
                nsw_gdp = t607[common] / gdp[common]
                out = pd.DataFrame({"book": nsw_gdp, "combined": nsw_gdp})
                out.index.name = "year"
                out.to_csv(STUDIES_OUT / "N1201.csv")
                data_dict["N1201"] = nsw_gdp
                outputs.append(str(STUDIES_OUT / "N1201.csv"))
                avg = float(nsw_gdp.mean())
                steps.append(f"N1201: {len(nsw_gdp)} years (NSW/GDP, avg={avg:.4f})")
                print(f"    [P19] N1201: {len(nsw_gdp)} years (NSW/GDP avg={avg:.4f})")

        # N1202: NSW/EC
        common = t607.index.intersection(comp.index)
        common = [y for y in common if y in years]
        if common:
            nsw_ec = t607[common] / comp[common]
            out = pd.DataFrame({"book": nsw_ec, "combined": nsw_ec})
            out.index.name = "year"
            out.to_csv(STUDIES_OUT / "N1202.csv")
            data_dict["N1202"] = nsw_ec
            outputs.append(str(STUDIES_OUT / "N1202.csv"))
            steps.append(f"N1202: {len(nsw_ec)} years (NSW/EC)")
            print(f"    [P19] N1202: {len(nsw_ec)} years")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
