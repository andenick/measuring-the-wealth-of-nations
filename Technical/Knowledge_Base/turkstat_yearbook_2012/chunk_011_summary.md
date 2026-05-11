# Chunk 011 Summary — Turkey's Statistical Yearbook 2012

## Extraction Metadata
- **Source**: chunk_011.pdf
- **Pages**: 10 (all digital, PyMuPDF extraction, confidence 1.00)
- **Yearbook pages covered**: 358–377
- **Chapters**: End of Chapter 21 (National Accounts) + Chapter 22 (Income and Living Conditions)

---

## Chapter Content

### Chapter 21 (National Accounts) — Final pages
Pages 358–359 contain the tail end of Chapter 21 with two household consumption expenditure tables (21.14 and 21.15) broken down by COICOP category.

### Chapter 22: Gelir ve Yaşam Koşulları / Income and Living Conditions
Pages 359–377. Source survey: **Gelir ve Yaşam Koşulları Araştırması** (Income and Living Conditions Survey, annual panel survey since 2006, ~12,800 households per year).

Pages 360–363: Methodology and definitions — household net annual disposable income, equivalence scale (OECD modified: 1.0/0.5/0.3), Gini coefficient, income types (salary/wage, entrepreneur income, rental, property, transfer).

Pages 370–371: **Tables 22.4 and 22.5** — annual average main job income by occupation and employment status (2007–2011). These are the most relevant earnings data for ST2.

Pages 372: **Table 22.6** — poverty rates and poverty gap (2009–2011).

Pages 377: Chapter 23 table of contents (Consumption Expenditures and Absolute Poverty).

---

## Tables Extracted

### chunk_011_table01 — Table 21.14: Household Consumption at Current Prices 2008–2012
- Unit: Thousand TL
- Rows: 11 COICOP categories (food/beverages/tobacco, clothing, housing/energy, furnishing, health, transport/communication, recreation/culture, education, restaurants/hotels, miscellaneous)
- Total consumption rose from 695.6 billion TL (2008) to 1,043.0 billion TL (2012)

### chunk_011_table02 — Table 21.15: Household Consumption at 1998 Constant Prices 2008–2012
- Unit: Thousand TL at 1998 prices
- Same 11 COICOP categories
- Real consumption: 73.8 billion TL (2008) to 82.6 billion TL (2012) — real growth of ~12%

### chunk_011_table03 — Table 22.4 (continuation): Average Annual Main Job Income by Occupation Group 2010–2011
- Unit: TL (nominal annual)
- Dimensions: Year (2010, 2011) × Geography (Turkey total, Rural males, Rural females, Urban males, Urban females) × ISCO-88 occupation group (9 groups + total)
- Note: This is the **continuation** page; years 2007–2009 appeared in a prior chunk (chunk_010 or earlier)
- Key finding: Turkey total average annual income rose from 12,558 TL (2010) to 14,159 TL (2011)

### chunk_011_table04 — Table 22.5: Average Annual Main Job Income by Employment Status 2007–2011
- Unit: TL (nominal annual)
- Dimensions: Year (2007–2011) × Geography (Turkey, Rural, Urban) × Sex (total, males, females) × ICSE employment status (total, regular employee, casual employee, employer, self-employed)
- **CRITICAL FOR ST2**: This is direct wage/salary income data covering 2007–2011
- Regular employee (ücretli, maaşlı) Turkey-total wages:
  - 2007: 10,308 TL/year
  - 2008: 11,471 TL/year
  - 2009: 13,014 TL/year
  - 2010: 13,707 TL/year
  - 2011: 14,904 TL/year
- Source: TurkStat Income and Living Conditions Survey 2007–2011

### chunk_011_table05 — Table 22.6: Poverty Rates and Poverty Gap by Relative Thresholds 2009–2011
- Unit: TL (threshold), thousands of persons (poor count), % (rate and gap)
- Dimensions: 4 threshold levels (40/50/60/70% of median) × 3 years × 3 geographies (Turkey, urban, rural)
- Turkey 60% threshold poverty rate: 24.3% (2009) → 23.8% (2010) → 22.9% (2011)

---

## Relevance Assessment for ST2 / Compensation of Employees

**HIGH RELEVANCE:**
- Table 22.5: Annual wage income by employment status 2007–2011. Provides time series for regular employee wages, casual wages, employer income, and self-employed income — directly relevant to compensation of employees estimates.
- Table 22.4 continuation: Wage differentials by occupation group 2010–2011 with urban/rural breakdown.

**MODERATE RELEVANCE:**
- Tables 21.14/21.15: Household consumption by category — useful for national accounts cross-checking but not direct compensation data.

**NOT RELEVANT to compensation:**
- Table 22.6: Poverty rates — demographic reference only.

**IMPORTANT NOTE**: Table 22.4 covers 2010–2011 only in this chunk. Years 2007–2009 for Table 22.4 were in a prior chunk. Table 22.5 covers the full 2007–2011 range and is complete.
