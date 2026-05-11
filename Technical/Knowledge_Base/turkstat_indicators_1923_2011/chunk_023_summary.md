# Chunk 023 Summary — TurkStat Statistical Indicators 1923-2011

## Document Pages Covered
Pages 728–737 (Book page numbers printed in PDF)

## Chapter
Chapter 20: National Accounts

## Tables Extracted

### Table 20.13 — GDP by Kind of Economic Activity at 1998 Prices
- **File**: `chunk_023_table2013_gdp_by_economic_activity_1998prices.csv`
- **Coverage**: 1998–2011 (annual)
- **Unit**: Billion TL (Milyar TL); 2005–2008 in Thousand TRY; from 2009 in TL
- **Content**: GDP broken down into 14 sector categories (Agriculture/Forestry/Hunting, Fishing, Mining, Manufacturing, Electricity/Gas/Water, Construction, Wholesale/Retail Trade, Hotels/Restaurants, Transport/Communication, Financial Intermediation, Ownership of Dwellings, Real Estate/Renting/Business, Public Admin/Defence, Education, Health, Other Community, Private Households) plus Total Sectors, FISIM deduction, Taxes-Subsidies, and Total GDP at Purchasers' Prices
- **Note**: 2011 preliminary (*); 2008 row for sector 9 (Real Estate) appears truncated in source

### Table 20.14 — GNP per Capita
- **File**: `chunk_023_table2014_gnp_per_capita.csv`
- **Coverage**: 1923–2006 (annual)
- **Unit**: TL (constant producers prices), TL (current producers prices), USD (current producers prices), all with % year-on-year change
- **Content**: Long-run GNP per capita series across multiple price bases (1948, 1968, 1987 base years); USD per capita series shows dollar income levels
- **Notable**: Multiple currency unit breaks due to base year changes; 2005–2006 given in TRY

### Table 20.15 — Sectoral Shares in GNP at Current Prices
- **File**: `chunk_023_table2015_sectoral_shares_gnp_current_prices.csv`
- **Coverage**: 1923–2006 (annual)
- **Unit**: Percent (%)
- **Sectors**: Agriculture, Industry, Services
- **Content**: Long-run structural transformation: Agriculture fell from ~40–50% (1920s) to ~9–10% (2000s); Industry rose from ~10% to ~25%; Services from ~40% to ~65%

### Table 20.16 — Sectoral Shares in GNP at Constant Prices
- **File**: `chunk_023_table2016_sectoral_shares_gnp_constant_prices.csv`
- **Coverage**: 1923–2006 (annual)
- **Unit**: Percent (%)
- **Sectors**: Agriculture, Industry, Services
- **Content**: Same structural transformation viewed at constant prices (1948, 1968, 1987 price bases)

### Table 20.17 — Sectoral Shares in GDP at Current Prices (Detailed)
- **File**: `chunk_023_table2017_gdp_sectoral_shares_current_prices.csv`
- **Coverage**: 1998–2011 (annual)
- **Unit**: Percent (%)
- **Content**: Full 14-sector breakdown of GDP shares at current prices; includes FISIM deduction and taxes-subsidies to reconcile to 100%
- **Note**: 2011 preliminary (*)

### Table 20.18 — Sectoral Shares in GDP at 1998 Constant Prices (Detailed)
- **File**: `chunk_023_table2018_gdp_sectoral_shares_1998constant_prices.csv`
- **Coverage**: 1998–2011 (annual)
- **Unit**: Percent (%)
- **Content**: Full 14-sector breakdown of GDP shares at constant 1998 prices
- **Note**: 2011 preliminary (*)

## Key Observations
- Manufacturing share in GDP (current prices) declined from 23.9% (1998) to 16.2% (2011)
- Construction share rose from 5.8% (1998) to 4.4% (2011) — with peak ~6.4% in 2006 at constant prices
- Financial intermediation share volatile (7.6% in 1998, 3.1% in 2011 at current prices)
- Agriculture at current prices fell from 12.1% (1998) to 7.8% (2011)
- FISIM deduction grew in significance: from 5.0% of GDP (1998) to 8.2% (2011) at constant prices

## Extraction Quality
- Good: Tables 20.14–20.18 extracted completely and cleanly
- Partial: Table 20.13 row for 2008 (sector 9 Real Estate value cut off at "3,473" — likely 3,473,xxx); rows for 2009–2011 missing some sector detail in the PDF text flow (columns 4–9 absent in text extraction for 2009+). These sectors' absolute values for 2009–2011 are available in Table 20.13 growth rates and shares but not directly recoverable from this chunk's text.
- No fabrication: missing cells left blank in CSV
