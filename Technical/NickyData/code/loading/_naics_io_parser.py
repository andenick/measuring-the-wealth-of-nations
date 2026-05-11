#!/usr/bin/env python3
"""L11b - Parse NAICS IO Tables from BEA JSON into CSV matrices.

Input:   Inputs/IO_Matrices/NAICS/{Use,Total_Requirements,Supply}_of_Commodities_Summary_{year}.json
         for years 1997, 2002, 2007, 2012, 2017
Output:  Inputs/IO_Matrices/NAICS/{year}_A_matrix_naics.csv
         Inputs/IO_Matrices/NAICS/{year}_L_matrix_naics.csv
         data/final-data/book/series/IO_productive_ratios.csv (annual interpolated)
Dependencies: None
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd

NAICS_DIR = Path("D:/Arcanum/Projects/ST2/Inputs/IO_Matrices/NAICS")
BENCHMARK_YEARS = [1997, 2002, 2007, 2012, 2017]

# Productive sector classification (Shaikh & Tonak criteria adapted to NAICS summary)
# Productive = goods production + transport + utilities + productive services
# Unproductive = FIRE, real estate, business services, government
# Trading = wholesale + retail
CLASSIFICATION = {
    "111CA": "productive",   # Farms
    "113FF": "productive",   # Forestry, fishing
    "211":   "productive",   # Oil and gas extraction
    "212":   "productive",   # Mining (except oil)
    "213":   "productive",   # Support activities for mining
    "22":    "productive",   # Utilities
    "23":    "productive",   # Construction
    "311FT": "productive",   # Food, beverages, tobacco
    "313TT": "productive",   # Textile mills, apparel
    "315AL": "productive",   # Apparel, leather
    "321":   "productive",   # Wood products
    "322":   "productive",   # Paper products
    "323":   "productive",   # Printing
    "324":   "productive",   # Petroleum and coal
    "325":   "productive",   # Chemical products
    "326":   "productive",   # Plastics and rubber
    "327":   "productive",   # Nonmetallic mineral
    "331":   "productive",   # Primary metals
    "332":   "productive",   # Fabricated metals
    "333":   "productive",   # Machinery
    "334":   "productive",   # Computer and electronic
    "335":   "productive",   # Electrical equipment
    "3361MV":"productive",   # Motor vehicles
    "3364OT":"productive",   # Other transportation equip
    "337":   "productive",   # Furniture
    "339":   "productive",   # Miscellaneous manufacturing
    "42":    "trading",      # Wholesale trade
    "44RT":  "trading",      # Retail trade
    "481":   "productive",   # Air transportation
    "482":   "productive",   # Rail transportation
    "483":   "productive",   # Water transportation
    "484":   "productive",   # Truck transportation
    "485":   "productive",   # Transit and ground passenger
    "486":   "productive",   # Pipeline transportation
    "487OS": "productive",   # Other transportation
    "493":   "productive",   # Warehousing and storage
    "511":   "unproductive", # Publishing (includes software)
    "512":   "productive",   # Motion picture and recording
    "513":   "unproductive", # Broadcasting and telecom
    "514":   "unproductive", # Data processing, internet
    "521CI": "unproductive", # Fed Reserve, credit intermediation
    "523":   "unproductive", # Securities, commodity contracts
    "524":   "unproductive", # Insurance
    "525":   "unproductive", # Funds, trusts, other financial
    "HS":    "unproductive", # Housing (owner-occupied)
    "ORE":   "unproductive", # Other real estate
    "532RL": "unproductive", # Rental and leasing
    "5411":  "unproductive", # Legal services
    "5412OP":"unproductive", # Miscellaneous professional
    "5415":  "unproductive", # Computer systems design
    "55":    "unproductive", # Management of companies
    "561":   "unproductive", # Administrative and support
    "562":   "productive",   # Waste management
    "61":    "productive",   # Educational services
    "621":   "productive",   # Ambulatory health care
    "622":   "productive",   # Hospitals
    "623":   "productive",   # Nursing and residential care
    "624":   "productive",   # Social assistance
    "711AS": "productive",   # Performing arts, spectator sports
    "713":   "productive",   # Amusements, gambling, recreation
    "721":   "productive",   # Accommodation
    "722":   "productive",   # Food services and drinking
    "81":    "productive",   # Other services
    "GFE":   "government",   # Federal government enterprises
    "GSLE":  "government",   # State/local government enterprises
    "GFG":   "government",   # General federal government
    "GSLG":  "government",   # General state/local government
}


def _parse_bea_io_json(filepath: Path) -> pd.DataFrame:
    """Parse BEA IO JSON into a records DataFrame."""
    with open(filepath, encoding="utf-8") as f:
        raw = json.load(f)
    data = raw["BEAAPI"]["Results"][0]["Data"]
    df = pd.DataFrame(data)
    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")
    return df


def _build_matrix(df: pd.DataFrame, row_filter: str = "Industry", col_filter: str = "Industry") -> pd.DataFrame:
    """Pivot IO data into a square matrix."""
    subset = df[(df["RowType"] == row_filter) & (df["ColType"] == col_filter)].copy()
    subset = subset[subset["RowCode"] != ""]
    subset = subset[subset["ColCode"] != ""]
    matrix = subset.pivot_table(
        index="RowCode", columns="ColCode", values="DataValue", aggfunc="first"
    ).fillna(0.0)
    return matrix


def _compute_a_matrix(use_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Compute A-matrix from Use table: a_ij = z_ij / x_j."""
    col_codes = use_df["ColCode"].astype(str)
    is_industry = ~col_codes.str.startswith("F") & ~col_codes.str.startswith("T") & (col_codes != "")
    industry_codes = sorted(col_codes[is_industry].unique())

    subset = use_df[use_df["ColCode"].isin(industry_codes)].copy()
    z = subset.pivot_table(
        index="RowCode", columns="ColCode", values="DataValue", aggfunc="first"
    ).fillna(0.0)

    # Total output: try T00TOP, then T018
    for total_code in ["T00TOP", "T018", "T019", "T001"]:
        total_row = use_df[use_df["RowCode"] == total_code]
        if not total_row.empty:
            break
    x = total_row.set_index("ColCode")["DataValue"]
    x = x[x.index.isin(industry_codes)]

    common_cols = z.columns.intersection(x.index)
    z = z[common_cols]
    x = x[common_cols]
    x_safe = x.replace(0, np.nan)

    A = z.div(x_safe, axis=1).fillna(0.0)
    return A, x


def load():
    """Parse NAICS IO tables and compute productive sector ratios."""
    steps = []
    outputs = []

    benchmark_data = {}

    for year in BENCHMARK_YEARS:
        use_path = NAICS_DIR / f"Use_of_Commodities_Summary_{year}.json"
        req_path = NAICS_DIR / f"Total_Requirements_IxI_Summary_{year}.json"

        if not use_path.exists() or not req_path.exists():
            steps.append(f"{year}: JSON files not found")
            continue

        # Parse Use table → A-matrix
        use_df = _parse_bea_io_json(use_path)
        A, gross_output = _compute_a_matrix(use_df)

        # Parse Total Requirements → Leontief inverse (B-matrix)
        req_df = _parse_bea_io_json(req_path)
        req_industry = req_df[
            ~req_df["RowCode"].str.startswith("F") &
            ~req_df["RowCode"].str.startswith("T") &
            (req_df["RowCode"] != "") &
            ~req_df["ColCode"].str.startswith("F") &
            ~req_df["ColCode"].str.startswith("T") &
            (req_df["ColCode"] != "")
        ]
        B = req_industry.pivot_table(
            index="RowCode", columns="ColCode", values="DataValue", aggfunc="first"
        ).fillna(0.0)

        # Save matrices
        a_path = NAICS_DIR / f"{year}_A_matrix_naics.csv"
        l_path = NAICS_DIR / f"{year}_L_matrix_naics.csv"
        A.to_csv(a_path)
        B.to_csv(l_path)
        outputs.extend([str(a_path), str(l_path)])

        # Compute productive sector ratios
        classified = {}
        for code in gross_output.index:
            classified[code] = CLASSIFICATION.get(code, "unproductive")

        go_prod = sum(gross_output[c] for c in gross_output.index if classified.get(c) == "productive")
        go_trade = sum(gross_output[c] for c in gross_output.index if classified.get(c) == "trading")
        go_total = gross_output.sum()

        # Intermediate inputs from Use table
        commodity_use = use_df[
            (use_df["RowType"] == "Commodity") & (use_df["ColType"] == "Industry")
        ].groupby("ColCode")["DataValue"].sum()

        m_prod = sum(commodity_use.get(c, 0) for c in commodity_use.index if classified.get(c) == "productive")
        m_total = commodity_use.sum()

        # Employment ratio from NIPA 6.5 (FTE by industry)
        # LineNumber -> classification mapping (per Appendix F sector rules)
        NIPA65_CLASSIFICATION = {
            4: "productive",    # Agriculture, forestry, fishing, hunting
            7: "productive",    # Mining
            11: "productive",   # Utilities
            12: "productive",   # Construction
            13: "productive",   # Manufacturing
            35: "trading",      # Wholesale trade
            38: "trading",      # Retail trade
            43: "productive",   # Transportation and warehousing
            52: "unproductive", # Information (mixed, but mostly unproductive per book)
            57: "unproductive", # Finance and insurance (FIRE)
            62: "unproductive", # Real estate and rental and leasing
            65: "unproductive", # Professional, scientific, technical services
            69: "unproductive", # Management of companies
            70: "mixed",        # Administrative and waste management
            73: "productive",   # Educational services
            74: "productive",   # Health care and social assistance
            79: "productive",   # Arts, entertainment, recreation
            82: "productive",   # Accommodation and food services
            85: "productive",   # Other services
            91: "productive",   # Federal government enterprises
            96: "productive",   # State/local government enterprises
        }
        fte_path = Path("D:/Arcanum/Projects/ST2/Inputs/API_Data/BEA/nipa_6_5D_fte_by_industry.csv")
        emp_prod_ratio = None
        if fte_path.exists():
            try:
                fte_raw = pd.read_csv(fte_path)
                yr_data = fte_raw[fte_raw["TimePeriod"] == year]
                emp_prod = 0
                emp_total = 0
                for _, row in yr_data.iterrows():
                    ln = int(row["LineNumber"])
                    val_str = str(row["DataValue"]).replace(",", "")
                    try:
                        val = float(val_str)
                    except ValueError:
                        continue
                    cls = NIPA65_CLASSIFICATION.get(ln)
                    if cls is None:
                        continue
                    if cls == "productive":
                        emp_prod += val
                    emp_total += val if cls != "mixed" else val * 0.5
                    if cls == "mixed":
                        emp_prod += val * 0.5  # waste mgmt is productive, admin is not
                if emp_total > 0:
                    emp_prod_ratio = emp_prod / emp_total
            except Exception:
                pass

        benchmark_data[year] = {
            "ratio_productive_output": (go_prod + go_trade) / go_total if go_total > 0 else 0,
            "ratio_productive_materials": m_prod / m_total if m_total > 0 else 0,
            "ratio_productive_employment": emp_prod_ratio if emp_prod_ratio else (go_prod + go_trade) / go_total,
            "go_productive": go_prod,
            "go_trading": go_trade,
            "go_total": go_total,
            "m_productive": m_prod,
            "n_sectors": len(A.columns),
            "a_matrix_shape": f"{A.shape[0]}x{A.shape[1]}",
        }

        # Condition number only for square submatrix
        sq_idx = A.index.intersection(A.columns)
        A_sq = A.loc[sq_idx, sq_idx]
        cond = np.linalg.cond(np.eye(len(A_sq)) - A_sq.values) if len(A_sq) > 0 else 0
        steps.append(f"{year}: A={A.shape[0]}x{A.shape[1]}, B={B.shape[0]}x{B.shape[1]}, "
                     f"cond={cond:.0f}, prod_ratio={benchmark_data[year]['ratio_productive_output']:.3f}")
        print(f"    [L11b] {year}: {A.shape[0]}x{A.shape[1]} A-matrix, "
              f"prod_output_ratio={benchmark_data[year]['ratio_productive_output']:.3f}")

    # Interpolate annual ratios (1997-2024)
    if benchmark_data:
        bm_df = pd.DataFrame(benchmark_data).T
        bm_df.index = bm_df.index.astype(int)
        ratio_cols = bm_df[["ratio_productive_output", "ratio_productive_materials", "ratio_productive_employment"]].astype(float)
        annual = ratio_cols.reindex(range(1997, 2025)).interpolate(method="linear")
        # Extrapolate 2018-2024 from last benchmark (2017)
        for col in annual.columns:
            annual[col] = annual[col].ffill()

        ratio_path = Path("data/final-data/book/series/IO_productive_ratios.csv")
        annual.index.name = "year"
        annual.to_csv(ratio_path)
        outputs.append(str(ratio_path))
        steps.append(f"Annual ratios: {len(annual)} years (1997-2024), interpolated from {len(benchmark_data)} benchmarks")
        print(f"    [L11b] Annual productive ratios: {len(annual)} years")

    return {
        "series_id": "IO_NAICS",
        "status": "ok" if benchmark_data else "fail",
        "steps": steps,
        "outputs": outputs,
    }


if __name__ == "__main__":
    result = load()
    for s in result["steps"]:
        print(s)
