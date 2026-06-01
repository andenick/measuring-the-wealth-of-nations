# =============================================================================
# RMWND Shiny — Interactive Data Explorer
# =============================================================================
# Shaikh & Tonak (1994) — Measuring the Wealth of Nations Replication
# R Shiny + Plotly with light/dark theme toggle.
# =============================================================================

source("global.R")

# =============================================================================
# UI
# =============================================================================

ui <- dashboardPage(
  skin = "blue",

  dashboardHeader(
    title = span(icon("chart-line"), "RMWND Explorer"),
    tags$li(
      class = "dropdown",
      tags$a(
        id = "theme_toggle", href = "#",
        onclick = "toggleTheme(); return false;",
        icon("moon")
      )
    )
  ),

  dashboardSidebar(
    width = 320,
    sidebarMenu(
      id = "main_tabs",

      tags$div(
        style = "padding: 15px; border-bottom: 1px solid var(--border-subtle);",
        tags$h4(
          style = "color: var(--text-primary); margin: 0;",
          icon("book-open"),
          "RMWND Data Explorer"
        ),
        tags$p(
          style = "color: var(--text-muted); font-size: 12px; margin: 5px 0 0 0;",
          "Shaikh & Tonak (1994)"
        )
      ),

      # Tab selector
      selectInput("active_tab", "Chapter Tab:",
                  choices = TAB_CHOICES, selected = DEFAULT_TAB),

      # Series selector (dynamic)
      uiOutput("series_selector"),

      # Year range slider
      sliderInput("year_range", "Year Range:",
                  min = YEAR_RANGE[1], max = YEAR_RANGE[2],
                  value = DEFAULT_YEAR_RANGE, step = 1, sep = ""),

      # View mode radio buttons
      radioButtons("view_mode", "View Mode:",
                   choices = c(
                     "All Sources" = "all_sources",
                     "Final Series" = "final_series",
                     "Author Construction" = "author_construction",
                     "Final Extension" = "final_extension",
                     "Select Individual" = "select_individual",
                     "Show Components" = "show_components"
                   ),
                   selected = "all_sources"),

      # Subsource multi-select (conditional)
      uiOutput("subsource_selector"),

      # Dual Y-axis toggle
      uiOutput("dual_axis_toggle"),

      tags$hr(style = "margin: 10px 0; border-color: var(--border-subtle);"),

      # Validation badge
      tags$div(
        style = "padding: 10px 15px; color: var(--text-muted); font-size: 12px;",
        uiOutput("sidebar_stats")
      )
    )
  ),

  dashboardBody(
    tags$head(
      tags$link(rel = "stylesheet", type = "text/css", href = "theme.css"),
      tags$script(src = "theme-toggle.js"),
      tags$link(rel = "preconnect", href = "https://fonts.googleapis.com"),
      tags$link(rel = "stylesheet",
                href = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap")
    ),

    fluidRow(
      # Series header
      column(12, uiOutput("series_header")),

      # Main chart
      column(12,
        box(width = 12, solidHeader = TRUE, class = "chart-container",
            plotlyOutput("main_chart", height = "480px"))
      ),

      # Detail tabs
      column(12,
        box(width = 12,
          tabsetPanel(
            id = "detail_tabs",

            tabPanel(
              title = span(icon("book"), "Methodology"),
              value = "methodology",
              uiOutput("methodology_panel")
            ),

            tabPanel(
              title = span(icon("quote-left"), "Quotes"),
              value = "quotes",
              uiOutput("quotes_panel")
            ),

            tabPanel(
              title = span(icon("chart-line"), "Extension"),
              value = "extension",
              uiOutput("extension_panel")
            ),

            tabPanel(
              title = span(icon("table"), "Data"),
              value = "data",
              DT::dataTableOutput("data_table"),
              downloadButton("download_csv", "Download CSV",
                             class = "btn-sm btn-info",
                             style = "margin-top: 10px;")
            ),

            tabPanel(
              title = span(icon("list-alt"), "Series Browser"),
              value = "browser",
              uiOutput("series_browser_panel")
            )
          )
        )
      )
    )
  )
)

# =============================================================================
# SERVER
# =============================================================================

server <- function(input, output, session) {
  log_section("Shiny Server Starting")

  # ---------------------------------------------------------------------------
  # Theme observer
  # ---------------------------------------------------------------------------
  observeEvent(input$app_theme, {
    mode <- input$app_theme
    if (!is.null(mode) && mode %in% c("light", "dark")) {
      set_chart_theme(mode)
    }
  })

  # ---------------------------------------------------------------------------
  # Reactive: current tab series IDs
  # ---------------------------------------------------------------------------
  tab_series_ids <- reactive({
    tab <- input$active_tab %||% DEFAULT_TAB
    tab_cfg <- TABS[[tab]]
    if (is.null(tab_cfg)) return(character(0))
    unlist(tab_cfg$series_ids)
  })

  # Reactive: current tab catalog entries
  tab_catalog <- reactive({
    ids <- tab_series_ids()
    Filter(function(s) s$series_id %in% ids, SERIES_CATALOG)
  })

  # Reactive: current selected series entry
  current_entry <- reactive({
    req(input$series_id)
    SERIES_CATALOG[[input$series_id]]
  })

  # ---------------------------------------------------------------------------
  # Dynamic UI: series selector
  # ---------------------------------------------------------------------------
  output$series_selector <- renderUI({
    entries <- tab_catalog()
    if (length(entries) == 0) {
      return(tags$p(style = "color: var(--text-muted); padding: 10px;",
                    "No series in this tab"))
    }
    choices <- setNames(
      vapply(entries, function(e) e$series_id, character(1)),
      vapply(entries, function(e) {
        paste0(e$series_id, ": ", substr(e$name, 1, 40),
               if (nchar(e$name) > 40) "..." else "")
      }, character(1))
    )
    selectInput("series_id", "Select Series:",
                choices = choices, selected = choices[1])
  })

  # Dynamic UI: subsource selector (only for select_individual)
  output$subsource_selector <- renderUI({
    req(input$view_mode)
    if (input$view_mode != "select_individual") return(NULL)
    entry <- current_entry()
    if (is.null(entry) || is.null(entry$data)) return(NULL)

    numeric_cols <- setdiff(
      names(entry$data)[vapply(entry$data, is.numeric, logical(1))], "year"
    )
    if (length(numeric_cols) == 0) return(NULL)

    selectizeInput("selected_subsources", "Select Subsources:",
                   choices = numeric_cols, selected = numeric_cols[1],
                   multiple = TRUE,
                   options = list(plugins = list("remove_button")))
  })

  # Dynamic UI: dual axis toggle
  output$dual_axis_toggle <- renderUI({
    entry <- current_entry()
    if (is.null(entry)) return(NULL)
    subsources <- entry$subsources %||% list()
    if (length(subsources) == 0) return(NULL)

    unit_groups <- unique(na.omit(vapply(subsources,
      function(s) safe_str(s, "units", ""), character(1))))
    unit_groups <- unit_groups[nzchar(unit_groups)]
    if (length(unit_groups) != 2) return(NULL)

    tags$div(
      style = "margin-top: 8px; padding: 0 15px;",
      checkboxInput("dual_axis", "Dual Y-Axis", value = FALSE),
      tags$small(style = "color: var(--text-muted); font-size: 11px;",
                 sprintf("Left: %s | Right: %s", unit_groups[1], unit_groups[2]))
    )
  })

  # Sidebar stats
  output$sidebar_stats <- renderUI({
    loaded <- sum(vapply(SERIES_CATALOG, function(s) isTRUE(s$has_data), logical(1)))
    total <- length(SERIES_CATALOG)
    tab_count <- length(tab_catalog())

    tags$div(
      tags$div(
        style = paste0("font-size: 13px; font-weight: 600; color: ",
                       if (loaded >= 60) "var(--success)" else "var(--warning)", ";"),
        paste0(loaded, " / ", total, " series loaded")
      ),
      tags$p(style = "margin: 4px 0 0 0;",
             paste0("Tab series: ", tab_count))
    )
  })

  # ---------------------------------------------------------------------------
  # Series header
  # ---------------------------------------------------------------------------
  output$series_header <- renderUI({
    entry <- current_entry()
    if (is.null(entry)) {
      return(tags$div(class = "figure-header",
                      tags$h3(class = "figure-title", "Select a series")))
    }

    tags$div(
      class = "figure-header",
      tags$div(class = "figure-chapter",
               paste0("Chapter ", entry$chapter %||% "?", " · ",
                      input$active_tab %||% "")),
      tags$h3(class = "figure-title",
              entry$series_id, ": ", clean_text(entry$name),
              status_badge(entry$extension_status)),
      tags$div(
        style = "color: var(--text-muted); font-size: 13px;",
        if (!is.null(entry$time_period_start)) {
          tagList(icon("calendar-alt"), " ",
                  format_year_range(entry$time_period_start, entry$time_period_end))
        },
        if (length(entry$figure_ids) > 0) {
          paste0(" | Figures: ", paste(unlist(entry$figure_ids), collapse = ", "))
        }
      )
    )
  })

  # ---------------------------------------------------------------------------
  # Main chart
  # ---------------------------------------------------------------------------
  output$main_chart <- renderPlotly({
    entry <- current_entry()
    if (is.null(entry)) {
      return(plotly_empty() %>% layout(title = "Select a series"))
    }

    view_mode <- input$view_mode %||% "all_sources"
    yr <- input$year_range %||% DEFAULT_YEAR_RANGE
    selected_subs <- input$selected_subsources %||% NULL
    use_dual <- isTRUE(input$dual_axis)

    tryCatch(
      build_series_chart(entry, view_mode, yr, selected_subs, use_dual),
      error = function(e) {
        log_error("Chart error: %s", e$message)
        plotly_empty() %>% layout(title = paste("Error:", e$message))
      }
    )
  })

  # ---------------------------------------------------------------------------
  # Methodology panel
  # ---------------------------------------------------------------------------
  output$methodology_panel <- renderUI({
    entry <- current_entry()
    if (is.null(entry)) return(tags$p("Select a series"))

    tagList(
      section_header("Series Information", "info"),
      methodology_item("Series ID", entry$series_id),
      methodology_item("Units", entry$units),
      methodology_item("Time Period",
                       format_year_range(entry$time_period_start, entry$time_period_end)),
      methodology_item("Extension Status", entry$extension_status),
      methodology_item("Subsources", entry$subsource_count),

      if (nchar(entry$construction_formula) > 0) {
        tagList(
          section_header("Construction Formula", "warning"),
          tags$div(
            style = "background: var(--bg-panel); padding: 15px; border-radius: 5px;
                     border-left: 3px solid var(--warning); font-family: 'Courier New', monospace;
                     color: var(--text-primary);",
            entry$construction_formula
          )
        )
      },

      if (nchar(entry$methodology_note) > 0) {
        tagList(
          section_header("Methodology Note", "warning"),
          tags$div(class = "info-panel",
                   tags$p(style = "color: var(--text-secondary);",
                          entry$methodology_note))
        )
      },

      if (length(entry$api_sources) > 0) {
        tagList(
          section_header("API Sources", "info"),
          tags$ul(lapply(entry$api_sources, function(api) {
            tags$li(style = "color: var(--accent);", as.character(api))
          }))
        )
      },

      if (entry$subsource_count > 0 && length(entry$subsources) > 0) {
        tagList(
          section_header("Subsource Details", "warning"),
          tags$div(
            style = "max-height: 300px; overflow-y: auto;",
            lapply(names(entry$subsources), function(ss_id) {
              ss <- entry$subsources[[ss_id]]
              if (!is.list(ss)) return(NULL)
              tags$div(
                class = "subsource-card",
                tags$div(style = "font-weight: bold; color: var(--highlight);",
                         ss_id, ": ", safe_str(ss, "source_name", "Unknown")),
                tags$div(
                  style = "display: flex; flex-wrap: wrap; gap: 10px; margin-top: 5px;",
                  if (!is.null(safe_field(ss, "time_period_start"))) {
                    tags$span(style = "color: var(--accent); font-size: 0.9em;",
                              paste0("Period: ", safe_field(ss, "time_period_start"),
                                     "-", safe_field(ss, "time_period_end")))
                  },
                  if (!is.null(safe_field(ss, "api"))) {
                    tags$span(style = "color: var(--success); font-size: 0.9em;",
                              paste0("API: ", safe_str(ss, "api")))
                  }
                )
              )
            })
          )
        )
      }
    )
  })

  # ---------------------------------------------------------------------------
  # Quotes panel
  # ---------------------------------------------------------------------------
  output$quotes_panel <- renderUI({
    entry <- current_entry()
    if (is.null(entry)) return(tags$p("Select a series"))

    quote_text <- entry$shaikh_quote %||% ""
    quote_page <- entry$shaikh_quote_page %||% ""

    tagList(
      if (nchar(quote_text) > 5 && quote_text != "N/A - See related figures") {
        tagList(
          section_header("Shaikh's Quote", "primary"),
          tags$div(
            class = "book-quote",
            tags$div(
              style = "font-style: italic; color: var(--text-primary); line-height: 1.6;",
              paste0('"', quote_text, '"')
            ),
            if (nchar(quote_page) > 0) {
              tags$div(
                style = "color: var(--text-muted); font-size: 0.9em; margin-top: 10px;",
                paste0("— Shaikh & Tonak (1994), p. ", quote_page)
              )
            }
          )
        )
      } else {
        tags$p(style = "color: var(--text-muted);",
               "No quote available for this series.")
      }
    )
  })

  # ---------------------------------------------------------------------------
  # Extension panel
  # ---------------------------------------------------------------------------
  output$extension_panel <- renderUI({
    entry <- current_entry()
    if (is.null(entry)) return(tags$p("Select a series"))

    ext_status <- entry$extension_status %||% "conceptual"

    tagList(
      section_header("Extension Status", "info"),
      tags$div(
        class = "info-panel",
        tags$div(
          style = "display: flex; justify-content: space-between; align-items: center;",
          tags$span(class = "info-label", "Status"),
          status_badge(ext_status)
        ),
        tags$div(
          style = "margin-top: 10px;",
          if (ext_status == "extended_2025") {
            tags$p(style = "color: var(--success);",
                   icon("check-circle"), " Extended through 2025")
          } else if (ext_status == "calculated") {
            tags$p(style = "color: var(--warning);",
                   icon("calculator"), " Calculated — no extension needed")
          } else {
            tags$p(style = "color: var(--text-muted);",
                   "Extension methodology pending review")
          }
        )
      ),

      if (length(entry$api_sources) > 0) {
        tagList(
          section_header("Extension API Sources", "info"),
          tags$ul(lapply(entry$api_sources, function(api) {
            tags$li(style = "color: var(--accent);", as.character(api))
          }))
        )
      }
    )
  })

  # ---------------------------------------------------------------------------
  # Data table
  # ---------------------------------------------------------------------------
  output$data_table <- DT::renderDataTable({
    entry <- current_entry()
    if (is.null(entry) || is.null(entry$data)) return(NULL)

    yr <- input$year_range %||% DEFAULT_YEAR_RANGE
    df <- entry$data[entry$data$year >= yr[1] & entry$data$year <= yr[2], ]

    datatable(df,
              options = list(pageLength = 20, scrollX = TRUE,
                             dom = "frtip", lengthMenu = c(10, 20, 50, 100)),
              style = "bootstrap4", class = "compact stripe hover")
  })

  output$download_csv <- downloadHandler(
    filename = function() {
      sid <- input$series_id %||% "data"
      paste0(sid, "_", Sys.Date(), ".csv")
    },
    content = function(file) {
      entry <- current_entry()
      if (!is.null(entry) && !is.null(entry$data)) {
        yr <- input$year_range %||% DEFAULT_YEAR_RANGE
        df <- entry$data[entry$data$year >= yr[1] & entry$data$year <= yr[2], ]
        write_csv(df, file)
      } else {
        write_csv(data.frame(Message = "No data available"), file)
      }
    }
  )

  # ---------------------------------------------------------------------------
  # Series browser panel
  # ---------------------------------------------------------------------------
  output$series_browser_panel <- renderUI({
    entries <- tab_catalog()
    if (length(entries) == 0) return(tags$p("No series in this tab"))

    tab <- input$active_tab %||% DEFAULT_TAB
    tab_label <- TABS[[tab]]$label %||% tab

    tagList(
      section_header(paste0("Series — ", tab_label), "primary"),
      tags$div(
        style = "font-size: 0.85em; color: var(--text-muted); margin-bottom: 15px;",
        paste0("Showing ", length(entries), " series in tab. ",
               "Total catalog: ", length(SERIES_CATALOG))
      ),
      tags$div(
        style = "max-height: 500px; overflow-y: auto;",
        lapply(entries, function(entry) {
          status_color <- switch(entry$extension_status,
            "extended_2025" = "#28a745",
            "calculated"    = "#ffc107",
            "conceptual"    = "#6c757d",
            "#888888"
          )
          tags$div(
            class = "series-card",
            style = "background: var(--bg-panel); border-radius: 8px; padding: 12px;
                     margin-bottom: 10px; border-left: 4px solid var(--accent);",
            tags$div(
              style = "display: flex; justify-content: space-between; align-items: center;",
              tags$div(
                tags$span(style = "color: var(--accent); font-weight: bold; font-size: 1.1em;",
                          entry$series_id),
                tags$span(style = "color: var(--text-secondary); margin-left: 10px;",
                          entry$name)
              ),
              tags$span(
                style = paste0("background: ", status_color,
                               "; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em;"),
                entry$extension_status
              )
            ),
            if (!is.null(entry$time_period_start)) {
              tags$div(style = "color: var(--accent); font-size: 0.9em; margin-top: 5px;",
                       format_year_range(entry$time_period_start, entry$time_period_end))
            },
            tags$div(
              style = "display: flex; gap: 15px; margin-top: 5px;",
              tags$span(style = "color: var(--text-muted); font-size: 0.85em;",
                        paste0("Subsources: ", entry$subsource_count)),
              if (isTRUE(entry$has_data)) {
                tags$span(style = "color: var(--success); font-size: 0.85em;",
                          icon("check"), " Data loaded")
              } else {
                tags$span(style = "color: var(--danger); font-size: 0.85em;",
                          icon("times"), " No data")
              }
            )
          )
        })
      ),

      section_header("Catalog Statistics", "info"),
      tags$div(
        class = "info-panel",
        style = "display: flex; flex-wrap: wrap; gap: 30px;",
        tags$div(
          tags$div(style = "color: var(--text-muted); font-size: 0.85em;", "Total Series"),
          tags$div(style = "color: var(--accent); font-size: 1.5em; font-weight: bold;",
                   length(SERIES_CATALOG))
        ),
        tags$div(
          tags$div(style = "color: var(--text-muted); font-size: 0.85em;", "With Data"),
          tags$div(style = "color: var(--success); font-size: 1.5em; font-weight: bold;",
                   sum(vapply(SERIES_CATALOG, function(s) isTRUE(s$has_data), logical(1))))
        ),
        tags$div(
          tags$div(style = "color: var(--text-muted); font-size: 0.85em;", "Extended"),
          tags$div(style = "color: var(--info); font-size: 1.5em; font-weight: bold;",
                   sum(vapply(SERIES_CATALOG,
                     function(s) s$extension_status == "extended_2025", logical(1))))
        )
      )
    )
  })
}

# =============================================================================
# Run
# =============================================================================
shinyApp(ui = ui, server = server)
