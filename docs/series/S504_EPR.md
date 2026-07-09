# EPR: S504 — Variable Capital (V*)

**Series**: S504
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated

## 1. shaikh_source

> "(wp)j = unit wage of production workers in the jth production sector, j = 1,..., k (from BLS), except services, for which (wp)serv = ecserv; xj ≡ (EC/WS)j = ratio of employee compensation EC to wages and salaries W, in the jth production sector, j = 1,..., k (from NIPA); (ecp)j = (wp)j·(xj) = estimated employee compensation of production workers in the jth production sector; Vj ≡ ecj · (Lp)j ≡ (Wp)j" (S&T 1994, Ch. 5 methodology, V* construction formula)

> "Productive labor is the production labor employed in capitalist production sectors: agriculture, mining, construction, transportation and public utilities, manufacturing, and productive services (defined as all services except business services, legal services, and private households, as in Table E.1)." (S&T 1994, Ch. 5, definition of productive labor)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. Chapter 5, Appendix H.1 (column V_star, productive variable capital, 1948–1989); Chapter 5 pp. 161–180 (decomposition of V into productive and unproductive wages).

## 2. shaikh_appendix_ref

Primary: **Appendix H.1**, column V_star (annual, 1948–1989).
Supplementary: **Table 5.7** (productive labor and wage shares); **Figure 5.6** (aggregate measures).
Source recipe: `V* = Σ_j (wp)_j × x_j × (Lp)_j` summed over productive sectors, with wage/employment inputs from BLS and the EC/WS ratio from NIPA.

## 3. extension_source

**BEA NIPA + BLS CES composite**, filtered through the productive/unproductive partition (V* is a partitioned subaggregate of total compensation, not a directly published series):
- **BEA NIPA Table 6.2D** — Compensation of Employees by Industry (cached `nipa_6_2D_compensation_by_industry.csv`, 2,673 rows; provenance file lists `purpose: "V* = variable capital (productive worker compensation)"`).
- **BEA NIPA Table T20100** — Aggregate compensation 1929–2025 (`nipa_T20100_compensation_1929_2025.csv`) for the total wage bill W.
- **BLS CES production-worker series** — `bls_ces_production_workers.csv`, 10 industry series (CES0500000006, CES0600000006, CES1000000006, CES2000000006, CES3000000006 and their all-employee counterparts) for the production-worker share.

Cached at `data/raw/Inputs/API_Data/BEA/` and `data/raw/Inputs/API_Data/BLS/`, pulled 2026-02-24. Construction is a derive operation that depends on S512 (productive wage share V*/W).

## 4. extension_url

BEA NIPA Table 6.2D (API): `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=NIPA&TableName=T60200D&Frequency=A&Year=ALL&ResultFormat=JSON`
BEA NIPA Table 2.1.0.0 web view: `https://apps.bea.gov/iTable/iTable.cfm?reqid=19&step=2`
BLS CES API (per series): `https://api.bls.gov/publicAPI/v2/timeseries/data/CES3000000006` (manufacturing production workers; analogous endpoints for the other 9 series).
BLS CES web home: `https://www.bls.gov/ces/`

## 5. conceptual_continuity

Variable Capital V* is the wages paid to productive workers — production-worker compensation in productive (capitalist-production-sector) industries. It is not a directly published series in any modern statistical account; it is a partitioned subaggregate constructed by applying the Marxian productive/unproductive partition (book Appendix C concordance) to industry-level BEA compensation and BLS CES production-worker shares. The modern extension recomputes V* in the same way the book does: production-worker compensation share per industry (BLS CES wp/x ratios) × total industry compensation (BEA NIPA 6.2D) → summed over productive industries. Per the Anu Extension Standard, V* is therefore extended by `derive` (not by lazy growth-rate splice on V* itself), and the derive operation leans on S512 (productive wage share V*/W) being extended first. Conceptual continuity is preserved subject to a faithful update of Appendix C to NAICS.

## 6. vintage_note

Book V* (1948–1989) uses pre-NAICS SIC industry classifications and BLS CES production-worker data as it existed by 1993; the book's Appendix C concordance is SIC-based. Modern BEA NIPA compensation has undergone comprehensive revisions (1999, 2003, 2009, 2013, 2018) that alter compensation levels; BLS CES underwent the 2003 establishment-survey overhaul (NAICS reclassification, reweighted sample). Treatment of stock-based and deferred compensation differs across vintages. Appendix C must be rewritten over NAICS industries (with new categories like information services and professional/business services) — the partition cannot be mechanically ported. Modern data pulled 2026-02-24 (BEA / BLS provenance files); BEA NIPA at September 2025 vintage; BLS CES at the standard monthly-revision vintage current as of the pull date.

## 7. methodology — 1990-1997 SIC↔NAICS bridge

**Bridge**: log-linear interpolation between book 1989 endpoint
(S504-A[1989] = 1206.40 $B) and BEA-derived first-EXT value
(S504-EXT[1998] = 1620.23 $B), populating S504-COMBINED for years 1990-1997
via a dedicated S504-INTERP subseries. Consistent with the S501–S503 bridge
per `internal-build/BUILD_NARRATIVE.md` Stage 5 cohort 3.

**Formula**: `v(t) = exp( ln(v0) + (t - 1989)/(1998 - 1989) · (ln(v1) - ln(v0)) )`

**Rationale**: BEA NIPA Table 6.2D (Compensation of Employees by Industry,
NAICS) begins 1998; V* (productive variable capital) cannot be reconstructed
for 1990-1997 without a bespoke SIC/NAICS reconciliation. Log-linear
(not linear) is preferred for a positive nominal $B series because the
underlying aggregate grows multiplicatively.

**Honesty**: these 8 values are **INTERPOLATED** — model-implied estimates
under a smooth-growth assumption, NOT BEA-published data. They carry
`stage="extension_bridge"` and live in a separately-named `S504-INTERP`
subseries (the chopped CSV exposes them as a distinct column). Sample
values: 1991 = 1288.12 $B, 1995 = 1468.52 $B.

**Documentation script**: `code/M04_manual/M04_S504_1990_1997_bridge.py`
(also acts as a verifier).

---

## workpackage A SUPERSESSION NOTICE (2026-07-01)

The extension methodology described above was revised by the workpackage A comprehensive-review rebuild
(headline ROE remediation). Level-splices and log-linear 1990-97 bridges described in this EPR
are RETIRED; see the workpackage A REBUILD ADDENDUM in `S504_DPR.md`, the as-built provenance strings
in `data/final/S504.csv`, and DIV-A10..A16 in `internal-review-notes_2026-07/WP-A_DIV_PATCHES.json`.
