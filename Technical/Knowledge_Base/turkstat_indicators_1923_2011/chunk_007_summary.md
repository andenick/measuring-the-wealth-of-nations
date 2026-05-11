# chunk_007 Summary — TurkStat Statistical Indicators 1923-2011
## Source pages: 274–283

## Content Overview
This chunk contains **Table 11.14** repeated for years 2002–2006, each year split into two sub-tables. The table is titled "Girişim bazında temel göstergeler" (Basic indicators on enterprises by economic activity) classified by NACE Rev.1.1 (European Community economic activity classification).

## Tables Extracted: 10 CSV files

| File | Year | Sub-table | Columns |
|------|------|-----------|---------|
| chunk_007_table01 | 2002 | Part 1 | Enterprises, Persons Employed, Employees, Personnel Costs (Million TL) |
| chunk_007_table02 | 2002 | Part 2 | Turnover, Production Value, Value-Added at Factor Cost (Million TL) |
| chunk_007_table03 | 2003 | Part 1 | Enterprises, Persons Employed, Employees, Personnel Costs (Million TL) |
| chunk_007_table04 | 2003 | Part 2 | Turnover, Production Value, Value-Added at Factor Cost (Million TL) |
| chunk_007_table05 | 2004 | Part 1 | Enterprises, Persons Employed, Employees, Personnel Costs (Million TL) |
| chunk_007_table06 | 2004 | Part 2 | Turnover, Production Value, Value-Added at Factor Cost (Million TL) |
| chunk_007_table07 | 2005 | Part 1 | Enterprises, Persons Employed, Employees, Personnel Costs (Million TL) |
| chunk_007_table08 | 2005 | Part 2 | Turnover, Production Value, Value-Added at Factor Cost (Million TL) |
| chunk_007_table09 | 2006 | Part 1 | Enterprises, Persons Employed, Employees, Personnel Costs (Million TL) |
| chunk_007_table10 | 2006 | Part 2 | Turnover, Production Value, Value-Added at Factor Cost (Million TL) |

## NACE Sectors Covered (Rev.1.1)
- C: Mining and quarrying
- D: Manufacturing
- E: Electricity, gas and water supply
- F: Construction
- G: Wholesale and retail trade; repair of motor vehicles
- H: Hotels and restaurants
- I: Transport, storage and communications
- K: Real estate, renting and business activities
- M: Education
- N: Health and social work
- O: Other community, social and personal service activities

## Key Observations for ST2 NickyData Extraction Focus
- **Ücretli çalışanlar (employed employees / wage workers)**: Available for each NACE sector, each year 2002–2006. Total economy figures:
  - 2002: 4,279,432 employees; Personnel costs 30,844,915,169 Million TL
  - 2003: 4,626,213 employees; Personnel costs 47,719,172,700 Million TL
  - 2004: 5,251,561 employees; Personnel costs 62,449,089,229 Million TL
  - 2005: 6,369,926 employees; Personnel costs 76,207,292,805 Million TL
  - 2006: 6,747,521 employees; Personnel costs 87,836,550,093 Million TL
- **Personel maliyetleri (personnel costs)**: This is a compensation-of-employees proxy, broken down by sector.
- **Faktör maliyetiyle katma değer (Value-added at factor cost)**: Available by sector 2002–2006. Total economy:
  - 2002: 128,880,465,323 Million TL
  - 2003: 143,318,607,847 Million TL
  - 2004: 174,004,663,245 Million TL
  - 2005: 185,797,967,886 Million TL
  - 2006: 210,976,441,499 Million TL
- These are **enterprise survey data** (covering formal sector enterprises), NOT full national accounts. They undercount the informal economy and agriculture. Should NOT be used directly as GDP or full CoE.
- Currency unit is **Million TL** (old Turkish Lira, pre-2005 redenomination for 2002–2004; from 2005 onwards the figures are in new TL / YTL — but the document labels remain "Million TL").

## Relevance to Extraction Focus
- **Moderate relevance**: Contains compensation data (personel maliyetleri) and sectoral employment by year 2002–2006.
- Does NOT contain macroeconomic GDP/GSYH aggregates — those are in other sections of the document.
- Does NOT cover pre-2002 years.
- The personnel cost series can serve as a partial wage bill proxy for formal enterprise sector.
