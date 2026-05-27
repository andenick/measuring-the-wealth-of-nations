# RMWND Shiny — Data Loader
# Loads series_registry.json, chopped CSVs, and catalog JSONs.

load_app_config <- function(path) {
  if (!file.exists(path)) {
    log_warn("app_config.json not found at %s", path)
    return(list())
  }
  jsonlite::fromJSON(path, simplifyVector = FALSE)
}

load_viz_style <- function(path) {
  if (!file.exists(path)) {
    log_warn("viz_style.json not found at %s", path)
    return(list())
  }
  jsonlite::fromJSON(path, simplifyVector = FALSE)
}

load_series_registry <- function(path) {
  if (!file.exists(path)) {
    log_warn("series_registry.json not found at %s", path)
    return(list())
  }
  reg <- jsonlite::fromJSON(path, simplifyVector = FALSE)
  if (!is.null(reg$series)) {
    return(reg$series)
  }
  reg
}

load_quotes_master <- function(path) {
  if (!file.exists(path) || is.na(path)) {
    return(list())
  }
  tryCatch(
    jsonlite::fromJSON(path, simplifyVector = FALSE),
    error = function(e) {
      log_warn("Failed to load quotes: %s", e$message)
      list()
    }
  )
}

load_chopped_csv <- function(series_id, chopped_dir) {
  pattern <- paste0("^", series_id, "[_.]")
  files <- list.files(chopped_dir, pattern = pattern, full.names = TRUE, ignore.case = TRUE)
  if (length(files) == 0) {
    csv_path <- file.path(chopped_dir, paste0(series_id, ".csv"))
    if (!file.exists(csv_path)) {
      return(NULL)
    }
    files <- csv_path
  }
  tryCatch(
    {
      df <- readr::read_csv(files[1], skip = 1, show_col_types = FALSE)
      if (!"year" %in% names(df) && "Year" %in% names(df)) names(df)[names(df) == "Year"] <- "year"
      df <- df[, !grepl("^\\.\\.\\.|^X\\d*$", names(df)), drop = FALSE]
      df
    },
    error = function(e) {
      log_warn("Failed to load chopped CSV for %s: %s", series_id, e$message)
      NULL
    }
  )
}

derive_extension_status <- function(entry) {
  status <- safe_str(entry, "status", "")
  has_ext <- !is.null(safe_field(entry, "extension"))

  if (grepl("validated_book_and_extension", status)) {
    return("extended_2025")
  }
  if (has_ext && status == "book_period_validated") {
    return("extended_2025")
  }
  if (status == "book_period_validated") {
    return("verified")
  }
  if (grepl("partial", status)) {
    return("partial")
  }
  if (status == "benchmark_only_matrix_derived") {
    return("calculated")
  }
  if (status == "data_unavailable") {
    return("not_applicable")
  }
  if (grepl("^pending", status)) {
    return("conceptual")
  }
  "conceptual"
}

build_series_catalog <- function(registry, chopped_dir) {
  catalog <- list()
  for (sid in names(registry)) {
    entry <- registry[[sid]]
    chopped <- load_chopped_csv(sid, chopped_dir)

    yr <- safe_field(entry, "year_range", list())
    tp_start <- if (length(yr) >= 1) yr[[1]] else safe_field(entry, "time_period_start")
    tp_end <- if (length(yr) >= 2) yr[[2]] else safe_field(entry, "time_period_end")

    subsources <- safe_field(
      entry, "subsources",
      safe_field(entry, "subseries", list())
    )

    catalog[[sid]] <- list(
      series_id = sid,
      name = safe_str(entry, "name", sid),
      chapter = safe_field(entry, "chapter"),
      units = safe_str(entry, "units", ""),
      time_period_start = tp_start,
      time_period_end = tp_end,
      extension_status = derive_extension_status(entry),
      construction_formula = safe_str(entry, "construction_formula", ""),
      shaikh_quote = safe_str(entry, "shaikh_quote", ""),
      shaikh_quote_page = safe_str(entry, "shaikh_quote_page", ""),
      api_sources = safe_field(entry, "api_sources", list()),
      subsource_count = length(subsources),
      subsources = subsources,
      figure_ids = safe_field(
        entry, "figures",
        safe_field(entry, "figure_ids", list())
      ),
      methodology_note = safe_str(entry, "methodology_note", ""),
      has_data = !is.null(chopped),
      data = chopped
    )
  }
  catalog
}

get_tab_series <- function(catalog, tab_series_ids) {
  Filter(function(s) s$series_id %in% tab_series_ids, catalog)
}

get_series_data <- function(catalog, series_id) {
  entry <- catalog[[series_id]]
  if (is.null(entry)) {
    return(NULL)
  }
  entry$data
}
