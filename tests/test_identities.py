"""Algebraic identity tests across the chopped series.

These are the load-bearing definitional identities from Shaikh & Tonak (1994):

    S505 (surplus value)              = S503 (GFP)   - S504 (V*)
    S506 (rate of exploitation)       = S505         / S504
    S516 (unproductive employment)    = L_total      - S515 (productive employment)
    S513 (Marxian profit rate)        = S505         / (S502 + S504)   [extension years]
    S607 (net social wage)            = S605 (B_w)   + S606 (G_w) - S604 (T_w)

Every identity is checked year-by-year using only years where the relevant
inputs are present (non-NaN). Tolerances are tuned per identity:

  * S505 / S516 / S607: absolute tolerance is appropriate because these are
    levels in billions of USD or thousands of workers; the chopped CSVs are
    typically rounded to 2 decimals, so the round-trip error can be ~0.01.
  * S506: ratio of two rounded levels; absolute tolerance ~5e-3 covers the
    propagated rounding error.
  * S513: only checked over -EXT years where the extension reconstructs the
    formula from S502/S504/S505; the book-period rate may use the book's
    own (un-rounded) numerator/denominator and is not re-derivable from the
    rounded chopped values.

Each test prints a compact summary of any failing year(s) before asserting.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

CHOPPED_DIR = Path(__file__).resolve().parents[1] / "chopped"


def _read_chopped(sid: str) -> pd.DataFrame:
    """Read a chopped CSV's numeric body. Header row is at line 2 (0-indexed=1)."""
    path = CHOPPED_DIR / f"{sid}.csv"
    if not path.exists():
        pytest.skip(f"{sid}.csv not present in chopped/")
    df = pd.read_csv(path, header=1)
    # Coerce "nan" strings to real NaN — anu-chopped writes literal "nan".
    df = df.replace({"nan": float("nan")})
    # Coerce all non-year columns to float.
    year_col = df.columns[0]
    for c in df.columns:
        if c == year_col:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
        else:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _series_column(df: pd.DataFrame, subseries_id: str) -> pd.Series:
    """Return the named subseries column indexed by year."""
    assert subseries_id in df.columns, (
        f"Subseries {subseries_id!r} not in columns {list(df.columns)}"
    )
    year_col = df.columns[0]
    return df.set_index(year_col)[subseries_id]


def _identity_diffs(lhs: pd.Series, rhs: pd.Series, *, abs_tol: float) -> pd.DataFrame:
    """Return a frame of rows where |lhs - rhs| > abs_tol, both sides non-null."""
    aligned = pd.concat({"lhs": lhs, "rhs": rhs}, axis=1)
    aligned = aligned.dropna()
    aligned["diff"] = (aligned["lhs"] - aligned["rhs"]).abs()
    return aligned[aligned["diff"] > abs_tol]


# ---------------------------------------------------------------------------
# S505 = S503 - S504  (book-period -A subseries)
# ---------------------------------------------------------------------------


@pytest.mark.identity
def test_S505_identity_book_period():
    """S505 (surplus value) vs S503 (GFP) - S504 (V*).

    NOTE — RE-EVALUATED post REVIEW_2026-07 (Phase 7.1), after the DIV-029
    de-splice of V*/W: the wedge S505 != S503 - S504 STILL EXISTS (42 book
    years, ~9-14 and growing), and the review has now formally EXPLAINED it
    as book-faithful, registering it as DIV-028 (headline).

    Per DIV-028: S503 is the GROSS Final Product GFP* = TP* - Mp, whereas the
    Marxian surplus is NET of productive fixed-capital depreciation Dp:
        VA* = GFP* - Dp           (Shaikh-Tonak net Marxian value added)
        S505 = S* = VA* - V*  = S503 - Dp - S504
    so S505 = S503 - S504 does NOT hold; the residual is exactly Dp (positive,
    growing), NOT a defect. The book's own e = S*/V* is the VA*-based rate
    (S506), which the pipeline reproduces (test_S506 PASSES). The de-splice
    did not — and was not expected to — close this gross-vs-net gap.

    The test therefore remains an imperative xfail: it surfaces the DIV-028
    wedge without blocking unrelated regressions. Retire it only when (a) the
    registry encodes VA*/Dp as their own series and the test is rewritten
    against VA*, or (b) the Dp wedge series is published. Do NOT "fix" this by
    re-basing S503 to VA* — GFP* is the correct, book-defined S503.
    """
    s503 = _series_column(_read_chopped("S503"), "S503-A")
    s504 = _series_column(_read_chopped("S504"), "S504-A")
    s505 = _series_column(_read_chopped("S505"), "S505-A")

    expected = s503 - s504
    diffs = _identity_diffs(s505, expected, abs_tol=1e-2)
    if not diffs.empty:
        pytest.xfail(
            f"DIV-028 (registered): S505-A != S503-A - S504-A for {len(diffs)} year(s); "
            f"residual = productive depreciation Dp (S503=GFP* is GROSS, S505=VA*-V* "
            f"is NET: VA*=GFP*-Dp). Book-faithful, not a defect; e=S506 reproduces.\n"
            f"{diffs.head(5).to_string()}"
        )


# ---------------------------------------------------------------------------
# S506 = S505 / S504  (book-period -A subseries)
# ---------------------------------------------------------------------------


@pytest.mark.identity
def test_S506_identity_book_period():
    s504 = _series_column(_read_chopped("S504"), "S504-A")
    s505 = _series_column(_read_chopped("S505"), "S505-A")
    s506 = _series_column(_read_chopped("S506"), "S506-A")

    expected = s505 / s504
    # Chopped S506 is typically rounded to 2 dp; absolute tol of 5e-3 covers
    # propagated rounding from the rounded numerator/denominator.
    diffs = _identity_diffs(s506, expected, abs_tol=5e-3)
    if not diffs.empty:
        pytest.fail(
            f"S506-A != S505-A / S504-A for {len(diffs)} year(s):\n{diffs.head(10).to_string()}"
        )


# ---------------------------------------------------------------------------
# S516 = L - S515  (productive vs unproductive employment), tested against an
# INDEPENDENT L across ALL years including the 1989/1990 seam.
#
# REVIEW_2026-07 item D2 (S515/S516 seam redesign, candidate (d)). The old
# test was tautological: it built l_total := S515 + S516 and then checked
# S516 == l_total - S515 (an algebraic identity that can never fail), touched
# only the book arm, and never compared against an independent L. It is
# replaced below by a genuinely independent test whose L is built from a
# SEPARATE source (the book TableE3 L_total for <=1989 + the fetched BLS CES
# total-nonfarm-incl-govt series CES0000000001, re-anchored to the book L at
# 1989 for >=1990) — the same primitive the pipeline consumes, but recomputed
# here from raw sources, NOT read back from S515/S516. If P02 regressed to the
# old private-L universe (or the 1961 anchor), the published S515+S516 sum
# would diverge from this independently-built L and these tests would FAIL.
#
# Book anchors quoted verbatim from Table 5.5 / Appendix F Table F.1 /
# TableE3_LaborStatistics.csv (all agree exactly):
#     1989: L = 113511, Lp = 41148, Lu = 72363, Lp/L = 0.363
#     1961: L =  64740, Lp = 29363, Lu = 35377, Lp/L = 0.454
#     1948: L =  58301, Lp = 32994, Lu = 25307
# ---------------------------------------------------------------------------

_BOOK_TABLES = Path(__file__).resolve().parents[1] / "data" / "source" / "book_tables"
_TOTAL_NONFARM_CACHE = (
    Path(__file__).resolve().parents[2]
    / "Inputs" / "predecessor-build" / "Inputs" / "API_Data" / "BLS"
    / "bls_ces_total_nonfarm_all_employees.csv"
)
_ANCHOR_YEAR = 1989


def _book_L_total() -> pd.Series:
    """Independent book L_total (TableE3 row L_total), 1948-1989, indexed by year."""
    path = _BOOK_TABLES / "TableE3_LaborStatistics.csv"
    if not path.exists():
        pytest.skip(f"{path} not present")
    # First line is a `#`-prefixed comment; header is row 2.
    df = pd.read_csv(path, skiprows=1)
    df = df.rename(columns={df.columns[0]: "row_idx"})
    row = df[df["Sector"] == "L_total"]
    assert not row.empty, "L_total row missing from TableE3"
    year_cols = [c for c in df.columns if str(c).isdigit() and 1900 <= int(c) <= 2100]
    return pd.Series({int(c): float(row.iloc[0][c]) for c in year_cols})


def _independent_L() -> pd.Series:
    """L independent of S515/S516: book L_total (<=1989) + re-anchored total
    nonfarm incl. govt (>=1990). Built here from raw sources only."""
    book_L = _book_L_total()
    if _TOTAL_NONFARM_CACHE.exists():
        tnf = pd.read_csv(_TOTAL_NONFARM_CACHE)
        tnf = tnf.dropna(subset=["value"]).set_index("year")["value"].astype(float)
        scale = float(book_L.loc[_ANCHOR_YEAR]) / float(tnf.loc[_ANCHOR_YEAR])
        ext = (tnf * scale)
        ext = ext[ext.index > _ANCHOR_YEAR]
        L = pd.concat([book_L[book_L.index <= _ANCHOR_YEAR], ext])
    else:
        L = book_L  # extension not fetched; book-arm test only
    return L.sort_index()


@pytest.mark.identity
def test_S516_identity_independent_L_all_years():
    """S515-COMBINED + S516-COMBINED == independent L, every year incl. the seam.

    Non-tautological: L is built from the book table + the fetched BLS
    total-nonfarm series, NOT from S515/S516. Tolerance 1.0 thousand covers
    chopped rounding.
    """
    s515 = _series_column(_read_chopped("S515"), "S515-COMBINED")
    s516 = _series_column(_read_chopped("S516"), "S516-COMBINED")
    L = _independent_L()

    lhs = (s515 + s516).dropna()
    common = lhs.index.intersection(L.index)
    assert len(common) >= 42, (
        f"Expected >=42 overlapping years (book span), got {len(common)}"
    )
    diffs = _identity_diffs(lhs.loc[common], L.loc[common], abs_tol=1.0)
    if not diffs.empty:
        pytest.fail(
            f"S515-COMBINED + S516-COMBINED != independent L for {len(diffs)} year(s) "
            f"(this fails if P02 uses a different L universe/anchor than the book):\n"
            f"{diffs.head(10).to_string()}"
        )


@pytest.mark.identity
def test_S515_S516_book_arm_matches_TableE3():
    """Book arms reproduce TableE3 exactly (S515-A = Lp_total; S516-A = L - Lp).

    Guards the digitized book values against round-trip / regression drift.
    """
    s515a = _series_column(_read_chopped("S515"), "S515-A")
    s516a = _series_column(_read_chopped("S516"), "S516-A")
    L = _book_L_total()
    common = L.index.intersection(s515a.dropna().index)
    lu_expected = (L.loc[common] - s515a.loc[common])
    diffs = _identity_diffs(s516a.loc[common], lu_expected, abs_tol=0.5)
    if not diffs.empty:
        pytest.fail(f"S516-A != TableE3 L - S515-A:\n{diffs.head(10).to_string()}")
    # Verbatim anchor checks (Table 5.5 / F.1).
    assert abs(float(s515a.loc[1989]) - 41148) < 0.5, "S515-A[1989] must equal book Lp 41148"
    assert abs(float(s516a.loc[1989]) - 72363) < 0.5, "S516-A[1989] must equal book Lu 72363"


@pytest.mark.identity
def test_S515_S516_seam_continuity():
    """Seam-continuity guard: the 1990 extension level must be within 5% of the
    1989 book level for Lp, Lu, and L. Catches an anchor-year regression (e.g.
    the retired 1961 splice, which gave a -16% Lp break) or an L-universe
    regression (private-only L, which gave a -22% Lu break)."""
    s515 = _series_column(_read_chopped("S515"), "S515-COMBINED")
    s516 = _series_column(_read_chopped("S516"), "S516-COMBINED")
    L = s515 + s516
    for name, s in [("Lp", s515), ("Lu", s516), ("L", L)]:
        v89, v90 = float(s.loc[1989]), float(s.loc[1990])
        rel = abs(v90 / v89 - 1.0)
        assert rel < 0.05, (
            f"{name} seam discontinuity {rel*100:.1f}% "
            f"(1989={v89:.1f} -> 1990={v90:.1f}); expected <5% "
            f"(a larger break signals an anchor-year or L-universe regression)."
        )


@pytest.mark.identity
def test_S511_share_declines_like_book():
    """Trend guard: Lp/L (S511-COMBINED) declines over the postwar period,
    matching Table 5.14 (change 1948-89 = -37%) and FULL_TEXT L454 (Lp/L
    'declines by more than 37%')."""
    share = _series_column(_read_chopped("S511"), "S511-COMBINED")
    b48, b89 = float(share.loc[1948]), float(share.loc[1989])
    change = (b89 - b48) / b48
    assert change < -0.20, (
        f"Lp/L book-period change {change*100:.1f}% (1948={b48:.3f} -> 1989={b89:.3f}); "
        f"book Table 5.14 reports about -37% — a non-declining share is a regression."
    )
    # Extension continues the decline (share[2024] < share[1990]).
    assert float(share.loc[2024]) < float(share.loc[1990]), (
        "Lp/L extension should keep declining (2024 < 1990)."
    )


# ---------------------------------------------------------------------------
# S513 = S505 / (S502 + S504)  (extension years only)
# ---------------------------------------------------------------------------


@pytest.mark.identity
def test_S513_flow_identity_extension():
    """v1.2 update (DIV-012): S513 primary is now stock-form r* = S*/(K*+V*); the
    flow-form r* = S*/(C*+V*) is retained as the S513-FLOW secondary subseries.
    This identity therefore checks S513-FLOW (not S513-EXT) against the flow formula.
    """
    s502 = _series_column(_read_chopped("S502"), "S502-EXT")
    s504 = _series_column(_read_chopped("S504"), "S504-EXT")
    s505 = _series_column(_read_chopped("S505"), "S505-EXT")
    s513_flow = _series_column(_read_chopped("S513"), "S513-FLOW")

    denom = s502 + s504
    expected = s505 / denom
    diffs = _identity_diffs(s513_flow, expected, abs_tol=5e-3)
    if diffs.empty:
        return

    pytest.fail(
        f"S513-FLOW != S505-EXT / (S502-EXT + S504-EXT) for {len(diffs)} year(s):\n"
        f"{diffs.head(10).to_string()}"
    )


# ---------------------------------------------------------------------------
# S607 = S605 + S606 - S604  (Net Social Wage, book-period -A subseries)
# ---------------------------------------------------------------------------


@pytest.mark.identity
def test_S607_identity_book_period():
    """Reconstruction-arm dollar identity NSW = B + G - T.

    D3 (DIV-064, 2026-07-02) swapped the S607 book-period PRIMARY (S607-A) to
    the book-faithful Appendix N value (Ntrrate*EC / Table N.1 1964), which is
    NOT the sum of the reconstruction dollar components S604/S605/S606 -- and,
    per DIV-066 (book 2-decimal rate-row rounding non-additivity), cannot be
    (the residual reaches ~28-30.8 $bn at 1989, a pure rounding artifact of
    transcribing the book's independently-rounded B1/EC, T1/EC, Ntrrate rows).
    The reconstruction dollar identity therefore now lives on the preserved
    S607-RECON-A arm, which this test still enforces exactly.
    """
    s604 = _series_column(_read_chopped("S604"), "S604-A")
    s605 = _series_column(_read_chopped("S605"), "S605-A")
    s606 = _series_column(_read_chopped("S606"), "S606-A")
    s607_recon = _series_column(_read_chopped("S607"), "S607-RECON-A")

    expected = s605 + s606 - s604
    diffs = _identity_diffs(s607_recon, expected, abs_tol=1e-2)
    if not diffs.empty:
        pytest.fail(
            f"S607-RECON-A != S605-A + S606-A - S604-A for {len(diffs)} year(s):\n"
            f"{diffs.head(10).to_string()}"
        )


@pytest.mark.identity
@pytest.mark.xfail(
    reason="DIV-064 + DIV-066 (2026-07-02): the book-faithful S607-A primary is "
    "Ntrrate*EC from Appendix N Table N.2/N.1, NOT the reconstruction sum "
    "B+G-T; the book's 2-decimal rate rounding makes it non-additive by "
    "construction (residual ~28-30.8 $bn). Divergence is intentional and "
    "registered; the reconstruction identity is enforced on S607-RECON-A.",
    strict=True,
)
def test_S607_book_primary_nonadditive_expected_xfail():
    s604 = _series_column(_read_chopped("S604"), "S604-A")
    s605 = _series_column(_read_chopped("S605"), "S605-A")
    s606 = _series_column(_read_chopped("S606"), "S606-A")
    s607_book = _series_column(_read_chopped("S607"), "S607-A")

    expected = s605 + s606 - s604
    diffs = _identity_diffs(s607_book, expected, abs_tol=1e-3)
    assert diffs.empty, "book primary matches reconstruction sum (unexpected)"
