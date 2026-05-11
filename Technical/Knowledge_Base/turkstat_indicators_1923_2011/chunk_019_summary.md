# chunk_019 Summary — National Accounts Chapter Opening

**Source document**: turkstat_indicators_1923_2011 (TurkStat Statistical Indicators 1923-2011)
**PDF pages covered**: 688–697 (chapter table of contents, explanation, Tables 20.1–20.3, and charts 20.1–20.4)
**Chapter**: Chapter 20 — National Accounts (Ulusal Hesaplar)

---

## Contents Overview

This chunk opens the **National Accounts chapter** — the most important chapter for GDP and factor income data. It contains:

1. **Chapter table of contents** (pages 688–689): Lists all 37 tables and 8 charts in the chapter, covering GNP/GDP by sector, expenditure approach, income approach, sectoral shares and growth rates.
2. **Methodological explanation** (page 690): Describes data sources: 1923–1947 from Bulutay/Yıldırım/Tezel, 1948+ from TurkStat. Series history: base year shifts (1948 → 1968 → 1987 → 1998). ESA-95 framework adopted in 2008 for 1998-base series.
3. **Table 20.1**: GNP by sector at current prices, 1923–2006 (pages 691–692).
4. **Table 20.2**: GNP by sector at constant prices, 1923–2006 (pages 693–694). Base years: 1923–1947 at 1948 prices; 1948–1967 at 1968 prices; 1968–2006 at 1987 prices.
5. **Table 20.3**: GDP per capita, 1998–2011 (page 695). Current TL, current USD, and constant 1998 TL, with mid-year population.
6. **Charts 20.1–20.4** (pages 696–697): GDP per capita bar charts (constant and current prices), GDP growth rate line charts.

---

## Tables Extracted

### chunk_019_table01 — GNP at current prices by sector (Table 20.1)
- **File**: `chunk_019_table01_GNP_current_prices_by_sector_1923_2006.csv`
- **Coverage**: 1923–2006, annual
- **Columns**: Year, GNP (Million TL), % change; Agriculture, Industry, Services (each with value and % change)
- **Unit**: Million TL throughout (note: values grow from 953 in 1923 to 575,783,962,136 in 2006 — hyperinflation era included)
- **Key values**: GNP 1923 = 953 M TL; 1987 = 75,019,388 M TL; 2006 = 575,783,962,136 M TL

### chunk_019_table02 — GNP at constant prices by sector (Table 20.2)
- **File**: `chunk_019_table02_GNP_constant_prices_by_sector_1923_2006.csv`
- **Coverage**: 1923–2006, annual
- **Columns**: Year, GNP, Agriculture, Industry, Services (all in Million TL, with % change columns)
- **Base years**: 1923–1947 at 1948 prices; 1948–1967 at 1968 prices; 1968–2006 at 1987 prices
- **Key observations**:
  - Real GNP 1923 = 2,929 M TL (1948 prices)
  - Real GNP 1987 = 75,019,388 M TL (1987 prices, base year)
  - Real GNP 2006 = 154,342,719 M TL (1987 prices)
  - Strong contraction in 1994 (-6.1%), 1999 (-6.1%), 2001 (-9.5%)
  - 1942–1943 WWII distortions visible in current prices but NOT in constant (real recovery)

### chunk_019_table03 — GDP per capita 1998–2011 (Table 20.3)
- **File**: `chunk_019_table03_GDP_per_capita_1998_2011.csv`
- **Coverage**: 1998–2011, annual
- **Columns**: Mid-year population (thousands), GDP per capita in current TL, % change, in current USD, % change, in constant 1998 TL, % change
- **Key values**:
  - 1998: $4,338 per capita
  - 2001: $3,021 (sharp drop due to financial crisis)
  - 2008: $10,438 (peak before crisis)
  - 2011: $10,469

---

## ST2 Relevance

- **Table 20.2** (constant price GNP series 1923–2006) is directly relevant to ST2 as the long-run real output series.
- **Table 20.1** provides current-price GNP for deflator construction.
- **No compensation of employees or factor share data in this chunk** — those tables (20.35–20.37, income approach) are listed in the TOC as pages 768–770 and will appear in later chunks.
- The chapter TOC confirms Tables 20.35–20.37 cover "Gelir yöntemiyle GSYH" (GDP by income/cost components) including wages.

---

## Notes on Series Breaks

- **1947/1948 break**: Constant price series switches from 1948-base to 1968-base — the 1948 value jumps from 8,192 (1948 prices) to 37,065 (1968 prices). These are different base-year series, not a growth discontinuity.
- **1967/1968 break**: Switches from 1968-prices to 1987-prices. The 1968 value of 105,461 (1968 prices) becomes 31,635,197 (1987 prices).
- Imputed bank service charges (FISIM) deducted from sectors throughout.
