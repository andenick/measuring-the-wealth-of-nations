"""P02_S701 -- Productive Labor Coefficient lambda_p (workpackage C rebuild, review 2026-07).

v2.0 (workpackage C): computes on the REBUILT I-O matrix cache
(`data/intermediate/io_matrices_rebuilt/`) and implements the moving-benchmark
extension recommended by P2_FROZEN_WEIGHTS_AUDIT.md. Replaces the v1.1 engine,
which consumed the defective `io_matrices_labeled/` cache (P2 findings: A was
column-share-normalized -> (I-A) near-singular, multipliers ~70x; the derived
"gross output" X was actually total intermediate purchases; the extension froze
the 1977 nominal X denominator forever).

Book methodology (S&T 1994, Ch4 sec 4.1 pp.80-83; Appendix-F-analog filter with
the P2 adjudication corrections: sector 85 unproductive 0.0, sectors 82/83 n/a):

    For each productive sector j with BLS coverage:
        hp_j     = production_workers_j x weekly_hours_j x 52     (hours/year)
        hp*_j    = hp_j / X_j          (X_j = GENUINE gross output, current-$)
        lambda_p = hp* (I - A)^{-1}    (rebuilt Leontief structure)
        S701     = mean_j(lambda_p_j) over covered sectors        (scalar series)

Subseries:
  - S701-A            book period, SIC benchmark years 1958-1977, matrices and
                      X of the SAME benchmark year (S&T's own re-benchmarking
                      practice; no frozen weights).
  - S701-EXT          1990-2024 annual. 1990-96: rebuilt 1977 SIC A (last
                      in-repo SIC benchmark) with X_j updated ANNUALLY from BEA
                      SIC-era GDP-by-industry VA growth; 1997-2024: nearest
                      previous NAICS benchmark L (1997/2002/2007/2012/2017) with
                      annual BEA gross output X and the SIC->NAICS bridge remap.
                      The 1997 SIC->NAICS break is ratio-spliced (documented
                      method change; splice factor in the provenance column).
  - S701-COMBINED     union of -A and -EXT.
  - S701-VAR-FROZEN77 registered variant: the OLD frozen-1977-weights method
                      (A and X both frozen at the rebuilt 1977 benchmark),
                      1990-2024 -- retained per P2 recommendation for
                      comparability with v1.x. NOT the published extension.

Outputs: data/intermediate/S701.csv + data/final/S701.csv
Units: hr_per_dollar (hours per CURRENT-year nominal dollar of gross output).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_RAW  # noqa: E402
from utils import io_rebuilt as ior  # noqa: E402


SERIES_ID = "S701"
SUB_BOOK = "S701-A"
SUB_EXT = "S701-EXT"
SUB_COMBINED = "S701-COMBINED"
SUB_FROZEN = "S701-VAR-FROZEN77"

BOOK_PERIOD = (1948, 1989)
EXT_PERIOD = (1990, 2024)

L01_OUTPUT = DATA_RAW / "ch07" / "L01_S701_output.csv"


def _load_panel() -> pd.DataFrame:
    if not L01_OUTPUT.exists():
        raise FileNotFoundError(f"L01_S701 output missing: {L01_OUTPUT}")
    return pd.read_csv(L01_OUTPUT)




def _scalar_sic(panel: pd.DataFrame, hours_year: int, matrix_year: int,
                X: pd.Series | None = None) -> tuple[Optional[float], int]:
    """SIC-path scalar: supersector hours split to io-85 grain by X share.
    Hours come from the N1 at-rest-rebuilt L01 panel (employment allocated so
    member rows sum to the true supersector total; correct dt07 weekly hours) --
    the former compute-time shims are gone (see utils.io_rebuilt docstrings)."""
    _, _, Xb = ior.load_sic(matrix_year)
    X_use = Xb if X is None else X
    hours = ior.hours_io85(panel, hours_year, X_use)
    if hours.empty:
        return None, 0
    lam, _, covered = ior.lambda_vector_sic(hours, matrix_year, X_musd=X_use)
    if len(covered) == 0:
        return None, 0
    return float(lam.loc[covered].mean()), len(covered)


def _scalar_naics(panel: pd.DataFrame, benchmark: int, year: int) -> tuple[Optional[float], int]:
    _, L = ior.load_naics(benchmark)
    Xn = ior.naics_X_annual(year)
    Xn = Xn[Xn.index.isin(L.columns)]
    h_naics = ior.hours_naics(panel, year, Xn)
    if h_naics.empty:
        return None, 0
    lam, _, covered = ior.lambda_vector_naics(h_naics, benchmark, year)
    if len(covered) == 0:
        return None, 0
    return float(lam.loc[covered].mean()), len(covered)


def compute_book_subseries(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for yr in ior.SIC_BENCHMARKS:
        if yr < BOOK_PERIOD[0] or yr > BOOK_PERIOD[1]:
            continue
        val, n = _scalar_sic(panel, yr, yr)
        rows.append({
            "series_id": SUB_BOOK, "year": yr,
            "value": val if val is not None else float("nan"),
            "units": "hr_per_dollar", "stage": "benchmark_book_sic_rebuilt",
            "provenance": (f"hp*=BLS_hours/X_j_rebuilt_gross_output; lambda_p=hp*x(I-A)^-1_rebuilt; "
                           f"matrix_year={yr}; n_covered_prod_sectors={n}; cache=io_matrices_rebuilt"),
        })
    return pd.DataFrame(rows)


def _splice_factor(panel: pd.DataFrame) -> tuple[float, dict]:
    """1997 both-ways overlap: SIC-path / NAICS-path."""
    v_sic, n_s = _scalar_sic(panel, 1997, 1977, X=ior.sic_X_annual(1997))
    v_naics, n_n = _scalar_naics(panel, 1997, 1997)
    if v_sic is None or v_naics is None or v_naics == 0:
        raise RuntimeError("cannot compute 1997 splice factor")
    return v_sic / v_naics, {"sic_path_1997": v_sic, "naics_path_1997": v_naics,
                             "n_sic": n_s, "n_naics": n_n}


def compute_extension_subseries(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    factor, splice_info = _splice_factor(panel)
    rows = []
    for yr in range(EXT_PERIOD[0], EXT_PERIOD[1] + 1):
        if yr <= 1996:
            val, n = _scalar_sic(panel, yr, 1977, X=ior.sic_X_annual(yr))
            if val is None:
                continue
            prov = (f"SIC_path: A=1977_rebuilt, X_j=annual_nominal(BEA_SIC_workbook_VA_growth); "
                    f"n={n}; moving_denominator")
        else:
            bench = ior.naics_benchmark_for(yr)
            raw, n = _scalar_naics(panel, bench, yr)
            if raw is None:
                continue
            val = raw * factor
            prov = (f"NAICS_path: L=BEA_TotalRequirements_{bench}, X=annual_BEA_gross_output({yr}); "
                    f"n={n}; ratio_spliced_at_1997 factor={factor:.6f} "
                    f"(sic_1997={splice_info['sic_path_1997']:.6f}/naics_1997={splice_info['naics_path_1997']:.6f}); "
                    f"unspliced={raw:.6f}")
        rows.append({
            "series_id": SUB_EXT, "year": yr, "value": val,
            "units": "hr_per_dollar", "stage": "extension_moving_benchmark",
            "provenance": prov,
        })
    return pd.DataFrame(rows), {"factor": factor, **splice_info}


def compute_frozen_variant(panel: pd.DataFrame) -> pd.DataFrame:
    """S701-VAR-FROZEN77: A and nominal X both frozen at the rebuilt 1977 benchmark."""
    rows = []
    for yr in range(EXT_PERIOD[0], EXT_PERIOD[1] + 1):
        val, n = _scalar_sic(panel, yr, 1977)   # X defaults to the 1977 benchmark X
        if val is None:
            continue
        rows.append({
            "series_id": SUB_FROZEN, "year": yr, "value": val,
            "units": "hr_per_dollar", "stage": "variant_frozen_1977_weights",
            "provenance": (f"VARIANT (not the published extension): A+X frozen at rebuilt 1977; "
                           f"n={n}; retains the v1.x IO-aging assumption for comparability "
                           f"(P2_FROZEN_WEIGHTS_AUDIT quantifies its bias)"),
        })
    return pd.DataFrame(rows)


def compute() -> pd.DataFrame:
    panel = _load_panel()
    book = compute_book_subseries(panel)
    ext, splice_info = compute_extension_subseries(panel)
    frozen = compute_frozen_variant(panel)
    combined = pd.concat([book.assign(series_id=SUB_COMBINED),
                          ext.assign(series_id=SUB_COMBINED)],
                         ignore_index=True).sort_values("year").reset_index(drop=True)
    out = pd.concat([book, ext, combined, frozen], ignore_index=True)
    out.attrs["splice_info"] = splice_info
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


PUBLISHED_SIG_FIGS = 3  # honest display precision for lambda (DIV-042; see F3, 2026-07-07)


def _round_sig(x: object, sig: int = PUBLISHED_SIG_FIGS) -> object:
    """Round to `sig` significant figures; pass through NaN/None/non-finite/zero.

    DIV-042 (F3 lambda-sensitivity, 2026-07-07): the recovered per-sector gross
    output X_j carries a ~+/-11.5% bound, so published lambda aggregates are honest
    only to ~+/-3-9% (MC) / +/-11.65% (worst-case). The historical 15-17 significant
    figures were false precision. Rounding is applied ONLY at the final/published
    emit stage; the data/intermediate CSV retains full float64 precision for
    regression/reproducibility, and the honest uncertainty is stated explicitly in
    the data/final/S701_LAMBDA_BAND.csv sidecar. See docs/series/S701_DPR.md
    "Precision & uncertainty (DIV-042)".
    """
    if x is None:
        return x
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return x
    if not math.isfinite(xf) or xf == 0.0:
        return xf
    return round(xf, -int(math.floor(math.log10(abs(xf)))) + (sig - 1))


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")   # full precision (regression/reproducibility)
    df_pub = df.copy()
    df_pub["value"] = df_pub["value"].map(_round_sig)        # honest published precision (DIV-042 / F3)
    final_path = write_series_csv(df_pub, SERIES_ID, stage="final")
    for sid in [SUB_BOOK, SUB_EXT, SUB_FROZEN]:
        sub = df[df["series_id"] == sid].dropna(subset=["value"])
        if len(sub):
            print(f"    [P02_S701] {sid}: {len(sub)} values, "
                  f"range=[{sub['value'].min():.4f}, {sub['value'].max():.4f}] hr/$")
    print(f"    [P02_S701] wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
