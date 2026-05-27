"""P02_S702 -- Unproductive Labor Coefficient (Ch7 real-fix, v1.1 Phase 4).

Replaces the prior matrix-derived proxy (`mean(column_sum(Leontief inverse)) x (1+r*)`)
with the book's actual unproductive labor coefficient construction. The previous
proxy was flagged in `Technical/Handoffs/CH7_REAL_FIX_PLAN.md` and the project
`CLAUDE.md` anti-pattern list as a placeholder pending BLS sourcing.

Book methodology (S&T 1994, Ch4 sec 4.1 pp.78-88; Appendix G; Appendix F Table F.1):

    For each unproductive sector j (productive_share < 0.5 per Appendix F):
        hu_j       = production_workers_j x weekly_hours_j x 52         (hours/year)
        Xj         = gross output of sector j (producer prices, from BEA IO)
        hu*_j      = hu_j / Xj                                          (hr/$)
        lambda_u*  = hu* (I - app*)^{-1}                                (Leontief, sector vector)
        S702-A(yr) = mean_j(lambda_u*_j)                                (scalar published series)

The legacy file documented this as "prices_of_production" but the v1.1 Ch7
real-fix repurposes S702 to its book-correct meaning: the UNPRODUCTIVE labor
coefficient (symmetric to S701's productive labor coefficient). Prices-of-
production per se are not separately reconstructed in v1.1 -- see S703 for
the deviation diagnostic the book actually publishes (Khanjian 6%-9%).

Inputs (consumed -- do not refetch):
  - L01_S702 panel:  data/raw/ch07/L01_S702_output.csv (BLS CES emp + hours,
    long format, sector x year, unproductive sectors only, 1948-2024).
  - Labeled BEA IO matrices: data/intermediate/io_matrices_labeled/
    {yr}_A_matrix_labeled.csv  +  {yr}_Z_matrix_labeled.csv. Sector codes are
    integer (1..85) matching Appendix F sector_code. Xj derived from Zj/Aij
    elementwise (where both nonzero) -- equivalent to Z column sum given the
    A-col-sum=1 normalization in this cache.
  - S701 final:      data/final/S701.csv (productive labor coefficient,
    written by P02_S701 in the same Phase 4 cohort -- used for unit
    consistency check only).

Subseries:
  - S702-A         book period (1948-1989), benchmark-year scalars at
                   1972, 1977 (only benchmark years with full BLS CES
                   unproductive-sector coverage); other SIC benchmark years
                   (1947, 1958, 1963, 1967) emitted as NaN with a coverage
                   note in the provenance column (NOT fabricated).
  - S702-EXT       extension period (1990-2024), annual where BLS CES
                   coverage exists; IO matrix weights held at the most-
                   recent applicable SIC/NAICS benchmark per year.
  - S702-COMBINED  union of -A and -EXT, kept distinct from the -A subseries
                   to honor Decision 0003 (binary extension policy: the
                   project's registry currently has `extension: None` for
                   S702; this -EXT/-COMBINED output anticipates the
                   registry-side extension authoring tracked separately).

Outputs:
  - data/intermediate/S702.csv
  - data/final/S702.csv
    Columns: series_id, year, value, units, stage, provenance

Units: `hours_per_dollar` (hr/$) -- distinct from the legacy `index` units
of the proxy. This is the unproductive analogue of S701's hr/$ coefficient.

Methodology distinction from the proxy:
  - Proxy applied a single scalar (1+r*) markup to the AVERAGE Leontief column
    sum across all 85 sectors regardless of productive/unproductive
    classification, producing a dimensionless "index" with no labor content.
  - Real fix uses BLS production-worker hours for the UNPRODUCTIVE partition
    only, divided by IO gross output, and aggregated per sector -- so the
    resulting hu*_j is in actual hours per dollar of unproductive sector output.
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


SERIES_ID = "S702"
SUB_BOOK = "S702-A"
SUB_EXT = "S702-EXT"
SUB_COMBINED = "S702-COMBINED"

# Benchmark IO years available in the labeled SIC cache.
BENCHMARK_YEARS_SIC = [1947, 1958, 1963, 1967, 1972, 1977]
BENCHMARK_YEARS_NAICS = [1997, 2002, 2007, 2012]

# Period definitions per task spec.
BOOK_PERIOD = (1948, 1989)
EXT_PERIOD = (1990, 2024)

# Input paths.
L01_OUTPUT = DATA_RAW / "ch07" / "L01_S702_output.csv"
IO_LABELED_DIR = DATA_INTERMEDIATE / "io_matrices_labeled"


def _io_paths(year: int) -> tuple[Path, Path]:
    """Return (A_path, Z_path) for a benchmark year, SIC or NAICS."""
    if year in BENCHMARK_YEARS_SIC:
        return (
            IO_LABELED_DIR / f"{year}_A_matrix_labeled.csv",
            IO_LABELED_DIR / f"{year}_Z_matrix_labeled.csv",
        )
    if year in BENCHMARK_YEARS_NAICS:
        # NAICS files have a different suffix; column/row codes are NAICS,
        # not BEA 85-SIC. Not used for S702-A but listed for completeness.
        return (
            IO_LABELED_DIR / f"{year}_A_matrix_naics_labeled.csv",
            IO_LABELED_DIR / f"{year}_Z_matrix_naics_labeled.csv",
        )
    raise ValueError(f"Year {year} not in labeled IO benchmark cache")


def _derive_gross_output(A_path: Path, Z_path: Path) -> pd.Series:
    """Derive sector gross output X_j from the labeled A and Z matrices.

    Because A_ij = Z_ij / X_j, we recover X_j elementwise wherever both Aij
    and Zij are non-zero and take the mean over rows (yields exact X_j when
    the BEA convention is consistent, which this cache's A-col-sum=1
    normalisation confirms it is). Returns a Series indexed by sector_code.
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
    # BEA Benchmark IO tables are in MILLIONS of dollars; rescale to dollars
    # so the resulting hr/$ coefficient is in standard units.
    Xj = Xj * 1.0e6
    # Sector codes are the column header (string) and the row index (int).
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
            f"L01_S702 output missing: {L01_OUTPUT}. Run L01_S702_labor_coefficient_unproductive first."
        )
    df = pd.read_csv(L01_OUTPUT)
    return df


def _sector_year_hours(panel: pd.DataFrame, year: int) -> pd.Series:
    """For one benchmark year, return hu_j = employment x weekly_hours x 52 by sector.

    Returns a Series indexed by sector_code; sectors with NaN BLS coverage
    are dropped. The 5 unproductive sectors with CES coverage in the L01
    panel are codes 69, 70, 71, 72, 74 (per the L01 cache inspection).
    """
    yr_panel = panel[panel["year"] == year].copy()
    yr_panel["hu_annual"] = (
        yr_panel["employment_thousands"] * 1000.0  # thousands -> persons
        * yr_panel["weekly_hours"]
        * 52.0
    )
    out = yr_panel.dropna(subset=["hu_annual"]).set_index("sector_code")["hu_annual"]
    return out


def _benchmark_scalar(year: int, panel: pd.DataFrame, X_year: int) -> tuple[Optional[float], str, int]:
    """Compute the S702 unproductive labor coefficient scalar for one year.

    `year`: target observation year (may be non-benchmark for EXT).
    `X_year`: which IO benchmark year supplies the A matrix / gross output
              denominator. For the book period -A we use year itself if it
              is a benchmark, else NaN. For EXT we use the most-recent
              applicable SIC benchmark (1977 throughout 1990-1996) or the
              NAICS benchmark year (1997, 2002, 2007, 2012) for later years.

    Returns (value, provenance, n_sectors). value is None if BLS coverage
    is empty for that year (no sectors with non-NaN hu).
    """
    hu_by_sec = _sector_year_hours(panel, year)
    if hu_by_sec.empty:
        return None, f"no_BLS_coverage_for_year_{year}", 0

    A_path, Z_path = _io_paths(X_year)
    if not A_path.exists() or not Z_path.exists():
        return None, f"missing_IO_for_X_year_{X_year}", 0

    X = _derive_gross_output(A_path, Z_path)
    B = _leontief_inverse(A_path)

    # hu* per sector = hu / X (hours / $); restrict to covered sectors.
    common = hu_by_sec.index.intersection(X.index)
    if len(common) == 0:
        return None, f"sector_code_mismatch_X_year_{X_year}", 0
    hu_star = hu_by_sec.loc[common] / X.loc[common]

    # Second-stage Leontief: lambda_u* = hu* @ B restricted to the covered sectors.
    # We build a length-n hu* vector with zeros for non-covered sectors, then
    # multiply by B and take the mean over covered sectors (the unproductive
    # partition we wrote BLS for). This is the natural extension of the
    # one-sector worked example in Ch4 footnote 4 to a sparse-coverage panel.
    n = B.shape[0]
    hu_full = pd.Series(0.0, index=B.index)
    hu_full.loc[common] = hu_star.loc[common]
    lambda_u = hu_full.to_numpy() @ B.to_numpy()  # shape (n,)
    lambda_u_ser = pd.Series(lambda_u, index=B.index)
    # Average across the covered (BLS-observed) unproductive sectors.
    value = float(lambda_u_ser.loc[common].mean())

    prov = (
        f"hu*=BLS_emp_hr_per_year/X_j; lambda_u*=hu*x(I-A)^-1; "
        f"X_year={X_year}; n_covered_unprod_sectors={len(common)}"
    )
    return value, prov, len(common)


def compute_book_subseries(panel: pd.DataFrame) -> pd.DataFrame:
    """S702-A: book-period (1948-1989) scalars, benchmark IO years only."""
    rows = []
    for yr in BENCHMARK_YEARS_SIC:
        if yr < BOOK_PERIOD[0] or yr > BOOK_PERIOD[1]:
            continue
        value, prov, n = _benchmark_scalar(yr, panel, X_year=yr)
        rows.append({
            "series_id":  SUB_BOOK,
            "year":       yr,
            "value":      value if value is not None else float("nan"),
            "units":      "hours_per_dollar",
            "stage":      "benchmark_book_sic",
            "provenance": prov,
        })
    return pd.DataFrame(rows)


def _pick_X_year_for_extension(year: int) -> int:
    """Choose IO benchmark year for extension years.

    1990-1996: latest SIC benchmark = 1977.
    1997-2001: NAICS 1997 (but its sector codes are NAICS, not 85-SIC;
               drop to 1977 SIC for sector-code compatibility with the
               L01_S702 panel which carries SIC-era sector_code values).
    >=1997:    Same caveat -- stay on 1977 SIC weights so the BLS panel
               sector_codes line up. This is an explicit IO-aging assumption
               documented in the EPR; alternative would be to remap.
    """
    return 1977


def compute_extension_subseries(panel: pd.DataFrame) -> pd.DataFrame:
    """S702-EXT: annual (1990-2024) where BLS CES unproductive coverage exists."""
    rows = []
    for yr in range(EXT_PERIOD[0], EXT_PERIOD[1] + 1):
        X_yr = _pick_X_year_for_extension(yr)
        value, prov, n = _benchmark_scalar(yr, panel, X_year=X_yr)
        if value is None:
            continue  # skip years with no BLS coverage; do not fabricate
        rows.append({
            "series_id":  SUB_EXT,
            "year":       yr,
            "value":      value,
            "units":      "hours_per_dollar",
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
    print(f"    [P02_S702] wrote {final_path.name}")
    print(f"    [P02_S702] {SUB_BOOK}: {len(book)} rows ({n_book_valid} with BLS coverage)")
    print(f"    [P02_S702] {SUB_EXT}:  {len(ext)} rows (BLS-covered years only)")
    print(f"    [P02_S702] {SUB_COMBINED}: {len(df[df['series_id'] == SUB_COMBINED])} rows")
    if n_book_valid:
        print(f"    [P02_S702] book sample (non-NaN):")
        print(book.dropna(subset=["value"]).head(4).to_string(index=False))
    if n_ext_valid:
        print(f"    [P02_S702] ext sample (first 3):")
        print(ext.head(3).to_string(index=False))
    return df


if __name__ == "__main__":
    run()
