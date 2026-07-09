"""P02_S512 — Process Productive Wage Share (V*/W).

Four subseries written to data/final/S512.csv:
  - S512-A         : book Table 5.7 column T512A, 1948-1989, stage=book_period
  - S512-EXT       : BEA NIPA 6.2D productive-sector share, 1998-end,
                     stage=extension. Level-spliced to the book endpoint:
                     scaling factor = book(1989) / nipa_raw(1998_anchor) so the
                     1998 extension value sits on a smooth continuation of the
                     book trend (per EPR section 5: "splice method is level,
                     rebased at 1989 to match the book's Table 5.7 value 0.36").
  - S512-INTERP    : Log-linear interpolation between book(1989) endpoint and
                     EXT(1998) first value, populating 1990-1997.
                     stage=extension_bridge; M04_S512 manual adjustment per
                     BUILD_NARRATIVE.md Stage 5 cohort 3 precedent (S501-S503).
  - S512-COMBINED  : 1948-1989 from S512-A, 1990-1997 from S512-INTERP,
                     1998-end from S512-EXT.

The 1990-1997 bridge is honestly flagged as INTERPOLATED — the underlying NIPA
6.2D data does not exist for those years. EXT proper remains BEA-only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S512_productive_wage_share import (  # noqa: E402
    LOADER,
    load_extension_components,
)
from utils.io import write_series_csv  # noqa: E402


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
    df["provenance"] = "Table5_7_KeyRatios.csv:T512A"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def _sic_partA():
    """Real SIC-basis partition VA/comp 1987-1997 (data/source/bea_sic). Materialized from
    BEA Historical Industry Accounts GDPbyInd_VA_SIC.xls (workpackage A 2026-07-01)."""
    p = Path(__file__).resolve().parents[2] / "data" / "source" / "bea_sic" / "GDPbyInd_partitionA_SIC_1987_1997.csv"
    return pd.read_csv(p)


def _total_comp_map():
    p = Path(__file__).resolve().parents[2] / "data" / "raw" / "bea" / "nipa_T20100_compensation_1929_2025.csv"
    w = pd.read_csv(p)
    return {int(r.year): r.compensation_millions / 1000.0 for r in w.itertuples()}


def _extension_frame(book_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Build S512-EXT (R1 de-spliced, honest raw share) + S512-EXT-SPLICED-DEPRECATED
    (old curve-fit, retained). workpackage A rebuild:

      R1  retire the projected-1998/nipa level-splice (it manufactured V* < true productive
          compensation and inflated S506 to the spurious 1.27 - see P1_FORENSIC_REPORT).
      R3  fill 1990-1997 with REAL SIC-basis data (productive-sector comp / total compensation),
          replacing the log-linear bridge.

    Honest V*/W = productive-sector compensation / total employee compensation, on a consistent
    concept across the seam: SIC (comp_prod_SIC / T20100) 1990-1997, NIPA 6.2D lines / line1
    1998-2024. The SIC->NAICS vintage break at 1997/98 (0.314 -> 0.269) is REAL and flagged,
    not spliced away (DIV-A11, DIV-010).
    """
    ext = load_extension_components()
    total      = ext["compensation_total"].rename(columns={"value": "W_nipa"})
    productive = ext["compensation_productive"].rename(columns={"value": "Vstar_nipa"})
    naics = total.merge(productive, on="year").sort_values("year").reset_index(drop=True)
    naics["share_raw"] = naics["Vstar_nipa"] / naics["W_nipa"]
    naics = naics[naics["year"] >= 1998]

    # --- SIC-basis real fill 1990-1997 ---
    sic = _sic_partA(); W = _total_comp_map()
    sic = sic[(sic["year"] >= 1990) & (sic["year"] <= 1997)].copy()
    sic["value"] = sic.apply(lambda r: r["comp_prod"] / W[int(r["year"])], axis=1)
    sic_rows = sic[["year", "value"]].copy()
    sic_rows["provenance"] = ("Real SIC-basis V*/W = productive-sector compensation "
                              "(comp_prod, GDPbyInd SIC) / total compensation (NIPA T20100); "
                              "REAL DATA replacing the retired log-linear bridge (R3)")

    naics_rows = naics[["year"]].copy()
    naics_rows["value"] = naics["share_raw"].values
    naics_rows["provenance"] = ("BEA NIPA 6.2D lines [5,7,11,12,13,43] / line 1 (de-spliced, "
                                "raw honest share - R1)")

    merged = pd.concat([sic_rows, naics_rows], ignore_index=True).sort_values("year").reset_index(drop=True)
    merged["series_id"] = "S512-EXT"
    merged["units"]     = "share"
    merged["stage"]     = "extension"
    ext_out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]

    # --- retained deprecated spliced arm (transparency; nothing silently deleted) ---
    book_a = book_df[book_df["series_id"] == "S512-A"][["year", "value"]].set_index("year")["value"]
    book_1989 = float(book_a.loc[1989]); seg = book_a.loc[1985:1989]
    slope = (seg.iloc[-1] - seg.iloc[0]) / (seg.index[-1] - seg.index[0])
    proj_1998 = book_1989 + slope * (1998 - 1989)
    nipa_1998 = float(naics.loc[naics["year"] == 1998, "share_raw"].iloc[0])
    scale = proj_1998 / nipa_1998 if nipa_1998 else 1.0
    dep = naics[["year"]].copy()
    dep["value"] = naics["share_raw"].values * scale
    dep["series_id"] = "S512-EXT-SPLICED-DEPRECATED"; dep["units"] = "share"; dep["stage"] = "extension_deprecated"
    dep["provenance"] = (f"DEPRECATED old level-splice (scale={scale:.4f}, proj_1998={proj_1998:.4f}); "
                         "curve-fit toward book that inflated S506-EXT to the spurious 1.27. Retained per DIV-A11.")
    dep_out = dep[["series_id", "year", "value", "units", "stage", "provenance"]]

    diag = {
        "book_1989": book_1989, "sic_1997": round(float(sic_rows.loc[sic_rows.year==1997,"value"].iloc[0]),4),
        "raw_1998": round(nipa_1998,4), "deprecated_spliced_1998": round(nipa_1998*scale,4),
        "ext_period": (int(ext_out["year"].min()), int(ext_out["year"].max())),
        "ext_last": round(float(ext_out.iloc[-1]["value"]),4),
    }
    return ext_out, dep_out, diag


def _interp_frame(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Build S512-INTERP — log-linear bridge for 1990-1997.

    Uses BOOK_LAST_YEAR (1989) and EXT_FIRST_YEAR (1998) endpoints.
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
    bridge["series_id"]  = "S512-INTERP"
    bridge["units"]      = "share"
    bridge["stage"]      = "extension_bridge"
    bridge["provenance"] = (
        f"Log-linear interpolation between book(1989)={book_endpoint:.4f} and "
        f"EXT(1998)={ext_endpoint:.4f}; "
        "M04_S512 methodological adjustment per BUILD_NARRATIVE.md Stage 5 "
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


def _combined_frame(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    a = book_df[book_df["series_id"] == "S512-A"][["year", "value"]].copy()
    a["series_id"] = "S512-COMBINED"
    a["stage"]     = "book_period"
    a["provenance"] = "Table5_7_KeyRatios.csv:T512A"

    e = ext_df[ext_df["series_id"] == "S512-EXT"][["year", "value", "provenance"]].copy()
    e = e[e["year"] > BOOK_LAST_YEAR].copy()
    e["series_id"] = "S512-COMBINED"
    e["stage"]     = "extension"

    out = pd.concat([a, e], ignore_index=True, sort=False).sort_values("year")
    out["units"] = "share"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]].reset_index(drop=True)


def run():
    book = _book_period_frame()
    try:
        ext, dep, diag = _extension_frame(book)
        combined = _combined_frame(book, ext)
        df = pd.concat([book, ext, dep, combined], ignore_index=True, sort=False)
        print(f"    [P02_S512] extension diag (R1 de-spliced + R3 real SIC 1990-97): {diag}")
    except Exception as exc:
        print(f"    [P02_S512] EXTENSION FAILED: {exc!r} — writing book-only")
        import traceback; traceback.print_exc()
        df = book
    write_series_csv(df, "S512", stage="intermediate")
    final_path = write_series_csv(df, "S512", stage="final")
    print(f"    [P02_S512] wrote {final_path.name} ({len(df)} rows, "
          f"subseries: {sorted(df['series_id'].unique())})")


if __name__ == "__main__":
    run()
