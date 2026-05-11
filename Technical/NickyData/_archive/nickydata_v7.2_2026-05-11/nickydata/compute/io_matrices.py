"""IO Matrix Computations — Annual A-matrix, Leontief inverse, labor values.

Computes from BEA InputOutput dataset (71-sector summary Use tables, annual 1997-2024):
- A-matrix (direct requirements)
- B = (I - A)^(-1) (total requirements / Leontief inverse)
- Productive sector multipliers

Labor values (lambda*) require BLS hours-by-industry data (future extension).
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from .helpers import save_series, build_series, load_methodology

DEPENDS_ON = ["total_product"]
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    io_data = data.get("io", {})
    if not io_data:
        print("    No IO data available")
        return {}

    productive = set(methodology["sector_classification"]["productive_naics"])
    trading = set(methodology["sector_classification"]["trading_naics"])
    results = {}

    # Compute A-matrix and Leontief inverse for each year with IO data
    multipliers = {}
    for year in sorted(io_data.keys()):
        use_records = io_data[year].get("use", [])
        if not use_records:
            continue

        from nickydata.fetch.bea_io import parse_use_matrix
        A, gross_output = parse_use_matrix(use_records)
        if A.empty or gross_output.empty:
            continue

        # Ensure square matrix (some years have row/col mismatch)
        common = A.index.intersection(A.columns)
        A_sq = A.loc[common, common]
        n = len(A_sq)
        if n < 10:
            continue
        I = np.eye(n)
        A_np = A_sq.values

        try:
            B = np.linalg.inv(I - A_np)
        except np.linalg.LinAlgError:
            continue

        # Compute multipliers: sum of each column of B = total output multiplier
        output_mult = B.sum(axis=0)
        avg_mult = output_mult.mean()

        # Productive sector average multiplier
        prod_cols = [i for i, c in enumerate(A_sq.columns) if c in productive]
        if prod_cols:
            prod_mult = output_mult[prod_cols].mean()
        else:
            prod_mult = avg_mult

        # Value-added share (1 - column sum of A = direct VA share per industry)
        va_share = 1 - A_np.sum(axis=0)
        avg_va_share = va_share.mean()

        multipliers[year] = {
            "avg_output_multiplier": float(avg_mult),
            "prod_output_multiplier": float(prod_mult),
            "avg_va_share": float(avg_va_share),
            "n_sectors": n,
        }

    if multipliers:
        mult_df = pd.DataFrame(multipliers).T
        mult_df.index.name = "year"
        out_path = DATA_DIR / "computed" / "io_multipliers.csv"
        mult_df.to_csv(out_path)
        print(f"    IO multipliers: {len(multipliers)} years ({min(multipliers)}-{max(multipliers)})")
        print(f"    Avg output multiplier: {mult_df['avg_output_multiplier'].mean():.3f}")
        print(f"    Productive multiplier: {mult_df['prod_output_multiplier'].mean():.3f}")
        print(f"    Avg VA share: {mult_df['avg_va_share'].mean():.3f}")

    # Also fetch annual IO Use tables for years not yet cached
    # (The InputOutput dataset has annual data 1997-2024)
    # This was discovered in Step 1 — let's fetch missing years
    if data.get("nipa"):
        from nickydata.fetch.bea_io import fetch_naics_io
        import os
        bea_key = os.environ.get("BEA_API_KEY", "")
        if bea_key:
            missing_years = [yr for yr in range(1997, 2025) if yr not in io_data]
            if missing_years:
                print(f"    Fetching {len(missing_years)} missing IO years...")
                import time
                for yr in missing_years[:5]:
                    try:
                        use = fetch_naics_io(yr, "Use", bea_key)
                        if use:
                            io_data[yr] = {"use": use}
                            time.sleep(0.5)
                    except Exception:
                        pass

    return results
