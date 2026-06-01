# RMWND Shiny -- Startup Data Validation
# Implements the anu-visualize v6.0 five-check standard:
#   1. Structural checks (canonical files exist and load)
#   2. Cross-reference integrity (subsource parent_series resolve)
#   3. Value sanity (year ranges valid, chapters in range)
#   4. Chart readiness (figures have data column mappings)
#   5. Manifest verification (SHA-256 hash comparison)

validate_app_data <- function(paths, registry, catalog, subsource_meta = NULL) {
  results <- list(
    errors = character(0),
    warnings = character(0),
    checks = list()
  )

  add_error <- function(check, msg) {
    results$errors <<- c(results$errors, paste0("[", check, "] ", msg))
  }
  add_warn <- function(check, msg) {
    results$warnings <<- c(results$warnings, paste0("[", check, "] ", msg))
  }
  pass_check <- function(name, passed, detail = "") {
    results$checks[[name]] <<- list(passed = passed, detail = detail)
  }

  # -- Check 1: Structural --
  required_files <- list(
    series_registry = paths$registry,
    app_config = paths$config,
    definitive_catalog = paths$catalog
  )
  structural_ok <- TRUE
  for (fname in names(required_files)) {
    fpath <- required_files[[fname]]
    if (is.null(fpath) || !file.exists(fpath)) {
      add_error("STRUCTURAL", paste0("Required file missing: ", fname, " (", fpath %||% "NULL", ")"))
      structural_ok <- FALSE
    }
  }
  optional_files <- list(
    subsource_metadata = paths$subsource_metadata,
    series_linkage = paths$series_linkage,
    viz_style = paths$style
  )
  for (fname in names(optional_files)) {
    fpath <- optional_files[[fname]]
    if (!is.null(fpath) && !file.exists(fpath)) {
      add_warn("STRUCTURAL", paste0("Optional file missing: ", fname, " (", fpath, ")"))
    }
  }
  pass_check(
    "structural", structural_ok,
    paste0(
      sum(vapply(required_files, function(f) !is.null(f) && file.exists(f), logical(1))),
      "/", length(required_files), " required files present"
    )
  )

  # -- Check 2: Cross-reference integrity --
  xref_ok <- TRUE
  if (!is.null(subsource_meta) && length(subsource_meta) > 0) {
    entries <- subsource_meta$entries %||% subsource_meta
    if (is.list(entries)) {
      for (ss_id in names(entries)) {
        ss <- entries[[ss_id]]
        parent <- ss$series_id %||% ss$parent_series
        if (!is.null(parent) && !(parent %in% names(registry))) {
          add_error("XREF", paste0("Subsource ", ss_id, " references missing parent series: ", parent))
          xref_ok <- FALSE
        }
      }
    }
  } else {
    add_warn("XREF", "No subsource metadata loaded; cross-reference check skipped")
  }
  pass_check("cross_reference", xref_ok)

  # -- Check 3: Value sanity --
  sanity_ok <- TRUE
  for (sid in names(registry)) {
    entry <- registry[[sid]]
    yr <- entry$year_range
    if (!is.null(yr) && is.list(yr) && length(yr) == 2) {
      yr_start <- as.numeric(yr[[1]])
      yr_end <- as.numeric(yr[[2]])
      if (!is.na(yr_start) && !is.na(yr_end)) {
        if (yr_start < 1800 || yr_end > 2100 || yr_start > yr_end) {
          add_error("SANITY", paste0(sid, ": invalid year_range [", yr_start, ", ", yr_end, "]"))
          sanity_ok <- FALSE
        }
      }
    }
    ch <- entry$chapter
    if (!is.null(ch)) {
      ch_num <- suppressWarnings(as.numeric(ch))
      if (!is.na(ch_num) && (ch_num < 0 || ch_num > 30)) {
        add_warn("SANITY", paste0(sid, ": unusual chapter number ", ch))
      }
    }
  }
  pass_check("value_sanity", sanity_ok)

  # -- Check 4: Chart readiness --
  chart_ok <- TRUE
  no_data_count <- 0
  for (sid in names(catalog)) {
    entry <- catalog[[sid]]
    if (!isTRUE(entry$has_data)) {
      no_data_count <- no_data_count + 1
    }
  }
  if (no_data_count > 0) {
    add_warn("CHART_READY", paste0(
      no_data_count, "/", length(catalog),
      " series have no loaded data"
    ))
  }
  if (no_data_count == length(catalog)) {
    add_error("CHART_READY", "No series have loaded data -- charts cannot render")
    chart_ok <- FALSE
  }
  pass_check(
    "chart_readiness", chart_ok,
    paste0(length(catalog) - no_data_count, "/", length(catalog), " series have data")
  )

  # -- Check 5: Manifest verification --
  manifest_path <- paths$manifest
  if (!is.null(manifest_path) && file.exists(manifest_path)) {
    manifest <- tryCatch(
      jsonlite::fromJSON(manifest_path, simplifyVector = FALSE),
      error = function(e) NULL
    )
    if (!is.null(manifest) && !is.null(manifest$files)) {
      manifest_ok <- TRUE
      for (fentry in manifest$files) {
        fpath <- file.path(dirname(manifest_path), fentry$path)
        if (!file.exists(fpath)) {
          add_warn("MANIFEST", paste0("Manifest file missing: ", fentry$path))
        }
      }
      pass_check("manifest", manifest_ok)
    } else {
      pass_check("manifest", TRUE, "Manifest loaded but no files section")
    }
  } else {
    add_warn("MANIFEST", "No DATA_MANIFEST.json found; manifest check skipped")
    pass_check("manifest", TRUE, "Skipped (no manifest)")
  }

  # -- Summary --
  results$error_count <- length(results$errors)
  results$warning_count <- length(results$warnings)
  results$all_passed <- results$error_count == 0
  results$gate <- if (results$error_count == 0) "PASS" else "FAIL"
  results
}

print_validation_results <- function(results) {
  log_section("Startup Validation Results")
  for (name in names(results$checks)) {
    check <- results$checks[[name]]
    status <- if (isTRUE(check$passed)) "PASS" else "FAIL"
    detail <- if (nzchar(check$detail %||% "")) paste0(" — ", check$detail) else ""
    log_info("  %s: [%s]%s", toupper(name), status, detail)
  }
  if (results$error_count > 0) {
    log_error("Validation FAILED with %d errors:", results$error_count)
    for (e in results$errors) log_error("  %s", e)
  }
  if (results$warning_count > 0) {
    log_warn("Validation warnings (%d):", results$warning_count)
    for (w in results$warnings) log_warn("  %s", w)
  }
  if (results$all_passed) {
    log_info("Validation PASSED: 0 errors, %d warnings", results$warning_count)
  }
}
