# AS2/ST2 Data Wishlist — Downloads, HDARP, and Expansion

**Created**: 2026-05-03
**Purpose**: Complete inventory of all data sources to download, HDARP, or acquire for perfect replication and expansion of the AS2 project.

---

## Tier 0: Immediate Downloads (Free PDFs with Data Tables)

### 0A. Shaikh's Original IO & Capital Stock Data (Bard Digital Commons)
- **URL**: https://digitalcommons.bard.edu/as_archive/73/ (IO and K Stock Data)
- **Also**: https://digitalcommons.bard.edu/as_archive/116/ (Worksheets and Data)
- **Also**: https://digitalcommons.bard.edu/as_archive/115/ (IO/NIPA Notes)
- **Content**: Shaikh's original handwritten IO tables, capital stock matrices, BEA data files, and the actual worksheets used to produce the book's results
- **Impact**: Definitive validation — compare our computed values against Shaikh's own spreadsheets

### 0B. Paitaridis & Tsoulfidis (2012) — US Unproductive Activities & Profit Rate
- **URL**: http://gesd.free.fr/paitara12.pdf (free PDF)
- **Content**: US productive/unproductive labor 1964-2007, rate of profit. Same ST methodology applied independently.
- **Impact**: Second independent US validation (alongside Mohun)

### 0C. Korea Study — Rieu & Park (2020) Working Paper
- **URL**: https://scholarworks.umass.edu/econ_workingpaper/244/ (UMass open access)
- **Content**: Korean productive/unproductive labor 1995-2015, industry-level surplus value rates
- **Impact**: 6th country added to cross-study comparison

### 0D. Mohun (2014) — Unproductive Labor US 1964-2010
- **URL**: https://simonmohun.com/Papers/RRPE2014_PuPlab_US.pdf
- **All publications**: https://simonmohun.com/smpublications.html
- **Content**: Extended Mohun exploitation data through 2010 (our N1401-N1404 only covers 1964-2001)
- **Impact**: Extends Mohun comparison by 9 years

### 0E. Brazil Study — Morrone, Marquetti, Miebach (2023)
- **URL**: https://repositorio.pucrs.br/dspace/bitstream/10923/26030/2/Productive_and_Unproductive_Sectors_Interactions_in_Brazil_A_Miyazawa_Analysis.pdf
- **Content**: Brazilian productive/unproductive sectors 2002-2014, Miyazawa IO analysis
- **Impact**: 7th country in cross-study comparison

### 0F. Mutlu & Tsoulfidis (2025) — 11 European Economies + USA
- **URL**: https://thenextrecession.wordpress.com/wp-content/uploads/2025/07/mutlu_tsoulfidis_falling-rate-of-profit-non-production-activities-and-stagnation-in-eleven-european-economies-and-the-usa-2.pdf
- **Content**: Productive/unproductive labor and profit rates for Austria, Belgium, Czech Republic, France, Germany, Italy, Netherlands, Portugal, Spain, UK, USA
- **Impact**: Expands cross-study comparison to potentially 18 countries

### 0G. Iran Study (2024) — Mapping Iran's National Accounts
- **URL**: https://www.tandfonline.com/doi/full/10.1080/00472336.2024.2384063
- **Content**: Iranian productive/unproductive labor 1986-2016, exploitation rate, profit rate
- **Impact**: 8th country; Middle Eastern comparison alongside Turkey

### 0H. Tsoulfidis et al. (2019) — US Unproductive Activities 1964-2015
- **URL**: https://ideas.repec.org/p/pra/mprapa/84035.html (MPRA open access)
- **Content**: Extended US unproductive activities through 2015
- **Impact**: Third independent US validation

---

## Tier 1: High-Value Downloads (Directly Improve Pipeline)

### 1A. Moos (2017) Full Paper PDF
- **URL**: https://scholarworks.umass.edu/econ_workingpaper/227/
- **Content**: Original paper with Figures 1-14 showing annual NSW data for cross-validation
- **Impact**: Definitive validation of Moos P21 replication

### 1B. BEA NIPA Guide (Complete Line Number Mapping)
- **URL**: http://piketty.pse.ens.fr/files/capitalisback/CountryData/USA/Methodo/NIPA%20Guide.pdf
- **Content**: Official BEA documentation mapping every line number in every NIPA table
- **Impact**: Fixes Moos P21 calibration (mean 0.023 → 0.011)

### 1C. Shaikh (2016) "Capitalism" on Archive.org
- **URL**: https://archive.org/details/capitalismcompet0000shai
- **Content**: 979-page book with extensive appendix data tables — profit rates, exploitation rates, value-price deviations through ~2011
- **Impact**: Cross-validates T506, T513 extensions for 1990-2011

### 1D. API Data Vintage Refresh
- **What**: Re-pull BLS CES, FRED TCU, BEA 6.2D from APIs
- **Impact**: Eliminates V15 WARNs, ensures 2025-vintage data

---

## Tier 2: HDARP Processing (Already Downloaded)

### 2A. TurkStat Statistical Indicators 1923-2011 (5.9MB)
- **File**: `Inputs/ExternalSources/Turkey2022/turkstat_statistical_indicators_1923_2011.pdf`
- **Extract**: GDP components, compensation of employees, national income breakdown
- **Estimated chunks**: ~70
- **Impact**: Proper Turkish labor share → N1602 converges toward -0.011

### 2B. TurkStat Yearbook 2012 (10.6MB)
- **File**: `Inputs/ExternalSources/Turkey2022/turkstat_yearbook_2012.pdf`
- **Extract**: Detailed budget by function, social security, employment, tax breakdown
- **Estimated chunks**: ~80+
- **Impact**: Cross-validates SBB Excel data

### 2C. Stats NZ Historical National Accounts (292KB)
- **File**: `Inputs/ExternalSources/Cronin2001/statsnz_national_accounts_historical.pdf`
- **Extract**: NZ GDP by industry, employment, compensation
- **Estimated chunks**: ~3-5
- **Impact**: Cross-validates Cronin Table 1

---

## Tier 3: New Papers to Download and Replicate

### 3A. Maniatis (2003) — Net Social Wage in Greece 1958-1995
- **URL**: https://www.researchgate.net/publication/24082522_The_net_social_wage_in_Greece_1958-95
- **Content**: Annual NSW/GDP for Greece, same ST methodology
- **Impact**: Greece becomes 4th NSW country

### 3B. Maniatis & Passas (2019) — NSW in 9 European Countries 1995-2015
- **URL**: https://www.researchgate.net/publication/323299775_The_net_social_wage_in_different_welfare_regimes
- **Content**: Annual NSW for 9 EU countries × 20 years
- **Impact**: Massive expansion of NSW cross-study comparison

### 3C. Missos (2021) — NSW in Greece During the Crisis
- **URL**: https://journals.sagepub.com/doi/abs/10.1177/0486613420930830
- **Content**: Updates Greek NSW through 2010s austerity
- **Impact**: Extends Greek series

### 3D. Guerrero (1992) — NSW in Spain 1870-1987
- **Content**: 117-year NSW series — longest historical
- **Impact**: Historical depth unprecedented

### 3E. Karahanoğulları (2009) — Marx's Value in Turkey 1988-2006
- **Content**: Turkish surplus value / variable capital data — needed for Figure 11 in Turkey paper
- **Impact**: Cross-validates Turkey exploitation rate

---

## Tier 4: Data for Pipeline Improvements

### 4A. BEA IO Benchmark Tables Post-1977 (SIC: 1982, 1987, 1992)
- **Where**: BEA historical benchmark IO tables at bea.gov
- **Impact**: T703 R² extends from 6 to 9 benchmark years

### 4B. BEA Fixed Assets by Industry
- **Where**: BEA API (Table 3.1ES)
- **Impact**: Proper K* for profit rate (DEC-010)

### 4C. BLS CES Pre-1998 Industry Compensation
- **Where**: BLS archives
- **Impact**: Fills SIC-NAICS gap for ec_u/ec_p (DEC-007)

### 4D. KLEMS 2024 Update
- **Where**: BLS KLEMS database
- **Impact**: Data freshness for T504 cross-validation

---

## Country Coverage After Full Implementation

| # | Country | Study | Period | Variables |
|---|---------|-------|--------|-----------|
| 1 | USA | Shaikh & Tonak (1994) | 1948-2024 | Full ST framework |
| 2 | USA | Mohun (2005, 2013) | 1964-2010 | Alternative classification |
| 3 | USA | Moos (2017) | 1959-2024 | NSW independent |
| 4 | USA | Paitaridis & Tsoulfidis (2012) | 1964-2007 | Profit rate + unproductive |
| 5 | USA | Tsoulfidis et al. (2019) | 1964-2015 | Extended unproductive |
| 6 | Turkey | Karabacak & Tonak (2022) | 1980-2019 | NSW |
| 7 | New Zealand | Cronin (2001) | 1972-1995 | Full ST framework |
| 8 | Greece | Maniatis (2003) | 1958-1995 | NSW |
| 9 | Greece | Missos (2021) | 1995-2019 | NSW crisis |
| 10 | Korea | Rieu & Park (2020) | 1995-2015 | Industry exploitation |
| 11 | Iran | (2024) | 1986-2016 | Full ST framework |
| 12 | Brazil | Morrone et al. (2023) | 2002-2014 | IO Miyazawa |
| 13 | Spain | Guerrero (1992) | 1870-1987 | NSW historical |
| 14-24 | 11 EU | Mutlu & Tsoulfidis (2025) | varies | Profit rate + unproductive |
| 25 | 9 EU | Maniatis & Passas (2019) | 1995-2015 | NSW comparative |

**Potential: 25+ country-studies spanning 1870-2025**

---

*Last updated: 2026-05-03*
