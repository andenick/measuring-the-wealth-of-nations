"""P02_S505 — Process Surplus Value (S*).

Three subseries written to data/final/S505.csv:
  - S505-A         : Appendix H.1 S_star, 1948-1989, stage=book_period
  - S505-EXT       : Derived S* = GFP - V* = S503-COMBINED - S504-COMBINED
                     stage=extension
  - S505-COMBINED  : 1948-1989 from S505-A, post-1989 from S505-EXT

Per EPR / registry construction: S505 extension is *derived* via the
identity S* = GFP - V*. It is NOT a growth-rate splice of S* directly
(see Anu Extension Standard no-lazy-splice rule). Coverage of the EXT
subseries inherits any gaps from S503-COMBINED ∩ S504-COMBINED.

Upstream dependencies (parallel cohort 3):
  - data/final/S503.csv must contain S503-COMBINED (written by P02_S503)
  - data/final/S504.csv must contain S504-COMBINED (written by P02_S504)

If either upstream COMBINED is unavailable, we fall back to a book-only
write with a clear stderr notice — never fabricate.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S505_surplus_value import LOADER  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def _book_period_frame() -> pd.DataFrame:
    df = LOADER.load()
    df["stage"]      = "book_period"
    df["provenance"] = "book_tableH1_1948_1989.csv:S_star"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def _load_upstream_combined(sid: str) -> pd.DataFrame:
    """Read data/final/<sid>.csv and return the -COMBINED rows.

    Falls back to -A (book-only) if -COMBINED is absent; the caller still gets
    a frame so book-period rows survive even when extension is incomplete.
    """
    path = DATA_FINAL / f"{sid}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Upstream {path} missing.")
    df = pd.read_csv(path)
    combined_id = f"{sid}-COMBINED"
    if combined_id in df["series_id"].unique():
        return df[df["series_id"] == combined_id][["year", "value"]].copy()
    # No COMBINED yet -> fall back to the -A book subseries (book period only)
    return df[df["series_id"] == f"{sid}-A"][["year", "value"]].copy()


def _extension_frame() -> tuple[pd.DataFrame, dict]:
    gfp = _load_upstream_combined("S503").rename(columns={"value": "GFP"})
    v   = _load_upstream_combined("S504").rename(columns={"value": "V_star"})

    # Confirm at least one post-1989 year exists in BOTH upstreams; otherwise
    # we can't compute a real extension and we should defer.
    s503_post = gfp[gfp["year"] > 1989]
    s504_post = v  [v  ["year"] > 1989]
    if s503_post.empty or s504_post.empty:
        raise RuntimeError(
            "Upstream EXT incomplete: "
            f"S503 post-1989 rows={len(s503_post)}, S504 post-1989 rows={len(s504_post)}. "
            "Cannot derive S505-EXT until S503-COMBINED and S504-COMBINED both extend."
        )

    merged = gfp.merge(v, on="year").sort_values("year").reset_index(drop=True)
    merged = merged[merged["year"] > 1989].copy()
    merged["value"] = merged["GFP"] - merged["V_star"]
    merged["series_id"]  = "S505-EXT"
    merged["units"]      = "billions_usd"
    merged["stage"]      = "extension"
    merged["provenance"] = "Derived S* = S503-COMBINED - S504-COMBINED (identity, no splice)"
    out = merged[["series_id", "year", "value", "units", "stage", "provenance"]]
    diag = {
        "n_rows":   len(out),
        "period":   (int(out["year"].min()), int(out["year"].max())) if not out.empty else None,
        "first":    float(out.iloc[0]["value"])  if not out.empty else None,
        "last":     float(out.iloc[-1]["value"]) if not out.empty else None,
    }
    return out, diag


def _combined_frame(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    a = book_df[book_df["series_id"] == "S505-A"][["year", "value", "provenance"]].copy()
    a["series_id"] = "S505-COMBINED"
    a["stage"]     = "book_period"

    e = ext_df[ext_df["series_id"] == "S505-EXT"][["year", "value", "provenance"]].copy()
    e = e[e["year"] > 1989].copy()
    e["series_id"] = "S505-COMBINED"
    e["stage"]     = "extension"

    out = pd.concat([a, e], ignore_index=True, sort=False)
    out["units"] = "billions_usd"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    book = _book_period_frame()
    try:
        ext, diag = _extension_frame()
        combined = _combined_frame(book, ext)
        df = pd.concat([book, ext, combined], ignore_index=True, sort=False)
        print(f"    [P02_S505] extension diag: {diag}")
    except Exception as exc:
        print(f"    [P02_S505] EXTENSION DEFERRED: {exc!r} — writing book-only")
        df = book
    write_series_csv(df, "S505", stage="intermediate")
    final_path = write_series_csv(df, "S505", stage="final")
    print(f"    [P02_S505] wrote {final_path.name} ({len(df)} rows, "
          f"subseries: {sorted(df['series_id'].unique())})")


if __name__ == "__main__":
    run()
