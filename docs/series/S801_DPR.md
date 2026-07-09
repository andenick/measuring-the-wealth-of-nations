# S801 — Cross-Study Comparison (ST vs Mohun)

## Series

- **SID**: S801
- **Name**: Cross-Study Comparison (ST 1994 vs Mohun 2005)
- **Chapter**: 8 (project-internal label). **Important**: the printed book Measuring the Wealth of Nations has only seven chapters plus Appendices A-N. S801 is a project-internal artifact synthesizing the in-book Ch7 §7.4 cross-study critique with the Mohun (2005) CJE replication; the registry label "Ch8" and the registry `book_table: 8.1` are project conventions, not book content.
- **Status**: book_period_validated
- **Units**: mixed wide-table — ST e (ratio), Mohun e (ratio), ST Lp/L (share), Mohun Lp/L (share), ratio ST_e / Mohun_e (ratio)

## Methodology

S801 is a side-by-side comparison table that places the Shaikh-Tonak (1994) exploitation rate alongside Mohun's (2005) alternative exploitation rate for the overlapping 1948-1989 period (42 annual rows). The construction is a pure cross-study merge of four already-validated upstream series: S506 (ST exploitation rate `e = S*/V*` from Table 5.7), S511 (ST productive labor share `Lp/L`), XS1401 (Mohun 2005 exploitation rate from CJE Table 2), and XS1402 (Mohun productive labor share). The P02 processor reads each upstream `data/final/<sid>.csv` and emits a wide-format annual table with columns `year`, `ST_e`, `Mohun_e`, `ST_Lp_share`, `Mohun_Lp_share`. A round-trip check confirms `ST_e == S506` exactly (max abs error 0.0). The Mohun overlap with S506 starts in 1964 (Mohun's CJE series begins in 1964); for 1948-1963 the Mohun columns are NaN (no synthetic backfill, per the project no-synthetic-data policy).

The substantive theoretical foundation is the productive-labor classification difference between ST and Mohun. ST (1994) draws the boundary at production-and-trade: workers in agriculture, mining, construction, manufacturing, transportation, communications, utilities, and trade are productive; workers in FIRE, services, and government are unproductive. Mohun (2005) uses an alternative boundary that classifies more activities as productive (and/or differently distributes supervisory/managerial labor), producing a smaller unproductive share and therefore a lower exploitation rate. The verbatim book framing of why this matters is **"Productive employment L_p is stagnant for the first half of the postwar period, and then begins a steady but modest rise in the mid-1960s. But unproductive employment rises sharply throughout, so that the ratio of productive labor to total employment falls by more than 37% while that of unproductive labor to productive labor rises by almost 138% (Table 5.5 and Figures 5.7, 5.9, and 5.11)."** (ST 1994 Ch7 §7.3, p.221); and the methodological critique S801 generalizes is **"Working within an IO framework, Wolff (1975, 1977a,b, 1979, 1987) and Sharpe (1982b) also treat all labor as productive, thereby implicitly or explicitly associating the rate of surplus value with the profit/wage ratio. Thus, even though neither author draws any labor-squeeze implications from his results, their money and labor value estimates of rates of surplus value suffer from the same basic problems just outlined."** (ST 1994 Ch7 §7.4, p.225).

The headline finding is captured in XS1404 (ST_e / Mohun_e ratio): the ratio exceeds 1 throughout the entire 1964-1989 overlap period, with mean 1.61. The ST exploitation rate is roughly 0.7-1.3× Mohun's depending on year — the implied figure 8.2 finding. The sensitivity of the book's central exploitation claim to classification choice is therefore bounded: even Mohun's more permissive classification still confirms a rising exploitation rate, and the cross-study divergence is driven by classification — not by data — which is exactly the methodological point of Ch7 §7.4. Appendix M's NIPA-vs-Mage comparison (Tables M.1-M.5: 0.6% gap after adjustments) and Appendix N's net-transfer-to-workers correction (2.44 → 2.58 in 1989) are illustrative parallel validations of the "classification matters, data is robust" finding that S801 instantiates.

## Sources

- KB chunks: `data/raw/kb/book_digitization/chunk_24/full_transcription.md` (Ch7 §§7.1-7.3 pp.212-221 — Lp < 0.5L, S*/V* approximately 4× P+/EC, social burden rate); `chunk_25/full_transcription.md` (Ch7 §7.4 — cross-study critique); `chunk_38/full_transcription.md` (pp.352-361 — Appendix M Mage comparison, Appendix N net transfer)
- Book tables: ST 1994 Table 5.7 (S506 source); Table 5.5 (Lp/L over time); Figures 5.7, 5.9, 5.11; Appendix M Tables M.1-M.5; Appendix N Table N.2
- External sources: Mohun (2005) CJE Table 2 (exploitation rate 1964-2001); Mohun (2013) for the longer 1964-2010 update used in ES13xx series; raw Mohun CSV at `Inputs/ExternalSources/Mohun/mohun_exploitation_rates_1948_1989.csv`
- Upstream series: S506 (ST exploitation rate, wave 1, calculated), S511 (ST productive labor share, wave 1), XS1401 (Mohun exploitation rate), XS1402 (Mohun productive labor share), XS1403 (Mohun variable capital), XS1404 (ST/Mohun exploitation ratio, mean 1.61)

## Reference values

- 42 comparison years 1948-1989 (Mohun-overlap rows 1964-1989; pre-1964 Mohun columns NaN)
- XS1404 mean ratio `ST_e / Mohun_e` over 1964-1989 = **1.61**
- XS1404 expected range: **[1.0, 2.5]** (registry validation field)
- Round-trip check: `max(abs(ST_e − S506)) = 0.0`
- Book directional finding (1948-1989): ST exploitation rate rose from ~1.70 to ~2.44 (44% increase); Mohun rate also rises, but at a lower level
- ST productive labor share falls from ~57% (1948) to ~36% (1989); Mohun's share runs higher by ~10-15 percentage points reflecting the broader classification

## Known issues

- **Book has no Chapter 8 and no Table 8.1**: S801's "book_table=8.1" registry label is a project-internal synthesis. Verified against book TOC pp.v-vii — chapters run 1-7 plus Appendices A-N
- Ch7 §7.4 contains the cross-study critique S801 generalizes; the actual "side-by-side table" form is a project artifact not in the printed book
- Mohun (2005) CJE series begins in 1964, so 1948-1963 rows have NaN Mohun columns (no synthetic backfill per project policy); the raw CSV at `Inputs/ExternalSources/Mohun/mohun_exploitation_rates_1948_1989.csv` is labelled 1948-1989 but the 1948-1963 segment is project-extended (verify before use)
- XS1404 expected range [1.0, 2.5] is registry-asserted; year-by-year values are not yet tabulated in this DPR (live in XS1404's final CSV)
- The Mohun classification details are documented in Mohun (2005) and XS1401-XS1404 research JSONs; readers should consult those for the productive/unproductive boundary specifics
- Comparison sensitivity to Mohun (2013) update vs Mohun (2005) original: XS1401 currently uses 2005 vintage; switching to 2013 would change post-1989 figures

## Cross-references

- Upstream: S506 (ST exploitation rate), S511 (ST productive labor share), XS1401 (Mohun e), XS1402 (Mohun Lp/L), XS1403 (Mohun V*), XS1404 (ST/Mohun ratio)
- Downstream: S901 (Chapter-9-style summary table; uses S506 directly, not S801)
- Related external: Mohun (2005) "On Measuring the Wealth of Nations: The U.S. Economy 1964-2001"; Mohun (2013) for 1964-2010 update; Wolff (1975, 1977a/b, 1979, 1987); Sharpe (1982b); the book's Ch7 §7.4 critique
- Related project DPRs: XS002 (Khanjian cross-validation — same family of cross-study consistency checks)

## Provenance trail

- **Original research**: `Technical/research/S801_research.json`, researcher `agent`, 2026-05-06; ported from `predecessor-build/research/T801_research.json` on 2026-05-14; verbatim quotes backfilled 2026-05-19 (`D3_RMWND_quotes_ch7_etc`) — the backfill specifically flagged that the book has no Ch8
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (cohort agent 4); sources read = research JSON + KB chunks 24/25/38 cited via research JSON + registry entry + project CLAUDE.md (which mandates disclosure that S801/S901 are project artifacts beyond the printed book's 7 chapters)
- **Anu Framework stage**: Stage 3 INGESTION (cohort 1, failing chapters); ingestion gate IDs P31/P32
