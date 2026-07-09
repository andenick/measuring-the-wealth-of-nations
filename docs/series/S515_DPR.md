# S515 — Productive Employment (Lp), narrow classification

**Chapter**: 5
**Source Table**: Appendix E.3 (Labor Statistics), p. 320, row `Lp_total`
**Units**: thousands of workers
**Period**: 1948-2024 (book arm 1948-1989; extension 1990-2024)
**Content Type**: time_series
**Status**: validated_book_and_extension

> **v1.3 note:** Status widened from `book_period_partial_1948_1961` to `book_period_validated`. The panel-backed rebuild (B6) supplies real book-arm data across the full book period 1948-1989; V03 PASS post-rebuild.
>
> **REVIEW_2026-07 item D2 note:** The extension was rebuilt with the book's own share×total construction (candidate (d), user-ratified — see `internal-review-notes_2026-07/S515_S516_SEAM_REDESIGN.md`). The splice/anchor year is now **1989** for both S515 and S516 (the pre-review code wrongly anchored S515 at 1961, discarding 28 years of genuine book data 1962-1989). `TableE3_LaborStatistics.csv` covers the **full book period 1948-1989** — the earlier "1948-1961 only" coverage claim was false and has been removed throughout.

## Definition

Total productive employment count, summed across sectors with the book's NARROW productive classification (which is more conservative than the BROAD classification used in Table 5.7 / S511).

## Classification Note (important)

The book uses two productive labor definitions:

- **Broad** (Table 5.7, S511): Lp/L = 0.57 in 1948. Includes a wider set of activities as productive.
- **Narrow** (Table E.3, S515): Lp/L = 0.454 in 1961. More conservative; excludes some borderline categories.

Both are book-published. They serve different analytical purposes:
- S511 (broad) drives the exploitation rate decomposition (V*/W).
- S515 (narrow) is the headcount basis for sector-by-sector labor reconciliation.

The new build keeps BOTH series as first-class, with this DPR documenting the boundary distinction. Cross-checking the two ratios is a useful sensitivity analysis but a difference is not a bug.

> **D2-rebuild correction:** the panel-backed `TableE3` Lp_total gives Lp/L = 0.566 (1948), 0.454 (1961), 0.363 (1989) — see the verified anchors below. Those replace the pre-rebuild degraded-KB values (the old "0.453 in 1948" figure was a mislabeled 1961 value). The D2 extension consumes the **S511 productive share** for both series, so the S515 book arm and the S511 share are reconciled on one productive perimeter rather than treated as divergent narrow/broad head-counts.

## Source

`TableE3_LaborStatistics.csv` is wide-by-year (years 1948-1989 are column headers, sectors are rows). The L01 loader transposes the Lp_total row to a year-indexed series.

## Reference

`Lp_total` row values verified directly against Table 5.5 / Appendix F Table F.1 / `TableE3_LaborStatistics.csv` (all three agree exactly):
- 1948 = 32,994 thousand (Lp/L = 0.566)
- 1961 = 29,363 thousand (Lp/L = 0.454)
- 1989 = 41,148 thousand (Lp/L = 0.363)
Validator PASS.

## Extension (1990-2024) — book share×total construction

The extension follows the book's own method (FULL_TEXT.md L449, verbatim): `(Lp)j = (Lp/L)j·Lj`, `Lp = Σ(Lp)j`, `Lu = L − Lp`. In practice the productive **share** Lp/L is the estimated primitive, and Lp is that share applied to total employment:

- **S515-EXT** = S511 productive share × book-anchored total employment L. The share is the clean, workpackage A-certified **S511-COMBINED** series (BLS CES super-sector Lp/L, additively level-spliced at 1989). Total employment L is BLS CES **total nonfarm all employees including government** (series `CES0000000001`, `data/raw/Inputs/API_Data/BLS/bls_ces_total_nonfarm_all_employees.csv`), multiplicatively re-anchored to the book L (113,511) at 1989. (The pre-review code used total *private* employees CES0500000001, which dropped government and caused the −22% Lu break.)
- **S515-COMBINED** = S515-A (book Lp_total, 1948-1989 book values retained) spliced to S515-EXT (1990-2024) at 1989.

Residual concept gap: the total-employment universe excludes self-employed and agriculture; this establishment-vs-household divergence is corrected at the 1989 anchor and is a documented DIV, not a defect. The 2003 SIC→NAICS CES overhaul (DIV-010 family) still applies to the share and the constructible arm below.

**Achieved seam** (extension 1990 vs book 1989): Lp **−0.7%** (book 41,148 → EXT 40,844.8) — continuous, within the 5% guard (previously −15%).

Sample extension values (`data/final/S515.csv`, `series_id == 'S515-EXT'`, thousands): EXT[1995] = 41,913.3, EXT[2010] = 38,783.9, EXT[2024] = 46,296.4.

### Honesty / transparency arms

Per the S506/S512 two-arm pattern, two additional distinct measures are retained (never consumed as the published Lp):

- **S515-EXT-CONSTRUCTIBLE** — the raw 3-super-sector production-worker count (mining/logging + construction + manufacturing, CES…0006), UNSPLICED. This is the honest BLS-native measure but captures only ~half the book's productive perimeter (super-sector Lp/L ≈ 0.195 vs book 0.363). Sample values: 1990 = 17,321.1; 2024 = 15,392.4 (thousands).
- **S515-EXT-OLD-DEPRECATED** — the frozen pre-review arm (raw super-sector count level-spliced at 1961). DEPRECATED, retained for transparency only; it discarded book data 1962-1989 — do not consume. Sample values: 1990 = 34,483.4; 2024 = 30,643.7 (thousands).

---

*Generated by anu-ingestion (re-authored from scratch).*

> Status upgraded book_period_validated -> validated_book_and_extension on 2026-07-07 (Phase-0 truth baseline, T3): populated extension block + -EXT/-COMBINED subseries + book-arm V03 PASS; parity with the pre-existing validated_book_and_extension series. See registry field `status_adjudication_2026_07_07`.