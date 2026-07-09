"""IO matrix utilities — load A and L matrices, compute summary statistics.

workpackage C (review 2026-07): repointed from the DEFECTIVE raw predecessor-build cache
(`data/source/io_matrices/`, whose SIC A matrices were column-share-normalized
and whose 1947/63/72/77 L files were not Leontief inverses — see
P2_MATRIX_VERIFICATION.md) to the REBUILT cache
(`data/intermediate/io_matrices_rebuilt/`, see WP-C_MATRIX_REBUILD.md there).
NAICS 2017 benchmark added (rebuilt from BEA Total Requirements).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .paths import ROOT


REBUILT_DIR = ROOT / "data" / "intermediate" / "io_matrices_rebuilt"

BENCHMARK_YEARS_SIC   = [1947, 1958, 1963, 1967, 1972, 1977]
BENCHMARK_YEARS_NAICS = [1997, 2002, 2007, 2012, 2017]


def load_a_matrix(year: int) -> pd.DataFrame:
    if year in BENCHMARK_YEARS_SIC:
        return pd.read_csv(REBUILT_DIR / f"{year}_A_rebuilt.csv", index_col=0)
    elif year in BENCHMARK_YEARS_NAICS:
        return pd.read_csv(REBUILT_DIR / f"{year}_A_naics_rebuilt.csv", index_col=0)
    raise ValueError(f"Year {year} not a benchmark IO year")


def load_l_matrix(year: int) -> pd.DataFrame:
    """Load Leontief inverse L = (I-A)^-1 from the rebuilt cache."""
    if year in BENCHMARK_YEARS_SIC:
        return pd.read_csv(REBUILT_DIR / f"{year}_L_rebuilt.csv", index_col=0)
    elif year in BENCHMARK_YEARS_NAICS:
        return pd.read_csv(REBUILT_DIR / f"{year}_L_naics_rebuilt.csv", index_col=0)
    raise ValueError(f"Year {year} not a benchmark IO year")


def a_matrix_summary(year: int) -> dict:
    """Summary statistics for a single rebuilt A-matrix benchmark year.

    max_eigenvalue is the spectral radius of A (Hawkins-Simon viability: < 1).
    leontief_max_dev checks (I-A)^-1 against the stored rebuilt L (internal
    identity; machine precision expected).
    """
    A = load_a_matrix(year).to_numpy()
    n = A.shape[0]
    sparsity = float((A != 0).sum() / (n * n))
    eigenvalues = np.linalg.eigvals(A)
    max_eig = float(np.abs(eigenvalues).max())
    try:
        cond = float(np.linalg.cond(A))
    except Exception:
        cond = float("nan")
    try:
        L = load_l_matrix(year).to_numpy()
        L_computed = np.linalg.inv(np.eye(n) - A)
        leontief_max_dev = float(np.abs(L_computed - L).max())
    except Exception:
        leontief_max_dev = float("nan")
    return {
        "year":             year,
        "n_sectors":        n,
        "sparsity":         round(sparsity, 4),
        "max_eigenvalue":   round(max_eig, 6),
        "condition_number": round(cond, 2),
        "leontief_max_dev": round(leontief_max_dev, 8) if not np.isnan(leontief_max_dev) else None,
    }


def b_matrix_summary(year: int) -> dict:
    """Summary stats for the rebuilt Leontief inverse B = (I-A)^-1.

    b_colsum_mean (mean total-requirements column multiplier over live columns)
    is the canonical interpretable scalar: for NAICS years it summarizes BEA's
    own published Total Requirements table; sane US values are ~1.8-2.7.
    """
    A = load_a_matrix(year).to_numpy()
    B = np.linalg.inv(np.eye(A.shape[0]) - A)
    colsums = B.sum(axis=0)
    live = colsums > 1.0 + 1e-9        # exclude zero/dummy columns (colsum == 1)
    live_sums = colsums[live] if live.any() else colsums
    return {
        "year":            year,
        "n_sectors":       B.shape[0],
        "n_live_columns":  int(live.sum()),
        "b_colsum_mean":   round(float(live_sums.mean()), 4),
        "b_colsum_max":    round(float(live_sums.max()), 4),
        "max_b_element":   round(float(np.abs(B).max()), 4),
        "b_trace":         round(float(np.trace(B)), 4),
        "b_frobenius_norm": round(float(np.linalg.norm(B)), 4),
    }
