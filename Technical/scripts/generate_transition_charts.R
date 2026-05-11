# ============================================
# generate_transition_charts.R
# ============================================
# Generates transition visualization charts for all 9 extended series.
# Shows book-period vs extension data overlay with splice marker.
#
# Usage: source("scripts/generate_transition_charts.R")
# Output: Outputs/Figures/transition_TXXX_splice_1989.html (9 files)
#
# Created: 2026-02-25 (Session 8 — G013 resolution)
# ============================================

library(plotly)
library(htmlwidgets)

# ── Resolve paths ──────────────────────────────────────────────────────────
project_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), winslash = "/")
shiny_r_dir  <- file.path(project_root, "ShinyApp", "R")
output_dir   <- normalizePath(file.path(project_root, "..", "Outputs", "Figures"), winslash = "/", mustWork = FALSE)

# Create output directory if needed
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

# ── Source chart infrastructure ────────────────────────────────────────────
source(file.path(shiny_r_dir, "data_loader.R"))
source(file.path(shiny_r_dir, "chart_builder.R"))

# ── Data path helpers ──────────────────────────────────────────────────────
chopped_dir <- file.path(project_root, "ST_Chopped", "ch05")
data_dir    <- file.path(project_root, "data")

safe_read <- function(path) {
  if (file.exists(path)) {
    read.csv(path, stringsAsFactors = FALSE)
  } else {
    warning(paste("File not found:", path))
    NULL
  }
}

# ── Define series data sources ─────────────────────────────────────────────
series_config <- list(
  T504 = list(
    book_file = file.path(chopped_dir, "ExploitationComposition_1948_1989.csv"),
    ext_file  = file.path(chopped_dir, "ExploitationComposition_1948_2024.csv")
  ),
  T505 = list(
    book_file = file.path(chopped_dir, "ExploitationComposition_1948_1989.csv"),
    ext_file  = file.path(chopped_dir, "ExploitationComposition_1948_2024.csv")
  ),
  T506 = list(
    book_file = file.path(chopped_dir, "ExploitationComposition_1948_1989.csv"),
    ext_file  = file.path(chopped_dir, "ExploitationComposition_1948_2024.csv")
  ),
  T511 = list(
    book_file = file.path(chopped_dir, "Table5_7_KeyRatios.csv"),
    ext_file  = file.path(chopped_dir, "Table5_7_Extended.csv")
  ),
  T512 = list(
    book_file = file.path(chopped_dir, "Table5_7_KeyRatios.csv"),
    ext_file  = file.path(chopped_dir, "Table5_7_Extended.csv")
  ),
  T513 = list(
    book_file = file.path(chopped_dir, "ProfitRates_1948_1989.csv"),
    ext_file  = file.path(chopped_dir, "ProfitRates_1948_2024.csv")
  ),
  T514 = list(
    book_file = file.path(chopped_dir, "ProfitRates_1948_1989.csv"),
    ext_file  = file.path(chopped_dir, "ProfitRates_1948_2024.csv")
  ),
  T515 = list(
    book_file = file.path(chopped_dir, "Employment_1948_1989.csv"),
    ext_file  = file.path(chopped_dir, "Employment_1948_1989.csv")
  ),
  T516 = list(
    book_file = file.path(chopped_dir, "Employment_1948_1989.csv"),
    ext_file  = file.path(chopped_dir, "Employment_1948_1989.csv")
  )
)

# ── Generate charts ────────────────────────────────────────────────────────
cat("Generating transition charts for 9 extended series...\n\n")
results <- list()

for (sid in names(series_config)) {
  cfg <- series_config[[sid]]
  cat(paste0("  ", sid, ": "))

  tryCatch({
    book_data <- safe_read(cfg$book_file)
    ext_data  <- safe_read(cfg$ext_file)

    if (is.null(book_data) || is.null(ext_data)) {
      cat("SKIP — data file not found\n")
      results[[sid]] <- "SKIP"
      next
    }

    # Filter book data to book period only
    if ("year" %in% names(book_data)) {
      book_data <- book_data[book_data$year <= 1989, ]
    }
    # Extension data: keep all years (or just post-splice)
    if ("year" %in% names(ext_data)) {
      ext_data <- ext_data[ext_data$year >= 1989, ]
    }

    # Build transition chart
    p <- build_transition_chart(sid, book_data, ext_data, splice_year = 1989)

    # Save as HTML
    out_file <- file.path(output_dir, paste0("transition_", sid, "_splice_1989.html"))
    htmlwidgets::saveWidget(p, out_file, selfcontained = TRUE)

    cat(paste0("OK -> ", basename(out_file), "\n"))
    results[[sid]] <- "OK"

  }, error = function(e) {
    cat(paste0("ERROR — ", e$message, "\n"))
    results[[sid]] <<- paste0("ERROR: ", e$message)
  })
}

# ── Summary ────────────────────────────────────────────────────────────────
cat("\n--- Summary ---\n")
cat(paste0("  Total: ", length(results), "\n"))
cat(paste0("  OK:    ", sum(results == "OK"), "\n"))
cat(paste0("  SKIP:  ", sum(results == "SKIP"), "\n"))
cat(paste0("  ERROR: ", sum(grepl("^ERROR", results)), "\n"))
cat(paste0("\nOutput directory: ", output_dir, "\n"))
