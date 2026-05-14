# S607 — Net Social Wage — Extension Provenance Record

**Series**: S607 — Net Social Wage (NSW = B_w + G_w − T_w)
**Book period**: 1952–1989 (canonical, `data/final/S607.csv`)
**Extension target**: 1990–2024
**Status**: extension_methodology_documented (extended data available; splice not yet executed)

## Extension source

`data/source/book_tables/Table6_3_Extended.csv` (already in the source tree) covers 1952–2024 (73 years) — produced by re-running the same NIPA component decomposition through modern years using the post-1989 BEA NIPA tables. This is the ST2 team's extension, salvageable for the new build because:

1. The construction methodology is identical (NIPA tables 3.1, 3.2, 3.3 component decomposition under Tonak's productive/unproductive partition).
2. The book-period overlap (1952–1989) matches Table6_3_NetSocialWage.csv values exactly (verified for 1952 and 1989 endpoints).
3. No proxy series; all components come from the same BEA NIPA family the book originally used.

## Splice methodology

`splice_year`: 1989 (last book year)
`splice_method`: "direct" — the extended table IS the same construction continued. No re-indexing needed.
`depends_on`: NIPA tables (no other registry series).

This is one of the few cases where a splice produces no discontinuity because the methodology continues unchanged. Validator will verify the 1989 overlap value is identical between Table6_3_NetSocialWage.csv and Table6_3_Extended.csv.

## Acceptance criteria for activation

- [ ] L01_S607 extended to also load Table6_3_Extended.csv as `S607-B` (raw extension, 1990–2024)
- [ ] P02_S607 extended to compose S607-COMBINED = S607-A (1952–1989) + S607-B (1990–2024)
- [ ] V03_S607 extended with V06 transition-quality check: |S607-A[1989] - S607-B[1989]| < 0.01 (overlap consistency)
- [ ] V03_S607 extended with V07 overlap-correlation check across 1952–1989 between the two sources (should be perfect, ~1.0)
- [ ] Headline finding documented: 1989 was the LAST year of consistently negative NSW; the series turns positive in the early 1990s as transfer programs expanded faster than tax burden on workers

## Faithfulness considerations

100% faithful — same agency, same tables, same construction method. No proxy substitutions. No lazy growth-rate splice on a derived quantity (the extension is itself a re-application of the original formula, not a separate observation series).

---

*Activation is a Wave 2 follow-up task — the data is already present, just not yet spliced into the canonical S607 series.*
