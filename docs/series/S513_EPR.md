# EPR: S513 — Marxian Profit Rate (r* = S*/(K*+V*), stock form)

**Series**: S513
**Generated**: 2026-05-23T00:00:00Z
**Revised**: 2026-05-24 (v1.2 Iter 3 stock-form primary adoption)
**Status**: book_period_validated (stock-form primary across full 1948-2024 span)

## 1. shaikh_source

"The production of data on the mass of surplus value S* and profit P allows us then to estimate and compare three measures of the rate of profit: the **Marxian general rate of profit r***, defined here as **the ratio of surplus value to total fixed capital K**;16 the average rate of profit r, defined as the ratio of profit-type income net of indirect business taxes (P = P+ − IBT) to K..." — Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, §5.5 p.122.

Footnote 16 (same page): "More properly, one should add the stock of circulating capital (i.e., inventories of raw materials and goods in process, which are the **stock equivalents** of C* and V*, or M and W in the orthodox case) to the stock of fixed capital. But consistent data on the former are not readily available."

See also p. 124: "Because the large rise in the value composition overwhelms the modest one in the rate of surplus value, the adjusted Marxian rate of profit falls by almost a third over this period."

## 2. shaikh_appendix_ref

Table 5.11 (Marxian rate of profit r*, 1948-1989, **stock form** per §5.5 p.122); Figures 5.10, 5.11 (long-run profit rate, decade comparisons); Figures 9.3, 9.4 (cross-period comparisons). Identity defined per §5.5 + Appendix H.1 with K* = fixed-capital stock (operational: BEA Fixed Assets Table 4.1 Line 1) and the footnote-16 ideal denominator adding the stock equivalents of C* and V*.

## 3. extension_source

DERIVED formula series (NOT a direct fetch). Extension is computed each year using the **same stock-form formula as the book period**:

    r* = S505 / (S517 + S504)

where S505 is extended surplus value (BEA NIPA-based), S517 is extended capital stock K* (BEA Fixed Assets Table 4.1 Line 1, Private nonresidential fixed assets, current-cost net stock), and S504 is extended variable capital (BEA NIPA wages + BLS CES production-worker share). The denominator uses the capital STOCK (K* + V*), matching the book canonical §5.5 definition. Cached API inputs feeding the components live under `Inputs/ST2/Inputs/API_Data/BEA/` (Fixed Assets 4.1, NIPA 6.2D compensation, T20100 compensation, 6.4D/6.5D FTE) and `Inputs/ST2/Inputs/API_Data/BLS/bls_ces_production_workers.csv`.

The previously-published flow-form r* = S505/(S502+S504) is retained as a secondary reference variant `S513-FLOW` subseries (marked `_secondary: true` in the registry), provided for continuity with pre-v1.2 headline values. It is not the headline series in v1.2+ because it contradicts the book §5.5 canonical definition.

## 4. extension_url

Component APIs (S513 itself is not fetched; it inherits its URLs from the components):
- BEA NIPA iTable: https://apps.bea.gov/iTable/iTable.cfm?reqid=19&step=2
- BEA Fixed Assets: https://apps.bea.gov/iTable/iTable.cfm?reqid=10&step=1
- BEA KLEMS: https://www.bea.gov/data/special-topics/integrated-industry-level-production-account-klems
- BLS CES (production workers): https://www.bls.gov/ces/

See dependent EPRs: `S505_EPR.md`, `S517_EPR.md`, `S504_EPR.md` (primary stock-form inputs); `S502_EPR.md` (used only for the secondary S513-FLOW variant).

## 5. conceptual_continuity

Shaikh & Tonak define r* in stock form (§5.5 p.122 + footnote 16) and treat it as the central rate-of-return measure of the book (Ch. 5; Table 5.11; Figs. 5.10–5.11). r* is a derived identity, not an observable, so the modern construct is conceptually identical to the book construct by construction: any preserved property of S505, S517, and S504 carries through to r* exactly. The Anu Extension Standard mandates the `derive` splice method for r* — recompute the ratio from independently extended components, never growth-rate-splice the ratio itself. v1.2 Iter 3 additionally enforces **formula uniformity across the splice year**: the same stock-form formula applies to both book period and extension, so the splice is a pure level concatenation (`splice_method: level`) rather than a methodological change. The pre-v1.2 published series mixed book stock-form 1948-1989 with EXT flow-form 1998-2024, producing a spurious +24% secular rise that contradicted the book's documented TRPF decline; v1.2 stock-form primary restores the −59% decline narrative of §5.5 / Ch.9. Classification breaks (SIC→NAICS for V*; the BEA 2013 R&D/IPP capitalization for K*) propagate into r* through the denominator and are documented in the component vintage notes rather than re-litigated here. The 1990-1997 SIC→NAICS bridge gap in S504 propagates to S513-EXT as missing years (not fabricated values), per the anti-fabrication invariant.

## 6. vintage_note

Book vintage: Shaikh & Tonak (1994) used NIPA / Fixed Assets vintages current through 1989 plus pre-NAICS SIC-based BLS data, with the Fixed Assets capital-stock concept matching what is now BEA Fixed Assets Table 4.1 Line 1. Modern vintage (this extension): post-comprehensive-revision BEA NIPA and Fixed Assets (notably the 2013 R&D / IPP capitalization, which raises K* levels), and NAICS-basis BLS CES from 2003 forward. Largest single vintage divergence is the BEA 2013 R&D / IPP capitalization through S517 K*. Last cached fetch of feeding components: see `Inputs/ST2/Inputs/API_Data/BEA/provenance.json` and `Inputs/ST2/Inputs/API_Data/BLS/provenance.json` for timestamps. S513 itself inherits the vintage of whichever component was fetched most recently. Anti-lazy-splice safeguard: the V03 validator rejects any direct level/growth splice of r* and requires formula recomputation per year.

## 7. v1.2 Iter 3 stock-form adoption note

The decision to adopt stock-form as primary across the full 1948-2024 span (replacing the prior book-stock + EXT-flow silent splice) was authorized in v1.2 Iter 1 Track A.1 examination (HIGH confidence) per `docs/variants/VPR_S513_stock_vs_flow_DECISION_BRIEF.md`. Key findings driving the change: (1) book §5.5 p.122 verbatim defines r* in stock form; (2) book-period chopped value 1989=0.3723 is byte-identical to the stock-form computation, proving the book period was always stock-form (only the prior EXT block was flow); (3) the pre-v1.2 splice silently switched denominators at 1989, producing a +24% secular rise that contradicted the book's documented decline; (4) stock-form primary restores the −59.4% endpoint-to-endpoint decline (OLS log-trend −1.66 %/yr) consistent with §5.5 / Ch.9 TRPF narrative; (5) ES1703 (Cronin 2001 NZ c/v, Pearce critique) reinforces methodologically against stock-flow mixing.
