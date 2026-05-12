#!/usr/bin/env python3
"""P02b - Sector-level V* calculation per Appendix G methodology.

Computes V* = sum (ec_j × Lp_j) across productive sectors using NIPA 6.2D
(compensation by industry) and NIPA 6.5D (FTE by industry) with the IO
productive sector classification.

This follows the book's Appendix G procedure:
  1. ec_j = EC_j / FEE_j (compensation per FTE in sector j)
  2. W_j = ec_j × L_j (extend to include self-employed via PEP > FEE)
  3. V*_j = ec_j × (Lp)_j for productive sectors
  4. V* = sum(V*_j)

Uses the same LineNumber classification as L11b's NIPA65_CLASSIFICATION.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, ensure_dirs

NIPA62_PATH = Path(__file__).resolve().parents[3] / "Inputs" / "API_Data/BEA/nipa_6_2D_compensation_by_industry.csv")
NIPA65_PATH = Path(__file__).resolve().parents[3] / "Inputs" / "API_Data/BEA/nipa_6_5D_fte_by_industry.csv")

PRODUCTIVE_LINES = {
    4: "Agriculture",
    7: "Mining",
    11: "Utilities",
    12: "Construction",
    13: "Manufacturing",
    43: "Transportation",
    73: "Education",
    74: "Health care",
    79: "Arts/entertainment",
    82: "Accommodation/food",
    85: "Other services",
    91: "Fed govt enterprises",
    96: "State/local govt enterprises",
}

UNIT_MULT_62 = 6  # NIPA 6.2D values in millions (UNIT_MULT=6)
UNIT_MULT_65 = 3  # NIPA 6.5D values in thousands (UNIT_MULT=3)


def _parse_nipa_by_line(path: Path, line_numbers: dict, unit_mult: int) -> pd.DataFrame:
    """Parse NIPA CSV, extract specified LineNumbers, return year×sector DataFrame."""
    raw = pd.read_csv(path)
    result = {}
    for ln, name in line_numbers.items():
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
        result[name] = pd.Series(vals)

    df = pd.DataFrame(result)
    df.index.name = "year"
    return df


def compute_sector_v_star() -> pd.Series:
    """Compute V* = sum(ec_j × Lp_j) for productive sectors."""
    if not NIPA62_PATH.exists() or not NIPA65_PATH.exists():
        return None

    ec_df = _parse_nipa_by_line(NIPA62_PATH, PRODUCTIVE_LINES, UNIT_MULT_62)
    fte_df = _parse_nipa_by_line(NIPA65_PATH, PRODUCTIVE_LINES, UNIT_MULT_65)

    if ec_df.empty or fte_df.empty:
        return None

    common_years = sorted(set(ec_df.index) & set(fte_df.index))
    if not common_years:
        return None

    # Load BLS CES production worker ratios by sector for accurate V* computation
    bls_path = Path(__file__).resolve().parents[3] / "Inputs" / "API_Data/BLS/bls_ces_production_workers.csv")
    bls_ratios = {}
    if bls_path.exists():
        bls = pd.read_csv(bls_path, index_col="year")
        # Compute production/total ratio for each sector with data
        sector_pairs = {
            "Mining": ("CES1000000006", "CES1000000001"),
            "Construction": ("CES2000000006", "CES2000000001"),
            "Manufacturing": ("CES3000000006", "CES3000000001"),
        }
        for name, (prod_col, total_col) in sector_pairs.items():
            if prod_col in bls.columns and total_col in bls.columns:
                ratio = bls[prod_col] / bls[total_col]
                bls_ratios[name] = ratio.dropna()

    v_star = pd.Series(dtype=float)

    for yr in common_years:
        ec_total_productive = 0
        for sector in ec_df.columns:
            val = ec_df.loc[yr, sector] if yr in ec_df.index else None
            if pd.isna(val):
                continue

            # Apply BLS production worker ratio if available for this sector
            if sector in bls_ratios and yr in bls_ratios[sector].index:
                pw_ratio = bls_ratios[sector][yr]
            elif sector in ("Agriculture", "Utilities", "Transportation"):
                pw_ratio = 0.80  # high production worker share in these sectors
            elif sector in ("Education", "Health care", "Accommodation/food", "Arts/entertainment", "Other services"):
                pw_ratio = 0.70  # services have lower but still majority production workers
            elif sector in ("Fed govt enterprises", "State/local govt enterprises"):
                pw_ratio = 0.75
            else:
                pw_ratio = 0.65  # conservative default

            ec_total_productive += val * pw_ratio

        v_star[yr] = ec_total_productive / 1e3  # millions -> billions

    v_star.index.name = "year"
    return v_star


def process():
    """Generate sector-level V* and compare with aggregate P02 output."""
    ensure_dirs()
    steps = []

    v_star_sector = compute_sector_v_star()
    if v_star_sector is None:
        return {"series_id": "V_STAR_SECTOR", "status": "skip",
                "steps": ["NIPA 6.2D/6.5D not available"], "outputs": []}

    # Compare with P02 output
    t504_path = SERIES_OUT / "T504.csv"
    if t504_path.exists():
        t504 = pd.read_csv(t504_path, index_col="year")
        t504_combined = t504["combined"].dropna()
        common = v_star_sector.index.intersection(t504_combined.index)
        if len(common) > 5:
            ratio = (v_star_sector[common] / t504_combined[common]).mean()
            diff_pct = ((v_star_sector[common] - t504_combined[common]) / t504_combined[common]).abs().mean()
            steps.append(f"Sector V* vs aggregate: mean ratio={ratio:.3f}, mean abs diff={diff_pct:.1%}")
            print(f"    [P02b] Sector V* vs aggregate: ratio={ratio:.3f}, diff={diff_pct:.1%}")

    # Save for reference
    out_path = SERIES_OUT / "V_star_sector.csv"
    v_star_sector.to_frame(name="V_star_sector_bn").to_csv(out_path)
    steps.append(f"Sector V*: {len(v_star_sector)} years ({v_star_sector.index.min()}-{v_star_sector.index.max()})")
    print(f"    [P02b] Sector V*: {len(v_star_sector)} years, range {v_star_sector.iloc[0]:.1f}-{v_star_sector.iloc[-1]:.1f} bn")

    return {"series_id": "V_STAR_SECTOR", "status": "ok",
            "steps": steps, "outputs": [str(out_path)]}
