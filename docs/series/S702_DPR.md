# S702 — Prices of Production (real, sector-disaggregated)

## Series

- **SID**: S702
- **Name**: Prices of Production (Chapter 7 series; real implementation per Ch4 §4.1 sector-disaggregated procedure)
- **Chapter**: 7; registry `book_table` label "7.2" is project-internal. The classical price-of-production methodology lives in **Chapter 4 §4.1** (pp.78-88)
- **Status**: validated_book_and_extension
- **Status note**: (v1.1 Phase 4 — proxy:true retired)
- **Units**: labor-value units (sector pp*_j in hr-equivalent of producer-price gross output)

## Methodology — real implementation (v1.1 Phase 4)

S702 implements the book's classical formula `pp*_j = (1 + r_bar)(c_j_labor + v_j_labor)` per ST 1994 Ch4 §4.1 (pp.81-83), with `c_j` and `v_j` constructed sector-by-sector via the matrix products quoted in p.81 and pp.81-82. The v1.0 scalar proxy `S701_proxy * (1 + r*)` has been retired (DIV-011); the real implementation works on sector vectors.

Formula (per `Technical/code/P02_processors/P02_S702_prices_of_production.py`, v1.1 rewrite):

```
c_j_labor = sum_i lambda_i* * (M_p)_p,ij        # constant capital, labor-value units, per sector
v_j_labor = sum_i lambda_i* * (CONW_p)_p,ij     # variable capital, labor-value units, per sector
pp*_j     = (1 + r_bar) * (c_j_labor + v_j_labor)
```

where `lambda*_j` (hr/$) comes from real S701 (v1.1), `(M_p)_p,ij` is the producer-price component of input flows from sector i to sector j (from labeled BEA IO matrices filtered by Appendix F), `(CONW_p)_p,ij` is the producer-price component of the production-worker consumption basket (constructed from BLS CES production-worker compensation + BEA NIPA EC/WS ratio), and `r_bar` is the uniform Marxian rate of profit from S513.

The book's verbatim methodological constraint (p.81) — that lambda*_j must be applied only to the producer-price components of commodity flows — is satisfied by construction. The Khanjian (1989) 6–9% S*/V* deviation envelope is now measurable for the first time via V03_S703.

## Sources

- **L01 + P02 (real implementation)**: `Technical/code/L01_loaders/L01_S702.py` (v1.1, loads real S701 lambda*, BLS CES wages, BEA NIPA EC tables, labeled IO matrices); `Technical/code/P02_processors/P02_S702_prices_of_production.py` (v1.1 rewrite, sector-disaggregated c/v construction and pp* aggregation)
- **External data — real fetches**:
  - Real S701 lambda*_j vector (upstream, v1.1)
  - BLS CES production-worker wages + employment + weekly hours, cached at `data/raw/Inputs/API_Data/BLS/` (pulled 2026-05-24)
  - BEA NIPA employee compensation tables (T10604 wages & salaries by industry), cached at `data/raw/Inputs/API_Data/BEA/` (pulled 2026-02-24)
  - BEA IO matrices supplying the input flows. **[SUPERSEDED — workpackage C v2.0 / F3 2026-07-07]** the published v2.0 engine reads the REBUILT cache `Technical/data/intermediate/io_matrices_rebuilt/` (via `utils.io_rebuilt`); the old defective labeled cache was retired to `Technical/MIGRATION/retired_io_20260707/io_matrices_labeled/`.
  - Appendix F productive-share filter, at `Technical/data/source/appendix_F/Table_F_1.csv`
- **KB chunks**: `data/raw/kb/book_digitization/chunk_11/full_transcription.md` (Ch4 §4.1 — disaggregated c, v construction); `chunk_14/full_transcription.md` (Ch5 §5.3 + Appendix G — variable capital, ec and wp); `chunk_15/full_transcription.md` (Section 5.5 profit-rate measures); `chunk_31/full_transcription.md` (Appendix E Tables E.1 / E.2); `chunk_33/full_transcription.md` (Appendix G Tables G.1 / G.2)
- **Book tables**: Ch4 §4.1 equations pp.78-88 (sector-disaggregated procedure); Appendix E Tables E.1 (`C* = M'_p + Dp` annual 1948-1989), E.2 (constant capital components); Appendix G Tables G.1 / G.2 (variable capital, sectoral Lp)
- **APIs**: BLS Public API v2; BEA API
- **Upstream series**: S401 (A-matrix), S402 (Leontief inverse B), S513 (Marxian profit rate r_bar), **S701 (real lambda* — v1.1)**

## Reference values

Coordinator backfills from `Technical/chopped/S702.csv` after agents 1-3 commit L01/P02 rewrites and `O01_generate_chopped.py` regenerates chopped output. Expected magnitude: pp*_j is O((1+r_bar) * lambda*_j) with r_bar typically 0.4–0.6 in book period.

- Six SIC benchmark years (book period): 1947, 1958, 1963, 1967, 1972, 1977
- Extension years (NAICS): 1997, 2002, 2007, 2012
- Markup `pp*_j / lambda*_j ≈ 1 + r_bar` expected at all benchmark years (book finding qualitatively confirmed: prices systematically exceed labor values via profit-rate markup)
- **Khanjian benchmark**: 6–9% deviation in S*/V* between price and value forms (ST 1994 Ch7 §7.3 p.223) — now measurable for the first time via S703
- 1948–1980 book aggregate finding: Marxian profit rate r* fell by almost a third, driven by C*/V* rising 77%
- 1980–1989 book aggregate finding: r* partially recovered by ~7% of its 1948 value as the rate of surplus value accelerated

## Precision & uncertainty (DIV-042) — Tier-A W1d, 2026-07-08

Published S702 values (`data/final/S702.csv`, `chopped/S702.csv`, extenbook Data sheet) are reported to **3 significant figures** with an explicit uncertainty-band sidecar at `data/final/S702_LAMBDA_BAND.csv` (year, central, lo, hi, basis). Basis: **DIV-042** — the SIC-era per-sector gross output X_j entering both the hours-allocation weights and the coefficient denominator `hu*_j = hu_j/X_j` is *recovered* (X = II_IO + bucket-VA) with a measured median per-sector error of ~±11.5%. The F3 sensitivity propagation (`internal-review-notes_2026-07-07/F3_lambda_sensitivity_{aggregate,sector}.csv`, 2026-07-07) shows the published S702 aggregate is honest only to ±6.4–9.4% (independent-error Monte Carlo — little averaging: only 2–5 covered unproductive sectors) up to ±11.65% (worst-case common-mode); sector-level λ_j carries ±7–11%. The previous 15–17 displayed digits were false precision. The band uses the worst-case common-mode bound: `lo = central/1.115`, `hi = central/0.885` (λ ∝ 1/X, hence asymmetric). Rounding is applied ONLY at the P02 final-emit stage (`P02_S702_prices_of_production._round_sig`); `data/intermediate/S702.csv` retains full float64 precision for regression/reproducibility, and downstream S703 consumes the full-precision L01 panels, not the rounded published values.

## Known issues

- **BLS CES 2003 overhaul null bridge (DIV-010)**: same v1.1 null-factor stubs as S701; v1.2 follow-up sources non-null factors from BLS Employment Situation news-release archive.
- **SIC↔NAICS coarse concordance (DIV-008 reference)**: applies to post-1997 extension arm; sector-mapping ambiguities documented.
- **`λ_m` aggregation note**: the book Section 4.2 (pp.86-88) describes sector-level value-added decomposition; v1.1 implementation works on sector vectors throughout (per Ch4 §4.1 procedure) — the v1.0 single-scalar `λ_m` defect is fully addressed.
- **Surplus accounting**: v1.1 uses VA*_j − V*_j per book Ch4 §4.1 (not the v1.0 GO_j − V*_j proxy error which misallocated depreciation).
- **1963 benchmark anomaly (WARN-03)**: may inherit from upstream S701 if the underlying labeled IO matrix has a 1963 gap; document via known_issues if observed in V03 rather than re-introducing proxy.
- **Six SIC benchmark years only** for book period.

## Cross-references

- Upstream: S401 (A-matrix), S402 (Leontief inverse B), **S701 (real lambda* — v1.1)**, S513 (Marxian profit rate), Appendix E Tables E.1 / E.2, Appendix G Tables G.1 / G.2, Appendix F productive-share filter
- Downstream: S703 (consistent-procedure regression, now real)
- Related external: Khanjian (1989) 6–9% S*/V* benchmark; Wolff (1977b) symmetric-treatment biases; ST 1994 Ch7 §7.4 cross-study critique
- Project artifacts: `internal-notes/CH7_REAL_FIX_PLAN.md`; `Technical/_v1.1_patches/S702_ch7_realfix_patch.json`; `Technical/_v1.1_patches/DIVERGENCE_REGISTER_DIV011_patch.json`

## Provenance trail

- **Original research**: `Technical/research/S702_research.json`, researcher `agent`, 2026-05-06; ported from `predecessor-build/research/T702_research.json` on 2026-05-14; verbatim quotes backfilled 2026-05-19 and 2026-05-23
- **DPR v1.0**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (proxy disclosure version)
- **DPR v1.1 (this version)**: 2026-05-24, v1.1 Phase 4 iteration 5 Ch7 real-fix agent 4. Real implementation replaces proxy disclosure. See DIV-011.
- **Anu Framework stage**: Stage 5 EXECUTION (Ch7 real-fix sub-stage); doctor gate IDs P13/P31/P36
