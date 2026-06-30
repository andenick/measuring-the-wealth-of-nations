# S701 — Labor Values (real, sector-disaggregated, hr/$)

## Series

- **SID**: S701
- **Name**: Labor Values (Chapter 7 series; real implementation per Ch4 §4.1 formula)
- **Chapter**: 7 (book §§7.1–7.5 magnitude framework); registry `book_table` label "7.1" is project-internal — the book's actual Table 7.1 is profit/accumulation/burden rates. The labor-value methodology lives in **Chapter 4 §4.1** (pp.78–88) and **Appendix G** (pp.304–322)
- **Status**: validated_book_and_extension
- **Status note**: (v1.1 Phase 4 — proxy:true retired)
- **Units**: hr/$ (labor-hours per dollar of producer-price gross output), per Ch4 §4.1 Figure 4.3 dimensional verification

## Methodology — real implementation (v1.1 Phase 4)

S701 implements the book's closed-form labor-value equation `lambda* = hp* * (I - A*)^{-1}` per ST 1994 Ch4 §4.1 (pp.80–83), where `hp*_j = hp_j / p_j` is the per-sector productive-labor-hours per dollar of producer-price gross output (hr/$). The v1.0 Leontief-column-mean proxy `mean(column_sum((I - A)^{-1}))` has been retired (DIV-011); the real implementation computes `hp*` directly from data.

Formula (per `Technical/code/P02_processors/P02_S701_labor_values.py`, v1.1 rewrite):

```
hp*_j = (Lp_j * h_j * 52) / X_j        # hr/$ per productive sector j
lambda*_j = hp* * (I - A*_p)^{-1}      # hr/$ sector vector; A*_p = productive sub-matrix
```

where `Lp_j` is BLS production-worker employment count per supersector (CES dataset), `h_j` is BLS average weekly hours per supersector, `X_j` is BEA producer-price gross output per sector (NIPA Table 1.7.5 SIC / GDP-by-Industry NAICS), and `(I - A*_p)^{-1}` is the Leontief inverse of the productive sub-matrix from labeled BEA benchmark IO tables filtered by the Appendix F productive-share mask. Sector aggregation follows the 8 ST productive sectors enumerated in Appendix G Table G.2 (agriculture, mining, construction, manufacturing, transportation & public utilities, productive services, government enterprises federal, government enterprises state-local).

The book's dimensional verification (Figure 4.3 p.83) — `lambda* = TV / GO_p` in hr/$ — is satisfied by construction for the first time in v1.1; the v1.0 proxy could not perform this check because it omitted `hp*` entirely.

## Sources

- **L01 + P02 (real implementation)**: `Technical/code/L01_loaders/L01_S701.py` (v1.1, loads BLS CES + BEA gross output + labeled IO matrices + Appendix F filter); `Technical/code/P02_processors/P02_S701_labor_values.py` (v1.1 rewrite, applies hp* formula then Leontief inverse on productive sub-matrix)
- **External data — real fetches**:
  - BLS CES production workers + weekly hours, cached at `data/raw/bls/bls_ces_<supersector>_employment.csv` and `_hours.csv` / `_hours_alt.csv` (pulled 2026-05-24 via `Technical/code/L00_setup/L00_bls_fetch.py`; provenance at `bls_ces_fetch_provenance.json`)
  - BEA gross output, cached at `data/raw/bea/nipa_1_7_5_gross_output_by_industry.csv` + `gdp_by_industry_gross_output.csv` (pulled 2026-02-24; provenance at `data/raw/bea/provenance.json`)
  - Labeled BEA IO matrices, cached at `Technical/data/intermediate/io_matrices_labeled/` (from `data/raw/io_matrices/`)
  - Appendix F productive-share filter, at `Technical/data/source/appendix_F/Table_F_1.csv` (85-sector categorical mask, derived from predecessor-build `io_85_to_nipa_13_concordance.csv` + Mohun 2013 Tables 2-3, provenance at `Technical/data/source/appendix_F/PROVENANCE.md`)
- **KB chunks**: `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_11/full_transcription.md` (Ch4 §4.1 pp.78-83 — closed-form equations + Figure 4.3); `chunk_14/full_transcription.md` (Appendix G variable capital); `chunk_15/full_transcription.md` (sector composition); `chunk_31/full_transcription.md` (Appendix E sectoral GVAp); `chunk_33/full_transcription.md` (Appendix F + G intro)
- **Book tables**: Ch4 §4.1 equations pp.80-83 (Figure 4.3 dimensional check); Appendix G Table G.2 (sectoral productive employment); Appendix F (productive shares — book's annual labor decomposition pp.292–301); Appendix E Tables E.1 / E.2
- **APIs**: BLS Public API v2 (free registration key, supplied via the `BLS_API_KEY` environment variable); BEA API
- **Upstream series**: S401 (A-matrix), S402 (Leontief inverse B), S513 (Marxian profit rate, used in downstream S702/S703)

## Reference values

Coordinator backfills from `Technical/chopped/S701.csv` after agents 1-3 commit L01/P02 rewrites and `O01_generate_chopped.py` regenerates the chopped output. Expected magnitude: O(0.1–10) hr/$ per sector; book Figure 4.3 worked-case anchor is 2 hr/$ for a single-sector toy economy.

- Six SIC benchmark years (book period): 1947, 1958, 1963, 1967, 1972, 1977
- Extension years (NAICS basis): 1997, 2002, 2007, 2012 (per BEA benchmark IO availability)
- Book's qualitative magnitude framework (Ch7 §7.3 p.221): **"Marxian total product TP* is roughly 82% of the IO measure of gross product GP, but about 1.5 times larger than the conventional measure of GNP."** S701 lambda* aggregates feed this framework via downstream Ch7 series.
- Dimensional verification (Figure 4.3 p.83): `lambda* = TV / GO_p` in hr/$ — satisfied by construction in v1.1, was unsatisfiable in v1.0 proxy.

## Known issues

- **BLS CES 2003 overhaul null bridge (DIV-010)**: v1.1 ships factor=1.0 stubs per supersector; non-null factors deferred to v1.2 (BLS Employment Situation news-release archive sourcing). Effect: intra-extension trend from 2003 onward may carry minor methodology-break artifacts; the 1989 SIC↔NAICS anchor reconciliation remains the dominant cross-period level adjustment.
- **SIC↔NAICS coarse concordance** (post-1997 sector mapping; DIV-008 reference): productive-classification mapping book ↔ extension is at supersector granularity; finer-grained sector reassignments not yet handled.
- **1963 benchmark anomaly (WARN-03)**: v1.0 proxy showed S701 = 0.00037 at 1963 (likely IO data gap); v1.1 real implementation may inherit if the gap is in the underlying labeled IO matrix. If V03 surfaces it, document as known_issue rather than re-introducing proxy.
- **Services sector compensation proxy**: per ST methodology, average compensation `ec_serv` is used as a stand-in for `(ecp)_serv` because BLS production-wage data are unavailable for services. Documented in Appendix G; preserved in v1.1 real implementation.
- **Agriculture productive-employment proxy**: ST uses mining-sector Lp/L ratio for agriculture (own BLS production-worker data unavailable). Preserved in v1.1.
- **Appendix F filter is categorical**: the 85-sector productive/unproductive mask in `Technical/data/source/appendix_F/Table_F_1.csv` is binary (productive=1.0, unproductive=0.0, plus 3 uncertain sectors flagged) rather than fractional. The per-sector fractional shares the user originally envisioned do not literally exist as a published table; within-sector productive ratios are applied at compute time via BLS production-worker series per ST/Mohun methodology.
- **Six SIC benchmark years only** for book period; no annual interpolation within the book period.

## Cross-references

- Upstream: S401 (A-matrix), S402 (Leontief inverse B), Appendix F productive-share filter, Appendix G Table G.2 (sectoral productive employment), BLS CES, BEA NIPA 1.7.5 / GDP-by-Industry
- Downstream: S702 (prices of production, now also real and sector-disaggregated), S703 (consistent-procedure regression)
- Related external: Wolff (1977b) symmetric-treatment biases S*/V* upward 4–8%; Khanjian (1989) consistent procedure 6–9% S*/V* deviation; ST 1994 Ch7 §7.4 cross-study critique
- Project artifacts: `Technical/Handoffs/CH7_REAL_FIX_PLAN.md`; `Technical/_v1.1_patches/S701_ch7_realfix_patch.json`; `Technical/_v1.1_patches/DIVERGENCE_REGISTER_DIV011_patch.json`

## Provenance trail

- **Original research**: `Technical/research/S701_research.json`, researcher `agent`, 2026-05-06; ported from `predecessor-build/research/T701_research.json` on 2026-05-14; verbatim quotes backfilled 2026-05-19 and 2026-05-23 (Stage 1 cohort 3 enrichment specifically anchored Ch4 §4.1 equations + Figure 4.3 dimensional check)
- **DPR v1.0**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (proxy disclosure version)
- **DPR v1.1 (this version)**: 2026-05-24, v1.1 Phase 4 iteration 5 Ch7 real-fix agent 4 (registry/DPR/EPR cohort, parallel to agents 1-3 doing L01/P02 rewrites). Real implementation replaces proxy disclosure. See DIV-011.
- **Anu Framework stage**: Stage 5 EXECUTION (Ch7 real-fix sub-stage); doctor gate IDs P13/P31/P36
