"""E_S513_stock_vs_flow — Parallel stock-form vs flow-form computation of S513 r*.

Problem
-------
S513 (Marxian profit rate r*) currently has a FORM-CHANGE at its 1989 splice:
  - S513-A (1948-1989): r* = S* / (K* + V*)   -- stock form (book Table 5.11)
  - S513-EXT (1998-2024): r* = S* / (C* + V*) -- flow form (registry-prescribed)

Now that S517-EXT (productive capital stock extension) is populated, both forms
are computable across the full 1948-2024 span. This script computes them in
parallel and quantifies the divergence so the splice form-change can be
documented as a methodology variant (per anu-variant), rather than just an
extension-time divergence.

Inputs (all -COMBINED long-format CSVs under data/final/)
---------------------------------------------------------
- S505: S*  (surplus value)
- S502: C*  (constant capital flow, Mp)
- S504: V*  (variable capital)
- S517: K*  (productive capital stock)

Outputs
-------
- Technical/data/scratch/S513_stock_vs_flow.csv (1948..2024, wide):
    [year, S_star, C_star, V_star, K_star, r_flow, r_stock,
     ratio_flow_to_stock, abs_diff]
- Console summary statistics: book-period mean diff, extension-period mean diff,
  max divergence year, sign analysis.

Notes
-----
Pure exploration. Does NOT touch series_registry.json, PIPELINE_STATE, LEDGER,
MANIFEST, or SUBSERIES_PLAN. Output is evidence for VPR_S513_stock_vs_flow.md.
"""
from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FINAL_DIR = PROJECT_ROOT / "data" / "final"
SCRATCH_DIR = PROJECT_ROOT / "data" / "scratch"

BOOK_END_YEAR = 1989
EXT_START_YEAR = 1990  # operational split for summary stats


def load_combined(series_id: str) -> dict[int, float]:
    """Load a single series's -COMBINED rows as {year: value}."""
    path = FINAL_DIR / f"{series_id}.csv"
    target = f"{series_id}-COMBINED"
    out: dict[int, float] = {}
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row["series_id"] != target:
                continue
            year = int(row["year"])
            value = float(row["value"])
            out[year] = value
    if not out:
        raise RuntimeError(f"No -COMBINED rows found for {series_id} at {path}")
    return out


def compute_rows() -> list[dict[str, object]]:
    """Compute r_flow and r_stock for every year all four series cover."""
    s_star = load_combined("S505")
    c_star = load_combined("S502")
    v_star = load_combined("S504")
    k_star = load_combined("S517")

    common = sorted(set(s_star) & set(c_star) & set(v_star) & set(k_star))
    rows: list[dict[str, object]] = []
    for year in common:
        s = s_star[year]
        c = c_star[year]
        v = v_star[year]
        k = k_star[year]
        denom_flow = c + v
        denom_stock = k + v
        r_flow = s / denom_flow if denom_flow else float("nan")
        r_stock = s / denom_stock if denom_stock else float("nan")
        ratio = r_flow / r_stock if r_stock else float("nan")
        abs_diff = r_flow - r_stock
        rows.append({
            "year": year,
            "S_star": s,
            "C_star": c,
            "V_star": v,
            "K_star": k,
            "r_flow": r_flow,
            "r_stock": r_stock,
            "ratio_flow_to_stock": ratio,
            "abs_diff": abs_diff,
        })
    return rows


def write_scratch(rows: list[dict[str, object]]) -> Path:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SCRATCH_DIR / "S513_stock_vs_flow.csv"
    fieldnames = [
        "year", "S_star", "C_star", "V_star", "K_star",
        "r_flow", "r_stock", "ratio_flow_to_stock", "abs_diff",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return out_path


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Compute mean / max / sign-analysis statistics for book and extension periods."""
    def _mean(xs: list[float]) -> float:
        return sum(xs) / len(xs) if xs else float("nan")

    book_rows = [r for r in rows if r["year"] <= BOOK_END_YEAR]
    ext_rows = [r for r in rows if r["year"] >= EXT_START_YEAR]

    book_flow = [float(r["r_flow"]) for r in book_rows]
    book_stock = [float(r["r_stock"]) for r in book_rows]
    book_diff = [float(r["abs_diff"]) for r in book_rows]

    ext_flow = [float(r["r_flow"]) for r in ext_rows]
    ext_stock = [float(r["r_stock"]) for r in ext_rows]
    ext_diff = [float(r["abs_diff"]) for r in ext_rows]

    max_div_row = max(rows, key=lambda r: abs(float(r["abs_diff"])))
    positive_diff = sum(1 for r in rows if float(r["abs_diff"]) > 0)
    negative_diff = sum(1 for r in rows if float(r["abs_diff"]) < 0)

    return {
        "n_book": len(book_rows),
        "n_ext": len(ext_rows),
        "book_mean_r_flow": _mean(book_flow),
        "book_mean_r_stock": _mean(book_stock),
        "book_mean_abs_diff": _mean(book_diff),
        "ext_mean_r_flow": _mean(ext_flow),
        "ext_mean_r_stock": _mean(ext_stock),
        "ext_mean_abs_diff": _mean(ext_diff),
        "max_div_year": max_div_row["year"],
        "max_div_abs_diff": float(max_div_row["abs_diff"]),
        "max_div_r_flow": float(max_div_row["r_flow"]),
        "max_div_r_stock": float(max_div_row["r_stock"]),
        "n_r_flow_gt_r_stock": positive_diff,
        "n_r_flow_lt_r_stock": negative_diff,
    }


def main() -> None:
    rows = compute_rows()
    out_path = write_scratch(rows)
    stats = summarize(rows)

    print(f"Wrote {len(rows)} rows to {out_path}")
    print(f"Year range: {rows[0]['year']}..{rows[-1]['year']}")
    print()
    print("=== Summary: stock-form vs flow-form r* ===")
    print(f"Book period      (<= {BOOK_END_YEAR}): n={stats['n_book']}")
    print(f"  mean r_flow    = {stats['book_mean_r_flow']:.4f}")
    print(f"  mean r_stock   = {stats['book_mean_r_stock']:.4f}")
    print(f"  mean abs_diff  = {stats['book_mean_abs_diff']:.4f}  (r_flow - r_stock)")
    print()
    print(f"Extension period (>= {EXT_START_YEAR}): n={stats['n_ext']}")
    print(f"  mean r_flow    = {stats['ext_mean_r_flow']:.4f}")
    print(f"  mean r_stock   = {stats['ext_mean_r_stock']:.4f}")
    print(f"  mean abs_diff  = {stats['ext_mean_abs_diff']:.4f}  (r_flow - r_stock)")
    print()
    print(f"Max divergence year: {stats['max_div_year']} "
          f"(r_flow={stats['max_div_r_flow']:.4f}, "
          f"r_stock={stats['max_div_r_stock']:.4f}, "
          f"abs_diff={stats['max_div_abs_diff']:.4f})")
    print(f"Sign analysis: r_flow > r_stock in {stats['n_r_flow_gt_r_stock']} years; "
          f"r_flow < r_stock in {stats['n_r_flow_lt_r_stock']} years")


if __name__ == "__main__":
    main()
