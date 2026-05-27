# RMWND Shiny -- Structured Logger
# Writes structured log entries to logs/ for framework cascade compliance.
# Consumed by validate_data.R and global.R.

LOG_DIR <- file.path(normalizePath(file.path(".."), mustWork = FALSE), "..", "viz", "shiny", "logs")

ensure_log_dir <- function() {
  dir <- normalizePath(file.path("logs"), mustWork = FALSE)
  if (!dir.exists(dir)) dir.create(dir, recursive = TRUE, showWarnings = FALSE)
  dir
}

log_to_file <- function(level, message, context = list()) {
  dir <- ensure_log_dir()
  log_file <- file.path(dir, paste0("app_", format(Sys.Date(), "%Y%m%d"), ".log"))

  entry <- paste0(
    format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"),
    " [", toupper(level), "] ",
    message
  )
  if (length(context) > 0) {
    ctx_str <- paste(names(context), vapply(context, as.character, character(1)),
      sep = "=", collapse = " "
    )
    entry <- paste0(entry, " | ", ctx_str)
  }

  tryCatch(
    cat(entry, "\n", file = log_file, append = TRUE),
    error = function(e) message(sprintf("[LOG-ERROR] Cannot write log: %s", e$message))
  )
}

log_structured <- function(action, details = list()) {
  dir <- ensure_log_dir()
  log_file <- file.path(dir, "structured.jsonl")

  entry <- list(
    timestamp = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"),
    action = action
  )
  entry <- c(entry, details)

  tryCatch(
    {
      json_str <- jsonlite::toJSON(entry, auto_unbox = TRUE)
      cat(json_str, "\n", file = log_file, append = TRUE)
    },
    error = function(e) message(sprintf("[LOG-ERROR] %s", e$message))
  )
}
