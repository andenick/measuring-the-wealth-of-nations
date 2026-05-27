# EPR: S516 — Unproductive Employment (Lu = L − Lp)

**Series**: S516
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated (extension block populated; derived identity; extension execution pending in L01/P02)

## 1. shaikh_source

"Lu = L − Lp = total unproductive labor." — Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, p. 109. Decomposition on the same page: "Total unproductive labor = nonproduction workers in production sectors + all workers in nonproduction sectors." (The decomposition is informative — Lu has two structural sources — but the operational definition for the time series is the identity Lu = L − Lp.)

## 2. shaikh_appendix_ref

Derived identity from S515 (Lp) and total employment L. The book reports Lu directly in Table 5.7 as the complement of Lp/L; the Appendix E series for Lu is implied by the Appendix E.3 Lp series together with total employment L from NIPA.

## 3. extension_source

DERIVED identity series (NOT a direct fetch). Extension is computed each year as:

    Lu = L_total − S515

where S515 is extended productive employment (see `S515_EPR.md`) and L_total is total nonfarm payroll employment from BLS CES (CES series `CEU0000000001` / `CES0000000001` for total nonfarm, seasonally adjusted, all employees). Cached BLS data: `Inputs/ST2/Inputs/API_Data/BLS/bls_ces_production_workers.csv` (the same BLS pull that supplies S515 also supplies the total-employment denominator; the L_total series may also be sourced from BEA NIPA 6.4D/6.5D full- and part-time employees if a NIPA-consistent total is preferred over the CES total).

## 4. extension_url

- BLS CES total nonfarm employment: https://data.bls.gov/timeseries/CES0000000001
- BLS CES landing page: https://www.bls.gov/ces/
- BLS Public Data API (v2): https://api.bls.gov/publicAPI/v2/timeseries/data/
- (Alternative NIPA-basis total employment: https://apps.bea.gov/iTable/iTable.cfm?reqid=19&step=2 — Tables 6.4D / 6.5D)

For the S515 input, see `S515_EPR.md`.

## 5. conceptual_continuity

Shaikh & Tonak define Lu as the residual of the productive/unproductive partition: unproductive employment is total employment minus productive employment (Ch. 5, p. 109; Table 5.7). Because Lu is a derived identity, the modern construct is conceptually identical to the book construct by construction — there is no separate definition to defend, only the consistency of the two inputs (S515 and L_total). Conceptual continuity of Lu therefore reduces entirely to the conceptual continuity of S515 (Appendix C concordance under NAICS) and the continuity of the total-employment measure (BLS CES total nonfarm, which is a stable BLS headline series). All structural questions about which sectors are "productive" live in S515's documentation, not here.

## 6. vintage_note

Book vintage: SIC-basis BLS employment with Shaikh–Tonak's then-current Appendix C concordance, supplying both Lp and L for the 1948–1961 KB-digitized window. Modern vintage: NAICS-basis BLS CES from 2003 forward; the 2003 SIC→NAICS overhaul affects both L and Lp simultaneously and cancels somewhat in the difference, but does not cancel completely because the partition itself changes. Vintage divergences in Lu are inherited from S515 (Appendix C update for NAICS; BLS CES 2003 overhaul; KB coverage gap 1962–1989). Last cached fetch: see `Inputs/ST2/Inputs/API_Data/BLS/provenance.json`. Splice method is `derive` — the splice is induced by S515 + L_total and there is no independent splice parameter for Lu.
