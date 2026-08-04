# EPR: S701 — Labor Values (real, sector-disaggregated, hr/$)

**Series**: S701
**Generated**: 2026-05-24T06:00:00Z (v1.1 Phase 4 iteration 5 Ch7 real-fix)
**Status**: validated_book_and_extension
**Supersedes**: prior `EXTENSION NOT APPLICABLE` stub (v1.0 iteration 9), authored when S701 was a Leontief-column-mean proxy with `extension: null`. v1.1 Phase 4 retires the proxy and populates a real extension arm.

## 1. shaikh_source

> "For the production sector j, let lambda_j = labor value per unit output; hp_j = hours of productive labor per unit output; app_ij = quantity of the ith production input used per unit output … Then unit labor values must satisfy the relation lambda_j = hp_j + sum_i lambda_i * app_ij. If we define row vectors lambda and hp … and an input-output coefficients matrix of (productive) inputs app … then we may equivalently write: lambda = hp + lambda * app; lambda = hp * (I - app)^{-1}." (Shaikh & Tonak 1994, Ch. 4 §4.1, p. 80)

> "Actual case (IO tables use money flows at producer prices): instead of quantity coefficients app_ij, we have money value coefficients app*_ij = p_i * app_ij / p_j … Corresponding labor coefficients: hp*_j = hp_j / p_j. Empirical formulas: lambda* = hp* + lambda* * app*; lambda* = hp* * (I - app*)^{-1}; where lambda* = row vector of labor-value/producer-price ratios, lambda*_j = lambda_j / p_j." (S&T 1994, Ch. 4 §4.1, p. 81)

> "app* = [1/5] ($/$ input coefficient); hp* = (8/5) (hr/$ labor coefficient); lambda* = hp* * [I - app*]^{-1} = (8/5) * [1 - 1/5]^{-1} = (8/5) * (5/4) = 2 hr/$. Verification: lambda* should equal TV/GO_p = 2000 hr / $1000 = 2 hr/$." (S&T 1994, Ch. 4 §4.1 Figure 4.3 dimensional check, p. 83)

Source: Shaikh, A., & Tonak, E. A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press. The load-bearing book quantity is `hp*_j` (productive-labor-hours per dollar of producer-price gross output, hr/$), recovered for the first time in v1.1 Phase 4 from BLS production-worker counts × average weekly hours ÷ BEA sector gross output, filtered through book Appendix F productive shares.

## 2. shaikh_appendix_ref

Primary methodology: **Chapter 4 §4.1**, pp. 78–88 (closed-form labor-value equations + Figure 4.3 worked example).
Sector enumeration: **Appendix G Table G.2** (the 8 ST productive sectors: agriculture, mining, construction, manufacturing, transportation & public utilities, productive services, government enterprises federal, government enterprises state-local).
Productive/unproductive split: **Appendix F Table F.1** (chunk 32 / pp. 292–301; book's annual labor decomposition, 1948–89). v1.1 substitute filter at `Technical/data/source/appendix_F/Table_F_1.csv` is an 85-sector categorical productive/unproductive mask derived from the predecessor-build `io_85_to_nipa_13_concordance.csv` + Mohun (2013) Tables 2-3, used because the per-sector fractional filter the user initially expected does not literally exist in the book.
Chapter 7 magnitude anchor: **Ch. 7 §7.3** p. 221 ("Marxian total product TP* is roughly 82% of the IO measure of gross product GP, but about 1.5 times larger than the conventional measure of GNP") — gives the qualitative ballpark S701 feeds.
Cross-check Figures: 4.3 (dimensional verification), 7.1.

## 3. extension_source

**Three feed-in sources, all real-data, all v1.1 Phase 4**:

1. **BLS Current Employment Statistics (CES)** — production-worker employment counts `(Lp)_j` and average weekly hours `(h)_j` per supersector, 1948–2024 where available (mining + construction + manufacturing have full 1948+ coverage; services 1964+; trade subsectors 1972+). Cached at `data/raw/Inputs/API_Data/BLS/bls_ces_<supersector_slug>_employment.csv` and `bls_ces_<supersector_slug>_hours.csv` / `_hours_alt.csv`, pulled 2026-05-24 via `Technical/code/L00_setup/L00_bls_fetch.py`. Provenance: `data/raw/Inputs/API_Data/BLS/bls_ces_fetch_provenance.json`. The BLS API key is read from the environment or a local `api_keys.env` file.

2. **BEA gross output `X_j`** — NIPA Table 1.7.5 (Gross Output by Industry, annual 1947+) and BEA Industry GDP-by-Industry (NAICS, 1997+). Cached at `data/raw/Inputs/API_Data/BEA/nipa_1_7_5_gross_output_by_industry.csv` and `gdp_by_industry_gross_output.csv`, pulled 2026-02-24 via `pull_bea_nipa_ch05.py`. Provenance: `data/raw/Inputs/API_Data/BEA/provenance.json`.

3. **BEA IO matrices** — the `(I - A*)^{-1}` Leontief inverse over BEA benchmark IO tables (1947-1977 SIC; 1997-2017 NAICS). **[SUPERSEDED — workpackage C v2.0 / F3 2026-07-07]** the published v2.0 engine reads the REBUILT cache `Technical/data/intermediate/io_matrices_rebuilt/` (via `utils.io_rebuilt`). The old labeled cache was proved DEFECTIVE (P2_MATRIX_VERIFICATION: labeled L not Leontief inverses; A column-share-normalized; NAICS A non-square 75x65) and retired to `Technical/MIGRATION/retired_io_20260707/io_matrices_labeled/`. Appendix F productive-share filter `Technical/data/source/appendix_F/Table_F_1.csv` is applied to mask unproductive sectors before computing the Leontief inverse on the productive sub-matrix.

Construction (per `Technical/code/P02_processors/P02_S701_labor_values.py` rewritten v1.1): per benchmark year, `hp*_j = (Lp_j * h_j * 52) / X_j`; then `lambda*_j = hp* * (I - A*_p)^{-1}` on the productive sub-matrix; sector results aggregated across the 8 ST productive sectors per Appendix G Table G.2.

## 4. extension_url

BLS Public API v2: `https://api.bls.gov/publicAPI/v2/timeseries/data/` (per-supersector CES series IDs: `CES<supersector>00000006` employment, `CES<supersector>00000007` average weekly hours, `CES<supersector>00000033` production-worker hours where published).

BEA API:
- NIPA gross output: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=NIPA&TableName=T10705&Frequency=A&Year=ALL&ResultFormat=JSON`
- GDP-by-Industry (NAICS): `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=GDPbyIndustry&TableID=15&Industry=ALL&Year=ALL&Frequency=A&ResultFormat=JSON`

BEA IO benchmark archive: https://www.bea.gov/industry/input-output-accounts-data

## 5. conceptual_continuity

`hp*_j` (hr/$) is a directly observable quantity: hours of productive labor per dollar of producer-price gross output, sector by sector. The book period (1947–1977 SIC benchmark years) and the extension period (1997+ NAICS benchmark years) compute *exactly the same formula* on extended data — there is no construct change, only a sector-classification change (SIC → NAICS) and a benchmark-year refresh. `lambda*_j = hp* * (I - A*)^{-1}` is then a matrix product on the same producer-price IO substrate the book uses. Because the construction is formula-based (not a directly-observed time series), an Anu growth-rate splice would be invalid here (per Anu rule "No Lazy Splices on Derived Quantities"); instead, the extension recomputes the formula on the NAICS substrate and reports the SIC/NAICS junction discontinuity honestly through the labeled-IO concordance documented in DIV-008. Methodological consistency book ↔ extension: identical (same Ch4 §4.1 formula, same productive-share filter concept, same Leontief inverse on productive sub-matrix).

## 5a. precision_and_uncertainty (DIV-042, Tier-A W1d 2026-07-08)

Published S701 values (final/chopped/extenbook) are reported to **3 significant figures**, with the DIV-042 uncertainty band in `data/final/S701_LAMBDA_BAND.csv` (lo = central/1.115, hi = central/0.885 — worst-case common-mode propagation of the ~±11.5% recovered-X_j bound; F3 sensitivity CSVs, `internal-review-notes_2026-07-07/`, 2026-07-07). Monte-Carlo (independent per-sector errors) half-widths are tighter: ±2.7–4.3% for the S701 aggregate; sector-level λ_j carries ±7–11%. The former 15–17 displayed digits were false precision. Full float64 precision is preserved in `data/intermediate/S701.csv`; the rounding is display-stage only (P02 final emit) and does not enter any downstream computation (S703 reads the full-precision L01 panels).

## 6. vintage_note

Book values (six SIC benchmark years 1947, 1958, 1963, 1967, 1972, 1977) computed from BEA SIC-basis benchmark IO tables as published 1947–1981 and BLS CES vintages back-revised to current vintage. Extension years (1997+) computed from BEA NAICS GDP-by-Industry pulled 2026-02-24 (approximately September 2025 NIPA vintage) and BLS CES pulled 2026-05-24. The 1990–1996 gap is the SIC–NAICS junction; no values are interpolated across it — the extension arm reports only NAICS-basis benchmark years. BLS CES values pre-June-2003 have been back-revised by ~22 years of annual benchmark revision into post-overhaul methodology; DIV-010 documents the 2003 methodology break and ships a null-bridge mechanism (factor=1.0 per supersector) that v1.2 will populate with non-null factors sourced from the BLS Employment Situation news-release archive. BEA comprehensive revisions (1999, 2003, 2009, 2013, 2018) alter post-1997 values relative to the book; pre-1997 book values are frozen at book vintage.
