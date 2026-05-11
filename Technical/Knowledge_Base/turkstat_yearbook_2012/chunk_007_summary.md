# chunk_007 Summary — turkstat_yearbook_2012

## Source pages: 235–246
## Chapter: 13 — İş İstatistikleri / Business Statistics

---

## Relevance to ST2 NickyData extraction focus

This chunk contains **no direct national accounts / GDP / compensation of employees data**. It covers business survey indices (turnover, employment, hours worked, wages) for industry, trade & services, and construction — all indexed to 2010=100. These are **sector-level wage and employment indices**, not SNA compensation-of-employees aggregates, but they are **closely related supporting series** for labour share analysis.

Key relevant tables:

- **Table 13.7** — Industrial employment index (2008–2012): Total manufacturing employment index peaks at 111.6 in 2012 vs 100.0 in 2010.
- **Table 13.8** — Industrial hours worked index (2008–2012): Closely tracks employment index.
- **Table 13.11** — Trade & Services employment index (2008–2012): 110.0 in 2012.
- **Table 13.13** — **Trade & Services gross wages and salaries index (brüt ücret-maaş endeksi)**: Most directly relevant wage series. Total T&S: 84.0 (2008) → 100.0 (2010) → 135.0 (2012). Strong wage growth 2010–2012.
- **Table 13.20** — **Construction sector gross wages and salaries index**: Total construction: 86.3 (2008) → 87.3 (2010) → 118.1 (2012). Also directly relevant.

---

## Tables extracted (13 CSV files)

| File | Table | Description |
|------|-------|-------------|
| chunk_007_table01 | 13.6 | Industrial turnover index 2008-2012 (2010=100) — 36 NACE rows |
| chunk_007_table02 | 13.7 | Industrial employment index 2008-2012 (2010=100) — 38 rows |
| chunk_007_table03 | 13.8 | Industrial hours worked index 2008-2012 (2010=100) — 38 rows |
| chunk_007_table04 | 13.10 | Trade & Services turnover index 2008-2012 (2010=100) — 32 rows |
| chunk_007_table05 | 13.11 | Trade & Services employment index 2008-2012 (2010=100) — 32 rows |
| chunk_007_table06 | 13.12 | Trade & Services hours worked index 2008-2012 (2010=100) — 32 rows |
| chunk_007_table07 | 13.13 | **Trade & Services gross wages & salaries index 2008-2012** — 32 rows |
| chunk_007_table08 | 13.14 | New buildings by investor type 2008-2012 (A/B/C/D metrics) |
| chunk_007_table09 | 13.16 | Completed buildings by storeys 2008-2012 |
| chunk_007_table10 | 13.17 | Completed dwellings by number of rooms 2008-2012 |
| chunk_007_table11 | 13.18 | Completed buildings avg floor area and cost 2008-2012 |
| chunk_007_table12 | 13.19 | **Construction employment index 2008-2012** (2010=100) |
| chunk_007_table13 | 13.20 | **Construction gross wages & salaries index 2008-2012** (2010=100) |

---

## Key data points (wage-related, for ST2 context)

### Trade & Services gross wages & salaries index (Table 13.13, 2010=100)
- Total: 84.0 (2008) | 88.3 (2009) | 100.0 (2010) | 117.5 (2011) | **135.0 (2012)**
- Wage growth 2010–2012: +35.0%
- Wage growth 2008–2012: +60.7%

### Construction gross wages & salaries index (Table 13.20, 2010=100)
- Total: 86.3 (2008) | 81.4 (2009) | 87.3 (2010) | 101.3 (2011) | **118.1 (2012)**
- Note: 2010 base value is 87.3, not 100.0 — this table uses a different normalisation scheme
- Wage growth 2010–2012 (from reported base): +35.3%

### Industrial employment index (Table 13.7, 2010=100)
- Total manufacturing: 105.8 (2008) → 95.4 (2009, crisis dip) → 100.0 (2010) → 112.2 (2012)

---

## Notes / caveats
- All business statistics indices use 2010=100 (except Table 13.22 construction turnover which uses 2005=100)
- These are **index series**, not absolute TL values — cannot directly compute wage levels without anchor year data
- Coverage is **registered/formal sector enterprises** meeting survey thresholds
- 2011* and 2012* data in construction permits tables are preliminary
- Tables 13.9 (industry gross wages) and 13.15 (construction permits continued) appear to be on pages not included in this chunk (pp. 238, 244)
