# ============================================
# test_artifacts.R — Comprehensive Artifact Validation Tests
# ============================================
# Validates ALL artifact types exist and have correct structure
# across the entire ST2 pipeline (26 series, 3 chapters).
#
# Sections:
#   A. Research JSONs (26 files)
#   B. Decomposition Files (26 files)
#   C. DPR Files (26 files)
#   D. Chopped CSVs (26 files)
#   E. Extenbooks (26 files)
#   F. Series CSVs (26+ files)
#   G. Absorbed CSVs (3 files)
#   H. FPR Files (17 files)
#   I. ANU_LEDGER.json
#   J. SUBSOURCE_METADATA.json
#   K. Cross-reference consistency
#
# Anu Standard v2.0 — D11 Dimension Coverage
# Created: 2026-03-21
# Runnable with: Rscript test_artifacts.R (from tests/ directory)
# ============================================

library(testthat)
library(jsonlite)

# ============================================
# SETUP — Resolve paths
# ============================================

# When run from tests/ directory, project_root is one level up
if (file.exists("../ANU_LEDGER.json")) {
  project_root <- normalizePath("..")
} else if (requireNamespace("here", quietly = TRUE)) {
  project_root <- here::here()
} else {
  project_root <- normalizePath(file.path(getwd(), ".."))
}

# Core paths
research_dir    <- file.path(project_root, "research")
docs_series_dir <- file.path(project_root, "docs", "series")
docs_figures_dir <- file.path(project_root, "docs", "figures")
chopped_dir     <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "chopped")
extenbooks_dir  <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "extenbooks")
series_dir      <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "series")
shiny_dir       <- file.path(project_root, "ANU_REPLICATOR", "data", "final-data", "shiny")
absorbed_dir    <- file.path(project_root, "absorbed")

# All 26 series IDs
ALL_SERIES <- c(
  paste0("T5", sprintf("%02d", 1:16)),   # T501-T516 (Chapter 5)
  paste0("T6", sprintf("%02d", 1:9)),     # T601-T609 (Chapter 6)
  "T901"                                  # T901      (Chapter 9)
)

# ============================================
# A. Research JSONs (26 files)
# ============================================

context("Artifact Validation — A. Research JSONs")

test_that("A1: research/ directory exists", {
  expect_true(dir.exists(research_dir),
              info = paste("research/ not found at", research_dir))
})

test_that("A2: all 26 T###_research.json files exist", {
  skip_if_not(dir.exists(research_dir), "research/ directory not found")
  for (sid in ALL_SERIES) {
    path <- file.path(research_dir, paste0(sid, "_research.json"))
    expect_true(file.exists(path),
                info = paste("Missing research JSON:", sid))
  }
})

test_that("A3: each research JSON has required fields", {
  skip_if_not(dir.exists(research_dir), "research/ directory not found")
  required_fields <- c("series_id", "series_name", "chapter", "entries")

  for (sid in ALL_SERIES) {
    path <- file.path(research_dir, paste0(sid, "_research.json"))
    skip_if_not(file.exists(path), paste(sid, "research.json not found"))

    rj <- tryCatch(fromJSON(path), error = function(e) NULL)
    skip_if(is.null(rj), paste("Could not parse", sid, "research.json"))

    for (field in required_fields) {
      expect_false(is.null(rj[[field]]),
                   info = paste(sid, "research.json missing field:", field))
    }
  }
})

test_that("A4: each research JSON series_id matches filename", {
  skip_if_not(dir.exists(research_dir), "research/ directory not found")

  for (sid in ALL_SERIES) {
    path <- file.path(research_dir, paste0(sid, "_research.json"))
    skip_if_not(file.exists(path), paste(sid, "not found"))

    rj <- tryCatch(fromJSON(path), error = function(e) NULL)
    skip_if(is.null(rj), paste("Could not parse", sid))

    expect_equal(rj$series_id, sid,
                 info = paste(sid, "series_id mismatch in research JSON"))
  }
})

test_that("A5: each research JSON has non-empty entries", {
  skip_if_not(dir.exists(research_dir), "research/ directory not found")

  for (sid in ALL_SERIES) {
    path <- file.path(research_dir, paste0(sid, "_research.json"))
    skip_if_not(file.exists(path), paste(sid, "not found"))

    rj <- tryCatch(fromJSON(path), error = function(e) NULL)
    skip_if(is.null(rj), paste("Could not parse", sid))

    entries <- rj$entries
    if (is.data.frame(entries)) {
      expect_gt(nrow(entries), 0,
                info = paste(sid, "has zero entries"))
    } else if (is.list(entries)) {
      expect_gt(length(entries), 0,
                info = paste(sid, "has zero entries"))
    }
  }
})

test_that("A6: kb_sources_searched paths resolve to real files (spot check)", {
  skip_if_not(dir.exists(research_dir), "research/ directory not found")

  # Spot check first 5 series
  for (sid in ALL_SERIES[1:5]) {
    path <- file.path(research_dir, paste0(sid, "_research.json"))
    skip_if_not(file.exists(path), paste(sid, "not found"))

    rj <- tryCatch(fromJSON(path), error = function(e) NULL)
    skip_if(is.null(rj) || is.null(rj$kb_sources_searched),
            paste(sid, "has no kb_sources_searched"))

    sources <- rj$kb_sources_searched
    # Check at least one source path resolves
    resolved <- vapply(sources, function(s) {
      full <- file.path(project_root, s)
      file.exists(full)
    }, logical(1))
    expect_true(any(resolved),
                info = paste(sid, "- no kb_sources_searched paths resolve"))
  }
})

# ============================================
# B. Decomposition Files (26 files)
# ============================================

context("Artifact Validation — B. Decomposition Files")

test_that("B1: docs/series/ directory exists", {
  expect_true(dir.exists(docs_series_dir),
              info = paste("docs/series/ not found at", docs_series_dir))
})

test_that("B2: all 26 T###_DECOMPOSITION.md files exist", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(docs_series_dir, paste0(sid, "_DECOMPOSITION.md"))
    expect_true(file.exists(path),
                info = paste("Missing DECOMPOSITION:", sid))
  }
})

test_that("B3: each DECOMPOSITION is non-empty (>200 bytes)", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(docs_series_dir, paste0(sid, "_DECOMPOSITION.md"))
    skip_if_not(file.exists(path), paste(sid, "DECOMPOSITION not found"))
    expect_gt(file.info(path)$size, 200,
              info = paste(sid, "DECOMPOSITION is too small"))
  }
})

test_that("B4: each DECOMPOSITION has required sections", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ not found")

  required_headings <- c("Quick Reference", "Sub-Components", "Construction Steps")

  for (sid in ALL_SERIES) {
    path <- file.path(docs_series_dir, paste0(sid, "_DECOMPOSITION.md"))
    skip_if_not(file.exists(path), paste(sid, "DECOMPOSITION not found"))

    content <- paste(readLines(path, warn = FALSE), collapse = "\n")
    for (heading in required_headings) {
      expect_true(grepl(heading, content, ignore.case = TRUE),
                  info = paste(sid, "DECOMPOSITION missing section:", heading))
    }
  }
})

# ============================================
# C. DPR Files (26 files)
# ============================================

context("Artifact Validation — C. DPR Files")

test_that("C1: all 26 T###_DPR.md files exist", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(docs_series_dir, paste0(sid, "_DPR.md"))
    expect_true(file.exists(path),
                info = paste("Missing DPR:", sid))
  }
})

test_that("C2: each DPR is non-empty (>100 bytes)", {
  skip_if_not(dir.exists(docs_series_dir), "docs/series/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(docs_series_dir, paste0(sid, "_DPR.md"))
    skip_if_not(file.exists(path), paste(sid, "DPR not found"))
    expect_gt(file.info(path)$size, 100,
              info = paste(sid, "DPR is too small"))
  }
})

# ============================================
# D. Chopped CSVs (26 files)
# ============================================

context("Artifact Validation — D. Chopped CSVs")

test_that("D1: chopped/ directory exists", {
  expect_true(dir.exists(chopped_dir),
              info = paste("chopped/ not found at", chopped_dir))
})

test_that("D2: all 26 T###_chopped.csv files exist", {
  skip_if_not(dir.exists(chopped_dir), "chopped/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(chopped_dir, paste0(sid, "_chopped.csv"))
    expect_true(file.exists(path),
                info = paste("Missing chopped CSV:", sid))
  }
})

test_that("D3: Row 1 is pipe-separated metadata", {
  skip_if_not(dir.exists(chopped_dir), "chopped/ not found")

  for (sid in ALL_SERIES[1:5]) {
    path <- file.path(chopped_dir, paste0(sid, "_chopped.csv"))
    skip_if_not(file.exists(path), paste(sid, "chopped not found"))

    lines <- readLines(path, n = 1, warn = FALSE)
    expect_true(grepl("\\|", lines[1]),
                info = paste(sid, "Row 1 is not pipe-separated metadata"))
  }
})

test_that("D4: Row 2 has dash-notation column IDs (T###-X)", {
  skip_if_not(dir.exists(chopped_dir), "chopped/ not found")

  for (sid in ALL_SERIES[1:5]) {
    path <- file.path(chopped_dir, paste0(sid, "_chopped.csv"))
    skip_if_not(file.exists(path), paste(sid, "chopped not found"))

    lines <- readLines(path, n = 2, warn = FALSE)
    skip_if(length(lines) < 2, paste(sid, "chopped has < 2 lines"))

    # Row 2 should contain the series ID with dash notation
    expect_true(grepl(paste0(sid, "-"), lines[2]),
                info = paste(sid, "Row 2 missing dash-notation column ID"))
  }
})

test_that("D5: Row 3+ are numeric data", {
  skip_if_not(dir.exists(chopped_dir), "chopped/ not found")

  for (sid in ALL_SERIES[1:5]) {
    path <- file.path(chopped_dir, paste0(sid, "_chopped.csv"))
    skip_if_not(file.exists(path), paste(sid, "chopped not found"))

    lines <- readLines(path, n = 5, warn = FALSE)
    skip_if(length(lines) < 3, paste(sid, "chopped has < 3 lines"))

    # Row 3 should start with a year (numeric)
    first_val <- strsplit(lines[3], ",")[[1]][1]
    expect_true(!is.na(suppressWarnings(as.numeric(first_val))),
                info = paste(sid, "Row 3 does not start with a numeric value"))
  }
})

test_that("D6: all 26 chopped CSVs have at least 10 data rows", {
  skip_if_not(dir.exists(chopped_dir), "chopped/ not found")

  for (sid in ALL_SERIES) {
    path <- file.path(chopped_dir, paste0(sid, "_chopped.csv"))
    skip_if_not(file.exists(path), paste(sid, "not found"))

    lines <- readLines(path, warn = FALSE)
    # Subtract 2 header rows
    data_rows <- length(lines) - 2
    expect_gte(data_rows, 10,
               info = paste(sid, "chopped has fewer than 10 data rows"))
  }
})

# ============================================
# E. Extenbooks (26 files)
# ============================================

context("Artifact Validation — E. Extenbooks")

test_that("E1: extenbooks/ directory exists", {
  expect_true(dir.exists(extenbooks_dir),
              info = paste("extenbooks/ not found at", extenbooks_dir))
})

test_that("E2: all 26 T###_extenbook.xlsx files exist", {
  skip_if_not(dir.exists(extenbooks_dir), "extenbooks/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(extenbooks_dir, paste0(sid, "_extenbook.xlsx"))
    expect_true(file.exists(path),
                info = paste("Missing extenbook:", sid))
  }
})

test_that("E3: each extenbook is non-trivial (>1KB)", {
  skip_if_not(dir.exists(extenbooks_dir), "extenbooks/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(extenbooks_dir, paste0(sid, "_extenbook.xlsx"))
    skip_if_not(file.exists(path), paste(sid, "extenbook not found"))
    expect_gt(file.info(path)$size, 1000,
              info = paste(sid, "extenbook is too small (<1KB)"))
  }
})

test_that("E4: extenbooks are valid xlsx (readxl spot check)", {
  skip_if_not(dir.exists(extenbooks_dir), "extenbooks/ not found")
  skip_if_not(requireNamespace("readxl", quietly = TRUE), "readxl not installed")

  # Spot check 3 extenbooks
  for (sid in c("T501", "T607", "T901")) {
    path <- file.path(extenbooks_dir, paste0(sid, "_extenbook.xlsx"))
    skip_if_not(file.exists(path), paste(sid, "extenbook not found"))

    sheets <- tryCatch(readxl::excel_sheets(path), error = function(e) NULL)
    expect_false(is.null(sheets),
                 info = paste(sid, "extenbook could not be read by readxl"))
    expect_gt(length(sheets), 0,
              info = paste(sid, "extenbook has no sheets"))
  }
})

# ============================================
# F. Series CSVs (26+ files)
# ============================================

context("Artifact Validation — F. Series CSVs")

test_that("F1: series/ directory exists", {
  expect_true(dir.exists(series_dir),
              info = paste("series/ not found at", series_dir))
})

test_that("F2: all 26 T###.csv files exist in series/", {
  skip_if_not(dir.exists(series_dir), "series/ not found")
  for (sid in ALL_SERIES) {
    path <- file.path(series_dir, paste0(sid, ".csv"))
    expect_true(file.exists(path),
                info = paste("Missing series CSV:", sid))
  }
})

test_that("F3: each series CSV has a 'year' column and at least one data column", {
  skip_if_not(dir.exists(series_dir), "series/ not found")

  for (sid in ALL_SERIES) {
    path <- file.path(series_dir, paste0(sid, ".csv"))
    skip_if_not(file.exists(path), paste(sid, "not found"))

    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE, nrows = 5),
                   error = function(e) NULL)
    skip_if(is.null(df), paste("Could not parse", sid, ".csv"))

    expect_true("year" %in% names(df),
                info = paste(sid, "series CSV missing 'year' column"))
    expect_gt(ncol(df), 1,
              info = paste(sid, "series CSV has only 1 column (no data columns)"))
  }
})

test_that("F4: no completely empty data columns in series CSVs", {
  skip_if_not(dir.exists(series_dir), "series/ not found")

  for (sid in ALL_SERIES) {
    path <- file.path(series_dir, paste0(sid, ".csv"))
    skip_if_not(file.exists(path), paste(sid, "not found"))

    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE),
                   error = function(e) NULL)
    skip_if(is.null(df), paste("Could not parse", sid))

    data_cols <- setdiff(names(df), "year")
    for (col in data_cols) {
      all_na <- all(is.na(df[[col]]) | df[[col]] == "")
      expect_false(all_na,
                   info = paste(sid, "column", col, "is completely empty"))
    }
  }
})

test_that("F5: year ranges are plausible (>= 1929 and <= 2025)", {
  skip_if_not(dir.exists(series_dir), "series/ not found")

  for (sid in ALL_SERIES) {
    path <- file.path(series_dir, paste0(sid, ".csv"))
    skip_if_not(file.exists(path), paste(sid, "not found"))

    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE),
                   error = function(e) NULL)
    skip_if(is.null(df) || !("year" %in% names(df)), paste(sid, "cannot check years"))

    years <- df$year[!is.na(df$year)]
    skip_if(length(years) == 0, paste(sid, "has no year values"))

    expect_gte(min(years), 1929,
               info = paste(sid, "has year <1929:", min(years)))
    expect_lte(max(years), 2025,
               info = paste(sid, "has year >2025:", max(years)))
  }
})

# ============================================
# G. Absorbed CSVs (3 files)
# ============================================

context("Artifact Validation — G. Absorbed CSVs")

test_that("G1: absorbed/ directory exists", {
  expect_true(dir.exists(absorbed_dir),
              info = paste("absorbed/ not found at", absorbed_dir))
})

test_that("G2: all 3 chapter absorbed CSVs exist", {
  skip_if_not(dir.exists(absorbed_dir), "absorbed/ not found")

  for (ch in c("05", "06", "09")) {
    path <- file.path(absorbed_dir, paste0("chapter_", ch, "_absorbed.csv"))
    expect_true(file.exists(path),
                info = paste("Missing absorbed CSV: chapter", ch))
  }
})

test_that("G3: absorbed CSVs have required columns", {
  skip_if_not(dir.exists(absorbed_dir), "absorbed/ not found")
  required_cols <- c("series_id", "subseries_id", "year", "value", "source_file")

  for (ch in c("05", "06", "09")) {
    path <- file.path(absorbed_dir, paste0("chapter_", ch, "_absorbed.csv"))
    skip_if_not(file.exists(path), paste("chapter", ch, "absorbed not found"))

    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE, nrows = 5),
                   error = function(e) NULL)
    skip_if(is.null(df), paste("Could not parse chapter", ch, "absorbed"))

    for (col in required_cols) {
      expect_true(col %in% names(df),
                  info = paste("chapter", ch, "absorbed missing column:", col))
    }
  }
})

test_that("G4: absorbed CSVs have plausible year ranges", {
  skip_if_not(dir.exists(absorbed_dir), "absorbed/ not found")

  for (ch in c("05", "06", "09")) {
    path <- file.path(absorbed_dir, paste0("chapter_", ch, "_absorbed.csv"))
    skip_if_not(file.exists(path), paste("chapter", ch, "not found"))

    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE),
                   error = function(e) NULL)
    skip_if(is.null(df) || !("year" %in% names(df)),
            paste("chapter", ch, "cannot check years"))

    years <- df$year[!is.na(df$year)]
    expect_gte(min(years), 1929,
               info = paste("chapter", ch, "absorbed has year <1929"))
    expect_lte(max(years), 2025,
               info = paste("chapter", ch, "absorbed has year >2025"))
  }
})

test_that("G5: absorbed CSVs reference correct series for their chapter", {
  skip_if_not(dir.exists(absorbed_dir), "absorbed/ not found")

  chapter_series <- list(
    "05" = paste0("T5", sprintf("%02d", 1:16)),
    "06" = paste0("T6", sprintf("%02d", 1:9)),
    "09" = "T901"
  )

  for (ch in names(chapter_series)) {
    path <- file.path(absorbed_dir, paste0("chapter_", ch, "_absorbed.csv"))
    skip_if_not(file.exists(path), paste("chapter", ch, "not found"))

    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE),
                   error = function(e) NULL)
    skip_if(is.null(df) || !("series_id" %in% names(df)),
            paste("chapter", ch, "cannot check series_id"))

    actual_series <- unique(df$series_id)
    expected <- chapter_series[[ch]]
    # At least some of the expected series should appear
    overlap <- intersect(actual_series, expected)
    expect_gt(length(overlap), 0,
              info = paste("chapter", ch, "absorbed has no expected series IDs"))
  }
})

test_that("G6: absorbed CSVs have no NA values in key columns", {
  skip_if_not(dir.exists(absorbed_dir), "absorbed/ not found")

  for (ch in c("05", "06", "09")) {
    path <- file.path(absorbed_dir, paste0("chapter_", ch, "_absorbed.csv"))
    skip_if_not(file.exists(path), paste("chapter", ch, "not found"))

    df <- tryCatch(read.csv(path, stringsAsFactors = FALSE),
                   error = function(e) NULL)
    skip_if(is.null(df), paste("chapter", ch, "cannot parse"))

    for (col in c("series_id", "year", "value")) {
      if (col %in% names(df)) {
        na_count <- sum(is.na(df[[col]]))
        expect_equal(na_count, 0,
                     info = paste("chapter", ch, "absorbed has", na_count, "NAs in", col))
      }
    }
  }
})

# ============================================
# H. FPR Files (17 files)
# ============================================

context("Artifact Validation — H. FPR Files")

test_that("H1: docs/figures/ directory exists", {
  expect_true(dir.exists(docs_figures_dir),
              info = paste("docs/figures/ not found at", docs_figures_dir))
})

test_that("H2: all expected Fig_*_FPR.md files exist", {
  skip_if_not(dir.exists(docs_figures_dir), "docs/figures/ not found")

  expected_fprs <- c(
    paste0("Fig_5_", 1:8, "_FPR.md"),
    paste0("Fig_6_", 1:4, "_FPR.md"),
    paste0("Fig_9_", 1:5, "_FPR.md")
  )

  for (f in expected_fprs) {
    path <- file.path(docs_figures_dir, f)
    expect_true(file.exists(path),
                info = paste("Missing FPR:", f))
  }
})

test_that("H3: each FPR is non-empty (>100 bytes)", {
  skip_if_not(dir.exists(docs_figures_dir), "docs/figures/ not found")

  fpr_files <- list.files(docs_figures_dir, pattern = "_FPR\\.md$", full.names = TRUE)
  skip_if(length(fpr_files) == 0, "No FPR files found")

  for (path in fpr_files) {
    expect_gt(file.info(path)$size, 100,
              info = paste(basename(path), "is too small"))
  }
})

test_that("H4: FPR count is at least 17", {
  skip_if_not(dir.exists(docs_figures_dir), "docs/figures/ not found")

  fpr_files <- list.files(docs_figures_dir, pattern = "_FPR\\.md$")
  expect_gte(length(fpr_files), 17,
             info = paste("Expected >=17 FPRs, found", length(fpr_files)))
})

# ============================================
# I. ANU_LEDGER.json
# ============================================

context("Artifact Validation — I. ANU_LEDGER.json")

test_that("I1: ANU_LEDGER.json exists", {
  ledger_path <- file.path(project_root, "ANU_LEDGER.json")
  expect_true(file.exists(ledger_path),
              info = "ANU_LEDGER.json not found at project root")
})

test_that("I2: ANU_LEDGER.json parses and has series entries", {
  ledger_path <- file.path(project_root, "ANU_LEDGER.json")
  skip_if_not(file.exists(ledger_path), "ANU_LEDGER.json not found")

  ledger <- tryCatch(fromJSON(ledger_path), error = function(e) NULL)
  expect_false(is.null(ledger), info = "ANU_LEDGER.json could not be parsed")
  expect_false(is.null(ledger$series), info = "ANU_LEDGER.json has no 'series' key")
})

test_that("I3: ANU_LEDGER has entries for all 26 series", {
  ledger_path <- file.path(project_root, "ANU_LEDGER.json")
  skip_if_not(file.exists(ledger_path), "ANU_LEDGER.json not found")

  ledger <- tryCatch(fromJSON(ledger_path), error = function(e) NULL)
  skip_if(is.null(ledger) || is.null(ledger$series), "Ledger not parseable")

  ledger_series <- names(ledger$series)
  for (sid in ALL_SERIES) {
    expect_true(sid %in% ledger_series,
                info = paste(sid, "missing from ANU_LEDGER"))
  }
})

test_that("I4: ANU_LEDGER summary totals are consistent", {
  ledger_path <- file.path(project_root, "ANU_LEDGER.json")
  skip_if_not(file.exists(ledger_path), "ANU_LEDGER.json not found")

  ledger <- tryCatch(fromJSON(ledger_path), error = function(e) NULL)
  skip_if(is.null(ledger) || is.null(ledger$summary), "Ledger summary not found")

  expect_equal(ledger$summary$total_series, 26,
               info = "Ledger total_series should be 26")
  expect_equal(ledger$summary$research_jsons, 26,
               info = "Ledger research_jsons should be 26")
  expect_equal(ledger$summary$decompositions, 26,
               info = "Ledger decompositions should be 26")
  expect_equal(ledger$summary$dprs, 26,
               info = "Ledger dprs should be 26")
  expect_equal(ledger$summary$chopped_csvs, 26,
               info = "Ledger chopped_csvs should be 26")
  expect_equal(ledger$summary$extenbooks, 26,
               info = "Ledger extenbooks should be 26")
})

# ============================================
# J. SUBSOURCE_METADATA.json
# ============================================

context("Artifact Validation — J. SUBSOURCE_METADATA.json")

test_that("J1: SUBSOURCE_METADATA.json exists", {
  path <- file.path(shiny_dir, "SUBSOURCE_METADATA.json")
  expect_true(file.exists(path),
              info = paste("SUBSOURCE_METADATA.json not found at", shiny_dir))
})

test_that("J2: SUBSOURCE_METADATA.json parses and has entries", {
  path <- file.path(shiny_dir, "SUBSOURCE_METADATA.json")
  skip_if_not(file.exists(path), "SUBSOURCE_METADATA.json not found")

  meta <- tryCatch(fromJSON(path), error = function(e) NULL)
  expect_false(is.null(meta), info = "SUBSOURCE_METADATA.json could not be parsed")

  # Should have some content (list or data.frame)
  if (is.data.frame(meta)) {
    expect_gt(nrow(meta), 0, info = "SUBSOURCE_METADATA is empty data frame")
  } else if (is.list(meta)) {
    expect_gt(length(meta), 0, info = "SUBSOURCE_METADATA is empty list")
  }
})

# ============================================
# K. Cross-reference consistency
# ============================================

context("Artifact Validation — K. Cross-Reference Consistency")

test_that("K1: series_registry.json exists and parses", {
  reg_path <- file.path(project_root, "series_registry.json")
  expect_true(file.exists(reg_path),
              info = "series_registry.json not found")

  reg <- tryCatch(fromJSON(reg_path), error = function(e) NULL)
  expect_false(is.null(reg), info = "series_registry.json could not be parsed")
})

test_that("K2: series_registry series list matches produced series CSVs", {
  reg_path <- file.path(project_root, "series_registry.json")
  skip_if_not(file.exists(reg_path), "series_registry.json not found")
  skip_if_not(dir.exists(series_dir), "series/ not found")

  reg <- tryCatch(fromJSON(reg_path), error = function(e) NULL)
  skip_if(is.null(reg) || is.null(reg$series), "Registry not parseable")

  registry_ids <- names(reg$series)
  series_files <- list.files(series_dir, pattern = "^T\\d+\\.csv$")
  series_csv_ids <- gsub("\\.csv$", "", series_files)

  # Every registry series in our 26 should have a CSV
  for (sid in ALL_SERIES) {
    if (sid %in% registry_ids) {
      expect_true(sid %in% series_csv_ids,
                  info = paste(sid, "in registry but no series CSV"))
    }
  }
})

test_that("K3: PIPELINE_STATE.json exists and has entries for all 26 series", {
  ps_path <- file.path(project_root, "PIPELINE_STATE.json")
  expect_true(file.exists(ps_path),
              info = "PIPELINE_STATE.json not found")

  ps <- tryCatch(fromJSON(ps_path), error = function(e) NULL)
  skip_if(is.null(ps) || is.null(ps$series), "PIPELINE_STATE not parseable")

  ps_ids <- names(ps$series)
  for (sid in ALL_SERIES) {
    expect_true(sid %in% ps_ids,
                info = paste(sid, "missing from PIPELINE_STATE"))
  }
})

test_that("K4: PIPELINE_STATE all 26 core series are loaded", {
  ps_path <- file.path(project_root, "PIPELINE_STATE.json")
  skip_if_not(file.exists(ps_path), "PIPELINE_STATE.json not found")

  ps <- tryCatch(fromJSON(ps_path), error = function(e) NULL)
  skip_if(is.null(ps) || is.null(ps$series), "PIPELINE_STATE not parseable")

  for (sid in ALL_SERIES) {
    entry <- ps$series[[sid]]
    skip_if(is.null(entry), paste(sid, "not in PIPELINE_STATE"))
    expect_true(isTRUE(entry$loaded),
                info = paste(sid, "is not marked as loaded in PIPELINE_STATE"))
  }
})

test_that("K5: FIGURE_SERIES_CATALOG.json figure IDs match FPR files", {
  catalog_path <- file.path(project_root, "FIGURE_SERIES_CATALOG.json")
  skip_if_not(file.exists(catalog_path), "FIGURE_SERIES_CATALOG.json not found")
  skip_if_not(dir.exists(docs_figures_dir), "docs/figures/ not found")

  catalog <- tryCatch(fromJSON(catalog_path), error = function(e) NULL)
  skip_if(is.null(catalog), "Could not parse FIGURE_SERIES_CATALOG")

  fpr_files <- list.files(docs_figures_dir, pattern = "_FPR\\.md$")
  fpr_ids <- gsub("_FPR\\.md$", "", fpr_files)

  catalog_ids <- catalog$figure_id
  skip_if(is.null(catalog_ids), "No figure_id column in catalog")

  # Every FPR file should have a catalog entry
  for (fid in fpr_ids) {
    expect_true(fid %in% catalog_ids,
                info = paste(fid, "has FPR file but no catalog entry"))
  }
})

test_that("K6: ANU_LEDGER series paths are consistent with actual files", {
  ledger_path <- file.path(project_root, "ANU_LEDGER.json")
  skip_if_not(file.exists(ledger_path), "ANU_LEDGER.json not found")

  ledger <- tryCatch(fromJSON(ledger_path), error = function(e) NULL)
  skip_if(is.null(ledger) || is.null(ledger$series), "Ledger not parseable")

  # Spot check 5 series
  for (sid in c("T501", "T506", "T607", "T609", "T901")) {
    entry <- ledger$series[[sid]]
    skip_if(is.null(entry), paste(sid, "not in ledger"))

    # Check that declared paths resolve (relative to project root's parent)
    if (!is.null(entry$research) && nchar(entry$research) > 0) {
      # Paths in ledger are relative to project parent (e.g., "Technical/research/...")
      full_path <- file.path(dirname(project_root), entry$research)
      expect_true(file.exists(full_path),
                  info = paste(sid, "ledger research path does not resolve:", entry$research))
    }
    if (!is.null(entry$chopped) && nchar(entry$chopped) > 0) {
      full_path <- file.path(dirname(project_root), entry$chopped)
      expect_true(file.exists(full_path),
                  info = paste(sid, "ledger chopped path does not resolve:", entry$chopped))
    }
  }
})

# ============================================
# Summary
# ============================================

cat("\n===================================================\n")
cat("Artifact Validation Complete\n")
cat("===================================================\n")
cat("  Sections: A-K (11 artifact categories)\n")
cat("  Series checked: 26 (T501-T516, T601-T609, T901)\n")
cat("  Artifact types: research, decomposition, DPR, chopped,\n")
cat("    extenbook, series CSV, absorbed, FPR, ledger,\n")
cat("    subsource metadata, cross-references\n")
cat("===================================================\n")
