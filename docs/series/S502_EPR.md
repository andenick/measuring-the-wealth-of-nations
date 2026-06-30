# EPR: S502 — Constant Capital (C*_m = M'_p, materials-only identity)

**Series**: S502
**Generated**: 2026-05-23T00:00:00Z (Stage 5 cohort 3, replaces orphan NOT_APPLICABLE stub from iteration 9)
**Status**: validated_book_and_extension

## 1. shaikh_source

> "M'_p represents the value of intermediate non-labor inputs (raw and auxiliary materials, energy, and intermediate goods and services) consumed in production by the productive sector, as distinguished from D_p which represents the consumption of fixed capital." (Shaikh & Tonak 1994, Ch. 5, materials-only identity per p. 95)

> "For all of these reasons, one cannot simply use NIPA data to fill in observations between IO benchmark years. Instead, we use NIPA data directly for components such as GVAp or CON (containing the latest available revisions) and indirectly to interpolate between benchmark estimates of other components such as M'p or RYcon." (S&T 1994, Ch. 5, methodology discussion accompanying Appendix H.1 construction)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. Chapter 5 (The Marxian Categories: Empirical Estimates), Appendix H.1, pp. 324–327.

## 2. shaikh_appendix_ref

Primary: **Appendix H.1**, column `Mp` (annual values, 1948–1989, pp. 324–327).
Methodological discussion in Ch. 5 main text (M'_p construction via the IO/NIPA integration described in Appendix H, including the use of input-output benchmark interpolation between benchmark years).
Figures: 5.4, 5.6, 9.1, 9.2 (M'_p plotted as a component of the Marxian total-product decomposition).

## 3. extension_source

**BEA GDP-by-Industry Accounts** — Intermediate Inputs (II) for the productive-sector NAICS industries (S502-EXT subseries). II is computed via the BEA-published identity II = Gross Output − Value Added at the industry level (productive/unproductive concordance documented in `Technical/docs/methodology/productive_classification_NAICS.md`, same partition as S501/S503). The pull caches the BEA Industry value-added components (`gdp_by_industry_value_added.csv`, `gdp_by_industry_gross_output.csv`) at `data/raw/bea/`, pulled 2026-02-24 by `pull_bea_nipa_ch05.py` and mirrored at `Technical/data/raw/bea/`.

## 4. extension_url

Web interface: https://www.bea.gov/data/gdp/gdp-industry
API endpoints used (constructed):
- VA: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=GDPbyIndustry&TableID=1&Industry=ALL&Year=ALL&Frequency=A&ResultFormat=JSON`
- GO: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=GDPbyIndustry&TableID=15&Industry=ALL&Year=ALL&Frequency=A&ResultFormat=JSON`

## 5. conceptual_continuity

C*_m / M'_p is the Marxian measure of the materials-only flow of productive constant capital: the value of intermediate non-labor produced inputs (raw materials, energy, intermediate goods and services) absorbed in production by the productive sector. It is conceptually distinct from D_p (depreciation of fixed capital), which the book handles via a separate series and which corresponds to S517 / fixed-asset consumption in the modern accounts.

In the modern BEA GDP-by-Industry framework, the directly published industry-level identity is:

    Gross Output (GO) = Value Added (VA) + Intermediate Inputs (II)

so II = GO − VA is the modern accounting equivalent of M'_p when summed across productive industries. The productive partition uses the same 8 top-level NAICS aggregates as S501 (Appendix C concordance): 11, 21, 22, 23, 31G, 42, 44RT, 48TW. All eight are TOP-LEVEL aggregates in the BEA cache — summing them does not double-count with sub-industry codes (which appear separately in the same CSV).

Growth-rate splice at 1997 is admissible under the Anu Extension Standard because II is a directly-observed flow (not a derived ratio): the EXT series enters at its observed 1997 BEA level, the book series stays at its observed 1948–1989 levels, and the 1990–1996 gap is bridged log-linearly. The only methodological adjustment is the SIC↔NAICS productive-industry concordance.

## 6. vintage_note

Book values 1948–1989 are frozen at the book's vintage: SIC-based BEA NIPA + IO tables as published by 1993. The modern extension uses BEA GDP-by-Industry NAICS data from 1997 forward, pulled 2026-02-24 (provenance `data/raw/bea/provenance.json`), approximately the September 2025 NIPA vintage.

The 1990–1996 gap is bridged log-linearly between the 1989 book endpoint (M'_p = 3278.25) and the 1997 BEA endpoint (II_productive = 3945.10), documented as methodological adjustment **M04_S502** in `DIVERGENCE_REGISTER.json`. The BEA endpoint exceeds the book endpoint by ~20%, consistent with normal nominal trend growth over 8 years (~2.3%/yr compound) plus modest comprehensive-revision level effects. BEA comprehensive revisions (1999, 2003, 2009, 2013, 2018) alter post-1997 values relative to the book; pre-1997 book values remain frozen.

A future variant (VPR_S502_alt_extension) could explore a level-rescale splice that re-anchors BEA(1997) onto a forward projection of the book series, but this would distort the post-1997 BEA growth profile and is therefore not the default per the Anu Extension Standard's preference for growth-rate splicing when both eras observe directly comparable flows.
