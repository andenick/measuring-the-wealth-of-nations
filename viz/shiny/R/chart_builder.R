# RMWND Shiny — Chart Builder
# Plotly chart construction with view modes, recession bands, splice markers,
# and dual-axis support. Consumes viz_style.json for theming.

RECESSIONS_NBER <- data.frame(
  start = c(1948, 1953, 1957, 1960, 1969, 1973, 1980, 1981, 1990, 2001, 2007, 2020),
  end   = c(1949, 1954, 1958, 1961, 1970, 1975, 1980, 1982, 1991, 2001, 2009, 2020),
  stringsAsFactors = FALSE
)

SPLICE_YEAR <- 1989

# Active chart theme (mutable; toggled by set_chart_theme())
CHART_THEME <- list(
  paper_bgcolor = "#ffffff",
  plot_bgcolor  = "#ffffff",
  font_color    = "#333333",
  grid_color    = "#e8e8e8",
  zeroline_color = "#cccccc",
  legend_bgcolor = "rgba(255,255,255,0.85)"
)

set_chart_theme <- function(mode) {
  if (mode == "dark") {
    CHART_THEME$paper_bgcolor  <<- "#16213e"
    CHART_THEME$plot_bgcolor   <<- "#16213e"
    CHART_THEME$font_color     <<- "#e8e8e8"
    CHART_THEME$grid_color     <<- "#333333"
    CHART_THEME$zeroline_color <<- "#555555"
    CHART_THEME$legend_bgcolor <<- "rgba(22,33,62,0.85)"
  } else {
    CHART_THEME$paper_bgcolor  <<- "#ffffff"
    CHART_THEME$plot_bgcolor   <<- "#ffffff"
    CHART_THEME$font_color     <<- "#333333"
    CHART_THEME$grid_color     <<- "#e8e8e8"
    CHART_THEME$zeroline_color <<- "#cccccc"
    CHART_THEME$legend_bgcolor <<- "rgba(255,255,255,0.85)"
  }
}

SERIES_COLORS <- c(
  "#ffcc00", "#00ccff", "#ff7f0e", "#2ca02c",
  "#d62728", "#9467bd", "#e377c2", "#8c564b",
  "#17becf", "#bcbd22", "#7f7f7f", "#1f77b4",
  "#98df8a", "#ff9896", "#c5b0d5", "#ffbb78"
)

# ---------------------------------------------------------------------------
# Core layout helper
# ---------------------------------------------------------------------------
apply_chart_layout <- function(p, title, y_label, subtitle = NULL) {
  full_title <- if (!is.null(subtitle)) {
    list(text = paste0(title, "<br><sup>", subtitle, "</sup>"),
         font = list(size = 14, color = CHART_THEME$font_color))
  } else {
    list(text = title, font = list(size = 14, color = CHART_THEME$font_color))
  }

  p %>% layout(
    title = full_title,
    xaxis = list(
      title = list(text = "Year", font = list(color = CHART_THEME$font_color)),
      dtick = 5,
      gridcolor = CHART_THEME$grid_color,
      zerolinecolor = CHART_THEME$zeroline_color,
      tickfont = list(color = CHART_THEME$font_color)
    ),
    yaxis = list(
      title = list(text = y_label, font = list(color = CHART_THEME$font_color)),
      gridcolor = CHART_THEME$grid_color,
      zerolinecolor = CHART_THEME$zeroline_color,
      tickfont = list(color = CHART_THEME$font_color)
    ),
    hovermode = "x unified",
    legend = list(
      orientation = "h", yanchor = "bottom", y = -0.18,
      xanchor = "center", x = 0.5,
      bgcolor = CHART_THEME$legend_bgcolor,
      font = list(color = CHART_THEME$font_color)
    ),
    plot_bgcolor  = CHART_THEME$plot_bgcolor,
    paper_bgcolor = CHART_THEME$paper_bgcolor,
    margin = list(l = 70, r = 50, t = 60, b = 80),
    font = list(family = "Inter, system-ui, -apple-system, sans-serif",
                color = CHART_THEME$font_color)
  )
}

# ---------------------------------------------------------------------------
# Recession bands
# ---------------------------------------------------------------------------
add_recession_bands <- function(p, year_range) {
  recs <- RECESSIONS_NBER[RECESSIONS_NBER$end >= year_range[1] &
                            RECESSIONS_NBER$start <= year_range[2], ]
  if (nrow(recs) == 0) return(p)

  shapes <- lapply(seq_len(nrow(recs)), function(i) {
    list(type = "rect", fillcolor = "rgba(200,200,200,0.2)",
         line = list(width = 0),
         x0 = recs$start[i], x1 = recs$end[i],
         y0 = 0, y1 = 1, yref = "paper", layer = "below")
  })
  p %>% layout(shapes = shapes)
}

# ---------------------------------------------------------------------------
# Book / Extension splice marker
# ---------------------------------------------------------------------------
add_splice_marker <- function(p, splice_year = SPLICE_YEAR) {
  existing <- tryCatch(p$x$layoutAttrs, error = function(e) list())
  shapes <- list(list(
    type = "line", x0 = splice_year, x1 = splice_year,
    y0 = 0, y1 = 1, yref = "paper",
    line = list(color = "#605ca8", dash = "dash", width = 1.5)
  ))
  p %>%
    layout(shapes = shapes) %>%
    add_annotations(
      x = splice_year, y = 1, yref = "paper",
      text = "Book | Extension", showarrow = FALSE,
      font = list(size = 9, color = "#605ca8"), yanchor = "bottom"
    )
}

# ---------------------------------------------------------------------------
# Main chart builder — routes by view mode
# ---------------------------------------------------------------------------
build_series_chart <- function(series_entry, view_mode, year_range,
                               selected_subsources = NULL, dual_axis = FALSE) {
  sid <- series_entry$series_id
  name <- series_entry$name %||% sid
  df <- series_entry$data

  if (is.null(df) || nrow(df) == 0) {
    return(plotly_empty() %>% layout(title = paste("No data for", sid)))
  }

  df <- df[df$year >= year_range[1] & df$year <= year_range[2], ]
  if (nrow(df) == 0) {
    return(plotly_empty() %>% layout(title = paste("No data in range for", sid)))
  }

  numeric_cols <- setdiff(names(df)[vapply(df, is.numeric, logical(1))], "year")
  if (length(numeric_cols) == 0) {
    return(plotly_empty() %>% layout(title = paste("No numeric columns for", sid)))
  }

  p <- plot_ly()

  if (view_mode == "final_series") {
    col <- if (sid %in% numeric_cols) sid else numeric_cols[1]
    p <- p %>% add_trace(
      data = df, x = ~year, y = as.formula(paste0("~`", col, "`")),
      type = "scatter", mode = "lines+markers",
      name = name, line = list(color = "#543c8a", width = 2),
      marker = list(size = 4)
    )
  } else if (view_mode == "author_construction") {
    book <- df[df$year <= SPLICE_YEAR, ]
    if (nrow(book) > 0) {
      col <- if (sid %in% numeric_cols) sid else numeric_cols[1]
      p <- p %>% add_trace(
        data = book, x = ~year, y = as.formula(paste0("~`", col, "`")),
        type = "scatter", mode = "lines+markers",
        name = paste0(name, " (Book)"),
        line = list(color = "#3c8dbc", width = 2),
        marker = list(size = 4)
      )
    }
  } else if (view_mode == "final_extension") {
    ext <- df[df$year >= SPLICE_YEAR, ]
    if (nrow(ext) > 0) {
      col <- if (sid %in% numeric_cols) sid else numeric_cols[1]
      p <- p %>% add_trace(
        data = ext, x = ~year, y = as.formula(paste0("~`", col, "`")),
        type = "scatter", mode = "lines+markers",
        name = paste0(name, " (Extension)"),
        line = list(color = "#f39c12", width = 2, dash = "dot"),
        marker = list(size = 3)
      )
    }
  } else if (view_mode == "select_individual" && !is.null(selected_subsources)) {
    cols_to_plot <- intersect(selected_subsources, numeric_cols)
    for (i in seq_along(cols_to_plot)) {
      col <- cols_to_plot[i]
      color <- SERIES_COLORS[((i - 1) %% length(SERIES_COLORS)) + 1]
      p <- p %>% add_trace(
        data = df, x = ~year, y = as.formula(paste0("~`", col, "`")),
        type = "scatter", mode = "lines",
        name = col, line = list(color = color, width = 2)
      )
    }
  } else {
    # all_sources / show_components — plot all numeric columns
    unit_groups <- list()
    subsources <- series_entry$subsources %||% list()

    for (i in seq_along(numeric_cols)) {
      col <- numeric_cols[i]
      color <- SERIES_COLORS[((i - 1) %% length(SERIES_COLORS)) + 1]
      ss_meta <- subsources[[gsub("-", "", col)]]
      units_val <- if (!is.null(ss_meta)) safe_str(ss_meta, "units", "default") else "default"
      unit_groups[[col]] <- units_val

      yaxis_str <- "y"
      if (dual_axis && length(unique(unlist(unit_groups))) == 2) {
        unique_units <- unique(unlist(unit_groups))
        if (units_val == unique_units[2]) yaxis_str <- "y2"
      }

      p <- p %>% add_trace(
        data = df, x = ~year, y = as.formula(paste0("~`", col, "`")),
        type = "scatter", mode = "lines",
        name = col, line = list(color = color, width = 2),
        yaxis = yaxis_str
      )
    }
  }

  units_label <- series_entry$units %||% "Value"
  subtitle_text <- paste0(sid, " · ", clean_text(name))
  p <- p %>% apply_chart_layout(name, units_label, subtitle = subtitle_text)

  if (dual_axis) {
    p <- p %>% layout(yaxis2 = list(
      title = "Secondary Axis", overlaying = "y", side = "right",
      gridcolor = CHART_THEME$grid_color,
      tickfont = list(color = CHART_THEME$font_color)
    ))
  }

  p <- p %>% add_recession_bands(year_range)

  show_splice <- any(df$year <= SPLICE_YEAR) && any(df$year > SPLICE_YEAR)
  if (show_splice && view_mode %in% c("all_sources", "final_series")) {
    p <- p %>% add_splice_marker()
  }

  p
}

# ---------------------------------------------------------------------------
# Multi-series overlay chart (for tab-level overview)
# ---------------------------------------------------------------------------
build_multi_series_chart <- function(catalog_entries, year_range) {
  p <- plot_ly()
  for (i in seq_along(catalog_entries)) {
    entry <- catalog_entries[[i]]
    df <- entry$data
    if (is.null(df) || nrow(df) == 0) next

    df <- df[df$year >= year_range[1] & df$year <= year_range[2], ]
    if (nrow(df) == 0) next

    sid <- entry$series_id
    numeric_cols <- setdiff(names(df)[vapply(df, is.numeric, logical(1))], "year")
    col <- if (sid %in% numeric_cols) sid else if (length(numeric_cols) > 0) numeric_cols[1] else next
    color <- SERIES_COLORS[((i - 1) %% length(SERIES_COLORS)) + 1]

    p <- p %>% add_trace(
      data = df, x = ~year, y = as.formula(paste0("~`", col, "`")),
      type = "scatter", mode = "lines",
      name = entry$name %||% sid,
      line = list(color = color, width = 1.5)
    )
  }

  p %>%
    apply_chart_layout("Multi-Series Overlay", "Value") %>%
    add_recession_bands(year_range)
}
