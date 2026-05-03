#!/usr/bin/env python3
"""P14 - Process labor values: T701, T702, T703.

For each benchmark year (1947-1977):
T701: Labor values lv* = hp* @ B (per sector + grouped summary)
T702: Prices of production pp_j = (1 + r_bar)(c_j + v_j)
T703: Value-price deviation metrics (MAD, correlation, R-squared)

Interpolates between benchmark years for annual 1947-1977 series.

Inputs:  parsed-raw/T701_{year}_hp_parsed.csv (from L12)
         parsed-raw/T402_{year}_parsed.csv (from L11)
         data/io-matrices/{year}_Z_matrix.csv
         Inputs/Concordances/io_85_to_nipa_13_concordance.csv
Outputs: final-data/series/T701.csv, T702.csv, T703.csv
Dependencies: L11, L12. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, INPUTS, IO_MATRICES, ensure_dirs
from utils.transforms.io_transforms import compute_labor_values, classify_sectors

SERIES_ID = "T701"
SERIES_IDS = ["T701", "T702", "T703"]
PRIORITY = 11
BENCHMARK_YEARS = [1947, 1958, 1963, 1967, 1972, 1977]


def _load_concordance_classification():
    conc_path = INPUTS / "Concordances" / "io_85_to_nipa_13_concordance.csv"
    df = pd.read_csv(conc_path)
    return df["io_sector_name"].tolist(), dict(zip(df["io_sector_name"], df["classification"]))


def _interpolate_annual(benchmark_data, year_range=(1947, 1977)):
    """Linear interpolation between benchmark years."""
    idx = pd.RangeIndex(year_range[0], year_range[1] + 1)
    s = pd.Series(benchmark_data, dtype=float)
    s = s.reindex(idx)
    s = s.interpolate(method="index")
    return s


def process():
    """Process labor values, prices of production, and deviations."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    sector_labels, classification = _load_concordance_classification()
    groups = classify_sectors(sector_labels, classification)
    productive_sectors = groups["productive"]

    t701_benchmarks = {}
    t702_benchmarks = {}
    t703_benchmarks = {}

    for year in BENCHMARK_YEARS:
        # Load hp* vector
        hp_path = PARSED_RAW / f"T701_{year}_hp_parsed.csv"
        b_path = PARSED_RAW / f"T402_{year}_parsed.csv"

        if not hp_path.exists() or not b_path.exists():
            steps.append(f"{year}: hp* or B matrix not found")
            continue

        hp_df = pd.read_csv(hp_path)
        b_df = pd.read_csv(b_path, index_col=0)

        # Build labor coefficients Series
        hp_series = pd.Series(hp_df["hp_star"].values, index=sector_labels)
        gross_output = hp_df["gross_output"].values

        # T701: Labor values lv* = hp* @ B
        labor_values = compute_labor_values(hp_series, b_df)

        # Summary: mean labor value for productive vs unproductive
        lv_prod = labor_values[labor_values.index.isin(productive_sectors)]
        lv_all_mean = labor_values.mean()
        lv_prod_mean = lv_prod.mean() if len(lv_prod) > 0 else 0.0
        t701_benchmarks[year] = lv_prod_mean
        steps.append(f"{year} T701: mean lv*={lv_all_mean:.6f} "
                     f"(productive={lv_prod_mean:.6f})")

        # T702: Prices of production (corrected methodology)
        # Uses value-added decomposition: VA_j = x_j - C_j, then V_j = VA_j × (V*/VA*)
        z_path = IO_MATRICES / f"{year}_Z_matrix.csv"
        if z_path.exists():
            z_arr = np.loadtxt(z_path, delimiter=",")
            n_sectors = len(sector_labels)

            # C_j = column sum of Z-matrix = total intermediate inputs to sector j
            c_j = z_arr[:n_sectors, :n_sectors].sum(axis=0)

            # VA_j = x_j - C_j (value added per sector)
            va_j = gross_output[:n_sectors] - c_j

            # V*/VA* ratio from book data (T507: S*/(S*+V*), so V*/VA* = 1 - T507)
            t507_path = SERIES_OUT / "T507.csv"
            v_va_ratio = 0.40
            if t507_path.exists():
                t507_df = pd.read_csv(t507_path, index_col=0)
                book_col = "book" if "book" in t507_df.columns else "combined"
                closest_yr = min(t507_df.index, key=lambda y: abs(y - year))
                surplus_ratio = t507_df.loc[closest_yr, book_col]
                v_va_ratio = 1.0 - surplus_ratio

            # V_j = VA_j × (V*/VA*) for productive sectors, 0 for unproductive
            prod_mask = np.array([s in productive_sectors for s in sector_labels[:n_sectors]])
            v_j = np.where(prod_mask & (va_j > 0), va_j * v_va_ratio, 0.0)
            s_j = np.where(prod_mask & (va_j > 0), va_j * (1.0 - v_va_ratio), 0.0)

            # Economy-wide uniform profit rate on productive sectors
            total_c_prod = c_j[prod_mask].sum()
            total_v_prod = v_j[prod_mask].sum()
            total_s_prod = s_j[prod_mask].sum()
            capital_total = total_c_prod + total_v_prod
            r_bar = total_s_prod / capital_total if capital_total > 0 else 0.0

            # Prices of production: PP_j = (1 + r̄)(C_j + V_j) for productive sectors
            pp_j = np.where(prod_mask, (1.0 + r_bar) * (c_j + v_j), 0.0)

            t702_benchmarks[year] = r_bar
            steps.append(f"{year} T702: r_bar={r_bar:.4f}, V*/VA*={v_va_ratio:.3f}")

            # T703: Value-price deviation (total-value regression)
            # Regress log(PP_j) on log(Λ_j) where Λ_j = λ_j × x_j (total labor value)
            lv_arr = labor_values.values[:n_sectors]
            x_j = gross_output[:n_sectors]
            total_lv = lv_arr * x_j  # total labor values (hours)
            total_pp = pp_j            # total prices of production ($)

            valid = prod_mask & (total_lv > 0) & (total_pp > 0)
            if valid.sum() > 5:
                log_lv_total = np.log(total_lv[valid])
                log_pp_total = np.log(total_pp[valid])
                slope, intercept = np.polyfit(log_lv_total, log_pp_total, 1)
                predicted = slope * log_lv_total + intercept
                ss_res = ((log_pp_total - predicted) ** 2).sum()
                ss_tot = ((log_pp_total - log_pp_total.mean()) ** 2).sum()
                r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
                corr = np.corrcoef(log_lv_total, log_pp_total)[0, 1]

                # Weighted average deviation
                wad = np.sum(np.abs(total_lv[valid] / total_lv[valid].sum() -
                                     total_pp[valid] / total_pp[valid].sum()))

                t703_benchmarks[year] = r_squared
                steps.append(f"{year} T703: R²={r_squared:.4f}, slope={slope:.3f}, "
                             f"corr={corr:.4f}, WAD={wad:.4f}, n={valid.sum()}")
            else:
                steps.append(f"{year} T703: insufficient valid sectors ({valid.sum()})")
        else:
            steps.append(f"{year}: Z-matrix not found, skipping T702/T703")

        print(f"    [P14] {year}: labor values computed ({len(labor_values)} sectors)")

    # Write output series with interpolation
    if t701_benchmarks:
        t701_annual = _interpolate_annual(t701_benchmarks)
        t701_out = pd.DataFrame({
            "value": t701_annual,
            "source": ["benchmark" if y in t701_benchmarks else "interpolated"
                        for y in t701_annual.index],
        })
        t701_out.index.name = "year"
        out_path = SERIES_OUT / "T701.csv"
        t701_out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["T701"] = t701_annual

    if t702_benchmarks:
        t702_annual = _interpolate_annual(t702_benchmarks)
        t702_out = pd.DataFrame({
            "value": t702_annual,
            "source": ["benchmark" if y in t702_benchmarks else "interpolated"
                        for y in t702_annual.index],
        })
        t702_out.index.name = "year"
        out_path = SERIES_OUT / "T702.csv"
        t702_out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["T702"] = t702_annual

    if t703_benchmarks:
        t703_annual = _interpolate_annual(t703_benchmarks)
        t703_out = pd.DataFrame({
            "value": t703_annual,
            "source": ["benchmark" if y in t703_benchmarks else "interpolated"
                        for y in t703_annual.index],
        })
        t703_out.index.name = "year"
        out_path = SERIES_OUT / "T703.csv"
        t703_out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["T703"] = t703_annual

    status = "ok" if data_dict else "fail"

    return {
        "series_id": SERIES_ID,
        "status": status,
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
