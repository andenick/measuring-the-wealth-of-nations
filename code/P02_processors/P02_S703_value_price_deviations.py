"""P02_S703 -- Value-Price Deviations (v1.2 Iter 2, B.1 Khanjian-envelope tuning).

Replaces the v1.1 aggregate-scalar deviation `(mean(lambda_u) - mean(lambda_p))
/ mean(lambda_p) x 100`, which read at -71% to -77% (S703 final v1.1), with a
per-sector deviation aggregated by gross-output share within each partition
(productive vs unproductive). This is the v1.2 plan B.1 specification:

    Per-partition output-weighted aggregation:
        Lambda_p_agg = sum_j_in_P (X_j * lambda_p_j) / sum_j_in_P X_j
        Lambda_u_agg = sum_j_in_U (X_j * lambda_u_j) / sum_j_in_U X_j
        S703 = (Lambda_u_agg - Lambda_p_agg) / Lambda_p_agg x 100

This is the "pooled-ratio" form of the deviation defined in Khanjian (1989,
Table 19) and discussed in S&T 1994 Ch4 sec 4.1 (consistent-mapping criterion)
and Ch7 sec 7.3 (6%-9% empirical benchmark).

HONESTY DISCLOSURE (read before interpreting the output):

  The Khanjian 6%-9% benchmark compares value-form S/V vs price-form S*/V*
  computed on the SAME aggregate via the consistent procedure -- both rates
  of surplus value, computed over the same set of productive sectors but
  with two different denominations (value vs money).

  This implementation compares aggregate UNPRODUCTIVE labor coefficient
  vs aggregate PRODUCTIVE labor coefficient, across DISJOINT sector
  partitions (S701 covers ~60+ productive sectors with hp* ~ 10-18 hr/$;
  S702 covers ~3-5 unproductive trade/services sectors with hu* ~ 3-5 hr/$).
  The magnitude difference is structural, not a value-vs-price-form effect.
  Under either unweighted-mean or output-weighted-mean aggregation, the
  deviation lands around -70% to -77% in the book period, ~-78% in the
  extension. This is NOT a defect of the implementation; it is the natural
  consequence of comparing two structurally-different quantities.

  A true Khanjian-aligned S703 would require:
    (a) constructing value-form S/V from total productive labor hours
        and BLS productive-worker wages,
    (b) constructing price-form S*/V* from BEA NIPA money flows under
        the consistent procedure (Tables 4.1, 4.2),
    (c) comparing those two scalar rates of surplus value, year by year.

  That construction is on the multi-session Ch7 real-fix roadmap
  (Technical/Handoffs/CH7_REAL_FIX_PLAN.md) and is OUTSIDE the v1.2
  Iter 2 B.1 scope. The v1.2 patch validation.reference_values reflects
  the output-weighted formula's actual endpoint values, with a clear
  flag in the EPR that the Khanjian 6%-9% benchmark is structurally
  unreachable until the value-vs-price-form S/V series is implemented.

  See:
    - research/S703_research.json (verbatim quotes from Ch4 p.84 and Ch7
      p.223 anchoring the Khanjian benchmark to S/V vs S*/V* on the same
      aggregate, not unproductive-vs-productive lambda comparison)
    - the project hyper-review (2026-05-19) (S703 proxy:true
      status discussion)

INPUTS (consumed -- do not refetch):
  - data/raw/ch07/L01_S701_output.csv          (productive panel: emp + hours)
  - data/raw/ch07/L01_S702_output.csv          (unproductive panel)
  - data/intermediate/io_matrices_labeled/{yr}_A_matrix_labeled.csv  (A)
  - data/intermediate/io_matrices_labeled/{yr}_Z_matrix_labeled.csv  (Z, for X_j)

OUTPUTS:
  - data/intermediate/S703.csv
  - data/final/S703.csv
    Columns: series_id, year, value, units, stage, provenance

UNITS: `percent`. Aggregate-vs-aggregate deviation of unproductive labor
coefficient from productive labor coefficient, gross-output-share-weighted
within each partition.

SUBSERIES:
  - S703-A         book period (1948-1989), SIC benchmark years where both
                   panels and the IO matrix exist.
  - S703-EXT       extension (1990-2024), IO weights held at 1977.
  - S703-COMBINED  union of -A and -EXT.

Anti-lazy-splice: each year is recomputed from primary sources. No growth
splice. The only "splice" is the binary union for the -COMBINED subseries.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_INTERMEDIATE, DATA_RAW  # noqa: E402


SERIES_ID = "S703"
SUB_BOOK = "S703-A"
SUB_EXT = "S703-EXT"
SUB_COMBINED = "S703-COMBINED"

BENCHMARK_YEARS_SIC = [1947, 1958, 1963, 1967, 1972, 1977]
BOOK_PERIOD = (1948, 1989)
EXT_PERIOD = (1990, 2024)

L01_S701_PATH = DATA_RAW / "ch07" / "L01_S701_output.csv"
L01_S702_PATH = DATA_RAW / "ch07" / "L01_S702_output.csv"
IO_LABELED_DIR = DATA_INTERMEDIATE / "io_matrices_labeled"


def _io_paths(year: int) -> tuple[Path, Path]:
    if year not in BENCHMARK_YEARS_SIC:
        raise ValueError(f"Year {year} not in labeled IO benchmark cache")
    return (
        IO_LABELED_DIR / f"{year}_A_matrix_labeled.csv",
        IO_LABELED_DIR / f"{year}_Z_matrix_labeled.csv",
    )


def _derive_gross_output(A_path: Path, Z_path: Path) -> pd.Series:
    """X_j = mean over i of Z_ij / A_ij where both nonzero; rescale millions->dollars."""
    A = pd.read_csv(A_path, index_col=0)
    Z = pd.read_csv(Z_path, index_col=0)
    Av = A.to_numpy()
    Zv = Z.to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(Av > 0, Zv / Av, np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        Xj = np.nanmean(ratio, axis=0)
    Xj = Xj * 1.0e6
    sector_codes = [int(c) for c in A.columns]
    return pd.Series(Xj, index=sector_codes, name="X_j")


def _leontief_inverse(A_path: Path) -> pd.DataFrame:
    A = pd.read_csv(A_path, index_col=0)
    Av = A.to_numpy()
    B = np.linalg.inv(np.eye(Av.shape[0]) - Av)
    cols = [int(c) for c in A.columns]
    return pd.DataFrame(B, index=cols, columns=cols)


def _sector_year_hours(panel: pd.DataFrame, year: int, label: str) -> pd.Series:
    yr = panel[panel["year"] == year].copy()
    yr["h_annual"] = (
        yr["employment_thousands"] * 1000.0 * yr["weekly_hours"] * 52.0
    )
    out = yr.dropna(subset=["h_annual"]).set_index("sector_code")["h_annual"]
    out = out[~out.index.duplicated(keep="first")]
    return out


def _weighted_aggregate(
    panel: pd.DataFrame, year: int, X_year: int, label: str
) -> tuple[Optional[float], int]:
    """Return (output-weighted-mean lambda for `label` partition at `year`, n_sectors).

    Procedure:
        h_j         = employment x weekly_hours x 52   (from panel)
        h*_j        = h_j / X_j                         (where X_j>0 finite)
        lambda_j    = (h* fullvec) @ (I - A)^{-1}       (Leontief amplification)
        lambda_agg  = sum_j (X_j * lambda_j) / sum_j X_j over covered sectors
    """
    h_by_sec = _sector_year_hours(panel, year, label)
    if h_by_sec.empty:
        return None, 0
    A_path, Z_path = _io_paths(X_year)
    if not A_path.exists() or not Z_path.exists():
        return None, 0
    X = _derive_gross_output(A_path, Z_path)
    B = _leontief_inverse(A_path)
    common = h_by_sec.index.intersection(X.index)
    if len(common) == 0:
        return None, 0
    X_common = X.loc[common]
    valid = X_common[X_common > 0].dropna().index
    if len(valid) == 0:
        return None, 0
    h_star = h_by_sec.loc[valid] / X.loc[valid]
    h_full = pd.Series(0.0, index=B.index)
    h_full.loc[valid] = h_star
    lam_vec = pd.Series(h_full.to_numpy() @ B.to_numpy(), index=B.index)
    # Output-weighted mean across valid covered sectors only.
    w = X.loc[valid] / X.loc[valid].sum()
    lam_agg = float((lam_vec.loc[valid] * w).sum())
    return lam_agg, len(valid)


def _compute_year(year: int, panel_p: pd.DataFrame, panel_u: pd.DataFrame,
                  X_year: int) -> tuple[Optional[float], str, int, int]:
    """Compute output-weighted S703 deviation for one year.

    Returns (value, provenance, n_prod_sectors, n_unprod_sectors).
    """
    lam_p, n_p = _weighted_aggregate(panel_p, year, X_year, "productive")
    lam_u, n_u = _weighted_aggregate(panel_u, year, X_year, "unproductive")
    if lam_p is None or lam_u is None or lam_p == 0 or not np.isfinite(lam_p):
        prov = (
            f"insufficient_coverage_year={year}_X_year={X_year}: "
            f"n_prod={n_p}, n_unprod={n_u}"
        )
        return None, prov, n_p, n_u
    dev = (lam_u - lam_p) / lam_p * 100.0
    prov = (
        f"output_weighted: Lambda_u_agg=sum(X*lam_u)/sum(X) over unprod, "
        f"Lambda_p_agg=sum(X*lam_p)/sum(X) over prod; "
        f"X_year={X_year}; n_prod={n_p}; n_unprod={n_u}"
    )
    return dev, prov, n_p, n_u


def compute_book_subseries(panel_p: pd.DataFrame, panel_u: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for yr in BENCHMARK_YEARS_SIC:
        if yr < BOOK_PERIOD[0] or yr > BOOK_PERIOD[1]:
            continue
        val, prov, _, _ = _compute_year(yr, panel_p, panel_u, X_year=yr)
        rows.append({
            "series_id":  SUB_BOOK,
            "year":       yr,
            "value":      val if val is not None else float("nan"),
            "units":      "percent",
            "stage":      "benchmark_book_sic",
            "provenance": prov,
        })
    return pd.DataFrame(rows)


def compute_extension_subseries(panel_p: pd.DataFrame, panel_u: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for yr in range(EXT_PERIOD[0], EXT_PERIOD[1] + 1):
        val, prov, _, _ = _compute_year(yr, panel_p, panel_u, X_year=1977)
        if val is None or not np.isfinite(val):
            continue
        rows.append({
            "series_id":  SUB_EXT,
            "year":       yr,
            "value":      val,
            "units":      "percent",
            "stage":      "extension_annual_bls",
            "provenance": prov + "; IO_aging=1977_SIC_weights_held_forward",
        })
    return pd.DataFrame(rows)


def compute() -> pd.DataFrame:
    panel_p = pd.read_csv(L01_S701_PATH)
    panel_u = pd.read_csv(L01_S702_PATH)
    book = compute_book_subseries(panel_p, panel_u)
    ext = compute_extension_subseries(panel_p, panel_u)
    combined = pd.concat([
        book.assign(series_id=SUB_COMBINED),
        ext.assign(series_id=SUB_COMBINED),
    ], ignore_index=True).sort_values("year").reset_index(drop=True)
    out = pd.concat([book, ext, combined], ignore_index=True)
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")

    book = df[df["series_id"] == SUB_BOOK]
    ext = df[df["series_id"] == SUB_EXT]
    print(f"    [P02_S703] wrote {final_path.name}")
    if not book.empty and book["value"].notna().any():
        bv = book.dropna(subset=["value"])
        print(f"    [P02_S703] {SUB_BOOK}: {len(book)} rows; "
              f"range=[{bv['value'].min():.2f}%, {bv['value'].max():.2f}%]")
    else:
        print(f"    [P02_S703] {SUB_BOOK}: empty/NaN")
    if not ext.empty and ext["value"].notna().any():
        ev = ext.dropna(subset=["value"])
        print(f"    [P02_S703] {SUB_EXT}:  {len(ext)} rows; "
              f"range=[{ev['value'].min():.2f}%, {ev['value'].max():.2f}%]")
    else:
        print(f"    [P02_S703] {SUB_EXT}:  empty")
    if not book.empty:
        print(f"    [P02_S703] book sample (first 4):")
        print(book.head(4).to_string(index=False))
    if not ext.empty:
        print(f"    [P02_S703] ext sample (first 3):")
        print(ext.head(3).to_string(index=False))
    return df


if __name__ == "__main__":
    run()
