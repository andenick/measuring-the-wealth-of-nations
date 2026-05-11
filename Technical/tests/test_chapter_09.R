# ============================================
# test_chapter_09.R — Chapter 9 Integration Tests
# ============================================
# 8 test sections required by Anu Review:
#   1. SERIES_METADATA
#   2. MAPPING_FIELDS
#   3. DATA_FILES
#   4. DPR_EXISTENCE
#   5. FIGURES
#   6. HELPERS
#   7. THEMATIC_BENCHMARKS
#   8. CROSS_CHAPTER
#
# Anu Standard v2.0 — Test Coverage Component
# Created: 2026-02-26 (Session 10 — Chapter 9 Build)
# Depends on: data_loader.R (CH9_SERIES_MAPPING), chart_builder.R, FIGURE_SERIES_CATALOG.json
# ============================================

library(testthat)
library(here)
library(jsonlite)

# ============================================
# SETUP — Source dependencies
# ============================================

project_root <- here::here()

# Source data_loader.R for CH9_SERIES_MAPPING
tryCatch(
  source(file.path(project_root, "ShinyApp", "R", "data_loader.R")),
  error = function(e) {
    if (!exists("AS2_PATHS")) {
      AS2_PATHS <<- list(
        inputs_root = file.path(project_root, "..", "Inputs"),
        data_root = file.path(project_root, "ShinyApp", "data"),
        st_chopped = file.path(project_root, "..", "Inputs", "ST_Chopped")
      )
    }
    source(file.path(project_root, "ShinyApp", "R", "data_loader.R"))
  }
)

# Source chart_builder.R for helper functions
tryCatch(
  source(file.path(project_root, "ShinyApp", "R", "chart_builder.R")),
  error = function(e) warning("chart_builder.R could not be loaded: ", e$message)
)

# Load FIGURE_SERIES_CATALOG.json
figure_catalog_path <- file.path(project_root, "FIGURE_SERIES_CATALOG.json")
figure_catalog <- if (file.exists(figure_catalog_path)) {
  fromJSON(figure_catalog_path)
} else {
  NULL
}

# Paths
docs_series_dir <- file.path(project_root, "docs", "series")
chopped_dir <- file.path(project_root, "..", "Inputs", "ST_Chopped", "ch09")
shiny_data_dir <- file.path(project_root, "ShinyApp", "data")

# ============================================
# 1. SERIES_METADATA
# ============================================

context("Chapter 9 Integration Tests — SERIES_METADATA")

test_that("SERIES_METADATA: CH9_SERIES_MAPPING exists and has 1 entry", {
  expect_true(exists("CH9_SERIES_MAPPING"))
  expect_equal(length(CH9_SERIES_MAPPING), 1)
})

test_that("SERIES_METADATA: T901 present as key", {
  actual_ids <- names(CH9_SERIES_MAPPING)
  expect_true("T901" %in% actual_ids, info = "T901 missing from mapping")
})

test_that("SERIES_METADATA: all series IDs are T9xx", {
  ids <- names(CH9_SERIES_MAPPING)
  expect_true(all(grepl("^T9\\d{2}$", ids)))
  chapters <- as.integer(substr(ids, 2, 2))
  expect_true(all(chapters == 9))
})

test_that("SERIES_METADATA: T901 is key series and extended", {
  t901 <- CH9_SERIES_MAPPING[["T901"]]
  expect_false(is.null(t901))
  expect_true(t901$is_key_series)
  expect_true(t901$is_extended)
})

# ============================================
# 2. MAPPING_FIELDS
# ============================================

context("Chapter 9 Integration Tests — MAPPING_FIELDS")

test_that("MAPPING_FIELDS: each entry has required fields", {
  required_fields <- c("name", "description", "formula", "data_patterns",
                        "is_extended", "is_conceptual", "is_key_series")
  for (id in names(CH9_SERIES_MAPPING)) {
    entry <- CH9_SERIES_MAPPING[[id]]
    for (field in required_fields) {
      expect_false(is.null(entry[[field]]),
                   info = paste(id, "missing field:", field))
    }
  }
})

test_that("MAPPING_FIELDS: each entry has subsources", {
  for (id in names(CH9_SERIES_MAPPING)) {
    entry <- CH9_SERIES_MAPPING[[id]]
    expect_true(length(entry$subsources) > 0,
                info = paste(id, "has no subsources"))
  }
})

test_that("MAPPING_FIELDS: each entry has book_table reference", {
  for (id in names(CH9_SERIES_MAPPING)) {
    entry <- CH9_SERIES_MAPPING[[id]]
    expect_false(is.null(entry$book_table),
                 info = paste(id, "missing book_table"))
  }
})

test_that("MAPPING_FIELDS: T901 subsources reference Ch5 and Ch6 series", {
  t901 <- CH9_SERIES_MAPPING[["T901"]]
  subs <- t901$subsources
  expect_true(any(grepl("T506", subs)), info = "T901 should reference T506")
  expect_true(any(grepl("T511", subs)), info = "T901 should reference T511")
  expect_true(any(grepl("T608", subs)), info = "T901 should reference T608")
})

# ============================================
# 3. DATA_FILES
# ============================================

context("Chapter 9 Integration Tests — DATA_FILES")

test_that("DATA_FILES: summary indicators book-period CSV exists", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  expect_true(file.exists(path), info = "summary_indicators_1948_1989.csv not found")
})

test_that("DATA_FILES: summary indicators extended CSV exists", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_2024.csv")
  expect_true(file.exists(path), info = "summary_indicators_1948_2024.csv not found")
})

test_that("DATA_FILES: book-period CSV has correct year range", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  expect_true("year" %in% names(df))
  expect_equal(min(df$year), 1948)
  expect_equal(max(df$year), 1989)
})

test_that("DATA_FILES: extended CSV covers 1948-2024", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_2024.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_2024.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  expect_true("year" %in% names(df))
  expect_equal(min(df$year), 1948)
  expect_true(max(df$year) >= 2024)
})

test_that("DATA_FILES: Chopped CSV exists in ST_Chopped/ch09", {
  skip_if_not(dir.exists(chopped_dir), "ST_Chopped/ch09/ directory not found")

  path <- file.path(chopped_dir, "Table9_1_SummaryIndicators.csv")
  expect_true(file.exists(path), info = "Table9_1_SummaryIndicators.csv not found")
})

test_that("DATA_FILES: book-period CSV has expected columns", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  expected_cols <- c("year", "T506_exploitation_rate", "T511_productive_labor_share",
                     "T512_productive_wage_share", "T513_marxian_profit_rate",
                     "T514_capacity_adj_profit_rate", "T608_nsw_v_star")
  for (col in expected_cols) {
    expect_true(col %in% names(df), info = paste("Missing column:", col))
  }
})

# ============================================
# 4. DPR_EXISTENCE
# ============================================

context("Chapter 9 Integration Tests — DPR_EXISTENCE")

test_that("DPR_EXISTENCE: T901_DPR.md exists", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")

  path <- file.path(docs_series_dir, "T901_DPR.md")
  expect_true(file.exists(path), info = "Missing DPR: T901")
})

test_that("DPR_EXISTENCE: T901 DPR is non-empty (>100 bytes)", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")

  path <- file.path(docs_series_dir, "T901_DPR.md")
  skip_if_not(file.exists(path), "T901 DPR not found")
  expect_gt(file.info(path)$size, 100,
            info = "T901 DPR is too small")
})

# ============================================
# 5. FIGURES
# ============================================

context("Chapter 9 Integration Tests — FIGURES")

test_that("FIGURES: FIGURE_SERIES_CATALOG.json exists and parses", {
  expect_true(file.exists(figure_catalog_path),
              info = "FIGURE_SERIES_CATALOG.json not found")
  expect_false(is.null(figure_catalog))
})

test_that("FIGURES: catalog has Ch9 entries", {
  skip_if(is.null(figure_catalog), "Figure catalog not loaded")
  ch9_figs <- figure_catalog[figure_catalog$chapter == 9, ]
  expect_gte(nrow(ch9_figs), 5,
             info = "Expected at least 5 Ch9 figure entries")
})

test_that("FIGURES: all Ch9 figures are time_series type", {
  skip_if(is.null(figure_catalog), "Figure catalog not loaded")
  ch9_figs <- figure_catalog[figure_catalog$chapter == 9, ]
  skip_if(nrow(ch9_figs) == 0, "No Ch9 figures found")
  expect_true(all(ch9_figs$type == "time_series"))
})

test_that("FIGURES: all Ch9 figures are empirical", {
  skip_if(is.null(figure_catalog), "Figure catalog not loaded")
  ch9_figs <- figure_catalog[figure_catalog$chapter == 9, ]
  skip_if(nrow(ch9_figs) == 0, "No Ch9 figures found")
  expect_true(all(ch9_figs$is_empirical))
})

# ============================================
# 6. HELPERS
# ============================================

context("Chapter 9 Integration Tests — HELPERS")

test_that("HELPERS: is_chapter9_series works correctly", {
  expect_true(is_chapter9_series("T901"))
  expect_false(is_chapter9_series("T506"))
  expect_false(is_chapter9_series("T607"))
  expect_false(is_chapter9_series("T9001"))
  expect_false(is_chapter9_series("X901"))
})

test_that("HELPERS: get_series_metadata returns valid metadata for T901", {
  meta <- get_series_metadata("T901")
  expect_false(is.null(meta))
  expect_equal(meta$name, "Summary Table (Key Indicators)")
  expect_true(meta$is_extended)
  expect_true(meta$is_key_series)
  expect_true(length(meta$data_patterns) > 0)
})

test_that("HELPERS: get_chapter_series(9) returns 1 entry", {
  ch9 <- get_chapter_series(9)
  expect_equal(length(ch9), 1)
})

test_that("HELPERS: get_chapter_series(9) returns only T9xx series", {
  ch9 <- get_chapter_series(9)
  ids <- names(ch9)
  expect_true(all(grepl("^T9\\d{2}$", ids)))
})

test_that("HELPERS: build_chapter9_chart function exists", {
  expect_true(exists("build_chapter9_chart", mode = "function"))
})

test_that("HELPERS: build_summary_indicators_chart function exists", {
  expect_true(exists("build_summary_indicators_chart", mode = "function"))
})

# ============================================
# 7. THEMATIC_BENCHMARKS
# ============================================

context("Chapter 9 Integration Tests — THEMATIC_BENCHMARKS")

test_that("THEMATIC_BENCHMARKS: e(1948) = 1.70", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  e_1948 <- df[df$year == 1948, "T506_exploitation_rate"]
  skip_if(length(e_1948) == 0, "1948 not found")

  expect_equal(round(e_1948, 2), 1.70, tolerance = 0.01,
               info = "e(1948) should be 1.70")
})

test_that("THEMATIC_BENCHMARKS: e(1989) = 2.44", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  e_1989 <- df[df$year == 1989, "T506_exploitation_rate"]
  skip_if(length(e_1989) == 0, "1989 not found")

  expect_equal(round(e_1989, 2), 2.44, tolerance = 0.01,
               info = "e(1989) should be 2.44")
})

test_that("THEMATIC_BENCHMARKS: Lp/L(1989) = 0.36", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  lpl_1989 <- df[df$year == 1989, "T511_productive_labor_share"]
  skip_if(length(lpl_1989) == 0, "1989 not found")

  expect_equal(round(lpl_1989, 2), 0.36, tolerance = 0.01,
               info = "Lp/L(1989) should be 0.36")
})

test_that("THEMATIC_BENCHMARKS: exploitation rate rising over time", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  e_start <- df[df$year == 1948, "T506_exploitation_rate"]
  e_end <- df[df$year == 1989, "T506_exploitation_rate"]
  skip_if(length(e_start) == 0 || length(e_end) == 0, "Benchmark years not found")

  expect_gt(e_end, e_start,
            info = "Exploitation rate should rise from 1948 to 1989")
  # Should rise by roughly 44%
  pct_change <- (e_end - e_start) / e_start * 100
  expect_gt(pct_change, 30, info = "Exploitation rate should rise by >30%")
})

test_that("THEMATIC_BENCHMARKS: productive labor share falling over time", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  lpl_start <- df[df$year == 1948, "T511_productive_labor_share"]
  lpl_end <- df[df$year == 1989, "T511_productive_labor_share"]
  skip_if(length(lpl_start) == 0 || length(lpl_end) == 0, "Benchmark years not found")

  expect_lt(lpl_end, lpl_start,
            info = "Productive labor share should fall from 1948 to 1989")
})

# ============================================
# 8. CROSS_CHAPTER
# ============================================

context("Chapter 9 Integration Tests — CROSS_CHAPTER")

test_that("CROSS_CHAPTER: T901 exploitation rate matches Ch5 authoritative data", {
  summary_path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(summary_path), "summary_indicators_1948_1989.csv not found")

  auth_path <- file.path(project_root, "..", "Inputs", "BookTables", "ch05",
                         "[2025.12.05] shaikh_tonak_authoritative_1948_1989.csv")
  skip_if_not(file.exists(auth_path), "Authoritative CSV not found")

  summary_df <- read.csv(summary_path, stringsAsFactors = FALSE)
  auth_df <- read.csv(auth_path, stringsAsFactors = FALSE)

  # Check 5 benchmark years
  for (yr in c(1948, 1958, 1967, 1977, 1989)) {
    s_val <- summary_df[summary_df$year == yr, "T506_exploitation_rate"]
    a_val <- auth_df[auth_df$year == yr, "exploitation_rate"]
    skip_if(length(s_val) == 0 || length(a_val) == 0,
            paste("Year", yr, "not found"))
    expect_equal(round(s_val, 2), round(a_val, 2), tolerance = 0.02,
                 info = paste("T901 e(", yr, ") should match Ch5 authoritative"))
  }
})

test_that("CROSS_CHAPTER: T901 NSW/V* matches Ch6 data for 1989", {
  summary_path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  nsw_path <- file.path(shiny_data_dir, "nsw_1952_1989.csv")
  skip_if_not(file.exists(summary_path) && file.exists(nsw_path),
              "Required CSVs not found")

  summary_df <- read.csv(summary_path, stringsAsFactors = FALSE)
  nsw_df <- read.csv(nsw_path, stringsAsFactors = FALSE)

  s_t608 <- summary_df[summary_df$year == 1989, "T608_nsw_v_star"]
  n_t608 <- nsw_df[nsw_df$year == 1989, "T608_nsw_v_star_ratio"]
  skip_if(length(s_t608) == 0 || length(n_t608) == 0 || is.na(s_t608) || s_t608 == "",
          "T608 values not found for 1989")

  expect_equal(as.numeric(s_t608), as.numeric(n_t608), tolerance = 0.001,
               info = "T901 T608(1989) should match Ch6 nsw_1952_1989.csv")
})

test_that("CROSS_CHAPTER: T901 draws from both Ch5 and Ch6", {
  meta <- get_series_metadata("T901")
  expect_false(is.null(meta))

  # Subsources should reference both Ch5 (T5xx) and Ch6 (T6xx) series
  has_ch5 <- any(grepl("T5", meta$subsources))
  has_ch6 <- any(grepl("T6", meta$subsources))
  expect_true(has_ch5, info = "T901 should reference Ch5 series in subsources")
  expect_true(has_ch6, info = "T901 should reference Ch6 series in subsources")
})

test_that("CROSS_CHAPTER: extended summary has more rows than book period", {
  book_path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  ext_path <- file.path(shiny_data_dir, "summary_indicators_1948_2024.csv")
  skip_if_not(file.exists(book_path) && file.exists(ext_path),
              "Required CSVs not found")

  book_df <- read.csv(book_path, stringsAsFactors = FALSE)
  ext_df <- read.csv(ext_path, stringsAsFactors = FALSE)

  expect_gt(nrow(ext_df), nrow(book_df),
            info = "Extended summary should have more rows than book period")
})

# ============================================
# Summary
# ============================================

# ============================================
# 9. ARTIFACT_EXISTENCE — Per-series artifact checks
# ============================================

context("Chapter 9 Integration Tests — ARTIFACT_EXISTENCE")

# Paths for artifact checks
research_dir <- file.path(project_root, "research")
anu_chopped_dir <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "chopped")
extenbooks_dir <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "extenbooks")
series_csv_dir <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "series")

test_that("ARTIFACT_EXISTENCE: T901 research JSON exists", {
  skip_if_not(dir.exists(research_dir), "research/ directory not found")
  path <- file.path(research_dir, "T901_research.json")
  expect_true(file.exists(path), info = "Missing research JSON: T901")
})

test_that("ARTIFACT_EXISTENCE: T901 DECOMPOSITION file exists", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")
  path <- file.path(docs_series_dir, "T901_DECOMPOSITION.md")
  expect_true(file.exists(path), info = "Missing DECOMPOSITION: T901")
})

test_that("ARTIFACT_EXISTENCE: T901 chopped CSV exists (Anu format)", {
  skip_if_not(dir.exists(anu_chopped_dir), "ANU chopped/ directory not found")
  path <- file.path(anu_chopped_dir, "T901_chopped.csv")
  expect_true(file.exists(path), info = "Missing Anu chopped CSV: T901")
})

test_that("ARTIFACT_EXISTENCE: T901 extenbook exists", {
  skip_if_not(dir.exists(extenbooks_dir), "extenbooks/ directory not found")
  path <- file.path(extenbooks_dir, "T901_extenbook.xlsx")
  expect_true(file.exists(path), info = "Missing extenbook: T901")
})

test_that("ARTIFACT_EXISTENCE: T901 series CSV exists", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  path <- file.path(series_csv_dir, "T901.csv")
  expect_true(file.exists(path), info = "Missing series CSV: T901")
})

# ============================================
# 10. DATA_RANGE_CHECKS — Year and value range validation
# ============================================

context("Chapter 9 Integration Tests — DATA_RANGE_CHECKS")

test_that("DATA_RANGE_CHECKS: T901 series CSV has years >= 1929 and <= 2025", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  path <- file.path(series_csv_dir, "T901.csv")
  skip_if_not(file.exists(path), "T901.csv not found")
  df <- tryCatch(read.csv(path, stringsAsFactors = FALSE), error = function(e) NULL)
  skip_if(is.null(df) || !("year" %in% names(df)), "T901 cannot check years")
  years <- df$year[!is.na(df$year)]
  skip_if(length(years) == 0, "T901 no year values")
  expect_gte(min(years), 1929, info = paste("T901 has year <1929:", min(years)))
  expect_lte(max(years), 2025, info = paste("T901 has year >2025:", max(years)))
})

test_that("DATA_RANGE_CHECKS: summary indicators book-period years are 1948-1989", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")
  df <- read.csv(path, stringsAsFactors = FALSE)
  expect_equal(min(df$year), 1948, info = "Book period should start at 1948")
  expect_equal(max(df$year), 1989, info = "Book period should end at 1989")
})

test_that("DATA_RANGE_CHECKS: summary indicators extended years cover 1948-2024", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_2024.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_2024.csv not found")
  df <- read.csv(path, stringsAsFactors = FALSE)
  expect_equal(min(df$year), 1948, info = "Extended should start at 1948")
  expect_gte(max(df$year), 2024, info = "Extended should reach at least 2024")
})

# ============================================
# 11. NO_NA_CHECKS — Key column completeness
# ============================================

context("Chapter 9 Integration Tests — NO_NA_CHECKS")

test_that("NO_NA_CHECKS: T901 series CSV has no NA in year column", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  path <- file.path(series_csv_dir, "T901.csv")
  skip_if_not(file.exists(path), "T901.csv not found")
  df <- tryCatch(read.csv(path, stringsAsFactors = FALSE), error = function(e) NULL)
  skip_if(is.null(df) || !("year" %in% names(df)), "T901 no year column")
  na_count <- sum(is.na(df$year))
  expect_equal(na_count, 0, info = paste("T901 has", na_count, "NA values in year column"))
})

test_that("NO_NA_CHECKS: summary indicators book-period has no NA in key columns", {
  path <- file.path(shiny_data_dir, "summary_indicators_1948_1989.csv")
  skip_if_not(file.exists(path), "summary_indicators_1948_1989.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  key_cols <- c("year", "T506_exploitation_rate", "T511_productive_labor_share")

  for (col in key_cols) {
    if (col %in% names(df)) {
      na_count <- sum(is.na(df[[col]]))
      expect_equal(na_count, 0,
                   info = paste("summary_indicators column", col, "has", na_count, "NAs"))
    }
  }
})

test_that("NO_NA_CHECKS: no completely empty data columns in T901 series CSV", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  path <- file.path(series_csv_dir, "T901.csv")
  skip_if_not(file.exists(path), "T901.csv not found")
  df <- tryCatch(read.csv(path, stringsAsFactors = FALSE), error = function(e) NULL)
  skip_if(is.null(df), "T901 cannot parse")
  data_cols <- setdiff(names(df), "year")
  for (col in data_cols) {
    all_na <- all(is.na(df[[col]]) | df[[col]] == "")
    expect_false(all_na, info = paste("T901 column", col, "is completely empty"))
  }
})

test_that("NO_NA_CHECKS: chapter_09_absorbed.csv has no NA in key columns", {
  absorbed_dir <- file.path(project_root, "absorbed")
  path <- file.path(absorbed_dir, "chapter_09_absorbed.csv")
  skip_if_not(file.exists(path), "chapter_09_absorbed.csv not found")

  df <- read.csv(path, stringsAsFactors = FALSE)
  for (col in c("series_id", "year", "value")) {
    if (col %in% names(df)) {
      na_count <- sum(is.na(df[[col]]))
      expect_equal(na_count, 0,
                   info = paste("chapter_09_absorbed column", col, "has", na_count, "NAs"))
    }
  }
})

# ============================================
# Summary
# ============================================

cat("\n--- Chapter 9 Test Summary ---\n")
cat("  11 test sections completed\n")
cat("  Series: T901 (1 derived/aggregator series)\n")
cat("  Period: 1948-1989 (book), 1948-2024 (extended)\n")
cat("  Key finding: Marxian categories diverge from orthodox — e +44%, Lp/L -37%\n")
cat("  Source: 100% derived from Ch5 (T501-T516) + Ch6 (T607, T608)\n")
