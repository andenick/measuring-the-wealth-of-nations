"""Input-output matrix operations for Chapters 4 and 7.

Implements:
  A-matrix construction (technical coefficients)
  B-matrix = (I - A)^{-1} (Leontief inverse)
  Labor value computation v = l x B
  Price of production computation
  Sector classification (productive/unproductive/trading)
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_technical_coefficients(
    z_matrix: pd.DataFrame,
    x_vector: pd.Series,
) -> pd.DataFrame:
    """Compute A-matrix: a_ij = z_ij / x_j.

    Parameters
    ----------
    z_matrix : pd.DataFrame
        Transactions matrix (rows = sectors, cols = sectors).
    x_vector : pd.Series
        Total output vector (indexed by sector).
    """
    x_safe = x_vector.replace(0, float("nan"))
    return z_matrix.div(x_safe, axis=1)


def compute_leontief_inverse(a_matrix: pd.DataFrame) -> pd.DataFrame:
    """B = (I - A)^{-1} (Leontief inverse)."""
    n = len(a_matrix)
    identity = np.eye(n)
    i_minus_a = identity - a_matrix.values
    b_values = np.linalg.inv(i_minus_a)
    return pd.DataFrame(b_values, index=a_matrix.index, columns=a_matrix.columns)


def compute_labor_values(
    labor_coefficients: pd.Series,
    b_matrix: pd.DataFrame,
) -> pd.Series:
    """v = l x B (labor values per unit output)."""
    l_vec = labor_coefficients.reindex(b_matrix.index).fillna(0).values
    v_vec = l_vec @ b_matrix.values
    return pd.Series(v_vec, index=b_matrix.columns)


def classify_sectors(
    sector_labels: list[str],
    classification: dict[str, str],
) -> dict[str, list[str]]:
    """Group sectors into productive/unproductive/trading categories.

    Parameters
    ----------
    sector_labels : list[str]
        Sector identifiers from the IO table.
    classification : dict[str, str]
        Maps sector label -> category ("productive", "unproductive", "trading").

    Returns
    -------
    dict with keys "productive", "unproductive", "trading", each a list of sector labels.
    """
    groups: dict[str, list[str]] = {"productive": [], "unproductive": [], "trading": []}
    for label in sector_labels:
        cat = classification.get(label, "unproductive")
        groups.setdefault(cat, []).append(label)
    return groups


def load_matrix_csv(path: str | Path, n: int = 85) -> np.ndarray:
    """Load a headerless CSV of floats into an (n x n) numpy array."""
    from pathlib import Path as _Path
    arr = np.loadtxt(_Path(path), delimiter=",")
    if arr.shape != (n, n):
        raise ValueError(f"Expected ({n},{n}) matrix, got {arr.shape} from {path}")
    return arr


def recover_gross_output(z_matrix: np.ndarray, a_matrix: np.ndarray) -> np.ndarray:
    """Recover gross output x_j = sum_i(z_ij) / sum_i(a_ij) for each column j.

    Where A column sums are zero (no intermediate inputs), x_j is set to 0.
    """
    z_col_sums = z_matrix.sum(axis=0)
    a_col_sums = a_matrix.sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.where(a_col_sums > 0, z_col_sums / a_col_sums, 0.0)
    return x


def distribute_employment(
    nipa_emp: pd.DataFrame,
    gross_output: np.ndarray,
    concordance_df: pd.DataFrame,
) -> np.ndarray:
    """Distribute 13-industry employment to 85 IO sectors using output weights.

    Parameters
    ----------
    nipa_emp : pd.DataFrame
        Must have columns 'industry' and 'employment'.
    gross_output : np.ndarray
        85-element gross output vector.
    concordance_df : pd.DataFrame
        Must have columns 'io_sector' (1-85), 'nipa_industry_name', and rows
        ordered by io_sector.

    Returns
    -------
    np.ndarray of shape (85,) — employment by IO sector.
    """
    emp_85 = np.zeros(85)
    conc = concordance_df.sort_values("io_sector").reset_index(drop=True)

    for _, row in nipa_emp.iterrows():
        ind_name = row["industry"]
        ind_emp = row["employment"]

        # Find IO sectors mapped to this NIPA industry
        mask = conc["nipa_industry_name"] == ind_name
        sector_indices = conc.loc[mask, "io_sector"].values.astype(int) - 1  # 0-based

        if len(sector_indices) == 0:
            continue

        # Weight by gross output share within this NIPA group
        outputs = gross_output[sector_indices]
        total_output = outputs.sum()
        if total_output > 0:
            weights = outputs / total_output
        else:
            weights = np.ones(len(sector_indices)) / len(sector_indices)

        emp_85[sector_indices] = ind_emp * weights

    return emp_85
