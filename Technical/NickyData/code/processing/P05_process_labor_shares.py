#!/usr/bin/env python3
"""P05 - Process labor shares: T511 (Lp/L), T512 (V*/W).

T511: IO-extended via productive employment ratio from L11b NAICS benchmarks.
T512: computed from V*/W components (T504 / NIPA total compensation).
Table5_7_Extended.csv is DEPRECATED (DEC-019).

Inputs:  parsed-raw/T511_parsed.csv, T512_parsed.csv (from L03)
         IO_productive_ratios.csv (from L11b)
         T504.csv (from P02, for T512 V*/W computation)
Outputs: final-data/series/T511.csv, T512.csv
Dependencies: L03. No upstream P## dependencies (PRIORITY 1).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs
from utils.data_io import load_parsed

SERIES_ID = "T511"
SERIES_IDS = ["T511", "T512"]
PRIORITY = 1

BENCHMARKS = {
    "T511": {1948: 0.57, 1967: 0.48, 1989: 0.37},
    "T512": {1948: 0.54, 1967: 0.46, 1989: 0.33},
}


def _validate_benchmarks(sid, series):
    """Check values against known benchmarks.

    Tolerance is 0.05 (NIPA vintage differences account for mid-period deviations).
    """
    bm = BENCHMARKS.get(sid, {})
    issues = []
    for year, expected in bm.items():
        if year in series.index:
            actual = series.loc[year]
            diff = abs(actual - expected)
            if diff > 0.05:
                issues.append(f"{sid}[{year}]: expected {expected}, got {actual:.4f} (diff={diff:.4f})")
            elif diff > 0.02:
                issues.append(f"{sid}[{year}]: NIPA vintage diff {actual:.4f} vs {expected} (within tolerance)")
    return issues


def _extend_t511_via_fte():
    """Extend T511 (Lp/L) using L22 annual FTE data (WP-1 direct).

    Uses NIPA 6.5D FTE by industry, classified by IO framework.
    Growth-rate splice preserves book 1989 level while using NIPA trend.
    """
    fte_path = PARSED_RAW / "annual_productive_employment.csv"
    if fte_path.exists():
        df = pd.read_csv(fte_path, index_col="year")
        if "Lp_L" in df.columns and df["Lp_L"].notna().sum() > 3:
            return df["Lp_L"]
    return None


def _extend_t511_via_io():
    """Fallback: extend T511 using IO productive ratios from P23."""
    io_path = SERIES_OUT / "IO_productive_ratios.csv"
    if not io_path.exists():
        return None
    io = pd.read_csv(io_path, index_col="year")
    if "ratio_productive_employment" in io.columns and io["ratio_productive_employment"].notna().sum() > 3:
        return io["ratio_productive_employment"]
    elif "ratio_productive_output" in io.columns:
        return io["ratio_productive_output"]
    return None


def process():
    """Process labor shares. T511/T512 book + IO-extended (Principle 3)."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # Load extension data sources for T511
    fte_ratio = _extend_t511_via_fte()
    io_ratio = _extend_t511_via_io()

    for sid in SERIES_IDS:
        book_df, _ = load_parsed(sid)
        book_series = book_df["value"] if book_df is not None else pd.Series(dtype=float)

        ext_series = pd.Series(dtype=float)

        if sid == "T511" and 1989 in book_series.index:
            book_1989 = book_series[1989]

            # WP-1: direct FTE from L22 (growth-rate splice at 1989)
            if fte_ratio is not None:
                first_fte = fte_ratio.first_valid_index()
                if first_fte and fte_ratio[first_fte] > 0:
                    # Interpolate 1990 to first FTE year
                    for yr in range(1990, first_fte):
                        frac = (yr - 1989) / (first_fte - 1989)
                        ext_series[yr] = book_1989 * (1 + frac * (fte_ratio[first_fte] / fte_ratio[first_fte] - 1))
                    # Growth-rate splice for FTE years
                    for yr in fte_ratio.index:
                        if yr > 1989:
                            ext_series[yr] = book_1989 * (fte_ratio[yr] / fte_ratio[first_fte])
                    steps.append(f"T511 FTE-extended: {len(ext_series)} years (WP-1 direct from NIPA 6.5D)")
                    print(f"    [P05] T511: FTE-based extension ({len(ext_series)} years)")

            # Fallback: IO ratios from P23
            if len(ext_series) == 0 and io_ratio is not None:
                first_io = io_ratio.index[io_ratio.index > 1989].min() if any(io_ratio.index > 1989) else None
                if first_io and io_ratio[first_io] > 0:
                    for yr in io_ratio.index:
                        if yr > 1989:
                            ext_series[yr] = book_1989 * (io_ratio[yr] / io_ratio[first_io])
                    steps.append(f"T511 IO-extended: {len(ext_series)} years via productive ratio trend")
                    print(f"    [P05] T511: IO-based extension ({len(ext_series)} years)")
        else:
            # Fallback: load pre-spliced extended data
            ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
            if ext_path.exists():
                ext_df = pd.read_csv(ext_path, index_col=0)
                ext_df.index = ext_df.index.astype(int)
                ext_series = ext_df["value"]
                if sid == "T511":
                    steps.append(f"T511 fallback: pre-spliced extended")
                    print(f"    [P05] T511: fallback to pre-spliced (IO ratios not available)")

        # For T512: try IO-classified V*/W from L22 (WP-1), then component approach, then fallback
        if sid == "T512":
            ext_series = pd.Series(dtype=float)

            # WP-1 approach: directly observed V*/W from NIPA 6.2D IO classification
            io_comp_path = PARSED_RAW / "annual_productive_compensation.csv"
            if io_comp_path.exists() and 1989 in book_series.index:
                io_comp = pd.read_csv(io_comp_path, index_col="year")
                if "V_star_W" in io_comp.columns:
                    io_vw = io_comp["V_star_W"]
                    book_1989 = book_series[1989]
                    first_io = io_vw.first_valid_index()
                    if first_io and io_vw[first_io] > 0:
                        # Growth-rate splice: preserve book 1989 level, use IO trend
                        for yr in range(1990, first_io):
                            frac = (yr - 1989) / (first_io - 1989)
                            ext_series[yr] = book_1989 + frac * (book_1989 * (io_vw[first_io] / io_vw[first_io]) - book_1989)
                        for yr in io_vw.index:
                            if yr > 1989:
                                ext_series[yr] = book_1989 * (io_vw[yr] / io_vw[first_io])
                        steps.append(f"T512 IO-classified V*/W: {len(ext_series)} years (WP-1 direct)")
                        print(f"    [P05] T512: IO-classified V*/W ({len(ext_series)} years)")

            # Fallback: component approach (T504/W)
            if len(ext_series) == 0:
                t504_path = SERIES_OUT / "T504.csv"
                nipa_comp_path = Path("D:/Arcanum/Projects/ST2/Inputs/API_Data/BEA/nipa_T20100_compensation_1929_2025.csv")
                if t504_path.exists() and nipa_comp_path.exists():
                    t504 = pd.read_csv(t504_path, index_col=0)
                    v_star = t504["combined"].dropna() if "combined" in t504.columns else pd.Series(dtype=float)
                    w_df = pd.read_csv(nipa_comp_path)
                    if "year" in w_df.columns and "compensation_millions" in w_df.columns:
                        w = w_df.set_index("year")["compensation_millions"] / 1e3
                        w = w[w.index >= 1990]
                        common = v_star.index.intersection(w.index)
                        ext_yrs = common[common > 1989]
                        if len(ext_yrs) > 0:
                            ext_series = v_star[ext_yrs] / w[ext_yrs]
                            steps.append(f"T512 V*/W from components: {len(ext_series)} years")
                            print(f"    [P05] T512: V*/W from components ({len(ext_series)} years)")

            # Last fallback: pre-spliced
            if len(ext_series) == 0:
                ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
                if ext_path.exists():
                    ext_df = pd.read_csv(ext_path, index_col=0)
                    ext_df.index = ext_df.index.astype(int)
                    ext_series = ext_df["value"]
                    print(f"    [P05] T512: fallback to pre-spliced")

        # Build output
        out = pd.DataFrame(index=sorted(set(book_series.index) | set(ext_series.index)))
        out.index.name = "year"
        out["book"] = book_series
        if len(ext_series) > 0:
            out["combined"] = ext_series.reindex(out.index)
            out["combined"] = out["combined"].fillna(out["book"])
        else:
            out["combined"] = out["book"]

        out_path = SERIES_OUT / f"{sid}.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict[sid] = out["combined"].dropna()

        issues = _validate_benchmarks(sid, out["combined"].dropna())
        status_note = "OK" if not issues else f"WARN: {'; '.join(issues)}"

        n_book = book_series.notna().sum()
        n_ext = ext_series.notna().sum()
        steps.append(f"{sid}: {n_book} book + {n_ext} ext rows | {status_note}")
        print(f"    [P05] {sid}: {n_book} book, {n_ext} ext | {status_note}")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }
