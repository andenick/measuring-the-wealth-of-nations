"""T501 (TP*), T502 (C*m), T503 (GFP* = TP* - C*m).

Book period: Table E.2 revenue accounts (1948-1961 available).
             Table H.1 has TP*, Mp for all 42 years.
Extension:   BEA GDP-by-Industry growth-rate splice (1997+ IO C*m overlay).

Formulas:
  TP* = GOp + GOtt (total product = production + trade gross output)
  C*m = Mp' (materials inputs into production)
  GFP* = TP* - C*m (gross final product)
"""

import pandas as pd
from pipeline.sources.book_data import load_table_h1, load_revenue_accounts
from pipeline.sources.api_fetch import load_nipa_csv

DEPENDS_ON = []  # no upstream compute dependencies


def compute(series_store: dict = None) -> dict[str, pd.DataFrame]:
    h1 = load_table_h1()

    # Book period from Table H.1
    tp_book = h1["TP_star"]
    cm_book = h1["Mp"]
    gfp_book = h1["GFP_star"]

    # Extension: GDP growth-rate splice from 1990+
    gdp_nipa = load_nipa_csv("nipa_1_7_5_gross_output_by_industry.csv")
    # TODO: implement extension logic matching v6.0 P01

    # For now, return book period only (extension to be added)
    t501 = pd.DataFrame({"book": tp_book, "combined": tp_book})
    t502 = pd.DataFrame({"book": cm_book, "combined": cm_book})
    t503 = pd.DataFrame({"book": gfp_book, "combined": gfp_book})

    for df in [t501, t502, t503]:
        df.index.name = "year"

    return {"T501": t501, "T502": t502, "T503": t503}
