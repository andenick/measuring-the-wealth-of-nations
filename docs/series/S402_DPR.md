# S402 — B-Matrix Summary (Leontief Inverse)

## Series

- **SID**: S402
- **Name**: B-Matrix (Leontief Inverse) — Summary
- **Chapter**: 4; book Table 4.2
- **Status**: book_period_validated
- **Status note**: (matched scope to S401 — SIC-only published spine)
- **Units**: matrix-summary scalars (n_sectors, max_b_element, b_column_sum_max, b_trace, b_frobenius_norm) per benchmark year

## Methodology

S402 is the Leontief inverse derived from S401 by `B = (I - A)^{-1}`. Each element `b_ij` gives the total output of sector i required directly plus indirectly per unit of final demand for sector j. The derivation requires inverting the `n × n` matrix `(I - A)` for each of the six benchmark years (1947, 1958, 1963, 1967, 1972, 1977) at the standardized 85×85 SIC sector aggregation produced by S401's pipeline (Appendix A multi-stage aggregation, force-account reversal, real-estate adjustment, eating-and-drinking-places estimation). The verbatim book derivation is **"λ = hp + λ · app  ⇒  λ = hp · (I − app)^{-1}."** (ST 1994 Ch4 §4.1, p.81) and, in money-flow form, **"Empirical formulas (λ* = hp* + λ* · app*  ⇒  λ* = hp* · (I − app*)^{-1}) where λ* = row vector of labor-value/producer-price ratios and app* is the productive-input coefficient matrix in money flows at producer prices."** (ST 1994 Ch4 §4.1, p.81).

In the S&T framework B is the operator that converts direct labor coefficients into embodied (total) labor values; equivalently, `x = B · f` maps final demand vectors to required gross output vectors. The labor-value vector `lambda* = hp* · B` and the total constant-capital and total surplus-value computations in Chapter 5 all flow through B. The worked example on p.83 demonstrates: with a single productive sector, `app* = 1/5` and `hp* = 8/5`, so `lambda* = (8/5)(1 - 1/5)^{-1} = (8/5)(5/4) = 2 hr/$`, which equals `TV/GO_p = 2000 hr / $1000`. This is the dimensional check confirming `(I - A*)` is invertible and `(I - A*)^{-1}` is non-negative — the Hawkins-Simon productive-economy condition that S401's max-eigenvalue diagnostic verifies upstream.

S402's published summary scalars are `n_sectors`, `max_b_element`, `b_column_sum_max`, `b_trace` (which must be ≥ `n_sectors` because `B = I + A + A^2 + …` makes the diagonal ≥ 1), and `b_frobenius_norm` (range [10.47, 103.02] over the six benchmarks — high at 1947 due to the near-singular A-matrix, normal range otherwise). S402 is a benchmark cross-section and per VAR-006 skips the chopped CSV / Extenbook pipeline. Note also that B is computed at producer prices, not unit quantities — the verbatim caveat is **"It is important to note that while there is enough information in standard (i.e. producer-price) input-output tables to calculate the purchaser price of aggregate inputs, outputs, and final demand components, there is not enough to calculate the purchaser price of individual commodities."** (ST 1994 Ch4 §4.1, p.80).

## Sources

- KB chunks: `data/raw/kb/book_digitization/chunk_10/full_transcription.md` (Ch4 §4.1, pp.78-83 — closed-form Leontief inverse, worked example); `chunk_27/full_transcription.md` (Appendix A — aggregation pipeline propagating into B)
- Book tables: ST 1994 Table 4.2 (B-Matrix) at 85×85 producer-price level
- External sources: BEA Benchmark Input-Output Accounts (1947, 1958, 1963, 1967, 1972, 1977) via S401 dependency
- Local files: derived in-pipeline from S401 outputs via `code/utils/io_matrix.py`; printed-book digitization at `data/source/book_tables/ch04/Table4_2_BMatrix.csv`

## Reference values

- Six benchmark years matching S401: 1947, 1958, 1963, 1967, 1972, 1977
- `b_frobenius_norm` range: `[10.47, 103.02]` — high at 1947 (near-singular A), normal otherwise
- `b_trace ≥ n_sectors` at every year (mathematical guarantee from `B = I + A + A^2 + …`)
- `(I - A)(I - A)^{-1} ≈ I` (leontief_max_dev < 1e-9 at all benchmarks where A is well-conditioned)
- Worked numerical check from Ch4 Figure 4.3 p.83: with `app* = 1/5`, `hp* = 8/5`, `lambda* = 2 hr/$`

## Known issues

- All approximation errors in S401's A-matrix (eating/drinking places, FAC scaling, g=0.25 ground rent) propagate into B through matrix inversion; the inversion can amplify near-singular behavior at 1947
- Numerical stability at 1947 is the worst of the six benchmarks (Frobenius norm 103.02 vs. ~10-30 elsewhere) and is a documented S&T issue, not a project artifact
- B is constructed at producer prices, not unit quantities, per the Ch4 §4.1 caveat — this matters when S701/S702 attempt to construct sector-disaggregated labor values
- No NAICS extension in the published spine (inherited from S401)
- The current Wave-1 S701/S702 implementation uses an aggregate scalar `mean(column_sum(B))` rather than `hp* · B`, which is a documented proxy (see S701/S702 DPRs); S402 itself is a faithful computation of B given S401's A

## Cross-references

- Upstream: S401 (A-matrix — the only direct input)
- Downstream: S701 (labor values, proxy), S702 (prices of production, proxy), S703 (value-price deviations, proxy) — all three currently substitute `mean(column_sum(B))` for the book's `hp* · B`
- Related external: any IO-based labor-value study (Wolff 1977a/b/1987; Sharpe 1982; Khanjian 1988/1989; Mohun 2005)

## Provenance trail

- **Original research**: `Technical/research/S402_research.json`, researcher `agent`, 2026-05-06; ported from `predecessor-build/research/T402_research.json` on 2026-05-14
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (cohort agent 4); sources read = research JSON + KB chunks 10/27 cited via research JSON + registry entry
- **Anu Framework stage**: Stage 3 INGESTION (cohort 1, failing chapters); ingestion gate IDs P31/P32
