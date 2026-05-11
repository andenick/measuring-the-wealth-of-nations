# chunk_004 Summary
**Document**: TurkStat Statistical Indicators 1923-2011
**Pages**: ~130–143 (Section 8 start — Labour Force chapter)
**Content type**: Definitions, labour force status tables, sectoral employment, unemployment/employment by education

## Contents

### Definitions page (page 130)
Bilingual Turkish/English glossary of all key labour market concepts:
- Non-institutional population, Labour force, Labour force participation rate
- Employed persons (at work / not at work), Employment rate
- Unemployed persons (definition, including 3-month job search criterion)
- Unemployment rate, Persons not in labour force
- Distinctions: regular employee vs casual, unpaid family worker, self-employed

### Table 8.1 — Non-institutional population by labour force status [Total], 1988–2003
- Full population accounting: total pop, age 15-, age 15+, labour force, not in LF, employed, unemployed
- Rates: labour force participation rate, unemployment rate, employment rate
- Split by Total / Male / Female
- Coverage: 1988–2003 (the 2004–2011 continuation is presumably in another chunk)
- CSV: `chunk_004_table01_labour_force_status_total.csv`

### Table 8.3 — Non-institutional population by labour force status [Rural], 2004–2011
- Same structure as Table 8.1 but for rural population only
- Split by Total / Male / Female
- CSV: `chunk_004_table02_labour_force_status_rural.csv`
- **Note**: Tables 8.2 (Urban) not present in this chunk.

### Table 8.4 — Employed persons by kind of economic activity [15+ age], Old Series (ISIC), 1923–2009
- 9 sectors: Agriculture/forestry/hunting/fishing, Mining, Manufacturing, Electricity/gas/water, Construction, Wholesale/retail/restaurants/hotels, Transport/communication/storage, Finance/insurance/real estate, Community/social/personal services
- Coverage: 1923–2009 total only (no male/female split in old series)
- Pre-1988 source: BULUTAY T. (1995) ILO/SIS Ankara, updated
- 1988–2009 source: Household Labour Force Survey
- CSV: `chunk_004_table03_employment_by_economic_activity_old_series.csv`
- **KEY for ST2**: Manufacturing and services employment series from 1923 onward.

### Table 8.4 (continued) — Employed persons by kind of economic activity, NACE Rev.2 (New Series), 2009–2011
- ~18 detailed NACE sectors including finance, real estate, professional services, public admin, education, health
- Split by Total / Male / Female
- Only 3 years available (2009–2011)
- CSV: `chunk_004_table04_employment_by_economic_activity_nace_rev2.csv`

### Table 8.5 — Unemployed persons by educational status [15+ age], 1988–2011
- 8 education level columns (illiterate through higher education)
- Split by Total / Male / Female
- Coverage: 1988–2003 and 2004–2011 (both parts present)
- CSV: `chunk_004_table05_unemployed_by_educational_status.csv`

### Table 8.6 — Employed persons by educational status [15+ age], 1988–2011
- 8 education level columns (illiterate through higher education)
- Split by Total / Male / Female
- Coverage: 1988–2003 and 2004–2011 (both parts present — the 2004–2011 part was on the first page of chunk_003)
- CSV: `chunk_004_table06_employed_by_educational_status.csv`

## Relevance to ST2 NickyData Extraction Focus
- **Employment totals (istihdam)**: Table 8.1 provides the definitive national employment headcount series with rates, 1988–2003.
- **Wage employees**: Not directly in this chunk — see Table 8.8 in chunk_003.
- **Sectoral employment**: Table 8.4 old series gives manufacturing employment 1923–2009 — useful for Moos shift and structural change analysis.
- **No direct GDP, compensation-of-employees (ucret), or national accounts monetary series** in this chunk. Those likely appear in earlier/later chapters (Chapter 9 or 10 typically covers national accounts in TurkStat publications).
- The rural labour force table (8.3) provides urban/rural decomposition context for labour share studies.
