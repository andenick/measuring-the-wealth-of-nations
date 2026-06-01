"""Regression tests: fresh chopped CSVs must match the golden snapshot.

The golden snapshot lives at `Technical/tests/golden_chopped/` and was
captured on 2026-05-24 (see VERSION.txt in that directory). Any unintentional
change to the pipeline output will surface as a test failure here.

Two-line metadata header (per anu-chopped wide format, Decision 0005):

    Row 1: per-column metadata strings (name, units, period, status)
    Row 2: column IDs (Year + per-subseries IDs)
    Row 3+: numeric data, with `nan` for missing year/subseries cells

To deliberately update the golden snapshot, replace the directory contents
from Technical/chopped/ and bump VERSION.txt.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

# Float comparison tolerances. The chopped CSVs round to ~14-15 sig figs when
# written from float64, so a tight tolerance is appropriate.
RTOL = 1e-9
ATOL = 1e-9

GOLDEN_DIR = Path(__file__).resolve().parent / "golden_chopped"
CHOPPED_DIR = Path(__file__).resolve().parents[1] / "chopped"


def _golden_csvs() -> list[Path]:
    return sorted(p for p in GOLDEN_DIR.glob("*.csv"))


def _pair_ids() -> list[str]:
    return [p.stem for p in _golden_csvs()]


def _read_chopped(path: Path) -> tuple[list[str], pd.DataFrame]:
    """Return (metadata_header_line, data_frame) for a chopped CSV.

    Row 1 is the per-column metadata string row. Row 2 is the column header
    line (Year + subseries IDs). Row 3+ are the numeric body.
    """
    with path.open("r", encoding="utf-8") as f:
        meta_line = f.readline().rstrip("\n")
    df = pd.read_csv(path, header=1)
    return [meta_line], df


@pytest.mark.regression
@pytest.mark.parametrize("sid", _pair_ids())
def test_chopped_matches_golden(sid: str):
    golden = GOLDEN_DIR / f"{sid}.csv"
    current = CHOPPED_DIR / f"{sid}.csv"

    if not current.exists():
        pytest.fail(f"Chopped CSV {sid}.csv has disappeared from Technical/chopped/")

    g_meta, g_df = _read_chopped(golden)
    c_meta, c_df = _read_chopped(current)

    # 1. Metadata row 1 must match exactly (free-form text — strict equality).
    assert c_meta == g_meta, (
        f"{sid}: metadata header row drift.\n  golden  : {g_meta[0]}\n  current : {c_meta[0]}"
    )

    # 2. Columns must match (order + names).
    assert list(c_df.columns) == list(g_df.columns), (
        f"{sid}: column drift.\n  golden  : {list(g_df.columns)}\n  current : {list(c_df.columns)}"
    )

    # 3. Numeric body must match within tight tolerance.
    try:
        pd.testing.assert_frame_equal(
            c_df.reset_index(drop=True),
            g_df.reset_index(drop=True),
            check_dtype=False,
            check_exact=False,
            rtol=RTOL,
            atol=ATOL,
        )
    except AssertionError as e:
        # Surface a compact summary of the first mismatching cells.
        merged = c_df.merge(
            g_df,
            on=c_df.columns[0],
            how="outer",
            suffixes=("_current", "_golden"),
            indicator=True,
        )
        only = merged[merged["_merge"] != "both"]
        head = only.head(5).to_string(index=False) if not only.empty else "(value drift, see assertion)"
        pytest.fail(f"{sid}: regression diff\n{e}\n\nFirst drift rows:\n{head}")


@pytest.mark.regression
def test_golden_directory_has_expected_count():
    n = len(_golden_csvs())
    assert n == 64, f"Golden snapshot should hold 64 chopped CSVs, found {n}"


@pytest.mark.regression
def test_chopped_directory_has_no_extra_files():
    """Ensure current chopped/ has the same SID set as the snapshot (no orphans/strays)."""
    golden_sids = {p.stem for p in _golden_csvs()}
    current_sids = {p.stem for p in CHOPPED_DIR.glob("*.csv")}
    new = current_sids - golden_sids
    removed = golden_sids - current_sids
    if new or removed:
        pytest.fail(
            f"SID drift: new in chopped/={sorted(new)}; missing from chopped/={sorted(removed)}.\n"
            "Update the golden snapshot if these changes are intentional."
        )
