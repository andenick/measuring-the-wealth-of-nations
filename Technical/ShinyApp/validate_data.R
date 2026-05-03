# Data Validator for Shaikh-Tonak Shiny App
# Checks that all required data files exist and are readable

library(readr)

cat("================================================================================\n")
cat("SHAIKH-TONAK SHINY APP - DATA VALIDATOR\n")
cat("================================================================================\n\n")

# Define expected data files
data_dir <- "data"
expected_files <- c(
  "profit_rates_1948_1989.csv",
  "exploitation_composition_1948_1989.csv",
  "employment_1948_1989.csv",
  "productivity_1948_1989.csv",
  "government_1948_1989.csv",
  "validation_targets.csv",
  "comprehensive_1948_1989.csv"
)

# Check if data directory exists
if (!dir.exists(data_dir)) {
  cat(sprintf("ERROR: Data directory '%s' not found!\n", data_dir))
  cat("Please ensure you're running this from the ShinyApp directory.\n")
  stop("Data directory missing")
}

cat(sprintf("Checking for %d required data files...\n\n", length(expected_files)))

all_ok <- TRUE

for (file in expected_files) {
  filepath <- file.path(data_dir, file)

  # Check if file exists
  if (!file.exists(filepath)) {
    cat(sprintf("[FAIL] %s - File not found\n", file))
    all_ok <- FALSE
    next
  }

  # Try to read the file
  tryCatch({
    data <- read_csv(filepath, show_col_types = FALSE)
    n_rows <- nrow(data)
    n_cols <- ncol(data)

    # Check for reasonable data size
    if (n_rows == 0) {
      cat(sprintf("[WARN] %s - File is empty (0 rows)\n", file))
      all_ok <- FALSE
    } else if (n_cols == 0) {
      cat(sprintf("[WARN] %s - No columns found\n", file))
      all_ok <- FALSE
    } else {
      cat(sprintf("[OK]   %s - %d rows, %d columns\n", file, n_rows, n_cols))

      # Show column names for first file as sample
      if (file == expected_files[1]) {
        cat(sprintf("       Columns: %s\n", paste(head(names(data), 5), collapse = ", ")))
      }
    }

  }, error = function(e) {
    cat(sprintf("[FAIL] %s - Error reading file: %s\n", file, e$message))
    all_ok <- FALSE
  })
}

cat("\n================================================================================\n")

if (all_ok) {
  cat("DATA VALIDATION PASSED\n")
  cat("\nAll data files are present and readable!\n")
  cat("You're ready to launch the app!\n")
  cat("Run: shiny::runApp()\n")
} else {
  cat("DATA VALIDATION FAILED\n")
  cat("\nSome data files are missing or corrupted.\n")
  cat("Please check the data preprocessing step.\n")
  cat("See: ../data/Tables/ for source data\n")
}

cat("================================================================================\n")
