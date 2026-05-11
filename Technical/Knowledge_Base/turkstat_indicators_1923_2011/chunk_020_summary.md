# chunk_020 Summary — National Accounts: GDP Detailed Tables

**Source document**: turkstat_indicators_1923_2011 (TurkStat Statistical Indicators 1923-2011)
**PDF pages covered**: 698–707 (Tables 20.4–20.7 compact series; Table 20.8 detailed subsectors 1923–2006)
**Chapter**: Chapter 20 — National Accounts (Ulusal Hesaplar)

---

## Contents Overview

This chunk contains dense GDP/GNP data tables continuing the National Accounts chapter:

1. **Tables 20.4 and 20.5** (page 698): GDP by sector at current prices and at 1998 constant prices, ESA-95 series, 1998–2011.
2. **Charts 20.5–20.6** (page 699): Sectoral growth rates of GDP at current and constant prices (2000–2011).
3. **Tables 20.6 and 20.7** (page 700): GDP sectoral shares (%) at current prices and 1998 constant prices, 1998–2011.
4. **Charts 20.7–20.8** (page 701): Sectoral share bar charts.
5. **Table 20.8** (pages 702–707 and continuing into chunk_021): GNP by detailed economic activity at current prices, 1923–2006. This is the most granular historical series, breaking Agriculture into livestock/forestry/fishing and Industry into mining/manufacturing/electricity-gas-water, plus Construction, Trade, Transportation-Communication, and Financial Institutions.

---

## Tables Extracted

### chunk_020_table01 — GDP at current prices by sector (Table 20.4), ESA-95
- **File**: `chunk_020_table01_GDP_current_prices_by_sector_1998_2011.csv`
- **Coverage**: 1998–2011, annual
- **Unit**: Billion TL (ESA-95, purchaser's prices)
- **Columns**: Year, GDP total, Agriculture, Industry, Services (each with value and % change)
- **Key values**:
  - 1998: GDP = 70,203,147 Billion TL; Agriculture 12.5%, Industry 32.6%, Services 51.7% (note: this matches Table 20.6 shares)
  - 2008: GDP = 950,534,251 Billion TL
  - 2011 (provisional): GDP = 1,298,062,004 Billion TL (+18.1%)

### chunk_020_table02 — GDP at 1998 constant prices by sector (Table 20.5), ESA-95
- **File**: `chunk_020_table02_GDP_constant1998_prices_by_sector_1998_2011.csv`
- **Coverage**: 1998–2011, annual
- **Unit**: Billion TL at 1998 prices (ESA-95)
- **Key real GDP growth rates**: 2001 crisis = -5.7%; 2009 crisis = -4.8%; 2010 recovery = +9.2%; 2011 = +8.5%
- **Industry**: peaked at 33,704,158 in 2007, fell in 2008-2009, recovered to 37,947,481 in 2011

### chunk_020_table03 — GDP sectoral shares at current prices (Table 20.6)
- **File**: `chunk_020_table03_GDP_shares_current_prices_1998_2011.csv`
- **Coverage**: 1998–2011, annual
- **Key trend**: Agriculture share falls from 12.5% (1998) to 8.0% (2011); Services rise from 51.7% to 56.3%; Industry relatively stable 24–33%.

### chunk_020_table04 — GDP sectoral shares at 1998 constant prices (Table 20.7)
- **File**: `chunk_020_table04_GDP_shares_constant1998_prices_1998_2011.csv`
- **Coverage**: 1998–2011, annual
- **Key trend**: In real terms, Industry share rises from 32.6% (1998) to 33.0% (2011) while Agriculture falls from 12.5% to 9.2%.

### chunk_020_table05 — GNP detailed subsectors at current prices (Table 20.8), 1923–2006
- **File**: `chunk_020_table05_GNP_detailed_subsectors_current_prices_1923_2006.csv`
- **Coverage**: 1923–2006, annual (note: table continues beyond this chunk)
- **Unit**: Million TL (current prices)
- **Columns**: Year; Agriculture (total, livestock, forestry, fishing); Industry (total, mining, manufacturing, electricity-gas-water); Construction; Trade; Transportation-Communication; Financial Institutions
- **IMPORTANT**: This is the most detailed historical GNP breakdown available in the publication. It enables sectoral analysis back to 1923.
- **Key subsectors for ST2**:
  - Manufacturing industry: shows value added 1923–2006
  - Financial institutions: separate series
  - Construction: separate series
  - Transportation and communication combined

---

## ST2 Relevance — CRITICAL

- **Tables 20.4 and 20.5** provide the authoritative **ESA-95 GDP series 1998–2011** used as the primary modern GDP benchmark for Turkey. This is the most comparable international standard series.
- **Table 20.8** provides the **long historical series 1923–2006** with subsectoral detail — essential for structural analysis.
- **No compensation of employees / factor income data yet** — those tables (20.35 "Gelir yöntemiyle GSYH", pages 768–770) include wages, operating surplus, and mixed income breakdown. These will appear in a later chunk (approximately chunk_022 or later).
- The chapter TOC lists:
  - Table 20.35: GDP by income approach/cost components at current prices (p. 768)
  - Table 20.36: Growth rates of GDP by cost components (p. 769)
  - Table 20.37: Shares of GDP by cost components (p. 770)
  These are the key tables for wage/profit/factor share data.

---

## Series Reconciliation Notes

- Tables 20.1/20.2 (chunk_019) use an older 1987-base series ending 2006.
- Tables 20.4/20.5 (this chunk) use the newer ESA-95 1998-base series starting 1998, extending to 2011.
- The two series **overlap 1998–2006** and can be cross-checked: the 1987-base GNP for 2006 is 154,342,719 M TL while the ESA-95 GDP for 2006 is 758,390,785 Billion TL — different due to both different base years and GNP vs GDP distinction (GNP includes net factor income from abroad).
- For the ESA-95 series, note that 2005–2008 data are in "Thousand YTL" (= Million old TL effectively), and from 1.1.2009 the designation changes from YTL to TL.
