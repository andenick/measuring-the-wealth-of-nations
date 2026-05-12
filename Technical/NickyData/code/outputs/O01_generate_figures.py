#!/usr/bin/env python3
"""O01 - Generate Publication Figures.

Same-color book/extension (solid vs dotted). No figure numbers in titles
(LaTeX captions handle numbering).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

from utils.paths import SERIES_OUT, STUDIES_OUT

OUTPUT_DIR = Path("D:/Arcanum/Projects/ST2/Outputs/Figures")

COLORS = ["#3c8dbc", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
SPLICE_COLOR = "#a0a0a0"
GRID_COLOR = "#e8e8e8"


def _load_series(sid):
    path = SERIES_OUT / f"{sid}.csv"
    if not path.exists():
        return None, None
    df = pd.read_csv(path, index_col=0)
    book = df["book"].dropna() if "book" in df.columns else pd.Series(dtype=float)
    combined = df["combined"].dropna() if "combined" in df.columns else book
    return book, combined


def _make_figure(title, ylabel, series_list, output_name, splice_year=1989):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (label, sid, _) in enumerate(series_list):
        book, combined = _load_series(sid)
        if combined is None:
            continue

        color = COLORS[i % len(COLORS)]
        book_data = combined[combined.index <= splice_year]
        ext_data = combined[combined.index >= splice_year]

        ax.plot(book_data.index, book_data.values,
                color=color, linewidth=2.5, solid_capstyle="round",
                label=f"{label}")
        if len(ext_data) > 1:
            ax.plot(ext_data.index, ext_data.values,
                    color=color, linewidth=2, linestyle=":",
                    label=f"{label} (1990–2024)")

    ax.axvline(x=splice_year, color=SPLICE_COLOR, linestyle="--",
               alpha=0.4, linewidth=1)

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.legend(loc="best", fontsize=9, framealpha=0.9)
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
        return {"status": "skip", "reason": "matplotlib not installed"}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    # Exploitation rate
    _make_figure(
        "Rate of Exploitation (e = S*/V*), 1948–2024",
        "Rate of Surplus Value",
        [("e = S*/V*", "T506", "-")],
        "Fig_5_5_exploitation_rate",
    )
    count += 1

    # Labor and wage shares
    _make_figure(
        "Productive Labor and Wage Shares, 1948–2024",
        "Share (0–1)",
        [("Lp/L", "T511", "-"), ("V*/W", "T512", "--")],
        "Fig_5_6_labor_wage_shares",
    )
    count += 1

    # Profit rates
    _make_figure(
        "Marxian Profit Rates, 1948–2024",
        "Rate of Profit",
        [("r*", "T513", "-"), ("r* (capacity-adj)", "T514", "--")],
        "Fig_5_7_profit_rates",
    )
    count += 1

    # Employment
    _make_figure(
        "Productive and Unproductive Employment, 1948–2024",
        "Employment (thousands)",
        [("Productive (Lp)", "T515", "-"), ("Unproductive (Lu)", "T516", "--")],
        "Fig_5_8_employment",
    )
    count += 1

    # Surplus ratio
    _make_figure(
        "Surplus Ratio S*/(S*+V*), 1948–2024",
        "Surplus Ratio",
        [("S*/(S*+V*)", "T507", "-")],
        "Fig_5_4_surplus_ratio",
    )
    count += 1

    # Summary (2-panel)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    _, e = _load_series("T506")
    _, lpl = _load_series("T511")

    if e is not None:
        book_e = e[e.index <= 1989]
        ext_e = e[e.index >= 1989]
        ax1.plot(book_e.index, book_e, color=COLORS[0], lw=2.5, label="1948–1989")
        ax1.plot(ext_e.index, ext_e, color=COLORS[0], lw=2, ls=":", label="1990–2024")
        ax1.axvline(1989, color=SPLICE_COLOR, ls="--", alpha=0.4)
        ax1.set_title("Rate of Exploitation (e)", fontweight="bold")
        ax1.set_ylabel("e = S*/V*")
        ax1.legend(fontsize=9)
        ax1.grid(True, color=GRID_COLOR, alpha=0.7)

    if lpl is not None:
        book_l = lpl[lpl.index <= 1989]
        ext_l = lpl[lpl.index >= 1989]
        ax2.plot(book_l.index, book_l, color=COLORS[0], lw=2.5, label="1948–1989")
        ax2.plot(ext_l.index, ext_l, color=COLORS[0], lw=2, ls=":", label="1990–2024")
        ax2.axvline(1989, color=SPLICE_COLOR, ls="--", alpha=0.4)
        ax2.set_title("Productive Labor Share (Lp/L)", fontweight="bold")
        ax2.set_ylabel("Lp/L")
        ax2.legend(fontsize=9)
        ax2.grid(True, color=GRID_COLOR, alpha=0.7)

    fig.suptitle("Key Marxian Indicators, 1948–2024", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_9_1_summary.png", dpi=150)
    plt.close(fig)
    count += 1
    print("  Fig_9_1_summary: saved")

    # NSW
    _make_figure(
        "Net Social Wage (NSW = B_w + G_w – T_w), 1952–2025",
        "Billions $",
        [("NSW", "T607", "-")],
        "Fig_6_1_net_social_wage",
        splice_year=1989,
    )
    count += 1

    # NSW Components
    fig, ax = plt.subplots(figsize=(10, 6))
    _, t604 = _load_series("T604")
    _, t605 = _load_series("T605")
    _, t607 = _load_series("T607")
    if t604 is not None:
        ax.plot(t604.index, t604, color=COLORS[1], lw=2, label="Total Taxes (T_w)")
    if t605 is not None:
        ax.plot(t605.index, t605, color=COLORS[2], lw=2, label="Benefits (B_w)")
    if t607 is not None:
        ax.plot(t607.index, t607, color=COLORS[0], lw=2, label="NSW")
        ax.axhline(0, color="black", lw=0.5)
    ax.set_title("NSW Components — Taxes vs Benefits", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Billions $", fontsize=11)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_6_4_nsw_components.png", dpi=150)
    plt.close(fig)
    print("  Fig_6_4_nsw_components: saved")
    count += 1

    # Cross-study NSW
    fig, ax = plt.subplots(figsize=(12, 6))
    study_data = [
        ("ST 1994 NSW/V*", "T608", SERIES_OUT),
        ("Moos NSW/NI", "N1301", STUDIES_OUT),
        ("Turkey NSW/GDP", "N1602", STUDIES_OUT),
    ]
    for i, (label, sid, base) in enumerate(study_data):
        path = base / f"{sid}.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            col = "combined" if "combined" in df.columns else df.columns[0]
            ax.plot(df.index, df[col], color=COLORS[i], lw=2, label=label)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Cross-Study NSW Comparison", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Ratio", fontsize=11)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_cross_study_nsw.png", dpi=150)
    plt.close(fig)
    print("  Fig_cross_study_nsw: saved")
    count += 1

    # ST vs Mohun exploitation
    fig, ax = plt.subplots(figsize=(10, 6))
    _, t506 = _load_series("T506")
    n1401_path = STUDIES_OUT / "N1401.csv"
    if t506 is not None:
        ax.plot(t506.index, t506, color=COLORS[0], lw=2, label="Shaikh-Tonak classification")
    if n1401_path.exists():
        df = pd.read_csv(n1401_path, index_col=0)
        ax.plot(df.index, df["combined"], color=COLORS[1], lw=2, label="Mohun classification")
    ax.set_title("Exploitation Rate: Shaikh-Tonak vs Mohun", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("e = S*/V*", fontsize=11)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, color=GRID_COLOR, alpha=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "Fig_st_vs_mohun.png", dpi=150)
    plt.close(fig)
    print("  Fig_st_vs_mohun: saved")
    count += 1

    # Moos structural shift
    fig, ax = plt.subplots(figsize=(10, 6))
    n1301_path = STUDIES_OUT / "N1301.csv"
    if n1301_path.exists():
        df = pd.read_csv(n1301_path, index_col=0)
        nsw = df["combined"]
        pre = nsw[nsw.index <= 2000]
        post = nsw[nsw.index > 2000]
        ax.plot(pre.index, pre, color=COLORS[0], lw=2, label="Pre-2000")
        ax.plot(post.index, post, color=COLORS[1], lw=2, label="Post-2000")
        ax.axhline(float(pre.mean()), color=COLORS[0], ls="--", alpha=0.5,
                   label=f"Pre mean: {float(pre.mean()):.4f}")
        ax.axhline(float(post.mean()), color=COLORS[1], ls="--", alpha=0.5,
                   label=f"Post mean: {float(post.mean()):.4f}")
        ax.axvline(2000, color=SPLICE_COLOR, ls="--", alpha=0.4)
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title("Moos (2017): Post-2000 Structural Shift in NSW/NI", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("NSW/NI", fontsize=11)
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
