"""P02_S514 - Capacity-adjusted Marxian profit rate: r*' = r* / u (DIVIDE).

D1 DECISION (2026-07-02): adopt the BOOK'S operation. Shaikh & Tonak (1994)
Table 5.8 defines the utilization-adjusted rate verbatim as

    r*' = r*/u      (equivalently r*' = S*/(K*.u))

i.e. the profit rate is DIVIDED by capacity utilization u, NOT multiplied by
it. Book prose (Ch.5 p.124, KB v2): "the mass of profit is divided by the rate
of capacity utilization, analogous to how actual output is divided by capacity
utilization to estimate potential output." u is a FRACTION (0-1); u=1 is
normal/full capacity. Dividing by u<1 scales the rate UP toward its
normal-capacity level.

This REPLACES the prior (v1.2) implementation r*_adj = r* x TCU/100, which
multiplied by utilization and therefore ran well BELOW the book's r*' (e.g.
1989: old 0.31 vs book 0.39). The old multiplied series is retained as a
clearly-labelled DEPRECATED comparison arm (S514-AMULT) per the two-arm rule.

u source, by arm (D1):
  * Book period 1948-1989 -> the book's OWN u (Shaikh 1992a, Table 5.8),
    a fraction. This reproduces the book's r*' row as closely as the build's
    r* (S513-A) allows. Full 1948-1989 coverage (no pre-1967 NaN gap anymore).
  * Extension 1990-2024 -> FRED TCU/100 (the book's Shaikh-1992 series ends
    1989). Source change at the 1989/1990 seam is documented (DIV).

Subseries written to data/final/S514.csv:
  - S514-A         : PRIMARY book-period r*' = S513-A / u_book, 1948-1989,
                     stage=book_period_derived. Benchmarked vs book r*'
                     (Table 5.8). Residual vs book (later years) reflects the
                     build's r*=S*/(K_net+V*) differing from the book's
                     r*=S*/K*_gross (the S517 gross-vs-net gap, D2) -> registered
                     divergence, NOT a construction error.
  - S514-EXT       : Extension r*' = S513-EXT / (FRED TCU/100), 1990-2024,
                     stage=extension. Anti-lazy-splice: computed fresh per year.
  - S514-COMBINED  : 1948-1989 from S514-A; post-1989 from S514-EXT.
  - S514-FLOW      : SECONDARY. r*' = S513-FLOW / (FRED TCU/100). Reference
                     variant (flow-form r*). NOT primary.
  - S514-AMULT     : DEPRECATED comparison arm = S513-A x TCU/100 (the OLD
                     multiply operation), 1967-1989. Retained for transparency
                     ONLY; do not use. stage=deprecated_comparison.

Graceful degradation: if S513.csv lacks S513-EXT (upstream not yet built),
emit book-only and log. If S513-FLOW absent, skip S514-FLOW with a note.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S514_capacity_adj_profit_rate import load_tcu, load_book_u  # noqa: E402
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
    """PRIMARY S514-A = S513-A / u_book (book Shaikh-1992 u), 1948-1989. DIVIDE."""
    s513_a = _load_s513_subseries("S513-A")
    u = load_book_u()
    merged = s513_a.merge(u, on="year", how="left").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["r_star"] / merged["u"]
    merged["series_id"]  = "S514-A"
    merged["units"]      = "rate"
    merged["stage"]      = "book_period_derived"
    merged["provenance"] = (
        "r*' = r*/u = S513-A / u_book (book Shaikh-1992a utilization, Table 5.8); "
        "DIVIDE per book Ch.5 p.124; residual vs book r*' = S517 gross-vs-net gap (D2/DIV)"
    )
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def _amult_deprecated_frame() -> pd.DataFrame:
    """DEPRECATED comparison arm S514-AMULT = S513-A x TCU/100 (old multiply op)."""
    s513_a = _load_s513_subseries("S513-A")
    tcu = load_tcu()
    merged = s513_a.merge(tcu, on="year", how="left").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["r_star"] * (merged["TCU"] / 100)
    merged["series_id"]  = "S514-AMULT"
    merged["units"]      = "rate"
    merged["stage"]      = "deprecated_comparison"
    merged["provenance"] = (
        "DEPRECATED (do not use): OLD operation r*_adj = S513-A x (TCU/100). "
        "Superseded by S514-A (r*'=r*/u) per D1 2026-07-02. Retained for comparison; TCU NaN pre-1967"
    )
    # Keep only rows where TCU exists (1967-1989 in the book period)
    out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]
    return out[(out["year"] <= 1989)].reset_index(drop=True)


def _gross_book_frame() -> pd.DataFrame:
    """S514-GROSS-A: book-faithful r*' = r*_gross / u_book, 1948-1989. DIVIDE.

    F2 (2026-07-07) book-period GROSS variant. Divides the book-faithful gross
    r* (S513-GROSS-A) by the book's own u (Table 5.8), reproducing the book's
    published r*' to MAE ~0.0023 (F2). Book period ONLY; no extension. NOT
    primary (S514-A/-COMBINED, net-based, are unchanged).
    """
    s513_g = _load_s513_subseries("S513-GROSS-A")
    u = load_book_u()
    merged = s513_g.merge(u, on="year", how="left").sort_values("year").reset_index(drop=True)
    merged = merged[(merged["year"] >= 1948) & (merged["year"] <= 1989)].copy()
    merged["value"] = merged["r_star"] / merged["u"]
    merged["series_id"]  = "S514-GROSS-A"
    merged["units"]      = "rate"
    merged["stage"]      = "variant_book_gross"
    merged["provenance"] = (
        "VARIANT book-faithful r*' = S513-GROSS-A / u_book (DIVIDE; book Table 5.8); "
        "= the book's published r*' (reproduces to MAE ~0.0023, F2 2026-07-07). "
        "Book period ONLY, no extension. NOT primary (S514-COMBINED is unchanged)."
    )
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def _extension_frame() -> tuple[pd.DataFrame, dict]:
    """Extension S514-EXT = S513-EXT / (FRED TCU/100), 1990-2024. DIVIDE."""
    s513_ext = _load_s513_subseries("S513-EXT")
    tcu = load_tcu()
    merged = s513_ext.merge(tcu, on="year", how="left").sort_values("year").reset_index(drop=True)
    # Anti-lazy-splice: r*' computed fresh per year as r* / (TCU/100)
    merged["value"] = merged["r_star"] / (merged["TCU"] / 100)
    merged["series_id"]  = "S514-EXT"
    merged["units"]      = "rate"
    merged["stage"]      = "extension"
    merged["provenance"] = (
        "r*' = S513-EXT / (FRED TCU/100); DIVIDE per book Ch.5; "
        "FRED TCU is the constructible u-proxy for the extension (book u ends 1989)"
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
    """SECONDARY S514-FLOW = S513-FLOW / (FRED TCU/100). DIVIDE. Reference variant."""
    try:
        s513_flow = _load_s513_subseries("S513-FLOW")
    except RuntimeError:
        return None, {"skipped": "S513-FLOW absent"}
    tcu = load_tcu()
    merged = s513_flow.merge(tcu, on="year", how="left").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["r_star"] / (merged["TCU"] / 100)
    merged["series_id"]  = "S514-FLOW"
    merged["units"]      = "rate"
    merged["stage"]      = "secondary_variant"
    merged["provenance"] = (
        "SECONDARY r*' = S513-FLOW / (FRED TCU/100); DIVIDE; flow-form reference variant, NOT primary"
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
    amult = _amult_deprecated_frame()
    parts = [book, amult]
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

    try:
        gross = _gross_book_frame()
        parts.append(gross)
        print(f"    [P02_S514] gross-book variant: {len(gross)} rows "
              f"({int(gross['year'].min())}-{int(gross['year'].max())})")
    except Exception as exc:
        print(f"    [P02_S514] GROSS-BOOK VARIANT DEFERRED: {exc!r}")

    df = pd.concat(parts, ignore_index=True, sort=False)
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    n_valid = df["value"].notna().sum()
    print(f"    [P02_S514] wrote {final_path.name} ({len(df)} rows, "
          f"{n_valid} non-NaN; subseries: {sorted(df['series_id'].unique())})")


if __name__ == "__main__":
    run()
