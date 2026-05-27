# EPR: S703 — Value-Price Deviations (real, consistent-procedure regression)

**Series**: S703
**Generated**: 2026-05-24T06:00:00Z (v1.1 Phase 4 iteration 5 Ch7 real-fix)
**Status**: validated_book_and_extension
**Supersedes**: prior `EXTENSION NOT APPLICABLE` stub (v1.0 iteration 9), authored when S703 was a `(S702 - S701)/S701 * 100` scalar (algebraically identical to S513 * 100) with `extension: null`. v1.1 Phase 4 retires the proxy and populates a real extension arm running the book's consistent-procedure regression.

## 1. shaikh_source

> "All these mappings were constructed on the assumption that purchasers' prices were proportional to labor values. This allowed us to check that the various elements add up to the correct totals, no matter how complicated the transfers of value involved. It also ensured that any discrepancies that arose between individual Marxian categories and their orthodox counterparts were due solely to conceptual differences, not to any price-value deviations that might exist." (Shaikh & Tonak 1994, Ch. 7 §7.3, p. 223)

> "In Chapter 4 we extend the analysis to the calculation of actual labor value magnitudes. We show that the correct procedure is consistent, in the sense that it gives the same ratios in value terms and in price terms when unit purchaser prices are equal to unit values (Tables 4.1 and 4.2). This means that in actual input-output tables, where purchasers' prices generally do differ from values, we can then interpret the deviations between value and money ratios as a measure of the aggregate effects of price-value deviations, if the procedure used is consistent in the sense just described." (S&T 1994, Ch. 7 §7.3, p. 223)

> "Using the consistent procedure, Khanjian (1989) shows that value and price rates of surplus value differ by only small amounts (6%-9%), which indicates that the effects of price-value deviations on aggregate measures are quite minor (Section 5.10, Table 5.12, and Figure 5.25)." (S&T 1994, Ch. 7 §7.3, p. 223)

Source: Shaikh & Tonak (1994), *Measuring the Wealth of Nations*. Cambridge University Press. The empirical claim S703 is meant to test — Khanjian's 6–9% S*/V* deviation envelope — is measurable for the first time in v1.1 Phase 4, because both S701 (real lambda*_j) and S702 (real pp*_j) are now sector-disaggregated under the consistent procedure.

## 2. shaikh_appendix_ref

Primary methodology: **Chapter 4 §4.1**, pp. 78–88 (consistent-procedure Tables 4.1, 4.2; inconsistent symmetric-treatment diagnosis Table 4.3 pp. 85–86).
Empirical anchor: **Chapter 7 §7.3** (p. 223 Khanjian 6–9% S*/V* benchmark) and **§7.4** (Wolff 4–8% bias from symmetric treatment, cumulative 12–15% upper envelope).
Khanjian source (cited in book): **§5.10 Table 5.12, Figure 5.25** of ST 1994 (S*/V* value vs price comparison).
Registry `book_table='7.3'` is a project-internal label — the book has no literal Table 7.3.
Note on R² > 0.95 claim: prior research files attributed an R² > 0.95 anchor to Ch7; direct re-read finds no such literal claim. The load-bearing book number is Khanjian's 6–9% S*/V* deviation, not 95% R².

## 3. extension_source

**Two real upstream series (no new data fetches required for S703 itself)**:

1. **Real S701 lambda*_j vector** — sector-disaggregated labor values in hr/$, output of `Technical/code/P02_processors/P02_S701_labor_values.py` (v1.1 rewrite).

2. **Real S702 pp*_j vector** — sector-disaggregated prices of production in labor-value units, output of `Technical/code/P02_processors/P02_S702_prices_of_production.py` (v1.1 rewrite).

Optional cross-reference: **Khanjian (1989)** — the book's empirical comparator series for the 6–9% S*/V* envelope. Not refetched in v1.1; the published Khanjian numbers serve as V03_S703 PASS/FAIL anchor.

Construction (per `Technical/code/P02_processors/P02_S703_value_price_deviations.py` v1.1 rewrite): per benchmark year, run OLS regression `log(lambda*_j) ~ a + b * log(pp*_j)` across the 8 ST productive sectors; report R² and slope; also compute aggregate S*/V* deviation per Khanjian procedure (price-form vs value-form rate of surplus value) and report deviation magnitude in percent.

## 4. extension_url

No new external endpoint — S703 is a pure regression on upstream real S701 + S702 outputs.

Book-period verification anchor: Khanjian (1989) "The Empirical Evidence Relating to the Existence of Prices of Production: A Critique of Wolff," *Review of Radical Political Economics* — full text via JSTOR / publisher archive (no API; PDF retrieval if needed).

Extension-period: same regression run on extension years where both real S701 and real S702 produce sector vectors (1997+ NAICS benchmark years per upstream EPRs).

## 5. conceptual_continuity

S703 is a regression on sector vectors, not a directly-observed time series, so the only meaningful "extension" is to run the same regression in additional (extension-period) benchmark years where sector data is available. The methodology — cross-sectional OLS of log labor values against log prices of production across productive sectors, per benchmark year — is identical book ↔ extension. The SIC → NAICS junction is handled implicitly: book years use SIC sectors (8 ST productive sectors); extension years use the NAICS-mapped productive industries per the upstream S701/S702 EPR concordance. Aggregate S*/V* deviation magnitude is comparable across SIC and NAICS years to within the precision of the productive-classification mapping. Methodological consistency book ↔ extension: identical (same regression specification, same Khanjian envelope as PASS/FAIL anchor).

## 6. vintage_note

S703 inherits the vintage profile of upstream S701 and S702 (see those EPRs §6). Book years use book-vintage BEA SIC IO + BLS CES; extension years use BEA NAICS pulled 2026-02-24 and BLS CES pulled 2026-05-24. BLS CES 2003 overhaul (DIV-010) and SIC-NAICS coarse concordance (DIV-008 reference) propagate from upstream. Six benchmark years is a small cross-section even in book period; regression R² should be interpreted with that small-n caveat documented in the V03 output. The Khanjian 6–9% S*/V* envelope is the load-bearing PASS/FAIL anchor; R² is a secondary diagnostic.
