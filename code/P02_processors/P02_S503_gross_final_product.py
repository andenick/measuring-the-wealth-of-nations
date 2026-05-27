"""P02_S503 — Process Gross Final Product (GFP) with BEA extension.

Three subseries emitted (mirrors S501 pattern):
  S503-A        : Book Table H.1 GFP_star column, 1948-1989 (pass-through).
  S503-EXT      : BEA Value Added for productive+trade NAICS top-level industries,
                  1997-2024. Growth-rate splice at 1997 per registry.
  S503-COMBINED : Book 1948-1989, log-linear bridge 1990-1996, EXT 1997-2024.

Conceptual continuity: GFP = TP* - C*_m is value added by productive industries.
BEA's GDP-by-Industry Value Added (VA = GO - II) is the modern accounting
equivalent restricted to the same productive partition used by S501/S502.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S503_gross_final_product import load  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S503"
BOOK_LAST_YEAR = 1989
EXT_FIRST_YEAR = 1997
EXT_LAST_YEAR = 2024


def _log_linear_bridge(book_endpoint: float, ext_endpoint: float,
                       y0: int, y1: int) -> pd.DataFrame:
    if book_endpoint <= 0 or ext_endpoint <= 0:
        raise ValueError("log-linear bridge requires positive endpoints")
    n = y1 - y0
    log0 = np.log(book_endpoint)
    log1 = np.log(ext_endpoint)
    rows = []
    for k in range(1, n):
        frac = k / n
        val = float(np.exp(log0 + frac * (log1 - log0)))
        rows.append({"year": y0 + k, "value": val})
    return pd.DataFrame(rows)


def run():
    book, bea_raw = load()

    # ---- S503-A : book pass-through ----
    book_out = book.copy()
    book_out["stage"] = "book_period"
    book_out["provenance"] = "book_tableH1_1948_1989.csv:GFP_star"
    book_out = book_out[["series_id", "year", "value", "units", "stage", "provenance"]]

    # ---- S503-EXT : growth-rate splice ----
    book_1989 = float(book.loc[book["year"] == BOOK_LAST_YEAR, "value"].iloc[0])
    bea_1997 = float(bea_raw.loc[bea_raw["year"] == EXT_FIRST_YEAR, "value"].iloc[0])

    ext = bea_raw.copy()
    ext = ext[(ext["year"] >= EXT_FIRST_YEAR) & (ext["year"] <= EXT_LAST_YEAR)].copy()
    ext["series_id"] = "S503-EXT"
    ext["units"] = "billions_usd"
    ext["stage"] = "extension"
    ext["provenance"] = (
        "BEA GDP-by-Industry Value Added; sum of productive+trade top-level NAICS "
        "industries [11,21,22,23,31G,42,44RT,48TW]; growth_rate splice at 1997"
    )
    ext_out = ext[["series_id", "year", "value", "units", "stage", "provenance"]]

    # ---- S503-COMBINED ----
    bridge = _log_linear_bridge(book_1989, bea_1997,
                                y0=BOOK_LAST_YEAR, y1=EXT_FIRST_YEAR)
    bridge["series_id"] = "S503-COMBINED"
    bridge["units"] = "billions_usd"
    bridge["stage"] = "extension_bridge"
    bridge["provenance"] = (
        f"Log-linear interpolation between book(1989)={book_1989:.2f} and "
        f"BEA(1997)={bea_1997:.2f}; M04_S503 methodological adjustment"
    )

    combined_book = book.copy()
    combined_book["series_id"] = "S503-COMBINED"
    combined_book["stage"] = "book_period"
    combined_book["provenance"] = "book_tableH1_1948_1989.csv:GFP_star (combined)"

    combined_ext = ext.copy()
    combined_ext["series_id"] = "S503-COMBINED"
    combined_ext["stage"] = "extension"
    combined_ext["provenance"] = (
        "BEA Value Added (productive+trade NAICS) — combined arm"
    )

    combined_out = pd.concat([
        combined_book[["series_id", "year", "value", "units", "stage", "provenance"]],
        bridge[["series_id", "year", "value", "units", "stage", "provenance"]],
        combined_ext[["series_id", "year", "value", "units", "stage", "provenance"]],
    ], ignore_index=True).sort_values("year").reset_index(drop=True)

    out = pd.concat([book_out, ext_out, combined_out], ignore_index=True)
    write_series_csv(out, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(out, SERIES_ID, stage="final")

    print(f"    [P02_S503] wrote {final_path.name}  ({len(out)} rows: "
          f"{(out['series_id']=='S503-A').sum()} A, "
          f"{(out['series_id']=='S503-EXT').sum()} EXT, "
          f"{(out['series_id']=='S503-COMBINED').sum()} COMBINED)")
    print(f"    [P02_S503] book_endpoint(1989)={book_1989:.2f}; "
          f"bea_endpoint(1997)={bea_1997:.2f}; "
          f"EXT_2024={float(ext_out.loc[ext_out['year']==2024, 'value'].iloc[0]):.2f}")
    return out


if __name__ == "__main__":
    run()
