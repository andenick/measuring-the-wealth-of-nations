# chunk_008 Summary — TurkStat Statistical Indicators 1923-2011
## Source pages: 284–337 (sampled pages; chunk covers approximately this range)

## Content Overview
This chunk contains two distinct sections:

### Section 1: Table 11.14 — Enterprise Basic Indicators by Economic Activity (pages 284–289)
Continuation of the NACE-classified enterprise survey. Covers years **2007, 2008, 2009**.
- 2007–2008: NACE Rev.1.1 classification (same sectors as chunk_007)
- 2009: **Classification switched to NACE Rev.2** — more disaggregated sectors, unit also changed from "Million TL" to plain "TL"

### Section 2: Table 11.37 — Industrial Turnover Index, NACE Rev.2 (page 334)
Selected manufacturing sub-sectors, base year 2005=100, years 2005–2011.

### Section 3: Table 11.38 — Quarterly Industrial Employment Index (pages 335–337)
Industrial employment index by:
- Main industrial groupings (total, intermediate goods, durable/non-durable consumer, energy, capital)
- Mining and quarrying sub-sectors
- Manufacturing sub-sectors (extensive disaggregation by product type)
- Electricity, gas and water utilities
Base year 2005=100, annual averages, years 2005–2011.

## Tables Extracted: 13 CSV files

| File | Content | Years |
|------|---------|-------|
| chunk_008_table01 | 11.14 NACE Rev.1.1 2007 Part 1 — Employment & Personnel Costs | 2007 |
| chunk_008_table02 | 11.14 NACE Rev.1.1 2007 Part 2 — Turnover, Production, Value-Added | 2007 |
| chunk_008_table03 | 11.14 NACE Rev.1.1 2008 Part 1 — Employment & Personnel Costs | 2008 |
| chunk_008_table04 | 11.14 NACE Rev.1.1 2008 Part 2 — Turnover, Production, Value-Added | 2008 |
| chunk_008_table05 | 11.14 NACE Rev.2 2009 Part 1 — Employment & Personnel Costs | 2009 |
| chunk_008_table06 | 11.14 NACE Rev.2 2009 Part 2 — Turnover, Production, Value-Added | 2009 |
| chunk_008_table07 | 11.37 Industrial Turnover Index — selected mfg sectors | 2005–2011 |
| chunk_008_table08 | 11.38 Quarterly Employment Index — main industrial groupings | 2005–2011 |
| chunk_008_table09 | 11.38 Quarterly Employment Index — mining sub-sectors | 2005–2011 |
| chunk_008_table10 | 11.38 Quarterly Employment Index — manufacturing part 1 | 2005–2011 |
| chunk_008_table11 | 11.38 Quarterly Employment Index — manufacturing part 2 | 2005–2011 |
| chunk_008_table12 | 11.38 Quarterly Employment Index — manufacturing part 3 | 2005–2011 |
| chunk_008_table13 | 11.38 Quarterly Employment Index — manufacturing part 4 + utilities | 2005–2011 |

## Key Observations for ST2 NickyData Extraction Focus

### Personnel Costs (Compensation Proxy) — Total Economy Enterprise Survey
- 2007: 103,468,454,970 Million TL; 7,007,493 wage employees
- 2008: 117,823,139,049 Million TL; 7,380,490 wage employees
- 2009: 119,425,401,816 TL (unit change); 6,921,035 wage employees

### NACE Rev.2 Classification Change (2009)
The 2009 switch to NACE Rev.2 adds new sectors not present in Rev.1.1:
- J: Information and communication (new separate sector)
- L: Real estate activities (slimmed down from K)
- M: Professional, scientific and technical activities (split from K)
- N: Administrative and support service activities (split from K)
- Q: Human health and social work (renamed from N)
- R: Arts, entertainment and recreation (new)
This makes direct 2008→2009 sectoral comparison problematic; the totals remain comparable.

### Industrial Employment Index (Table 11.38) — HIGH RELEVANCE
The quarterly industrial employment index provides an **annual employment quantity index** (2005=100) for:
- Total industry: rose to 106.7 in 2007, dropped to 96.2 in 2009 (GFC dip), recovered to 105.9 by 2011
- Manufacturing total: similar pattern — peak 106.3 (2008), trough 95.5 (2009), recovery 105.9 (2011)
- This is useful for employment deflation / quantity adjustment of labour data.
- Note the electricity/gas sector employment index DECLINED steadily (100→75.8 by 2011), likely due to privatisation.

### Value-Added at Factor Cost — Enterprise Survey Totals
- 2007: 231,880,826,661 Million TL
- 2008: 270,493,624,299 Million TL
- 2009: 258,386,157,884 TL
These are NOT full GDP — they cover formal enterprises only, exclude agriculture and public administration.

## Critical Caveats
1. **Unit discontinuity**: 2002–2008 personnel costs in "Million TL"; 2009 in "TL" (so 2009 figures are directly comparable to 2008 Million TL values × 1,000,000 if the labelling is consistent — but the magnitude suggests the 2009 figures ARE in plain TL, making them ~1,000x larger in nominal terms than expected. Likely a presentation change in the source publication. Treat with care — verify against known GDP/CoE totals before using.)
2. These enterprise survey tables cover the **formal non-agricultural private sector** predominantly. Do not confuse with national accounts aggregates.
3. GDP/GSYH macro series and full compensation of employees are in other chapters of this document (chapters 3–5 typically).
