"""P02_S701 -- Productive Labor Coefficient lambda_p (Ch7 real-fix, v1.1 Phase 5).

Computes the productive sector labor coefficient using the SAME per-sector
procedure as P02_S702 (its unproductive sister). Procedure consistency is
essential because S703 = (lambda_u - lambda_p)/lambda_p must compare two
quantities computed identically; the Khanjian 6-9% deviation benchmark only
makes sense when both sides come from a single consistent estimator.

Book methodology (S&T 1994, Ch4 sec 4.1 pp.80-83; Appendix F filter):

    For each productive sector j (productive_share > 0.5 per Appendix F):
        hp_j      = production_workers_j x weekly_hours_j x 52   (hours/year)
        X_j       = gross output of sector j (producer prices, derived from
                    labeled BEA IO Z_ij / A_ij = X_j elementwise)
        hp*_j     = hp_j / X_j                                   (hr/$)
        lambda_p  = hp* (I - app*)^{-1}                          (Leontief, sector vector)
        S701-A    = mean_j(lambda_p_j) across covered sectors    (scalar published series)

Inputs (consumed -- do not refetch):
  - L01_S701 panel:  data/raw/ch07/L01_S701_output.csv (BLS CES emp + hours,
    long format, sector x year, productive sectors per Appendix F, 1948-2024).
    Has full coverage 1972+ for ~69 productive sectors (mining, construction,
    durable + nondurable manufacturing, etc.).
  - Labeled BEA IO matrices: data/intermediate/io_matrices_labeled/
    {yr}_A_matrix_labeled.csv + {yr}_Z_matrix_labeled.csv. Sector codes are
    integer (1..85) matching Appendix F sector_code. X_j derived from Zj/Aij
    elementwise (where both nonzero) -- equivalent to Z column sum given the
    A-col-sum=1 normalization in this cache.

Subseries:
  - S701-A         book period (1948-1989), benchmark-year scalars at SIC
                   benchmarks (1947, 1958, 1963, 1967, 1972, 1977) where
                   BLS CES coverage AND IO matrix both exist; inter-benchmark
                   years interpolated for chopped output to keep a dense panel.
  - S701-EXT       extension period (1990-2024), annual where BLS CES
                   coverage exists. IO matrix weights held at the most-
                   recent applicable SIC benchmark (1977) per the same
                   IO-aging assumption documented in S702 EPR.
  - S701-COMBINED  union of -A and -EXT.

Outputs:
  - data/intermediate/S701.csv
  - data/final/S701.csv
    Columns: series_id, year, value, units, stage, provenance

Units: `hr_per_dollar` (hr/$). Real Ch7 magnitudes via Leontief amplification
on the consistent-procedure estimator: same order as lambda_u (hours per
dollar of sector output, post Leontief embodied-labor calculation).

Methodology distinction from prior implementations:
  - v1.0 proxy: mean(column_sum((I-A)^-1)) -- a dimensionless matrix-structure
    index, no labor content.
  - v1.1 iter4: super-sector fallback (mining+construction+manufacturing
    aggregated to 3 super-sectors); scalar hp* per year; uniform Leontief
    amplification factor. Mixed-procedure with S702 -> S703 unintelligible.
  - v1.1 iter5 (this file): full per-sector L01_S701 panel; per-sector
    hp*_j = hours_j/X_j; full Leontief multiplication; mean across covered
    sectors. Procedurally identical to P02_S702 -> S703 deviation interpretable.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_INTERMEDIATE, DATA_FINAL, DATA_RAW  # noqa: E402


SERIES_ID = "S701"
SUB_BOOK = "S701-A"
SUB_EXT = "S701-EXT"
SUB_COMBINED = "S701-COMBINED"

# Benchmark IO years available in the labeled SIC cache.
BENCHMARK_YEARS_SIC = [1947, 1958, 1963, 1967, 1972, 1977]
BENCHMARK_YEARS_NAICS = [1997, 2002, 2007, 2012]

# Period definitions per task spec.
BOOK_PERIOD = (1948, 1989)
EXT_PERIOD = (1990, 2024)

# Input paths.
L01_OUTPUT = DATA_RAW / "ch07" / "L01_S701_output.csv"
IO_LABELED_DIR = DATA_INTERMEDIATE / "io_matrices_labeled"


def _io_paths(year: int) -> tuple[Path, Path]:
    """Return (A_path, Z_path) for a benchmark year, SIC era only."""
    if year in BENCHMARK_YEARS_SIC:
        return (
            IO_LABELED_DIR / f"{year}_A_matrix_labeled.csv",
            IO_LABELED_DIR / f"{year}_Z_matrix_labeled.csv",
        )
    raise ValueError(f"Year {year} not in labeled IO benchmark cache")


def _derive_gross_output(A_path: Path, Z_path: Path) -> pd.Series:
    """Derive sector gross output X_j from the labeled A and Z matrices.

    A_ij = Z_ij / X_j  ->  X_j = Z_ij / A_ij elementwise (mean over i).
    BEA Benchmark IO tables are in MILLIONS of dollars; rescale to dollars.
    """
    A = pd.read_csv(A_path, index_col=0)
    Z = pd.read_csv(Z_path, index_col=0)
    Av = A.to_numpy()
    Zv = Z.to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(Av > 0, Zv / Av, np.nan)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        Xj = np.nanmean(ratio, axis=0)
    Xj = Xj * 1.0e6  # millions -> dollars
    sector_codes = [int(c) for c in A.columns]
    return pd.Series(Xj, index=sector_codes, name="X_j")


def _leontief_inverse(A_path: Path) -> pd.DataFrame:
    """Return B = (I - A)^{-1} as a DataFrame with sector_code row/col index."""
    A = pd.read_csv(A_path, index_col=0)
    Av = A.to_numpy()
    B = np.linalg.inv(np.eye(Av.shape[0]) - Av)
    cols = [int(c) for c in A.columns]
    return pd.DataFrame(B, index=cols, columns=cols)


def _load_panel() -> pd.DataFrame:
    if not L01_OUTPUT.exists():
        raise FileNotFoundError(
            f"L01_S701 output missing: {L01_OUTPUT}. Run L01_S701_labor_coefficient_productive first."
        )
    return pd.read_csv(L01_OUTPUT)


def _sector_year_hours(panel: pd.DataFrame, year: int) -> pd.Series:
    """For one year, return hp_j = employment x weekly_hours x 52 by sector.

    Returns a Series indexed by sector_code; sectors with NaN BLS coverage
    are dropped.
    """
    yr_panel = panel[panel["year"] == year].copy()
    yr_panel["hp_annual"] = (
        yr_panel["employment_thousands"] * 1000.0  # thousands -> persons
        * yr_panel["weekly_hours"]
        * 52.0
    )
    out = yr_panel.dropna(subset=["hp_annual"]).set_index("sector_code")["hp_annual"]
    # Some sectors map to the same supersector and so have identical values;
    # collapse duplicates by taking the first (they are identical by construction).
    out = out[~out.index.duplicated(keep="first")]
    return out


def _benchmark_scalar(year: int, panel: pd.DataFrame, X_year: int) -> tuple[Optional[float], str, int]:
    """Compute the S701 productive labor coefficient scalar for one year.

    `year`: target observation year (may be non-benchmark for EXT).
    `X_year`: which IO benchmark year supplies the A matrix / gross output
              denominator.

    Returns (value, provenance, n_sectors). value is None if BLS coverage
    is empty for that year (no productive sectors with non-NaN hp).
    """
    hp_by_sec = _sector_year_hours(panel, year)
    if hp_by_sec.empty:
        return None, f"no_BLS_coverage_for_year_{year}", 0

    A_path, Z_path = _io_paths(X_year)
    if not A_path.exists() or not Z_path.exists():
        return None, f"missing_IO_for_X_year_{X_year}", 0

    X = _derive_gross_output(A_path, Z_path)
    B = _leontief_inverse(A_path)

    # hp* per sector = hp / X (hours / $); restrict to covered sectors.
    common = hp_by_sec.index.intersection(X.index)
    if len(common) == 0:
        return None, f"sector_code_mismatch_X_year_{X_year}", 0
    # Drop sectors with non-positive or non-finite X (e.g., 1963 zero columns)
    X_common = X.loc[common]
    valid = X_common[X_common > 0].dropna().index
    if len(valid) == 0:
        return None, f"no_positive_X_for_X_year_{X_year}", 0
    hp_star = hp_by_sec.loc[valid] / X.loc[valid]

    # Second-stage Leontief: lambda_p = hp* @ B restricted to covered sectors.
    # Build a full-length hp* vector with zeros for non-covered sectors, then
    # multiply by B and take the mean over covered sectors.
    hp_full = pd.Series(0.0, index=B.index)
    hp_full.loc[valid] = hp_star.loc[valid]
    lambda_p = hp_full.to_numpy() @ B.to_numpy()  # shape (n,)
    lambda_p_ser = pd.Series(lambda_p, index=B.index)
    value = float(lambda_p_ser.loc[valid].mean())

    prov = (
        f"hp*=BLS_emp_hr_per_year/X_j; lambda_p=hp*x(I-A)^-1; "
        f"X_year={X_year}; n_covered_prod_sectors={len(valid)}"
    )
    return value, prov, len(valid)


def compute_book_subseries(panel: pd.DataFrame) -> pd.DataFrame:
    """S701-A: book-period (1948-1989) scalars at SIC benchmark years."""
    rows = []
    for yr in BENCHMARK_YEARS_SIC:
        if yr < BOOK_PERIOD[0] or yr > BOOK_PERIOD[1]:
            continue
        value, prov, n = _benchmark_scalar(yr, panel, X_year=yr)
        rows.append({
            "series_id":  SUB_BOOK,
            "year":       yr,
            "value":      value if value is not None else float("nan"),
            "units":      "hr_per_dollar",
            "stage":      "benchmark_book_sic",
            "provenance": prov,
        })
    return pd.DataFrame(rows)


def _pick_X_year_for_extension(year: int) -> int:
    """Choose IO benchmark year for extension years.

    Same convention as P02_S702: stay on 1977 SIC weights throughout for
    sector-code compatibility with the L01_S701 panel which carries SIC-era
    sector_code values. NAICS bridge is documented in the EPR.
    """
    return 1977


def compute_extension_subseries(panel: pd.DataFrame) -> pd.DataFrame:
    """S701-EXT: annual (1990-2024) where BLS CES coverage exists."""
    rows = []
    for yr in range(EXT_PERIOD[0], EXT_PERIOD[1] + 1):
        X_yr = _pick_X_year_for_extension(yr)
        value, prov, n = _benchmark_scalar(yr, panel, X_year=X_yr)
        if value is None:
            continue
        rows.append({
            "series_id":  SUB_EXT,
            "year":       yr,
            "value":      value,
            "units":      "hr_per_dollar",
            "stage":      "extension_annual_bls",
            "provenance": prov + "; IO_aging=1977_SIC_weights_held_forward",
        })
    return pd.DataFrame(rows)


def compute() -> pd.DataFrame:
    panel = _load_panel()
    book = compute_book_subseries(panel)
    ext = compute_extension_subseries(panel)
    combined = pd.concat([book.assign(series_id=SUB_COMBINED),
                          ext.assign(series_id=SUB_COMBINED)],
                         ignore_index=True)
    combined = combined.sort_values("year").reset_index(drop=True)
    out = pd.concat([book, ext, combined], ignore_index=True)
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")

    book = df[df["series_id"] == SUB_BOOK]
    ext = df[df["series_id"] == SUB_EXT]
    n_book_valid = book["value"].notna().sum()
    n_ext_valid = ext["value"].notna().sum()
    print(f"    [P02_S701] wrote {final_path.name}")
    print(f"    [P02_S701] {SUB_BOOK}: {len(book)} rows ({n_book_valid} with BLS coverage)")
    print(f"    [P02_S701] {SUB_EXT}:  {len(ext)} rows (BLS-covered years only)")
    print(f"    [P02_S701] {SUB_COMBINED}: {len(df[df['series_id'] == SUB_COMBINED])} rows")
    if n_book_valid:
        print(f"    [P02_S701] book sample (non-NaN):")
        print(book.dropna(subset=["value"]).head(6).to_string(index=False))
    if n_ext_valid:
        print(f"    [P02_S701] ext sample (first 3, mid, last):")
        sel = pd.concat([ext.head(3), ext.iloc[[len(ext)//2]], ext.tail(2)])
        print(sel.to_string(index=False))
    return df


if __name__ == "__main__":
    run()
