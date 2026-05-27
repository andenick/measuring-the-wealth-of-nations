# RMWND Shiny — global.R
# Library loads, configuration, data loading, and validation.
# Sourced once at app startup before UI/server.

library(shiny)
library(shinydashboard)
library(plotly)
library(jsonlite)
library(readr)
library(DT)

# Source modules
source("R/helpers.R")
source("R/logger.R")
source("R/config.R")
source("R/data_loader.R")
source("R/chart_builder.R")
source("R/validate_data.R")

log_section("RMWND Shiny App — Startup")

# Load configuration
APP_CONFIG <- load_app_config(RMWND_PATHS$config)
VIZ_STYLE <- load_viz_style(RMWND_PATHS$style)

# Load series registry and build catalog
log_info("Loading series registry from: %s", RMWND_PATHS$registry)
SERIES_REGISTRY <- load_series_registry(RMWND_PATHS$registry)
log_info("Registry contains %d series", length(SERIES_REGISTRY))

log_info("Building series catalog from chopped directory: %s", RMWND_PATHS$chopped_dir)
SERIES_CATALOG <- build_series_catalog(SERIES_REGISTRY, RMWND_PATHS$chopped_dir)
loaded_count <- sum(vapply(SERIES_CATALOG, function(s) isTRUE(s$has_data), logical(1)))
log_info("Catalog built: %d series, %d with data", length(SERIES_CATALOG), loaded_count)

# Load quotes if available
QUOTES_MASTER <- load_quotes_master(RMWND_PATHS$quotes)

# Load subsource metadata for validation
SUBSOURCE_META <- tryCatch(
  jsonlite::fromJSON(RMWND_PATHS$subsource_metadata, simplifyVector = FALSE),
  error = function(e) {
    log_warn("No subsource metadata: %s", e$message)
    NULL
  }
)

# Run startup validation (anu-visualize v6.0 standard)
VALIDATION_RESULTS <- validate_app_data(RMWND_PATHS, SERIES_REGISTRY, SERIES_CATALOG, SUBSOURCE_META)
print_validation_results(VALIDATION_RESULTS)
log_structured("startup_validation", list(
  gate = VALIDATION_RESULTS$gate,
  errors = VALIDATION_RESULTS$error_count,
  warnings = VALIDATION_RESULTS$warning_count
))

# Tab configuration from app_config
TABS <- APP_CONFIG$tabs %||% list()
DEFAULT_TAB <- APP_CONFIG$default_tab %||% "ch5"
YEAR_RANGE <- as.numeric(unlist(APP_CONFIG$year_range %||% list(1925, 2025)))
DEFAULT_YEAR_RANGE <- as.numeric(unlist(APP_CONFIG$default_year_range %||% list(1929, 2025)))

# Build tab choices for UI
TAB_CHOICES <- setNames(
  names(TABS),
  vapply(TABS, function(t) t$label %||% "Unknown", character(1))
)

log_section("Startup Complete")
log_info("Tabs: %s", paste(names(TABS), collapse = ", "))
log_info("Loaded: %d / %d series with data", loaded_count, length(SERIES_CATALOG))
log_info(
  "Validation: %s (%d errors, %d warnings)",
  VALIDATION_RESULTS$gate, VALIDATION_RESULTS$error_count, VALIDATION_RESULTS$warning_count
)
