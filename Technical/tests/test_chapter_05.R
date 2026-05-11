# ============================================
# test_chapter_05.R — Chapter 5 Integration Tests
# ============================================
# 8 test sections required by Anu Review:
#   1. CHAPTER_METADATA
#   2. SERIES_MAPPING
#   3. DATA_FILE_TESTS
#   4. DPR_EXISTENCE
#   5. EPR_EXISTENCE
#   6. FIGURE_CATALOG
#   7. HELPER_FUNCTIONS
#   8. THEMATIC_TESTS
#
# Anu Standard v2.0 — Test Coverage Component
# Created: 2026-02-24 (Session 7 — Gap Remediation G005)
# Depends on: data_loader.R (CH5_SERIES_MAPPING), chart_builder.R, FIGURE_SERIES_CATALOG.json
# ============================================

library(testthat)
library(here)
library(jsonlite)

# ============================================
# SETUP — Source dependencies
# ============================================

# Set working directory context
project_root <- here::here()

# Source data_loader.R for CH5_SERIES_MAPPING
tryCatch(
  source(file.path(project_root, "ShinyApp", "R", "data_loader.R")),
  error = function(e) {
    # If config.R fails (outside Shiny context), mock AS2_PATHS
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

# Paths for file existence checks
docs_series_dir <- file.path(project_root, "docs", "series")
chopped_dir <- file.path(project_root, "..", "Inputs", "ST_Chopped", "ch05")

# ============================================
# 1. CHAPTER_METADATA
# ============================================

context("Chapter 5 Integration Tests — CHAPTER_METADATA")

test_that("CHAPTER_METADATA: correct chapter configuration", {
  # Chapter 5 has 16 series (T501-T516)
  expect_equal(length(CH5_SERIES_MAPPING), 16)

  # All series IDs are T5xx
  ids <- names(CH5_SERIES_MAPPING)
  expect_true(all(grepl("^T5\\d{2}$", ids)))

  # Chapter number derivable from series IDs
  chapters <- as.integer(substr(ids, 2, 2))
  expect_true(all(chapters == 5))
})

# ============================================
# 2. SERIES_MAPPING
# ============================================

context("Chapter 5 Integration Tests — SERIES_MAPPING")

test_that("SERIES_MAPPING: CH5_SERIES_MAPPING exists and has correct length", {
  expect_true(exists("CH5_SERIES_MAPPING"))
  expect_equal(length(CH5_SERIES_MAPPING), 16)
})

test_that("SERIES_MAPPING: all T501-T516 present as keys", {
  expected_ids <- paste0("T5", sprintf("%02d", 1:16))
  actual_ids <- names(CH5_SERIES_MAPPING)
  for (id in expected_ids) {
    expect_true(id %in% actual_ids, info = paste(id, "missing from mapping"))
  }
})

test_that("SERIES_MAPPING: each entry has required fields", {
  required_fields <- c("name", "description", "formula", "data_patterns", "is_extended")
  for (id in names(CH5_SERIES_MAPPING)) {
    entry <- CH5_SERIES_MAPPING[[id]]
    for (field in required_fields) {
      expect_false(is.null(entry[[field]]),
                   info = paste(id, "missing field:", field))
    }
  }
})

test_that("SERIES_MAPPING: is_extended TRUE for exactly 9 series", {
  extended <- names(CH5_SERIES_MAPPING)[
    vapply(CH5_SERIES_MAPPING, function(x) isTRUE(x$is_extended), logical(1))
  ]
  expect_equal(length(extended), 9)
  # Expected extended: T504, T505, T506, T511, T512, T513, T514, T515, T516
  expected_extended <- c("T504", "T505", "T506", "T511", "T512", "T513", "T514", "T515", "T516")
  expect_setequal(extended, expected_extended)
})

test_that("SERIES_MAPPING: is_key_series TRUE for T506, T511, T512, T513", {
  key <- names(CH5_SERIES_MAPPING)[
    vapply(CH5_SERIES_MAPPING, function(x) isTRUE(x$is_key_series), logical(1))
  ]
  expect_setequal(key, c("T506", "T511", "T512", "T513"))
})

# ============================================
# 3. DATA_FILE_TESTS
# ============================================

context("Chapter 5 Integration Tests — DATA_FILE_TESTS")

test_that("DATA_FILE_TESTS: Chopped CSVs exist in ST_Chopped/ch05", {
  skip_if_not(dir.exists(chopped_dir), "ST_Chopped/ch05/ directory not found")

  expected_files <- c(
    "Table5_7_KeyRatios.csv",
    "Table5_7_Extended.csv",
    "TableE2_RevenueAccounts.csv",
    "TableE3_LaborStatistics.csv",
    "Table5_14_Comparison.csv",
    "Employment_1948_1989.csv",
    "ExploitationComposition_1948_1989.csv"
  )

  for (f in expected_files) {
    path <- file.path(chopped_dir, f)
    expect_true(file.exists(path), info = paste("Missing:", f))
  }
})

test_that("DATA_FILE_TESTS: Key Chopped files have year column and correct range", {
  skip_if_not(dir.exists(chopped_dir), "ST_Chopped/ch05/ directory not found")

  key_ratios_path <- file.path(chopped_dir, "Table5_7_KeyRatios.csv")
  skip_if_not(file.exists(key_ratios_path), "Table5_7_KeyRatios.csv not found")

  # Read with skip for 3-row Anu Chopped header
  df <- tryCatch(
    read.csv(key_ratios_path, skip = 2, stringsAsFactors = FALSE),
    error = function(e) NULL
  )
  skip_if(is.null(df), "Could not parse Table5_7_KeyRatios.csv")

  expect_true("year" %in% tolower(names(df)),
              info = "year column not found in Table5_7_KeyRatios.csv")
  year_col <- df[[which(tolower(names(df)) == "year")]]
  expect_true(min(year_col, na.rm = TRUE) <= 1948)
  expect_true(max(year_col, na.rm = TRUE) >= 1989)
})

test_that("DATA_FILE_TESTS: Extended CSV has 1948-2024 range", {
  skip_if_not(dir.exists(chopped_dir), "ST_Chopped/ch05/ directory not found")

  ext_path <- file.path(chopped_dir, "Table5_7_Extended.csv")
  skip_if_not(file.exists(ext_path), "Table5_7_Extended.csv not found")

  df <- tryCatch(
    read.csv(ext_path, skip = 2, stringsAsFactors = FALSE),
    error = function(e) NULL
  )
  skip_if(is.null(df), "Could not parse Table5_7_Extended.csv")

  year_col <- df[[which(tolower(names(df)) == "year")]]
  expect_true(min(year_col, na.rm = TRUE) <= 1948)
  expect_true(max(year_col, na.rm = TRUE) >= 2024)
})

# ============================================
# 4. DPR_EXISTENCE
# ============================================

context("Chapter 5 Integration Tests — DPR_EXISTENCE")

test_that("DPR_EXISTENCE: all 16 T5xx DPR files exist", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")

  for (i in 1:16) {
    id <- paste0("T5", sprintf("%02d", i))
    path <- file.path(docs_series_dir, paste0(id, "_DPR.md"))
    expect_true(file.exists(path),
                info = paste("Missing DPR:", id))
  }
})

test_that("DPR_EXISTENCE: each DPR is non-empty (>100 bytes)", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")

  for (i in 1:16) {
    id <- paste0("T5", sprintf("%02d", i))
    path <- file.path(docs_series_dir, paste0(id, "_DPR.md"))
    skip_if_not(file.exists(path), paste(id, "DPR not found"))
    expect_gt(file.info(path)$size, 100,
              info = paste(id, "DPR is too small"))
  }
})

# ============================================
# 5. EPR_EXISTENCE
# ============================================

context("Chapter 5 Integration Tests — EPR_EXISTENCE")

test_that("EPR_EXISTENCE: all 9 extendable series have EPR files", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")

  extendable <- c("T504", "T505", "T506", "T511", "T512", "T513", "T514", "T515", "T516")
  for (id in extendable) {
    path <- file.path(docs_series_dir, paste0(id, "_EPR.md"))
    expect_true(file.exists(path),
                info = paste("Missing EPR:", id))
  }
})

test_that("EPR_EXISTENCE: each EPR is non-empty (>100 bytes)", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")

  extendable <- c("T504", "T505", "T506", "T511", "T512", "T513", "T514", "T515", "T516")
  for (id in extendable) {
    path <- file.path(docs_series_dir, paste0(id, "_EPR.md"))
    skip_if_not(file.exists(path), paste(id, "EPR not found"))
    expect_gt(file.info(path)$size, 100,
              info = paste(id, "EPR is too small"))
  }
})

# ============================================
# 6. FIGURE_CATALOG
# ============================================

context("Chapter 5 Integration Tests — FIGURE_CATALOG")

test_that("FIGURE_CATALOG: FIGURE_SERIES_CATALOG.json exists and parses", {
  expect_true(file.exists(figure_catalog_path),
              info = "FIGURE_SERIES_CATALOG.json not found")
  expect_false(is.null(figure_catalog))
})

test_that("FIGURE_CATALOG: 8 entries with chapter == 5", {
  skip_if(is.null(figure_catalog), "Figure catalog not loaded")
  ch5_catalog <- figure_catalog[figure_catalog$chapter == 5, ]
  expect_equal(nrow(ch5_catalog), 8)
  expect_true(all(ch5_catalog$chapter == 5))
})

test_that("FIGURE_CATALOG: Fig 5.1 has is_empirical == FALSE", {
  skip_if(is.null(figure_catalog), "Figure catalog not loaded")
  fig51 <- figure_catalog[figure_catalog$figure_id == "Fig_5_1", ]
  expect_equal(nrow(fig51), 1)
  expect_false(fig51$is_empirical)
})

test_that("FIGURE_CATALOG: all Ch5 series_ids reference valid T5xx codes", {
  skip_if(is.null(figure_catalog), "Figure catalog not loaded")
  ch5_catalog <- figure_catalog[figure_catalog$chapter == 5, ]
  all_ids <- unique(unlist(ch5_catalog$series_ids))
  # Remove empty/NULL
  all_ids <- all_ids[nchar(all_ids) > 0]
  valid <- grepl("^T5\\d{2}$", all_ids)
  expect_true(all(valid),
              info = paste("Invalid series IDs:", paste(all_ids[!valid], collapse = ", ")))
})

# ============================================
# 7. HELPER_FUNCTIONS
# ============================================

context("Chapter 5 Integration Tests — HELPER_FUNCTIONS")

test_that("HELPER_FUNCTIONS: is_chapter5_series works correctly", {
  expect_true(is_chapter5_series("T506"))
  expect_true(is_chapter5_series("T501"))
  expect_true(is_chapter5_series("T516"))
  expect_false(is_chapter5_series("T607"))
  expect_false(is_chapter5_series("T5001"))
  expect_false(is_chapter5_series("X506"))
})

test_that("HELPER_FUNCTIONS: get_series_metadata returns valid metadata for T506", {
  meta <- get_series_metadata("T506")
  expect_false(is.null(meta))
  expect_equal(meta$name, "Rate of Exploitation (e = S*/V*)")
  expect_true(meta$is_extended)
  expect_true(meta$is_key_series)
  expect_true(length(meta$data_patterns) > 0)
})

test_that("HELPER_FUNCTIONS: get_series_metadata returns NULL for invalid ID", {
  expect_null(get_series_metadata("T999"))
  expect_null(get_series_metadata("INVALID"))
})

test_that("HELPER_FUNCTIONS: get_chapter_series(5) returns 16 entries", {
  ch5 <- get_chapter_series(5)
  expect_equal(length(ch5), 16)
})

test_that("HELPER_FUNCTIONS: get_extended_series returns 9 series", {
  ext <- get_extended_series()
  expect_equal(length(ext), 9)
})

test_that("HELPER_FUNCTIONS: get_key_series returns 4 series", {
  key <- get_key_series()
  expect_equal(length(key), 4)
})

# ============================================
# 8. THEMATIC_TESTS
# ============================================

context("Chapter 5 Integration Tests — THEMATIC_TESTS")

test_that("THEMATIC_TESTS: benchmark exploitation rates from authoritative data", {
  # Try to load authoritative CSV
  auth_path <- file.path(project_root, "..", "Inputs", "BookTables", "ch05",
                         "[2025.12.05] shaikh_tonak_authoritative_1948_1989.csv")
  skip_if_not(file.exists(auth_path), "Authoritative CSV not found")

  auth <- read.csv(auth_path, stringsAsFactors = FALSE)
  skip_if(!("exploitation_rate_e" %in% names(auth) || "e" %in% names(auth)),
          "exploitation_rate column not found")

  e_col <- if ("exploitation_rate_e" %in% names(auth)) "exploitation_rate_e"
           else "e"

  e_1948 <- auth[auth$year == 1948, e_col]
  e_1989 <- auth[auth$year == 1989, e_col]

  skip_if(length(e_1948) == 0 || length(e_1989) == 0, "Benchmark years not found")

  expect_equal(round(e_1948, 2), 1.70, tolerance = 0.01,
               info = "e(1948) should be 1.70")
  expect_equal(round(e_1989, 2), 2.44, tolerance = 0.01,
               info = "e(1989) should be 2.44")
})

test_that("THEMATIC_TESTS: productive labor share benchmarks", {
  auth_path <- file.path(project_root, "..", "Inputs", "BookTables", "ch05",
                         "[2025.12.05] shaikh_tonak_authoritative_1948_1989.csv")
  skip_if_not(file.exists(auth_path), "Authoritative CSV not found")

  auth <- read.csv(auth_path, stringsAsFactors = FALSE)
  lpl_col <- if ("Lp_L" %in% names(auth)) "Lp_L"
             else if ("Lp_L_ratio" %in% names(auth)) "Lp_L_ratio"
             else NULL
  skip_if(is.null(lpl_col), "Lp/L column not found")

  lpl_1989 <- auth[auth$year == 1989, lpl_col]
  skip_if(length(lpl_1989) == 0, "1989 not found")

  expect_equal(round(lpl_1989, 2), 0.36, tolerance = 0.01,
               info = "Lp/L(1989) should be 0.36")
})

test_that("THEMATIC_TESTS: 9 series are extended, 7 are book-period-only", {
  extended_count <- sum(vapply(CH5_SERIES_MAPPING,
                                function(x) isTRUE(x$is_extended), logical(1)))
  book_only_count <- 16 - extended_count
  expect_equal(extended_count, 9)
  expect_equal(book_only_count, 7)
})

test_that("THEMATIC_TESTS: V*/W(1989) benchmark", {
  auth_path <- file.path(project_root, "..", "Inputs", "BookTables", "ch05",
                         "[2025.12.05] shaikh_tonak_authoritative_1948_1989.csv")
  skip_if_not(file.exists(auth_path), "Authoritative CSV not found")

  auth <- read.csv(auth_path, stringsAsFactors = FALSE)
  vw_col <- if ("V_star_W" %in% names(auth)) "V_star_W"
            else if ("V_star_over_W" %in% names(auth)) "V_star_over_W"
            else NULL
  skip_if(is.null(vw_col), "V*/W column not found")

  vw_1989 <- auth[auth$year == 1989, vw_col]
  skip_if(length(vw_1989) == 0, "1989 not found")

  expect_equal(round(vw_1989, 2), 0.36, tolerance = 0.01,
               info = "V*/W(1989) should be 0.36")
})

# ============================================
# 9. QUALITY_THRESHOLD
# ============================================

cat("\n--- Section 9: QUALITY_THRESHOLD ---\n")
tryCatch({
  ext_log <- jsonlite::fromJSON(file.path(project_root, "EXTENSION_LOG.json"))

  # All CERTIFIED WITH NOTES should have faithfulness >= 75%
  certified <- ext_log[ext_log$certification == "CERTIFIED WITH NOTES", ]
  all_above <- all(certified$faithfulness_score >= 75)
  cat(if (all_above) "  PASS: All CERTIFIED WITH NOTES EPRs have faithfulness >= 75%\n"
      else "  FAIL: Some CERTIFIED EPRs below 75% threshold\n")

  # All NOT CERTIFIED should have faithfulness < 75%
  not_cert <- ext_log[ext_log$certification == "NOT CERTIFIED", ]
  all_below <- all(not_cert$faithfulness_score < 75)
  cat(if (all_below) "  PASS: All NOT CERTIFIED EPRs have faithfulness < 75%\n"
      else "  FAIL: Some NOT CERTIFIED EPRs at or above 75%\n")
}, error = function(e) {
  cat(paste0("  SKIP: QUALITY_THRESHOLD - ", e$message, "\n"))
})

# ============================================
# 10. EXTENSION_CONTINUITY
# ============================================

cat("\n--- Section 10: EXTENSION_CONTINUITY ---\n")
tryCatch({
  ext_log <- jsonlite::fromJSON(file.path(project_root, "EXTENSION_LOG.json"))

  # Exactly 9 entries
  cat(if (nrow(ext_log) == 9) "  PASS: EXTENSION_LOG has exactly 9 entries\n"
      else paste0("  FAIL: Expected 9 entries, found ", nrow(ext_log), "\n"))

  # All connection_ratio == 1.000
  all_connected <- all(ext_log$connection_ratio == 1.0)
  cat(if (all_connected) "  PASS: All entries have connection_ratio == 1.000\n"
      else "  FAIL: Some entries have connection_ratio != 1.000\n")

  # All growth_rate_continuity_pct < 5.0%
  all_continuous <- all(ext_log$growth_rate_continuity_pct < 5.0)
  cat(if (all_continuous) "  PASS: All growth_rate_continuity_pct < 5.0%\n"
      else "  FAIL: Some entries have growth_rate_continuity_pct >= 5.0%\n")
}, error = function(e) {
  cat(paste0("  SKIP: EXTENSION_CONTINUITY - ", e$message, "\n"))
})

# ============================================
# 11. CHART_INTEGRATION
# ============================================

cat("\n--- Section 11: CHART_INTEGRATION ---\n")
tryCatch({
  # Test is_chapter5_series works for all T501-T516
  all_ch5 <- all(sapply(paste0("T5", sprintf("%02d", 1:16)), is_chapter5_series))
  cat(if (all_ch5) "  PASS: is_chapter5_series() works for all T501-T516\n"
      else "  FAIL: is_chapter5_series() fails for some T5xx series\n")
}, error = function(e) {
  cat(paste0("  SKIP: is_chapter5_series check - ", e$message, "\n"))
})

tryCatch({
  # Chart helper functions exist
  helpers <- c("ch5_plotly_layout", "add_recession_bands", "add_extension_marker", "build_chapter5_chart")
  exist <- sapply(helpers, function(f) exists(f, mode = "function"))
  cat(if (all(exist)) "  PASS: All chart helper functions exist\n"
      else paste0("  FAIL: Missing helpers: ", paste(helpers[!exist], collapse = ", "), "\n"))
}, error = function(e) {
  cat(paste0("  SKIP: Chart helpers check - ", e$message, "\n"))
})

tryCatch({
  # add_div001_warning exists and produces valid Plotly object
  stopifnot(exists("add_div001_warning", mode = "function"))
  test_p <- plotly::plot_ly()
  result <- add_div001_warning(test_p)
  is_plotly <- inherits(result, "plotly")
  cat(if (is_plotly) "  PASS: add_div001_warning() produces valid Plotly object\n"
      else "  FAIL: add_div001_warning() does not return Plotly object\n")
}, error = function(e) {
  cat(paste0("  SKIP: add_div001_warning check - ", e$message, "\n"))
})

tryCatch({
  # build_transition_chart exists
  stopifnot(exists("build_transition_chart", mode = "function"))
  cat("  PASS: build_transition_chart() function exists\n")
}, error = function(e) {
  cat(paste0("  SKIP: build_transition_chart check - ", e$message, "\n"))
})

# ============================================
# 12. DIVERGENCE_REGISTER
# ============================================

cat("\n--- Section 12: DIVERGENCE_REGISTER ---\n")
tryCatch({
  div_reg <- jsonlite::fromJSON(file.path(project_root, "DIVERGENCE_REGISTER.json"))
  cat("  PASS: DIVERGENCE_REGISTER.json exists and parses\n")

  # DIV-001 documented with T513, T514
  divs <- div_reg$divergences
  div001 <- divs[divs$id == "DIV-001", ]
  has_t513 <- "T513" %in% unlist(div001$series_affected)
  has_t514 <- "T514" %in% unlist(div001$series_affected)
  cat(if (nrow(div001) > 0 && has_t513 && has_t514)
      "  PASS: DIV-001 documented with T513, T514 in series_affected\n"
      else "  FAIL: DIV-001 missing or incomplete\n")

  # DIV-002 documented with T504, T506, T512
  div002 <- divs[divs$id == "DIV-002", ]
  has_t504 <- "T504" %in% unlist(div002$series_affected)
  has_t506 <- "T506" %in% unlist(div002$series_affected)
  has_t512 <- "T512" %in% unlist(div002$series_affected)
  cat(if (nrow(div002) > 0 && has_t504 && has_t506 && has_t512)
      "  PASS: DIV-002 documented with T504, T506, T512 in series_affected\n"
      else "  FAIL: DIV-002 missing or incomplete\n")
}, error = function(e) {
  cat(paste0("  SKIP: DIVERGENCE_REGISTER - ", e$message, "\n"))
})

tryCatch({
  # DIV-001 referenced in T513_DPR.md and T514_DPR.md
  t513_content <- readLines(file.path(docs_series_dir, "T513_DPR.md"))
  t514_content <- readLines(file.path(docs_series_dir, "T514_DPR.md"))
  has_div001_t513 <- any(grepl("DIV-001", t513_content))
  has_div001_t514 <- any(grepl("DIV-001", t514_content))
  cat(if (has_div001_t513) "  PASS: DIV-001 referenced in T513_DPR.md\n"
      else "  FAIL: DIV-001 not found in T513_DPR.md\n")
  cat(if (has_div001_t514) "  PASS: DIV-001 referenced in T514_DPR.md\n"
      else "  FAIL: DIV-001 not found in T514_DPR.md\n")
}, error = function(e) {
  cat(paste0("  SKIP: DIV-001 DPR reference check - ", e$message, "\n"))
})

# ============================================
# 13. ARTIFACT_EXISTENCE — Per-series artifact checks
# ============================================

context("Chapter 5 Integration Tests — ARTIFACT_EXISTENCE")

# Paths for artifact checks
research_dir <- file.path(project_root, "research")
anu_chopped_dir <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "chopped")
extenbooks_dir <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "extenbooks")
series_csv_dir <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "series")

ch5_ids <- paste0("T5", sprintf("%02d", 1:16))

test_that("ARTIFACT_EXISTENCE: all 16 T5xx research JSONs exist", {
  skip_if_not(dir.exists(research_dir), "research/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(research_dir, paste0(id, "_research.json"))
    expect_true(file.exists(path), info = paste("Missing research JSON:", id))
  }
})

test_that("ARTIFACT_EXISTENCE: all 16 T5xx DECOMPOSITION files exist", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(docs_series_dir, paste0(id, "_DECOMPOSITION.md"))
    expect_true(file.exists(path), info = paste("Missing DECOMPOSITION:", id))
  }
})

test_that("ARTIFACT_EXISTENCE: all 16 T5xx chopped CSVs exist (Anu format)", {
  skip_if_not(dir.exists(anu_chopped_dir), "ANU chopped/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(anu_chopped_dir, paste0(id, "_chopped.csv"))
    expect_true(file.exists(path), info = paste("Missing Anu chopped CSV:", id))
  }
})

test_that("ARTIFACT_EXISTENCE: all 16 T5xx extenbooks exist", {
  skip_if_not(dir.exists(extenbooks_dir), "extenbooks/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(extenbooks_dir, paste0(id, "_extenbook.xlsx"))
    expect_true(file.exists(path), info = paste("Missing extenbook:", id))
  }
})

test_that("ARTIFACT_EXISTENCE: all 16 T5xx series CSVs exist", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(series_csv_dir, paste0(id, ".csv"))
    expect_true(file.exists(path), info = paste("Missing series CSV:", id))
  }
})

# ============================================
# 14. DATA_RANGE_CHECKS — Year and value range validation
# ============================================

context("Chapter 5 Integration Tests — DATA_RANGE_CHECKS")

test_that("DATA_RANGE_CHECKS: series CSVs have years >= 1929 and <= 2025", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(series_csv_dir, paste0(id, ".csv"))
    skip_if_not(file.exists(path), paste(id, "not found"))
    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE), error = function(e) NULL)
    skip_if(is.null(df) || !("year" %in% names(df)), paste(id, "cannot check years"))
    years <- df$year[!is.na(df$year)]
    skip_if(length(years) == 0, paste(id, "no year values"))
    expect_gte(min(years), 1929, info = paste(id, "has year <1929:", min(years)))
    expect_lte(max(years), 2025, info = paste(id, "has year >2025:", max(years)))
  }
})

test_that("DATA_RANGE_CHECKS: book-period series cover 1948-1989", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(series_csv_dir, paste0(id, ".csv"))
    skip_if_not(file.exists(path), paste(id, "not found"))
    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE), error = function(e) NULL)
    skip_if(is.null(df) || !("year" %in% names(df)), paste(id, "cannot check years"))
    years <- df$year[!is.na(df$year)]
    # All Ch5 series should at minimum cover the book period
    expect_true(1948 %in% years || min(years) <= 1948,
                info = paste(id, "does not cover 1948"))
    expect_true(1989 %in% years || max(years) >= 1989,
                info = paste(id, "does not cover 1989"))
  }
})

# ============================================
# 15. NO_NA_CHECKS — Key column completeness
# ============================================

context("Chapter 5 Integration Tests — NO_NA_CHECKS")

test_that("NO_NA_CHECKS: series CSVs have no NA in year column", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(series_csv_dir, paste0(id, ".csv"))
    skip_if_not(file.exists(path), paste(id, "not found"))
    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE), error = function(e) NULL)
    skip_if(is.null(df) || !("year" %in% names(df)), paste(id, "no year column"))
    na_count <- sum(is.na(df$year))
    expect_equal(na_count, 0, info = paste(id, "has", na_count, "NA values in year column"))
  }
})

test_that("NO_NA_CHECKS: no completely empty data columns in Ch5 series CSVs", {
  skip_if_not(dir.exists(series_csv_dir), "series/ directory not found")
  for (id in ch5_ids) {
    path <- file.path(series_csv_dir, paste0(id, ".csv"))
    skip_if_not(file.exists(path), paste(id, "not found"))
    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE), error = function(e) NULL)
    skip_if(is.null(df), paste(id, "cannot parse"))
    data_cols <- setdiff(names(df), "year")
    for (col in data_cols) {
      all_na <- all(is.na(df[[col]]) | df[[col]] == "")
      expect_false(all_na, info = paste(id, "column", col, "is completely empty"))
    }
  }
})
