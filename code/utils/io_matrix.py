"""IO matrix utilities — load A and L matrices, compute summary statistics."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .paths import ROOT


IO_DIR = ROOT / "data" / "source" / "io_matrices"


BENCHMARK_YEARS_SIC   = [1947, 1958, 1963, 1967, 1972, 1977]
BENCHMARK_YEARS_NAICS = [1997, 2002, 2007, 2012]


def load_a_matrix(year: int) -> pd.DataFrame:
    if year in BENCHMARK_YEARS_SIC:
        return pd.read_csv(IO_DIR / f"{year}_A_matrix.csv", index_col=0)
    elif year in BENCHMARK_YEARS_NAICS:
        return pd.read_csv(IO_DIR / "NAICS" / f"{year}_A_matrix_naics.csv", index_col=0)
    raise ValueError(f"Year {year} not a benchmark IO year")


def load_l_matrix(year: int) -> pd.DataFrame:
    """Load Leontief inverse L = (I-A)^-1."""
    if year in BENCHMARK_YEARS_SIC:
        return pd.read_csv(IO_DIR / f"{year}_L_matrix.csv", index_col=0)
    raise ValueError(f"L matrix for year {year} not in SIC cache")


def a_matrix_summary(year: int) -> dict:
    """Summary statistics for a single A-matrix benchmark year."""
    A = load_a_matrix(year).to_numpy()
    n = A.shape[0]
    sparsity = float((A != 0).sum() / (n * n))
    eigenvalues = np.linalg.eigvals(A)
    max_eig = float(np.abs(eigenvalues).max())
    try:
        cond = float(np.linalg.cond(A))
    except Exception:
        cond = float("nan")
    # Leontief deviation: compare (I-A) inverse against the cached L matrix where available
    try:
        L = load_l_matrix(year).to_numpy()
        I_minus_A = np.eye(n) - A
        L_computed = np.linalg.inv(I_minus_A)
        leontief_max_dev = float(np.abs(L_computed - L).max())
    except Exception:
        leontief_max_dev = float("nan")
    return {
        "year":             year,
        "n_sectors":        n,
        "sparsity":         round(sparsity, 4),
        "max_eigenvalue":   round(max_eig, 6),
        "condition_number": round(cond, 2),
        "leontief_max_dev": round(leontief_max_dev, 6) if not np.isnan(leontief_max_dev) else None,
    }


def b_matrix_summary(year: int) -> dict:
    """Summary stats for Leontief inverse B = (I-A)^-1."""
    A = load_a_matrix(year).to_numpy()
    I_minus_A = np.eye(A.shape[0]) - A
    B = np.linalg.inv(I_minus_A)
    return {
        "year":            year,
        "n_sectors":       B.shape[0],
        "max_b_element":   round(float(np.abs(B).max()), 4),
        "b_column_sum_max": round(float(B.sum(axis=0).max()), 4),
        "b_trace":         round(float(np.trace(B)), 4),
        "b_frobenius_norm": round(float(np.linalg.norm(B)), 4),
    }
