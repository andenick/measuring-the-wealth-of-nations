# ============================================
# chart_builder.R — Chapter 5 Plotly Chart Builders
# ============================================
# Modular chart construction functions for 16 T5xx series.
# These builders are additive — the existing inline chart code
# in server_logic.R remains untouched.
#
# Anu Standard v2.0 — Chart Builder Component
# Created: 2026-02-24 (Session 7 — Gap Remediation G004)
# Depends on: data_loader.R (CH5_SERIES_MAPPING)
# ============================================

library(plotly)

# ============================================
# STANDARD PLOTLY HELPERS
# ============================================
# Note: is_chapter5_series() and is_chapter6_series() are defined in data_loader.R
# (loaded first via source in app.R). Do NOT redefine here to avoid duplicates.

#' Apply consistent Chapter 5 layout to a Plotly object
#' @param p Plotly object
#' @param title Chart title
#' @param y_label Y-axis label
#' @param subtitle Optional subtitle text
#' @return Modified Plotly object
ch5_plotly_layout <- function(p, title, y_label, subtitle = NULL) {
  full_title <- if (!is.null(subtitle)) {
    list(
      text = paste0(title, "<br><sup>", subtitle, "</sup>"),
      font = list(size = 14)
    )
  } else {
    list(text = title, font = list(size = 14))
  }

  p %>%
    layout(
      title = full_title,
      xaxis = list(
        title = "Year",
        dtick = 5,
        gridcolor = "#e0e0e0"
      ),
      yaxis = list(
        title = y_label,
        gridcolor = "#e0e0e0"
      ),
      hovermode = "x unified",
      legend = list(
        orientation = "h",
        yanchor = "bottom",
        y = -0.2,
        xanchor = "center",
        x = 0.5
      ),
      plot_bgcolor = "white",
      paper_bgcolor = "white",
      margin = list(t = 60, b = 80)
    )
}

#' Add NBER recession shading bands to a Plotly chart
#' @param p Plotly object
#' @param year_range Numeric vector c(min_year, max_year)
#' @return Modified Plotly object with recession bands
add_recession_bands <- function(p, year_range) {
  recessions <- data.frame(
    start = c(1948, 1953, 1957, 1960, 1969, 1973, 1980, 1981, 1990, 2001, 2007, 2020),
    end   = c(1949, 1954, 1958, 1961, 1970, 1975, 1980, 1982, 1991, 2001, 2009, 2020)
  )

  # Filter to visible range
  recessions <- recessions[recessions$end >= year_range[1] & recessions$start <= year_range[2], ]

  shapes <- lapply(seq_len(nrow(recessions)), function(i) {
    list(
      type = "rect",
      fillcolor = "rgba(200, 200, 200, 0.2)",
      line = list(color = "transparent"),
      x0 = recessions$start[i],
      x1 = recessions$end[i],
      y0 = 0,
      y1 = 1,
      yref = "paper",
      layer = "below"
    )
  })

  p %>% layout(shapes = shapes)
}

#' Add a vertical marker line at the book/extension boundary
#' @param p Plotly object
#' @param splice_year Year of the transition (default 1989)
#' @return Modified Plotly object
add_extension_marker <- function(p, splice_year = 1989) {
  p %>%
    layout(shapes = list(
      list(
        type = "line",
        x0 = splice_year,
        x1 = splice_year,
        y0 = 0,
        y1 = 1,
        yref = "paper",
        line = list(
          color = "#605ca8",
          dash = "dash",
          width = 1.5
        )
      )
    )) %>%
    add_annotations(
      x = splice_year,
      y = 1,
      yref = "paper",
      text = "Book | Extension",
      showarrow = FALSE,
      font = list(size = 9, color = "#605ca8"),
      yanchor = "bottom"
    )
}

# ── DIV-001 Warning Annotation ──────────────────────────────────────────────
add_div001_warning <- function(p) {
  p %>%
    add_annotations(
      x = 0.02, y = 0.98,
      xref = "paper", yref = "paper",
      text = paste0("<b>DIV-001:</b> Uses total K (BEA Fixed Assets)<br>",
                     "instead of productive K*.<br>",
                     "Level affected; trend direction preserved."),
      showarrow = FALSE,
      font = list(size = 9, color = "#d9534f"),
      bgcolor = "rgba(217, 83, 79, 0.1)",
      bordercolor = "#d9534f",
      borderwidth = 1,
      xanchor = "left",
      yanchor = "top"
    )
}

# ============================================
# SPECIALIZED CHART BUILDERS
# ============================================

#' Build exploitation rate chart (T506: e = S*/V*)
#' @param data Data frame with columns: year, exploitation_rate (or e)
#' @param year_range Numeric vector c(min_year, max_year)
#' @param show_extension Logical — if TRUE, color-codes book vs extension
#' @return Plotly object
build_exploitation_chart <- function(data, year_range, show_extension = TRUE) {
  # Identify the exploitation rate column
  e_col <- if ("exploitation_rate" %in% names(data)) "exploitation_rate"
           else if ("e" %in% names(data)) "e"
           else if ("T506" %in% names(data)) "T506"
           else stop("Cannot find exploitation rate column in data")

  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  if (show_extension && max(df$year) > 1989) {
    # Book period
    book <- df[df$year <= 1989, ]
    ext  <- df[df$year >= 1989, ]

    p <- p %>%
      add_trace(data = book, x = ~year, y = ~get(e_col),
                type = "scatter", mode = "lines+markers",
                name = "Book Period (1948-1989)",
                line = list(color = "#3c8dbc", width = 2),
                marker = list(size = 4, color = "#3c8dbc")) %>%
      add_trace(data = ext, x = ~year, y = ~get(e_col),
                type = "scatter", mode = "lines+markers",
                name = "Extension (1990+)",
                line = list(color = "#f39c12", width = 2, dash = "dot"),
                marker = list(size = 3, color = "#f39c12"))
  } else {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~get(e_col),
                type = "scatter", mode = "lines+markers",
                name = "e = S*/V*",
                line = list(color = "#3c8dbc", width = 2),
                marker = list(size = 4))
  }

  # Add benchmark annotations
  p <- p %>%
    add_annotations(x = 1948, y = 1.70, text = "1.70", showarrow = TRUE,
                    arrowhead = 0, ax = 30, ay = -20, font = list(size = 10)) %>%
    add_annotations(x = 1989, y = 2.44, text = "2.44", showarrow = TRUE,
                    arrowhead = 0, ax = -30, ay = -20, font = list(size = 10))

  p %>%
    ch5_plotly_layout(ifelse(!is.null(get_series_metadata("T506")), get_series_metadata("T506")$name, "Rate of Exploitation (e = S*/V*)"), "Ratio",
                      subtitle = "Shaikh & Tonak Chapter 5, Table 5.7") %>%
    add_recession_bands(year_range)
}

#' Build employment decomposition chart (T511, T515, T516)
#' @param data Data frame with year, Lp, Lu, L_total (or similar) columns
#' @param year_range Numeric vector
#' @param show_decomposition Logical — show stacked Lp + Lu
#' @return Plotly object
build_employment_chart <- function(data, year_range, show_decomposition = TRUE) {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  if (show_decomposition) {
    # Check for Lp and Lu columns
    lp_col <- if ("Lp" %in% names(df)) "Lp"
              else if ("Lp_k" %in% names(df)) "Lp_k"
              else NULL
    lu_col <- if ("Lu" %in% names(df)) "Lu"
              else if ("Lu_k" %in% names(df)) "Lu_k"
              else NULL

    if (!is.null(lp_col) && !is.null(lu_col)) {
      p <- p %>%
        add_trace(data = df, x = ~year, y = ~get(lp_col),
                  type = "scatter", mode = "lines",
                  name = "Productive (Lp)",
                  fill = "tozeroy",
                  fillcolor = "rgba(60, 141, 188, 0.3)",
                  line = list(color = "#3c8dbc", width = 2)) %>%
        add_trace(data = df, x = ~year, y = ~get(lu_col),
                  type = "scatter", mode = "lines",
                  name = "Unproductive (Lu)",
                  fill = "tozeroy",
                  fillcolor = "rgba(243, 156, 18, 0.3)",
                  line = list(color = "#f39c12", width = 2))
    }
  }

  # Add Lp/L ratio on secondary axis if available
  if ("Lp_L_ratio" %in% names(df)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~Lp_L_ratio,
                type = "scatter", mode = "lines",
                name = "Lp/L ratio",
                yaxis = "y2",
                line = list(color = "#dd4b39", width = 2, dash = "dash"))
  }

  p %>%
    ch5_plotly_layout(ifelse(!is.null(get_series_metadata("T515")), "Employment: Productive vs Unproductive", "Employment Decomposition (Productive vs Unproductive)"),
                      "Employment (thousands)",
                      subtitle = "Tables 5.9-5.10, Appendix E.3") %>%
    layout(yaxis2 = list(
      title = "Lp/L Ratio",
      overlaying = "y",
      side = "right",
      range = c(0, 1)
    )) %>%
    add_recession_bands(year_range)
}

#' Build profit rate chart (T513, T514)
#' @param data Data frame with year, r_star_pct, r_star_adj_pct columns
#' @param year_range Numeric vector
#' @param show_capacity_adj Logical — show capacity-adjusted variant
#' @return Plotly object
build_profit_rate_chart <- function(data, year_range, show_capacity_adj = TRUE) {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  # Marxian profit rate
  if ("r_star_pct" %in% names(df)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~r_star_pct,
                type = "scatter", mode = "lines",
                name = "Marxian r*",
                line = list(color = "#3c8dbc", width = 2))
  }

  # Capacity-adjusted
  if (show_capacity_adj && "r_star_adj_pct" %in% names(df)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~r_star_adj_pct,
                type = "scatter", mode = "lines",
                name = "r* (capacity-adjusted)",
                line = list(color = "#00a65a", width = 2, dash = "dot"))
  }

  # Conventional comparison
  if ("r_nipa_pct" %in% names(df)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~r_nipa_pct,
                type = "scatter", mode = "lines",
                name = "NIPA r (conventional)",
                line = list(color = "#f39c12", width = 1.5, dash = "dash"))
  }

  p <- p %>%
    ch5_plotly_layout(ifelse(!is.null(get_series_metadata("T513")), get_series_metadata("T513")$name, "Marxian vs Conventional Profit Rates"),
                      "Percent (%)",
                      subtitle = "Table 5.8 | Note: DIV-001 — uses total K, not productive K*") %>%
    add_recession_bands(year_range)

  add_div001_warning(p)
}

#' Build revenue-side Marxian accounts chart (T501-T505)
#' @param data Data frame with year and component columns
#' @param year_range Numeric vector
#' @return Plotly object
build_revenue_chart <- function(data, year_range) {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  series_cols <- list(
    list(col = "TP_star",    name = "TP* (Total Product)",     color = "#3c8dbc"),
    list(col = "C_star",     name = "C* (Constant Capital)",   color = "#f39c12"),
    list(col = "VA_star",    name = "VA* (Value Added)",       color = "#00a65a"),
    list(col = "V_star",     name = "V* (Variable Capital)",   color = "#dd4b39"),
    list(col = "S_star",     name = "S* (Surplus Value)",      color = "#605ca8")
  )

  for (s in series_cols) {
    if (s$col %in% names(df)) {
      p <- p %>%
        add_trace(data = df, x = ~year, y = ~get(s$col),
                  type = "scatter", mode = "lines",
                  name = s$name,
                  line = list(color = s$color, width = 2))
    }
  }

  p %>%
    ch5_plotly_layout(ifelse(!is.null(get_series_metadata("T501")), "Revenue-Side Marxian Accounts", "Revenue-Side Marxian Accounts (Table 5.5)"),
                      "Billions (current $)",
                      subtitle = "TP*, C*, VA*, V*, S*")
}

# ── Exploitation Composition Chart ───────────────────────────────────────────
build_exploitation_composition_chart <- function(data, year_range, series_id = "T507") {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]
  meta <- get_series_metadata(series_id)
  title <- if (!is.null(meta)) meta$name else series_id

  val_col <- if (series_id %in% names(df)) series_id
             else {
               nums <- setdiff(names(df)[sapply(df, is.numeric)], "year")
               if (length(nums) > 0) nums[1] else stop("No numeric column found")
             }

  p <- plot_ly() %>%
    add_trace(data = df, x = ~year, y = ~get(val_col),
              type = "scatter", mode = "lines+markers",
              name = title,
              line = list(color = "#605ca8", width = 2),
              marker = list(size = 4, color = "#605ca8"))

  p %>%
    ch5_plotly_layout(title, "Ratio",
                      subtitle = paste0("Table 5.7 | ", series_id)) %>%
    add_recession_bands(year_range)
}

# ── Transition Chart Builder ─────────────────────────────────────────────────
build_transition_chart <- function(series_id, book_data, ext_data, splice_year = 1989) {
  meta <- get_series_metadata(series_id)
  title <- if (!is.null(meta)) meta$name else series_id

  # Find the value column (series_id or first numeric after year)
  val_col <- if (series_id %in% names(book_data)) series_id
             else {
               nums <- setdiff(names(book_data)[sapply(book_data, is.numeric)], "year")
               if (length(nums) > 0) nums[1] else stop("No numeric column found")
             }

  ext_val_col <- if (series_id %in% names(ext_data)) series_id
                 else {
                   nums <- setdiff(names(ext_data)[sapply(ext_data, is.numeric)], "year")
                   if (length(nums) > 0) nums[1] else stop("No numeric column in ext_data")
                 }

  p <- plot_ly() %>%
    add_trace(data = book_data, x = ~year, y = ~get(val_col),
              type = "scatter", mode = "lines+markers",
              name = "Book Period",
              line = list(color = "#3c8dbc", width = 2),
              marker = list(size = 4, color = "#3c8dbc")) %>%
    add_trace(data = ext_data, x = ~year, y = ~get(ext_val_col),
              type = "scatter", mode = "lines+markers",
              name = "Extension",
              line = list(color = "#f39c12", width = 2, dash = "dot"),
              marker = list(size = 3, color = "#f39c12")) %>%
    ch5_plotly_layout(
      paste0("Transition: ", title, " (", series_id, ")"),
      "Value",
      subtitle = paste0("Splice year: ", splice_year, " | Method: Direct Level Match")
    ) %>%
    add_extension_marker(splice_year)

  p
}

# ============================================
# CHAPTER 6 — NET SOCIAL WAGE CHART BUILDERS
# ============================================

#' Apply consistent Chapter 6 layout to a Plotly object
#' @param p Plotly object
#' @param title Chart title
#' @param y_label Y-axis label
#' @param subtitle Optional subtitle text
#' @return Modified Plotly object
ch6_plotly_layout <- function(p, title, y_label, subtitle = NULL) {
  full_title <- if (!is.null(subtitle)) {
    list(
      text = paste0(title, "<br><sup>", subtitle, "</sup>"),
      font = list(size = 14)
    )
  } else {
    list(text = title, font = list(size = 14))
  }

  p %>%
    layout(
      title = full_title,
      xaxis = list(
        title = "Year",
        dtick = 5,
        gridcolor = "#e0e0e0"
      ),
      yaxis = list(
        title = y_label,
        gridcolor = "#e0e0e0"
      ),
      hovermode = "x unified",
      legend = list(
        orientation = "h",
        yanchor = "bottom",
        y = -0.2,
        xanchor = "center",
        x = 0.5
      ),
      plot_bgcolor = "white",
      paper_bgcolor = "white",
      margin = list(t = 60, b = 80)
    )
}

#' Build NSW trend chart (T607, or T605/T606 components)
#' @param data Data frame with year and NSW columns
#' @param year_range Numeric vector c(min_year, max_year)
#' @return Plotly object
build_nsw_trend_chart <- function(data, year_range) {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  # NSW line
  nsw_col <- if ("T607_nsw" %in% names(df)) "T607_nsw"
             else if ("nsw" %in% names(df)) "nsw"
             else if ("T607" %in% names(df)) "T607"
             else NULL

  if (!is.null(nsw_col)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~get(nsw_col),
                type = "scatter", mode = "lines+markers",
                name = "NSW",
                line = list(color = "#dd4b39", width = 2.5),
                marker = list(size = 4, color = "#dd4b39"))
  }

  # Benefits line
  ben_col <- if ("T605_benefits" %in% names(df)) "T605_benefits"
             else if ("total_benefits" %in% names(df)) "total_benefits"
             else NULL

  if (!is.null(ben_col)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~get(ben_col),
                type = "scatter", mode = "lines",
                name = "Benefits (B_w)",
                line = list(color = "#00a65a", width = 1.5, dash = "dot"))
  }

  # Govt services line
  gs_col <- if ("T606_govt_services" %in% names(df)) "T606_govt_services"
            else if ("govt_services_workers" %in% names(df)) "govt_services_workers"
            else NULL

  if (!is.null(gs_col)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~get(gs_col),
                type = "scatter", mode = "lines",
                name = "Govt Services (G_w)",
                line = list(color = "#3c8dbc", width = 1.5, dash = "dash"))
  }

  # Add zero reference line
  p <- p %>%
    layout(shapes = list(
      list(type = "line", x0 = year_range[1], x1 = year_range[2],
           y0 = 0, y1 = 0, line = list(color = "black", width = 1, dash = "solid"))
    ))

  p %>%
    ch6_plotly_layout("Net Social Wage (NSW = B_w + G_w - T_w)",
                      "Millions of Current $",
                      subtitle = "Chapter 6 | NSW < 0: workers are net payers to the state") %>%
    add_recession_bands(year_range)
}

#' Build wage comparison chart (T608, T609 ratio views)
#' @param data Data frame with year and ratio columns
#' @param year_range Numeric vector
#' @return Plotly object
build_wage_comparison_chart <- function(data, year_range) {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  # NSW/V* ratio
  nsw_vs_col <- if ("T608_nsw_v_star" %in% names(df)) "T608_nsw_v_star"
                else if ("nsw_v_star_ratio" %in% names(df)) "nsw_v_star_ratio"
                else NULL

  if (!is.null(nsw_vs_col)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~get(nsw_vs_col),
                type = "scatter", mode = "lines+markers",
                name = "NSW/V*",
                line = list(color = "#605ca8", width = 2),
                marker = list(size = 4, color = "#605ca8"))
  }

  # NSW/NI share
  nsw_ni_col <- if ("T609_nsw_ni_share" %in% names(df)) "T609_nsw_ni_share"
                else if ("nsw_ni_share" %in% names(df)) "nsw_ni_share"
                else NULL

  if (!is.null(nsw_ni_col)) {
    p <- p %>%
      add_trace(data = df, x = ~year, y = ~get(nsw_ni_col),
                type = "scatter", mode = "lines+markers",
                name = "NSW/NI",
                line = list(color = "#f39c12", width = 2),
                marker = list(size = 4, color = "#f39c12"))
  }

  # Zero line
  p <- p %>%
    layout(shapes = list(
      list(type = "line", x0 = year_range[1], x1 = year_range[2],
           y0 = 0, y1 = 0, line = list(color = "black", width = 1, dash = "solid"))
    ))

  p %>%
    ch6_plotly_layout("NSW Ratio Measures",
                      "Ratio",
                      subtitle = "Chapter 6, Table 6.4") %>%
    add_recession_bands(year_range)
}

#' Build tax decomposition chart (T601-T604 stacked area)
#' @param data Data frame with year and tax component columns
#' @param year_range Numeric vector
#' @return Plotly object
build_tax_decomposition_chart <- function(data, year_range) {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  tax_cols <- list(
    list(col = "T601_personal_tax", alt = "personal_income_tax_workers",
         name = "Income Tax (IT_w)", color = "#3c8dbc"),
    list(col = "T602_social_insurance", alt = "social_insurance_workers",
         name = "Social Insurance (SI_w)", color = "#f39c12"),
    list(col = "T603_indirect_tax", alt = "sales_excise_tax_workers",
         name = "Sales/Excise + Property (SE_w+PT_w)", color = "#00a65a")
  )

  for (tc in tax_cols) {
    col_name <- if (tc$col %in% names(df)) tc$col
                else if (tc$alt %in% names(df)) tc$alt
                else NULL
    if (!is.null(col_name)) {
      p <- p %>%
        add_trace(data = df, x = ~year, y = ~get(col_name),
                  type = "scatter", mode = "lines",
                  name = tc$name,
                  stackgroup = "one",
                  fillcolor = paste0(tc$color, "80"),
                  line = list(color = tc$color, width = 1))
    }
  }

  p %>%
    ch6_plotly_layout("Tax Decomposition: Workers' Tax Burden",
                      "Millions of Current $",
                      subtitle = "Chapter 6, Table 6.1 | Stacked components of T_w") %>%
    add_recession_bands(year_range)
}

#' Build a Chapter 6 chart for a given series ID
#' @param series_id Character series ID (e.g., "T607")
#' @param data Data frame containing the series data
#' @param year_range Numeric vector c(min_year, max_year)
#' @return Plotly object
build_chapter6_chart <- function(series_id, data, year_range) {
  if (!is_chapter6_series(series_id)) {
    stop(paste("Series", series_id, "is not a Chapter 6 series"))
  }

  chart <- switch(series_id,
    "T601" = build_tax_decomposition_chart(data, year_range),
    "T602" = build_tax_decomposition_chart(data, year_range),
    "T603" = build_tax_decomposition_chart(data, year_range),
    "T604" = build_tax_decomposition_chart(data, year_range),
    "T605" = build_nsw_trend_chart(data, year_range),
    "T606" = build_nsw_trend_chart(data, year_range),
    "T607" = build_nsw_trend_chart(data, year_range),
    "T608" = build_wage_comparison_chart(data, year_range),
    "T609" = build_wage_comparison_chart(data, year_range),
    # Fallback
    {
      meta <- get_series_metadata(series_id)
      title <- if (!is.null(meta)) meta$name else series_id
      numeric_cols <- setdiff(names(data)[vapply(data, is.numeric, logical(1))], "year")
      if (length(numeric_cols) == 0) stop("No numeric columns to plot")
      p <- plot_ly(data = data[data$year >= year_range[1] & data$year <= year_range[2], ],
                   x = ~year, y = ~get(numeric_cols[1]),
                   type = "scatter", mode = "lines+markers",
                   name = numeric_cols[1],
                   line = list(color = "#dd4b39", width = 2))
      p %>% ch6_plotly_layout(title, numeric_cols[1])
    }
  )

  chart
}

# ============================================
# CHAPTER 9 — SUMMARY INDICATORS CHART BUILDERS
# ============================================

#' Apply consistent Chapter 9 layout to a Plotly object
#' @param p Plotly object
#' @param title Chart title
#' @param y_label Y-axis label
#' @param subtitle Optional subtitle text
#' @return Modified Plotly object
ch9_plotly_layout <- function(p, title, y_label, subtitle = NULL) {
  full_title <- if (!is.null(subtitle)) {
    list(
      text = paste0(title, "<br><sup>", subtitle, "</sup>"),
      font = list(size = 14)
    )
  } else {
    list(text = title, font = list(size = 14))
  }

  p %>%
    layout(
      title = full_title,
      xaxis = list(
        title = "Year",
        dtick = 5,
        gridcolor = "#e0e0e0"
      ),
      yaxis = list(
        title = y_label,
        gridcolor = "#e0e0e0"
      ),
      hovermode = "x unified",
      legend = list(
        orientation = "h",
        yanchor = "bottom",
        y = -0.2,
        xanchor = "center",
        x = 0.5
      ),
      plot_bgcolor = "white",
      paper_bgcolor = "white",
      margin = list(t = 60, b = 80)
    )
}

#' Build summary indicators chart (T901: multi-line key indicators)
#' @param data Data frame with year and indicator columns
#' @param year_range Numeric vector c(min_year, max_year)
#' @return Plotly object
build_summary_indicators_chart <- function(data, year_range) {
  df <- data[data$year >= year_range[1] & data$year <= year_range[2], ]

  p <- plot_ly()

  indicators <- list(
    list(col = "T506_exploitation_rate", name = "e = S*/V*", color = "#3c8dbc"),
    list(col = "T511_productive_labor_share", name = "Lp/L", color = "#f39c12"),
    list(col = "T512_productive_wage_share", name = "V*/W", color = "#00a65a"),
    list(col = "T608_nsw_v_star", name = "NSW/V*", color = "#dd4b39")
  )

  for (ind in indicators) {
    if (ind$col %in% names(df)) {
      vals <- as.numeric(df[[ind$col]])
      if (any(!is.na(vals))) {
        p <- p %>%
          add_trace(x = df$year, y = vals,
                    type = "scatter", mode = "lines+markers",
                    name = ind$name,
                    line = list(color = ind$color, width = 2),
                    marker = list(size = 3, color = ind$color))
      }
    }
  }

  p %>%
    ch9_plotly_layout("Key Marxian Indicators (Summary)",
                      "Ratio / Share",
                      subtitle = "Chapter 9, Table 9.1 | Derived from Ch 5 + Ch 6") %>%
    add_recession_bands(year_range)
}

#' Build a Chapter 9 chart for a given series ID
#' @param series_id Character series ID (e.g., "T901")
#' @param data Data frame containing the series data
#' @param year_range Numeric vector c(min_year, max_year)
#' @return Plotly object
build_chapter9_chart <- function(series_id, data, year_range) {
  if (!is_chapter9_series(series_id)) {
    stop(paste("Series", series_id, "is not a Chapter 9 series"))
  }

  chart <- switch(series_id,
    "T901" = build_summary_indicators_chart(data, year_range),
    # Fallback
    {
      p <- plot_ly(data = data[data$year >= year_range[1] & data$year <= year_range[2], ],
                   x = ~year, type = "scatter", mode = "lines")
      p %>% ch9_plotly_layout(series_id, "Value")
    }
  )

  chart
}

# ============================================
# CHAPTER 5 DISPATCHER
# ============================================

#' Build a Chapter 5 chart for a given series ID
#' @param series_id Character series ID (e.g., "T506")
#' @param data Data frame containing the series data
#' @param year_range Numeric vector c(min_year, max_year)
#' @return Plotly object
build_chapter5_chart <- function(series_id, data, year_range) {
  if (!is_chapter5_series(series_id)) {
    stop(paste("Series", series_id, "is not a Chapter 5 series"))
  }

  # Route to specialized builders
  chart <- switch(series_id,
    "T506" = build_exploitation_chart(data, year_range),
    "T511" = build_employment_chart(data, year_range),
    "T515" = build_employment_chart(data, year_range),
    "T516" = build_employment_chart(data, year_range),
    "T513" = build_profit_rate_chart(data, year_range),
    "T514" = build_profit_rate_chart(data, year_range),
    "T501" = build_revenue_chart(data, year_range),
    "T502" = build_revenue_chart(data, year_range),
    "T503" = build_revenue_chart(data, year_range),
    "T504" = build_revenue_chart(data, year_range),
    "T505" = build_revenue_chart(data, year_range),
    "T507" = build_exploitation_composition_chart(data, year_range, "T507"),
    "T510" = build_exploitation_composition_chart(data, year_range, "T510"),
    "T508" = build_revenue_chart(data, year_range),
    "T509" = build_revenue_chart(data, year_range),
    "T512" = build_exploitation_chart(data, year_range),
    # Fallback: generic time series plot
    {
      meta <- get_series_metadata(series_id)
      title <- if (!is.null(meta)) meta$name else series_id

      # Try to find a plottable column
      numeric_cols <- setdiff(names(data)[vapply(data, is.numeric, logical(1))], "year")
      if (length(numeric_cols) == 0) stop("No numeric columns to plot")

      p <- plot_ly(data = data[data$year >= year_range[1] & data$year <= year_range[2], ],
                   x = ~year, y = ~get(numeric_cols[1]),
                   type = "scatter", mode = "lines+markers",
                   name = numeric_cols[1],
                   line = list(color = "#3c8dbc", width = 2))

      p %>% ch5_plotly_layout(title, numeric_cols[1])
    }
  )

  chart
}
