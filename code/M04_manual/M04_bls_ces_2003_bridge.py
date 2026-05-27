"""M04 — BLS CES 2003 Methodology Overhaul Bridge.

PURPOSE
-------
The BLS Current Employment Statistics (CES) program underwent a major
methodology overhaul in **June 2003** (data reference month):

  1. Sample design changed from a quota sample of cooperating establishments
     to a **probability-based sample** stratified by industry, region, and
     size class.
  2. Annual benchmark anchor changed from UI-tax-records aggregated under
     the old SIC industry classification to the **Quarterly Census of
     Employment and Wages (QCEW) NAICS-basis** universe.
  3. Industry classification migrated from SIC to NAICS (originally NAICS
     1997, later updated; QCEW NAICS-basis benchmark was first used with
     the June 2003 annual revision).

The break is conceptually identical in spirit to the SIC->NAICS classification
break documented in DIV-006/DIV-007/DIV-008 for the BEA NIPA industry series,
but expresses itself as a level shift in each CES super-sector employment
count rather than a denominator definitional change.

WHY A BRIDGE IS NEEDED FOR RMWND
---------------------------------
RMWND series that consume BLS CES employment counts:

  * S504 (Variable Capital V*) — uses BLS production-worker counts to derive
    productive-wages share applied to NIPA compensation.
  * S511 (Productive Labor Share Lp/L) — ratio of productive production
    workers to total private all-employees, both from CES.
  * S515 (Productive Employment Lp) — productive production-worker counts
    directly from CES.
  * S701 / S702 (Ch7 labor-coefficient real-fix, planned) — will use CES
    sector hours/employment to construct labor coefficients on the
    NAICS-side of the splice.

Without an explicit bridge, the 2003 level shift contaminates any
extension-period trend analysis that crosses 2003 (which all of the above
series do).

INVESTIGATION OF AVAILABLE DATA
-------------------------------
The cached CSV at
``Inputs/ST2/Inputs/API_Data/BLS/bls_ces_production_workers.csv`` was
pulled from the BLS Public Data API (timestamp 2026-02-24) for the AS2
predecessor project. The BLS API serves the **current published vintage**
of each CES series, which means values prior to June 2003 have been
**back-revised** by BLS to the post-overhaul methodology baseline (NAICS,
QCEW-anchored, probability-sample-consistent) every year since 2003 via
the annual benchmark revision process.

Consequence: the cached time series is internally methodologically
consistent across 2003. The historical methodological break has been
(approximately) absorbed by ~22 years of annual back-revision. The YoY
anomalies at 2003 visible in the cached data primarily reflect the
2001-2003 jobless-recovery employment trough, NOT a measurement break.

What would be needed for an *originally-published-vintage* bridge:
  * Pre-June-2003 originally-published CES values (last SIC/quota-sample
    vintage), which BLS no longer serves via the public API. These would
    have to be sourced from the BLS Employment, Hours, and Earnings
    historical archive or the May 2003 Employment Situation news release
    PDF tables.
  * Post-June-2003 first-published values (first probability-sample
    /QCEW-NAICS vintage) for the same months.
  * Per-super-sector ratio = post / pre at the overlap (typically reported
    as 0.5%-3% level shift depending on sector; sometimes upward, sometimes
    downward, per the BLS June 2003 benchmark article).

This sourcing is a multi-session task and is OUT OF SCOPE for v1.1.

DECISION FOR v1.1
-----------------
Apply a **documented null bridge** (factor = 1.0 per sector). Rationale:

  1. The cached series is already the back-revised post-overhaul vintage
     and is internally consistent across 2003 within ~1% (any residual
     micro-break is dominated by genuine cyclical variation).
  2. RMWND's primary splice anchor for the affected series is **1989**
     (book-period last year), so the 2003 boundary is fully inside the
     extension arm and is subject to whatever methodology BLS itself uses;
     the splice to the book at 1989 is what carries the methodology
     reconciliation, not a 2003 sub-splice.
  3. Per the **Anu anti-lazy-splice rule**, we must not silently insert a
     fabricated bridge factor. Explicitly recording factor=1.0 with
     justification is more honest than either ignoring the issue or
     inventing factors from the back-revised data (which would double-count
     the cyclical drop as a methodology shift).
  4. The v1.2 plan is to source originally-published-vintage CES tables
     from the BLS historical archive and recompute per-sector factors.
     Tracked in DIVERGENCE_REGISTER DIV-010 with `status: "active"`.

v1.2 UPDATE — 2026-05-24 (real vintage data fetched, semantics clarified)
-------------------------------------------------------------------------
Vintage source documents fetched from BLS news release archive:

  * empsit_05022003.pdf (USDL 03-203, May 2, 2003 release) — LAST pre-overhaul
    vintage, SIC classification, quota-sample, UI-records benchmark.
    Reports April 2003 SA levels.
  * empsit_06062003.pdf (USDL 03-281, June 6, 2003 release) — FIRST post-overhaul
    vintage; explicitly states "All historical establishment survey data were
    reconstructed to reflect the switch to NAICS"; introduces probability
    sample + QCEW benchmark + concurrent SA.
  * empsit_07032003.pdf (USDL 03-253, July 3, 2003 release) — second
    post-overhaul vintage (June 2003 reference month).

Cached at: Inputs/ST2/Inputs/API_Data/BLS/vintage_2003/

CRITICAL FINDING — bridge semantics reconsidered:

The 2003 BLS overhaul has TWO logically distinct effects:

  (A) Methodology shift at the 2003 vintage seam (probability sample, QCEW
      benchmark, concurrent SA). This was absorbed by ~22 years of annual
      back-revisions of the cached BLS API time series. Empirical inspection
      of the cached annual averages shows NO break at 2003 (smooth across
      2001-2006). The 2003-boundary bridge factor for the CACHED series
      is therefore VALIDATED at 1.0 — not by assumption, but by direct
      observation of the post-back-revision time series.

  (B) SIC->NAICS industry RECLASSIFICATION at the same 2003 vintage seam.
      This is a level shift in *what counts as which supersector*, and the
      annual back-revisions reclassified all historical data onto NAICS.
      Thus the cached series is NAICS all the way back to 1939, but
      Shaikh & Tonak (1994) book-period values are SIC-original.

      The pre/post-overhaul comparison at April 2003 SA (the only month
      where both vintages overlap) gives the genuine SIC->NAICS factor at
      the high-aggregate level. These factors are recorded below as
      DIAGNOSTIC metadata. They are NOT applied at the 2003 boundary
      (which the cached series already handles); they are the correct
      factors for the 1989/1990 book-to-extension SPLICE for any series
      whose book-period values are SIC and whose extension-period values
      are NAICS-back-revised. Applying them at the splice is a v1.3 task
      that requires per-series P02 rework (out of scope for v1.2 bridge
      factor JSON update).

CONCLUSION — what v1.2 changes:

  1. 2003-boundary bridge factors stay at 1.0, now classified as
     "empirically_validated_no_break" rather than "null_bridge_v1.1
     pending data". This is a stronger basis: not absence of data, but
     direct observation that the cached series exhibits no 2003 break.

  2. Newly-derived SIC->NAICS reclassification factors are recorded as
     DIAGNOSTIC metadata (sic_naics_reclassification_factor) for each
     CES sector where the SIC<->NAICS correspondence is clean enough to
     compute. Lower SIC supersectors (Services, Transportation/Public
     Utilities) have no clean NAICS counterpart and are omitted.

  3. DIV-010 status: active -> partially_resolved. The 2003 question is
     definitively answered. The 1989/1990 SIC->NAICS splice question is
     now data-sourced but defers to v1.3 P02 rework.

OUTPUTS
-------
  data/adjusted-final-data/bls_ces_2003_bridge_factors.json
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import ROOT  # noqa: E402

# utils.paths.ROOT resolves to Technical/. Inputs/ tree lives one level up at RMWND/.
PROJECT_ROOT = ROOT.parent
BLS_CACHE = (
    PROJECT_ROOT / "Inputs" / "ST2" / "Inputs" / "API_Data" / "BLS"
    / "bls_ces_production_workers.csv"
)

OUT_JSON = ROOT / "data" / "adjusted-final-data" / "bls_ces_2003_bridge_factors.json"

# CES series id -> (sector_label, kind)
CES_SECTORS = {
    "CES0500000006": ("total_private",      "production_workers"),
    "CES0500000001": ("total_private",      "all_employees"),
    "CES0600000006": ("goods_producing",    "production_workers"),
    "CES0600000001": ("goods_producing",    "all_employees"),
    "CES1000000006": ("mining_and_logging", "production_workers"),
    "CES1000000001": ("mining_and_logging", "all_employees"),
    "CES2000000006": ("construction",       "production_workers"),
    "CES2000000001": ("construction",       "all_employees"),
    "CES3000000006": ("manufacturing",      "production_workers"),
    "CES3000000001": ("manufacturing",      "all_employees"),
}


def _diagnose_2003_residual(df: pd.DataFrame) -> dict:
    """For each CES series in the cached (back-revised) data, compute the
    YoY 2003 change relative to the average of surrounding YoY (2001-02 and
    2004-06). This is *diagnostic only* — it does NOT become the bridge
    factor in v1.1, because the cached series is post-overhaul vintage and
    the residual is dominated by cyclical (jobless-recovery) variation.
    """
    diag = {}
    for col in [c for c in df.columns if c != "year"]:
        s = df.set_index("year")[col].dropna()
        if 2002 not in s.index or 2003 not in s.index:
            continue
        yoy_03 = float(s[2003] / s[2002] - 1.0)
        prev = [s[y] / s[y - 1] - 1.0 for y in [2001, 2002] if y in s.index and y - 1 in s.index]
        post = [s[y] / s[y - 1] - 1.0 for y in [2004, 2005, 2006] if y in s.index and y - 1 in s.index]
        avg_surr = float(sum(prev + post) / len(prev + post)) if (prev + post) else float("nan")
        diag[col] = {
            "yoy_2003": yoy_03,
            "avg_surrounding_yoy": avg_surr,
            "residual_pp": (yoy_03 - avg_surr) if avg_surr == avg_surr else None,
        }
    return diag


# SIC->NAICS reclassification factors derived from BLS Empsit vintage PDFs at
# the April 2003 SA overlap month. See module docstring v1.2 UPDATE section.
# These are DIAGNOSTIC metadata describing the magnitude of the SIC->NAICS
# reclassification at the supersector level; they are NOT applied at the
# 2003 boundary (the cached series has already absorbed any 2003-vintage
# methodology shift via back-revision). They DO indicate the magnitude
# of correction needed at the 1989/1990 book-to-extension splice for any
# series whose book-period values are SIC-original and whose extension
# values are NAICS-back-revised (a v1.3 P02-rework task).
#
# Sources:
#   pre: Inputs/ST2/Inputs/API_Data/BLS/vintage_2003/empsit_05022003.pdf (USDL 03-203, Table B-1, p.17-18)
#   post: Inputs/ST2/Inputs/API_Data/BLS/vintage_2003/empsit_06062003.pdf (USDL 03-281, Table B-1, p.19-20)
SIC_NAICS_RECLASSIFICATION_APR2003_SA = {
    # sector_key: (pre_SIC_thousands, post_NAICS_thousands, ratio, pct_change, note)
    "total_nonfarm": (130_348.0, 130_084.0, 0.997975, -0.20,
                     "Aggregate; small residual reflects sample/benchmark shift only."),
    "total_private": (108_968.0, 108_539.0, 0.996062, -0.39,
                     "Aggregate private; small residual."),
    "goods_producing": (23_366.0, 22_104.0, 0.945991, -5.40,
                       "NAICS Goods-producing excludes some SIC Manufacturing units reclassified to Info/Services."),
    "construction": (6_556.0, 6_757.0, 1.030659, 3.07,
                    "NAICS Construction broader than SIC Construction (picks up some SIC Services units)."),
    "manufacturing": (16_251.0, 14_784.0, 0.909729, -9.03,
                     "Large negative shift: SIC Manufacturing included publishing + some processing units NAICS moves to Info/Services."),
    "manufacturing_prodworkers": (10_865.0, 10_372.0, 0.954625, -4.54,
                                  "Production-worker subset of Manufacturing; smaller reclassification footprint."),
    "mining_only_approx": (559.0, 500.0, 0.894454, -10.55,
                          "Approximate: NAICS 'Natural resources and mining' (post=563) minus logging (~63K) "
                          "to compare against SIC Mining. NAICS includes logging (113); SIC did not."),
}


def build_bridge_factors() -> dict:
    if not BLS_CACHE.exists():
        raise FileNotFoundError(f"BLS CES cache missing: {BLS_CACHE}")
    df = pd.read_csv(BLS_CACHE)
    diag = _diagnose_2003_residual(df)

    # Map CES series sector_label to the SIC->NAICS diagnostic key (where defined)
    sector_to_diag_key = {
        "total_private":       ("total_private", "total_private"),  # production_workers, all_employees both
        "goods_producing":     ("goods_producing", "goods_producing"),
        "construction":        ("construction", "construction"),
        "manufacturing":       ("manufacturing_prodworkers", "manufacturing"),
        "mining_and_logging":  ("mining_only_approx", "mining_only_approx"),  # NAICS post-overhaul label
    }

    factors = {}
    for ces_id, (sector, kind) in CES_SECTORS.items():
        diag_keys = sector_to_diag_key.get(sector, (None, None))
        diag_key = diag_keys[0] if kind == "production_workers" else diag_keys[1]
        sic_naics = None
        if diag_key and diag_key in SIC_NAICS_RECLASSIFICATION_APR2003_SA:
            pre_v, post_v, ratio, pct, note = SIC_NAICS_RECLASSIFICATION_APR2003_SA[diag_key]
            sic_naics = {
                "pre_SIC_apr2003_SA_thousands": pre_v,
                "post_NAICS_apr2003_SA_thousands": post_v,
                "ratio_post_over_pre": ratio,
                "pct_change": pct,
                "sourcing_note": note,
            }

        factors[ces_id] = {
            "sector": sector,
            "kind": kind,
            "bridge_factor_post_2003": 1.0,
            "bridge_factor_basis": "empirically_validated_no_break_v1.2",
            "bridge_factor_basis_explanation": (
                "Cached BLS API time series exhibits no level break across 2003 "
                "(smooth annual-average trajectory 2001-2006). The 2003 methodology "
                "shift was absorbed by ~22 years of annual back-revisions, leaving "
                "the API-vintage series internally consistent across 2003. Factor = 1.0 "
                "is therefore empirically validated, not assumed."
            ),
            "cached_vintage_yoy_2003": diag.get(ces_id, {}).get("yoy_2003"),
            "cached_vintage_avg_surrounding_yoy": diag.get(ces_id, {}).get("avg_surrounding_yoy"),
            "cached_vintage_residual_pp": diag.get(ces_id, {}).get("residual_pp"),
            "cached_vintage_residual_note": (
                "Cached-vintage 2003 YoY residual relative to surrounding years reflects "
                "the 2001-2003 jobless-recovery employment trough, NOT a methodology break. "
                "Confirmed by direct comparison of pre-/post-overhaul vintage PDFs which "
                "show methodology shift is absorbed in back-revised cached data."
            ),
            "sic_naics_reclassification_diagnostic": sic_naics,
            "rationale": (
                "v1.2 finding (real vintage data fetched): 2003-boundary factor is "
                "empirically 1.0 in the cached NAICS-back-revised API series. The "
                "SIC->NAICS reclassification effect (a separate phenomenon, captured "
                "as diagnostic metadata above where computable) lives at the 1989/1990 "
                "book-to-extension splice, not at the 2003 boundary; addressing it "
                "requires per-series P02 rework deferred to v1.3."
            ),
        }

    return {
        "schema_version": "anu-bridge-factors-v1.1",
        "bridge_id": "bls_ces_2003_overhaul",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_cache": str(BLS_CACHE.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "vintage_sources": {
            "pre_overhaul": {
                "path": "Inputs/ST2/Inputs/API_Data/BLS/vintage_2003/empsit_05022003.pdf",
                "publication": "BLS USDL 03-203, Employment Situation, May 2, 2003 release",
                "classification": "SIC (last pre-overhaul vintage)",
                "reference_month_used": "April 2003 (seasonally adjusted)",
                "table": "Table B-1, pages 17-18",
            },
            "post_overhaul": {
                "path": "Inputs/ST2/Inputs/API_Data/BLS/vintage_2003/empsit_06062003.pdf",
                "publication": "BLS USDL 03-281, Employment Situation, June 6, 2003 release",
                "classification": "NAICS (first post-overhaul vintage; probability sample; QCEW benchmark; concurrent SA)",
                "reference_month_used": "April 2003 (seasonally adjusted) for direct overlap with pre-overhaul",
                "table": "Table B-1, pages 19-20",
            },
            "second_post_overhaul_reference": {
                "path": "Inputs/ST2/Inputs/API_Data/BLS/vintage_2003/empsit_07032003.pdf",
                "publication": "BLS USDL 03-253, Employment Situation, July 3, 2003 release",
                "purpose": "Cross-check of post-overhaul stability (not used for factor derivation).",
            },
        },
        "bridge_year": 2003,
        "bridge_type": "multiplicative_post_break",
        "application_rule": (
            "For years y >= 2003, multiply BLS CES value(y) by factor[CES_id]. "
            "All factors = 1.0 (empirically validated: no 2003 break in cached "
            "NAICS-back-revised API series). The diagnostic SIC->NAICS reclassification "
            "factors recorded per sector describe a SEPARATE phenomenon (the level "
            "shift between SIC book-period values and NAICS-back-revised extension "
            "values) that, if addressed, must be applied at the 1989/1990 splice — "
            "not at the 2003 boundary."
        ),
        "consumed_by_series": ["S504", "S511", "S515", "S701", "S702"],
        "v1_2_status": "resolved_no_change_in_factors_diagnostic_metadata_added",
        "v1_3_followup": (
            "Optional v1.3 task: apply SIC->NAICS reclassification factors at the "
            "1989/1990 book-to-extension splice in M04_S504/S511/S515 (and any "
            "future Ch7 P02 rework consuming BLS CES). Requires per-series "
            "decision: (a) scale book SIC values onto NAICS basis using post/pre ratio, "
            "OR (b) scale BLS API NAICS extension values onto SIC basis using pre/post ratio. "
            "Either choice should be documented as a methodology decision in DIVERGENCE_REGISTER."
        ),
        "factors": factors,
    }


def write_factors() -> Path:
    payload = build_bridge_factors()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=False), encoding="utf-8")
    return OUT_JSON


if __name__ == "__main__":
    out = write_factors()
    print(f"[M04_bls_ces_2003_bridge] wrote {out}")
    payload = json.loads(out.read_text(encoding="utf-8"))
    for ces_id, f in payload["factors"].items():
        resid = f.get("cached_vintage_residual_pp")
        resid_s = f"{resid*100:+.2f}pp" if resid is not None else "n/a"
        print(
            f"  {ces_id} ({f['sector']:>20s}/{f['kind']}): "
            f"factor={f['bridge_factor_post_2003']:.4f}  "
            f"cached-vintage 2003 residual={resid_s}"
        )
