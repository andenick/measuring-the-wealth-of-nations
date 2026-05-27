# S703 — Value-Price Deviations (real, consistent-procedure regression)

## Series

- **SID**: S703
- **Name**: Value-Price Deviations (Chapter 7 consistent-procedure regression; real implementation v1.1)
- **Chapter**: 7; registry `book_table` label "7.3" is project-internal — the book has no literal Table 7.3. The empirical anchor is Khanjian (1989) 6–9% S*/V* deviation reported in **Ch. 7 §7.3** (p.223) and the consistent-procedure framework in **Ch. 4 §4.1** Tables 4.1–4.3
- **Status**: validated_book_and_extension
- **Status note**: (v1.1 Phase 4 — proxy:true retired)
- **Units**: percent (aggregate S*/V* deviation between price and value forms); also reports per-year R² from cross-sectional regression

## Methodology — real implementation (v1.1 Phase 4)

S703 implements the book's consistent-procedure cross-sectional regression per ST 1994 Ch4 §4.1 + Ch7 §7.3 (p.223). The v1.0 percent-deviation scalar `(S702 - S701)/S701 * 100` (which was algebraically identical to S513 * 100 — see DIV-011 supersession note) has been retired. With both S701 and S702 now real and sector-disaggregated in v1.1, the book's empirical test is performed for the first time.

Procedure (per `Technical/code/P02_processors/P02_S703_value_price_deviations.py`, v1.1 rewrite):

```
per benchmark year y:
  log(lambda*_j) ~ a_y + b_y * log(pp*_j)        # cross-sectional OLS across 8 ST productive sectors
  R²_y = goodness of fit
  S*/V*_value(y), S*/V*_price(y) = aggregate rates of surplus value, value and price forms
  deviation_pct(y) = |S*/V*_price(y) - S*/V*_value(y)| / S*/V*_value(y) * 100
```

The Khanjian (1989) 6–9% S*/V* envelope (ST 1994 Ch7 §7.3 p.223) is the load-bearing PASS/FAIL anchor; R² is a secondary diagnostic with small-cross-section caveats (8 productive sectors per benchmark year).

## Sources

- **L01 + P02 (real implementation)**: real S701 + S702 upstream (v1.1); `Technical/code/P02_processors/P02_S703_value_price_deviations.py` (v1.1 rewrite, runs cross-sectional regression and computes Khanjian-style aggregate deviation)
- **No new external data fetches required** — S703 is a pure regression on real upstream sector vectors
- **External comparator**: Khanjian (1989) "The Empirical Evidence Relating to the Existence of Prices of Production: A Critique of Wolff," *Review of Radical Political Economics*; serves as V03_S703 anchor
- **KB chunks**: `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_11/full_transcription.md` (Ch4 §4.1 Tables 4.1-4.3 — consistent/inconsistent procedure); `chunk_25/full_transcription.md` (Ch7 §7.3–§7.4 — Khanjian 6–9%, Wolff 12–15% bias); `chunk_33/full_transcription.md` (Appendix G V* methodology); `chunk_34/full_transcription.md` (Appendix G Table G.2 V* formulas); `chunk_36/full_transcription.md` (Appendix J C*/TP* stability)
- **Book tables**: Ch4 §4.1 Tables 4.1, 4.2 (consistent procedure worked examples); Table 4.3 (inconsistent symmetric-treatment diagnosis); §5.10 Table 5.12, Figure 5.25 (Khanjian comparison)
- **Upstream series**: **S701 (real lambda* — v1.1)**, **S702 (real pp* — v1.1)**, S513 (Marxian profit rate r_bar, used in S702)

## Reference values

Coordinator backfills from `Technical/chopped/S703.csv` after agents 1-3 commit P02_S703 rewrite and `O01_generate_chopped.py` regenerates chopped output.

- Six SIC benchmark years (book period): 1947, 1958, 1963, 1967, 1972, 1977
- Extension years (NAICS): 1997, 2002, 2007, 2012 (per upstream S701/S702 NAICS benchmark availability)
- **Khanjian benchmark**: 6–9% S*/V* deviation between price and value forms (ST 1994 Ch7 §7.3 p.223) — primary PASS/FAIL anchor
- **Wolff comparator**: 12–15% upper envelope (sum of Wolff 4–8% inconsistent-procedure bias + Khanjian 6–9% baseline)
- v1.1 `expected_range` tightened to `[0.0, 15.0]` (vs v1.0 proxy's `[0.0, 100.0]` that had to accept matrix-artifact range)
- Book does NOT literally claim R² > 0.95 (prior research-file attribution flagged for re-verification); R² treated as secondary diagnostic only
- Note: v0 ST2-era implementation R² 0.70–0.98 was driven by scalar-λ_m + GO−V* surplus error in the proxy, not by a real failure of LTV; v1.1 sector-disaggregated procedure should produce R² consistent with the consistent-procedure framework

## Known issues

- **BLS CES 2003 overhaul null bridge (DIV-010)**: propagates from upstream S701/S702.
- **SIC↔NAICS coarse concordance (DIV-008 reference)**: propagates from upstream.
- **Small cross-section (6 SIC + 4 NAICS benchmark years × 8 productive sectors)**: R² should be interpreted cautiously; aggregate Khanjian deviation magnitude is the load-bearing test.
- **1963 benchmark anomaly (WARN-03)**: may propagate from upstream IO data gap; if observed in V03, document as known_issue rather than re-introducing proxy.
- **Book R²>0.95 attribution unverified**: prior research files assert R²>0.95; direct Ch7 re-read finds no such literal claim. Load-bearing book number is Khanjian's 6–9% S*/V*, not 95% R².
- **Sector-level value-added decomposition (ST 1994 §4.2 pp.86-88)**: handled inside upstream S701/S702 v1.1 implementations; S703 inherits the disaggregated form.

## Cross-references

- Upstream: **S701 (real labor values — v1.1)**, **S702 (real prices of production — v1.1)**, S513 (Marxian profit rate)
- Downstream: none (S703 is the empirical test endpoint of the Ch7 framework)
- Related external: Khanjian (1988, 1989), Wolff (1977a/b, 1979, 1987), Sharpe (1982); ST 1994 Ch7 §7.4 cross-study critique
- Divergence record: `DIVERGENCE_REGISTER.json` entry DIV-011 (Chapter 7 proxy retirement)

## Provenance trail

- **Original research**: `Technical/research/S703_research.json`, researcher `agent`, 2026-05-06; ported from `ST2/research/T703_research.json` on 2026-05-14; verbatim quotes backfilled 2026-05-19 and 2026-05-23
- **DPR v1.0**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (proxy disclosure version)
- **DPR v1.1 (this version)**: 2026-05-24, v1.1 Phase 4 iteration 5 Ch7 real-fix agent 4. Real implementation replaces proxy disclosure. See DIV-011.
- **Anu Framework stage**: Stage 5 EXECUTION (Ch7 real-fix sub-stage); doctor gate IDs P13/P31/P36
