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
SIC_BENCHMARK_YEARS = [1947, 1958, 1963, 1967, 1972, 1977]
NAICS_BENCHMARK_YEARS = [1997, 2002, 2007, 2012, 2017]
BENCHMARK_YEARS = SIC_BENCHMARK_YEARS  # SIC years processed as before


def _load_concordance_classification():
    conc_path = INPUTS / "Concordances" / "io_85_to_nipa_13_concordance.csv"
    df = pd.read_csv(conc_path)
    return df["io_sector_name"].tolist(), dict(zip(df["io_sector_name"], df["classification"]))


def _interpolate_annual(benchmark_data, year_range=None):
    """Linear interpolation between benchmark years."""
    if year_range is None:
        min_yr = min(benchmark_data.keys())
        max_yr = max(benchmark_data.keys())
        year_range = (min_yr, max_yr)
    idx = pd.RangeIndex(year_range[0], year_range[1] + 1)
    s = pd.Series(benchmark_data, dtype=float)
    s = s.reindex(idx)
    s = s.interpolate(method="index")
    return s


def process():
    """Process labor values, prices of production, and deviations."""
    ensure_dirs()
    steps = []
    scatter_frames = []
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

            # T703a: Ochoa-style regression: log(market_value) on log(labor_value)
            # Market value = GO_j (gross output in $), Labor value = lambda*_j × GO_j (hours)
            # This is the CORRECT specification per Section 5.10: R² should be ~0.98 for SIC era
            lv_arr = labor_values.values[:n_sectors]
            x_j = gross_output[:n_sectors]
            total_lv = lv_arr * x_j  # total labor values (hours)
            total_mv = x_j            # total market values ($)

            valid_ochoa = (total_lv > 0) & (total_mv > 0) & (x_j > 0)
            if valid_ochoa.sum() > 5:
                log_lv_o = np.log(total_lv[valid_ochoa])
                log_mv_o = np.log(total_mv[valid_ochoa])
                slope_o, intercept_o = np.polyfit(log_lv_o, log_mv_o, 1)
                corr_o = np.corrcoef(log_lv_o, log_mv_o)[0, 1]
                r_sq_o = corr_o ** 2
                steps.append(f"{year} T703 Ochoa: R2={r_sq_o:.4f}, slope={slope_o:.3f}, n={valid_ochoa.sum()}")
                print(f"    [P14] {year} Ochoa: R2={r_sq_o:.4f}, slope={slope_o:.3f}, n={valid_ochoa.sum()}")

                # Export scatter data for Shiny visualization
                sector_names = sector_labels[:n_sectors] if len(sector_labels) >= n_sectors else [f"sector_{i}" for i in range(n_sectors)]
                scatter_rows = []
                for i in range(n_sectors):
                    if valid_ochoa[i]:
                        scatter_rows.append({
                            "year": year,
                            "sector": sector_names[i] if i < len(sector_names) else f"sector_{i}",
                            "log_labor_value": float(log_lv_o[sum(valid_ochoa[:i])]) if sum(valid_ochoa[:i]) < len(log_lv_o) else np.nan,
                            "log_market_price": float(log_mv_o[sum(valid_ochoa[:i])]) if sum(valid_ochoa[:i]) < len(log_mv_o) else np.nan,
                            "labor_value": float(total_lv[i]),
                            "market_price": float(total_mv[i]),
                        })
                scatter_frames.append(pd.DataFrame(scatter_rows))

            # T703b: PP regression (comparison)
            total_pp = pp_j
            valid = prod_mask & (total_lv > 0) & (total_pp > 0)
            if valid.sum() > 5:
                log_lv_total = np.log(total_lv[valid])
                log_pp_total = np.log(total_pp[valid])
                slope, intercept = np.polyfit(log_lv_total, log_pp_total, 1)
                predicted = slope * log_lv_total + intercept
                ss_res = ((log_pp_total - predicted) ** 2).sum()
                ss_tot = ((log_pp_total - log_pp_total.mean()) ** 2).sum()
                r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

                t703_benchmarks[year] = r_squared
                steps.append(f"{year} T703 PP: R2={r_squared:.4f}, slope={slope:.3f}, n={valid.sum()}")
            else:
                steps.append(f"{year} T703: insufficient valid sectors ({valid.sum()})")
        else:
            steps.append(f"{year}: Z-matrix not found, skipping T702/T703")

        print(f"    [P14] {year}: labor values computed ({len(labor_values)} sectors)")

    # NAICS era (1997-2017): use NAICS IO matrices from L11b
    naics_dir = Path(__file__).resolve().parents[3] / "Inputs" / "IO_Matrices/NAICS")
    fte_path = Path(__file__).resolve().parents[3] / "Inputs" / "API_Data/BEA/nipa_6_5D_fte_by_industry.csv")
    naics_cls_path = Path(__file__).resolve().parent.parent.parent / "classifications.json"

    if naics_dir.exists() and naics_cls_path.exists():
        import json as _json
        with open(naics_cls_path, encoding="utf-8") as f:
            naics_cls_raw = _json.load(f)
        naics_io_cls = {k: v for k, v in naics_cls_raw.get("naics_io", {}).items()
                        if not k.startswith("_")}
        naics_productive = {c for c, v in naics_io_cls.items() if v == "productive"}

        # Load FTE data for employment distribution
        fte_raw = pd.read_csv(fte_path) if fte_path.exists() else pd.DataFrame()

        for year in NAICS_BENCHMARK_YEARS:
            a_path = naics_dir / f"{year}_A_matrix_naics.csv"
            l_path = naics_dir / f"{year}_L_matrix_naics.csv"
            if not a_path.exists() or not l_path.exists():
                steps.append(f"{year} NAICS: matrices not found")
                continue

            try:
                A_naics = pd.read_csv(a_path, index_col=0)
                B_naics = pd.read_csv(l_path, index_col=0)

                # Align A and B to common sectors
                common_sectors_ab = A_naics.columns.intersection(B_naics.columns)
                A_naics = A_naics.loc[common_sectors_ab, common_sectors_ab]
                B_naics = B_naics.loc[common_sectors_ab, common_sectors_ab]
            except Exception as e:
                steps.append(f"{year} NAICS: matrix parse/align error ({e})")
                continue

            n_sectors = len(A_naics)
            try:  # wrap entire NAICS year computation
            sector_codes = list(A_naics.columns)

            # Approximate hp* from FTE data: hp*_j = FTE_j / GO_j
            # GO_j approximated from column sums of Use table or from detail_io_aggregates
            # Simpler: use B-matrix diagonal as proxy for labor intensity
            # The Leontief inverse B_jj gives total output needed per unit of final demand
            # For a first approximation, use 1/B_jj as relative labor efficiency

            # Better approach: construct hp* from NIPA 6.5D FTE if available
            hp_naics = pd.Series(0.0, index=sector_codes)

            if not fte_raw.empty:
                yr_fte = fte_raw[fte_raw["TimePeriod"] == year]
                # Map NIPA 6.5D aggregate lines to NAICS IO sector codes
                # This is approximate — NIPA lines aggregate multiple IO sectors
                nipa_to_io = {
                    4: ["111CA", "113FF"],
                    7: ["211", "212", "213"],
                    11: ["22"],
                    12: ["23"],
                    13: ["311FT", "313TT", "315AL", "321", "322", "323", "324", "325",
                         "326", "327", "331", "332", "333", "334", "335", "3361MV", "3364OT", "337", "339"],
                    35: ["42"],
                    38: ["44RT"],
                    43: ["481", "482", "483", "484", "485", "486", "487OS", "493"],
                    73: ["61"],
                    74: ["621", "622", "623", "624"],
                    79: ["711AS", "713"],
                    82: ["721", "722"],
                    85: ["81"],
                }
                for _, row in yr_fte.iterrows():
                    ln = int(row["LineNumber"])
                    val_str = str(row["DataValue"]).replace(",", "")
                    try:
                        fte_val = float(val_str)
                    except ValueError:
                        continue
                    io_codes = nipa_to_io.get(ln, [])
                    if io_codes:
                        per_code = fte_val / len(io_codes)
                        for c in io_codes:
                            if c in hp_naics.index:
                                hp_naics[c] = per_code

            # Normalize: hp*_j = FTE_j / GO_j (use A-matrix column sums + 1 as GO proxy)
            go_proxy = A_naics.sum(axis=0) + 1.0
            for c in sector_codes:
                if hp_naics.get(c, 0) > 0 and go_proxy.get(c, 0) > 0:
                    hp_naics[c] = hp_naics[c] / go_proxy[c]

            if hp_naics.sum() <= 0:
                steps.append(f"{year} NAICS: no employment data, using uniform hp*")
                hp_naics = pd.Series(1.0 / n_sectors, index=sector_codes)

            # T701: labor values lv* = hp* @ B
            # Align indices: hp* and B may have different sector orderings
            common_sectors = hp_naics.index.intersection(B_naics.columns)
            hp_aligned = hp_naics.reindex(common_sectors, fill_value=0)
            B_aligned = B_naics.loc[common_sectors, common_sectors]
            lv_naics = hp_aligned @ B_aligned
            lv_naics = lv_naics.reindex(sector_codes, fill_value=0)
            lv_prod = lv_naics[[c for c in lv_naics.index if c in naics_productive]]
            lv_mean = float(lv_prod.mean()) if len(lv_prod) > 0 else float(lv_naics.mean())
            t701_benchmarks[year] = lv_mean

            # T702: uniform profit rate using GDPbyIndustry VA data (WP-2 fix)
            prod_mask = np.array([c in naics_productive for c in sector_codes])

            # Load actual VA by industry from L21 for this year
            va_annual_path = PARSED_RAW / "gdpbyindustry_va_annual.csv"
            va_by_sector = {}
            if va_annual_path.exists():
                va_annual = pd.read_csv(va_annual_path)
                yr_va = va_annual[va_annual["year"] == year]
                for _, row in yr_va.iterrows():
                    ind = row.get("industry", "")
                    val = row.get("value_added")
                    if ind and pd.notna(val):
                        va_by_sector[ind] = val

            # Map VA to IO sector codes
            va_j = np.zeros(n_sectors)
            for i, code in enumerate(sector_codes):
                va_j[i] = va_by_sector.get(code, 0.0)

            # If no L21 data, fall back to A-matrix proxy
            if sum(va_j) <= 0:
                go_vals = (A_naics.sum(axis=0) + 1.0).values
                a_vals = A_naics.values
                c_j_proxy = a_vals.sum(axis=0) * go_vals
                va_j = go_vals - c_j_proxy

            t507_path = SERIES_OUT / "T507.csv"
            v_va_ratio = 0.40
            if t507_path.exists():
                t507_df = pd.read_csv(t507_path, index_col=0)
                col = "combined" if "combined" in t507_df.columns else "book"
                closest = min(t507_df.index, key=lambda y: abs(y - year))
                v_va_ratio = 1.0 - t507_df.loc[closest, col]

            v_j = np.where(prod_mask & (va_j > 0), va_j * v_va_ratio, 0.0)
            s_j = np.where(prod_mask & (va_j > 0), va_j * (1.0 - v_va_ratio), 0.0)
            k_total = v_j[prod_mask].sum()
            r_bar = s_j[prod_mask].sum() / k_total if k_total > 0 else 0.0
            t702_benchmarks[year] = r_bar

            # T703: Ochoa regression — use A-matrix proxy for GO
            go_proxy_series = A_naics.sum(axis=0) + 1.0
            # Ensure alignment: lv_naics, go, and prod_mask must have same length
            common_cols = lv_naics.index.intersection(go_proxy_series.index)
            lv_aligned = lv_naics.reindex(common_cols, fill_value=0).values
            go_aligned = go_proxy_series.reindex(common_cols, fill_value=0).values
            pm_aligned = np.array([c in naics_productive for c in common_cols])
            total_lv = lv_aligned * go_aligned
            total_mv = go_aligned
            valid = (total_lv > 0) & (total_mv > 0) & pm_aligned
            if valid.sum() > 5:
                log_lv = np.log(total_lv[valid])
                log_mv = np.log(total_mv[valid])
                slope, _ = np.polyfit(log_lv, log_mv, 1)
                corr = np.corrcoef(log_lv, log_mv)[0, 1]
                r_sq = corr ** 2
                t703_benchmarks[year] = r_sq
                print(f"    [P14] {year} NAICS Ochoa: R2={r_sq:.4f}, slope={slope:.3f}, n={valid.sum()}")
            else:
                print(f"    [P14] {year} NAICS: insufficient valid sectors")

                steps.append(f"{year} NAICS: lv_mean={lv_mean:.6f}, r_bar={r_bar:.4f}")
                print(f"    [P14] {year} NAICS: labor values computed ({n_sectors} sectors)")
            except Exception as e:
                steps.append(f"{year} NAICS: computation error ({e})")
                print(f"    [P14] {year} NAICS: SKIP ({e})")

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

    # Write scatter data for Shiny visualization
    if scatter_frames:
        scatter_df = pd.concat(scatter_frames, ignore_index=True)
        from utils.paths import SHINY_OUT
        scatter_path = SHINY_OUT / "T701_scatter.csv"
        scatter_df.to_csv(scatter_path, index=False)
        outputs.append(str(scatter_path))
        steps.append(f"Scatter data: {len(scatter_df)} points across {scatter_df['year'].nunique()} benchmarks")

    status = "ok" if data_dict else "fail"

    return {
        "series_id": SERIES_ID,
        "status": status,
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
