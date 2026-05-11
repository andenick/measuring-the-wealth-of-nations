# chunk_011 Summary
**Document**: turkstat_indicators_1923_2011 (TurkStat Statistical Indicators 1923–2011)
**PDF Pages**: 369–378 (book pagination)
**Topic**: Table 11.42 — Employment and basic indicators in financial intermediary institutions by economic activity (continued)

## Content Overview
This chunk is entirely Table 11.42, presenting five sub-tables for financial intermediary institutions (NACE Section K: Finance and Insurance Activities) by NACE Rev.2 sub-code. The table covers **2002–2010** (2002–2008 in one page group, 2009–2010 in a continuation panel).

## Sub-Tables Extracted

### Table 1 — Annual average number of employees (Ucretle calisanlarin yillik ortalama sayisi)
- Total financial & insurance (K): grew from 179,569 (2002) to 279,897 (2010)
- Monetary intermediation (64.11+64.19): 131,127 → 187,824
- Insurance (65): 10,018 → 15,875
- Auxiliary activities (66): 22,875 → 58,651

### Table 2 — Number of female employees (Ucretle calisan kadin sayisi)
- Total K: 73,929 (2002) → 132,475 (2010)
- Female share of total employment rose across all sub-sectors

### Table 3 — Number of male employees (Ucretle calisan erkek sayisi)
- Total K: 105,640 (2002) → 147,422 (2010)
- Male employment grew more slowly than female, indicating feminization of the sector

## NACE Codes Covered
| Code | Description |
|------|-------------|
| K | Financial and insurance activities (total) |
| 64 | Financial service activities (excl. insurance and pension funding) |
| 64.11+64.19 | Monetary intermediation (central bank, commercial banks, participation banks) |
| 64.91 | Financial leasing companies |
| 64.92 | Other credit granting (from 2009) |
| 64.99 | Other financial service activities n.e.c. (from 2009) |
| 65 | Insurance, reinsurance and pension funding |
| 65.11 | Life insurance |
| 65.12+65.20 | Non-life insurance and reinsurance |
| 66 | Activities auxiliary to financial services and insurance |
| 66.11 | Administration of financial markets / stock exchanges (from 2009) |
| 66.12 | Security and commodity contracts brokerage |
| 66.19 | Other auxiliary activities (credit surety cooperatives) |
| 66.21 | Risk and damage evaluation / insurance experts (from 2009) |
| 66.22 | Insurance agents and brokers (legal entities) |
| 66.30 | Fund management / portfolio management companies (from 2009) |

## Relevance to ST2 NickyData Extraction Focus
- **Wages and compensation**: Tables 4 (personnel cost) and 5 (wages & salaries) in this chunk directly provide **compensation of employees** for financial sector (2002–2010) in current TL.
- **Employment**: Annual average employee counts by gender and NACE sub-sector (2002–2010).
- These data belong to NACE K (financial intermediaries), not the economy-wide national accounts aggregates, but are relevant for sectoral labor share construction.
- No GDP/GSYH data in this chunk.

## CSV Files Written
- `chunk_011_table01_financial_intermediaries_annual_avg_employees.csv`
- `chunk_011_table02_financial_intermediaries_female_employees.csv`
- `chunk_011_table03_financial_intermediaries_male_employees.csv`
- `chunk_011_table04_financial_intermediaries_personnel_cost.csv`
- `chunk_011_table05_financial_intermediaries_wages_salaries.csv`

## Data Quality Notes
- Series break in 2009: several sub-categories newly included (66.11, 66.21, 66.30, consumer finance companies, lenders, asset management etc.)
- 2007 onwards: commercial banks reclassified as "deposit money banks"
- 2006 onwards: Special Finance Houses reclassified as Participation Banks
- 2003: Credit surety cooperatives of craftsmen/artisans first included
- Units: employment = persons; monetary values = Turkish Lira (current)
