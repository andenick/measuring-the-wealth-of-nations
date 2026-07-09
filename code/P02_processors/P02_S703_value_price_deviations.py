"""P02_S703 -- Productive/Unproductive Labor-Coefficient Partition Gap (workpackage C v2.0).

HONEST RELABEL (workpackage C review 2026-07). What this series measures:

    S703 = (Lambda_u_agg - Lambda_p_agg) / Lambda_p_agg x 100   [percent]

    Lambda_p_agg = gross-output-weighted mean of lambda_p over the covered
                   PRODUCTIVE partition (S701 machinery);
    Lambda_u_agg = same over the covered UNPRODUCTIVE partition (S702 machinery).

It is the aggregate gap between the unproductive and productive partitions'
embodied-labor-per-dollar coefficients. It is NOT the book's Khanjian
value-price deviation: ST 1994 Ch7 sec 7.3 (folio 223) cites Khanjian (1989)
that the VALUE-form and PRICE-form rates of surplus value (S/V vs S*/V*),
computed on the SAME aggregate under the consistent procedure, differ by only
6%-9%. That comparison requires the full value-form S/V construction (lambda
applied to the NIPA flow decomposition of Ch4 Tables 4.1/4.2, incl. the
royalties recirculation) which is NOT implemented in this repo; the sector-level
NIPA flow decomposition needed for it is not among the inputs. Registered as a
divergence (see WP-C_DIV_PATCHES.json); the Khanjian 6%-9% band must NEVER be
used as a validator anchor for this series.

v2.0 changes vs v1.2:
  - computed on the REBUILT matrix cache (io_matrices_rebuilt/; sane Leontief
    multipliers ~2 instead of the defective ~70x -- see WP-C_MATRIX_REBUILD.md);
  - moving-benchmark extension identical to S701/S702 (1990-96 SIC path with
    annual X; 1997+ NAICS benchmark step-function with annual X);
  - the 1997 SIC->NAICS break is NOT ratio-spliced here: the deviation is a
    scale-free ratio, so common-mode method effects largely cancel; both 1997
    values are recorded in the provenance instead.
  - P2 Appendix-F corrections applied (82/83 excluded as n/a).

Units: percent. On the rebuilt matrices the gap is much smaller than the
defective-cache -66..-81% and varies in sign (computed: book benchmarks
-65% (1967) -> -18% (1977); extension roughly -23%..+15%): with genuine
gross-output denominators, the covered unproductive sectors (esp. retail) are
not uniformly less labor-intensive per dollar than the productive average.
The partition gap itself is the series' subject; its 1997 overlap values under
both methods are recorded in the provenance (method-sensitive, unspliced).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_RAW  # noqa: E402
from utils import io_rebuilt as ior  # noqa: E402


SERIES_ID = "S703"
SUB_BOOK = "S703-A"
SUB_EXT = "S703-EXT"
SUB_COMBINED = "S703-COMBINED"

BOOK_PERIOD = (1948, 1989)
EXT_PERIOD = (1990, 2024)

L01_S701_PATH = DATA_RAW / "ch07" / "L01_S701_output.csv"
L01_S702_PATH = DATA_RAW / "ch07" / "L01_S702_output.csv"
EXCLUDED_NA_SECTORS = {82, 83}          # P2 Appendix-F adjudication: n/a columns


def _agg_sic(panel: pd.DataFrame, year: int, matrix_year: int,
             X: pd.Series | None = None) -> tuple[Optional[float], int]:
    """Gross-output-weighted mean lambda over the covered partition (SIC path).

    Uses the N1 at-rest-rebuilt L01 panel (supersector employment allocated to
    io-85 members summing to the true total; correct dt07 weekly hours), split
    to matrix grain by X share -- the former compute-time shims are gone
    (see utils.io_rebuilt).
    """
    _, _, Xb = ior.load_sic(matrix_year)
    X_use = Xb if X is None else X
    hours = ior.hours_io85(panel, year, X_use)
    if hours.empty:
        return None, 0
    lam, Xu, covered = ior.lambda_vector_sic(hours, matrix_year, X_musd=X_use)
    if len(covered) == 0:
        return None, 0
    w = Xu.loc[covered] / Xu.loc[covered].sum()
    return float((lam.loc[covered] * w).sum()), len(covered)


def _agg_naics(panel: pd.DataFrame, year: int, benchmark: int) -> tuple[Optional[float], int]:
    _, L = ior.load_naics(benchmark)
    Xn = ior.naics_X_annual(year)
    Xn = Xn[Xn.index.isin(L.columns)]
    hours = ior.hours_naics(panel, year, Xn)
    if hours.empty:
        return None, 0
    lam, Xu, covered = ior.lambda_vector_naics(hours, benchmark, year)
    if len(covered) == 0:
        return None, 0
    w = Xu.loc[covered] / Xu.loc[covered].sum()
    return float((lam.loc[covered] * w).sum()), len(covered)


def _dev(lam_u: Optional[float], lam_p: Optional[float]) -> Optional[float]:
    if lam_u is None or lam_p is None or lam_p == 0 or not np.isfinite(lam_p):
        return None
    return (lam_u - lam_p) / lam_p * 100.0


def compute() -> pd.DataFrame:
    panel_p = pd.read_csv(L01_S701_PATH)
    panel_u = pd.read_csv(L01_S702_PATH)
    panel_u = panel_u[~panel_u["sector_code"].isin(EXCLUDED_NA_SECTORS)].copy()

    rows = []
    # ---- book benchmarks
    for yr in ior.SIC_BENCHMARKS:
        if yr < BOOK_PERIOD[0] or yr > BOOK_PERIOD[1]:
            continue
        lp, n_p = _agg_sic(panel_p, yr, yr)
        lu, n_u = _agg_sic(panel_u, yr, yr)
        val = _dev(lu, lp)
        rows.append({
            "series_id": SUB_BOOK, "year": yr,
            "value": val if val is not None else float("nan"),
            "units": "percent", "stage": "benchmark_book_sic_rebuilt",
            "provenance": (f"partition_gap output-weighted; matrix_year={yr}; "
                           f"n_prod={n_p}; n_unprod={n_u}; cache=io_matrices_rebuilt"
                           if val is not None else
                           f"insufficient_unproductive_coverage_{yr} (NOT fabricated)"),
        })

    # ---- 1997 both-ways (documented method-change overlap, no splice)
    lp97s, _ = _agg_sic(panel_p, 1997, 1977, X=ior.sic_X_annual(1997))
    lu97s, _ = _agg_sic(panel_u, 1997, 1977, X=ior.sic_X_annual(1997))
    lp97n, _ = _agg_naics(panel_p, 1997, 1997)
    lu97n, _ = _agg_naics(panel_u, 1997, 1997)
    both_ways = (f"1997_overlap: sic_path_dev={_dev(lu97s, lp97s):.4f}pct, "
                 f"naics_path_dev={_dev(lu97n, lp97n):.4f}pct")

    # ---- extension
    for yr in range(EXT_PERIOD[0], EXT_PERIOD[1] + 1):
        if yr <= 1996:
            X = ior.sic_X_annual(yr)
            lp, n_p = _agg_sic(panel_p, yr, 1977, X=X)
            lu, n_u = _agg_sic(panel_u, yr, 1977, X=X)
            method = "SIC_path A=1977_rebuilt X=annual"
        else:
            bench = ior.naics_benchmark_for(yr)
            lp, n_p = _agg_naics(panel_p, yr, bench)
            lu, n_u = _agg_naics(panel_u, yr, bench)
            method = f"NAICS_path L={bench} X=annual"
        val = _dev(lu, lp)
        if val is None or not np.isfinite(val):
            continue
        rows.append({
            "series_id": SUB_EXT, "year": yr, "value": val,
            "units": "percent", "stage": "extension_moving_benchmark",
            "provenance": (f"partition_gap output-weighted; {method}; n_prod={n_p}; "
                           f"n_unprod={n_u}; scale_free_no_splice; {both_ways}"),
        })

    df = pd.DataFrame(rows)
    book = df[df["series_id"] == SUB_BOOK]
    ext = df[df["series_id"] == SUB_EXT]
    combined = pd.concat([book.assign(series_id=SUB_COMBINED),
                          ext.assign(series_id=SUB_COMBINED)],
                         ignore_index=True).sort_values("year").reset_index(drop=True)
    out = pd.concat([book, ext, combined], ignore_index=True)
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    for sid in [SUB_BOOK, SUB_EXT]:
        sub = df[df["series_id"] == sid].dropna(subset=["value"])
        if len(sub):
            print(f"    [P02_S703] {sid}: {len(sub)} values, "
                  f"range=[{sub['value'].min():.2f}%, {sub['value'].max():.2f}%]")
    print(f"    [P02_S703] wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()
