# EPR: S501 — Total Product (TP*)

**Series**: S501
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated

## 1. shaikh_source

> "Total value TV*: Sum of gross outputs of production and total trade sectors." (Shaikh & Tonak 1994, Ch. 5, Appendix H notation)

> "For all of these reasons, one cannot simply use NIPA data to fill in observations between IO benchmark years. Instead, we use NIPA data directly for components such as GVAp or CON (containing the latest available revisions) and indirectly to interpolate between benchmark estimates of other components such as M'p or RYcon." (S&T 1994, Ch. 5, methodology discussion accompanying Appendix H.1 construction)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. Chapter 5 (The Marxian Categories: Empirical Estimates), Appendix H.1, pp. 324–327, with revenue-side cross-check in Appendix E.2 (p. 310, 1948–1961 subset).

## 2. shaikh_appendix_ref

Primary: **Appendix H.1**, column TP_star (annual values, 1948–1989, p. 324–327).
Cross-check: **Appendix E.2**, column TP_star (1948–1961 subset, p. 310, duplicate-source validation).
Figures: 5.4, 5.6, 9.1, 9.2 (TP* plotted as Marxian total product aggregate).

## 3. extension_source

**BEA GDP-by-Industry Accounts** — value-added series for the productive-sector NAICS industries (S501-EXT subseries; productive/unproductive concordance documented in `Technical/docs/methodology/productive_classification_NAICS.md`). The pull caches the BEA Industry value-added components (`gdp_by_industry_value_added.csv`, `gdp_by_industry_va_components.csv`, `gdp_by_industry_gross_output.csv`) and NIPA Gross Output by Industry Table 1.7.5 (`nipa_1_7_5_gross_output_by_industry.csv`) at `Inputs/ST2/Inputs/API_Data/BEA/`, pulled 2026-02-24 by `pull_bea_nipa_ch05.py`.

## 4. extension_url

Web interface: https://www.bea.gov/data/gdp/gdp-industry
API endpoint (constructed): `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=GDPbyIndustry&TableID=15&Industry=ALL&Year=ALL&Frequency=A&ResultFormat=JSON`
Companion NIPA Gross-Output endpoint: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=NIPA&TableName=T10705&Frequency=A&Year=ALL&ResultFormat=JSON`

## 5. conceptual_continuity

Total Product TP* is the Marxian measure of total value produced in the productive economy — the gross output (or, equivalently, M'_p + GFP) of agriculture, mining, construction, transportation and public utilities, manufacturing, and productive services. The book computes it from BEA NIPA + Input-Output tables under the SIC industrial classification through 1989. The modern BEA GDP-by-Industry account directly observes gross output and value added at the industry level under NAICS from 1997 forward; once the Appendix-C productive/unproductive partition is rewritten over NAICS industries, the modern series measures the same construct (gross value generated in productive industries). TP* is a directly-observed aggregate (not a derived ratio), so a growth-rate splice at the SIC↔NAICS junction is admissible under the Anu Extension Standard. The only methodological adjustment is the SIC↔NAICS productive-industry concordance.

## 6. vintage_note

Book values 1948–1989 are frozen at the book's vintage: SIC-based BEA NIPA + IO tables as published by 1993. Modern extension uses BEA GDP-by-Industry NAICS data from 1997 forward, pulled 2026-02-24 (provenance file `Inputs/ST2/Inputs/API_Data/BEA/provenance.json`), representing approximately the September 2025 NIPA vintage. The 1990–1996 gap is bridged log-linearly between the 1989 book endpoint and the 1997 BEA NAICS endpoint, documented as methodological adjustment M04_S501 in `DIVERGENCE_REGISTER.json`. BEA comprehensive revisions (1999, 2003, 2009, 2013, 2018) alter post-1997 values relative to the book; pre-1997 book values remain frozen.
