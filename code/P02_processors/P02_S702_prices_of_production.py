"""P02_S702 -- Unproductive Labor Coefficient lambda_u (workpackage C rebuild, review 2026-07).

v2.0 (workpackage C): computes on the REBUILT I-O matrix cache and the moving-benchmark
extension, mirroring P02_S701 exactly (procedure consistency is what makes the
S703 partition-gap diagnostic interpretable). See P02_S701 module docstring for
the full method + the P2 findings that retired the v1.1 engine.

Registry/name note: the series retains its historical registry name "Prices of
Production", but what it computes (since v1.1, unchanged here in concept) is
the UNPRODUCTIVE labor coefficient lambda_u -- the symmetric sister of S701's
lambda_p, built from the unproductive partition of the BLS CES panel
(io-85 sectors 69 wholesale, 70 retail, 71 finance+insurance, 72 real estate,
74 business services). P2 Appendix-F adjudication corrections applied: io-85
82/83 are special IO columns (n/a, not labor-bearing -- they carry no BLS data
and are now EXPLICITLY excluded, not just accidentally NaN); io-85 85 general
government is unproductive per the book but carries no CES coverage in the L01
panel, so it does not enter (honest-missing, not fabricated).

Subseries: S702-A (book SIC benchmarks), S702-EXT (1990-2024 moving benchmark,
ratio-spliced at the 1997 SIC->NAICS break), S702-COMBINED, S702-VAR-FROZEN77
(the old frozen-1977-weights method as a registered variant).

Units: hours_per_dollar (hours per current-year nominal dollar of gross output).
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


SERIES_ID = "S702"
SUB_BOOK = "S702-A"
SUB_EXT = "S702-EXT"
SUB_COMBINED = "S702-COMBINED"
SUB_FROZEN = "S702-VAR-FROZEN77"

BOOK_PERIOD = (1948, 1989)
EXT_PERIOD = (1990, 2024)

L01_OUTPUT = DATA_RAW / "ch07" / "L01_S702_output.csv"

# P2 Appendix-F adjudication: 82 (business travel) and 83 (office supplies) are
# special IO intermediate-use columns, not labor-bearing sectors -> n/a.
EXCLUDED_NA_SECTORS = {82, 83}


def _load_panel() -> pd.DataFrame:
    if not L01_OUTPUT.exists():
        raise FileNotFoundError(f"L01_S702 output missing: {L01_OUTPUT}")
    df = pd.read_csv(L01_OUTPUT)
    return df[~df["sector_code"].isin(EXCLUDED_NA_SECTORS)].copy()




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
            "units": "hours_per_dollar", "stage": "benchmark_book_sic_rebuilt",
            "provenance": (f"hu*=BLS_hours/X_j_rebuilt_gross_output; lambda_u=hu*x(I-A)^-1_rebuilt; "
                           f"matrix_year={yr}; n_covered_unprod_sectors={n}; cache=io_matrices_rebuilt"
                           if val is not None else f"no_BLS_unproductive_coverage_for_{yr} (NOT fabricated)"),
        })
    return pd.DataFrame(rows)


def _splice_factor(panel: pd.DataFrame) -> tuple[float, dict]:
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
            "units": "hours_per_dollar", "stage": "extension_moving_benchmark",
            "provenance": prov,
        })
    return pd.DataFrame(rows), {"factor": factor, **splice_info}


def compute_frozen_variant(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for yr in range(EXT_PERIOD[0], EXT_PERIOD[1] + 1):
        val, n = _scalar_sic(panel, yr, 1977)
        if val is None:
            continue
        rows.append({
            "series_id": SUB_FROZEN, "year": yr, "value": val,
            "units": "hours_per_dollar", "stage": "variant_frozen_1977_weights",
            "provenance": (f"VARIANT (not the published extension): A+X frozen at rebuilt 1977; "
                           f"n={n}; retains the v1.x IO-aging assumption for comparability"),
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

    DIV-042 (F3 lambda-sensitivity, 2026-07-07): recovered per-sector gross output
    X_j carries a ~+/-11.5% bound, so published lambda_u aggregates are honest only
    to ~+/-6-9% (MC) / +/-11.65% (worst-case). The historical 15-17 significant
    figures were false precision. Rounding is applied ONLY at the final/published
    emit stage; data/intermediate retains full float64 precision, and the honest
    uncertainty is stated in data/final/S702_LAMBDA_BAND.csv. See
    docs/series/S702_DPR.md "Precision & uncertainty (DIV-042)".
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
            print(f"    [P02_S702] {sid}: {len(sub)} values, "
                  f"range=[{sub['value'].min():.4f}, {sub['value'].max():.4f}] hr/$")
    print(f"    [P02_S702] wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
