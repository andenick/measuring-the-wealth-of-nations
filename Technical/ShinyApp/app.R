# ============================================
# SHAIKH-TONAK MARXIAN ANALYSIS SHINY APP
# ============================================
# Comprehensive Presentation Tool for Professor Tonak
# Interactive visualization of Marxian economic indicators (1948-2024)
# Multi-methodology comparison: ST94, M05, TP19
# Based on Shaikh & Tonak (1994) "Measuring the Wealth of Nations"
#
# Author: Arcanum Project
# Date: December 7, 2025
# Version: 2.0 - Professor Tonak Presentation Edition
# ============================================
# NEW FEATURES:
# - Extended coverage: 1948-2024 (vs original 1948-1989)
# - Multi-methodology comparison (ST94, M05, TP19)
# - Industry classification schema (SIC/NAICS)
# - HDARP-extracted literature citations with page references
# - Questions for Professor Tonak section
# - Book vs Implementation validation
# ============================================

# Load required packages
library(shiny)
library(shinydashboard)
library(tidyverse)
library(plotly)
library(DT)
library(scales)
library(writexl) # For Excel export
library(zip) # For ZIP creation

# ============================================
# PATH CONFIGURATION
# ============================================
source("config.R")
source("R/data_loader.R")
source("R/chart_builder.R")

# ============================================
# DATA LOADING
# ============================================

# Define data directory (using config-based path)
data_dir <- AS2_PATHS$data_root

# Load profit rates data (extended 1948-2024)
profit_rates <- tryCatch(
  {
    # Try extended version first, fall back to original
    extended_file <- file.path(data_dir, "profit_rates_1948_2024.csv")
    original_file <- file.path(data_dir, "profit_rates_1948_1989.csv")

    if (file.exists(extended_file)) {
      data <- read_csv(extended_file, show_col_types = FALSE)
    } else {
      data <- read_csv(original_file, show_col_types = FALSE)
    }

    if (!("r_star_pct" %in% names(data))) {
      stop("Missing required column: r_star_pct")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading profit_rates:", e$message))
  }
)

# Load exploitation and composition data (extended 1948-2024)
exploitation <- tryCatch(
  {
    extended_file <- file.path(data_dir, "exploitation_composition_1948_2024.csv")
    original_file <- file.path(data_dir, "exploitation_composition_1948_1989.csv")

    if (file.exists(extended_file)) {
      data <- read_csv(extended_file, show_col_types = FALSE)
    } else {
      data <- read_csv(original_file, show_col_types = FALSE)
    }

    if (!("exploitation_rate" %in% names(data))) {
      stop("Missing required column: exploitation_rate")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading exploitation:", e$message))
  }
)

# Load employment data (extended 1948-2024)
employment <- tryCatch(
  {
    extended_file <- file.path(data_dir, "employment_1948_2024.csv")
    original_file <- file.path(data_dir, "employment_1948_1989.csv")

    if (file.exists(extended_file)) {
      data <- read_csv(extended_file, show_col_types = FALSE)
      # Normalize column names for compatibility
      if ("L_total_k" %in% names(data) && !("L_total" %in% names(data))) {
        data <- data %>% mutate(L_total = L_total_k)
      }
      if ("Lp_k" %in% names(data) && !("Lp" %in% names(data))) {
        data <- data %>% mutate(Lp = Lp_k)
      }
      if ("Lu_k" %in% names(data) && !("Lu" %in% names(data))) {
        data <- data %>% mutate(Lu = Lu_k)
      }
    } else {
      data <- read_csv(original_file, show_col_types = FALSE)
    }

    # Check for either column name version
    if (!("L_total" %in% names(data)) && !("L_total_k" %in% names(data))) {
      stop("Missing required column: L_total or L_total_k")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading employment:", e$message))
  }
)

# Load productivity data
productivity <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "productivity_1948_1989.csv"),
      show_col_types = FALSE
    )
    if (!("marxian_productivity" %in% names(data))) {
      stop("Missing required column: marxian_productivity")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading productivity:", e$message))
  }
)

# Load government data
government <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "government_1948_1989.csv"),
      show_col_types = FALSE
    )
    if (!("G_total" %in% names(data))) {
      stop("Missing required column: G_total")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading government:", e$message))
  }
)

# Load validation targets
validation_targets <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "validation_targets.csv"),
      show_col_types = FALSE
    )
    if (!("r_star_adjusted" %in% names(data))) {
      stop("Missing required column: r_star_adjusted")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading validation_targets:", e$message))
  }
)

# Load comprehensive dataset
comprehensive <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "comprehensive_1948_1989.csv"),
      show_col_types = FALSE
    )
    if (!("year" %in% names(data))) {
      stop("Missing required column: year")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading comprehensive:", e$message))
  }
)

# Load questions dataset
questions <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "shaikh_tonak_questions.csv"),
      show_col_types = FALSE
    )
    if (!("Question" %in% names(data))) {
      stop("Missing required column: Question")
    }
    data
  },
  error = function(e) {
    stop(paste("Error loading questions:", e$message))
  }
)

# ============================================
# NEW DATA FOR PROFESSOR TONAK PRESENTATION
# ============================================

# Load methodology comparison data (ST94 vs M05 vs TP19)
methodology_comparison <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "methodology_comparison_1948_2024.csv"),
      show_col_types = FALSE
    )
    data
  },
  error = function(e) {
    # Create empty placeholder if file doesn't exist
    tibble(Year = integer(), Period = character(), ST94_e = numeric())
  }
)

# Load industry classification matrix
industry_classification <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "industry_classification_matrix.csv"),
      show_col_types = FALSE
    )
    data
  },
  error = function(e) {
    tibble(Industry = character(), SIC_Code = character())
  }
)

# Load literature citations with HDARP page references
literature_citations <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "literature_citations.csv"),
      show_col_types = FALSE
    )
    data
  },
  error = function(e) {
    tibble(Citation_ID = character(), Authors = character())
  }
)

# Load questions specifically for Professor Tonak
questions_for_tonak <- tryCatch(
  {
    data <- read_csv(file.path(data_dir, "questions_for_tonak.csv"),
      show_col_types = FALSE
    )
    data
  },
  error = function(e) {
    tibble(Question_Number = integer(), Question = character())
  }
)

# Load Mohun comparison data
mohun_comparison <- tryCatch(
  read_csv(file.path(data_dir, "mohun_comparison.csv"), show_col_types = FALSE),
  error = function(e) tibble(year = integer())
)

# Load Moos NSW comparison data
moos_nsw_comparison <- tryCatch(
  read_csv(file.path(data_dir, "moos_nsw_comparison.csv"), show_col_types = FALSE),
  error = function(e) tibble(year = integer())
)

# Load international NSW data
international_nsw <- tryCatch(
  read_csv(file.path(data_dir, "international_nsw.csv"), show_col_types = FALSE),
  error = function(e) tibble(year = integer())
)

# Load NSW extended data
nsw_extended <- tryCatch(
  {
    ext_file <- file.path(data_dir, "nsw_1952_2025.csv")
    orig_file <- file.path(data_dir, "nsw_1952_1989.csv")
    if (file.exists(ext_file)) read_csv(ext_file, show_col_types = FALSE)
    else read_csv(orig_file, show_col_types = FALSE)
  },
  error = function(e) tibble(year = integer())
)

# ============================================
# FIGURE & SERIES CATALOG DATA
# ============================================

# Load figure catalog (JSON array -> data.frame)
figure_catalog_df <- tryCatch(
  {
    raw <- jsonlite::fromJSON(
      file.path(AS2_PATHS$shiny_root, "..", "FIGURE_SERIES_CATALOG.json"),
      simplifyDataFrame = TRUE
    )
    # series_ids is a list column; convert to comma-separated string for display
    raw$series_ids_str <- sapply(raw$series_ids, function(x) {
      if (length(x) == 0) "" else paste(x, collapse = ", ")
    })
    raw
  },
  error = function(e) {
    warning(paste("Could not load FIGURE_SERIES_CATALOG.json:", e$message))
    tibble(
      figure_id = character(), chapter = integer(), title = character(),
      type = character(), is_empirical = logical(), series_ids = list(),
      series_ids_str = character(), year_start = integer(), year_end = integer(),
      description = character()
    )
  }
)

# Load series catalog (named list from JSON)
series_catalog <- tryCatch(
  {
    raw <- jsonlite::fromJSON(
      file.path(AS2_PATHS$shiny_root, "..", "ANU_REPLICATOR", "data", "final-data", "shiny", "series_catalog.json")
    )
    raw$series  # the "series" key holds the named list
  },
  error = function(e) {
    warning(paste("Could not load series_catalog.json:", e$message))
    list()
  }
)

# Load figure column map
figure_column_map <- tryCatch(
  {
    raw <- jsonlite::fromJSON(
      file.path(AS2_PATHS$shiny_root, "..", "ANU_REPLICATOR", "data", "final-data", "shiny", "figure_column_map.json")
    )
    raw$figure_column_map
  },
  error = function(e) {
    warning(paste("Could not load figure_column_map.json:", e$message))
    list()
  }
)

# Path to per-chapter CSV data for figure previews
figures_data_path <- file.path(AS2_PATHS$shiny_root, "..", "ANU_REPLICATOR", "data", "final-data", "shiny")

# Determine year range from loaded data
max_year <- max(profit_rates$year, na.rm = TRUE)
min_year <- min(profit_rates$year, na.rm = TRUE)
is_extended <- max_year > 1989

# Create unified long-format dataset for flexible filtering
all_series_long <- bind_rows(
  # Profit rates
  profit_rates %>%
    select(year, value = r_star_pct) %>%
    mutate(series = "Marxian r*", units = "Percent", category = "Profit Rates"),
  profit_rates %>% select(year, value = r_star_adj_pct) %>%
    mutate(series = "Marxian r* (capacity-adj)", units = "Percent", category = "Profit Rates"),
  profit_rates %>% select(year, value = r_nipa_pct) %>%
    mutate(series = "NIPA r", units = "Percent", category = "Profit Rates"),
  profit_rates %>% select(year, value = r_nipa_adj_pct) %>%
    mutate(series = "NIPA r (capacity-adj)", units = "Percent", category = "Profit Rates"),
  profit_rates %>% select(year, value = capacity_utilization) %>%
    mutate(series = "Capacity Utilization", units = "Ratio", category = "Profit Rates"),

  # Exploitation and composition
  exploitation %>%
    select(year, value = exploitation_rate) %>%
    mutate(series = "Exploitation Rate (S*/V*)", units = "Ratio", category = "Exploitation"),
  exploitation %>% select(year, value = surplus_ratio) %>%
    mutate(series = "Surplus Ratio (S*/Y)", units = "Ratio", category = "Exploitation"),
  exploitation %>% select(year, value = value_composition) %>%
    mutate(series = "Value Composition (C*/V*)", units = "Ratio", category = "Composition"),
  exploitation %>% select(year, value = materialized_composition) %>%
    mutate(series = "Materialized Composition", units = "Ratio", category = "Composition"),

  # Employment
  employment %>%
    select(year, value = Lp_L_ratio) %>%
    mutate(series = "Productive Share (Lp/L)", units = "Ratio", category = "Employment"),
  employment %>% select(year, value = Lu_L_ratio) %>%
    mutate(series = "Unproductive Share (Lu/L)", units = "Ratio", category = "Employment"),

  # Productivity
  productivity %>%
    select(year, value = marxian_index) %>%
    mutate(series = "Marxian Productivity Index", units = "Index (1948=100)", category = "Productivity"),
  productivity %>% select(year, value = conventional_index) %>%
    mutate(series = "Conventional Productivity Index", units = "Index (1948=100)", category = "Productivity"),
  productivity %>% select(year, value = bls_productivity_index) %>%
    mutate(series = "BLS Productivity Index", units = "Index (1948=100)", category = "Productivity"),

  # Government
  government %>%
    select(year, value = G_S_ratio) %>%
    mutate(series = "Government/Surplus (G/S*)", units = "Ratio", category = "Government"),
  government %>% select(year, value = G_GDP_ratio) %>%
    mutate(series = "Government/GDP (G/GDP)", units = "Ratio", category = "Government")
) %>%
  filter(!is.na(value)) # Remove any missing values

# Define recession periods (NBER dates 1948-1989)
# Define recession periods (NBER dates 1948-2024)
recessions <- tibble(
  start = c(1948, 1953, 1957, 1960, 1969, 1973, 1980, 1981, 1990, 2001, 2007, 2020),
  end = c(1949, 1954, 1958, 1961, 1970, 1975, 1980, 1982, 1991, 2001, 2009, 2020),
  label = c(
    "1948-49", "1953-54", "1957-58", "1960-61",
    "1969-70", "1973-75", "1980", "1981-82",
    "1990-91", "2001", "2007-09 Great Recession", "2020 COVID"
  )
)

# Define color scheme
colors <- list(
  primary = "#3c8dbc", # Blue
  success = "#00a65a", # Green
  warning = "#f39c12", # Orange
  danger = "#dd4b39", # Red
  info = "#00c0ef", # Light blue
  purple = "#605ca8", # Purple
  teal = "#39cccc", # Teal
  gray = "#d2d6de", # Gray
  book_period = "#3c8dbc", # Blue for validated book period
  extension = "#f39c12", # Orange for extension period
  transition = "#605ca8" # Purple for SIC-NAICS transition
)

# ============================================
# USER INTERFACE
# ============================================
# UI definition moved to ui.R
# Tab definitions moved to R/ui_tabs.R
# ============================================

source("ui.R")

# ============================================
# SERVER LOGIC
# ============================================
# Server definition moved to server.R
# Server logic moved to R/server_logic.R
# ============================================

source("server.R")

# ============================================
# RUN APPLICATION
# ============================================

shinyApp(ui = ui, server = server)
