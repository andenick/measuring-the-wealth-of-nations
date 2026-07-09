"""Shared engine for the REBUILT I-O matrix cache (workpackage C, review 2026-07).

Replaces all downstream use of `io_matrices_labeled/` for Leontief computations.
The rebuilt cache (`Technical/data/intermediate/io_matrices_rebuilt/`) contains:
  - SIC 85x85 A/L with A = Z / gross-output-X (P2 finding: the old cache's A was
    normalized by column-intermediate totals -> near-singular (I-A));
  - NAICS 71x71 L taken directly from BEA's published Total Requirements (IxI,
    summary) benchmark tables, A = I - L^{-1};
  - X gross-output vectors in millions of dollars.
See `io_matrices_rebuilt/WP-C_MATRIX_REBUILD.md` for the full method + validation.

Extension design implemented here (P2 frozen-weights audit recommendation =
moving benchmark weights; frozen-1977 retained as a documented variant):
  1990-1996  : rebuilt 1977 SIC A/L (last in-repo SIC benchmark; the 1982/87/92
               SIC benchmarks are not in the repo) + X_j updated ANNUALLY via
               NIPA-bucket value-added growth from the BEA archive workbook
               GDPbyInd_VA_SIC.xls (72SIC + 87SIC sheets, chained at 1987).
  1997-2024  : nearest previous NAICS benchmark L (1997/2002/2007/2012/2017) +
               annual BEA GDP-by-industry gross output X; BLS panel hours
               remapped io-85 -> NAICS-71 via sic_naics_bridge.csv, split across
               multi-target bridges in proportion to target gross output.
  1997 break : ratio-splice (the 1997 SIC->NAICS scheme change is the documented
               method change); splice factors are computed from the 1997
               both-ways overlap and reported by the callers.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_TECH = Path(__file__).resolve().parents[2]          # Technical/
REBUILT_DIR = _TECH / "data" / "intermediate" / "io_matrices_rebuilt"
BRIDGE_CSV = _TECH / "data" / "source" / "concordances" / "sic_naics_bridge.csv"
GO_CACHE = _TECH / "data" / "raw" / "bea" / "gdp_by_industry_gross_output.csv"
SIC_WORKBOOK = _TECH / "data" / "raw" / "bea" / "GDPbyInd_VA_SIC.xls"
CONC_IO85 = _TECH.parent / "Inputs" / "predecessor-build" / "Inputs" / "Concordances" / "io_85_to_nipa_13_concordance.csv"

SIC_BENCHMARKS = [1947, 1958, 1963, 1967, 1972, 1977]
NAICS_BENCHMARKS = [1997, 2002, 2007, 2012, 2017]

# NIPA-13 bucket -> workbook VA aggregate title (same map as the T1 rebuild)
_BUCKET_TITLE = {
    1: "Agriculture, forestry, and fishing", 2: "Mining", 3: "Construction",
    4: "Durable goods", 5: "Nondurable goods", 6: "Transportation",
    7: "Communications", 8: "Electric, gas, and sanitary services",
    9: "Wholesale trade", 10: "Retail trade",
    11: "Finance, insurance, and real estate", 12: "Services", 13: "Government",
}
_GOVT_ENTERPRISE_SECTORS = {79, 80}


# ------------------------------------------------------------------ SIC side
@lru_cache(maxsize=None)
def load_sic(year: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Return (A, L, X_musd) for a rebuilt SIC benchmark year, int sector codes."""
    if year not in SIC_BENCHMARKS:
        raise ValueError(f"{year} is not a rebuilt SIC benchmark")
    A = pd.read_csv(REBUILT_DIR / f"{year}_A_rebuilt.csv", index_col=0)
    L = pd.read_csv(REBUILT_DIR / f"{year}_L_rebuilt.csv", index_col=0)
    X = pd.read_csv(REBUILT_DIR / f"{year}_X_gross_output.csv", index_col=0)["gross_output_musd"]
    for m in (A, L):
        m.columns = [int(c) for c in m.columns]
        m.index = [int(i) for i in m.index]
    X.index = [int(i) for i in X.index]
    return A, L, X


@lru_cache(maxsize=1)
def _workbook_va() -> tuple[pd.DataFrame, pd.DataFrame]:
    """(VA72, VA87) blocks: title-indexed, year columns, duplicate titles summed."""
    out = []
    for sheet in ("72SIC_VA, GO, II", "87SIC_VA, GO, II"):
        df = pd.read_excel(SIC_WORKBOOK, sheet_name=sheet, header=None)
        years = [int(v) for v in df.iloc[0, 2:].dropna().tolist()]
        rows = df[df[0].astype(str).str.strip() == "VA"]
        acc: dict = {}
        for _, r in rows.iterrows():
            title = str(r[1]).strip()
            vals = pd.to_numeric(r[2:2 + len(years)], errors="coerce").to_numpy(dtype=float)
            if title in acc:
                acc[title] = np.nansum([acc[title], vals], axis=0)
            else:
                acc[title] = vals
        out.append(pd.DataFrame.from_dict(acc, orient="index", columns=years))
    return out[0], out[1]


@lru_cache(maxsize=1)
def _bucket_of() -> dict:
    conc = pd.read_csv(CONC_IO85)
    return dict(zip(conc["io_sector"], conc["nipa_industry"]))


def sic_X_annual(year: int) -> pd.Series:
    """X_j (millions $) for a post-benchmark SIC year 1978-1997.

    X_j(t) = X_j(1977, rebuilt) * g_b(t), with bucket nominal growth
    g_b(t) = [VA87(b,t)/VA87(b,1987)] * [VA72(b,1987)/VA72(b,1977)]
    (chained at 1987 across the two workbook SIC vintages). Government
    enterprises (io 79/80) use the 'Government enterprises' VA line.
    This updates the DOLLAR DENOMINATOR annually (removes the Channel-1
    frozen-nominal bias identified in P2_FROZEN_WEIGHTS_AUDIT.md) while the
    1977 technical structure A is held (no in-repo 1982/87/92 SIC benchmark).
    """
    if not (1978 <= year <= 1997):
        raise ValueError("sic_X_annual covers 1978-1997 only")
    _, _, X77 = load_sic(1977)
    VA72, VA87 = _workbook_va()
    bucket_of = _bucket_of()

    def growth(title: str) -> float:
        a = VA87.loc[title, year] if title in VA87.index and year in VA87.columns else np.nan
        b = VA87.loc[title, 1987] if title in VA87.index else np.nan
        c = VA72.loc[title, 1987] if title in VA72.index else np.nan
        d = VA72.loc[title, 1977] if title in VA72.index else np.nan
        if all(np.isfinite(v) and v > 0 for v in (a, b, c, d)):
            return float((a / b) * (c / d))
        return np.nan

    g_by_bucket = {b: growth(t) for b, t in _BUCKET_TITLE.items()}
    g_ge = growth("Government enterprises")
    g_econ = growth("Gross domestic product /1/")

    X = pd.Series(0.0, index=X77.index)
    for j in X77.index:
        if X77[j] <= 0:
            continue
        if j in _GOVT_ENTERPRISE_SECTORS and np.isfinite(g_ge):
            g = g_ge
        else:
            g = g_by_bucket.get(_bucket_of().get(j), np.nan)
        if not np.isfinite(g):
            g = g_econ
        X[j] = X77[j] * g
    return X


# ---------------------------------------------------------------- NAICS side
@lru_cache(maxsize=None)
def load_naics(year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (A, L) for a rebuilt NAICS benchmark year, str industry codes."""
    if year not in NAICS_BENCHMARKS:
        raise ValueError(f"{year} is not a rebuilt NAICS benchmark")
    A = pd.read_csv(REBUILT_DIR / f"{year}_A_naics_rebuilt.csv", index_col=0)
    L = pd.read_csv(REBUILT_DIR / f"{year}_L_naics_rebuilt.csv", index_col=0)
    return A, L


@lru_cache(maxsize=1)
def _go_annual() -> pd.DataFrame:
    go = pd.read_csv(GO_CACHE)
    go = go[go["Frequency"] == "A"].copy()
    go["musd"] = pd.to_numeric(go["DataValue"], errors="coerce") * 1000.0
    return go[["Year", "Industry", "musd"]]


def naics_X_annual(year: int) -> pd.Series:
    """Annual BEA gross output by NAICS-71 industry, millions $ (1997-2025)."""
    go = _go_annual()
    gy = go[go["Year"] == year].dropna(subset=["musd"])
    return gy.set_index("Industry")["musd"]


@lru_cache(maxsize=1)
def _bridge() -> pd.DataFrame:
    return pd.read_csv(BRIDGE_CSV)


def naics_benchmark_for(year: int) -> int:
    """Step-function nearest-previous NAICS benchmark (P2 recommendation #3)."""
    cands = [b for b in NAICS_BENCHMARKS if b <= year]
    if not cands:
        raise ValueError(f"no NAICS benchmark at or before {year}")
    return max(cands)


# ------------------------------------------ supersector hours (at-rest panel)
def supersector_hours(panel: pd.DataFrame, year: int) -> pd.DataFrame:
    """One row per BLS supersector: (slug, H_ss annual hours, member io85 codes).

    Reads the N1 at-rest-rebuilt L01 panel (T3.3), in which:
      - each supersector's employment total is ALLOCATED across its member
        io-85 sectors (member rows SUM back to the true supersector total), and
      - `weekly_hours` already carries the correct datatype-07 average-weekly-
        hours series (~39-41 hr) rather than the earnings-like dt33 mixup.
    The supersector total is therefore reconstructed by SUMMING the member
    rows' allocated employment, and hours are read directly. The former
    compute-time corrections -- supersector de-duplication (`.iloc[0]` on the
    replicated column) and the manufacturing weekly-hours/earnings substitution
    (`_mfg_hours_fix`) -- are removed; the fix now lives in the panel at rest.
    The X-share split of H_ss to matrix grain (in the callers) stays: it is
    inherent to the BLS-supersector -> IO-sector granularity mismatch, not a
    defect correction.
    """
    yr = panel[(panel["year"] == year)].dropna(subset=["bls_supersector_slug"]).copy()
    rows = []
    for slug, g in yr.groupby("bls_supersector_slug"):
        emp = g["employment_thousands"].sum(min_count=1)   # allocated rows -> supersector total
        wk = g["weekly_hours"].dropna().iloc[0] if g["weekly_hours"].notna().any() else np.nan
        if not (np.isfinite(emp) and np.isfinite(wk)):
            continue
        rows.append({"slug": slug, "H_ss": float(emp) * 1000.0 * float(wk) * 52.0,
                     "members": sorted(g["sector_code"].dropna().astype(int).unique().tolist())})
    return pd.DataFrame(rows)


def hours_io85(panel: pd.DataFrame, year: int, X: pd.Series) -> pd.Series:
    """Per-io85-sector annual hours: supersector totals split by X share."""
    ss = supersector_hours(panel, year)
    out: dict[int, float] = {}
    for r in ss.itertuples():
        members = [j for j in r.members if j in X.index and np.isfinite(X.get(j, np.nan)) and X.get(j, 0) > 0]
        if not members:
            continue
        w = X.loc[members].astype(float)
        w = w / w.sum()
        for j in members:
            out[j] = out.get(j, 0.0) + r.H_ss * float(w[j])
    return pd.Series(out, dtype=float)


def hours_naics(panel: pd.DataFrame, year: int, X_naics: pd.Series) -> pd.Series:
    """Per-NAICS-industry annual hours: supersector totals split across the
    union of the members' bridge targets by NAICS gross-output share."""
    ss = supersector_hours(panel, year)
    br = _bridge()
    out: dict[str, float] = {}
    for r in ss.itertuples():
        targets = br[br["bea_io_85_code"].isin(r.members)]["bea_naics_71_code"].unique().tolist()
        targets = [t for t in targets if t in X_naics.index and X_naics[t] > 0]
        if not targets:
            continue
        w = X_naics.loc[targets].astype(float)
        w = w / w.sum()
        for t in targets:
            out[t] = out.get(t, 0.0) + r.H_ss * float(w[t])
    return pd.Series(out, dtype=float)


# ------------------------------------------------------------- lambda engine
def lambda_vector_sic(hours_io85: pd.Series, year_matrix: int,
                      X_musd: pd.Series | None = None
                      ) -> tuple[pd.Series, pd.Series, pd.Index]:
    """(lambda vector, X used [$M], covered index) on the rebuilt SIC matrices.

    lambda = hstar @ L with hstar_j = hours_j / (X_j * 1e6) on covered sectors,
    zeros elsewhere (sparse-coverage convention retained from v1.1 so book and
    extension remain procedurally identical).
    """
    _, L, Xb = load_sic(year_matrix)
    X = Xb if X_musd is None else X_musd
    covered = [j for j in hours_io85.index
               if j in X.index and np.isfinite(X.get(j, np.nan)) and X.get(j, 0) > 0
               and np.isfinite(hours_io85[j])]
    covered = pd.Index(sorted(set(covered)))
    hstar = pd.Series(0.0, index=L.index)
    hstar.loc[covered] = hours_io85.loc[covered].astype(float) / (X.loc[covered].astype(float) * 1e6)
    lam = pd.Series(hstar.to_numpy() @ L.to_numpy(), index=L.columns)
    return lam, X, covered


def lambda_vector_naics(h_naics: pd.Series, benchmark: int, year: int
                        ) -> tuple[pd.Series, pd.Series, pd.Index]:
    """(lambda vector, X used [$M], covered NAICS index) on rebuilt NAICS L.

    `h_naics` = annual hours by NAICS-71 industry (from `hours_naics`).
    """
    _, L = load_naics(benchmark)
    X = naics_X_annual(year)
    X = X[X.index.isin(L.columns)]
    covered = pd.Index(sorted(c for c in h_naics.index
                              if c in X.index and X[c] > 0 and np.isfinite(h_naics[c])))
    hstar = pd.Series(0.0, index=L.index)
    hstar.loc[covered] = h_naics.loc[covered] / (X.loc[covered] * 1e6)
    lam = pd.Series(hstar.to_numpy() @ L.to_numpy(), index=L.columns)
    return lam, X, covered
