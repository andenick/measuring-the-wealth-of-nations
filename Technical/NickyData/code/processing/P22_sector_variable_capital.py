#!/usr/bin/env python3
"""P02b - Sector-level V* per Appendix G: V* = Σ (ecp_j × Lp_j).

Uses NIPA 6.2D (compensation), NIPA 6.5D (FTE), BLS CES (production workers)
with the NIPA 6.5 → IO productive sector classification.

For sectors with BLS production worker data (mining, construction, manufacturing):
  V*_j = (BLS_wage_j × supplements_ratio) × BLS_prod_workers_j

For other productive sectors (transport, health, education, etc.):
  V*_j = (EC_j / FEE_j) × (FEE_j × pw_fraction_j)
  where pw_fraction comes from GVA ratio or sector-specific estimate

Inputs:  Inputs/API_Data/BEA/nipa_6_2D_compensation_by_industry.csv
         Inputs/API_Data/BEA/nipa_6_5D_fte_by_industry.csv
         Inputs/API_Data/BLS/bls_ces_production_workers.csv
         nipa_65_to_io_classification.json
Outputs: final-data/series/V_star_sector.csv
         final-data/series/K_star_by_industry.csv (if Fixed Assets available)
Dependencies: L06b (Fixed Assets, optional)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, CONFIG, ensure_dirs

SERIES_IDS = []
PRIORITY = 2

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
API_DATA = PROJECT_ROOT / "Inputs" / "API_Data"
NIPA62_PATH = API_DATA / "BEA" / "nipa_6_2D_compensation_by_industry.csv"
NIPA65_PATH = API_DATA / "BEA" / "nipa_6_5D_fte_by_industry.csv"
BLS_PATH = API_DATA / "BLS" / "bls_ces_production_workers.csv"


def _load_classification() -> dict:
    cls_path = CONFIG / "nipa_65_to_io_classification.json"
    if not cls_path.exists():
        return {}
    with open(cls_path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def _parse_nipa_by_line(path: Path, line_numbers: list[int]) -> pd.DataFrame:
    """Parse NIPA CSV, extract specified LineNumbers, return year×line DataFrame."""
    raw = pd.read_csv(path)
    result = {}
    for ln in line_numbers:
        subset = raw[raw["LineNumber"] == ln].copy()
        if subset.empty:
            continue
        vals = {}
        for _, row in subset.iterrows():
            yr = int(row["TimePeriod"])
            val_str = str(row["DataValue"]).replace(",", "")
            try:
                vals[yr] = float(val_str)
            except ValueError:
                continue
        result[ln] = pd.Series(vals)
    df = pd.DataFrame(result)
    df.index.name = "year"
    return df


def _load_bls_pw_ratios() -> dict[str, pd.Series]:
    """Load BLS CES production worker ratios by sector."""
    if not BLS_PATH.exists():
        return {}
    bls = pd.read_csv(BLS_PATH, index_col="year")
    sector_pairs = {
        7: ("CES1000000006", "CES1000000001"),    # Mining
        12: ("CES2000000006", "CES2000000001"),   # Construction
        13: ("CES3000000006", "CES3000000001"),   # Manufacturing
    }
    ratios = {}
    for ln, (prod_col, total_col) in sector_pairs.items():
        if prod_col in bls.columns and total_col in bls.columns:
            ratio = bls[prod_col] / bls[total_col]
            ratios[ln] = ratio.dropna()
    return ratios


# Default production worker fractions for sectors without BLS data
DEFAULT_PW_FRACTIONS = {
    4: 0.80,   # Agriculture
    11: 0.80,  # Utilities
    43: 0.75,  # Transportation
    54: 0.70,  # Motion pictures
    55: 0.65,  # Broadcasting/telecom
    72: 0.85,  # Waste management
    73: 0.70,  # Education
    74: 0.70,  # Health care
    79: 0.75,  # Arts/entertainment
    82: 0.80,  # Accommodation/food
    85: 0.70,  # Other services
    91: 0.75,  # Fed govt enterprises
    96: 0.75,  # State/local govt enterprises
}


def compute_sector_v_star() -> tuple[pd.Series, list[str]]:
    """Compute V* = Σ(ec_j × Lp_j) for productive sectors."""
    steps = []
    cls_data = _load_classification()
    if not cls_data:
        return pd.Series(dtype=float), ["Classification not found"]

    productive_lines = cls_data.get("productive_lines", [])
    if not productive_lines:
        return pd.Series(dtype=float), ["No productive lines defined"]

    if not NIPA62_PATH.exists() or not NIPA65_PATH.exists():
        return pd.Series(dtype=float), ["NIPA 6.2D or 6.5D not found"]

    ec_df = _parse_nipa_by_line(NIPA62_PATH, productive_lines)
    fte_df = _parse_nipa_by_line(NIPA65_PATH, productive_lines)
    bls_ratios = _load_bls_pw_ratios()

    steps.append(f"EC data: {len(ec_df)} years × {len(ec_df.columns)} sectors")
    steps.append(f"FTE data: {len(fte_df)} years × {len(fte_df.columns)} sectors")
    steps.append(f"BLS PW ratios: {len(bls_ratios)} sectors")

    common_years = sorted(set(ec_df.index) & set(fte_df.index))
    v_star = pd.Series(dtype=float)

    for yr in common_years:
        total = 0.0
        for ln in productive_lines:
            if ln not in ec_df.columns:
                continue
            ec = ec_df.loc[yr, ln] if yr in ec_df.index else None
            if pd.isna(ec) or ec <= 0:
                continue

            if ln in bls_ratios and yr in bls_ratios[ln].index:
                pw_ratio = bls_ratios[ln][yr]
            else:
                pw_ratio = DEFAULT_PW_FRACTIONS.get(ln, 0.70)

            total += ec * pw_ratio

        if total > 0:
            v_star[yr] = total / 1e3  # millions → billions

    v_star.index.name = "year"
    steps.append(f"Sector V*: {len(v_star)} years ({int(v_star.index.min())}-{int(v_star.index.max())})")
    return v_star, steps


def process():
    """Compute sector V* and compare with aggregate P02."""
    ensure_dirs()

    v_star_sector, steps = compute_sector_v_star()
    if v_star_sector.empty:
        print(f"    [P02b] Sector V*: skipped ({steps[-1] if steps else 'no data'})")
        return {"series_id": "V_STAR_SECTOR", "status": "skip", "steps": steps, "outputs": []}

    # Compare with P02 aggregate
    t504_path = SERIES_OUT / "T504.csv"
    if t504_path.exists():
        t504 = pd.read_csv(t504_path, index_col=0)
        col = "combined" if "combined" in t504.columns else t504.columns[-1]
        t504_combined = t504[col].dropna()
        t504_combined.index = t504_combined.index.astype(int)
        common = v_star_sector.index.intersection(t504_combined.index)
        if len(common) > 5:
            ratio = (v_star_sector[common] / t504_combined[common]).mean()
            diff_pct = ((v_star_sector[common] - t504_combined[common]).abs() / t504_combined[common]).mean()
            steps.append(f"Sector vs aggregate: ratio={ratio:.3f}, mean diff={diff_pct:.1%}")
            print(f"    [P02b] Sector V*/Aggregate V*: {ratio:.3f} (diff {diff_pct:.1%})")

    out_path = SERIES_OUT / "V_star_sector.csv"
    v_star_sector.to_frame(name="V_star_sector_bn").to_csv(out_path)
    print(f"    [P02b] Sector V*: {len(v_star_sector)} years, "
          f"{v_star_sector.iloc[0]:.1f} → {v_star_sector.iloc[-1]:.1f} bn")

    return {"series_id": "V_STAR_SECTOR", "status": "ok",
            "steps": steps, "outputs": [str(out_path)]}
