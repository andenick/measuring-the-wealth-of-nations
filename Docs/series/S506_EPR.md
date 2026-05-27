# EPR: S506 — Rate of Exploitation (e = S*/V*)

**Series**: S506
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated

## 1. shaikh_source

> "The rate of exploitation is the ratio of surplus labor time to necessary labor time. This can be calculated for any capitalistically employed wage labor, be it productive or unproductive. Necessary labor time is simply the value of the labor power involved, that is, the labor value of the average annual consumption per worker in the activities in question. Surplus labor time is excess of working time over necessary labor time." (S&T 1994, Ch. 5, definition of the rate of exploitation)

> "Because the rate of exploitation of productive workers is simply the rate of surplus value, we can directly estimate the rate of exploitation of unproductive workers. We use the money rate of surplus value S*/V* since we already know that it is quite close to the value rate, as shown in Section 4.2." (S&T 1994, Ch. 5, on the empirical identification of e with S*/V*)

> "Figure 5.13 is the pièce de résistance. It compares the rate of surplus value S*/V* (which is the rate of exploitation of productive workers) with its 'naive' equivalent (P+)/EC. At midperiod, the former is almost four times as large as the latter. It also rises by over 40% during the postwar period, whereas the latter actually falls by almost 30%." (S&T 1994, Ch. 5, on the empirical trajectory of e)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. Chapter 5, Table 5.7 (rate of surplus value e = S*/V*); identity from Appendix H.1 series.

## 2. shaikh_appendix_ref

Primary: **Table 5.7** (rate of surplus value column, annual benchmarks 1948–1989, p. 121).
Supplementary: **Appendix H.1** (S_star and V_star columns supplying numerator and denominator); **Figure 5.6** (S*/V* plotted as time series); **Figure 5.13** (S*/V* vs naive P+/EC comparison).
Identity: e = S* / V* = S505 / S504 in this project's series IDs.

## 3. extension_source

**Derived ratio**: S506-EXT = S505-COMBINED / S504-COMBINED. S506 has no standalone API pull; it inherits its source matrix from its components:
- **S505** (Surplus Value) — itself derived from S503 − S504.
- **S504** (Variable Capital) — BEA NIPA Table 6.2D + BLS CES production-worker shares, partitioned by the productive/unproductive concordance.

Underlying upstream caches: `Inputs/ST2/Inputs/API_Data/BEA/` (NIPA 6.2D, NIPA 1.7.5, GDP-by-Industry) and `Inputs/ST2/Inputs/API_Data/BLS/` (CES production-worker series), pulled 2026-02-24.

## 4. extension_url

n/a — S506 is a derived ratio. Upstream API endpoints (inherited):
- BEA NIPA 6.2D: `https://apps.bea.gov/api/data?...&datasetname=NIPA&TableName=T60200D&...` (via S504)
- BLS CES: `https://api.bls.gov/publicAPI/v2/timeseries/data/<series_id>` (via S504)
- BEA GDP-by-Industry: `https://apps.bea.gov/api/data?...&datasetname=GDPbyIndustry&...` (via S503 → S501)

## 5. conceptual_continuity

Rate of exploitation e = S*/V* is the central Marxian ratio of surplus value to variable capital — the rate at which capital extracts surplus from productive labor. It is a pure ratio of two aggregate series, both of which are themselves partitioned/derived subaggregates rather than directly published time series. Per the Anu Extension Standard prohibition on lazy splices on derived quantities (rule: "If the original computed a formula (ratio = X/Y), the extension must compute the same formula with extended component data"), S506 must be extended by `derive` — recomputed at each year from independently extended S505 and S504. A direct growth-rate splice on e would silently sever its structural interpretation. Conceptual continuity holds whenever the numerator and denominator carry their Marxian definitions intact; the book's Appendix C productive/unproductive partition (updated to NAICS) is the key methodological hinge.

## 6. vintage_note

As a dimensionless ratio, S506 inherits all vintage divergences from S505 and S504 but introduces none of its own. Unit-vintage issues cancel by construction. The Appendix-C-to-NAICS concordance update is the dominant source of cross-vintage drift: any inconsistency between the book-period SIC partition and the modern NAICS partition will move the level of e at the 1989 splice point. Book values 1948–1989 frozen at the book's vintage (Table 5.7 endpoints: 1948 e=1.70, 1989 e=2.44); modern data pulled 2026-02-24 (BEA / BLS provenance).
