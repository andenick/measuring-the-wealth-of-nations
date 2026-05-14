# S511 — Extension Provenance Record

**Series**: Productive Labor Share (Lp/L)
**Units**: share
**Book period**: 1948–1989 (canonical, in `data/final/S511.csv`)
**Extension target**: 1990–2024 (post-book)
**Status**: extension_methodology_documented (data fetch pending API keys)

## Splice methodology

- **Splice year**: 1989
- **Splice method**: `level`
- **Dependencies on other series**: (none)

## Extension data source(s)

- `S511-EXT` — BLS CES (period [1990, 2024], units share)
- `S511-COMBINED` —  (period [1948, 2024], units share)

## Activation criteria

Before the extension is fetched and spliced into `data/final/S511.csv`:

- [ ] `data/user-inputs/api_keys.env` provisioned (BEA, BLS, or FRED as required)
- [ ] L## loader extended to fetch the extension subsource and write it to `data/raw/`
- [ ] P## processor extended to perform the splice and emit `S###-COMBINED`
- [ ] V## validator extended with transition-quality checks (V06/V07 per the Anu Extension Standard): connection ratio in [0.95, 1.05], overlap correlation ≥ 0.95, no SIGN-flip across the splice point
- [ ] EPR updated with the actual API series IDs, agency URLs, and faithfulness rating (per Anu Extension Standard rubric)

## Faithfulness considerations

Per the Anu Extension Standard (no proxies, no lazy splices on derived quantities): the extension MUST use the agency/table the book originally drew from, or document any substitution explicitly. For S511, the canonical BEA/BLS/FRED endpoint is recorded in the registry under `subseries[S###-B].source`. Any divergence requires a Concept Match Justification in this EPR.
