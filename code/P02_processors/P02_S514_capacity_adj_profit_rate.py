"""P02_S514 - Capacity-adjusted Marxian profit rate: r*_adj = r* x TCU/100.

Stock-form primary (v1.2 Iter 3, lockstep with P02_S513).

TCU = Federal Reserve total capacity utilization (FRED series TCU).
Available 1967-present; for 1948-1966 (no TCU data), emit NaN per the
no-synthetic-data rule.

Subseries written to data/final/S514.csv:
  - S514-A         : r*_adj using S513-A (book stock-form r*), 1948-1989,
                     stage=book_period_derived. NaN pre-1967 (no TCU).
                     Formula: S513-A x TCU/100.
  - S514-EXT       : r*_adj using S513-EXT (stock-form extended r*),
                     1990-2024, stage=extension. Anti-lazy-splice:
                     computed fresh year by year as S513-EXT_t x TCU_t/100;
                     not a growth-splice of book r*_adj.
                     Coverage gap 1990-1997 inherited from S513-EXT.
  - S514-COMBINED  : 1948-1989 from S514-A; post-1989 from S514-EXT.
  - S514-FLOW      : SECONDARY (_secondary: true). r*_adj using S513-FLOW
                     (flow-form r*) x TCU/100, 1998-2024. Retained as
                     reference variant for cross-check vs v1.1 publication.
                     NOT primary. See VPR_S513_stock_vs_flow_DECISION_BRIEF.

Form-switch rationale (v1.2 Iter 3): S514 cascades S513's form choice.
S513 adopted stock-form primary per book Table 5.11 §5.5 (verbatim
definition: r* = S*/(K*+V*)). v1.1 published a stock-form 1948-1989 +
flow-form 1998-2024 splice that introduced wrong-sign trend artifact;
v1.2 restores book canonical form across the entire 1948-2024 span,
which propagates one-to-one into the TCU-multiplied capacity-adjusted
series here.

Graceful degradation: if S513.csv missing S513-EXT (upstream not yet
built), emit S514-A book-only and log the reason. If S513-FLOW absent,
skip S514-FLOW with a note.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S514_capacity_adj_profit_rate import load_tcu  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S514"


def _load_s513_subseries(subseries_id: str) -> pd.DataFrame:
    path = DATA_FINAL / "S513.csv"
    if not path.exists():
        raise FileNotFoundError(f"S513 final not found at {path}; run P02_S513 first.")
    df = pd.read_csv(path)
    sub = df[df["series_id"] == subseries_id][["year", "value"]].rename(columns={"value": "r_star"})
    if sub.empty:
        raise RuntimeError(f"{subseries_id} subseries empty in {path.name}; cannot derive S514.")
    return sub


def _book_period_frame() -> pd.DataFrame:
    """Stock-form S514-A = S513-A (stock-form book r*) x TCU/100, 1948-1989."""
    s513_a = _load_s513_subseries("S513-A")
    tcu = load_tcu()
    merged = s513_a.merge(tcu, on="year", how="left").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["r_star"] * (merged["TCU"] / 100)
    merged["series_id"]  = "S514-A"
    merged["units"]      = "rate"
    merged["stage"]      = "book_period_derived"
    merged["provenance"] = (
        "Stock-form r*_adj = S513-A (stock) x (TCU/100); "
        "Book Table 5.11; TCU NaN pre-1967"
    )
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def _extension_frame() -> tuple[pd.DataFrame, dict]:
    """Stock-form S514-EXT = S513-EXT (stock-form) x TCU/100, 1990-2024."""
    s513_ext = _load_s513_subseries("S513-EXT")
    tcu = load_tcu()
    merged = s513_ext.merge(tcu, on="year", how="left").sort_values("year").reset_index(drop=True)
    # Anti-lazy-splice: r*_adj computed fresh from extended stock-form r* and TCU
    merged["value"] = merged["r_star"] * (merged["TCU"] / 100)
    merged["series_id"]  = "S514-EXT"
    merged["units"]      = "rate"
    merged["stage"]      = "extension"
    merged["provenance"] = (
        "Stock-form r*_adj = S513-EXT (stock) x (FRED TCU/100); "
        "fresh ratio per year, no growth-splice; v1.2 Iter 3 stock-form primary"
    )
    out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]
    valid = out.dropna(subset=["value"])
    diag = {
        "n_rows":  len(out),
        "n_valid": int(len(valid)),
        "period":  (int(out["year"].min()), int(out["year"].max())) if len(out) else (None, None),
    }
    return out, diag


def _combined_frame(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    a = book_df[book_df["series_id"] == "S514-A"][["year", "value", "provenance"]].copy()
    a["series_id"] = "S514-COMBINED"
    a["stage"]     = "book_period_derived"

    e = ext_df[ext_df["series_id"] == "S514-EXT"][["year", "value", "provenance"]].copy()
    e = e[e["year"] > 1989].copy()
    e["series_id"] = "S514-COMBINED"
    e["stage"]     = "extension"

    out = pd.concat([a, e], ignore_index=True, sort=False)
    out["units"] = "rate"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def _flow_secondary_frame() -> tuple[pd.DataFrame | None, dict]:
    """SECONDARY S514-FLOW = S513-FLOW (flow-form) x TCU/100. Retained as
    reference variant. NOT primary. Skipped silently if S513-FLOW absent.
    """
    try:
        s513_flow = _load_s513_subseries("S513-FLOW")
    except RuntimeError:
        return None, {"skipped": "S513-FLOW absent"}
    tcu = load_tcu()
    merged = s513_flow.merge(tcu, on="year", how="left").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["r_star"] * (merged["TCU"] / 100)
    merged["series_id"]  = "S514-FLOW"
    merged["units"]      = "rate"
    merged["stage"]      = "secondary_variant"
    merged["provenance"] = (
        "SECONDARY flow-form r*_adj = S513-FLOW (flow) x (FRED TCU/100); "
        "retained as reference variant, NOT primary "
        "(see VPR_S513_stock_vs_flow_DECISION_BRIEF)"
    )
    out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]
    valid = out.dropna(subset=["value"])
    diag = {
        "n_rows":  len(out),
        "n_valid": int(len(valid)),
        "period":  (int(out["year"].min()), int(out["year"].max())) if len(out) else (None, None),
    }
    return out, diag


def run():
    book = _book_period_frame()
    parts = [book]
    try:
        ext, diag = _extension_frame()
        combined = _combined_frame(book, ext)
        parts.extend([ext, combined])
        print(f"    [P02_S514] extension diag: {diag}")
    except Exception as exc:
        print(f"    [P02_S514] EXTENSION DEFERRED: {exc!r} - writing book-only")

    flow_df, flow_diag = _flow_secondary_frame()
    if flow_df is not None:
        parts.append(flow_df)
        print(f"    [P02_S514] FLOW secondary diag: {flow_diag}")
    else:
        print(f"    [P02_S514] FLOW secondary skipped: {flow_diag}")

    df = pd.concat(parts, ignore_index=True, sort=False)
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    n_valid = df["value"].notna().sum()
    print(f"    [P02_S514] wrote {final_path.name} ({len(df)} rows, "
          f"{n_valid} non-NaN; subseries: {sorted(df['series_id'].unique())})")


if __name__ == "__main__":
    run()
