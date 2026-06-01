"""P02_S504 — Process Variable Capital (V*).

Four subseries written to data/final/S504.csv:
  - S504-A         : Appendix H.1 V_star, 1948-1989, stage=book_period
  - S504-EXT       : Derived V* = (V*/W) × W
                      * V*/W from S512-EXT (must run P02_S512 first)
                      * W from BEA NIPA T20100 (total compensation, $billions)
                     stage=extension, period 1998-2024 (BEA 6.2D begins 1998)
  - S504-INTERP    : Log-linear interpolation between book(1989) endpoint and
                     BEA(1998) first EXT value, populating 1990-1997.
                     stage=extension_bridge; M04_S504 manual adjustment per
                     BUILD_NARRATIVE.md Stage 5 cohort 3 precedent (S501-S503).
  - S504-COMBINED  : 1948-1989 from S504-A, 1990-1997 from S504-INTERP,
                     1998-2024 from S504-EXT.

Per EPR section 5: V* extended by `derive`, not lazy growth-rate splice.
The 1990-1997 bridge is an honestly-flagged interpolation (NOT raw data);
EXT proper remains BEA-only and does NOT include the interp years.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S504_variable_capital import (  # noqa: E402
    LOADER,
    load_total_compensation,
)
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


BOOK_LAST_YEAR = 1989
EXT_FIRST_YEAR = 1998  # BEA NIPA 6.2D begins 1998


def _log_linear_bridge(book_endpoint: float, ext_endpoint: float,
                       y0: int, y1: int) -> pd.DataFrame:
    """Log-linear interpolation from (y0, book_endpoint) to (y1, ext_endpoint),
    returning rows for years y0+1 .. y1-1 (open interval).

    Mirrors the _log_linear_bridge in P02_S501/S502/S503 — same SIC-NAICS bridge
    precedent (BUILD_NARRATIVE.md Stage 5 cohort 3).
    """
    if book_endpoint <= 0 or ext_endpoint <= 0:
        raise ValueError("log-linear bridge requires positive endpoints")
    n = y1 - y0
    log0 = np.log(book_endpoint)
    log1 = np.log(ext_endpoint)
    rows = []
    for k in range(1, n):  # k=1..n-1 -> years y0+1..y1-1
        frac = k / n
        val = float(np.exp(log0 + frac * (log1 - log0)))
        rows.append({"year": y0 + k, "value": val})
    return pd.DataFrame(rows)


def _book_period_frame() -> pd.DataFrame:
    df = LOADER.load()
    df["stage"]      = "book_period"
    df["provenance"] = "book_tableH1_1948_1989.csv:V_star"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def _extension_frame() -> tuple[pd.DataFrame, dict]:
    s512_path = DATA_FINAL / "S512.csv"
    if not s512_path.exists():
        raise FileNotFoundError(
            f"S512 final not found at {s512_path}; run P02_S512 before P02_S504."
        )
    s512 = pd.read_csv(s512_path)
    s512_ext = s512[s512["series_id"] == "S512-EXT"][["year", "value"]]
    s512_ext = s512_ext.rename(columns={"value": "vshare"})
    if s512_ext.empty:
        raise RuntimeError("S512-EXT subseries empty; cannot derive S504-EXT.")

    w = load_total_compensation().rename(columns={"value": "W_bn"})  # $billions
    merged = s512_ext.merge(w, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["vshare"] * merged["W_bn"]
    merged["series_id"]  = "S504-EXT"
    merged["units"]      = "billions_usd"
    merged["stage"]      = "extension"
    merged["provenance"] = "S512-EXT × BEA NIPA T20100 (compensation_millions / 1000)"
    out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]
    diag = {
        "n_rows":    len(out),
        "period":    (int(out["year"].min()), int(out["year"].max())),
        "ext_1998":  float(out.loc[out["year"]==1998, "value"].iloc[0]),
        "ext_last":  float(out.iloc[-1]["value"]),
    }
    return out, diag


def _interp_frame(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Build S504-INTERP — log-linear bridge for 1990-1997.

    Uses the BOOK_LAST_YEAR (1989) and EXT_FIRST_YEAR (1998) endpoints; output
    rows cover years 1990..1997 inclusive (open interval over the bridge).
    Mirrors the M04_S501/S502/S503 methodological adjustment recipe.
    """
    book_endpoint = float(
        book_df.loc[book_df["year"] == BOOK_LAST_YEAR, "value"].iloc[0]
    )
    ext_endpoint = float(
        ext_df.loc[ext_df["year"] == EXT_FIRST_YEAR, "value"].iloc[0]
    )
    bridge = _log_linear_bridge(book_endpoint, ext_endpoint,
                                y0=BOOK_LAST_YEAR, y1=EXT_FIRST_YEAR)
    bridge["series_id"]  = "S504-INTERP"
    bridge["units"]      = "billions_usd"
    bridge["stage"]      = "extension_bridge"
    bridge["provenance"] = (
        f"Log-linear interpolation between book(1989)={book_endpoint:.2f} and "
        f"BEA-derived EXT(1998)={ext_endpoint:.2f}; "
        "M04_S504 methodological adjustment per BUILD_NARRATIVE.md Stage 5 "
        "cohort 3 (S501-S503 precedent); INTERPOLATED VALUE — not raw data"
    )
    bridge = bridge[["series_id", "year", "value", "units", "stage", "provenance"]]
    diag = {
        "book_1989":     book_endpoint,
        "ext_1998":      ext_endpoint,
        "n_interp_rows": len(bridge),
        "interp_period": (int(bridge["year"].min()), int(bridge["year"].max())),
        "interp_1991":   float(bridge.loc[bridge["year"]==1991, "value"].iloc[0]),
        "interp_1995":   float(bridge.loc[bridge["year"]==1995, "value"].iloc[0]),
    }
    return bridge, diag


def _combined_frame(book_df: pd.DataFrame, ext_df: pd.DataFrame,
                    interp_df: pd.DataFrame) -> pd.DataFrame:
    a = book_df[book_df["series_id"] == "S504-A"][["year", "value", "provenance"]].copy()
    a["series_id"] = "S504-COMBINED"
    a["stage"]     = "book_period"

    b = interp_df[["year", "value", "provenance"]].copy()
    b["series_id"] = "S504-COMBINED"
    b["stage"]     = "extension_bridge"

    e = ext_df[ext_df["series_id"] == "S504-EXT"][["year", "value", "provenance"]].copy()
    e = e[e["year"] >= EXT_FIRST_YEAR].copy()
    e["series_id"] = "S504-COMBINED"
    e["stage"]     = "extension"

    out = pd.concat([a, b, e], ignore_index=True, sort=False).sort_values("year")
    out["units"] = "billions_usd"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]].reset_index(drop=True)


def run():
    book = _book_period_frame()
    try:
        ext, diag = _extension_frame()
        interp, idiag = _interp_frame(book, ext)
        combined = _combined_frame(book, ext, interp)
        df = pd.concat([book, ext, interp, combined], ignore_index=True, sort=False)
        print(f"    [P02_S504] extension diag: {diag}")
        print(f"    [P02_S504] interp    diag: {idiag}")
    except Exception as exc:
        print(f"    [P02_S504] EXTENSION FAILED: {exc!r} — writing book-only")
        df = book
    write_series_csv(df, "S504", stage="intermediate")
    final_path = write_series_csv(df, "S504", stage="final")
    print(f"    [P02_S504] wrote {final_path.name} ({len(df)} rows, "
          f"subseries: {sorted(df['series_id'].unique())})")


if __name__ == "__main__":
    run()
