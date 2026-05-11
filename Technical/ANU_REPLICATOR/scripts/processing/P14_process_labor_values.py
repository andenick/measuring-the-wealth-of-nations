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
from lib.paths import SERIES_OUT, PARSED_RAW, INPUTS, IO_MATRICES, ensure_dirs
from lib.transforms.io_transforms import compute_labor_values, classify_sectors

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

        # T702: Prices of production
        # Load Z-matrix for intermediate input costs
        z_path = IO_MATRICES / f"{year}_Z_matrix.csv"
        if z_path.exists():
            z_arr = np.loadtxt(z_path, delimiter=",")

            # c_j = sum of intermediate inputs to sector j (column sum of Z for productive inputs)
            prod_mask = np.array([s in productive_sectors for s in sector_labels])
            c_j = z_arr[prod_mask, :].sum(axis=0)  # intermediate costs from productive sectors

            # v_j = labor compensation proxy (employment × mean value-added per worker)
            emp = hp_df["employment"].values
            # Use labor value as weight for variable capital
            v_j = emp * lv_prod_mean  # simplified: v_j ∝ employment × avg labor value

            # Economy-wide surplus = gross output - c - v
            total_x = gross_output.sum()
            total_c = c_j.sum()
            total_v = v_j.sum()
            surplus = total_x - total_c - total_v
            capital_proxy = total_c + total_v
            r_bar = surplus / capital_proxy if capital_proxy > 0 else 0.0

            # pp_j = (1 + r_bar)(c_j + v_j)
            pp = (1 + r_bar) * (c_j + v_j)

            # Normalize to per-unit: pp_j / x_j
            with np.errstate(divide="ignore", invalid="ignore"):
                pp_unit = np.where(gross_output > 0, pp / gross_output, 0.0)

            t702_benchmarks[year] = r_bar
            steps.append(f"{year} T702: r_bar={r_bar:.4f}")

            # T703: Value-price deviation
            # Compare labor values to production prices for productive sectors
            lv_arr = labor_values.values
            valid = (lv_arr > 0) & (pp_unit > 0)
            if valid.sum() > 2:
                mad = np.abs(lv_arr[valid] - pp_unit[valid]).mean()
                corr = np.corrcoef(lv_arr[valid], pp_unit[valid])[0, 1]
                # R² from log regression
                log_lv = np.log(lv_arr[valid])
                log_pp = np.log(pp_unit[valid])
                ss_res = ((log_lv - log_pp) ** 2).sum()
                ss_tot = ((log_lv - log_lv.mean()) ** 2).sum()
                r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

                t703_benchmarks[year] = r_squared
                steps.append(f"{year} T703: MAD={mad:.6f}, corr={corr:.4f}, R²={r_squared:.4f}")
            else:
                steps.append(f"{year} T703: insufficient valid sectors for deviation analysis")
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
