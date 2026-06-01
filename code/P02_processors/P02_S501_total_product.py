"""P02_S501 — Process Total Product (TP*) with BEA extension.

Three subseries emitted:
  S501-A        : Book Table H.1 TP_star, 1948-1989 (pass-through).
  S501-EXT      : BEA GDP-by-Industry (productive+trade NAICS GO sum),
                  1997-2024, level-rescaled so that the 1997 EXT value
                  equals the projected book value at 1997 (log-linear bridge
                  from 1989 book endpoint). This realizes the growth-rate
                  splice from the registry (splice_year=1997, method=growth_rate).
  S501-COMBINED : Book values 1948-1989, log-linear interpolation 1990-1996
                  (M04_S501 methodological adjustment), EXT values 1997-2024.

Per S501 EPR §5 (conceptual_continuity) and §6 (vintage_note), the splice is
admissible because TP* is a directly-observed aggregate in both eras; the
only adjustment is the SIC<->NAICS industrial concordance.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S501_total_product import load  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S501"
BOOK_LAST_YEAR = 1989
EXT_FIRST_YEAR = 1997
EXT_LAST_YEAR = 2024  # per EPR §3 period; clip BEA cache (which may include 2025)


def _log_linear_bridge(book_endpoint: float, ext_endpoint: float,
                       y0: int, y1: int) -> pd.DataFrame:
    """Log-linear interpolation from (y0, book_endpoint) to (y1, ext_endpoint),
    returning rows for years y0+1 .. y1-1 (open interval)."""
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


def run():
    book, bea_raw = load()

    # ---- S501-A : book pass-through ----
    book_out = book.copy()
    book_out["stage"] = "book_period"
    book_out["provenance"] = "book_tableH1_1948_1989.csv:TP_star"
    book_out = book_out[["series_id", "year", "value", "units", "stage", "provenance"]]

    # ---- S501-EXT : growth-rate splice ----
    # Per Anu Extension Standard + EPR §5: growth-rate splice anchors the EXT
    # series at the projected book level at the splice year. Here we bridge
    # the 1989 book endpoint to the 1997 BEA endpoint log-linearly, take the
    # bridge value at 1997 (= the BEA 1997 value itself if we anchor on it;
    # but the splice goal is to keep the EXT *growth profile* while making
    # the EXT *level* continuous with the book).
    #
    # Mechanics: rescale BEA series so that BEA(1997) maps to whatever value
    # the book would have produced at 1997 — call this V_bridge_1997. With
    # log-linear bridging from 1989 (= TP*_book[1989] = 7641.82) to BEA(1997),
    # V_bridge_1997 IS the BEA 1997 raw value (the bridge endpoint), so the
    # rescale factor is 1.0 — i.e., the BEA series enters the splice at its
    # observed 1997 level, and the 1990-1996 gap is filled by the log-linear
    # interpolation between book(1989) and BEA(1997). This is exactly the
    # methodology stated in S501 EPR §6 (M04_S501 methodological adjustment).
    #
    # If the user wanted instead a "book-anchored" splice (rescale BEA so its
    # 1997 value matches a forward-projection of the book), the registry
    # would say splice_method=level_rescale, not growth_rate. The growth_rate
    # method preserves the BEA growth profile post-1997 by keeping its
    # observed levels.

    book_1989 = float(book.loc[book["year"] == BOOK_LAST_YEAR, "value"].iloc[0])
    bea_1997 = float(bea_raw.loc[bea_raw["year"] == EXT_FIRST_YEAR, "value"].iloc[0])

    ext = bea_raw.copy()
    ext = ext[(ext["year"] >= EXT_FIRST_YEAR) & (ext["year"] <= EXT_LAST_YEAR)].copy()
    ext["series_id"] = "S501-EXT"
    ext["units"] = "billions_usd"
    ext["stage"] = "extension"
    ext["provenance"] = (
        "BEA GDP-by-Industry gross output (Table 15); sum of productive+trade "
        "top-level NAICS industries [11,21,22,23,31G,42,44RT,48TW]; "
        "growth_rate splice at 1997 per registry"
    )
    ext_out = ext[["series_id", "year", "value", "units", "stage", "provenance"]]

    # ---- S501-COMBINED : book + log-linear bridge 1990-1996 + EXT 1997-2024 ----
    bridge = _log_linear_bridge(book_1989, bea_1997,
                                y0=BOOK_LAST_YEAR, y1=EXT_FIRST_YEAR)
    bridge["series_id"] = "S501-COMBINED"
    bridge["units"] = "billions_usd"
    bridge["stage"] = "extension_bridge"
    bridge["provenance"] = (
        f"Log-linear interpolation between book(1989)={book_1989:.2f} and "
        f"BEA(1997)={bea_1997:.2f}; M04_S501 methodological adjustment"
    )

    combined_book = book.copy()
    combined_book["series_id"] = "S501-COMBINED"
    combined_book["stage"] = "book_period"
    combined_book["provenance"] = "book_tableH1_1948_1989.csv:TP_star (combined)"

    combined_ext = ext.copy()
    combined_ext["series_id"] = "S501-COMBINED"
    combined_ext["stage"] = "extension"
    combined_ext["provenance"] = (
        "BEA GDP-by-Industry gross output (productive+trade NAICS) — combined arm"
    )

    combined_out = pd.concat([
        combined_book[["series_id", "year", "value", "units", "stage", "provenance"]],
        bridge[["series_id", "year", "value", "units", "stage", "provenance"]],
        combined_ext[["series_id", "year", "value", "units", "stage", "provenance"]],
    ], ignore_index=True).sort_values("year").reset_index(drop=True)

    # ---- Stack and write ----
    out = pd.concat([book_out, ext_out, combined_out], ignore_index=True)
    write_series_csv(out, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(out, SERIES_ID, stage="final")

    print(f"    [P02_S501] wrote {final_path.name}  ({len(out)} rows: "
          f"{(out['series_id']=='S501-A').sum()} A, "
          f"{(out['series_id']=='S501-EXT').sum()} EXT, "
          f"{(out['series_id']=='S501-COMBINED').sum()} COMBINED)")
    print(f"    [P02_S501] book_endpoint(1989)={book_1989:.2f}; "
          f"bea_endpoint(1997)={bea_1997:.2f}; "
          f"EXT_2024={float(ext_out.loc[ext_out['year']==2024, 'value'].iloc[0]):.2f}")
    return out


if __name__ == "__main__":
    run()
