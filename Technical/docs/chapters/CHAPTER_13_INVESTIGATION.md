# Chapter 13 Investigation: Moos (2017) — Neoliberal NSW 21st Century

## Paper Metadata

| Field | Value |
|-------|-------|
| Author | Katherine A. Moos |
| Title | Neoliberal Redistributive Policy: The U.S. Net Social Wage in the 21st Century |
| Year | 2017 |
| Type | Working Paper 2017-18, UMass Amherst |
| Period | 1959-2012 (54 years) |
| DOI | N/A (working paper) |
| HDARP Location | `external_papers/state_welfare/2017_Moos_NSW_21st_Century/` |

## Significance

This is the most important external paper because it discovers the **dramatic structural shift** in the US Net Social Wage after 2000:
- **1959-2000**: Mean NSW ≈ 0% of GDP (consistent with Shaikh-Tonak)
- **2001-2012**: Mean NSW ≈ 5% of GDP (unprecedented positive shift)
- **2010 peak**: NSW = 8.6% of GDP, 16.1% of employee compensation

This challenges the Shaikh-Tonak thesis that workers are net subsidizers of the state — at least in the 21st century, the direction reversed.

## Series to Replicate

| ID | Name | Formula | Period |
|----|------|---------|--------|
| N1301 | NSW/GDP (Moos) | NSW / GDP | 1959-2012 |
| N1302 | NSW/EC (Moos) | NSW / Employee Compensation | 1959-2012 |
| N1303 | Unemployment Intensity | U_rate x avg_duration | 1959-2012 |
| N1304 | Moos vs ST Validation | Moos NSW vs ST94 NSW for overlap | 1959-1997 |
| N1305 | Post-2000 Shift | NSW trend break indicator | 2000-2012 |

## Methodology (from HDARP extraction)

### NSW Formula (Moos version)
```
NSW = (Social Insurance Benefits + Medicare + Medicaid + Other transfers)
    + (Education expenditure allocated to workers)
    + (Infrastructure allocated to workers)
    - (Personal income taxes allocated to workers)
    - (Social insurance contributions)
    - (Sales and excise taxes allocated to workers)
```

### Key Methodological Differences from ST94

1. **Medicare/Medicaid**: Moos includes these as worker benefits (post-1965)
2. **ACA Impact**: 2010+ includes Affordable Care Act transfers
3. **Allocation Method**: Uses labor share for mixed expenditures (same as ST94)
4. **Unemployment Intensity**: Novel metric = unemployment rate x average duration

### Data Sources Required

| NIPA Table | Content | For Series |
|-----------|---------|-----------|
| Table 2.1 | Personal income, compensation | N1301, N1302 |
| Table 3.1 | Government receipts & expenditures | N1301 |
| Table 3.2 | Federal government detail | N1301 |
| Table 3.3 | State/local government detail | N1301 |
| GDP | Gross domestic product | N1301 denominator |
| BLS | Unemployment rate and duration | N1303 |

All available in Robin BEA module and existing `Inputs/API_Data/BEA/`.

## Benchmark Values (from HDARP Tables 1-3)

### Table 1: Comparison with ST94 (1959-1997)
| Statistic | ST94 Original | Moos Replication |
|-----------|--------------|-----------------|
| NSW/GDP Min | ~-1.2% | -1.2% |
| NSW/GDP Median | ~1.3% | 1.3% |
| NSW/GDP Mean | ~2.0% | 2.0% |
| NSW/GDP Max | ~5.0% | 5.0% |

### Table 2: Full Period (1959-2012)
| Statistic | Value |
|-----------|-------|
| Min | -1.2% GDP |
| Median | 1.3% GDP |
| Mean | 2.0% GDP |
| Max | 8.6% GDP (2010) |

### Table 3: Recession Peaks
| Year | NSW/GDP | Unemployment Intensity |
|------|---------|----------------------|
| 1983 | 4.8% | 9.6% rate, 20.06 weeks avg |
| 2010 | 8.6% | 9.6% rate, 33.0 weeks avg |

## Cross-Validation Plan

1. Compare N1301 with T607/GDP for 1959-1989 overlap
2. Compare N1304 (Moos replication of ST) with original ST94 values
3. Verify 2010 peak matches Table 2 benchmark (8.6%)
4. Check unemployment intensity against BLS FRED data

## Implementation Plan

1. Extract data values from HDARP transcription tables
2. Create L## script to load/compute NSW components from NIPA
3. Create P## script to compute all 5 series
4. Validate against HDARP benchmark values
5. Generate cross-study comparison with T607-T609
