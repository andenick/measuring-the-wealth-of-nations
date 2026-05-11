# Chunk 006 Summary — TurkStat Statistical Indicators 1923–2011

## Pages covered
Book pages 251–273 (document section pages)

## Section coverage
Entirely within **Section 11 (Industry and Business Statistics)**:
- Methodological explanation pages for Annual Business Statistics, Annual Industry and Service Statistics, and Annual Industrial Products Statistics (PRODCOM)
- Numerical tables: Manufacturing industry private sector (11.3), Rate of change (11.4), Food/beverage/tobacco (11.5), Other manufacturing (11.13)

---

## Tables extracted

### Table 11.3 (p.263) — Manufacturing industry, private sector
- Series: 1950–2001
- Variables per year:
  - Number of establishments
  - Annual average number of employees (ücretle çalışanlar)
  - Annual average number of persons engaged (çalışanlar)
  - Annual payments to employees / wages (ücretle çalışanlara yapılan yıllık ödemeler) — Million TL
  - Input (Million TL)
  - Output (Million TL)
  - Value added / Katma değer (Million TL)
- **This is HIGHLY RELEVANT**: Contains annual wage payments to employees in manufacturing (private sector) 1950–2001 in current Million TL.
- **CSV**: `chunk_006_table01_manufacturing_private_sector.csv`

### Table 11.4 (p.264) — Annual rate of change in manufacturing: establishments, employment, wages, value added
- Series: 1951–2001
- Variables: % change in establishments, employment, wages, value added
- **Relevant for verifying wage growth rates** — notably large nominal wage growth: 67.6% (1980), 94.3% (1990), 107.2% (1989), 111.1% (1997)
- **CSV**: `chunk_006_table02_manufacturing_annual_rate_of_change.csv`

### Table 11.5 (p.265) — Food, beverage and tobacco industries
- Series: 1950–2001
- Same structure as Table 11.3: establishments, persons engaged, wage payments, input, output, value added
- Unit: Million TL
- **CSV**: `chunk_006_table03_food_beverage_tobacco_industry.csv`

### Table 11.13 (p.273) — Other manufacturing industries
- Series: 1950–2001
- Same structure as Tables 11.3 and 11.5
- Unit: Million TL
- **CSV**: `chunk_006_table04_other_manufacturing_industry.csv`

---

## Methodological pages (no numerical tables)

### pp.251–256: Annual Business Statistics / Annual Industry and Service Statistics
- Analytical framework: EU Council regulations 58/97 and 295/2008
- NACE Rev.1.1 (2002–2008) and NACE Rev.2 (2009+) sectoral coverage
- Excluded: Agriculture, Financial & Insurance (NACE K), Public Administration
- Key definitions provided (bilingual TR/EN):
  - **Wages and salaries** (Maaş ve ücretler): total remuneration in cash or kind, gross of income tax and employee social security contributions, excluding employer social security contributions
  - **Personnel cost** = gross wages + employer social security contributions
  - **Value-added at factor cost** = gross income from operations after adjusting for subsidies and indirect taxes
  - **Number of employees** (ücretli çalışanlar): persons with employment contract receiving compensation
  - **Number of persons engaged** (çalışanlar): employees + working owners + unpaid family workers

---

## Relevance to ST2 NickyData extraction focus

### STRONG relevance — manufacturing wages data
- Table 11.3 provides **annual wage payments to employees** in manufacturing private sector 1950–2001 in current TL. This is sectoral compensation data (not national accounts aggregate) but highly useful for labour share analysis.
- Table 11.4 provides **annual % change in wages** — usable to cross-check or extend the series.
- The manufacturing wage data covers a long run (1950–2001) and is clearly labelled.

### Caveats / scope limitations
- This is **manufacturing sector only** (private sector establishments with 10+ employees), not economy-wide national accounts compensation of employees.
- Coverage criterion changed over time: 10+ employees (pre-1983), 25+ with separate simplified form for 10–24 (1983–1993), uniform 10+ (1993–2002).
- Values are in **current (nominal) Million TL** — need deflation for real series.
- Series ends at 2001 in this chunk. Subsequent years may appear in later chunks.
- No GDP / GSYH data in this chunk.
