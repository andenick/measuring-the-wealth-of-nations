# S901 — Summary Indicators (Chapter-9-Style Summary Table)

## Series

- **SID**: S901
- **Name**: Summary Indicators (project-internal Chapter-9-style summary table)
- **Chapter**: 9 (project-internal label). **Important**: the printed book has only seven chapters plus Appendices A-N. There is no Chapter 9 and no Table 9.1 in the book. The in-book analog is Ch7 §§7.1-7.5 ("Summary and conclusions"). S901 is a project-internal aggregation that mirrors what a printed summary table would have contained.
- **Status**: book_period_validated
- **Status note**: (1948-1989; extension blocked until upstream extensions complete)
- **Units**: mixed long-format (ratio / rate / share by column)

## Methodology

S901 is a purely derived composite table assembling key Marxian indicators from Ch5 (production accounts) and Ch6 (distribution accounts) into a single long-format summary. No independent NIPA inputs are required. The P02 processor reads each upstream `data/final/<sid>.csv`, projects the `<sid>-A` (book-period) subseries, and emits one long-format row per `(year, indicator)` pair. The six indicators are: `S506` (exploitation rate `e = S*/V*`), `S511` (productive labor share `Lp/L`), `S512` (productive wage share `V*/W`), `S513` (Marxian profit rate `r* = S*/(C*+V*)` — pending K* sourcing), `S514` (capacity-adjusted profit rate `r*_adj = r* · TCU` — pending K* and TCU), and `S608` (NSW/V* ratio from Wave 2). Pending indicators are explicit NaN, not synthesized values.

The substantive content S901 is meant to display is the book's headline empirical contrast between Marxian and orthodox magnitudes. The verbatim summary anchor is **"Marxian total product TP* is roughly 82% of the IO measure of gross product GP, but about 1.5 times larger than the conventional measure of GNP. Marxian gross final product GFP*, on the other hand, is about 15% smaller than GNP (Table 5.4). Surplus value S* is almost double the most inclusive measure of profit-type income P+ (defined as NNP minus employee compensation), while productive labor L_p is less than one-half of all employment L. As a result, the rate of surplus value S*/V* is typically almost four times as large as the ratio of profit-type income to employee compensation P+/EC, while the Marxian measure of productivity q* (defined as real total product per productive labor hour) is about 3 times as large as the conventional measure (defined as real GDP per labor hour) (Section 5.12, Table 5.14)."** (ST 1994 Ch7 §7.3, p.221). The two-phase profit-rate narrative the table is meant to surface is **"From 1948 to 1980, the rate of surplus value rises modestly by roughly 22%, while the adjusted value composition rises by over 77% (and the adjusted materialized composition C*K/(V*+S*) rises by over 56%). The rising value composition overwhelms the rising rate of surplus value, so that the adjusted Marxian rate of profit falls by almost a third over this period. This is striking empirical support for Marx's theory of the falling rate of profit."** (ST 1994 Ch7 §7.1, p.214); and **"The second period, from 1980 to 1989, spans the Reagan-Bush era … The rise in the rate of surplus value accelerates in this period, more than doubling its trend rate. Moreover, the growth in the value and materialized compositions decelerate in this period … The overall effect is to modestly reverse the fall in the general rate of profit, recovering about 8% of its initial value."** (ST 1994 Ch7 §7.1, p.214).

V03 validation is purely a round-trip: for every populated `(year, indicator)` cell, the value must equal the corresponding cell in the upstream final CSV at the matching year with `abs_err < 1e-9`. Current PASS rate: 164/164 populated pairs across 4 columns × 41 years. The remaining 88 cells (S513 + S514 columns × all years) are NaN by design — they activate when K* (productive fixed-capital stock) and TCU (capacity utilization) are sourced. The project's no-synthetic-data rule is the explicit reason these cells remain NaN rather than carrying placeholder values. S901's reason-for-existing is captured in the book's own self-description of its purpose: **"The whole purpose of this book has been to show that the middle road is truly different, both theoretically and empirically."** (ST 1994 Ch7 §7.2, p.220).

## Sources

- KB chunks: `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_24/full_transcription.md` (Ch7 §7.1 — Phase-1 1948-1980 narrative, Figure 7.1 social-burden rate, Figure 7.2 NIPA-vs-Marxian rate); `chunk_25/full_transcription.md` (Ch7 §7.3 — Lp < 0.5L, S*/V* approximately 4× P+/EC, value composition rising 90%); `Knowledge_Base/tables/page_140_marxian_orthodox_comparison.csv` (Table 5.14 comparison ratios — TP*/GP=82%, TP*/GNP=147%, S*/P=224%, S*/V*=210% of orthodox equivalents); `Knowledge_Base/SUMMARY_KEY_FINDINGS.md`; `Technical/docs/chapters/CHAPTER_9_INVESTIGATION.md`; `Knowledge_Base/text/narrative_chunk_{15,16,17}_ch5.md`; `Knowledge_Base/text/narrative_chunk_{18,20}_ch6.md`
- Book tables: Table 5.14 (Marxian vs orthodox comparison ratios, p.140); Figures 7.1 / 7.2 (in-book equivalents of "Chapter 9 figures"); the book has no actual Table 9.1
- External sources: none — S901 is purely aggregative
- Upstream series: S506, S511, S512, S513 (pending K*), S514 (pending K* and TCU), S608
- Local files: each upstream's `data/final/<sid>.csv`

## Reference values

- 41 book-period years 1948-1989; 164/164 populated `(year, indicator)` cells pass round-trip with `abs_err < 1e-9`
- Headline 1948-1989 book values (drawn from Ch7 §7.3 p.221 and the project's Wave-1 finals):
  - Exploitation rate `e = S*/V*`: 1.70 (1948) → 2.44 (1989), +44%
  - Productive labor share `Lp/L`: 0.57 (1948) → 0.36 (1989), −37%
  - Productive wage share `V*/W`: 0.54 (1948) → 0.36 (1989), −33%
  - Net social wage (NSW): negative throughout the postwar period (workers are net payers to the state, per Ch7 §7.3 p.223 and Appendix N)
- Marxian-vs-orthodox ratios from Table 5.14 (p.140): TP*/GP = 82%, TP*/GNP = 147%, S*/P = 224%, S*/V* = 210% of conventional equivalents
- Marxian profit rate (book aggregate): falls 25% over 1948-1989; NIPA-based net rate r'n falls 39% (faster because of the rising social burden rate b — Figure 7.2)
- Coverage gap: 88 cells (S513 + S514 columns × 41 years) are NaN pending K* and TCU; no synthetic fill

## Known issues

- **Book has no Chapter 9 and no Table 9.1**: S901 is a project-internal aggregation. Verified against book TOC pp.v-vii — chapters run 1-7 plus Appendices A-N
- Purely derived — inherits all upstream caveats from S506, S511, S512, S513, S514, S608
- Extension beyond 1989 blocked until all six upstream series are independently extended (Stage 4 EPRs)
- Table 5.14 comparison ratios are period-specific and may not hold under NAICS reclassification (1997+)
- S513 (Marxian profit rate) requires K* (productive fixed capital stock) — currently uses total K, producing understated levels but correct trend ([internal-decision-record])
- S514 requires both K* and TCU (capacity utilization) — neither sourced yet
- VA*/W constant assumption partially resolved in Session 14 ([internal-decision-record]); S506/S512 extension period carries small systematic error from SIC-NAICS gap interpolation
- The CHAPTER_9_INVESTIGATION.md project doc is the load-bearing internal record of why S901 has the columns it does

## Cross-references

- Upstream: S506 (exploitation rate), S511 (Lp/L), S512 (V*/W), S513 (r*), S514 (r*_adj), S608 (NSW/V*)
- Comparison data: Table 5.14 (page_140_marxian_orthodox_comparison.csv)
- Downstream: visualization layer (Stage 7); publication summary tables
- Related: S801 (cross-study comparison — same family of "summary view" artifacts); AS001 (social burden rate `b = t + eu` — the mechanism linking S513 to NIPA r'n)

## Provenance trail

- **Original research**: `Technical/research/S901_research.json`, researcher `agent`, 2026-03-21; ported from `ST2/research/T901_research.json` on 2026-05-14; verbatim quotes backfilled 2026-05-19 (`D3_RMWND_quotes_ch7_etc`) and 2026-05-23 (`stage1_cohort3_enrich`, `stage1_cohort3_S901AS001AS002`)
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (cohort agent 4); sources read = research JSON + KB chunks 24/25 + Knowledge_Base/tables/page_140 + Knowledge_Base/SUMMARY_KEY_FINDINGS + Technical/docs/chapters/CHAPTER_9_INVESTIGATION + registry entry + project CLAUDE.md (which mandates disclosure that S901 is a project artifact beyond the book's 7 chapters)
- **Anu Framework stage**: Stage 3 INGESTION (cohort 1, failing chapters); ingestion gate IDs P31/P32
