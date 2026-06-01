# RMWND Shiny — Helper Functions
# Defensive access, badges, section headers, and UI utilities.

safe_field <- function(obj, field, default = NULL) {
  if (is.null(obj) || !is.list(obj)) return(default)
  val <- tryCatch(obj[[field]], error = function(e) NULL)
  if (is.null(val)) default else val
}

safe_str <- function(obj, field, default = "") {
  val <- safe_field(obj, field, default)
  if (is.null(val) || length(val) == 0 || is.na(val[1])) default else as.character(val[1])
}

`%||%` <- function(a, b) if (!is.null(a)) a else b

clean_text <- function(txt) {
  if (is.null(txt) || !nzchar(txt)) return("")
  gsub("\\s+", " ", trimws(txt))
}

format_year_range <- function(start, end) {
  s <- if (!is.null(start) && !is.na(start)) as.character(start) else "?"

  e <- if (!is.null(end) && !is.na(end)) as.character(end) else "?"
  paste0(s, " – ", e)
}

status_badge <- function(status) {
  colors <- list(
    verified      = "#28a745",
    extended_2025 = "#543c8a",
    calculated    = "#ffc107",
    needs_source  = "#dc3545",
    conceptual    = "#6c757d",
    partial       = "#fd7e14",
    historical    = "#8c564b",
    not_applicable = "#6c757d"
  )
  labels <- list(
    verified      = "\u2713 Verified",
    extended_2025 = "\u2197 Extended",
    calculated    = "\u2699 Calculated",
    needs_source  = "\u26a0 Needs Source",
    conceptual    = "\U0001f4ca Conceptual",
    partial       = "\u25d0 Partial",
    historical    = "\U0001f4dc Historical",
    not_applicable = "\u2014 N/A"
  )
  bg <- colors[[status]] %||% "#6c757d"
  lbl <- labels[[status]] %||% status
  tags$span(
    class = "status-badge",
    style = paste0("background:", bg, ";"),
    lbl
  )
}

section_header <- function(title, type = "info") {
  colors <- list(
    success = "#28a745",
    warning = "#ffc107",
    info    = "#543c8a",
    danger  = "#dc3545",
    primary = "#543c8a"
  )
  col <- colors[[type]] %||% "#543c8a"
  tags$div(
    style = paste0("border-left: 4px solid ", col, "; padding: 8px 12px; margin: 15px 0 10px 0; ",
                   "font-weight: bold; color: var(--text-primary); font-size: 14px;"),
    title
  )
}

methodology_item <- function(label, value) {
  tags$div(
    class = "methodology-item",
    tags$span(class = "info-label", label),
    tags$div(class = "info-value", as.character(value))
  )
}

source_link <- function(text, url, type = "url") {
  if (is.null(url) || !nzchar(url)) {
    return(tags$span(style = "color: var(--text-muted);", text))
  }
  tags$a(class = "source-link", href = url, target = "_blank", text)
}

book_quote_panel <- function(text, source_label = "Shaikh (2016)") {
  tags$div(
    class = "book-quote",
    tags$div(
      style = "font-style: italic; color: var(--text-primary); line-height: 1.6;",
      paste0('"', text, '"')
    ),
    tags$div(
      style = "color: var(--text-muted); font-size: 0.9em; margin-top: 10px;",
      paste0("— ", source_label)
    )
  )
}

log_info    <- function(fmt, ...) message(sprintf(paste0("[INFO] ", fmt), ...))
log_debug   <- function(fmt, ...) {} # silent in production
log_warn    <- function(fmt, ...) message(sprintf(paste0("[WARN] ", fmt), ...))
log_error   <- function(fmt, ...) message(sprintf(paste0("[ERROR] ", fmt), ...))
log_section <- function(title) message(paste0("\n=== ", title, " ==="))
