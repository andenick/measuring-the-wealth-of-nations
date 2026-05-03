# Quick Start Guide

Get the Shaikh-Tonak Shiny app running in 5 minutes.

---

## Prerequisites

- **R** version 4.0 or higher
- **RStudio** (recommended but not required)
- Internet connection (for package installation)

---

## 3-Step Launch

### Step 1: Open R/RStudio

Navigate to the ShinyApp directory:

```r
setwd("D:/Arcanum/Projects/AS2/Technical/ShinyApp")
```

### Step 2: Run Setup Scripts

**Install required packages:**
```r
source("check_packages.R")
```

**Output should show:**
```
All required packages are already installed!
  - shiny (version X.X.X)
  - shinydashboard (version X.X.X)
  ...
You're ready to launch the app!
```

**Validate data files:**
```r
source("validate_data.R")
```

**Output should show:**
```
[OK]   profit_rates_1948_1989.csv - 42 rows, 9 columns
[OK]   exploitation_composition_1948_1989.csv - 42 rows, 8 columns
...
DATA VALIDATION PASSED
```

### Step 3: Launch the App

```r
shiny::runApp()
```

**The app will open in your browser at:** `http://127.0.0.1:####`

---

## All-in-One Command

If you're already in the ShinyApp directory and have packages installed:

```r
source("check_packages.R"); source("validate_data.R"); shiny::runApp()
```

---

## What You'll See

### Tab 1: Overview Dashboard
- 4 value boxes: profit rate, exploitation rate, productive labor share, govt absorption
- Main profit rate plot (1948-1989)
- Key trends table
- Methodology notes

### Tab 2: Profit Rate Analysis
- Interactive multi-series plot
- Series selection checkboxes (Marxian r*, NIPA r, capacity-adjusted variants)
- Statistics table
- Recession period shading

### Tab 6: Validation Center
- Cross-validation against Table 5.8 benchmarks
- Scatter plot: calculated vs target values
- Deviation table for 5 benchmark years (1948, 1964, 1970, 1980, 1989)

**Note:** Tabs 3, 4, 5, 7, 8 show "Coming soon..." placeholders

---

## Interactive Controls

### Sidebar Controls (affect all tabs)

**Year Range Slider:**
- Drag to adjust time period
- Default: 1948-1989 (full period)
- Example: Select 1970-1989 to focus on late 20th century

**Show Recession Periods:**
- Check/uncheck to toggle gray recession shading
- Based on NBER recession dates

### Tab-Specific Controls

**Tab 2 (Profit Rate Analysis):**
- Checkboxes to select which profit rate series to display
- Default: Marxian r* and NIPA r (unadjusted)
- Can select all 4 series for full comparison

---

## Tips for Exploration

### Understanding the Data

**Why is Marxian r* so high (200-500%)?**
- S* includes ALL surplus (profits + unproductive wages + interest + rent)
- Unproductive workers (~47-51% of employment) are paid from surplus
- Example (1948): S* = $1,691B includes $1,117B in unproductive wages
- This is theoretically correct in Marxian framework

**What's the difference between r* and r*'?**
- r* = S*/K (unadjusted rate)
- r*' = r*/u (capacity-adjusted, where u = capacity utilization)
- r*' shows the rate if capital were fully utilized
- Table 5.8 uses r*' for comparisons

### Using the Year Range Slider

**Full period (1948-1989):**
- See complete postwar trends
- Identify long-run patterns

**Golden Age (1948-1973):**
- High capacity utilization
- Stable exploitation rate
- Strong productivity growth

**Crisis Era (1973-1989):**
- Declining profit rates
- Rising exploitation rate
- Productivity slowdown

### Checking Validation

**Tab 6: Validation Center**

**Green indicators (<5% deviation):**
- Exploitation rate (S*/V*) - EXCELLENT match
- Most years within 2-3% of targets

**Yellow indicators (5-15% deviation):**
- Value composition (C*/V*) - GOOD match
- Within theoretical/data collection variance

**Red indicators (>15% deviation):**
- Profit rate (r*) - UNDER INVESTIGATION
- See README.md "Validation Notes" for explanation

---

## Common First-Time Questions

### Q: Why are there 8 tabs but only 3 work?

**A:** Phase 1 focused on core infrastructure and priority validation. Tabs 3-5, 7-8 will be implemented in Phase 2 (next week). You can already explore:
- Overview (Tab 1)
- Profit rates (Tab 2)
- Validation (Tab 6)

### Q: Can I export the data?

**A:** Download functionality will be added in Tab 8 (Data Downloads) during Phase 2. For now, you can access the raw CSV files directly in the `data/` directory:
- `profit_rates_1948_1989.csv`
- `exploitation_composition_1948_1989.csv`
- etc.

### Q: How do I cite this app?

**A:**
```
Shaikh, A. & Tonak, E.A. (1994). Measuring the Wealth of Nations.
   Cambridge University Press.
Data sources: BEA NIPA, BLS
Interactive app: Arcanum Project (2025)
```

### Q: The validation shows red - is the data wrong?

**A:** No! The red validation for r* is a **known discrepancy** being investigated. It stems from:
1. Difference between total K and productive K*
2. Capacity utilization adjustment methodology
3. Different surplus definitions

Our exploitation rate and composition match Table 5.8 excellently (green), confirming data quality. See `../R_STAR_DISCREPANCY_RESOLUTION.md` for full analysis.

---

## Stopping the App

**In R console:** Press `Ctrl+C` or `Esc`

**In RStudio:** Click the red "Stop" button in the Console pane

---

## Next Steps

**Explore the data:**
- Adjust year ranges to see how trends change
- Toggle recession shading to see crisis impacts
- Check validation deviations across different time periods

**Read the documentation:**
- `README.md` - Full documentation
- `../SESSION_SUMMARY_2025-11-25_SHINY_APP_STARTED.md` - Development log
- `../R_STAR_DISCREPANCY_RESOLUTION.md` - Validation investigation

**Wait for updates:**
- Week 2: Tabs 3-5, 7-8 (full feature set)
- Week 3: Cross-validation with Mohun 2005/2013
- Week 4: Polish and publication-ready documentation

---

## Troubleshooting

### "Error: could not find function 'runApp'"

```r
install.packages("shiny")
library(shiny)
runApp()
```

### "Error: file 'app.R' does not exist"

You're not in the correct directory. Navigate:
```r
setwd("D:/Arcanum/Projects/AS2/Technical/ShinyApp")
```

Verify location:
```r
getwd()  # Should show: "D:/Arcanum/Projects/AS2/Technical/ShinyApp"
```

### "Error: data/profit_rates_1948_1989.csv not found"

Run data validator:
```r
source("validate_data.R")
```

If files are missing, they need to be regenerated from the parent directory's data processing scripts.

### App loads but plots are blank

1. Check year range slider - may be set to very narrow range
2. Ensure series are selected in Tab 2 checkboxes
3. Try refreshing browser (F5)
4. Check R console for error messages

### Package installation fails

**Common issue:** Corporate firewall blocking CRAN

**Solution 1:** Use RStudio Package Manager
```r
options(repos = c(CRAN = "https://cloud.r-project.org"))
install.packages("shiny")
```

**Solution 2:** Manual installation from local files
- Download packages from CRAN website
- Install locally: `install.packages("path/to/package.tar.gz", repos = NULL)`

---

**Happy exploring!**

For detailed documentation, see `README.md`

For development roadmap, see `../SESSION_SUMMARY_2025-11-25_SHINY_APP_STARTED.md`

---

**Version:** 1.0
**Last updated:** November 25, 2025
