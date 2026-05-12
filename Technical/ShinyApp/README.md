# Shaikh-Tonak Marxian Analysis Shiny App

Interactive visualization of Marxian economic indicators for the United States, 1948-1989, based on Shaikh & Tonak (1994) *Measuring the Wealth of Nations*.

## Overview

This Shiny application provides interactive exploration of:
- **Profit rates** (Marxian vs conventional measures)
- **Exploitation rates** and capital composition
- **Employment** trends (productive vs unproductive labor)
- **Productivity** comparisons (Marxian vs conventional)
- **Government absorption** of surplus
- **Cross-validation** against Table 5.8 benchmarks from the original book

**Dataset:** 42 years of annual data (1948-1989)
**Data sources:** BEA NIPA, BLS
**Methodology:** Marxian categories derived from national accounts using Mohun conservation principle

---

## Quick Start

### Option 1: Automated Setup (Recommended)

```r
# 1. Navigate to the ShinyApp directory
setwd("")

# 2. Check and install required packages
source("check_packages.R")

# 3. Validate data files
source("validate_data.R")

# 4. Launch the app
shiny::runApp()
```

The app will open in your default web browser at `http://127.0.0.1:####`

### Option 2: Manual Setup

**Required packages:**
- shiny
- shinydashboard
- tidyverse (dplyr, ggplot2, readr, tidyr)
- plotly
- DT
- scales
- openxlsx (optional, for Excel exports)

**Installation:**
```r
install.packages(c("shiny", "shinydashboard", "tidyverse", "plotly",
                   "DT", "scales", "openxlsx"))
```

**Launch:**
```r
shiny::runApp("")
```

---

## Application Structure

### Tab 1: Overview Dashboard
- Summary statistics (value boxes)
- Main profit rate trend plot
- Key trends table (1948 vs 1989)
- About section with methodology notes

### Tab 2: Explore by Question ✅ NEW!
- **30 comprehensive questions** organized by category and priority
- Interactive question cards with hover effects
- **Rich modal dialogs** with:
  - Detailed answer and explanation
  - Mathematical formulas in styled boxes
  - Category-specific visualizations
  - Book references from Shaikh & Tonak (1994)
- **Smart filtering** by priority (CRITICAL/HIGH/MEDIUM/LOW) and category
- **One-click navigation** to relevant analysis tabs
- Categories covered:
  - Profit Rate (8 questions)
  - Surplus Value & Exploitation (7 questions)
  - Employment & Productive Labor (6 questions)
  - Capital Composition (5 questions)
  - Data & Methodology (3 questions)
  - Government Absorption (1 question)

### Tab 3: Profit Rate Analysis
- Multi-series comparison:
  - Marxian r* (S*/K)
  - Marxian r* (capacity-adjusted)
  - NIPA r (conventional)
  - NIPA r (capacity-adjusted)
- Interactive series selection
- Descriptive statistics table
- Recession period shading

### Tab 4: Exploitation & Composition ✅
- Exploitation rate (S*/V*) and surplus ratio (S*/Y) dual y-axis plot
- Value composition (C*/V*) and materialized composition trends
- Decade aggregation table with averages and ranges
- 4 value boxes showing current metrics and trends
- Collapsible explanation box with theoretical notes

### Tab 5: Employment Analysis ✅
- Employment composition plot (Lp/L vs Lu/L shares)
- Stacked area chart of absolute employment levels
- Productivity comparison (Marxian Y/Lp vs Conventional Y/L vs BLS)
- Statistics table with mean, 1948, and 1989 values
- 4 value boxes for total employment, productive share, trend, and productivity growth

### Tab 6: Government Absorption ✅
- Government absorption ratios (G/S* and G/GDP) over time
- Federal vs State/Local stacked area expenditure breakdown
- Decade statistics table with averages
- 4 value boxes for current spending, ratios, and growth
- Theoretical explanation of Marxian treatment of government

### Tab 7: Validation Center
- Cross-validation against Shaikh-Tonak Table 5.8 benchmarks
- Scatter plot: calculated vs target values
- Deviation table with benchmark years (1948, 1964, 1970, 1980, 1989)
- Known discrepancies documented transparently

### Tab 8: Literature Navigator ✅
- Primary reference display (Shaikh & Tonak 1994)
- Methodological documentation (data sources, key steps)
- Related literature (Mohun, Basu, Kliman)
- Knowledge base extraction links
- Citation guide (APA format, BibTeX)

### Tab 9: Data Downloads ✅
- 7 individual CSV download buttons (profit rates, exploitation, employment, etc.)
- Filtered data export with year range selection
- Multiple format support: CSV, Excel multi-sheet, RData
- Codebook download (TXT format with variable definitions)
- Excel exports include metadata sheet
- RData exports include all filtered datasets + metadata object

---

## Global Controls

**Year Range Slider** (sidebar)
- Adjust the time period displayed across all tabs
- Default: 1948-1989 (full period)

**Show Recession Periods** (sidebar checkbox)
- Toggle recession shading on profit rate plots
- Based on NBER recession dates

---

## Data Files

The app loads 8 preprocessed CSV files from the `data/` directory:

1. **profit_rates_1948_1989.csv** (5.9 KB)
   - r_star_pct, r_star_adj_pct, r_nipa_pct, r_nipa_adj_pct
   - capacity_utilization, S_star, K, GDP

2. **exploitation_composition_1948_1989.csv** (5.9 KB)
   - exploitation_rate, surplus_ratio
   - value_composition, materialized_composition
   - S_Y, V_Y, C_Y

3. **employment_1948_1989.csv** (3.7 KB)
   - L_total, Lp_productive, Lu_unproductive
   - Lp_L_ratio, Lu_L_ratio

4. **productivity_1948_1989.csv** (3.8 KB)
   - marxian_productivity, conventional_productivity
   - marxian_index, conventional_index, bls_productivity_index

5. **government_1948_1989.csv** (3.9 KB)
   - G_total, G_federal, G_state_local
   - G_S_ratio, G_GDP_ratio, net_surplus

6. **validation_targets.csv** (529 bytes)
   - Benchmark values from Table 5.8 (5 years)
   - r_star_adjusted, exploitation_rate, value_composition

7. **comprehensive_1948_1989.csv** (8.3 KB)
   - Combined dataset with all key metrics
   - Used for overview and downloads

8. **shaikh_tonak_questions.csv** (15.2 KB) ✅ NEW!
   - 30 comprehensive questions with detailed explanations
   - Question_Number, Question, Category, Priority, Target_Tab
   - Explanation, Formula, Definition, Book_Reference
   - Powers the "Explore by Question" interactive feature

**Total data size:** 47 KB (very fast loading)

---

## Key Concepts

### Marxian Categories

**Productive Labor (Lp)**
- Workers directly engaged in surplus value production
- Manufacturing, construction, agriculture, mining
- ~49-53% of total employment (1948-1989)

**Unproductive Labor (Lu)**
- Workers whose wages are paid from surplus, not from value created
- Finance, insurance, real estate, retail trade, government
- ~47-51% of total employment

**Surplus Value (S*)**
- Total surplus appropriated from productive labor
- **Includes:** corporate profits + unproductive wages + interest + rent
- S* = GDP - V* (productive workers' wages)
- **Why high?** S* includes ~$1 trillion in unproductive wages (1948)

**Variable Capital (V*)**
- Wages of productive workers only
- V* = λ_m × Hp, where λ_m = Hp/GDP

**Constant Capital (C*)**
- Value transferred from means of production
- C* = Y - S* - V*, where Y = productive output

### Key Ratios

**Marxian Profit Rate: r* = S*/K**
- S* = total surplus value
- K = capital stock (nonresidential fixed assets)
- **Our values:** 300% (1948) → 186% (1989)
- **Why high?** S* includes unproductive wages

**Capacity-Adjusted Rate: r*' = r*/u**
- u = capacity utilization (0.71-0.91)
- Adjusts for underutilization of capital
- **Table 5.8 values:** 52% (1948) → 39% (1989)

**Exploitation Rate: e = S*/V***
- Ratio of unpaid to paid labor
- 1.70 (1948) → 2.44 (1989) [+43%]
- Measures intensity of exploitation

**Value Composition: C*/V***
- Capital intensity per worker
- 3.27 (1948) → 6.20 (1989) [+89%]
- Rising capital-labor ratio

---

## Validation Notes

### Excellent Agreement
- **Exploitation rate (S*/V*)**: Within 5% of Table 5.8 benchmarks
- **Value composition (C*/V*)**: Within 10-15% of targets

### Under Investigation
- **Profit rate (r*)**: Large deviation from Table 5.8
  - **Root causes:**
    1. We use total K, not productive K* = C*f
    2. Missing capacity utilization adjustment in comparison
  - **Resolution:** Calculate K* using productive share, apply u adjustment
  - **See:** `../R_STAR_DISCREPANCY_RESOLUTION.md` for details

---

## Technical Details

**Architecture**
- Single-file app.R (957 lines)
- Defensive data loading with tryCatch wrappers
- Unified long-format dataset for flexible filtering
- Reactive expressions for dynamic year range filtering

**Visualization**
- plotly for interactive charts (hover, zoom, pan)
- DT for interactive tables (sort, search, filter)
- Recession period shading (NBER dates)
- Color-coded validation status

**Performance**
- Pre-aggregated data (32 KB total)
- Instant load time (<1 second)
- No complex joins or calculations in app
- Responsive even on low-end hardware

---

## Troubleshooting

### App won't launch

**Error: "could not find function 'shiny::runApp'"**
```r
install.packages("shiny")
library(shiny)
runApp()
```

**Error: "data/profit_rates_1948_1989.csv not found"**
- Ensure you're running from the ShinyApp directory
- Use `setwd()` to navigate to correct location
- Verify data files exist with `source("validate_data.R")`

**Error: "package 'plotly' not found"**
```r
source("check_packages.R")  # Auto-installs missing packages
```

### Performance issues

**App is slow to load**
- First load compiles packages (~5-10 seconds normal)
- Subsequent loads should be instant
- Check file paths are relative, not absolute

**Plots not rendering**
- Ensure plotly package is installed
- Check browser console for JavaScript errors
- Try different browser (Chrome recommended)

### Data validation errors

**Run the validator:**
```r
source("validate_data.R")
```

**Expected output:**
```
[OK]   profit_rates_1948_1989.csv - 42 rows, 9 columns
[OK]   exploitation_composition_1948_1989.csv - 42 rows, 8 columns
...
DATA VALIDATION PASSED
```

---

## Development Roadmap

### Phase 1: Core Infrastructure ✅ COMPLETE
- Directory structure
- Data preprocessing (7 files)
- Helper scripts (check_packages.R, validate_data.R)
- app.R skeleton with data loading
- Tabs 1, 2, 6 implemented

### Phase 2: Full Feature Set ✅ COMPLETE
- ✅ Tab 4: Exploitation & Composition (dual y-axis plots, decade tables)
- ✅ Tab 5: Employment Analysis (stacked areas, productivity comparisons)
- ✅ Tab 6: Government Absorption (ratio plots, federal/state breakdown)
- ✅ Tab 8: Literature Navigator (references, methodology, citations)
- ✅ Tab 9: Data Downloads (CSV, Excel, RData exports with 10+ handlers)

### Phase 2.5: Question-Linking Innovation ✅ COMPLETE
- ✅ Tab 2: Explore by Question (30 comprehensive questions)
- ✅ Interactive question cards with priority badges
- ✅ Rich modal dialogs with formulas, definitions, visualizations
- ✅ Smart filtering by category and priority
- ✅ One-click tab navigation from questions
- ✅ 414 lines of new code (app.R: 2,121 → 2,535 lines)
- ✅ Questions CSV with 8 fields per question
- ✅ Inspired by Capitalism Data app innovations

### Phase 3: Cross-Validation
- Implement K* calculation (productive capital)
- Mohun 2005/2013 comparison
- Resolve r* discrepancy
- Comprehensive validation report

### Phase 4: Polish & Documentation
- Advanced features (custom plots, annotations)
- Mobile responsiveness
- Publication-quality documentation
- User testing and feedback
- Expand questions to 50+ covering all theoretical aspects

---

## References

**Primary Source:**
- Shaikh, A. & Tonak, E.A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts.* Cambridge University Press.
  - Especially Chapter 5: "The Accounting Framework" (Tables 5.5-5.14)
  - Table 5.8: Key validation benchmarks

**Methodological Extensions:**
- Mohun, S. (2005). "On Measuring the Wealth of Nations: The US Economy, 1964-2001." *Cambridge Journal of Economics* 29(5): 799-815.
- Mohun, S. (2013). "Unproductive Labor in the US Economy 1964-2010." *Review of Radical Political Economics* 46(3): 355-379.

**Data Sources:**
- Bureau of Economic Analysis (BEA): NIPA Tables
- Bureau of Labor Statistics (BLS): Productivity data
- Federal Reserve Economic Data (FRED): Time series

---

## License

This application is for academic research purposes. Data sources are publicly available from BEA and BLS.

**Citation:**
If you use this app in research or teaching, please cite:
- Original methodology: Shaikh & Tonak (1994)
- Data sources: BEA NIPA, BLS
- App: Arcanum Project (2025)

---

## Contact & Feedback

**Documentation:**
- Full session summary: `../SESSION_SUMMARY_2025-11-25_SHINY_APP_STARTED.md`
- Profit rate investigation: `../PROFIT_RATE_ANALYSIS_2025-11-25.md`
- Discrepancy resolution: `../R_STAR_DISCREPANCY_RESOLUTION.md`

**Files:**
- app.R: Main application (957 lines)
- check_packages.R: Package installer (89 lines)
- validate_data.R: Data validator (77 lines)

**Project directory:** `

---

**Version:** 2.5
**Last updated:** November 25, 2025
**Status:** Phase 2.5 Complete - ALL 9 TABS FULLY FUNCTIONAL + QUESTION-LINKING FEATURE
**App size:** 2,535 lines (up from 970 in Phase 1, +414 in Phase 2.5)
**Questions:** 30 comprehensive questions across 6 categories
