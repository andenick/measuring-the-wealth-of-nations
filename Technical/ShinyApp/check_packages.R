# Package Checker for Shaikh-Tonak Shiny App
# Automatically installs missing required packages

cat("================================================================================\n")
cat("SHAIKH-TONAK SHINY APP - PACKAGE CHECKER\n")
cat("================================================================================\n\n")

# List of required packages
required_packages <- c(
  "shiny",           # Core Shiny framework
  "shinydashboard",  # Dashboard layout
  "tidyverse",       # Data manipulation (includes dplyr, ggplot2, readr, tidyr)
  "plotly",          # Interactive plots
  "DT",              # Interactive data tables
  "scales",          # Axis/number formatting
  "openxlsx"         # Excel export (optional but recommended)
)

# Check which packages are already installed
installed <- rownames(installed.packages())
missing <- required_packages[!required_packages %in% installed]

if (length(missing) == 0) {
  cat("All required packages are already installed!\n\n")
  cat("Installed packages:\n")
  for (pkg in required_packages) {
    cat(sprintf("  - %s (version %s)\n", pkg, packageVersion(pkg)))
  }
  cat("\nYou're ready to launch the app!\n")
  cat("Run: shiny::runApp('ShinyApp')\n")

} else {
  cat(sprintf("Found %d missing packages:\n", length(missing)))
  for (pkg in missing) {
    cat(sprintf("  - %s\n", pkg))
  }

  cat("\nInstalling missing packages...\n\n")

  for (pkg in missing) {
    cat(sprintf("Installing %s...", pkg))
    tryCatch({
      install.packages(pkg, dependencies = TRUE, quiet = TRUE)
      cat(" [OK]\n")
    }, error = function(e) {
      cat(" [FAILED]\n")
      cat(sprintf("  Error: %s\n", e$message))
    })
  }

  cat("\n================================================================================\n")
  cat("Installation complete!\n")
  cat("\nVerifying installation...\n")

  # Re-check
  installed <- rownames(installed.packages())
  still_missing <- required_packages[!required_packages %in% installed]

  if (length(still_missing) == 0) {
    cat("\nAll packages successfully installed!\n")
    cat("You're ready to launch the app!\n")
    cat("Run: shiny::runApp('ShinyApp')\n")
  } else {
    cat("\nWARNING: Some packages failed to install:\n")
    for (pkg in still_missing) {
      cat(sprintf("  - %s\n", pkg))
    }
    cat("\nPlease install these manually:\n")
    cat(sprintf("  install.packages(c('%s'))\n", paste(still_missing, collapse = "', '")))
  }
}

cat("\n================================================================================\n")
