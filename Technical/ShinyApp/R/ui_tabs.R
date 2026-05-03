# =============================================================================
# UI TAB DEFINITIONS
# =============================================================================
# Functions for each tab in the Shiny dashboard
# Extracted from app.R for better organization
# =============================================================================

# TAB 1: OVERVIEW
# =============================================================================
ui_tab_overview <- function() {
  tabItem(
    tabName = "overview",
    h2("Shaikh-Tonak Marxian Analysis: Overview"),
    p("Interactive visualization of Marxian economic indicators for the United States, 1948-1989"),
    fluidRow(
      # Summary statistics
      valueBoxOutput("vbox_r_star", width = 3),
      valueBoxOutput("vbox_exploitation", width = 3),
      valueBoxOutput("vbox_productive_share", width = 3),
      valueBoxOutput("vbox_govt_absorption", width = 3)
    ),
    fluidRow(
      box(
        title = "Marxian Profit Rate (r* = S*/K)",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("overview_profit_plot", height = "400px")
      )
    ),
    fluidRow(
      box(
        title = "Key Trends (1948-1989)",
        status = "info",
        solidHeader = TRUE,
        width = 6,
        DTOutput("overview_trends_table")
      ),
      box(
        title = "About This Dataset",
        status = "success",
        solidHeader = TRUE,
        width = 6,
        p(strong("Methodology:"), " Marxian categories derived from BEA National Income and Product Accounts"),
        p(strong("Productive Labor:"), " Workers directly engaged in surplus value production"),
        p(strong("Surplus Value (S*):"), " Total surplus including unproductive wages paid from surplus"),
        p(strong("Variable Capital (V*):"), " Wages of productive workers only"),
        p(strong("Constant Capital (C*):"), " Value transferred from means of production"),
        hr(),
        p(strong("Key Findings:")),
        tags$ul(
          tags$li("Marxian profit rate declined 39% (1948-1989)"),
          tags$li("Exploitation rate rose 43% (S*/V*: 1.70 → 2.44)"),
          tags$li("Productive labor share fell 8% (Lp/L: 0.53 → 0.49)"),
          tags$li("Government absorbed increasing share of surplus")
        ),
        hr(),
        p(
          strong("Reference:"), " Shaikh, A. & Tonak, E.A. (1994). ", em("Measuring the Wealth of Nations."),
          " Cambridge University Press, Chapter 5."
        )
      )
    )
  )
}

# TAB 2: QUESTIONS
# =============================================================================
ui_tab_questions <- function() {
  tabItem(
    tabName = "questions",
    h2("Explore by Question"),
    p("Click on any question below to see detailed analysis, visualizations, and methodology"),
    fluidRow(
      # Filter controls
      box(
        title = "Filter Questions",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        collapsible = TRUE,
        fluidRow(
          column(
            4,
            selectInput("question_priority_filter",
              "Priority Level:",
              choices = c("All" = "all", "CRITICAL", "HIGH", "MEDIUM", "LOW"),
              selected = "all",
              width = "100%"
            )
          ),
          column(
            4,
            selectInput("question_category_filter",
              "Category:",
              choices = c(
                "All" = "all",
                "Profit Rate" = "Profit Rate",
                "Surplus Value" = "Surplus Value",
                "Capital Composition" = "Capital Composition",
                "Employment" = "Employment",
                "Government" = "Government",
                "Data & Methodology" = "Data & Methodology"
              ),
              selected = "all",
              width = "100%"
            )
          ),
          column(
            4,
            div(
              style = "padding-top: 25px;",
              h4(textOutput("questions_count"), style = "color: #3c8dbc; font-weight: bold;")
            )
          )
        )
      )
    ),
    fluidRow(
      box(
        title = "Questions",
        status = "info",
        solidHeader = TRUE,
        width = 12,
        div(
          style = "max-height: 800px; overflow-y: auto;",
          uiOutput("question_cards")
        )
      )
    )
  )
}

# TAB 3: METHODOLOGY
# =============================================================================
ui_tab_methodology <- function() {
  tabItem(
    tabName = "methodology",
    h2("Multi-Methodology Comparison"),
    p("Compare three major approaches: ST94 (Shaikh-Tonak 1994), M05 (Mohun 2005), TP19 (Tsoulfidis-Paitaridis 2019)"),
    fluidRow(
      valueBoxOutput("method_book_match", width = 4),
      valueBoxOutput("method_current_e", width = 4),
      valueBoxOutput("method_divergence", width = 4)
    ),
    fluidRow(
      box(
        title = "Exploitation Rate (S*/V*) by Methodology",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("methodology_exploitation_plot", height = "450px"),
        p(em("Note: Book benchmarks (dots) shown for validation. Shaded area indicates extension period (1990-2024)."))
      )
    ),
    fluidRow(
      box(
        title = "Productive Labor Share (Lp/L) by Methodology",
        status = "success",
        solidHeader = TRUE,
        width = 6,
        plotlyOutput("methodology_labor_plot", height = "350px")
      ),
      box(
        title = "Profit Rate Trends by Methodology",
        status = "warning",
        solidHeader = TRUE,
        width = 6,
        plotlyOutput("methodology_profit_plot", height = "350px")
      )
    ),
    fluidRow(
      box(
        title = "Methodology Comparison Table",
        status = "info",
        solidHeader = TRUE,
        width = 12,
        DTOutput("methodology_comparison_table")
      )
    ),
    fluidRow(
      box(
        title = "Why Do Methods Differ?",
        status = "danger",
        solidHeader = TRUE,
        width = 12,
        collapsible = TRUE,
        h4("Key Classification Differences"),
        tags$ul(
          tags$li(
            strong("Eating & Drinking Places (SIC 58 → NAICS 722):"),
            " ST94 = Unproductive (lumped with Retail), M05/TP19 = Productive (transforms food)"
          ),
          tags$li(
            strong("Information Sector (NAICS 51):"),
            " ST94 = Mixed (no SIC equivalent), M05/TP19 = Productive (produces information commodities)"
          ),
          tags$li(
            strong("Computer Systems Design (NAICS 5415):"),
            " ST94 = Mixed (SIC 7370 Business Services), M05/TP19 = Productive (software production)"
          )
        ),
        hr(),
        h4("Methodology Timeline"),
        p(strong("1948-1987:"), " Use ST94 (original I-O integration, SIC-based)"),
        p(strong("1988-1996:"), " Use M05 SM approximation (better BLS data allows calibration)"),
        p(strong("1997-2024:"), " Use TP19 NAICS classification (proper post-1997 classification)"),
        hr(),
        h4("Reference"),
        p("See ", strong("Chapter 5, pp. 151-194"), " of Shaikh & Tonak (1994) for original methodology."),
        p("See ", strong("Mohun (2005), Table 1, p.358"), " for SM approximation details."),
        p("See ", strong("Tsoulfidis & Paitaridis (2019), Table 1, p.238"), " for NAICS implementation.")
      )
    )
  )
}

# TAB: FIGURES & SERIES BROWSER
# =============================================================================
ui_tab_figures_series <- function() {
  tabItem(
    tabName = "figures_series",
    h2("Figures & Series Browser"),
    p("Browse the complete catalog of book figures and their underlying data series"),
    fluidRow(
      column(
        3,
        selectInput("fig_chapter_filter", "Chapter:",
          choices = c("All" = "All", "5" = "5", "6" = "6", "9" = "9"),
          selected = "All", width = "100%"
        )
      ),
      column(
        3,
        selectInput("fig_type_filter", "Figure Type:",
          choices = c("All" = "All", "Time Series" = "time_series",
                      "Cross-Sectional" = "cross_sectional", "Conceptual" = "conceptual"),
          selected = "All", width = "100%"
        )
      ),
      column(
        3,
        selectInput("fig_empirical_filter", "Empirical Only:",
          choices = c("All" = "All", "Yes" = "TRUE", "No" = "FALSE"),
          selected = "All", width = "100%"
        )
      ),
      column(
        3,
        div(
          style = "padding-top: 25px;",
          h4(textOutput("fig_count_display"), style = "color: #3c8dbc; font-weight: bold;")
        )
      )
    ),
    fluidRow(
      box(
        title = "Figure Catalog",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        DTOutput("figures_table")
      )
    ),
    fluidRow(
      box(
        title = "Series Details",
        status = "success",
        solidHeader = TRUE,
        width = 6,
        uiOutput("series_detail")
      ),
      box(
        title = "Figure Preview",
        status = "info",
        solidHeader = TRUE,
        width = 6,
        plotlyOutput("fig_preview", height = "400px")
      )
    )
  )
}

# TAB 4: PROFIT RATE
# =============================================================================
ui_tab_profit_rate <- function() {
  tabItem(
    tabName = "profit_rate",
    h2("Profit Rate Analysis"),
    p("Comparison of Marxian and conventional profit rate measures"),
    fluidRow(
      box(
        title = "Profit Rate Measures (1948-2024)",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        fluidRow(
          column(12,
            radioButtons("method_overlay", "Methodology Overlay:",
              choices = c("None" = "none", "ST94" = "ST94", "Mohun 2005" = "M05",
                          "Tsoulfidis 2019" = "TP19", "All Methods" = "All"),
              selected = "none", inline = TRUE
            )
          )
        ),
        plotlyOutput("profit_rate_plot", height = "500px")
      )
    ),
    fluidRow(
      box(
        title = "Series Selection",
        status = "info",
        width = 4,
        checkboxGroupInput("profit_series",
          "Select series to display:",
          choices = c(
            "Marxian r* (unadjusted)" = "r_star_pct",
            "Marxian r* (capacity-adjusted)" = "r_star_adj_pct",
            "NIPA r (unadjusted)" = "r_nipa_pct",
            "NIPA r (capacity-adjusted)" = "r_nipa_adj_pct"
          ),
          selected = c("r_star_pct", "r_nipa_pct")
        )
      ),
      box(
        title = "Profit Rate Statistics",
        status = "success",
        width = 8,
        DTOutput("profit_stats_table")
      )
    ),
    fluidRow(
      box(
        title = "Understanding Profit Rates",
        status = "warning",
        solidHeader = TRUE,
        width = 12,
        collapsible = TRUE,
        collapsed = TRUE,
        h4("Marxian Profit Rate (r*)"),
        p(strong("Definition:"), " r* = S*/K, where S* is total surplus value and K is capital stock"),
        p(strong("Key insight:"), " S* includes wages of unproductive workers (paid from surplus), making r* higher than conventional measures"),
        p(strong("Why capacity-adjusted?"), " r*' = r*/u adjusts for capacity utilization (u), showing rate at full capacity"),
        hr(),
        h4("NIPA Profit Rate (r)"),
        p(strong("Definition:"), " r = Corporate Profits / Capital Stock (conventional measure)"),
        p(strong("Difference:"), " Excludes unproductive wages, interest, rent from surplus definition"),
        hr(),
        h4("Note on r* Values"),
        p("Marxian profit rates appear high (200-500%) because:"),
        tags$ul(
          tags$li("S* includes ALL surplus appropriation (profits + unproductive wages + interest + rent)"),
          tags$li("Unproductive workers represent ~47-51% of total employment"),
          tags$li("Their wages (~$1.1 trillion in 1948) are paid from surplus, not from value they create"),
          tags$li("This is theoretically correct within the Marxian framework")
        ),
        p(strong("See Validation tab"), " for comparison with Shaikh-Tonak Table 5.8 benchmarks")
      )
    )
  )
}

# TAB 5: EXPLOITATION
# =============================================================================
ui_tab_exploitation <- function() {
  tabItem(
    tabName = "exploitation",
    h2("Exploitation & Capital Composition"),
    p("Analysis of surplus extraction and organic composition of capital"),
    fluidRow(
      valueBoxOutput("exploit_current", width = 3),
      valueBoxOutput("exploit_change", width = 3),
      valueBoxOutput("value_comp_current", width = 3),
      valueBoxOutput("surplus_ratio_current", width = 3)
    ),
    fluidRow(
      box(
        title = "Exploitation Rate (S*/V*) and Surplus Ratio (S*/Y)",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("exploitation_plot", height = "450px")
      )
    ),
    fluidRow(
      box(
        title = "Capital Composition Analysis",
        status = "success",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("composition_plot", height = "450px")
      )
    ),
    fluidRow(
      box(
        title = "Exploitation Metrics by Decade",
        status = "warning",
        solidHeader = TRUE,
        width = 6,
        DTOutput("exploitation_decade_table")
      ),
      box(
        title = "Understanding Exploitation & Composition",
        status = "info",
        solidHeader = TRUE,
        width = 6,
        collapsible = TRUE,
        h4("Exploitation Rate (S*/V*)"),
        p(strong("Definition:"), " Ratio of surplus value to variable capital"),
        p(strong("Interpretation:"), " Higher values = more surplus extracted per dollar of productive wages"),
        p(strong("Trend 1948-1989:"), " Rose from 1.32 to 2.44 (+84%), showing intensified exploitation"),
        hr(),
        h4("Surplus Ratio (S*/Y)"),
        p(strong("Definition:"), " Share of total value product going to surplus"),
        p(strong("Formula:"), " S*/Y = S*/(C* + V* + S*)"),
        hr(),
        h4("Value Composition (C*/V*)"),
        p(strong("Definition:"), " Ratio of constant to variable capital"),
        p(strong("Interpretation:"), " Rising C*/V* indicates mechanization and rising capital intensity"),
        p(strong("Significance:"), " Key determinant of the profit rate: r* = (S*/V*) / (1 + C*/V*)")
      )
    )
  )
}

# TAB 6: EMPLOYMENT
# =============================================================================
ui_tab_employment <- function() {
  tabItem(
    tabName = "employment",
    h2("Employment Analysis"),
    p("Productive vs. unproductive labor composition and productivity trends"),
    fluidRow(
      valueBoxOutput("emp_total_current", width = 3),
      valueBoxOutput("emp_productive_share", width = 3),
      valueBoxOutput("emp_productive_trend", width = 3),
      valueBoxOutput("productivity_growth", width = 3)
    ),
    fluidRow(
      box(
        title = "Employment Composition (1948-1989)",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("employment_composition_plot", height = "450px")
      )
    ),
    fluidRow(
      box(
        title = "Absolute Employment Levels (thousands)",
        status = "success",
        solidHeader = TRUE,
        width = 7,
        plotlyOutput("employment_absolute_plot", height = "400px")
      ),
      box(
        title = "Employment Statistics",
        status = "info",
        solidHeader = TRUE,
        width = 5,
        DTOutput("employment_stats_table")
      )
    ),
    fluidRow(
      box(
        title = "Productivity Comparison: Marxian vs. Conventional",
        status = "warning",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("productivity_comparison_plot", height = "450px")
      )
    ),
    fluidRow(
      box(
        title = "Understanding Productive vs. Unproductive Labor",
        status = "danger",
        solidHeader = TRUE,
        width = 12,
        collapsible = TRUE,
        collapsed = TRUE,
        h4("Productive Labor (Lp)"),
        p(strong("Definition:"), " Workers directly engaged in producing surplus value"),
        p(strong("Sectors:"), " Manufacturing, construction, agriculture, mining, transportation"),
        p(strong("Trend:"), " Fell from 53% to 49% of total employment (1948-1989)"),
        hr(),
        h4("Unproductive Labor (Lu)"),
        p(strong("Definition:"), " Workers not engaged in surplus production, paid from surplus"),
        p(strong("Sectors:"), " Finance, insurance, real estate, advertising, government administration"),
        p(strong("Trend:"), " Rose from 47% to 51% of total employment"),
        hr(),
        h4("Marxian vs. Conventional Productivity"),
        p(strong("Marxian:"), " Y/Lp - Output per productive worker only"),
        p(strong("Conventional:"), " Y/L - Output per total worker (BLS measure)"),
        p(strong("Key insight:"), " Marxian productivity rises faster as Lp/L falls")
      )
    )
  )
}

# TAB 7: GOVERNMENT
# =============================================================================
ui_tab_government <- function() {
  tabItem(
    tabName = "government",
    h2("Government Absorption of Surplus"),
    p("Analysis of government expenditure as deduction from surplus value"),
    fluidRow(
      valueBoxOutput("govt_total_current", width = 3),
      valueBoxOutput("govt_surplus_ratio", width = 3),
      valueBoxOutput("govt_gdp_ratio", width = 3),
      valueBoxOutput("govt_growth", width = 3)
    ),
    fluidRow(
      box(
        title = "Government Absorption Ratios (1948-1989)",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("government_ratios_plot", height = "450px")
      )
    ),
    fluidRow(
      box(
        title = "Government Expenditure by Level",
        status = "success",
        solidHeader = TRUE,
        width = 7,
        plotlyOutput("government_levels_plot", height = "400px")
      ),
      box(
        title = "Government Statistics by Decade",
        status = "info",
        solidHeader = TRUE,
        width = 5,
        DTOutput("government_decade_table")
      )
    ),
    fluidRow(
      box(
        title = "Understanding Government as Surplus Absorption",
        status = "warning",
        solidHeader = TRUE,
        width = 12,
        collapsible = TRUE,
        collapsed = TRUE,
        h4("Marxian Treatment of Government"),
        p(strong("Key insight:"), " Government expenditure represents unproductive consumption paid from surplus"),
        p(strong("G/S* ratio:"), " Share of surplus absorbed by government spending"),
        p(strong("Trend:"), " Rose from 3.4% (1948) to higher levels by 1989"),
        hr(),
        h4("Components"),
        p(strong("Federal:"), " Defense, social programs, administration"),
        p(strong("State & Local:"), " Education, infrastructure, public services"),
        hr(),
        h4("Theoretical Significance"),
        tags$ul(
          tags$li("Government workers are unproductive (transfer value, don't create it)"),
          tags$li("Government spending reduces surplus available for accumulation"),
          tags$li("Rising G/S* can constrain capital accumulation and growth")
        )
      )
    )
  )
}

# TAB 8: VALIDATION
# =============================================================================
ui_tab_validation <- function() {
  tabItem(
    tabName = "validation",
    h2("Validation Center"),
    p("Cross-validation against Shaikh-Tonak (1994) Table 5.8 benchmarks"),
    fluidRow(
      valueBoxOutput("validation_status", width = 4),
      valueBoxOutput("validation_r_star", width = 4),
      valueBoxOutput("validation_exploitation", width = 4)
    ),
    fluidRow(
      box(
        title = "Calculated vs. Target Values (Table 5.8 Benchmark Years)",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        plotlyOutput("validation_scatter", height = "500px")
      )
    ),
    fluidRow(
      box(
        title = "Deviation from Table 5.8 Targets",
        status = "warning",
        solidHeader = TRUE,
        width = 12,
        DTOutput("validation_table")
      )
    ),
    fluidRow(
      box(
        title = "Validation Notes",
        status = "danger",
        solidHeader = TRUE,
        width = 12,
        collapsible = TRUE,
        h4("Known Discrepancies"),
        p(strong("Issue:"), " Marxian profit rate r* shows large deviation from Table 5.8"),
        tags$ul(
          tags$li(strong("Our calculation:"), " r* ≈ 300% (1948) → 186% (1989)"),
          tags$li(strong("Table 5.8 target:"), " r*' ≈ 52% (1948) → 39% (1989)"),
          tags$li(strong("Ratio:"), " ~5.8x difference")
        ),
        hr(),
        h4("Root Causes Identified"),
        p("1. ", strong("Capital Stock Definition:")),
        tags$ul(
          tags$li("We use K = Total nonresidential fixed assets"),
          tags$li("Table 5.8 uses K* = C*f = Productive fixed capital only"),
          tags$li("K* should be smaller than K (only productive sectors)")
        ),
        p("2. ", strong("Capacity Utilization Adjustment:")),
        tags$ul(
          tags$li("Table 5.8 shows r*' = (S*/K*)/u (capacity-adjusted)"),
          tags$li("We calculate r* = S*/K (unadjusted)")
        ),
        hr(),
        h4("Resolution Strategy"),
        p("The displayed values use our current methodology. To match Table 5.8:"),
        tags$ol(
          tags$li("Calculate K* = K × (Y/GDP) to estimate productive capital"),
          tags$li("Apply capacity adjustment: r*' = (S*/K*)/u"),
          tags$li("Cross-validate with Mohun (2005, 2013) alternative estimates")
        ),
        p(strong("Status:"), " Investigation ongoing. See Technical/R_STAR_DISCREPANCY_RESOLUTION.md for details"),
        hr(),
        h4("Validation Quality"),
        p(strong("Exploitation rate (S*/V*):"), " EXCELLENT match (within 5%)"),
        p(strong("Value composition (C*/V*):"), " GOOD match (within 10-15%)"),
        p(strong("Profit rate (r*):"), " UNDER INVESTIGATION (see above)")
      )
    )
  )
}

# TAB 9: LITERATURE
# =============================================================================
ui_tab_literature <- function() {
  tabItem(
    tabName = "literature",
    h2("Literature Navigator"),
    p("Key references, methodological notes, and knowledge base links"),
    fluidRow(
      box(
        title = "Primary Reference",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        h3("Shaikh, Anwar M. & Tonak, E. Ahmet (1994)"),
        h4(em("Measuring the Wealth of Nations: The Political Economy of National Accounts")),
        p(strong("Publisher:"), " Cambridge University Press"),
        p(strong("Chapter 5:"), " \"The Profit Rate and Its Components\" (pp. 151-194)"),
        hr(),
        p(strong("Key Contributions:")),
        tags$ul(
          tags$li("Rigorous derivation of Marxian categories from NIPA data"),
          tags$li("Distinction between productive and unproductive labor"),
          tags$li("Calculation of S*, V*, C* from national accounts"),
          tags$li("Empirical evidence for tendential fall in profit rate")
        ),
        hr(),
        p(strong("Table 5.8:"), " Benchmark values used for validation in this app")
      )
    ),
    fluidRow(
      box(
        title = "Methodological Documentation",
        status = "success",
        solidHeader = TRUE,
        width = 6,
        collapsible = TRUE,
        h4("Data Sources"),
        tags$ul(
          tags$li(strong("BEA NIPA:"), " National Income and Product Accounts"),
          tags$li(strong("BLS:"), " Productivity and employment data"),
          tags$li(strong("Federal Reserve:"), " Capacity utilization (manufacturing)")
        ),
        hr(),
        h4("Key Methodological Steps"),
        tags$ol(
          tags$li("Classify industries as productive vs. unproductive"),
          tags$li("Calculate productive output Y from GDP"),
          tags$li("Derive V* (productive wages), S* (total surplus), C* (constant capital)"),
          tags$li("Compute exploitation rate S*/V*, composition C*/V*, profit rate r* = S*/K")
        ),
        hr(),
        p(strong("See:"), " Shaikh & Tonak (1994), Appendix 5.1 for detailed classification")
      ),
      box(
        title = "Related Literature",
        status = "info",
        solidHeader = TRUE,
        width = 6,
        collapsible = TRUE,
        h4("Follow-up Studies"),
        tags$ul(
          tags$li(strong("Mohun (2005):"), " \"Distributive Shares in the US Economy, 1964-2001\""),
          tags$li(strong("Mohun (2013):"), " \"Unproductive Labor in the US Economy 1964-2010\""),
          tags$li(strong("Basu & Manolakos (2013):"), " \"Is There a Tendency for the Rate of Profit to Fall?\""),
          tags$li(strong("Kliman (2011):"), em(" The Failure of Capitalist Production"))
        ),
        hr(),
        h4("Critical Debates"),
        tags$ul(
          tags$li("Productive vs. unproductive labor classification"),
          tags$li("Treatment of fixed capital depreciation"),
          tags$li("Capacity utilization adjustments"),
          tags$li("Alternative measures of capital stock (K vs. K*)")
        )
      )
    ),
    fluidRow(
      box(
        title = "Knowledge Base Extractions",
        status = "warning",
        solidHeader = TRUE,
        width = 12,
        h4("Available Documentation"),
        p("The following knowledge base files contain detailed extraction and analysis:"),
        tags$ul(
          tags$li(strong("R_STAR_DISCREPANCY_RESOLUTION.md:"), " Investigation of profit rate calculation differences"),
          tags$li(strong("VALIDATION_RESULTS.md:"), " Cross-validation against Table 5.8 benchmarks"),
          tags$li(strong("METHODOLOGY_NOTES.md:"), " Step-by-step calculation procedures"),
          tags$li(strong("DATA_PROVENANCE.md:"), " Data sources and transformations")
        ),
        hr(),
        p(em("Note: Links to knowledge base files can be implemented with file path references or downloadable PDFs"))
      )
    ),

    # NEW: HDARP Extracted Literature with page citations
    fluidRow(
      box(
        title = "HDARP-Extracted Literature Database",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        h4(icon("book-open"), " Complete Bibliography with Page-Level Citations"),
        p("All sources have been processed through HDARP (Hybrid Direct Agent Reading Protocol) for maximum extraction accuracy."),
        DTOutput("literature_citations_table")
      )
    ),
    fluidRow(
      box(
        title = "Methodology Evolution Timeline",
        status = "info",
        solidHeader = TRUE,
        width = 12,
        h4("Development of Marxian National Accounting"),
        fluidRow(
          column(
            3,
            div(
              class = "well", style = "text-align: center; background-color: #3c8dbc; color: white;",
              h4("1984"),
              p(strong("Semmler")),
              p("Competition, Monopoly, and Differential Profit Rates"),
              p(em("Foundational theory"))
            )
          ),
          column(
            3,
            div(
              class = "well", style = "text-align: center; background-color: #00a65a; color: white;",
              h4("1994"),
              p(strong("Shaikh & Tonak")),
              p("Measuring the Wealth of Nations"),
              p(em("ST94 methodology"))
            )
          ),
          column(
            3,
            div(
              class = "well", style = "text-align: center; background-color: #f39c12; color: white;",
              h4("2005"),
              p(strong("Mohun")),
              p("Distributive Shares in the US Economy"),
              p(em("M05 SM approximation"))
            )
          ),
          column(
            3,
            div(
              class = "well", style = "text-align: center; background-color: #605ca8; color: white;",
              h4("2019"),
              p(strong("Tsoulfidis & Paitaridis")),
              p("Capital Intensity and the Great Recession"),
              p(em("TP19 NAICS methodology"))
            )
          )
        )
      )
    ),
    fluidRow(
      box(
        title = "Citation Guide",
        status = "danger",
        solidHeader = TRUE,
        width = 12,
        collapsible = TRUE,
        collapsed = TRUE,
        h4("How to Cite This App"),
        p(strong("APA Format:")),
        p(
          "Arcanum Project. (2025). ", em("Shaikh-Tonak Marxian Analysis Shiny App (1948-1989)."),
          " Interactive data visualization. Based on Shaikh, A. M., & Tonak, E. A. (1994). ",
          em("Measuring the Wealth of Nations."), " Cambridge University Press."
        ),
        hr(),
        h4("How to Cite Shaikh & Tonak (1994)"),
        p(strong("APA Format:")),
        p(
          "Shaikh, A. M., & Tonak, E. A. (1994). ", em("Measuring the wealth of nations: The political economy of national accounts."),
          " Cambridge University Press."
        ),
        hr(),
        p(strong("BibTeX:"), " (available in Downloads tab)")
      )
    )
  )
}

# TAB 10: DOWNLOADS
# =============================================================================
ui_tab_downloads <- function() {
  tabItem(
    tabName = "downloads",
    h2("Data Downloads"),
    p("Export datasets in multiple formats for further analysis"),
    fluidRow(
      infoBox(
        "Available Datasets",
        value = "11",
        subtitle = "Extended datasets ready for download",
        icon = icon("database"),
        color = "blue",
        width = 4
      ),
      infoBox(
        "Time Period",
        value = "1948-2024",
        subtitle = "77 years of annual data",
        icon = icon("calendar"),
        color = "green",
        width = 4
      ),
      infoBox(
        "Formats",
        value = "CSV, Excel, RData",
        subtitle = "Multiple export options",
        icon = icon("file-export"),
        color = "orange",
        width = 4
      )
    ),
    fluidRow(
      box(
        title = "Individual Dataset Downloads",
        status = "primary",
        solidHeader = TRUE,
        width = 12,
        p("Download individual datasets (CSV format):"),
        hr(),
        fluidRow(
          column(
            6,
            h4("Core Economic Indicators"),
            downloadButton("download_profit_rates", "Profit Rates (1948-1989)",
              class = "btn-primary", style = "margin: 5px; width: 95%;"
            ),
            br(),
            downloadButton("download_exploitation", "Exploitation & Composition",
              class = "btn-primary", style = "margin: 5px; width: 95%;"
            ),
            br(),
            downloadButton("download_employment", "Employment Data",
              class = "btn-primary", style = "margin: 5px; width: 95%;"
            ),
            br(),
            downloadButton("download_productivity", "Productivity Measures",
              class = "btn-primary", style = "margin: 5px; width: 95%;"
            )
          ),
          column(
            6,
            h4("Supplementary Data"),
            downloadButton("download_government", "Government Expenditures",
              class = "btn-success", style = "margin: 5px; width: 95%;"
            ),
            br(),
            downloadButton("download_validation", "Validation Targets (Table 5.8)",
              class = "btn-success", style = "margin: 5px; width: 95%;"
            ),
            br(),
            downloadButton("download_comprehensive", "Comprehensive Dataset (All Series)",
              class = "btn-warning", style = "margin: 5px; width: 95%;"
            )
          )
        )
      )
    ),
    fluidRow(
      box(
        title = "Filtered Data Export",
        status = "success",
        solidHeader = TRUE,
        width = 6,
        p("Export data with current year range filter applied:"),
        p(strong("Current selection:"), textOutput("download_year_range", inline = TRUE)),
        hr(),
        radioButtons("download_format",
          "Select format:",
          choices = c(
            "CSV" = "csv",
            "Excel (.xlsx)" = "xlsx",
            "R Data (.RData)" = "rdata"
          ),
          selected = "csv"
        ),
        hr(),
        downloadButton("download_filtered", "Download Filtered Data",
          class = "btn-success btn-lg", style = "width: 100%;"
        )
      ),
      box(
        title = "Data Dictionary",
        status = "info",
        solidHeader = TRUE,
        width = 6,
        h4("Variable Definitions"),
        p(strong("r_star_pct:"), " Marxian profit rate S*/K (%)"),
        p(strong("r_nipa_pct:"), " NIPA profit rate (%)"),
        p(strong("exploitation_rate:"), " S*/V* (surplus/variable capital)"),
        p(strong("value_composition:"), " C*/V* (constant/variable capital)"),
        p(strong("Lp_L_ratio:"), " Productive labor share"),
        p(strong("G_S_ratio:"), " Government/surplus ratio"),
        hr(),
        downloadButton("download_codebook", "Download Full Codebook (TXT)",
          class = "btn-info", style = "width: 100%;"
        )
      )
    )
  )
}

# SIDEBAR FUNCTION
# =============================================================================
ui_sidebar <- function() {
  dashboardSidebar(
    width = 300,
    sidebarMenu(
      id = "tabs",
      menuItem("Overview", tabName = "overview", icon = icon("dashboard")),
      menuItem("Explore by Question", tabName = "questions", icon = icon("question-circle")),
      menuItem("Methodology Comparison",
        tabName = "methodology", icon = icon("code-compare"),
        badgeLabel = "NEW", badgeColor = "green"
      ),
      menuItem("Figures & Series", tabName = "figures_series", icon = icon("th"),
        badgeLabel = "NEW", badgeColor = "green"
      ),
      menuItem("Profit Rate Analysis", tabName = "profit_rate", icon = icon("chart-line")),
      menuItem("Exploitation & Composition", tabName = "exploitation", icon = icon("balance-scale")),
      menuItem("Employment Analysis", tabName = "employment", icon = icon("users")),
      menuItem("Government Absorption", tabName = "government", icon = icon("university")),
      menuItem("Validation Center", tabName = "validation", icon = icon("check-circle")),
      menuItem("Literature Navigator", tabName = "literature", icon = icon("book")),
      menuItem("Data Downloads", tabName = "downloads", icon = icon("download"))
    ),

    # Global controls
    hr(),
    h5("Global Controls", style = "padding-left: 15px; font-weight: bold;"),
    sliderInput("year_range",
      "Year Range:",
      min = 1948,
      max = 2024,
      value = c(1948, 2024),
      step = 1,
      sep = ""
    ),
    checkboxInput("show_recessions",
      "Show Recession Periods",
      value = TRUE
    ),
    checkboxInput("show_period_shading",
      "Show Book/Extension Period Shading",
      value = TRUE
    ),
    hr(),

    # Data info
    h5("Dataset Information", style = "padding-left: 15px; font-weight: bold;"),
    p(strong("Period:"), " 1948-2024 (Extended)", style = "padding-left: 15px; font-size: 12px;"),
    p(strong("Observations:"), " 77 years", style = "padding-left: 15px; font-size: 12px;"),
    p(strong("Source:"), " BEA NIPA, BLS", style = "padding-left: 15px; font-size: 12px;"),
    p(strong("Reference:"), " Shaikh & Tonak (1994)", style = "padding-left: 15px; font-size: 12px;")
  )
}
