"""P02_S513 — Compute Marxian Profit Rate r* (stock-form primary, flow-form secondary).

v1.2 Iter 3 (2026-05-24): Stock-form r* = S* / (K* + V*) adopted as PRIMARY across
the full 1948-2024 span per `docs/variants/VPR_S513_stock_vs_flow_DECISION_BRIEF.md`
(HIGH confidence). The book canonical form per §5.5 p.122 is the stock form; the
prior published splice (book stock + EXT flow) silently switched denominators at
1989 and reversed the secular sign (+24%). Stock-form restores book-faithful
TRPF decline (-59% 1948-2024) consistent with §5.5 / Ch.9 narrative.

Four subseries written to data/final/S513.csv:

  - S513-A         : Book-period r* = S505-A / (S517-A + S504-A)
                     stock form, 1948-1989. UNCHANGED from prior implementation
                     because book-period data was already stock-form (the prior
                     EXT block was the only flow-form computation, which is
                     deprecated as primary in v1.2 Iter 3).
                     stage=book_period_derived
  - S513-EXT       : Extension r* = S505-COMBINED / (S517-COMBINED + S504-COMBINED)
                     stock form, post-1989. SAME formula as S513-A.
                     stage=extension
  - S513-COMBINED  : Concatenation of S513-A (1948-1989) + S513-EXT (post-1989).
                     Single formula across full span; no form-change splice.
                     stage=book_period | extension per source
  - S513-FLOW      : SECONDARY (reference) flow-form r* = S505-COMBINED /
                     (S502-COMBINED + S504-COMBINED), full span where defined.
                     Retained for variant comparison and continuity with
                     pre-v1.2 published values. Marked `_secondary: true` in
                     registry; not part of the headline narrative.
                     stage=secondary_variant

Upstream dependencies (parallel cohort 3):
  - data/final/S505.csv must contain S505-COMBINED (written by P02_S505)
  - data/final/S517.csv must contain S517-COMBINED (written by P02_S517)
  - data/final/S504.csv must contain S504-COMBINED (written by P02_S504)
  - data/final/S502.csv must contain S502-COMBINED (written by P02_S502)
                       — required only for the secondary S513-FLOW subseries.

If S517-COMBINED or S505-COMBINED is missing any post-1989 year (e.g. the
1990-1997 SIC→NAICS bridge gap), the corresponding S513-EXT year is left out
of the output. Anti-fabrication: no interpolation, no growth-rate splice.

References:
  - docs/variants/VPR_S513_stock_vs_flow.md
  - docs/variants/VPR_S513_stock_vs_flow_DECISION_BRIEF.md
  - Shaikh & Tonak (1994), Measuring the Wealth of Nations, §5.5 p.122 + fn.16
  - Book Table 5.11 (Marxian rate of profit r*, 1948-1989, stock form)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S513"


def _load_combined(sid: str) -> pd.DataFrame:
    """Load the -COMBINED subseries of an upstream P02 output."""
    path = DATA_FINAL / f"{sid}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Upstream {path} missing.")
    df = pd.read_csv(path)
    combined_id = f"{sid}-COMBINED"
    if combined_id not in df["series_id"].unique():
        raise RuntimeError(f"{combined_id} subseries not present in {path.name}.")
    return df[df["series_id"] == combined_id][["year", "value"]].copy()


def _load_subseries(sid: str, subseries_id: str) -> pd.DataFrame:
    path = DATA_FINAL / f"{sid}.csv"
    df = pd.read_csv(path)
    return df[df["series_id"] == subseries_id][["year", "value"]].copy()


def _book_period_frame() -> pd.DataFrame:
    """Stock-form r* = S505-A / (S517-A + S504-A) over 1948-1989."""
    s505 = _load_subseries("S505", "S505-A").rename(columns={"value": "S_star"})
    s504 = _load_subseries("S504", "S504-A").rename(columns={"value": "V_star"})
    s517 = _load_subseries("S517", "S517-A").rename(columns={"value": "K_star"})
    merged = (
        s505.merge(s504, on="year")
            .merge(s517, on="year")
            .sort_values("year")
            .reset_index(drop=True)
    )
    merged["value"]      = merged["S_star"] / (merged["K_star"] + merged["V_star"])
    merged["series_id"]  = "S513-A"
    merged["units"]      = "rate"
    merged["stage"]      = "book_period_derived"
    merged["provenance"] = "Stock-form r* = S505-A / (S517-A + S504-A); Book Table 5.11 / §5.5"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def _extension_frame_stock() -> tuple[pd.DataFrame, dict]:
    """Stock-form extension r* = S505-COMBINED / (S517-COMBINED + S504-COMBINED), post-1989."""
    s505 = _load_combined("S505").rename(columns={"value": "S_star"})
    s517 = _load_combined("S517").rename(columns={"value": "K_star"})
    s504 = _load_combined("S504").rename(columns={"value": "V_star"})

    merged = (
        s505.merge(s517, on="year")
            .merge(s504, on="year")
            .sort_values("year")
            .reset_index(drop=True)
    )
    merged = merged[merged["year"] > 1989].copy()
    # Anti-fabrication: drop any row where a component is NaN (e.g. 1990-1997 gap).
    pre_drop_n = len(merged)
    merged = merged.dropna(subset=["S_star", "K_star", "V_star"]).reset_index(drop=True)
    dropped = pre_drop_n - len(merged)

    if merged.empty:
        raise RuntimeError(
            "Upstream EXT incomplete for stock-form: "
            "S505/S517/S504 -COMBINED produced no overlapping post-1989 years."
        )

    merged["value"]      = merged["S_star"] / (merged["K_star"] + merged["V_star"])
    merged["series_id"]  = "S513-EXT"
    merged["units"]      = "rate"
    merged["stage"]      = "extension"
    merged["provenance"] = (
        "Stock-form r* = S505-COMBINED / (S517-COMBINED + S504-COMBINED); "
        "v1.2 Iter 3 stock-form primary adoption"
    )
    out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]
    diag = {
        "n_rows": len(out),
        "dropped_nan_years": dropped,
        "period": (int(out["year"].min()), int(out["year"].max())) if not out.empty else None,
        "first":  float(out.iloc[0]["value"])  if not out.empty else None,
        "last":   float(out.iloc[-1]["value"]) if not out.empty else None,
    }
    return out, diag


def _flow_frame_secondary() -> tuple[pd.DataFrame, dict]:
    """SECONDARY flow-form r* = S505-COMBINED / (S502-COMBINED + S504-COMBINED), full span.

    Retained as variant subseries for reference and continuity with pre-v1.2
    published values. NOT the primary headline; see DECISION_BRIEF §5.
    """
    s505 = _load_combined("S505").rename(columns={"value": "S_star"})
    s502 = _load_combined("S502").rename(columns={"value": "C_star"})
    s504 = _load_combined("S504").rename(columns={"value": "V_star"})

    merged = (
        s505.merge(s502, on="year")
            .merge(s504, on="year")
            .sort_values("year")
            .reset_index(drop=True)
    )
    pre_drop_n = len(merged)
    merged = merged.dropna(subset=["S_star", "C_star", "V_star"]).reset_index(drop=True)
    dropped = pre_drop_n - len(merged)

    if merged.empty:
        raise RuntimeError("Upstream insufficient for S513-FLOW secondary subseries.")

    merged["value"]      = merged["S_star"] / (merged["C_star"] + merged["V_star"])
    merged["series_id"]  = "S513-FLOW"
    merged["units"]      = "rate"
    merged["stage"]      = "secondary_variant"
    merged["provenance"] = (
        "SECONDARY flow-form r* = S505-COMBINED / (S502-COMBINED + S504-COMBINED); "
        "retained as reference variant, NOT primary (see VPR_S513_stock_vs_flow_DECISION_BRIEF)"
    )
    out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]
    diag = {
        "n_rows": len(out),
        "dropped_nan_years": dropped,
        "period": (int(out["year"].min()), int(out["year"].max())) if not out.empty else None,
    }
    return out, diag


def _combined_frame(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    """S513-COMBINED = S513-A (1948-1989) concatenated with S513-EXT (post-1989).

    Both arms share identical stock-form formula; no form-change splice.
    """
    a = book_df[book_df["series_id"] == "S513-A"][["year", "value", "provenance"]].copy()
    a["series_id"] = "S513-COMBINED"
    a["stage"]     = "book_period"

    e = ext_df[ext_df["series_id"] == "S513-EXT"][["year", "value", "provenance"]].copy()
    e = e[e["year"] > 1989].copy()
    e["series_id"] = "S513-COMBINED"
    e["stage"]     = "extension"

    out = pd.concat([a, e], ignore_index=True, sort=False)
    out["units"] = "rate"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    book = _book_period_frame()
    frames = [book]
    try:
        ext, ext_diag = _extension_frame_stock()
        combined = _combined_frame(book, ext)
        frames.extend([ext, combined])
        print(f"    [P02_S513] stock-form extension diag: {ext_diag}")
    except Exception as exc:
        print(f"    [P02_S513] STOCK-FORM EXTENSION DEFERRED: {exc!r}")
        ext = None

    try:
        flow, flow_diag = _flow_frame_secondary()
        frames.append(flow)
        print(f"    [P02_S513] flow-form (secondary) diag: {flow_diag}")
    except Exception as exc:
        print(f"    [P02_S513] FLOW SECONDARY DEFERRED: {exc!r}")

    df = pd.concat(frames, ignore_index=True, sort=False)
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(
        f"    [P02_S513] {len(df)} rows; subseries: "
        f"{sorted(df['series_id'].unique())}; wrote {final_path.name}"
    )
    return df


if __name__ == "__main__":
    run()
