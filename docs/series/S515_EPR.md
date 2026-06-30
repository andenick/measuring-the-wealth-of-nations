# EPR: S515 — Productive Employment (Lp)

**Series**: S515
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated (extension block populated; book-period KB digitization covers 1948–1961; extension execution pending in L01/P02)

## 1. shaikh_source

"Productive labor is the production labor employed in capitalist production sectors: agriculture, mining, construction, transportation and public utilities, manufacturing, and productive services (defined as all services except business services, legal services, and private households, as in Table E.1)." — Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, p. 109. The component definitions used to assemble Lp are also given on p. 109: "L_j = total employment in jth sector (from NIPA) = 'persons engaged in production' (PEP) = full-time equivalent employees (FEE) + self-employed persons (SEP); L = ∑L_j = total labor; (Lp/L)_j = ratio of production/total workers in jth production sector (BLS); (Lp)_j = (Lp/L)_j · (L_j) = estimated production worker employment in the jth production sector."

## 2. shaikh_appendix_ref

Appendix E.3 (productive employment Lp series, 1948–1961 in the salvaged KB digitization); Table 5.7 (productive labor share Lp/L); Appendix C (productive/unproductive sector concordance). The book's full 1948–1989 series exists in print; the current KB digitization covers 1948–1961.

## 3. extension_source

DIRECT-fetch composite. Extension uses BLS CES (Current Employment Statistics) industry-level production-worker employment, aggregated through the Shaikh–Tonak Appendix C productive/unproductive concordance updated to NAICS industries. Cached input: `data/raw/bls/bls_ces_production_workers.csv` (provenance in `provenance.json`). Concretely: for each NAICS industry mapped to a "productive" sector under the updated Appendix C, the CES production-worker series (CES code ending in `08` for production/nonsupervisory workers within the AE Employment, All Employees super-table family) is pulled; sums across productive sectors give Lp.

## 4. extension_url

- BLS CES landing page: https://www.bls.gov/ces/
- BLS CES production / nonsupervisory workers data: https://www.bls.gov/webapps/legacy/cesbtab2.htm
- BLS Public Data API (v2) endpoint used: https://api.bls.gov/publicAPI/v2/timeseries/data/

See `data/raw/bls/provenance.json` for the exact series IDs cached.

## 5. conceptual_continuity

Shaikh & Tonak define Lp as the count of workers employed in productive sectors and engaged in production activity within those sectors, with the partition fixed by Appendix C (Ch. 5, p. 109; Table 5.7). The construct is directly observable in BLS CES at the industry level: BLS publishes "production and nonsupervisory workers" by NAICS industry continuously since 1964 (SIC basis) and on a comparable NAICS basis since 2003. Conceptual continuity is high *provided* Appendix C is updated to the NAICS taxonomy — without this update, the partition drifts (e.g., misclassifying NAICS 51 information industries or modern logistics sub-industries). The KB coverage gap 1962–1989 in the book series is a digitization artifact, not a data-availability issue: the book's print Appendix E.3 covers all 1948–1989; a fuller KB extraction or a BLS-based reconstruction would close the gap.

## 6. vintage_note

Book vintage: BLS CES SIC-basis 1948–1989 production-worker series, with Shaikh–Tonak's then-current Appendix C concordance. Modern vintage: BLS CES NAICS basis from 2003 forward (the 2003 SIC→NAICS overhaul is the single largest series-break); pre-2003 SIC-basis values are not directly comparable level-by-level to post-2003 NAICS-basis values without crosswalk adjustment. Last cached fetch: see `data/raw/bls/provenance.json`. Extension splice method is `level` (the count series is rebased at the latest available book endpoint and carried forward), appropriate because the construct is directly observable in both eras. Book-period registry `year_range` is honestly recorded as [1948, 1961] reflecting the current KB digitization extent.

## 7. Super-sector aggregation caveat (Stage 5 execution note, 2026-05-23)

The cached BLS CES file `bls_ces_production_workers.csv` contains only the 5 super-sector aggregates (total private; goods-producing; mining/logging; construction; manufacturing). The book's Appendix C concordance partitions 85 SIC sectors and additionally classifies productive labor in transportation/public utilities and certain productive services. Faithful 85-sector reconstruction is **not possible from the cached super-sector data alone**.

The Stage 5 extension therefore uses the following honest super-sector approximation:
- **Raw Lp_ext** = sum of production workers in the 3 productive goods-producing super-sectors (mining/logging + construction + manufacturing) from CES1000000006, CES2000000006, CES3000000006, in thousands, 1948-2024.
- **Splice anchor**: 1961, the latest available book endpoint in the current KB digitization of Appendix E.3 (S515-A covers 1948-1961). When/if the book-period digitization is extended through 1989, the anchor should move to 1989 (a constant in P02_S515 controls this).
- **Multiplicative level splice**: raw BLS Lp at 1961 ≈ 8,099 (thousands); book Lp at 1961 = 33,615; scale factor ≈ 4.15. Post-1961 raw values are multiplied by this scale to anchor the level. The multiplicative form preserves the growth-rate trajectory of the raw BLS series, appropriate because both series are non-negative levels.

Acknowledged divergence: extension uses BLS CES 5-super-sector aggregation; book values use 85 SIC sectors per Appendix C; this divergence is **documented as an acknowledged caveat**. Sample spliced extension values: EXT[1995]=39,063, EXT[2010]=29,098, EXT[2024]=35,081 (thousands). Because the splice anchor is 1961 (not 1989), the post-1961 trajectory reflects the goods-producing super-sector dynamic rather than the book's broader productive labor concept; this gap should be revisited when fuller book-period digitization is available.
