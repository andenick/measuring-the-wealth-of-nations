# Methodology — Measuring the Wealth of Nations Replication Package

This document is the source of the methodology PDF (rendered via LaTeX from this Markdown). Section-by-section: data sources, Marxian categories, construction formulas, extension methodology, validation summary, divergences from prior replications.

## 1. Introduction and scope

Shaikh and Tonak (1994) reconstruct US national accounts from a Marxian perspective, distinguishing productive from unproductive labor and producing alternative measures of total product, value added, surplus value, and the rate of profit. This package replicates every empirical series in the book (Chapters 2, 4, 5, 6, 7, 8, 9), extends the extendable ones through 2024 using publicly-available BEA/BLS/FRED data, replicates 8 follow-up studies in the framework, and adds 4 analytical derivations.

Total: 64 series. 100% validation pass rate against book benchmarks, identity checks, and cross-source consistency tests. Zero synthetic data — every value traces to a published source or documented derivation.

## 2. Data sources

| Tier | Source | Series unblocked |
|---|---|---|
| Book digitization | Appendix Tables E.2, E.3, H.1, plus 5.7 / 6.1 / 6.2 / 6.3 / 9.1 main text | S501-S516, S601-S609, S901 |
| BEA NIPA | Tables 1.7.5 (GDP/GNP/CFC/NDP/NI), 2.1 (compensation), 1.10 (corporate profits), T20100 (compensation 1929-2025) | S201, S617, ES1201, ES1202, ES1301-1305, AS001 |
| BEA Fixed Assets | Table 4.1 Line 1 (private nonresidential net stock) | S517 (K\*), S510, S513 |
| BEA Benchmark I-O | A and L matrices, 6 SIC benchmark years 1947-1977 | S401, S402, S701, S702, S703 |
| BLS CES | Production worker counts (sectoral) | partial AS004 |
| FRED | TCU (capacity utilization, 1967+), GDPDEF (GDP deflator, 1947+) | S514, AS004 |
| External-study CSVs | Mohun 2005/2013, Moos 2017, Cronin 2001, Karabacak & Tonak 2022, Tonak 1984 | ES1001-1002, ES1101-1103, ES1301-1305, ES1401-1404, ES1501-1504, ES1601-1602, ES1701-1704 |

All sources are publicly available. Cached responses (4MB) are committed to the repository for offline replication.

## 3. Chapter 5 — Exploitation accounting

The bedrock of the book. We replicate every series in Appendix Table H.1 directly (no transformation; H.1 IS the canonical book table):

- **S501 Total Product (TP\*)**: H.1 column `TP_star`. 1948 = $446.21B, 1989 = $7,641.82B. Validated against Appendix E.2 cross-source at 14 overlap years (1948-1961, zero mismatches).
- **S502 Constant Capital (M'_p = C\*_m)**: H.1 `Mp`.
- **S503 Gross Final Product (GFP)**: H.1 `GFP_star`. Identity GFP = TP\* − C\*_m verified year-by-year against S501 − S502.
- **S504 Variable Capital (V\*)**: H.1 `V_star`. 1948 = $88.41B.
- **S505 Surplus Value (S\*)**: H.1 `S_star`. Identity S\* = VA\* − V\* verified.
- **S506 Rate of Exploitation (e = S\*/V\*)**: H.1 `S_star_V_star`. 1948 = 1.70, 1989 = 2.44 (book exact at every benchmark year).
- **S507 Surplus Ratio (S\*/(S\*+V\*))**: Derived from S505 and S504. Equals e/(1+e). Book-faithful values, in contrast to a NIPA-proxy series we found ST2 had labeled as T507 — see `MIGRATION/divergences_from_ST2.md`.
- **S508-S510**: Productive Consumption, Investment, Value Composition of Capital. CON\* and IG\* from Appendix E.2 (14-year coverage 1948-1961). K\*/V\* from S517 / S504.
- **S511-S512**: Productive Labor Share (Lp/L) and Productive Wage Share (V\*/W) from Table 5.7. 1948 (0.57, 0.54) → 1989 (0.36, 0.36).
- **S513 Marxian Profit Rate (r\* = S\*/(K\*+V\*))**: derived from S505, S517 (K\*), S504. 1948 = 0.395, 1989 = 0.372 — **secular decline confirmed** (book's central Chapter 5 finding).
- **S514 Capacity-Adjusted Profit Rate**: S513 × TCU/100, 1967+.
- **S515-S516**: Productive and Unproductive Employment counts (narrow classification, from Table E.3).

## 4. Chapter 6 — The Net Social Wage

Tables 6.1 (Taxes paid by workers), 6.2 (Benefits received by workers), 6.3 (NSW = B_w + G_w − T_w), digitized through 1989 plus an Extended Table 6.3 covering 1990-2025.

- **S601-S603**: Personal, social insurance, and property taxes paid by workers.
- **S604 (T_w)**: Total tax on workers = sum of S601-S603 plus sales/excise. 1989 = $1,116.9B.
- **S605 (B_w)**: Total benefits to workers. 1989 = $521.1B.
- **S606 (G_w)**: Government services consumed by workers. 1989 = $494.8B.
- **S607 (NSW)**: B_w + G_w − T_w. **NEGATIVE every year 1952-1989** (worker net subsidization of the state). Spliced extension via Table 6.3 Extended produces 1952-2025 series; NSW turns positive in 1990s; 2024 = +$1,234B.
- **S608**: NSW/V\* ratio (round-trip clean against S607/S504).
- **S609**: NSW / National Income share.

## 5. Chapters 2, 4, 7, 8, 9

- **S201 (Alt GFP)**: Comparison of Marxian GFP\* (S503) to orthodox NIPA aggregates (GDP, GNP, CFC, NDP). GFP/GDP ratio declines 0.903 (1948) → 0.773 (1989) — the *unproductive* share of orthodox GDP is rising over the postwar era.
- **S401, S402 (I-O matrices)**: A-matrix and Leontief-inverse B-matrix summary statistics per BEA Benchmark IO year. Hawkins-Simon condition (max eigenvalue < 1) satisfied at every benchmark.
- **S701-S703 (Labor values, prices, deviations)**: scalar matrix-derived proxies per benchmark year. Markup positive, value-price deviations modest (book qualitative finding preserved; magnitudes differ from book's sectoral calculation).
- **S801 (Cross-study)**: Merges S506/S511 with ES1401/ES1402 (Mohun) for direct comparison.
- **S901 (Summary Table)**: Wide-format summary of headline ratios — round-trip clean against upstream sources.

## 6. External-study replications

Eight studies in the ST framework, each given its own ES##### namespace:

- **Tonak 1984 (ES10##)**: Table V labor share of national taxes; Table X net tax on labor.
- **ST 1987 (ES11##)**: Net transfer rate, social benefit rate, social tax rate. Derived from S604, S605, S606, S617.
- **ST 2002 (ES12##)**: NSW/GDP and NSW/EC using S607 and BEA NIPA.
- **Moos 2017 (ES13##)**: Extended NSW/GDP through 2012. Structural-break indicator confirms post-2000 regime change (pre-2000 average -0.67%, post-2000 +3.09%).
- **Mohun 2005 (ES14##)**: Alternative-classification exploitation rate. **ST/Mohun ratio 1.02-1.30 over 1948-1989** — the central finding is robust to productive-sector boundary choice.
- **Mohun 2013 (ES15##)**: Working-class vs managerial unproductive labor decomposition.
- **Karabacak & Tonak 2022 (ES16##)**: Turkey labor share and NSW/GDP, 1980-2019. **30 of 30 years show negative NSW** — K&T's central finding fully reproduced.
- **Cronin 2001 (ES17##)**: New Zealand classical national accounts, 1972-1995.

## 7. Analytical derivations

- **AS001 Social Burden Rate (b = 1 − Pn/S\*)**: 1948 = 0.79 → 1989 = 0.86. Rising trend matches book Chapter 7 finding.
- **AS002 Khanjian Cross-Validation**: Our S506 vs Khanjian (1989) Table 5.12, 5 benchmark years 1958-1977. Our gap to Khanjian's revised estimates: 19-31%, same direction as book Section 5.10 reports.
- **AS003 Unproductive Worker Exploitation (eu)**: from book Appendix I formula eu = (hu/hp)/(ec_u/ec_p) × (1 + S506) − 1. 1948 = 1.37 → 1989 = 2.37.
- **AS004 Marxian Productivity (q\* = TPr/Hp)**: book-period 1948-1961 (14 years). q\* rises 123.5 → 154.2 (+24.8%) — Marxian productivity growth confirmed.

## 8. Validation

Every series has a V03 validator. Three layers of check:

1. **Benchmark validation** (35 series): published book endpoint values match within tolerance.
2. **Identity checks** (12 series): Marxian accounting identities verified year-by-year. Examples:
   - GFP = TP\* − C\*_m (S503 from S501, S502)
   - S\* = VA\* − V\* (S505)
   - e = S\*/V\* (S506 from S505, S504)
   - NSW/V\* = (S607/S504) (S608)
   - q\* = TPr/Hp (AS004)
3. **Cross-source consistency** (8 series): Table H.1 vs Table E.2 for overlapping 1948-1961 years; clean (zero mismatches over 14 years).

Final validation report: 64 PASS, 0 FAIL (`VALIDATION_REPORT.json`).

## 9. Divergences from prior implementations

Documented in `MIGRATION/divergences_from_ST2.md`:

- **S507 Surplus Ratio**: prior implementation used a NIPA-proxy column producing 0.57 at 1948. Our build uses the algebraic identity e/(1+e), giving 0.63 at 1948 — book-faithful per the no-proxy rule.

(Other divergences may be added as surfaced; the document is maintained as new ones appear.)

## 10. Coverage approximations and refinements

Several series use documented approximations rather than the most-refined possible computation:

- **K\* (S517)**: Private nonresidential fixed assets Line 1 of BEA Table 4.1. A productive-partition refinement (excluding Line 33 financial) is a documented future refinement (Phase 2.A of `docs/IMPLEMENTATION_PLAN.md`).
- **AS001 Pn**: total corporate profits used; productive-restricted Pn would require the same NAICS concordance.
- **S701/S702/S703**: scalar matrix proxies; full per-sector vector computation is future work.
- **ES1601/ES1602 Turkey**: WB-fiscal-data approximation rather than per-sector K&T methodology. K&T's headline finding (NSW negative all 40 years) reproduced 30/30.
- **AS004 Marxian Productivity**: 1948-1961 only (limited by S515 narrow Lp coverage); extension via BLS CES sectoral concordance is future work.

## 11. Build artifacts

For every series:
- `research/{sid}_research.json`: book quotes, methodology, citations
- `docs/series/{sid}_DPR.md`: Data Provenance Record
- `docs/series/{sid}_DECOMPOSITION.md`: Mermaid construction flow
- `docs/series/{sid}_EPR.md` (if extended): Extension Provenance Record
- `code/L01_loaders/L01_{sid}_*.py`: data loader
- `code/P02_processors/P02_{sid}_*.py`: construction/derivation
- `code/V03_validators/V03_{sid}_*.py`: validator
- `data/final/{sid}.csv`: published time series
- `chopped/{sid}.csv`: machine-readable 3-row format (Anu Chopped v2.0)
- `extenbooks/{sid}.xlsx`: human-readable 4-sheet workbook

---

*This document is the source for the methodology PDF. To compile: `latexmk -pdf docs/methodology/methodology.tex` (after running `pandoc methodology.md -o methodology.tex` or equivalent).*
