> **D4 REBUILD (2026-07-02) — SUPERSEDES the text below (pending D5 doc-regen).**
> This series has been rebuilt from Mohun's ACTUAL published estimates: Mohun's unproductive burden ratio Lu/Lp from his published shares: 1964=0.724, 2003=0.961, 2010=0.905; ST/Mohun comparison predecessor-build 1964=0.809 (+11.7%, DIV-058).
> Units are now a **share/ratio over 1964-2010** (benchmark anchors, table/text-grade), NOT
> thousands of FTE over 1948-1989. The old 1948-1989 thousands series was a mislabeled
> predecessor-build decomposition (DIV-050/051) and is retained as a variant arm (chopped/_variants_predecessor-build/).
> Attribution: **Mohun (2014), RRPE 46(3):355-379**, DOI 10.1177/0486613413506080.
> Source: `data/source/external_studies/mohun_2013_published_shares.csv`. See D4 report.

# XS1504 — Unproductive Burden Ratio Lu/Lp (Mohun 2013)

**Status**: book_period_validated
---

## Methodology

XS1504 implements the classic "unproductive burden" ratio Lu/Lp defined in Mohun (2013), "Unproductive Labor in the U.S. Economy 1964-2010" (RRPE 46(3)). The data source is Mohun's published full-time-equivalent (FTE) employment dataset, loaded via loader L15 from `Inputs/ExternalSources/Mohun/` and processed by P20. The construction divides total unproductive FTE employment (XS1503, which contains Mohun's working-class unproductive Lu_wc plus supervisory Lu_sup) by Mohun's productive FTE employment series Lp, yielding a dimensionless ratio. Conceptually the ratio answers: for each productive worker, how many unproductive workers must be supported out of surplus value? The series covers 1964-2010 (the full Mohun panel), and rises consistently as unproductive employment grows from roughly 42% to 49% of total. The 1948-1989 book-period validation window shows a range of 0.76-0.92, all within the registry's expected_range [0.5, 3.0] and within share-series tolerance for cross-checking against Mohun's published Table 1. The transformation is a single algebraic division with no splice, no proxy, and no extension; both numerator and denominator come from the same FTE accounting universe (Mohun's adaptation of BLS Current Employment Statistics combined with BEA National Income & Product Accounts), so dimensional consistency is automatic and no scale correction is applied. The series carries a documented analytical caveat (registered in `known_issues`): Mohun's own Section 6 finding is that the rising Lu/Lp ratio is largely uninformative as a burden measure once decomposed by class — working-class unproductive labor absorbed a flat 12.8% of value-added throughout 1964-2010, while only the supervisory subcomponent drives rising surplus absorption. V20 therefore validates the level and trend of XS1504 but flags that interpretation requires reading alongside XS1501-XS1503 and the class decomposition presented in the Mohun (2013) DPR for the parent study.
