"""E_S517_gross_vs_net.py — VPR exploration script.

Compares S517 (Productive Capital Stock K*) under net-stock vs gross-stock
methodologies, per book Table 5.8 ambiguity (book text says "gross", current
S517 implementation uses BEA Fixed Assets Table 4.1 net stock).

Inputs:
  - data/raw/Inputs/API_Data/BEA/fixed_assets_4_1_net_stock.csv (Line 1, current $)
  - data/raw/Inputs/API_Data/BEA/fixed_assets_4_2_gross_stock.csv (Line 1, Fisher Quantity Index)

Notes on BEA data availability:
  BEA Fixed Assets does NOT publish a current-cost GROSS stock series for
  private nonresidential fixed assets. The closest gross-form data available are:
    - Table 4.2: chain-type Fisher quantity indexes (real, dimensionless)
    - Historical-cost net (FAAt403) — different vintage convention
  See VPR doc for the resulting interpretive constraint.

Output:
  - data/scratch/S517_gross_vs_net.csv
    columns = [year, net_stock_bn, gross_quantity_index, implied_gross_stock_bn, ratio_net_to_implied_gross]
"""
from __future__ import annotations
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # bundle root
NET_CSV = PROJECT_ROOT / "data/raw/Inputs/API_Data/BEA/fixed_assets_4_1_net_stock.csv"
GROSS_CSV = PROJECT_ROOT / "data/raw/Inputs/API_Data/BEA/fixed_assets_4_2_gross_stock.csv"
OUT_CSV = PROJECT_ROOT / "Technical/data/scratch/S517_gross_vs_net.csv"

# Book reference values (BEA Table 4.1 Line 1 net stock, current dollars, billions)
BOOK_REFERENCE_VALUES = {1925: 126.977, 1948: 291.557, 1958: 551.356,
                         1967: 871.188, 1980: 3800.29, 1989: 6699.84}


def parse_value(s: str) -> float | None:
    s = s.replace(",", "").replace('"', "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_line1(path: Path, value_col_index: int = 8) -> dict[int, float]:
    """Return {year: data_value} for LineNumber=1 rows."""
    out: dict[int, float] = {}
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[2] != "1":
                continue
            try:
                year = int(row[4])
            except (ValueError, IndexError):
                continue
            val = parse_value(row[value_col_index])
            if val is None:
                continue
            out[year] = val
    return out


def main() -> None:
    # BEA Fixed Assets Table 4.1 reports DataValue in millions of current dollars
    # (UNIT_MULT=6 = "Millions"); convert to billions to match book convention.
    net_raw = load_line1(NET_CSV)
    net = {y: v / 1000.0 for y, v in net_raw.items()}
    gross_idx = load_line1(GROSS_CSV)  # Fisher quantity index (dimensionless)
    years = sorted(set(net) & set(gross_idx))
    if not years:
        raise RuntimeError("No overlapping years")
    print(f"Year range: {years[0]}-{years[-1]} ({len(years)} years)")

    # Implied gross stock in current dollars:
    # We use the gross quantity index normalized to a base year where book
    # gross ≈ net (BEA convention: 2017 = 100 typically). Without an
    # independent current-$ gross level anchor, we anchor the gross series
    # so its 1948 value matches the 1948 net level. This gives a HYPOTHETICAL
    # gross series whose *dynamics* reflect gross-stock growth (faster than
    # net during periods of low scrappage / long service lives) but whose
    # *level* matches net at the anchor year.
    anchor_year = 1948
    if anchor_year not in years:
        anchor_year = years[0]
    anchor_net = net[anchor_year]
    anchor_idx = gross_idx[anchor_year]
    scale = anchor_net / anchor_idx  # bn$ per index unit at anchor

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "net_stock_bn", "gross_quantity_index",
                    "implied_gross_stock_bn_anchored_1948",
                    "ratio_net_to_implied_gross",
                    "book_reference_net_bn", "net_book_pct_diff"])
        for y in years:
            net_v = net[y]
            gi = gross_idx[y]
            implied_gross = gi * scale
            ratio = net_v / implied_gross if implied_gross else None
            book_ref = BOOK_REFERENCE_VALUES.get(y)
            book_pct = (100.0 * (net_v - book_ref) / book_ref) if book_ref else None
            w.writerow([y, f"{net_v:.3f}", f"{gi:.4f}", f"{implied_gross:.3f}",
                        f"{ratio:.4f}" if ratio is not None else "",
                        f"{book_ref:.3f}" if book_ref else "",
                        f"{book_pct:+.2f}" if book_pct is not None else ""])

    # Print summary for book period endpoints
    print("\nBook-period endpoints (1948-1989):")
    print(f"{'year':>6} {'net_bn':>14} {'gross_idx':>12} {'implied_gross_bn':>20} {'ratio':>8} {'book_ref':>12} {'pct_diff':>10}")
    for y in (1948, 1958, 1967, 1980, 1989):
        if y in years:
            net_v = net[y]; gi = gross_idx[y]; ig = gi * scale
            ratio = net_v / ig
            br = BOOK_REFERENCE_VALUES.get(y, 0.0)
            pct = 100.0 * (net_v - br) / br if br else 0.0
            print(f"{y:>6} {net_v:>14,.2f} {gi:>12.4f} {ig:>20,.2f} {ratio:>8.4f} {br:>12,.2f} {pct:>+10.2f}%")

    print(f"\nAnchor: {anchor_year} (scale = {scale:.4f} bn$/idx)")
    print(f"\nWrote {OUT_CSV}")


if __name__ == "__main__":
    main()
