#!/usr/bin/env python3
"""O01 - Generate Publication Figures: standalone SVG/PNG for key book figures.

Produces publication-quality figures using matplotlib for the main empirical
findings from Shaikh & Tonak (1994), extended through 2024.

Output: Outputs/Figures/Fig_X_Y.png (+ .svg if available)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

from utils.paths import SERIES_OUT, STUDIES_OUT

OUTPUT_DIR = Path("D:/Arcanum/Projects/ST2/Outputs/Figures")

BOOK_COLOR = "#3c8dbc"      # Blue for book period
EXT_COLOR = "#f39c12"       # Orange for extension
SPLICE_COLOR = "#605ca8"    # Purple for splice year
GRID_COLOR = "#e0e0e0"


def _load_series(sid):
    """Load a series and return book + combined as separate Series."""
    path = SERIES_OUT / f"{sid}.csv"
    if not path.exists():
        return None, None
    df = pd.read_csv(path, index_col=0)
    book = df["book"].dropna() if "book" in df.columns else pd.Series(dtype=float)
    combined = df["combined"].dropna() if "combined" in df.columns else book
    return book, combined


def _make_figure(title, ylabel, series_list, output_name, splice_year=1989):
    """Create a standard figure with book period + extension."""
    fig, ax = plt.subplots(figsize=(10, 6))

    for label, sid, style in series_list:
        book, combined = _load_series(sid)
        if combined is None:
            continue

        # Book period
        book_data = combined[combined.index <= splice_year]
        ext_data = combined[combined.index >= splice_year]

        ax.plot(book_data.index, book_data.values,
                color=BOOK_COLOR, linewidth=2, label=f"{label} (book)")
        if len(ext_data) > 1:
            ax.plot(ext_data.index, ext_data.values,
                    color=EXT_COLOR, linewidth=2, linestyle=style,
                    label=f"{label} (extended)")

    ax.axvline(x=splice_year, color=SPLICE_COLOR, linestyle="--",
               alpha=0.5, label=f"Splice year ({splice_year})")

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    ax.set_xlim(1948, 2025)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f"{output_name}.png", dpi=150)
    try:
        fig.savefig(OUTPUT_DIR / f"{output_name}.svg")
    except Exception:
        pass
    plt.close(fig)
    print(f"  {output_name}: saved")


def generate():
    if not HAS_MPL:
        print("  matplotlib not available — skipping figure generation")
        return {"status": "skip", "reason": "matplotlib not installed"}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    # Fig 5.5: Rate of Exploitation (e = S*/V*)
    _make_figure(
        "Figure 5.5: Rate of Exploitation (e = S*/V*), 1948-2024",
        "Rate of Surplus Value",
        [("e = S*/V*", "T506", "-")],
        "Fig_5_5_exploitation_rate",
    )
    count += 1

    # Fig 5.6: Productive Labor Share (Lp/L) and Wage Share (V*/W)
    _make_figure(
        "Figure 5.6: Productive Labor and Wage Shares, 1948-2024",
        "Share (0-1)",
        [("Lp/L", "T511", "-"), ("V*/W", "T512", "--")],
        "Fig_5_6_labor_wage_shares",
    )
    count += 1

    # Fig 5.7: Profit Rates
    _make_figure(
        "Figure 5.7: Marxian Profit Rates, 1948-2024",
        "Rate of Profit",
        [("r*", "T513", "-"), ("r* (adj)", "T514", "--")],
        "Fig_5_7_profit_rates",
    )
    count += 1

    # Fig 5.8: Employment
    _make_figure(
        "Figure 5.8: Productive and Unproductive Employment, 1948-2024",
        "Employment (thousands)",
        [("Productive (Lp)", "T515", "-"), ("Unproductive (Lu)", "T516", "--")],
        "Fig_5_8_employment",
    )
    count += 1

    # Fig 5.4: Surplus Ratio
    _make_figure(
        "Figure 5.4: Surplus Ratio S*/(S*+V*), 1948-2024",
        "Surplus Ratio",
        [("S*/(S*+V*)", "T507", "-")],
        "Fig_5_4_surplus_ratio",
    )
    count += 1

    # Fig 9.1: Summary — exploitation + labor share
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    _, e = _load_series("T506")
    _, lpl = _load_series("T511")

    if e is not None:
        book_e = e[e.index <= 1989]
        ext_e = e[e.index >= 1989]
        ax1.plot(book_e.index, book_e, color=BOOK_COLOR, lw=2, label="Book")
        ax1.plot(ext_e.index, ext_e, color=EXT_COLOR, lw=2, label="Extended")
        ax1.axvline(1989, color=SPLICE_COLOR, ls="--", alpha=0.5)
        ax1.set_title("Rate of Exploitation (e)", fontweight="bold")
        ax1.set_ylabel("e = S*/V*")
        ax1.legend()
        ax1.grid(True, color=GRID_COLOR, alpha=0.7)

    if lpl is not None:
        book_l = lpl[lpl.index <= 1989]
        ext_l = lpl[lpl.index >= 1989]
        ax2.plot(book_l.index, book_l, color=BOOK_COLOR, lw=2, label="Book")
        ax2.plot(ext_l.index, ext_l, color=EXT_COLOR, lw=2, label="Extended")
        ax2.axvline(1989, color=SPLICE_COLOR, ls="--", alpha=0.5)
        ax2.set_title("Productive Labor Share (Lp/L)", fontweight="bold")
        ax2.set_ylabel("Lp/L")
        ax2.legend()
        ax2.grid(True, color=GRID_COLOR, alpha=0.7)

    fig.suptitle("Figure 9.1: Key Marxian Indicators, 1948-2024", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_9_1_summary.png", dpi=150)
    plt.close(fig)
    count += 1
    print("  Fig_9_1_summary: saved")

    # Fig 6.1: Net Social Wage with components
    _make_figure(
        "Figure 6.1: Net Social Wage (NSW = B_w + G_w - T_w), 1952-2025",
        "Billions $",
        [("NSW", "T607", "-")],
        "Fig_6_1_net_social_wage",
        splice_year=1989,
    )
    count += 1

    # Fig 6.4: NSW Tax vs Benefit
    fig, ax = plt.subplots(figsize=(10, 6))
    _, t604 = _load_series("T604")
    _, t605 = _load_series("T605")
    _, t607 = _load_series("T607")
    if t604 is not None:
        ax.plot(t604.index, t604, color="#e74c3c", lw=2, label="Total Taxes (T_w)")
    if t605 is not None:
        ax.plot(t605.index, t605, color="#2ecc71", lw=2, label="Benefits (B_w)")
    if t607 is not None:
        ax.plot(t607.index, t607, color=BOOK_COLOR, lw=2, label="NSW")
        ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Figure 6.4: NSW Components — Taxes vs Benefits", fontsize=14, fontweight="bold")
    ax.set_ylabel("Billions $", fontsize=12)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_6_4_nsw_components.png", dpi=150)
    plt.close(fig)
    print("  Fig_6_4_nsw_components: saved")
    count += 1

    # Fig cross-study: NSW comparison across studies
    fig, ax = plt.subplots(figsize=(12, 6))
    study_colors = ["#3c8dbc", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
    study_data = [
        ("ST 1994 NSW/V*", "T608", SERIES_OUT),
        ("Moos NSW/GDP", "N1301", STUDIES_OUT),
        ("Turkey NSW/GDP", "N1602", STUDIES_OUT),
    ]
    for i, (label, sid, base) in enumerate(study_data):
        path = base / f"{sid}.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            col = "combined" if "combined" in df.columns else df.columns[0]
            ax.plot(df.index, df[col], color=study_colors[i % len(study_colors)], lw=2, label=label)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Cross-Study NSW Comparison", fontsize=14, fontweight="bold")
    ax.set_ylabel("Ratio", fontsize=12)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_cross_study_nsw.png", dpi=150)
    plt.close(fig)
    print("  Fig_cross_study_nsw: saved")
    count += 1

    # Fig ST vs Mohun exploitation rates
    fig, ax = plt.subplots(figsize=(10, 6))
    _, t506 = _load_series("T506")
    n1401_path = STUDIES_OUT / "N1401.csv"
    if t506 is not None:
        ax.plot(t506.index, t506, color=BOOK_COLOR, lw=2, label="ST classification")
    if n1401_path.exists():
        df = pd.read_csv(n1401_path, index_col=0)
        ax.plot(df.index, df["combined"], color="#e74c3c", lw=2, label="Mohun classification")
    ax.set_title("Exploitation Rate: Shaikh-Tonak vs Mohun Classification", fontsize=14, fontweight="bold")
    ax.set_ylabel("e = S*/V*", fontsize=12)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_st_vs_mohun.png", dpi=150)
    plt.close(fig)
    print("  Fig_st_vs_mohun: saved")
    count += 1

    # Fig Moos structural shift
    fig, ax = plt.subplots(figsize=(10, 6))
    n1301_path = STUDIES_OUT / "N1301.csv"
    if n1301_path.exists():
        df = pd.read_csv(n1301_path, index_col=0)
        nsw = df["combined"]
        pre = nsw[nsw.index <= 2000]
        post = nsw[nsw.index > 2000]
        ax.plot(pre.index, pre, color=BOOK_COLOR, lw=2, label="Pre-2000")
        ax.plot(post.index, post, color="#e74c3c", lw=2, label="Post-2000")
        ax.axhline(float(pre.mean()), color=BOOK_COLOR, ls="--", alpha=0.5, label=f"Pre mean: {float(pre.mean()):.4f}")
        ax.axhline(float(post.mean()), color="#e74c3c", ls="--", alpha=0.5, label=f"Post mean: {float(post.mean()):.4f}")
        ax.axvline(2000, color=SPLICE_COLOR, ls="--", alpha=0.5)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Moos (2017): Post-2000 Structural Shift in NSW/GDP", fontsize=14, fontweight="bold")
    ax.set_ylabel("NSW/GDP", fontsize=12)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_moos_structural_shift.png", dpi=150)
    plt.close(fig)
    print("  Fig_moos_structural_shift: saved")
    count += 1

    print(f"\n  Total: {count} figures generated")
    return {"status": "ok", "figures": count}


if __name__ == "__main__":
    generate()
