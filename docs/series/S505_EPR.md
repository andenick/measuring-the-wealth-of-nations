# EPR: S505 — Surplus Value (S* = VA* − V*)

**Series**: S505
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated

## 1. shaikh_source

> "The estimates of variable capital in the previous section allow us to calculate surplus value and surplus product. By definition, S* = VA* − V* = surplus value (in money form); S*/V* = rate of surplus value; NP* = the necessary product (consumption of productive workers) = V*; SP* = FP* − NP* = surplus product." (S&T 1994, Ch. 5, definition of surplus value)

> "For U.S. data, the orthodox measure VA = P + EC remains within 10% of the Marxian measure VA* = V* + S*, so the difference between P/EC and S*/V* is largely due to the fact that V* = Wp << EC." (S&T 1994, Ch. 5, on the Marxian vs orthodox value-added measures)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. Chapter 5, Appendix H.1 column S_star (surplus value, 1948–1989). Identity: S* = VA* − V*, with VA* ≈ GFP (where indirect taxes on production are netted).

## 2. shaikh_appendix_ref

Primary: **Appendix H.1**, column S_star (annual, 1948–1989).
Supplementary: **Table 5.7** (rate of surplus value S*/V*); **Figures 5.4, 5.6** (Marxian aggregate measures, plotted alongside V* and TP*).
Identity: S* = GFP − V* = S503 − S504 in this project's series IDs.

## 3. extension_source

**Derived series**: S505-EXT = S503-COMBINED − S504-COMBINED (Gross Final Product minus Variable Capital). S505 itself has no standalone modern data pull — it inherits its source matrix from its inputs:
- **S503** (Gross Final Product, GFP) — derived from S501 (TP*) and S502 (C*_m), both ultimately from BEA NIPA + GDP-by-Industry (`data/raw/Inputs/API_Data/BEA/` cache).
- **S504** (Variable Capital, V*) — BEA NIPA Table 6.2D compensation + BLS CES production-worker shares.

No new API pull is performed for S505; the extension is fully derived from S503 and S504 via the identity.

## 4. extension_url

n/a — S505 is derived from S503 and S504. The upstream API endpoints are inherited from those EPRs:
- BEA NIPA: `https://apps.bea.gov/api/data?...&datasetname=NIPA&TableName=T10705&...` (via S501/S502/S503)
- BEA NIPA Table 6.2D: `https://apps.bea.gov/api/data?...&datasetname=NIPA&TableName=T60200D&...` (via S504)
- BLS CES: `https://api.bls.gov/publicAPI/v2/timeseries/data/<series_id>` (via S504)

## 5. conceptual_continuity

Surplus Value S* is the residual of productive value added (GFP, or VA* under the strict Marxian definition) over variable capital — the Marxian surplus appropriated by capital from productive workers. It is a derived identity, not a directly observed series. The book itself constructs S* by computing GFP and V* separately and subtracting (Appendix H.1 derivation), then publishes the resulting series. The modern extension does exactly the same: S* = GFP_t − V*_t with both inputs independently extended via their own EPRs. Per the Anu Extension Standard prohibition on "lazy splices on derived quantities," S505 is extended by `derive` (computing the identity at each year), never by direct growth-rate splice on S* itself. Conceptual continuity is mechanical: S505 is faithful to the book's construction so long as S503 and S504 are.

## 6. vintage_note

S505 inherits all vintage divergences from its inputs:
- S503 vintage issues (via S501: SIC↔NAICS reclassification; BEA NIPA comprehensive revisions 1999/2003/2009/2013/2018; 1990–1996 log-linear bridge M04_S501).
- S504 vintage issues (BLS CES 2003 NAICS overhaul; BEA NIPA compensation revisions; Appendix C concordance update for NAICS; stock-based and deferred compensation treatment differences).
No additional vintage divergence is introduced by the S* = GFP − V* identity. Book values 1948–1989 are frozen at the book's vintage; modern values are functions of the BEA / BLS pulls dated 2026-02-24.
