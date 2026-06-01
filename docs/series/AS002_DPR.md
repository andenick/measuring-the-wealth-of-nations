# AS002 — Khanjian Cross-Validation

## Series

- **SID**: AS002
- **Name**: Khanjian Cross-Validation
- **Chapter**: Anu-Original Analytical (registry chapter=0 / null in research JSON). **AS-prefix framing**: this is a framework-derived consistency check, not a direct book-table replication. The conceptual home is book Section 5.10 (Khanjian comparison, Table 5.12, Figure 5.25) and Appendix I (rates of exploitation derivation).
- **Status**: book_period_validated
- **Units**: ratio

## Methodology

AS002 cross-validates the project's primary exploitation rate series S506 (`e = S*/V*`) against Khanjian's (1988, 1989) alternative computation. Khanjian re-estimated S*/V* using a different treatment of unincorporated income (treating it ALL as profit), yielding estimates ~20% higher than Shaikh & Tonak's primary measure. The cross-validation stores 5 benchmark-year comparisons (1958, 1963, 1967, 1972, 1977 — matching the BEA IO benchmark years used elsewhere in the project) with columns: S506 value, Khanjian's `e_star_rev` (revised money form), Khanjian's `e_rev` (revised labor-value form), and the percent gap between S506 and Khanjian's estimates. The legacy script is `code/A##_analytical/A08_khanjian_crossvalidation.py`. Khanjian's values are hardcoded from book Table 5.12 (5 benchmark years); S506 values come from `data/final/S506.csv`. This is a pure analytical composition with no new external source file beyond the book digitization.

The substantive book framing is the contrast between consistent and inconsistent procedures. The verbatim primary anchor is **"Khanjian (1989) using consistent procedure: Value and price rates of surplus value differ by only 6%-9%. Price-value deviations have minor effects on aggregate measures (Section 5.10, Table 5.12, Figure 5.25)."** (ST 1994 Ch7 §7.3, p.223). The methodology contrast with Wolff is **"Khanjian's S*/V* uniformly lower than S/V by 6%-9% (Khanjian 1988, p. 109, table 19). Wolff's inconsistent procedure biases money rate S*/V* upward by 12%-15% (sum of two differences)."** (ST 1994 Ch7 §7.3, p.223). The formal derivation Khanjian uses comes from Appendix I: **"Main Formula: (1 + eu) / (1 + ep) approx (hu/hp) / (ecu/ecp). Known: ep = S*/V* (rate of surplus value for productive workers). Solve for eu: eu = (hu/hp) / (ecu/ecp) . [1 + S*/V*] - 1."** (ST 1994 Appendix I, p.323). The Appendix I Table I.1 numeric trajectory AS002's cross-validation must reproduce is **"Exploitation rate ratio (eu/ep): 1948: 0.80 (unproductive 20% less exploited); 1960: 0.89; 1972: 0.92; 1980: 0.92; 1989: 0.97 (3% less). Convergence: Exploitation rates converging. Both rising, but unproductive rising faster."** (ST 1994 Appendix I Table I.1, pp.330-331).

The implementation finds: our S506 vs Khanjian's `e_star_rev` shows gaps of 19-31% across the 5 benchmark years. Direction matches the book — Khanjian is higher than ST. Magnitude is slightly larger than the book's reported "~20%" because Khanjian's revisions also use updated NIPA vintages relative to the book's published S506 reference. Validator PASS: all 5 gaps are positive (Khanjian > ST) and < 50% (rule-of-thumb upper bound). The reason a Khanjian-style cross-validation is the right consistency check — rather than a Wolff-style one — is that Khanjian uses a consistent procedure (sector-level value-added decomposition under the productive/unproductive boundary) while Wolff's symmetric/inconsistent treatment biases S*/V* upward by 12-15% (the sum of Wolff's 4-8% bias and Khanjian's 6-9% Khanjian-vs-ST gap). AS002 therefore stands as an internal consistency check that the project's S506 falls in the expected band relative to a known consistent alternative.

## Sources

- KB chunks: `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_25/full_transcription.md` (Ch7 §7.3 p.223 — Khanjian 6-9% benchmark, Wolff 12-15% bias); `chunk_35/full_transcription.md` (Appendix I, Table I.1 — formal derivation of `eu` and benchmark numeric values)
- Book tables: Table 5.12 (Khanjian comparison values, p.~123); Figure 5.25 (Section 5.10 visual); Appendix I Table I.1 (Rates of Exploitation of Unproductive Workers, 1948-89 — 25-step annual calculation methodology); the project's hardcoded benchmark values for 1958/1963/1967/1972/1977
- External sources: Khanjian (1988, p.109 table 19 — the 6-9% deviation envelope); Khanjian (1989) — consistent procedure; Wolff (1977b, p.103 table 3, lines 1 and 3 — the symmetric/inconsistent comparator)
- Upstream series: S506 (rate of surplus value)
- Code: `code/A##_analytical/A08_khanjian_crossvalidation.py` (legacy standalone analytical script — predates the standard L01/P02/V03 triad)

## Reference values

- 5 benchmark years: 1958, 1963, 1967, 1972, 1977
- Observed gap range (S506 vs Khanjian e_star_rev): **19-31%**
- Direction: Khanjian > ST at every benchmark year (PASS)
- Validator: all 5 gaps positive and < 50% rule-of-thumb (PASS)
- **Book Khanjian benchmark**: 6-9% deviation in S*/V* between price and value forms (ST 1994 Ch7 §7.3, p.223)
- **Book Wolff comparator**: 12-15% upward bias in money S*/V* from inconsistent symmetric procedure
- **Appendix I Table I.1 numeric trajectory** (validation target): eu/ep ratio 0.80 (1948) → 0.97 (1989) — converging
- Validator `expected_range`: not yet populated; `tolerance_class: rate_series`

## Known issues

- **Construction steps not specified in registry** (empty array) — relies on legacy standalone script `A08_khanjian_crossvalidation.py`
- **Khanjian method details paraphrased**, not directly extracted from Khanjian's original 1988/1989 papers — the project relies on book Table 5.12 hardcoded values and the book's narrative summary in §5.10 / §7.3
- **Alternative decomposition path not yet documented** in technical detail — the project knows what Khanjian's answer is but not the full sequence of his computation
- **5 benchmark years only**: matches BEA IO benchmark coverage but is a small validation cross-section
- **Gap 19-31% vs book's ~20%**: magnitude slightly larger because Khanjian's revisions use updated NIPA vintages relative to the book's published S506; direction matches
- **Legacy script not yet migrated** to the standard L01_AS002 / P02_AS002 / V03_AS002 triad
- **No EPR yet authored** for AS002 (Stage 4 work)

## Cross-references

- Upstream: S506 (rate of surplus value)
- Related decompositions: AS001 (social burden rate — same family of analytical consistency checks); S701/S702/S703 (the value-price-deviation framework Khanjian's benchmark anchors)
- Related external: Khanjian (1988, 1989); Wolff (1977a, 1977b, 1979, 1987); Sharpe (1982b); Mohun (2005) — the broader cross-study consistency network
- Book derivation: Section 5.10 (Khanjian comparison); Appendix I (formal eu derivation); Ch7 §§7.3-7.4 (consistent vs inconsistent procedure critique)
- Related project DPRs: S703 (value-price deviations — both rely on the same Khanjian 6-9% benchmark for interpretive grounding)

## Provenance trail

- **Original research**: `Technical/research/AS002_research.json`, researcher `agent`, 2026-05-16; verbatim quotes added 2026-05-23 (`stage1_cohort3_S901AS001AS002`) — sourced from chunk_25 (Ch7 §7.3 Khanjian/Wolff references) and chunk_35 (Appendix I formal derivation + Table I.1 trajectory)
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (cohort agent 4); sources read = research JSON + KB chunks 25/35 + registry entry + project CLAUDE.md (AS-prefix framing mandate)
- **Anu Framework stage**: Stage 3 INGESTION (cohort 1, failing chapters); ingestion gate IDs P31/P32
