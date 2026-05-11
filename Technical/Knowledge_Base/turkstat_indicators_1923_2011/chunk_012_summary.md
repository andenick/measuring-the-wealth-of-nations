# chunk_012 Summary
**Document**: turkstat_indicators_1923_2011 (TurkStat Statistical Indicators 1923–2011)
**PDF Pages**: 379–388 (book pagination)
**Topics**: Table 11.42 (continued, final pages) + Table 11.43 (new table begins)

## Content Overview
This chunk contains two distinct tables:
1. **Pages 379–386**: Final sub-tables of Table 11.42 — social security contributions, purchase of goods & services, production value, and value added at factor cost for financial intermediary institutions (2002–2010).
2. **Pages 387–388**: Beginning of Table 11.43 — Number of broadcasting institutions and employment (1995–1999).

---

## Table 11.42 Sub-Tables (Continued)

### Table 1 — Contributions to Social Security (Sosyal guvenlik masraflari)
- Total K: 428.9M TL (2002) → 1,838.2M TL (2010)
- Monetary intermediation: 290.6M → 1,405.8M TL

### Table 2 — Purchase of Goods and Services (Mal ve hizmet satin alisi)
- Total K: 7.74B TL (2002) → 21.06B TL (2010)
- Note: Insurance sector (NACE 65) shows dramatic jump in 2006 (non-life insurance purchases up ~2.3x) reflecting market expansion

### Table 3 — Production Value (Uretim degeri)
- Total K: 20.31B TL (2002) → 74.90B TL (2010)
- Monetary intermediation (64.11+64.19): 14.73B → 56.26B TL
- Note: 2009 values unusually high vs 2010 for banking sector, suggesting methodological or valuation shift

### Table 4 — Value Added at Factor Cost (Faktor maliyetiyle katma deger)
- Total K: 12.57B TL (2002) → 53.84B TL (2010)
- Monetary intermediation: 8.90B → 43.52B TL
- **KEY SERIES FOR LABOR SHARE**: Combined with wages & salaries / personnel cost from chunk_011, these value-added figures enable labor share computation for NACE K subsectors (2002–2010)

#### Implied labor share (wages+salaries / value added at factor cost), sector K total:
| Year | Wages & Salaries (TL) | Value Added (TL) | Labor Share |
|------|----------------------|------------------|-------------|
| 2002 | 3,402,570,505 | 12,571,660,625 | 27.1% |
| 2004 | 5,129,396,082 | 19,525,187,087 | 26.3% |
| 2006 | 7,118,871,157 | 29,254,357,418 | 24.3% |
| 2008 | 10,582,237,180 | 32,262,900,621 | 32.8% |
| 2010 | 12,911,586,177 | 53,837,498,991 | 24.0% |

---

## Table 11.43 — Broadcasting Institutions: Number and Employment (1995–1999)
Coverage: Radio, Radio-Television combined, Television; by broadcasting type A/B/C/D

### Key totals (all types, A):
| Year | Institutions | Avg Employees | Avg Persons Engaged |
|------|-------------|---------------|---------------------|
| 1995 | 1,448 | 19,224 | 19,974 |
| 1996 | 1,189 | 17,735 | 18,853 |
| 1997 | 1,453 | 21,942 | 23,050 |
| 1998 | 1,852 | 25,219 | 25,912 |
| 1999 | 1,545 | 21,084 | 21,766 |

### National (B) totals:
| Year | Institutions | Avg Employees |
|------|-------------|---------------|
| 1995 | 36 | 8,748 |
| 1996 | 40 | 9,028 |
| 1997 | 40 | 9,757 |
| 1998 | 72 | 9,738 |
| 1999 | 40 | 9,778 |

## Relevance to ST2 NickyData Extraction Focus
- **Value added + compensation data** in Tables 1–4 of 11.42 are directly relevant for constructing **labor share in financial services** (NACE K), a sectoral component of economy-wide labor share.
- Value added at factor cost for banking (64.11+64.19) is directly usable as a proxy for financial sector GVA contribution.
- Table 11.43 (broadcasting employment) has lower relevance to the core national accounts / labor share focus but provides NACE J-adjacent service sector employment data.
- No economy-wide GDP/GSYH series in this chunk.

## CSV Files Written
- `chunk_012_table01_financial_intermediaries_social_security_contributions.csv`
- `chunk_012_table02_financial_intermediaries_purchase_goods_services.csv`
- `chunk_012_table03_financial_intermediaries_production_value.csv`
- `chunk_012_table04_financial_intermediaries_value_added_factor_cost.csv`
- `chunk_012_table05_broadcasting_institutions_employment.csv`

## Data Quality Notes
- Value added figures show volatility in insurance subsectors (65.12+65.20) 2005–2008, likely reflecting reinsurance premium flows and natural disaster events
- Financial leasing (64.91) shows anomalous drop in production value 2005 (494M vs 957M in 2004) — likely reclassification
- Broadcasting table 11.43 covers years 1995–1999 in this chunk; continuation in subsequent chunks
- Units: employment = persons; monetary values = Turkish Lira (current, nominal)
