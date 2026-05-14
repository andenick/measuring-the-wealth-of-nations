# S501 — Extension Provenance Record

**Series**: Total Product (TP*)
**Units**: billions_usd
**Book period**: 1948–1989 (canonical, in `data/final/S501.csv`)
**Extension target**: 1990–2024 (post-book)
**Status**: extension_methodology_documented (data fetch pending API keys)

## Splice methodology

- **Splice year**: 1997
- **Splice method**: `growth_rate`
- **Dependencies on other series**: (none)

**Growth-rate splice**: the extension subseries (`S###-B` or `-EXT`) is rebased so its value at the splice year matches the book series' implied splice-year value; subsequent years carry forward by the extension source's year-on-year growth. This is the appropriate method when both eras directly observe the same construct under different industrial classifications (e.g., SIC vs NAICS), per the Anu Extension Standard.

## Extension data source(s)

- `S501-COMBINED` —  (period [1948, 2024], units billions_dollars)

## Activation criteria

Before the extension is fetched and spliced into `data/final/S501.csv`:

- [ ] `data/user-inputs/api_keys.env` provisioned (BEA, BLS, or FRED as required)
- [ ] L## loader extended to fetch the extension subsource and write it to `data/raw/`
- [ ] P## processor extended to perform the splice and emit `S###-COMBINED`
- [ ] V## validator extended with transition-quality checks (V06/V07 per the Anu Extension Standard): connection ratio in [0.95, 1.05], overlap correlation ≥ 0.95, no SIGN-flip across the splice point
- [ ] EPR updated with the actual API series IDs, agency URLs, and faithfulness rating (per Anu Extension Standard rubric)

## Faithfulness considerations

Per the Anu Extension Standard (no proxies, no lazy splices on derived quantities): the extension MUST use the agency/table the book originally drew from, or document any substitution explicitly. For S501, the canonical BEA/BLS/FRED endpoint is recorded in the registry under `subseries[S###-B].source`. Any divergence requires a Concept Match Justification in this EPR.
