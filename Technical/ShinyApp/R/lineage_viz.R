# =============================================================================
# Data Lineage Visualization for Shaikh-Tonak Shiny App
# =============================================================================
#
# Provides interactive visualization of data transformation chains showing
# exactly where each data point comes from and how it was calculated.
#
# Usage:
#   source("R/lineage_viz.R")
#   output$lineage_graph <- renderVisNetwork({
#     render_lineage_graph(selected_series_id)
#   })
#
# Dependencies:
#   - visNetwork
#   - dplyr
#   - jsonlite
#
# Author: Shaikh-Tonak Replication Project
# Date: January 26, 2026
# =============================================================================

library(visNetwork)
library(dplyr)
library(jsonlite)

# -----------------------------------------------------------------------------
# DATA LINEAGE DEFINITIONS
# -----------------------------------------------------------------------------

#' Define the lineage chain for profit rate calculation
#'
#' Returns a list of nodes and edges representing the data transformation
#' pipeline for profit rates.
#'
#' @return list with nodes and edges data frames
get_profit_rate_lineage <- function() {

  # Define nodes in the transformation chain
  nodes <- data.frame(
    id = c(
      "bea_nipa", "bea_io", "fred_capacity", "bls_employment",
      "labor_values", "employment_dist", "surplus_value", "capital_stock",
      "utilization", "profit_rate_raw", "validation", "profit_rate_final"
    ),
    label = c(
      "BEA NIPA\n(1929-2025)",
      "BEA I-O Tables\n(1947-1982)",
      "FRED Capacity\nUtilization",
      "BLS Employment\nStatistics",
      "Labor Value\nCoefficients (λ*)",
      "Employment\nDistribution (Lp/L)",
      "Surplus Value\n(S = VA* - W)",
      "Capital Stock\n(K)",
      "Capacity\nUtilization (u)",
      "Raw Profit Rate\nr = S/(K×u)",
      "Benchmark\nValidation",
      "Final Profit Rate\nSeries (1948-2024)"
    ),
    group = c(
      "source", "source", "source", "source",
      "calculation", "calculation", "calculation", "calculation",
      "calculation", "calculation", "validation", "output"
    ),
    level = c(
      1, 1, 1, 1,
      2, 2, 3, 3,
      3, 4, 5, 6
    ),
    title = c(
      "Bureau of Economic Analysis National Income and Product Accounts<br>Tables: 1.12, 1.1.5, 6.1<br>626,281 records",
      "BEA Input-Output Benchmark Tables<br>7 benchmark years: 1947-1982<br>85 industries",
      "Federal Reserve Economic Data<br>Series: CAPUTLB00004S<br>Capacity Utilization Index",
      "Bureau of Labor Statistics<br>Employment by Industry<br>Monthly to Annual",
      "Calculated from I-O inverse<br>λ* = (I - A)⁻¹ × employment vector<br>Per Shaikh-Tonak methodology",
      "Productive vs Unproductive Labor<br>Based on Mohun (2005, 2013)<br>Industry classification",
      "S = Value Added - Wages<br>Using Marxian definitions<br>Per Shaikh-Tonak Ch. 5",
      "Fixed Assets by Industry<br>Productive capital only<br>Real terms (2017$)",
      "Actual/Potential Output<br>Smoothed series<br>1973 interpolation",
      "r = SP/(K×u)<br>Where SP = productive surplus<br>K = productive capital",
      "Compared to Book Tables 5.4-5.8<br>93.8% exact matches<br>MAE = 0.000937",
      "Extended Series 1948-2024<br>77 annual observations<br>Ready for analysis"
    ),
    stringsAsFactors = FALSE
  )

  # Define edges (transformation relationships)
  edges <- data.frame(
    from = c(
      "bea_nipa", "bea_io", "bea_io", "bls_employment",
      "labor_values", "employment_dist", "bea_nipa", "fred_capacity",
      "surplus_value", "capital_stock", "utilization",
      "profit_rate_raw", "validation"
    ),
    to = c(
      "surplus_value", "labor_values", "employment_dist", "employment_dist",
      "surplus_value", "surplus_value", "capital_stock", "utilization",
      "profit_rate_raw", "profit_rate_raw", "profit_rate_raw",
      "validation", "profit_rate_final"
    ),
    label = c(
      "VA, Wages", "Technical\nCoeffs", "Employment\nRows", "Industry\nDetail",
      "λ*", "Lp/L", "Fixed\nAssets", "CAPUTL",
      "S", "K", "u",
      "Raw r", "Validated r"
    ),
    arrows = "to",
    stringsAsFactors = FALSE
  )

  return(list(nodes = nodes, edges = edges))
}


#' Define the lineage chain for exploitation rate calculation
#'
#' @return list with nodes and edges data frames
get_exploitation_rate_lineage <- function() {

  nodes <- data.frame(
    id = c(
      "nipa_va", "nipa_wages", "employment", "industry_class",
      "va_star", "w_star", "exploitation_raw", "book_benchmark",
      "exploitation_final"
    ),
    label = c(
      "NIPA Value\nAdded",
      "NIPA Wages &\nSalaries",
      "Employment\nby Industry",
      "Industry\nClassification",
      "Productive VA\n(VA*)",
      "Productive\nWages (W*)",
      "Raw Exploitation\ne = S/V",
      "Book Table 5.7\nBenchmark",
      "Final Exploitation\nRate (1948-2024)"
    ),
    group = c(
      "source", "source", "source", "source",
      "calculation", "calculation", "calculation", "validation",
      "output"
    ),
    level = c(1, 1, 1, 1, 2, 2, 3, 4, 5),
    title = c(
      "BEA NIPA Table 1.12<br>Industry Value Added",
      "BEA NIPA Compensation<br>Wages and Salaries",
      "BLS Employment<br>by Industry",
      "Mohun (2005) Classification<br>Productive/Unproductive",
      "VA* = Σ(VAᵢ × Pᵢ)<br>Where P = productive ratio",
      "W* = Σ(Wᵢ × Pᵢ)<br>Productive workers' wages",
      "e = (VA* - W*) / W*<br>Rate of surplus value",
      "Shaikh-Tonak (1994) Table 5.7<br>e = 1.70 (1948) → 2.44 (1989)",
      "Extended series<br>77 annual observations"
    ),
    stringsAsFactors = FALSE
  )

  edges <- data.frame(
    from = c(
      "nipa_va", "nipa_wages", "employment", "industry_class",
      "industry_class", "va_star", "w_star",
      "exploitation_raw", "book_benchmark"
    ),
    to = c(
      "va_star", "w_star", "industry_class", "va_star",
      "w_star", "exploitation_raw", "exploitation_raw",
      "book_benchmark", "exploitation_final"
    ),
    label = c(
      "VA by\nIndustry", "Wages by\nIndustry", "Employment\nRatios", "Productive\nWeights",
      "Productive\nWeights", "VA*", "W*",
      "Raw e", "Validated e"
    ),
    arrows = "to",
    stringsAsFactors = FALSE
  )

  return(list(nodes = nodes, edges = edges))
}


# -----------------------------------------------------------------------------
# VISUALIZATION FUNCTIONS
# -----------------------------------------------------------------------------

#' Render an interactive lineage graph
#'
#' Creates a visNetwork visualization of the data lineage for a given series.
#'
#' @param series_id Character string identifying the series
#'   ("profit_rate", "exploitation_rate", "employment", "nsw")
#' @param height Height of the visualization in pixels
#' @param width Width of the visualization in pixels
#'
#' @return visNetwork object
#'
#' @examples
#' render_lineage_graph("profit_rate")
#' render_lineage_graph("exploitation_rate", height = "600px")
render_lineage_graph <- function(series_id = "profit_rate",
                                  height = "500px",
                                  width = "100%") {

  # Get lineage data based on series
  lineage <- switch(series_id,
    "profit_rate" = get_profit_rate_lineage(),
    "exploitation_rate" = get_exploitation_rate_lineage(),
    # Default to profit rate
    get_profit_rate_lineage()
  )

  nodes <- lineage$nodes
  edges <- lineage$edges

  # Define colors by group
  nodes$color <- case_when(
    nodes$group == "source" ~ "#4CAF50",      # Green for data sources
    nodes$group == "calculation" ~ "#2196F3", # Blue for calculations
    nodes$group == "validation" ~ "#FF9800",  # Orange for validation
    nodes$group == "output" ~ "#9C27B0",      # Purple for final output
    TRUE ~ "#607D8B"                           # Grey default
  )

  # Define shapes by group
  nodes$shape <- case_when(
    nodes$group == "source" ~ "database",
    nodes$group == "calculation" ~ "box",
    nodes$group == "validation" ~ "diamond",
    nodes$group == "output" ~ "star",
    TRUE ~ "dot"
  )

  # Build the network
  visNetwork(nodes, edges, height = height, width = width) %>%
    visNodes(
      font = list(size = 12, face = "arial"),
      borderWidth = 2,
      borderWidthSelected = 4,
      shadow = TRUE
    ) %>%
    visEdges(
      arrows = "to",
      smooth = list(type = "cubicBezier"),
      color = list(color = "#848484", highlight = "#FF5722"),
      font = list(size = 10, align = "middle")
    ) %>%
    visHierarchicalLayout(
      direction = "UD",       # Up-down layout
      levelSeparation = 100,
      nodeSpacing = 150,
      sortMethod = "directed"
    ) %>%
    visOptions(
      highlightNearest = list(enabled = TRUE, degree = 1, hover = TRUE),
      nodesIdSelection = TRUE,
      selectedBy = "group"
    ) %>%
    visInteraction(
      hover = TRUE,
      hoverConnectedEdges = TRUE,
      tooltipStyle = "position: fixed; visibility: visible; padding: 10px;"
    ) %>%
    visPhysics(enabled = FALSE) %>%  # Disable physics for hierarchical layout
    visLegend(
      addNodes = data.frame(
        label = c("Data Source", "Calculation", "Validation", "Output"),
        shape = c("database", "box", "diamond", "star"),
        color = c("#4CAF50", "#2196F3", "#FF9800", "#9C27B0")
      ),
      useGroups = FALSE,
      position = "right",
      width = 0.15
    )
}


#' Create a simple lineage text representation
#'
#' For non-interactive display or export.
#'
#' @param series_id Series identifier
#' @return Character string with ASCII lineage representation
render_lineage_text <- function(series_id = "profit_rate") {

  if (series_id == "profit_rate") {
    text <- "
PROFIT RATE DATA LINEAGE
========================

[BEA NIPA 1966] → [Rebase 1958] → [Splice 1919] → [Fed G.17] → [Splice 2010] → [FRED INDPRO] → [Final Series]

Detailed Chain:
───────────────
1. BEA NIPA Tables (1929-2025)
   └─→ Value Added, Wages, Fixed Assets
       └─→ Capital Stock (K)
       └─→ Surplus Value (S = VA - W)

2. BEA I-O Tables (1947-1982)
   └─→ Technical Coefficients
       └─→ Labor Value Coefficients (λ*)
   └─→ Employment Distribution
       └─→ Productive/Unproductive Ratio (Lp/L)

3. FRED Capacity Utilization
   └─→ Utilization Rate (u)

4. Calculation: r = S / (K × u)
   └─→ Raw Profit Rate Series

5. Validation vs Book Tables 5.4-5.8
   └─→ 93.8% exact matches
   └─→ MAE = 0.000937

6. Final Output: Profit Rate Series (1948-2024)
"
  } else if (series_id == "exploitation_rate") {
    text <- "
EXPLOITATION RATE DATA LINEAGE
==============================

Detailed Chain:
───────────────
1. NIPA Value Added by Industry
   └─→ Apply productive weights
       └─→ VA* (Productive Value Added)

2. NIPA Wages by Industry
   └─→ Apply productive weights
       └─→ W* (Productive Wages)

3. Industry Classification (Mohun 2005)
   └─→ Productive ratios by industry
   └─→ Employment weights

4. Calculation: e = (VA* - W*) / W*
   └─→ Raw Exploitation Rate

5. Validation vs Book Table 5.7
   └─→ e = 1.70 (1948) verified
   └─→ e = 2.44 (1989) verified

6. Final Output: Exploitation Rate (1948-2024)
"
  } else {
    text <- "Series lineage not defined."
  }

  return(text)
}


# -----------------------------------------------------------------------------
# SHINY MODULE
# -----------------------------------------------------------------------------

#' Lineage Visualization UI Module
#'
#' @param id Module namespace ID
lineageVizUI <- function(id) {
  ns <- NS(id)

  tagList(
    fluidRow(
      column(4,
        selectInput(
          ns("series_select"),
          "Select Data Series:",
          choices = c(
            "Profit Rate" = "profit_rate",
            "Exploitation Rate" = "exploitation_rate"
          ),
          selected = "profit_rate"
        )
      ),
      column(4,
        selectInput(
          ns("view_mode"),
          "View Mode:",
          choices = c(
            "Interactive Graph" = "graph",
            "Text Diagram" = "text"
          ),
          selected = "graph"
        )
      ),
      column(4,
        actionButton(
          ns("refresh_btn"),
          "Refresh",
          icon = icon("sync"),
          class = "btn-primary"
        )
      )
    ),
    hr(),
    conditionalPanel(
      condition = sprintf("input['%s'] == 'graph'", ns("view_mode")),
      visNetworkOutput(ns("lineage_graph"), height = "500px")
    ),
    conditionalPanel(
      condition = sprintf("input['%s'] == 'text'", ns("view_mode")),
      verbatimTextOutput(ns("lineage_text"))
    ),
    hr(),
    h4("Data Sources"),
    htmlOutput(ns("source_info"))
  )
}


#' Lineage Visualization Server Module
#'
#' @param id Module namespace ID
lineageVizServer <- function(id) {
  moduleServer(id, function(input, output, session) {

    # Render interactive graph
    output$lineage_graph <- renderVisNetwork({
      input$refresh_btn  # Trigger on refresh
      render_lineage_graph(input$series_select)
    })

    # Render text diagram
    output$lineage_text <- renderText({
      render_lineage_text(input$series_select)
    })

    # Render source information
    output$source_info <- renderUI({
      series <- input$series_select

      if (series == "profit_rate") {
        HTML("
          <ul>
            <li><strong>BEA NIPA</strong>: <a href='https://www.bea.gov/data/national-accounts' target='_blank'>bea.gov/data/national-accounts</a></li>
            <li><strong>FRED</strong>: <a href='https://fred.stlouisfed.org/series/CAPUTLB00004S' target='_blank'>Capacity Utilization</a></li>
            <li><strong>BLS</strong>: <a href='https://www.bls.gov/data/' target='_blank'>Employment Statistics</a></li>
            <li><strong>Methodology</strong>: Shaikh & Tonak (1994) Chapter 5</li>
          </ul>
        ")
      } else {
        HTML("
          <ul>
            <li><strong>BEA NIPA</strong>: Value Added and Compensation by Industry</li>
            <li><strong>Classification</strong>: Mohun (2005, 2013) Productive Labor</li>
            <li><strong>Benchmark</strong>: Shaikh & Tonak (1994) Table 5.7</li>
          </ul>
        ")
      }
    })
  })
}


# -----------------------------------------------------------------------------
# EXPORTS
# -----------------------------------------------------------------------------

# Export functions for use in main app
# These can be called directly or via the Shiny module

# Example usage in app.R:
# source("R/lineage_viz.R")
#
# # Option 1: Direct use
# output$lineage <- renderVisNetwork({
#   render_lineage_graph(input$series_id)
# })
#
# # Option 2: Module use
# lineageVizUI("lineage_module")
# lineageVizServer("lineage_module")
