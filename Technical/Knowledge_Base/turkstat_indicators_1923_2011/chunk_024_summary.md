# Chunk 024 Summary — TurkStat Statistical Indicators 1923-2011

## Document Pages Covered
Pages 738–747 (Book page numbers printed in PDF)

## Chapter
Chapter 20: National Accounts

## Tables Extracted

### Table 20.19 — Sectoral Growth Rates of GDP at Current Prices
- **File**: `chunk_024_table2019_gdp_sectoral_growth_rates_current_prices.csv`
- **Coverage**: 1999–2011 (year-on-year changes)
- **Unit**: Percent (%)
- **Content**: Growth rates for all 14 sectors plus FISIM change, Taxes-Subsidies change, and total GDP growth at current prices
- **Note**: 2011 preliminary (*). Negative values present (e.g. Financial Intermediation -25.4% in 2002; Construction -18.1% in 2009)

### Table 20.20 — Sectoral Growth Rates of GDP at 1998 Constant Prices
- **File**: `chunk_024_table2020_gdp_sectoral_growth_rates_1998constant_prices.csv`
- **Coverage**: 1999–2011 (year-on-year changes)
- **Unit**: Percent (%)
- **Content**: Real sectoral growth rates (volume changes). Shows 2001 crisis (-5.7% total GDP), 2009 contraction (-4.8% total GDP), and recovery periods
- **Key findings**:
  - 2001 crisis worst hit: Construction -17.4%, Agriculture -8.1%, Manufacturing -7.6%
  - 2009 crisis: Construction -16.1%, Manufacturing -7.2%, Wholesale/Retail -10.4%
  - Strong recovery 2010: Construction +18.3%, Manufacturing +13.6%
  - 2011 broad-based growth: GDP +8.5%

### Table 20.21 — GDP by Expenditure Approach at Current Prices (Levels)
- **File**: `chunk_024_table2021_gdp_expenditure_approach_current_prices.csv`
- **Coverage**: 1980–2006 (annual levels)
- **Unit**: Million TL (Milyon TL); 2005–2006 in TRY
- **Components**:
  - Private final consumption expenditures (total + sub-components from 1987: food/beverages, durable goods, semi-durable/non-durable, energy/transport/communication, services, ownership of dwellings)
  - Gross Fixed Capital Formation: Public sector (total, machinery & equipment, building construction, other construction) + Private sector (total, machinery & equipment, building construction)
  - Government final consumption expenditure (total, wages & salaries, other current)
  - Change in stocks
  - Exports of goods and services
  - Imports of goods and services (deducted)
  - GDP total
- **Note**: GFCF sub-components for 2004–2006 partially cut off in PDF text flow; 2003 GDP total confirmed at 358,699,628,542 from continuation page

### Table 20.22 — Growth Rate of GDP by Expenditure Approach at Current Prices
- **File**: `chunk_024_table2022_gdp_expenditure_growth_rates_current_prices.csv`
- **Coverage**: 1981–2006 (year-on-year changes)
- **Unit**: Percent (%)
- **Content**: Nominal growth rates for all GDP expenditure components
- **Notable patterns**:
  - Consistently high nominal growth throughout 1980s–1990s (hyperinflation era)
  - 1994 crisis: GDP +95.2% nominal (high inflation), investment subdued
  - 2001 crisis: GDP +47.2% nominal but GFCF private machinery fell -14.1%
  - Post-2001 stabilization: GDP growth moderated from ~47% to ~15% by 2005

## Key Observations for ST2 NickyData
- **Real GDP growth rates (Table 20.20)** are the most relevant for ST2 analysis:
  - 1999: -3.4%, 2000: +6.8%, 2001: -5.7%, 2002: +6.2%, 2003: +5.3%, 2004: +9.4%, 2005: +8.4%, 2006: +6.9%, 2007: +4.7%, 2008: +0.7%, 2009: -4.8%, 2010: +9.2%, 2011: +8.5%
- **Expenditure composition (Table 20.21)**: Private consumption dominated (typically 60–70% of GDP); investment (GFCF) was ~20–25%; exports and imports roughly balanced with Turkey running current account deficits
- **GFCF public vs private**: Private sector GFCF consistently larger than public from mid-1980s onward; private machinery & equipment grew rapidly in 2000s

## Extraction Quality
- Tables 20.19 and 20.20: Complete extraction, all values recovered
- Table 20.21: Good for 1980–2003; 2004–2006 rows partially truncated in PDF text extraction (line wrapping issues for very large numbers). GDP totals for earlier years confirmed cross-checked against Table 20.22 growth rates
- Table 20.22: Complete extraction, all years 1981–2006 recovered
- No data fabrication: missing/truncated cells left blank in CSV

## Chunk Boundary Notes
- These chunks (023–024) cover pages ~728–747
- No sign of Tables 20.35–20.37 (income/cost components: compensation of employees, operating surplus, mixed income, taxes on production) — those tables are in later chunks
- The expenditure-side GDP tables (20.21–20.22) end at 2006; more recent data may appear in companion tables in later chunks
