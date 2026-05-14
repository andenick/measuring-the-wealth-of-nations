"""L01_S511 — Load Productive Labor Share (Lp/L) book-period series, 1948-1989.

Source: Book Table 5.7 (digitized as Table5_7_KeyRatios.csv), column `T511A`
which holds the book's published Lp/L values for benchmark years with
interpolation between (the book itself publishes 1948, 1958, 1967, 1977, 1989).

Why T511A specifically: the file has two parallel columns — `T511A` (book values,
the authoritative source) and `T511` (replicator output). The DPR uses the
book-as-source rule, so we load T511A.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "S511",
    subseries_id  = "S511-A",
    source_file   = BOOK_TABLES / "Table5_7_KeyRatios.csv",
    source_column = "T511A",
    units         = "share",
)


def run():
    df = LOADER.load()
    print(f"    [L01_{LOADER.series_id}] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()
