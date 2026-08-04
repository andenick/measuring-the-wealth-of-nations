# EPR: S517 — Productive Capital Stock (K*)

**Series**: S517
**Generated**: 2026-05-23T00:00:00Z
**Status**: validated_book_and_extension

## 1. shaikh_source

> "We are interested in the productive part of the capital stock K*, which corresponds to the capital tied up in productive industries. … The relevant measure for the rate of profit is capital stock that is measured at current replacement costs." (Shaikh & Tonak 1994, Ch. 5, p. 122)

> "K* = C*f: Fixed nonresidential gross private capital ($ billions)" (Shaikh & Tonak 1994, Ch. 5, Tables 5.8 and 5.9 column gloss, per `data/raw/kb/book_digitization/chunk_15/tables/tables_5.8_and_5.9_summary.md` line 26)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. Chapter 5 (The Marxian Categories: Empirical Estimates); Tables 5.8–5.9 (K* in r* construction); Figures 5.5 and 5.8 (K* time-series plots); Appendix H (K* net stock of fixed capital — text-only in the published volume and not yet extracted in the current KB build).

## 2. shaikh_appendix_ref

Primary: **Appendix H** (K* annual values 1948–1989, text-only — not extracted in the current KB build).
Cross-checks in extracted KB: Tables 5.8 / 5.9 (K* = C*f column, billions current USD; chunk_15 summary); Figures 5.5 and 5.8 (K* plotted as the denominator of r* alongside S* and V*).
Operational book reference (because Appendix H endpoints are unextracted): BEA Fixed Assets Table 4.1 Line 1 (Current-Cost Net Stock) restricted to 1948–1989, with benchmark endpoints 1948=291.557, 1958=551.356, 1967=871.188, 1980=3800.290, 1989=6699.840 (billions current USD). This substitution is documented in `_stage3_patches/S517_v2_patch.json` (iteration 8, Stage 3 cohort 2).

## 3. extension_source

**BEA Fixed Assets Table 4.1, Line 1 — Private nonresidential fixed assets, Current-Cost Net Stock.** Pre-cached at `data/raw/Inputs/API_Data/BEA/fixed_assets_4_1_net_stock.csv` (7600 rows; coverage 1925–2024; BEA API pull dated 2026-02-24; provenance: `data/raw/Inputs/API_Data/BEA/provenance_fixed_assets.json` with `purpose='Capital stock K for profit rate r* = S*/(C*+V*)'`). The extension uses the same underlying BEA series that supplies the book-period operational reference; the splice is therefore trivial (`splice_method=level`, `rescale_factor=1.0`, `splice_year=1989`).

## 4. extension_url

Web interface: https://apps.bea.gov/iTable/?reqid=10&step=2&isuri=1 (select "Fixed Assets", Table 4.1, Current-Cost Net Stock).
API endpoint (constructed): `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=FixedAssets&TableName=FAAt401&Frequency=A&Year=ALL&ResultFormat=JSON` (Line 1 = Private nonresidential fixed assets).

## 5. conceptual_continuity

Productive Capital Stock K* is the current-cost net stock of fixed capital deployed in the productive economy. It is a directly-observed aggregate (not a derived ratio) and is therefore eligible for a level splice under the Anu Extension Standard. Because the book-period operational reference and the extension both draw on the *identical* BEA Fixed Assets Table 4.1 Line 1 series (Private nonresidential, Current-Cost Net Stock), there is no series-change discontinuity to bridge at the 1989/1990 seam: the splice is exact and the rescale factor is 1.0. The only methodological caveat — shared symmetrically across the seam — is that Table 4.1 Line 1 is the aggregate private-nonresidential stock and has not yet been filtered through the 85-IO productive-sector concordance (which would subtract the financial-sector component, estimated 5–10% of the aggregate, and re-aggregate the productive industries: agriculture, mining, construction, manufacturing, transportation, communications, utilities, trade). This refinement is a future Stage 5 task per `docs/IMPLEMENTATION_PLAN.md` Phase 2.A; deferring it leaves both book and extension uniformly biased upward in level (preserving comparability across the splice) rather than imposing an asymmetric correction on one side only.

A second caveat: book Table 5.8 specifies K* = **gross** stock (`C*f` = "Fixed nonresidential gross private capital"), whereas this implementation uses BEA's **net** stock (Current-Cost Net Stock per Table 4.1). The net-stock choice matches the verbatim p. 122 language ("capital stock that is measured at current replacement costs") and is the canonical current-cost denominator for r* in the ST re-implementation framework; for strict gross-stock replication, BEA Table 4.2 (Current-Cost Gross Stock) would be the alternative source (not yet pulled, deferred per the Stage 3 v2 patch). This affects the level (gross > net) but not the qualitative trajectory.

> **Disclosure footnote (added v1.1 Phase 5, iteration 3 coordinator follow-up).** ST 1994 prose calls K* "gross capital stock" (e.g., Table 5.8 header), but published values match BEA Fixed Assets Table 4.1 NET stock exactly at all 5 benchmark years (1948 = 292, 1958 = 551, 1967 = 871, 1980 = 3 800, 1989 = 6 700 $B). The book's terminology is in error; the implementation is net stock. BEA publishes no current-cost gross stock for private nonresidential fixed assets. See `Technical/DIVERGENCE_REGISTER.json` entry **DIV-008** for the full divergence record.

## 6. vintage_note

BEA API pull dated 2026-02-24 (per `data/raw/Inputs/API_Data/BEA/provenance_fixed_assets.json`); represents approximately the late-2025 / early-2026 BEA Fixed Assets vintage. Because the book's Appendix H K* values are text-only and not yet extracted, the operational book reference for S517 uses the same modern BEA Table 4.1 series as the extension — i.e., book values are *not* frozen at the 1993 publication vintage as they are for series with successfully extracted Appendix data (e.g., S501 TP*). Once Appendix H is extracted via a follow-on KB pass, S517-A can be re-anchored to the book-vintage values and the splice re-derived (likely shifting to a non-trivial rescale factor). BEA Fixed Assets is subject to periodic comprehensive revisions (1999, 2003, 2009, 2013, 2018, 2023); these revise back to the start of the series, so both pre- and post-1989 values reflect the 2026-02-24 vintage rather than separate book / extension vintages.

## Book-period Gross-K* variant (2026-07-07, K-plan)

The book (Table 5.8) tabulated a GROSS K* (C*_f). This variant materializes that book-faithful gross axis for the checkable book period; the primary net S517-A runs ~21.8% below it (DIV-058, narrowed here to the extension arm). Book period 1948-1989 only; **no extension** — current-dollar gross stock is genuinely non-constructible from 1990 onward (BEA discontinued current-cost gross-stock reporting at the 1997 comprehensive revision; FA Table 4.2 is a dimensionless Fisher quantity index, not a current-$ series). Materialized as `S517-GROSS-A`, validated against the book's own printed Table 5.8 cells (`validation.variant_reference_values`, full 42-year column). Not primary; the shipped net series is unchanged. See F2_KSTAR_FIDELITY.md + DIV-070.
