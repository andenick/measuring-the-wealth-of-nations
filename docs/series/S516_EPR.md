# EPR: S516 — Unproductive Employment (Lu = L − Lp)

**Series**: S516
**Generated**: 2026-05-23T00:00:00Z
**Status**: validated_book_and_extension (book arm 1948-1989 from TableE3; extension 1990-2024 = L − Lp on one book-anchored L basis — REVIEW_2026-07 item D2)

## 1. shaikh_source

"Lu = L − Lp = total unproductive labor." — Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, p. 109. Decomposition on the same page: "Total unproductive labor = nonproduction workers in production sectors + all workers in nonproduction sectors." (The decomposition is informative — Lu has two structural sources — but the operational definition for the time series is the identity Lu = L − Lp.)

## 2. shaikh_appendix_ref

Derived identity from S515 (Lp) and total employment L. The book reports Lu directly in Table 5.7 as the complement of Lp/L; the Appendix E series for Lu is implied by the Appendix E.3 Lp series together with total employment L from NIPA.

## 3. extension_source

DERIVED identity series (NOT a direct fetch). Extension is computed each year as:

    Lu = L_reanchored − S515-EXT

where `S515-EXT` is the published productive employment Lp (S511 share × L; see `S515_EPR.md`) and `L_reanchored` is total nonfarm employment **including government** — BLS CES series `CES0000000001` (all employees, total nonfarm), cached at `data/raw/Inputs/API_Data/BLS/bls_ces_total_nonfarm_all_employees.csv` — multiplicatively re-anchored to the book L (113,511) at 1989. This is the **same** single L basis and anchor year that P02_S515 uses, so `L = Lp + Lu` holds at every year including the seam. (The pre-review build subtracted from total *private* employment CES0500000001, dropping government and driving the −22% Lu break; that bug is retired.)

## 4. extension_url

- BLS CES total nonfarm employment: https://data.bls.gov/timeseries/CES0000000001
- BLS CES landing page: https://www.bls.gov/ces/
- BLS Public Data API (v2): https://api.bls.gov/publicAPI/v2/timeseries/data/
- (Alternative NIPA-basis total employment: https://apps.bea.gov/iTable/iTable.cfm?reqid=19&step=2 — Tables 6.4D / 6.5D)

For the S515 input, see `S515_EPR.md`.

## 5. conceptual_continuity

Shaikh & Tonak define Lu as the residual of the productive/unproductive partition: unproductive employment is total employment minus productive employment (Ch. 5, p. 109; Table 5.7). Because Lu is a derived identity, the modern construct is conceptually identical to the book construct by construction — there is no separate definition to defend, only the consistency of the two inputs (S515 and L_total). Conceptual continuity of Lu therefore reduces entirely to the conceptual continuity of S515 (Appendix C concordance under NAICS) and the continuity of the total-employment measure (BLS CES total nonfarm, which is a stable BLS headline series). All structural questions about which sectors are "productive" live in S515's documentation, not here.

## 6. vintage_note

Book vintage: SIC-basis BLS employment with Shaikh–Tonak's then-current Appendix C concordance, supplying both Lp and L across the **full book period 1948–1989** (digitized in `TableE3_LaborStatistics.csv`; there is no 1962–1989 book gap). Modern vintage: NAICS-basis BLS CES from 2003 forward; the 2003 SIC→NAICS overhaul (DIV-010 family) affects both L and Lp simultaneously and cancels somewhat in the difference, but does not cancel completely because the partition itself changes. Vintage divergences in Lu are inherited from S515 (Appendix C update for NAICS; BLS CES 2003 overhaul). Last cached fetch: see `data/raw/Inputs/API_Data/BLS/provenance.json`. Splice method is `derive` — the splice is induced by S515-EXT + the shared book-anchored L (both anchored at 1989), and there is no independent splice parameter for Lu.
