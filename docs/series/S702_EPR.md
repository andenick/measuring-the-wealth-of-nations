# EPR: S702 — Prices of Production (real, sector-disaggregated)

**Series**: S702
**Generated**: 2026-05-24T06:00:00Z (v1.1 Phase 4 iteration 5 Ch7 real-fix)
**Status**: validated_book_and_extension
**Supersedes**: prior `EXTENSION NOT APPLICABLE` stub (v1.0 iteration 9), authored when S702 was a `S701_proxy × (1 + r*)` scalar with `extension: null`. v1.1 Phase 4 retires the proxy and populates a real extension arm.

## 1. shaikh_source

> "For aggregate money value calculations, this is adequate because we are only interested in the sum of money values. But for labor value calculations, we generally need to know the individual elements of the productive sectors. Therefore we may also think of the production-row elements in Figure 4.1 as matrices representing corresponding partitions of the matrix pictured in Figure 3.11." (Shaikh & Tonak 1994, Ch. 4 §4.1, p. 79)

> "Since the lambda_j*'s are ratios of labor values to producer prices, we must be careful to apply them only to the producer-price components of commodity flows. Thus the labor value of productive inputs C is derived by multiplying the producer price of the ith input by the labor-value/producer-price ratio lambda_i*. In terms of Figure 4.1, this means that the matrix of constant capital is calculated by multiplying only the matrix of elements (M_p)_p by lambda*." (S&T 1994, Ch. 4 §4.1, p. 81)

> "The same issue arises in the calculation of the labor value of productive labor power V. Given some estimate of the consumption basket of production workers CONW_p, the labor value of this is the labor-value/producer-price ratio vector lambda* multiplied only by the producer price component (CONW_p)_p." (S&T 1994, Ch. 4 §4.1, pp. 81–82)

Source: Shaikh & Tonak (1994), *Measuring the Wealth of Nations*. Cambridge University Press. The classical formula `pp*_j = (1 + r_bar)(c_j_labor + v_j_labor)` is implemented sector-by-sector for the first time in v1.1 Phase 4, with sector `c_j` and `v_j` constructed via the matrix products quoted above.

## 2. shaikh_appendix_ref

Primary methodology: **Chapter 4 §4.1**, pp. 78–88 (sector-disaggregated c, v construction; Figure 4.1 productive-row matrix partition).
Variable capital: **Appendix G** Tables G.1 (variable capital methodology), G.2 (sectoral productive-employment definitions).
Constant capital decomposition: **Appendix E** Tables E.1 (`C* = M'_p + Dp` annual 1948–1989), E.2 (sectoral GVA / constant capital).
Profit-rate equalization: ST 1994 §5.5 (three profit-rate measures including the uniform `r_bar`), supplies S513 input.
Empirical anchor: **Ch. 7 §7.3**, p. 223 (Khanjian 6–9% S*/V* benchmark — measurable for the first time once both S701 and S702 are real and sector-disaggregated).
Registry `book_table='7.2'` is a project-internal label, not a literal book table.

## 3. extension_source

**Four feed-in sources, all real-data, all v1.1 Phase 4**:

1. **Real S701 lambda* vector** — sector-disaggregated labor-value/producer-price ratios (hr/$), output of `Technical/code/P02_processors/P02_S701_labor_values.py` (v1.1 rewrite). This is the load-bearing input both `c_j = lambda_i* * (M_p)_p,ij` and `v_j = lambda* * (CONW_p)_p,j` depend on.

2. **BLS CES production-worker compensation** — for `(CONW_p)_j` (consumption basket / wage bill of production workers per sector). Average hourly earnings + employment + weekly hours from `data/raw/bls/`, pulled 2026-05-24.

3. **BEA NIPA employee compensation tables** — for the EC/WS ratio `x_j` (compensation per wage-and-salary worker) used to scale BLS production-wage to total compensation per ST 1994 Appendix G methodology. Cached at `data/raw/bea/`, pulled 2026-02-24.

4. **Labeled BEA IO matrices** — for `(M_p)_p,ij` (producer-price component of input flows from sector i to sector j). Cached at `Technical/data/intermediate/io_matrices_labeled/`. Appendix F productive-share filter `Technical/data/source/appendix_F/Table_F_1.csv` masks unproductive sectors before the matrix products.

Profit rate `r_bar` from S513 Marxian profit rate (already real, no proxy). Construction per `Technical/code/P02_processors/P02_S702_prices_of_production.py` (v1.1 rewrite): per benchmark year, compute `c_j_labor` and `v_j_labor` via the Ch4 §4.1 matrix products on the productive sub-matrix, then `pp*_j = (1 + r_bar) * (c_j_labor + v_j_labor)`.

## 4. extension_url

BLS Public API v2: `https://api.bls.gov/publicAPI/v2/timeseries/data/` (CES series for employment, weekly hours, average hourly earnings per supersector).

BEA API:
- NIPA employee compensation: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=NIPA&TableName=T10604&Frequency=A&Year=ALL&ResultFormat=JSON` (Table 6.4 wages & salaries by industry)
- NIPA gross output: `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=NIPA&TableName=T10705&Frequency=A&Year=ALL&ResultFormat=JSON`
- GDP-by-Industry intermediate-input flows (input to (M_p)_p reconstruction): `https://apps.bea.gov/api/data?UserID=<KEY>&method=GetData&datasetname=GDPbyIndustry&TableID=8&Industry=ALL&Year=ALL&Frequency=A&ResultFormat=JSON`

BEA IO benchmark archive: https://www.bea.gov/industry/input-output-accounts-data

## 5. conceptual_continuity

`pp*_j = (1 + r_bar)(c_j_labor + v_j_labor)` is a derived (formula-type) quantity — sector constant and variable capital in labor-value units, times one plus the uniform rate of profit. The book period and the extension period compute the same formula on extended sector-disaggregated data; the SIC → NAICS junction is the only methodological change, handled by re-mapping the productive-share filter and the (M_p)_p matrix to NAICS sectors per the BEA IO benchmark concordance. Because the construction is formula-type (per Anu rule "No Lazy Splices on Derived Quantities"), an extension growth-rate splice would be invalid; instead, the extension recomputes the formula from extended BLS + BEA + IO components. Methodological consistency book ↔ extension: identical (same Ch4 §4.1 c_j and v_j matrix products, same profit-rate equalization, same Khanjian (1989) empirical anchor in S703).

## 6. vintage_note

Book values (six SIC benchmark years 1947–1977) computed from BEA SIC-basis benchmark IO tables + NIPA + BLS CES, all at book vintage (published 1947–1981). Extension years (1997+ NAICS benchmark years) computed from BEA NAICS data pulled 2026-02-24 (approximately September 2025 NIPA vintage) and BLS CES pulled 2026-05-24. The 1990–1996 SIC–NAICS junction is not interpolated; only benchmark years on each side are reported. BLS CES 2003 overhaul affects extension arm: DIV-010 ships v1.1 null-bridge factors (=1.0 per supersector) with a v1.2 follow-up to source non-null factors from the BLS Employment Situation news-release archive. BEA comprehensive revisions (1999, 2003, 2009, 2013, 2018) alter post-1997 values relative to book; pre-1997 book values frozen.
