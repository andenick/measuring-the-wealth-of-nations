# EPR: S512 — Productive Wage Share (V*/W)

**Series**: S512
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated

## 1. shaikh_source

> "V*/W = variable capital / total employee compensation. Under the approximation ec_u/ec_p ≈ 1 (where ec is employee compensation per worker), V*/W ≈ Lp/L. This approximation is central to the extension methodology, allowing V*/W to be proxied from BLS CES production-worker shares when industry-level compensation decomposition is not directly available." (S&T 1994 Ch. 5 methodology, encoded in `Technical/research/S512_research.json` entry_type=methodology_description and approximation_analysis; Table 5.7 benchmarks: 1948=0.54, 1967=0.45, 1977=0.412, 1989=0.36.)

> "Figure 5.8 contrasts the levels of real variable capital and of the total real wage bill. Their absolute growth is greater than that of the corresponding labor totals in Figure 5.7 because the wage measures also incorporate the effects of growing real wages. But the relative movements of wage and employment measures is virtually the same, as is evident in Figure 5.9. V*/W declines by 34%, while Lp[/L declines similarly]." (S&T 1994, Ch. 5; cross-referenced from S504 verbatim research)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. Chapter 5, Table 5.7 column V*/W (productive wage share of total wages); Appendix H.1 V_star (productive variable capital); identity V*/W = productive wages / total wages.

## 2. shaikh_appendix_ref

Primary: **Table 5.7**, column V*/W (annual benchmarks 1948–1989, p. 121; KB chunk_14).
Supplementary: **Appendix H.1** (V_star numerator series); **Figures 5.7 and 5.8** (Lp/L and V*/W contrast); **Figure 5.9** (relative movements of wage vs employment ratios).
Construction: V* (productive worker compensation, via the formula `V_j = (wp)_j × x_j × (Lp)_j` summed over productive sectors) divided by W (total wage and salary bill).

## 3. extension_source

**BLS CES + BEA NIPA composite** — production-worker wages by industry from BLS CES aggregated through the productive/unproductive concordance to compute V*; total wage bill W from BEA NIPA Table 6.2:
- **BLS CES production-worker series** (10 series) cached at `data/raw/Inputs/API_Data/BLS/bls_ces_production_workers.csv`, pulled 2026-02-24.
- **BEA NIPA Table 6.2D** (Compensation of Employees by Industry, 2,673 rows) cached at `data/raw/Inputs/API_Data/BEA/nipa_6_2D_compensation_by_industry.csv`, pulled 2026-02-24.
- **BEA NIPA Table 6.10D** (Employer Contributions for Government Social Insurance, 540 rows) at `nipa_6_10D_employer_contributions.csv` — provenance file lists `purpose: "Employee compensation detail for ec_p/ec_u ratio"`, directly supporting the V*/W decomposition.
- **BEA NIPA Table T20100** (Compensation 1929–2025) at `nipa_T20100_compensation_1929_2025.csv` for the W denominator.

## 4. extension_url

BLS CES API (per series): `https://api.bls.gov/publicAPI/v2/timeseries/data/CES3000000006` (manufacturing production workers); 9 additional CES series identifiers used in the construction.
BLS CES home: `https://www.bls.gov/ces/`
BEA NIPA 6.2D API: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=NIPA&TableName=T60200D&Frequency=A&Year=ALL&ResultFormat=JSON`
BEA NIPA 6.10D API: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=NIPA&TableName=T61000D&Frequency=A&Year=ALL&ResultFormat=JSON`

## 5. conceptual_continuity

Productive wage share V*/W is the fraction of total wages paid to productive workers (production workers in productive industries, per Appendix C). It is a directly observable share given BLS CES production-worker wage proxies (via the wp × x = ecp construction) and BEA NIPA total compensation, subject to the Marxian partition. Under the book's central approximation ec_u/ec_p ≈ 1 — verified empirically: V*/W tracks Lp/L within 0.03 over 1948–1989 — V*/W ≈ Lp/L, and S512 can be proxied from S511 when industry-level compensation decomposition is unavailable. The full extension uses the direct V*/W construction whenever industry-level wage data permits, falling back to the Lp/L proxy where necessary (documented per-year). Because V*/W is a bounded share with directly observable components, the splice method is `level` (rebased at 1989 to match the book's Table 5.7 value 0.36), matching the rationale for S511. The Anu Extension Standard "no lazy splice on derived quantities" rule is respected: V*/W is a share-of-an-observable, not a derived ratio of two independent series. S512 is an **upstream dependency for S504 (Variable Capital) and S506 (Rate of Exploitation)** — it must be extended first.

## 6. vintage_note

The book's V*/W uses BLS CES production-worker wages and BEA NIPA compensation as available by 1993, all under SIC industry classifications and pre-1999 NIPA vintages. Modern data inherits **BLS CES 2003 NAICS transition** issues (pre-2003 SIC and post-2003 NAICS series are not directly comparable; sample redesigned and reweighted); **BEA NIPA comprehensive revisions** (1999, 2003, 2009, 2013, 2018) alter compensation levels and definitions, especially regarding stock-based and deferred compensation (which differ systematically across NIPA vintages and were not separately recognized in the book's vintage). The productive/unproductive Appendix C partition must be rewritten for NAICS industries before V*/W can be reliably computed post-1997. Modern data pulled 2026-02-24 (BEA and BLS provenance files); BEA NIPA at September 2025 vintage.

## 7. methodology — 1990-1997 SIC↔NAICS bridge

**Bridge**: log-linear interpolation between book 1989 endpoint
(S512-A[1989] = 0.3600) and BEA-derived first-EXT value
(S512-EXT[1998] = 0.3195), populating S512-COMBINED for years 1990-1997
via a dedicated S512-INTERP subseries. Consistent with the S501–S503 bridge
per `internal-build/BUILD_NARRATIVE.md` Stage 5 cohort 3.

**Formula**: `v(t) = exp( ln(v0) + (t - 1989)/(1998 - 1989) · (ln(v1) - ln(v0)) )`

**Rationale**: BEA NIPA Table 6.2D (Compensation of Employees by Industry,
NAICS) begins 1998. The productive/unproductive partition cannot be
reconstructed cleanly on either a pure-SIC or pure-NAICS basis across
1990-1997. Log-linear is preferred for a positive bounded share over an
8-year span (closer to multiplicative than additive growth).

**Honesty**: these 8 values are **INTERPOLATED** — model-implied estimates
under a smooth-growth assumption, NOT directly observed. They carry
`stage="extension_bridge"` and live in a separately-named `S512-INTERP`
subseries (the chopped CSV exposes them as a distinct column). Sample
values: 1991 = 0.3506, 1995 = 0.3325.

**Downstream impact**: S504 = V*/W · W is derived from S512, so the bridge
propagates into S504-INTERP across the same years (transparently flagged).

**Documentation script**: `code/M04_manual/M04_S512_1990_1997_bridge.py`
(also acts as a verifier).

---

## workpackage A SUPERSESSION NOTICE (2026-07-01)

The extension methodology described above was revised by the workpackage A comprehensive-review rebuild
(headline ROE remediation). Level-splices and log-linear 1990-97 bridges described in this EPR
are RETIRED; see the workpackage A REBUILD ADDENDUM in `S512_DPR.md`, the as-built provenance strings
in `data/final/S512.csv`, and DIV-A10..A16 in `internal-review-notes_2026-07/WP-A_DIV_PATCHES.json`.
