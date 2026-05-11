# Chunk 012 Summary — Turkey's Statistical Yearbook 2012

## Extraction Metadata
- **Source**: chunk_012.pdf
- **Pages**: 10 (all digital, PyMuPDF extraction, confidence 1.00)
- **Yearbook pages covered**: 378–404
- **Chapters**: Chapter 23 intro (Consumption Expenditures and Absolute Poverty) + Chapter 25 (Labour Cost and Structure of Earnings)

---

## Chapter Content

### Chapter 23: Tüketim Harcamaları ve Mutlak Yoksulluk / Consumption Expenditures and Absolute Poverty
Pages 378–379: Methodology explanation for Household Budget Survey (HBS). Surveys applied 2009 (12,600 HH), 2010–2011 (13,248 HH per year). No data tables appear in this chunk for Chapter 23 — only the chapter explanation pages. Tables 23.1–23.9 begin at p.381+ (next chunk).

### Chapter 25: İşgücü Maliyeti ve Kazanç Yapısı / Labour Cost and Structure of Earnings
Pages 397–404. This is the **most important chapter for ST2 labour cost data**.

**Two sub-sections covered:**

#### A. Kazanç Yapısı (Structure of Earnings)
Source: **Kazanç Yapısı Araştırması** (Structure of Earnings Survey) — structural survey conducted every 4 years (2006, 2010). Covers enterprises with 10+ employees. Scope: NACE Rev.1.1 sectors C-K and M-O (2006); NACE Rev.2 sectors B-N and P-S (2010).

Publication tables based on full-time employees only: 99.3% of employees in 2006, 98.7% in 2010.

Key concepts defined (pp.398–399):
- **Aylık ücret** (Monthly wage): basic wages + overtime + shift premiums + other regular payments
- **Kazanç** (Earnings): basic wages + regular payments + irregular payments (bonuses, profit shares) + in-kind payments
- **Saatlik ücret** (Hourly wage): monthly wage ÷ monthly paid hours

#### B. İşgücü Maliyeti Endeksi (Labour Cost Index)
Quarterly index, base year 2008. NACE Rev.2 coverage. Three sub-indices: total labour cost, earnings, and labour cost excluding earnings (= employer social security contributions + severance/termination payments).

Pages 400–401: Methodology, classification details, sector coverage (B through N excluding L).

---

## Tables Extracted

### chunk_012_table01 — Table 25.1: Monthly Average Gross Wage and Annual Average Gross Earnings by Sex and Major Occupational Group, 2006 and 2010
- Unit: TL
- **CRITICAL FOR ST2**: This is the formal Structure of Earnings Survey data — the most rigorous wage measurement in the yearbook
- Dimensions: Year (2006, 2010) × Sex (Total, Males, Females) × ISCO-88 (2006) or ISCO-08 (2010) occupation groups
- Columns: employee share (%), monthly paid hours, hourly average gross wage (TL), monthly average gross wage (TL), annual average gross earnings (TL)

**Key findings — Turkey all sectors, all employees:**

| Year | Sex | Monthly Paid Hours | Monthly Avg Gross Wage (TL) | Annual Avg Gross Earnings (TL) |
|------|-----|-------------------|----------------------------|-------------------------------|
| 2006 | Total | 199.7 | 1,103 | 14,252 |
| 2006 | Males | 200.3 | 1,107 | 14,316 |
| 2006 | Females | 197.5 | 1,091 | 14,036 |
| 2010 | Total | 200.1 | 1,512 | 19,694 |
| 2010 | Males | 201.1 | 1,510 | 19,683 |
| 2010 | Females | 196.9 | 1,519 | 19,728 |

Note: Female total wages are slightly higher than males in 2010 aggregate due to compositional effects (higher female share in high-wage professional/clerical groups).

**Occupation group wage spread 2010 (all employees, TL annual):**
- Managers (ISCO-08 group 1): 49,170
- Professionals (ISCO-08 group 2): 33,974
- Technicians (ISCO-08 group 3): 24,628
- Clerical support (ISCO-08 group 4): 21,478
- Service and sales (ISCO-08 group 5): 13,787
- Craft and trades (ISCO-08 group 7): 16,921
- Plant/machine operators (ISCO-08 group 8): 14,544
- Elementary occupations (ISCO-08 group 9): 13,032

---

## Tables NOT Yet Extracted (in subsequent chunks)
Per chapter TOC (p.397), the following tables are in chunk_013 or later:
- **Table 25.2**: Monthly avg gross wage and annual avg gross earnings by sex and educational attainment, 2006 and 2010 (p.405)
- **Table 25.3**: By sex and age group, 2006 and 2010 (p.406)
- **Table 25.4**: By sex and managerial responsibility, 2006 and 2010 (p.407)
- **Table 25.5**: Hourly labour cost index 2008–2012 (p.407) — **CRITICAL**
- **Table 25.6**: Hourly earnings index 2008–2012 (p.408) — **CRITICAL**
- **Table 25.7**: Hourly labour cost excluding earnings index 2008–2012 (p.408) — **CRITICAL**

---

## Relevance Assessment for ST2 / Compensation of Employees

**HIGH RELEVANCE:**
- Table 25.1: Formal Structure of Earnings Survey data for 2006 and 2010. Provides gross wages and earnings by occupation — this is the most rigorous wage measurement in the yearbook. Annual gross earnings are a close proxy for compensation of employees per worker.
- NOTE: Tables 25.5–25.7 (labour cost indices 2008–2012) are in chunk_013 and are CRITICAL — they would allow interpolation/extrapolation of wage levels for years 2008–2012.

**NOT RELEVANT to compensation:**
- Chapter 23 explanation pages — HBS methodology only, no tables in this chunk.

**Gap**: No 2007, 2008, 2009, 2011, or 2012 point-in-time wage level data from Structure of Earnings Survey (survey is only quadrennial: 2006 and 2010). The Labour Cost Index (tables 25.5–25.7, in next chunk) fills this gap by providing quarterly index from 2008 base year through 2012.
