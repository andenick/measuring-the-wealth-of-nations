# S401 — A-Matrix Summary (Technical Coefficients)

## Series

- **SID**: S401
- **Name**: A-Matrix (Direct Requirements) — Summary
- **Chapter**: 4 (IO framework and labor-value foundations); book Table 4.1
- **Status**: book_period_validated
- **Status note**: (extension covers 1997-2012 NAICS benchmark attempts; mismatched sector schemes mean SIC benchmarks are the published S401 spine)
- **Units**: matrix-summary scalars (n_sectors, sparsity, max_eigenvalue, condition_number, leontief_max_dev) per benchmark year

## Methodology

S401 tabulates summary diagnostics of the Shaikh-Tonak direct-requirements (A) matrix for each BEA benchmark input-output year. For each sector j the technical coefficient is `a_ij = z_ij / x_j`, where `z_ij` is the dollar flow from industry i to industry j as an intermediate input and `x_j` is total gross output of industry j (in producer prices). The book's framework places this construction in Chapter 4 §4.1 (pp.78-83): the A-matrix is the empirical input-output coefficient matrix `app* = (a*_ij)` constructed in money flows at producer prices, with the labor-value vector subsequently solved as `lambda* = hp* + lambda* · app*` ⇒ `lambda* = hp* · (I − app*)^{-1}`. The verbatim foundation is **"For the production sector j, let lambda_j = labor value per unit output; hp_j = hours of productive labor per unit output; app_ij = quantity of the ith production input used per unit output. Then unit labor values must satisfy the relation lambda_j = hp_j + sum_i lambda_i * app_ij … lambda = hp * (I - app)^{-1}."** (ST 1994 Ch4 §4.1, pp.80-81).

The construction reproduces S&T's Appendix A multi-stage aggregation pipeline: Juillard's unpublished tables begin at 105×116 for 1963/1967/1972/1977 and 90×99 for 1947/1958, and are aggregated through a deterministic sequence (105×116 → 87×98 → 87×94 → 82×88) before the final 82×88 transaction matrix Z and the output vector x are used to compute A. Force-account construction (the imputation of government-employed construction wages as a construction-industry output) is reversed using the FAC72 scaling formula for non-1972 years. Fictitious real-estate imputed flows are removed. Eating-and-drinking-places flows are separately estimated for 1947/1958/1963/1967 using an iterative method documented in §A.3.5. The result is a comparable 85×85 SIC-sector A-matrix at each of six benchmark years: 1947, 1958, 1963, 1967, 1972, 1977. The verbatim aggregation specification is **"Step 1: Create consistent 82×88 tables from BEA published tables — adjust for classification of industries, adjust treatment of secondary products, ensure imports comparable across years. Step 2: Aggregate 82×88 tables into 8×11 summary tables following the structure of Figure 5.1. Details in Appendix A."** (ST 1994 Ch5, p.91).

The summary diagnostics emitted per benchmark year are: `n_sectors` (matrix dimension after aggregation), `sparsity` (fraction of zero entries), `max_eigenvalue` (largest real eigenvalue of A — the Hawkins-Simon productive-economy diagnostic), `condition_number` (numerical stability indicator), and `leontief_max_dev` (a check on `(I - A)(I - A)^{-1} = I`). The Hawkins-Simon condition `max_eigenvalue < 1` is satisfied at every benchmark year (observed range 0.495 to 0.982), confirming the constructed economy is productive. The 1947 matrix is poorly conditioned (max_eig 0.982), reflecting documented data-quality issues in BEA's first benchmark; matrices from 1958 onward are well-conditioned (max_eig 0.45-0.85). The series is a benchmark cross-section; per VAR-006 it skips the standard chopped-CSV / Extenbook annual time-series pipeline.

## Sources

- KB chunks: `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_10/full_transcription.md` (Ch4 §4.1, pp.78-83 — IO framework, labor-value equations, A* / B* derivation); `chunk_27/full_transcription.md` (Appendix A §§A.3.1-A.3.5, pp.243-260 — Juillard tables, aggregation pipeline, FAC reversal, real-estate adjustment)
- Book tables: ST 1994 Table 4.1 (A-Matrix) at the 85×85 level; Figure 5.1 (8×11 summary structure)
- External sources: BEA Benchmark Input-Output Accounts (1947, 1958, 1963, 1967, 1972, 1977); Juillard (1988) dissertation tables; BEA (1980) for force-account construction definition
- Local files: `data/source/io_matrices/<year>_A_matrix.csv` (6 files copied from BEA Benchmark IO via predecessor-build IO_Matrices); printed-book digitization at `data/source/book_tables/ch04/Table4_1_AMatrix.csv`
- Code: `code/utils/io_matrix.py` (loaders + summary diagnostics)

## Reference values

- Six benchmark years: 1947, 1958, 1963, 1967, 1972, 1977
- `max_eigenvalue` range over benchmarks: `[0.495, 0.982]` (Hawkins-Simon `< 1` satisfied at every year)
- 1947 is the most poorly conditioned matrix (`max_eig = 0.98`, documented BEA data-quality issue)
- 1958-1977 well-conditioned (`max_eig` in `[0.45, 0.85]`)
- Validator `expected_range` for summary scalars: `[0.0, 1.0]` (eigenvalue-style ratios)
- No annual interpolation (book is explicit that BEA IO benchmarks exist only at these six years during the SIC era; verbatim: **"U.S. IO tables are available only for select benchmark years: 1947, 1958, 1963, 1967, 1972, 1977."** — ST 1994 Ch5, p.89)

## Known issues

- Eating-and-drinking-places iterative estimation for 1947-1967 introduces approximation error (S&T acknowledge oil-input distortion in §A.3.5)
- Force-account construction scaling for non-1972 years uses FAC72 ratio formula because actual BEA imputations are not obtainable for earlier benchmarks
- Ground-rent proportion `g = 0.25` is a constant approximation for IO benchmark tables; annual data uses more detailed derivation (g ≈ 0.28-0.30)
- No NAICS extension in the published spine: the 1997-2012 benchmark attempts produce shape-mismatched matrices because BEA changed sector definitions; the registry status `validated_book_and_extension` is interpreted as "validated where the schema can be made comparable" and the published series remains SIC-only
- 1963 benchmark exhibits the same underlying data gap that affects S701/S702 (downstream consumers); see WARN-03 in those DPRs

## Cross-references

- Downstream dependencies: S402 (Leontief inverse B = (I-A)^{-1}); S701 (labor values, proxy); S702 (prices of production, proxy)
- Upstream raw data: BEA Benchmark IO tables; Juillard (1988) aggregation procedures
- Related series: none (S401 is a foundational IO infrastructure series, not a transformation of another final series)

## Provenance trail

- **Original research**: `Technical/research/S401_research.json`, researcher `agent`, 2026-05-06; ported from `predecessor-build/research/T401_research.json` on 2026-05-14
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (cohort agent 4); sources read = research JSON + KB chunks 10/27 cited via research JSON + registry entry
- **Anu Framework stage**: Stage 3 INGESTION (cohort 1, failing chapters); ingestion gate IDs P31/P32
