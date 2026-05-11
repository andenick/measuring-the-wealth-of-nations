# DEC-012 Verification Report: No Synthetic Data Compliance

**Date**: 2026-05-06
**Standard**: DEC-012 — Prohibition of synthetic/random data generation in production series
**Scope**: Formerly-synthetic series clusters N1001/N1002, N1601/N1602, N1701-N1704
**Result**: PASS — No violations found

---

## Cluster 1: N1001/N1002 (Tonak 1984)

**Processing script**: `code/processing/P20_process_remaining_chapters.py`

**Findings**:
- No `np.random`, `random.`, `synthetic`, `seed()`, or equivalent calls present in P20.
- N1001 is computed as `labor_taxes / total_taxes` from `table_V_taxes_labor_nonlabor_1952_1980.csv`.
- N1002 is computed as `net_tax / taxes_paid_by_labor` from `table_X_net_tax_1952_1980.csv`.
- All three required source CSVs confirmed present on disk:
  - `D:\Arcanum\Projects\ST2\Inputs\ExternalSources\Tonak1984\table_V_taxes_labor_nonlabor_1952_1980.csv`
  - `D:\Arcanum\Projects\ST2\Inputs\ExternalSources\Tonak1984\table_X_net_tax_1952_1980.csv`
  - `D:\Arcanum\Projects\ST2\Inputs\ExternalSources\Tonak1984\table_IX_benefits_labor_1952_1980.csv`
- Code path: reads from CSV, computes ratio — no fallback synthetic generation.
- If CSVs are missing the script logs `data_unavailable` and skips, it does not generate placeholder data.

**DEC-012 Status**: COMPLIANT

---

## Cluster 2: N1601/N1602 (Turkey)

**Processing script**: `code/processing/P18_process_turkey_nsw.py`

**Findings**:
- No `np.random`, `random.`, `synthetic`, `seed()`, or equivalent calls present in P18.
- N1601 (labor share): loaded exclusively from `turkstat_compensation_labor_share_1980_2006.csv` via HDARP extraction. The loop `for yr in range(1980, 2020)` only assigns values where `yr in turkstat_ls.index`; years 2007-2019 receive no assignment and remain NaN, consistent with DEC-012 intent.
- Source CSV confirmed present: `data/raw-data/parsed/turkstat_compensation_labor_share_1980_2006.csv`
- N1602 (NSW/GDP): derived from SBB consolidated budget and World Bank fiscal data combined with real labor share. The `np` import is used only for `np.nan` checks and `np.isnan()` guards — not for random generation.
- If TurkStat data is missing, the function returns `data_unavailable` with an empty dict (no synthetic fill).

**DEC-012 Status**: COMPLIANT
**NaN gap confirmed**: 2007-2019 entries for N1601 produce no values (not filled with synthetic estimates).

---

## Cluster 3: N1701-N1704 (Cronin 2001, New Zealand)

**Processing script**: `code/processing/P20_process_remaining_chapters.py` (same file as Cluster 1)

**Findings**:
- No `np.random`, `random.`, `synthetic`, `seed()`, or equivalent calls present in P20.
- All four series read directly from paper tables encoded as CSV:
  - N1701: `surplus_share_of_total_value_pct` from `cronin_table2_ratios_1972_1995.csv`
  - N1702: `rate_of_surplus_value_pct` from `cronin_table2_ratios_1972_1995.csv`
  - N1703: `value_composition_of_capital_pct` from `cronin_table2_ratios_1972_1995.csv`
  - N1704: `total_value_mNZD` from `cronin_table1_nzsna_classical_1972_1995.csv`
- Both required source CSVs confirmed present on disk:
  - `D:\Arcanum\Projects\ST2\Inputs\ExternalSources\Cronin2001\cronin_table2_ratios_1972_1995.csv`
  - `D:\Arcanum\Projects\ST2\Inputs\ExternalSources\Cronin2001\cronin_table1_nzsna_classical_1972_1995.csv`
- Additional supporting sources also present: World Bank NZ national accounts, FRED NZ GDP, StatsNZ historical PDF, NZ fiscal time series XLSX.
- If CSVs are missing the script logs `data_unavailable` and produces no output.

**DEC-012 Status**: COMPLIANT

---

## Summary Table

| Series   | Source                          | np.random | Synthetic fallback | Source CSV present | DEC-012 |
|----------|---------------------------------|-----------|-------------------|--------------------|---------|
| N1001    | Tonak1984 Table V (HDARP CSV)   | None      | None              | YES                | PASS    |
| N1002    | Tonak1984 Table X (HDARP CSV)   | None      | None              | YES                | PASS    |
| N1601    | TurkStat Table 20.37 (HDARP CSV)| None      | None (NaN gap)    | YES                | PASS    |
| N1602    | SBB + World Bank fiscal CSVs    | None      | None              | YES (if data avail)| PASS    |
| N1701    | Cronin 2001 Table 2 CSV         | None      | None              | YES                | PASS    |
| N1702    | Cronin 2001 Table 2 CSV         | None      | None              | YES                | PASS    |
| N1703    | Cronin 2001 Table 2 CSV         | None      | None              | YES                | PASS    |
| N1704    | Cronin 2001 Table 1 CSV         | None      | None              | YES                | PASS    |

**Overall result: All 8 series are DEC-012 compliant. No synthetic data generation detected.**
