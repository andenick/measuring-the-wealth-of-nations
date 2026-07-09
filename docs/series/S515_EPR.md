# EPR: S515 — Productive Employment (Lp)

**Series**: S515
**Generated**: 2026-05-23T00:00:00Z
**Status**: validated_book_and_extension (book arm 1948-1989 from TableE3; extension 1990-2024 built by P02 via the book share×total method — REVIEW_2026-07 item D2)

## 1. shaikh_source

"Productive labor is the production labor employed in capitalist production sectors: agriculture, mining, construction, transportation and public utilities, manufacturing, and productive services (defined as all services except business services, legal services, and private households, as in Table E.1)." — Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, p. 109. The component definitions used to assemble Lp are also given on p. 109: "L_j = total employment in jth sector (from NIPA) = 'persons engaged in production' (PEP) = full-time equivalent employees (FEE) + self-employed persons (SEP); L = ∑L_j = total labor; (Lp/L)_j = ratio of production/total workers in jth production sector (BLS); (Lp)_j = (Lp/L)_j · (L_j) = estimated production worker employment in the jth production sector."

## 2. shaikh_appendix_ref

Appendix E.3 / Table 5.5 (productive employment Lp series, **full book period 1948–1989**, digitized in `TableE3_LaborStatistics.csv`); Table 5.7 (productive labor share Lp/L); Appendix C (productive/unproductive sector concordance). The full 1948–1989 book series is present in the canonical panel — the earlier "digitization covers 1948–1961" claim was false and has been removed.

## 3. extension_source

SHARE×TOTAL composite, following the book's own construction (FULL_TEXT.md L449: `(Lp)j = (Lp/L)j·Lj`, `Lp = Σ(Lp)j`). **S515-EXT = productive share × total employment L**, anchored at 1989:

- **Productive share** = the clean, workpackage A-certified **S511-COMBINED** series (BLS CES super-sector Lp/L, additively level-spliced at 1989). S515 consumes this share rather than re-deriving Lp from a truncated head-count.
- **Total employment L** = BLS CES **total nonfarm all employees including government** (series `CES0000000001`), cached at `data/raw/Inputs/API_Data/BLS/bls_ces_total_nonfarm_all_employees.csv`, multiplicatively re-anchored to the book L (113,511) at 1989.
- Then `Lp = share · L`; S516 takes `Lu = L − Lp` on the same L basis.

This retires the pre-review method (raw sum of production workers in 3 goods-producing super-sectors level-spliced at 1961), which is now kept only as the break-flagged `S515-EXT-CONSTRUCTIBLE` and `S515-EXT-OLD-DEPRECATED` transparency arms (§7).

## 4. extension_url

- BLS CES landing page: https://www.bls.gov/ces/
- BLS CES production / nonsupervisory workers data: https://www.bls.gov/webapps/legacy/cesbtab2.htm
- BLS Public Data API (v2) endpoint used: https://api.bls.gov/publicAPI/v2/timeseries/data/

See `data/raw/Inputs/API_Data/BLS/provenance.json` for the exact series IDs cached.

## 5. conceptual_continuity

Shaikh & Tonak define Lp as the count of workers employed in productive sectors and engaged in production activity within those sectors, with the partition fixed by Appendix C (Ch. 5, p. 109; Table 5.7). The construct is directly observable in BLS CES at the industry level: BLS publishes "production and nonsupervisory workers" by NAICS industry continuously since 1964 (SIC basis) and on a comparable NAICS basis since 2003. Conceptual continuity is high because the extension estimates the productive **share** (S511) and applies it to a book-anchored total employment L, exactly as the book does — rather than estimating a truncated Lp level directly. There is **no** book-series coverage gap: `TableE3_LaborStatistics.csv` covers all of 1948–1989, so S515-A/S515-COMBINED retain every genuine book year and the extension continues from a matched level at the true 1989 overlap.

## 6. vintage_note

Book vintage: BLS CES SIC-basis 1948–1989 production-worker series, with Shaikh–Tonak's then-current Appendix C concordance. Modern vintage: BLS CES NAICS basis from 2003 forward (the 2003 SIC→NAICS overhaul is the single largest series-break); pre-2003 SIC-basis values are not directly comparable level-by-level to post-2003 NAICS-basis values without crosswalk adjustment (the DIV-010 SIC→NAICS family still applies to the S511 share and to the constructible arm). Last cached fetch: see `data/raw/Inputs/API_Data/BLS/provenance.json`. The extension splice/anchor is at **1989**: the S511 share is level-spliced at 1989 and total employment L is multiplicatively re-anchored to the book L at 1989, so `Lp = share·L` is continuous across the seam. Book-period registry `year_range` is [1948, 1989] — the full book period digitized in `TableE3`.

## 7. Extension construction + honesty arms (REVIEW_2026-07 item D2, 2026-07-02)

The published extension no longer estimates Lp directly from a truncated super-sector head-count. Instead it applies the book's share×total rule with the clean S511 share (§3):

- **S515-EXT** = `S511-COMBINED` productive share × book-anchored total employment `L`, where `L` = BLS CES total nonfarm all employees **including government** (`CES0000000001`, `data/raw/Inputs/API_Data/BLS/bls_ces_total_nonfarm_all_employees.csv`) multiplicatively re-anchored to book L (113,511) at 1989. **S515-COMBINED** = book S515-A (1948-1989) spliced to S515-EXT (1990-2024) at 1989.
- **Achieved seam** (extension 1990 vs book 1989): Lp **−0.7%** (41,148 → 40,844.8) — continuous, within the 5% guard (was −15%). Sample extension values (`data/final/S515.csv`, `S515-EXT`, thousands): EXT[1995] = 41,913.3, EXT[2010] = 38,783.9, EXT[2024] = 46,296.4.
- **Residual concept gap** (documented DIV, not a defect): the total-employment universe excludes self-employed and agriculture (establishment-vs-household); this is corrected at the 1989 anchor. The productive-perimeter narrowing on the super-sector share and the 2003 SIC→NAICS overhaul (DIV-010 family) still apply to the share.

Two honest transparency arms are retained (S506/S512 two-arm pattern; neither is the published Lp):

- **S515-EXT-CONSTRUCTIBLE** — raw sum of production workers in the 3 goods-producing super-sectors (mining/logging CES1000000006 + construction CES2000000006 + manufacturing CES3000000006), UNSPLICED, 1948-2024. A DISTINCT break-flagged measure capturing ~half the book's productive perimeter (super-sector Lp/L ≈ 0.195 vs book 0.363). Sample: 1990 = 17,321.1; 2024 = 15,392.4 (thousands).
- **S515-EXT-OLD-DEPRECATED** — the frozen pre-review arm (raw super-sector count level-spliced at 1961, scale ≈ 1.99 = book Lp 29,363 / raw 14,749 @1961). DEPRECATED, retained for transparency only; it discarded book data 1962-1989 — do not consume. Sample: 1990 = 34,483.4; 2024 = 30,643.7 (thousands).
