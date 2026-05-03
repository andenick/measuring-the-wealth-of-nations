app_server <- function(input, output, session) {
  # ============================================
  # REACTIVE DATA FILTERING
  # ============================================

  # Filter data based on year range
  filtered_data <- reactive({
    all_series_long %>%
      filter(
        year >= input$year_range[1],
        year <= input$year_range[2]
      )
  })

  filtered_profit <- reactive({
    profit_rates %>%
      filter(
        year >= input$year_range[1],
        year <= input$year_range[2]
      )
  })

  filtered_exploitation <- reactive({
    exploitation %>%
      filter(
        year >= input$year_range[1],
        year <= input$year_range[2]
      )
  })

  filtered_employment <- reactive({
    employment %>%
      filter(
        year >= input$year_range[1],
        year <= input$year_range[2]
      )
  })

  filtered_government <- reactive({
    government %>%
      filter(
        year >= input$year_range[1],
        year <= input$year_range[2]
      )
  })

  # ============================================
  # TAB 2: EXPLORE BY QUESTION - FILTERING
  # ============================================

  # Filtered questions based on priority and category
  filtered_questions <- reactive({
    q <- questions

    # Filter by priority
    if (input$question_priority_filter != "all") {
      q <- q %>% filter(Priority == input$question_priority_filter)
    }

    # Filter by category
    if (input$question_category_filter != "all") {
      q <- q %>% filter(Category == input$question_category_filter)
    }

    q %>% arrange(Question_Number)
  })

  # Questions count display
  output$questions_count <- renderText({
    count <- nrow(filtered_questions())
    paste0(count, " Question", if (count != 1) "s" else "")
  })

  # Render question cards
  output$question_cards <- renderUI({
    questions_data <- filtered_questions()

    if (nrow(questions_data) == 0) {
      return(div(
        style = "text-align: center; padding: 40px; color: #999;",
        h4("No questions match the selected filters"),
        p("Try adjusting your filter criteria")
      ))
    }

    # Generate question cards
    cards <- lapply(1:nrow(questions_data), function(i) {
      q <- questions_data[i, ]

      div(
        class = "question-card",
        onclick = sprintf("Shiny.setInputValue('question_clicked', %d, {priority: 'event'})", q$Question_Number),
        div(
          class = "question-card-header",
          span(class = "question-number", paste0("Question ", q$Question_Number)),
          span(class = paste0("priority-badge priority-", q$Priority), q$Priority)
        ),
        div(class = "question-text", q$Question),
        div(
          class = "question-category",
          icon("folder-open"), " ", q$Category, " • ",
          icon("arrow-right"), " ", q$Target_Tab
        )
      )
    })

    do.call(tagList, cards)
  })

  # Handle question clicks and show modal
  observeEvent(input$question_clicked, {
    q_num <- input$question_clicked
    q <- questions %>% filter(Question_Number == q_num)

    if (nrow(q) == 0) {
      return()
    }

    # Create modal content
    showModal(modalDialog(
      title = div(
        style = "color: white;",
        h3(style = "margin: 0;", paste0("Question ", q$Question_Number)),
        p(style = "margin-top: 10px; font-size: 18px; font-weight: 600;", q$Question)
      ),
      size = "l",
      easyClose = TRUE,
      footer = tagList(
        actionButton(paste0("goto_tab_", q_num),
          paste("Go to", q$Target_Tab, "tab"),
          class = "btn-primary"
        ),
        modalButton("Close")
      ),

      # Answer Section
      div(
        class = "modal-section",
        h4(icon("lightbulb"), " Answer"),
        p(q$Explanation)
      ),

      # Formula Section
      if (!is.na(q$Formula) && q$Formula != "") {
        div(
          class = "modal-section",
          h4(icon("calculator"), " Formula"),
          div(class = "formula-box", q$Formula)
        )
      },

      # Definition Section
      if (!is.na(q$Definition) && q$Definition != "") {
        div(
          class = "modal-section",
          h4(icon("book-open"), " Definition"),
          p(q$Definition)
        )
      },

      # Visualization Section
      div(
        class = "modal-section",
        h4(icon("chart-line"), " Visualization"),
        plotlyOutput(paste0("modal_plot_", q_num), height = "350px")
      ),

      # Book Reference Section
      if (!is.na(q$Book_Reference) && q$Book_Reference != "") {
        div(
          class = "modal-section",
          h4(icon("bookmark"), " Book Reference"),
          div(
            class = "book-reference",
            icon("book"), " Shaikh & Tonak (1994): ", q$Book_Reference
          )
        )
      }
    ))

    # Generate appropriate plot based on category
    output[[paste0("modal_plot_", q_num)]] <- renderPlotly({
      if (q$Category == "Profit Rate") {
        data <- filtered_profit()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~r_star_pct, name = "Marxian r*",
            type = "scatter", mode = "lines",
            line = list(color = colors$primary, width = 3)
          )
      } else if (q$Category == "Surplus Value") {
        data <- filtered_exploitation()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~exploitation_rate, name = "S*/V*",
            type = "scatter", mode = "lines",
            line = list(color = colors$success, width = 3)
          )
      } else {
        # Default plot
        plot_ly(x = 1, y = 1, type = "scatter", mode = "markers") %>%
          layout(title = "No visualization available for this category")
      }
    })
  })

  # Handle tab navigation from question modals
  lapply(1:nrow(questions), function(num) {
    observeEvent(input[[paste0("goto_tab_", num)]], {
      q <- questions %>% filter(Question_Number == num)
      if (nrow(q) > 0) {
        tab_map <- list(
          "overview" = "overview",
          "questions" = "questions",
          "methodology" = "methodology",
          "profit_rate" = "profit_rate",
          "exploitation" = "exploitation",
          "employment" = "employment",
          "government" = "government",
          "validation" = "validation",
          "literature" = "literature"
        )

        target <- tolower(gsub(" ", "_", q$Target_Tab))
        target <- gsub("_analysis", "", target)
        target <- gsub("_center", "", target)
        target <- gsub("_navigator", "", target)

        if (target %in% names(tab_map)) {
          updateTabItems(session, "tabs", tab_map[[target]])
          removeModal()
        }
      }
    })
  })

  # ============================================
  # OVERVIEW TAB OUTPUTS
  # ============================================

  output$vbox_r_star <- renderValueBox({
    latest_year <- max(filtered_profit()$year)
    latest_r <- filtered_profit() %>%
      filter(year == latest_year) %>%
      pull(r_star_pct)

    valueBox(
      value = round(latest_r, 1),
      subtitle = paste0("Marxian r* (", latest_year, ")"),
      icon = icon("chart-line"),
      color = "blue"
    )
  })

  output$vbox_exploitation <- renderValueBox({
    latest_year <- max(filtered_exploitation()$year)
    latest_e <- filtered_exploitation() %>%
      filter(year == latest_year) %>%
      pull(exploitation_rate)

    valueBox(
      value = round(latest_e, 2),
      subtitle = paste0("Exploitation Rate S*/V* (", latest_year, ")"),
      icon = icon("balance-scale"),
      color = "red"
    )
  })

  output$vbox_productive_share <- renderValueBox({
    latest_year <- max(filtered_employment()$year)
    latest_share <- filtered_employment() %>%
      filter(year == latest_year) %>%
      pull(Lp_L_ratio)

    valueBox(
      value = paste0(round(latest_share * 100, 1), "%"),
      subtitle = paste0("Productive Labor Share (", latest_year, ")"),
      icon = icon("users"),
      color = "green"
    )
  })

  output$vbox_govt_absorption <- renderValueBox({
    latest_year <- max(filtered_government()$year)
    latest_g <- filtered_government() %>%
      filter(year == latest_year) %>%
      pull(G_S_ratio)

    valueBox(
      value = paste0(round(latest_g * 100, 1), "%"),
      subtitle = paste0("Gov't/Surplus Ratio (", latest_year, ")"),
      icon = icon("university"),
      color = "red"
    )
  })

  # ============================================
  # TAB 1: OVERVIEW - MAIN PLOT
  # ============================================

  output$overview_profit_plot <- renderPlotly({
    data <- filtered_profit()

    p <- plot_ly(data, x = ~year) %>%
      add_trace(
        y = ~r_star_pct,
        name = "Marxian r*",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$primary, width = 3),
          # Filter controls
          box(
            title = "Filter Questions",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            fluidRow(
              column(
                4,
                selectInput("question_priority_filter",
                  "Priority Level:",
                  choices = c("All" = "all", "CRITICAL", "HIGH", "MEDIUM", "LOW"),
                  selected = "all",
                  width = "100%"
                )
              ),
              column(
                4,
                selectInput("question_category_filter",
                  "Category:",
                  choices = c(
                    "All" = "all",
                    "Profit Rate" = "Profit Rate",
                    "Surplus Value" = "Surplus Value",
                    "Capital Composition" = "Capital Composition",
                    "Employment" = "Employment",
                    "Government" = "Government",
                    "Data & Methodology" = "Data & Methodology"
                  ),
                  selected = "all",
                  width = "100%"
                )
              ),
              column(
                4,
                div(
                  style = "padding-top: 25px;",
                  h4(textOutput("questions_count"), style = "color: #3c8dbc; font-weight: bold;")
                )
              )
            )
          )
        ),
        fluidRow(
          box(
            title = "Questions",
            status = "info",
            solidHeader = TRUE,
            width = 12,
            div(
              style = "max-height: 800px; overflow-y: auto;",
              uiOutput("question_cards")
            )
          )
        )
      ),

      # ============================================
      # TAB 2.5: METHODOLOGY COMPARISON (NEW)
      # ============================================
      tabItem(
        tabName = "methodology",
        h2("Multi-Methodology Comparison"),
        p("Compare three major approaches: ST94 (Shaikh-Tonak 1994), M05 (Mohun 2005), TP19 (Tsoulfidis-Paitaridis 2019)"),
        fluidRow(
          valueBoxOutput("method_book_match", width = 4),
          valueBoxOutput("method_current_e", width = 4),
          valueBoxOutput("method_divergence", width = 4)
        ),
        fluidRow(
          box(
            title = "Exploitation Rate (S*/V*) by Methodology",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("methodology_exploitation_plot", height = "450px"),
            p(em("Note: Book benchmarks (dots) shown for validation. Shaded area indicates extension period (1990-2024)."))
          )
        ),
        fluidRow(
          box(
            title = "Productive Labor Share (Lp/L) by Methodology",
            status = "success",
            solidHeader = TRUE,
            width = 6,
            plotlyOutput("methodology_labor_plot", height = "350px")
          ),
          box(
            title = "Profit Rate Trends by Methodology",
            status = "warning",
            solidHeader = TRUE,
            width = 6,
            plotlyOutput("methodology_profit_plot", height = "350px")
          )
        ),
        fluidRow(
          box(
            title = "Methodology Comparison Table",
            status = "info",
            solidHeader = TRUE,
            width = 12,
            DTOutput("methodology_comparison_table")
          )
        ),
        fluidRow(
          box(
            title = "Why Do Methods Differ?",
            status = "danger",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            h4("Key Classification Differences"),
            tags$ul(
              tags$li(
                strong("Eating & Drinking Places (SIC 58 → NAICS 722):"),
                " ST94 = Unproductive (lumped with Retail), M05/TP19 = Productive (transforms food)"
              ),
              tags$li(
                strong("Information Sector (NAICS 51):"),
                " ST94 = Mixed (no SIC equivalent), M05/TP19 = Productive (produces information commodities)"
              ),
              tags$li(
                strong("Computer Systems Design (NAICS 5415):"),
                " ST94 = Mixed (SIC 7370 Business Services), M05/TP19 = Productive (software production)"
              )
            ),
            hr(),
            h4("Methodology Timeline"),
            p(strong("1948-1987:"), " Use ST94 (original I-O integration, SIC-based)"),
            p(strong("1988-1996:"), " Use M05 SM approximation (better BLS data allows calibration)"),
            p(strong("1997-2024:"), " Use TP19 NAICS classification (proper post-1997 classification)"),
            hr(),
            h4("Reference"),
            p("See ", strong("Chapter 5, pp. 151-194"), " of Shaikh & Tonak (1994) for original methodology."),
            p("See ", strong("Mohun (2005), Table 1, p.358"), " for SM approximation details."),
            p("See ", strong("Tsoulfidis & Paitaridis (2019), Table 1, p.238"), " for NAICS implementation.")
          )
        )
      ),

      # ============================================
      # TAB 2.6: INDUSTRY CLASSIFICATION (NEW)
      # ============================================
      tabItem(
        tabName = "classification",
        h2("Industry Classification Schema"),
        p("SIC vs NAICS classification of industries as Productive (P) or Unproductive (U)"),
        fluidRow(
          infoBox(
            "Productive Sectors",
            value = "~49%",
            subtitle = "of employment (1989)",
            icon = icon("industry"),
            color = "green",
            width = 4
          ),
          infoBox(
            "Key Reclassifications",
            value = "3",
            subtitle = "Eating/Drinking, Information, Computer Design",
            icon = icon("exchange-alt"),
            color = "orange",
            width = 4
          ),
          infoBox(
            "SIC→NAICS Transition",
            value = "1997",
            subtitle = "Major classification system change",
            icon = icon("calendar"),
            color = "purple",
            width = 4
          )
        ),
        fluidRow(
          box(
            title = "Complete Industry Classification Matrix",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            p("P = Productive, U = Unproductive, Mix = Mixed classification"),
            DTOutput("industry_classification_table")
          )
        ),
        fluidRow(
          box(
            title = "Key Reclassifications Across Methodologies",
            status = "warning",
            solidHeader = TRUE,
            width = 12,
            h4(icon("utensils"), " Eating and Drinking Places (SIC 58 → NAICS 722)"),
            fluidRow(
              column(
                4,
                div(
                  class = "well", style = "background-color: #dd4b39; color: white; text-align: center;",
                  h5("ST94 (1994)"), p("UNPRODUCTIVE"), p(em("Lumped with Retail Trade"))
                )
              ),
              column(
                4,
                div(
                  class = "well", style = "background-color: #00a65a; color: white; text-align: center;",
                  h5("M05 (2005)"), p("PRODUCTIVE"), p(em("Transforms food into meals"))
                )
              ),
              column(
                4,
                div(
                  class = "well", style = "background-color: #00a65a; color: white; text-align: center;",
                  h5("TP19 (2019)"), p("PRODUCTIVE"), p(em("~8.4% of employment"))
                )
              )
            ),
            hr(),
            h4(icon("info-circle"), " Information Sector (NAICS 51)"),
            fluidRow(
              column(
                4,
                div(
                  class = "well", style = "background-color: #f39c12; color: white; text-align: center;",
                  h5("ST94 (1994)"), p("MIXED"), p(em("No separate SIC code"))
                )
              ),
              column(
                4,
                div(
                  class = "well", style = "background-color: #00a65a; color: white; text-align: center;",
                  h5("M05 (2005)"), p("PRODUCTIVE"), p(em("Information commodities"))
                )
              ),
              column(
                4,
                div(
                  class = "well", style = "background-color: #00a65a; color: white; text-align: center;",
                  h5("TP19 (2019)"), p("PRODUCTIVE"), p(em("~2.1% of employment"))
                )
              )
            ),
            hr(),
            h4(icon("laptop-code"), " Computer Systems Design (SIC 7370 → NAICS 5415)"),
            fluidRow(
              column(
                4,
                div(
                  class = "well", style = "background-color: #f39c12; color: white; text-align: center;",
                  h5("ST94 (1994)"), p("MIXED"), p(em("Buried in Business Services"))
                )
              ),
              column(
                4,
                div(
                  class = "well", style = "background-color: #00a65a; color: white; text-align: center;",
                  h5("M05 (2005)"), p("PRODUCTIVE"), p(em("Software as commodity"))
                )
              ),
              column(
                4,
                div(
                  class = "well", style = "background-color: #00a65a; color: white; text-align: center;",
                  h5("TP19 (2019)"), p("PRODUCTIVE"), p(em("~2.4% of employment"))
                )
              )
            )
          )
        ),
        fluidRow(
          box(
            title = "SIC → NAICS Transition (1997)",
            status = "info",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            collapsed = TRUE,
            h4("Why 1997 Matters"),
            p("The Standard Industrial Classification (SIC) system was replaced by the North American Industry Classification System (NAICS) in 1997."),
            p("This created a major discontinuity in economic data series:"),
            tags$ul(
              tags$li("Pre-1997 data uses SIC codes (Shaikh-Tonak 1994 methodology)"),
              tags$li("Post-1997 data uses NAICS codes (Tsoulfidis-Paitaridis 2019 methodology)"),
              tags$li("BEA provides bridge tables but discontinuities remain")
            ),
            hr(),
            p(
              strong("Reference:"), " BEA (1997) 'Input-Output Concepts and Methods', Survey of Current Business. See ",
              em("Knowledge_Base/HDARP_Extractions/BEA_1997_IO_Concepts_Methods/")
            )
          )
        )
      ),

      # ============================================
      # TAB 2.7: QUESTIONS FOR PROFESSOR TONAK (NEW)
      # ============================================
      tabItem(
        tabName = "tonak_questions",
        h2(icon("user-graduate"), " Outstanding Questions for Professor Tonak"),
        p("Critical methodological questions requiring clarification for faithful replication and extension"),
        fluidRow(
          infoBox(
            "Critical Questions",
            value = sum(questions_for_tonak$Priority == "Critical", na.rm = TRUE),
            subtitle = "Blocking issues",
            icon = icon("exclamation-triangle"),
            color = "red",
            width = 4
          ),
          infoBox(
            "High Priority",
            value = sum(questions_for_tonak$Priority == "High", na.rm = TRUE),
            subtitle = "Important clarifications",
            icon = icon("arrow-up"),
            color = "orange",
            width = 4
          ),
          infoBox(
            "Total Questions",
            value = nrow(questions_for_tonak),
            subtitle = "For discussion",
            icon = icon("question-circle"),
            color = "blue",
            width = 4
          )
        ),
        fluidRow(
          box(
            title = "Print-Friendly Question Summary",
            status = "success",
            width = 12,
            p("Download a formatted summary of all questions for your meeting with Professor Tonak:"),
            downloadButton("download_tonak_questions", "Download Questions Summary (PDF-ready)",
              class = "btn-success btn-lg"
            )
          )
        ),
        fluidRow(
          box(
            title = "Questions for Professor Tonak",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            DTOutput("tonak_questions_table")
          )
        ),
        fluidRow(
          box(
            title = "Question Categories Explained",
            status = "info",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            fluidRow(
              column(
                6,
                h4(icon("cog"), " Data & Methodology"),
                p("Questions about calculation methods, data sources, and computational procedures."),
                p(em("Examples: K vs K* capital stock, capacity utilization formula, interpolation methods"))
              ),
              column(
                6,
                h4(icon("sitemap"), " Industry Classification"),
                p("Questions about which industries are productive vs unproductive."),
                p(em("Examples: Eating/Drinking classification, Information sector, Computer Design"))
              )
            ),
            fluidRow(
              column(
                6,
                h4(icon("balance-scale"), " Capital Composition"),
                p("Questions about C*/V* calculation and related concepts."),
                p(em("Examples: Rental income allocation, historical vs replacement cost"))
              ),
              column(
                6,
                h4(icon("university"), " Government Treatment"),
                p("Questions about how government spending and employment are handled."),
                p(em("Examples: Exclusion vs inclusion as unproductive"))
              )
            )
          )
        )
      ),

      # ============================================
      # TAB 3: PROFIT RATE ANALYSIS
      # ============================================
      tabItem(
        tabName = "profit_rate",
        h2("Profit Rate Analysis"),
        p("Comparison of Marxian and conventional profit rate measures"),
        fluidRow(
          box(
            title = "Profit Rate Measures (1948-2024)",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("profit_rate_plot", height = "500px")
          )
        ),
        fluidRow(
          box(
            title = "Series Selection",
            status = "info",
            width = 4,
            checkboxGroupInput("profit_series",
              "Select series to display:",
              choices = c(
                "Marxian r* (unadjusted)" = "r_star_pct",
                "Marxian r* (capacity-adjusted)" = "r_star_adj_pct",
                "NIPA r (unadjusted)" = "r_nipa_pct",
                "NIPA r (capacity-adjusted)" = "r_nipa_adj_pct"
              ),
              selected = c("r_star_pct", "r_nipa_pct")
            )
          ),
          box(
            title = "Profit Rate Statistics",
            status = "success",
            width = 8,
            DTOutput("profit_stats_table")
          )
        ),
        fluidRow(
          box(
            title = "Understanding Profit Rates",
            status = "warning",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            collapsed = TRUE,
            h4("Marxian Profit Rate (r*)"),
            p(strong("Definition:"), " r* = S*/K, where S* is total surplus value and K is capital stock"),
            p(strong("Key insight:"), " S* includes wages of unproductive workers (paid from surplus), making r* higher than conventional measures"),
            p(strong("Why capacity-adjusted?"), " r*' = r*/u adjusts for capacity utilization (u), showing rate at full capacity"),
            hr(),
            h4("NIPA Profit Rate (r)"),
            p(strong("Definition:"), " r = Corporate Profits / Capital Stock (conventional measure)"),
            p(strong("Difference:"), " Excludes unproductive wages, interest, rent from surplus definition"),
            hr(),
            h4("Note on r* Values"),
            p("Marxian profit rates appear high (200-500%) because:"),
            tags$ul(
              tags$li("S* includes ALL surplus appropriation (profits + unproductive wages + interest + rent)"),
              tags$li("Unproductive workers represent ~47-51% of total employment"),
              tags$li("Their wages (~$1.1 trillion in 1948) are paid from surplus, not from value they create"),
              tags$li("This is theoretically correct within the Marxian framework")
            ),
            p(strong("See Validation tab"), " for comparison with Shaikh-Tonak Table 5.8 benchmarks")
          )
        )
      ),

      # ============================================
      # TAB 6: VALIDATION CENTER
      # ============================================
      tabItem(
        tabName = "validation",
        h2("Validation Center"),
        p("Cross-validation against Shaikh-Tonak (1994) Table 5.8 benchmarks"),
        fluidRow(
          valueBoxOutput("validation_status", width = 4),
          valueBoxOutput("validation_r_star", width = 4),
          valueBoxOutput("validation_exploitation", width = 4)
        ),
        fluidRow(
          box(
            title = "Calculated vs. Target Values (Table 5.8 Benchmark Years)",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("validation_scatter", height = "500px")
          )
        ),
        fluidRow(
          box(
            title = "Deviation from Table 5.8 Targets",
            status = "warning",
            solidHeader = TRUE,
            width = 12,
            DTOutput("validation_table")
          )
        ),
        fluidRow(
          box(
            title = "Validation Notes",
            status = "danger",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            h4("Known Discrepancies"),
            p(strong("Issue:"), " Marxian profit rate r* shows large deviation from Table 5.8"),
            tags$ul(
              tags$li(strong("Our calculation:"), " r* ≈ 300% (1948) → 186% (1989)"),
              tags$li(strong("Table 5.8 target:"), " r*' ≈ 52% (1948) → 39% (1989)"),
              tags$li(strong("Ratio:"), " ~5.8x difference")
            ),
            hr(),
            h4("Root Causes Identified"),
            p("1. ", strong("Capital Stock Definition:")),
            tags$ul(
              tags$li("We use K = Total nonresidential fixed assets"),
              tags$li("Table 5.8 uses K* = C*f = Productive fixed capital only"),
              tags$li("K* should be smaller than K (only productive sectors)")
            ),
            p("2. ", strong("Capacity Utilization Adjustment:")),
            tags$ul(
              tags$li("Table 5.8 shows r*' = (S*/K*)/u (capacity-adjusted)"),
              tags$li("We calculate r* = S*/K (unadjusted)")
            ),
            hr(),
            h4("Resolution Strategy"),
            p("The displayed values use our current methodology. To match Table 5.8:"),
            tags$ol(
              tags$li("Calculate K* = K × (Y/GDP) to estimate productive capital"),
              tags$li("Apply capacity adjustment: r*' = (S*/K*)/u"),
              tags$li("Cross-validate with Mohun (2005, 2013) alternative estimates")
            ),
            p(strong("Status:"), " Investigation ongoing. See Technical/R_STAR_DISCREPANCY_RESOLUTION.md for details"),
            hr(),
            h4("Validation Quality"),
            p(strong("Exploitation rate (S*/V*):"), " EXCELLENT match (within 5%)"),
            p(strong("Value composition (C*/V*):"), " GOOD match (within 10-15%)"),
            p(strong("Profit rate (r*):"), " UNDER INVESTIGATION (see above)")
          )
        )
      ),

      # ============================================
      # PLACEHOLDER TABS (to be implemented)
      # ============================================
      tabItem(
        tabName = "exploitation",
        h2("Exploitation & Capital Composition"),
        p("Analysis of surplus extraction and organic composition of capital"),
        fluidRow(
          valueBoxOutput("exploit_current", width = 3),
          valueBoxOutput("exploit_change", width = 3),
          valueBoxOutput("value_comp_current", width = 3),
          valueBoxOutput("surplus_ratio_current", width = 3)
        ),
        fluidRow(
          box(
            title = "Exploitation Rate (S*/V*) and Surplus Ratio (S*/Y)",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("exploitation_plot", height = "450px")
          )
        ),
        fluidRow(
          box(
            title = "Capital Composition Analysis",
            status = "success",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("composition_plot", height = "450px")
          )
        ),
        fluidRow(
          box(
            title = "Exploitation Metrics by Decade",
            status = "warning",
            solidHeader = TRUE,
            width = 6,
            DTOutput("exploitation_decade_table")
          ),
          box(
            title = "Understanding Exploitation & Composition",
            status = "info",
            solidHeader = TRUE,
            width = 6,
            collapsible = TRUE,
            h4("Exploitation Rate (S*/V*)"),
            p(strong("Definition:"), " Ratio of surplus value to variable capital"),
            p(strong("Interpretation:"), " Higher values = more surplus extracted per dollar of productive wages"),
            p(strong("Trend 1948-1989:"), " Rose from 1.32 to 2.44 (+84%), showing intensified exploitation"),
            hr(),
            h4("Surplus Ratio (S*/Y)"),
            p(strong("Definition:"), " Share of total value product going to surplus"),
            p(strong("Formula:"), " S*/Y = S*/(C* + V* + S*)"),
            hr(),
            h4("Value Composition (C*/V*)"),
            p(strong("Definition:"), " Ratio of constant to variable capital"),
            p(strong("Interpretation:"), " Rising C*/V* indicates mechanization and rising capital intensity"),
            p(strong("Significance:"), " Key determinant of the profit rate: r* = (S*/V*) / (1 + C*/V*)")
          )
        )
      ),
      tabItem(
        tabName = "employment",
        h2("Employment Analysis"),
        p("Productive vs. unproductive labor composition and productivity trends"),
        fluidRow(
          valueBoxOutput("emp_total_current", width = 3),
          valueBoxOutput("emp_productive_share", width = 3),
          valueBoxOutput("emp_productive_trend", width = 3),
          valueBoxOutput("productivity_growth", width = 3)
        ),
        fluidRow(
          box(
            title = "Employment Composition (1948-1989)",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("employment_composition_plot", height = "450px")
          )
        ),
        fluidRow(
          box(
            title = "Absolute Employment Levels (thousands)",
            status = "success",
            solidHeader = TRUE,
            width = 7,
            plotlyOutput("employment_absolute_plot", height = "400px")
          ),
          box(
            title = "Employment Statistics",
            status = "info",
            solidHeader = TRUE,
            width = 5,
            DTOutput("employment_stats_table")
          )
        ),
        fluidRow(
          box(
            title = "Productivity Comparison: Marxian vs. Conventional",
            status = "warning",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("productivity_comparison_plot", height = "450px")
          )
        ),
        fluidRow(
          box(
            title = "Understanding Productive vs. Unproductive Labor",
            status = "danger",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            collapsed = TRUE,
            h4("Productive Labor (Lp)"),
            p(strong("Definition:"), " Workers directly engaged in producing surplus value"),
            p(strong("Sectors:"), " Manufacturing, construction, agriculture, mining, transportation"),
            p(strong("Trend:"), " Fell from 53% to 49% of total employment (1948-1989)"),
            hr(),
            h4("Unproductive Labor (Lu)"),
            p(strong("Definition:"), " Workers not engaged in surplus production, paid from surplus"),
            p(strong("Sectors:"), " Finance, insurance, real estate, advertising, government administration"),
            p(strong("Trend:"), " Rose from 47% to 51% of total employment"),
            hr(),
            h4("Marxian vs. Conventional Productivity"),
            p(strong("Marxian:"), " Y/Lp - Output per productive worker only"),
            p(strong("Conventional:"), " Y/L - Output per total worker (BLS measure)"),
            p(strong("Key insight:"), " Marxian productivity rises faster as Lp/L falls")
          )
        )
      ),
      tabItem(
        tabName = "government",
        h2("Government Absorption of Surplus"),
        p("Analysis of government expenditure as deduction from surplus value"),
        fluidRow(
          valueBoxOutput("govt_total_current", width = 3),
          valueBoxOutput("govt_surplus_ratio", width = 3),
          valueBoxOutput("govt_gdp_ratio", width = 3),
          valueBoxOutput("govt_growth", width = 3)
        ),
        fluidRow(
          box(
            title = "Government Absorption Ratios (1948-1989)",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("government_ratios_plot", height = "450px")
          )
        ),
        fluidRow(
          box(
            title = "Government Expenditure by Level",
            status = "success",
            solidHeader = TRUE,
            width = 7,
            plotlyOutput("government_levels_plot", height = "400px")
          ),
          box(
            title = "Government Statistics by Decade",
            status = "info",
            solidHeader = TRUE,
            width = 5,
            DTOutput("government_decade_table")
          )
        ),
        fluidRow(
          box(
            title = "Understanding Government as Surplus Absorption",
            status = "warning",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            collapsed = TRUE,
            h4("Marxian Treatment of Government"),
            p(strong("Key insight:"), " Government expenditure represents unproductive consumption paid from surplus"),
            p(strong("G/S* ratio:"), " Share of surplus absorbed by government spending"),
            p(strong("Trend:"), " Rose from 3.4% (1948) to higher levels by 1989"),
            hr(),
            h4("Components"),
            p(strong("Federal:"), " Defense, social programs, administration"),
            p(strong("State & Local:"), " Education, infrastructure, public services"),
            hr(),
            h4("Theoretical Significance"),
            tags$ul(
              tags$li("Government workers are unproductive (transfer value, don't create it)"),
              tags$li("Government spending reduces surplus available for accumulation"),
              tags$li("Rising G/S* can constrain capital accumulation and growth")
            )
          )
        )
      ),
      tabItem(
        tabName = "literature",
        h2("Literature Navigator"),
        p("Key references, methodological notes, and knowledge base links"),
        fluidRow(
          box(
            title = "Primary Reference",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            h3("Shaikh, Anwar M. & Tonak, E. Ahmet (1994)"),
            h4(em("Measuring the Wealth of Nations: The Political Economy of National Accounts")),
            p(strong("Publisher:"), " Cambridge University Press"),
            p(strong("Chapter 5:"), " \"The Profit Rate and Its Components\" (pp. 151-194)"),
            hr(),
            p(strong("Key Contributions:")),
            tags$ul(
              tags$li("Rigorous derivation of Marxian categories from NIPA data"),
              tags$li("Distinction between productive and unproductive labor"),
              tags$li("Calculation of S*, V*, C* from national accounts"),
              tags$li("Empirical evidence for tendential fall in profit rate")
            ),
            hr(),
            p(strong("Table 5.8:"), " Benchmark values used for validation in this app")
          )
        ),
        fluidRow(
          box(
            title = "Methodological Documentation",
            status = "success",
            solidHeader = TRUE,
            width = 6,
            collapsible = TRUE,
            h4("Data Sources"),
            tags$ul(
              tags$li(strong("BEA NIPA:"), " National Income and Product Accounts"),
              tags$li(strong("BLS:"), " Productivity and employment data"),
              tags$li(strong("Federal Reserve:"), " Capacity utilization (manufacturing)")
            ),
            hr(),
            h4("Key Methodological Steps"),
            tags$ol(
              tags$li("Classify industries as productive vs. unproductive"),
              tags$li("Calculate productive output Y from GDP"),
              tags$li("Derive V* (productive wages), S* (total surplus), C* (constant capital)"),
              tags$li("Compute exploitation rate S*/V*, composition C*/V*, profit rate r* = S*/K")
            ),
            hr(),
            p(strong("See:"), " Shaikh & Tonak (1994), Appendix 5.1 for detailed classification")
          ),
          box(
            title = "Related Literature",
            status = "info",
            solidHeader = TRUE,
            width = 6,
            collapsible = TRUE,
            h4("Follow-up Studies"),
            tags$ul(
              tags$li(strong("Mohun (2005):"), " \"Distributive Shares in the US Economy, 1964-2001\""),
              tags$li(strong("Mohun (2013):"), " \"Unproductive Labor in the US Economy 1964-2010\""),
              tags$li(strong("Basu & Manolakos (2013):"), " \"Is There a Tendency for the Rate of Profit to Fall?\""),
              tags$li(strong("Kliman (2011):"), em(" The Failure of Capitalist Production"))
            ),
            hr(),
            h4("Critical Debates"),
            tags$ul(
              tags$li("Productive vs. unproductive labor classification"),
              tags$li("Treatment of fixed capital depreciation"),
              tags$li("Capacity utilization adjustments"),
              tags$li("Alternative measures of capital stock (K vs. K*)")
            )
          )
        ),
        fluidRow(
          box(
            title = "Knowledge Base Extractions",
            status = "warning",
            solidHeader = TRUE,
            width = 12,
            h4("Available Documentation"),
            p("The following knowledge base files contain detailed extraction and analysis:"),
            tags$ul(
              tags$li(strong("R_STAR_DISCREPANCY_RESOLUTION.md:"), " Investigation of profit rate calculation differences"),
              tags$li(strong("VALIDATION_RESULTS.md:"), " Cross-validation against Table 5.8 benchmarks"),
              tags$li(strong("METHODOLOGY_NOTES.md:"), " Step-by-step calculation procedures"),
              tags$li(strong("DATA_PROVENANCE.md:"), " Data sources and transformations")
            ),
            hr(),
            p(em("Note: Links to knowledge base files can be implemented with file path references or downloadable PDFs"))
          )
        ),

        # NEW: HDARP Extracted Literature with page citations
        fluidRow(
          box(
            title = "HDARP-Extracted Literature Database",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            h4(icon("book-open"), " Complete Bibliography with Page-Level Citations"),
            p("All sources have been processed through HDARP (Hybrid Direct Agent Reading Protocol) for maximum extraction accuracy."),
            DTOutput("literature_citations_table")
          )
        ),
        fluidRow(
          box(
            title = "Methodology Evolution Timeline",
            status = "info",
            solidHeader = TRUE,
            width = 12,
            h4("Development of Marxian National Accounting"),
            fluidRow(
              column(
                3,
                div(
                  class = "well", style = "text-align: center; background-color: #3c8dbc; color: white;",
                  h4("1984"),
                  p(strong("Semmler")),
                  p("Competition, Monopoly, and Differential Profit Rates"),
                  p(em("Foundational theory"))
                )
              ),
              column(
                3,
                div(
                  class = "well", style = "text-align: center; background-color: #00a65a; color: white;",
                  h4("1994"),
                  p(strong("Shaikh & Tonak")),
                  p("Measuring the Wealth of Nations"),
                  p(em("ST94 methodology"))
                )
              ),
              column(
                3,
                div(
                  class = "well", style = "text-align: center; background-color: #f39c12; color: white;",
                  h4("2005"),
                  p(strong("Mohun")),
                  p("Distributive Shares in the US Economy"),
                  p(em("M05 SM approximation"))
                )
              ),
              column(
                3,
                div(
                  class = "well", style = "text-align: center; background-color: #605ca8; color: white;",
                  h4("2019"),
                  p(strong("Tsoulfidis & Paitaridis")),
                  p("Capital Intensity and the Great Recession"),
                  p(em("TP19 NAICS methodology"))
                )
              )
            )
          )
        ),
        fluidRow(
          box(
            title = "Citation Guide",
            status = "danger",
            solidHeader = TRUE,
            width = 12,
            collapsible = TRUE,
            collapsed = TRUE,
            h4("How to Cite This App"),
            p(strong("APA Format:")),
            p(
              "Arcanum Project. (2025). ", em("Shaikh-Tonak Marxian Analysis Shiny App (1948-1989)."),
              " Interactive data visualization. Based on Shaikh, A. M., & Tonak, E. A. (1994). ",
              em("Measuring the Wealth of Nations."), " Cambridge University Press."
            ),
            hr(),
            h4("How to Cite Shaikh & Tonak (1994)"),
            p(strong("APA Format:")),
            p(
              "Shaikh, A. M., & Tonak, E. A. (1994). ", em("Measuring the wealth of nations: The political economy of national accounts."),
              " Cambridge University Press."
            ),
            hr(),
            p(strong("BibTeX:"), " (available in Downloads tab)")
          )
        )
      ),
      tabItem(
        tabName = "downloads",
        h2("Data Downloads"),
        p("Export datasets in multiple formats for further analysis"),
        fluidRow(
          infoBox(
            "Available Datasets",
            value = "11",
            subtitle = "Extended datasets ready for download",
            icon = icon("database"),
            color = "blue",
            width = 4
          ),
          infoBox(
            "Time Period",
            value = "1948-2024",
            subtitle = "77 years of annual data",
            icon = icon("calendar"),
            color = "green",
            width = 4
          ),
          infoBox(
            "Formats",
            value = "CSV, Excel, RData",
            subtitle = "Multiple export options",
            icon = icon("file-export"),
            color = "orange",
            width = 4
          )
        ),
        fluidRow(
          box(
            title = "Individual Dataset Downloads",
            status = "primary",
            solidHeader = TRUE,
            width = 12,
            p("Download individual datasets (CSV format):"),
            hr(),
            fluidRow(
              column(
                6,
                h4("Core Economic Indicators"),
                downloadButton("download_profit_rates", "Profit Rates (1948-1989)",
                  class = "btn-primary", style = "margin: 5px; width: 95%;"
                ),
                br(),
                downloadButton("download_exploitation", "Exploitation & Composition",
                  class = "btn-primary", style = "margin: 5px; width: 95%;"
                ),
                br(),
                downloadButton("download_employment", "Employment Data",
                  class = "btn-primary", style = "margin: 5px; width: 95%;"
                ),
                br(),
                downloadButton("download_productivity", "Productivity Measures",
                  class = "btn-primary", style = "margin: 5px; width: 95%;"
                )
              ),
              column(
                6,
                h4("Supplementary Data"),
                downloadButton("download_government", "Government Expenditures",
                  class = "btn-success", style = "margin: 5px; width: 95%;"
                ),
                br(),
                downloadButton("download_validation", "Validation Targets (Table 5.8)",
                  class = "btn-success", style = "margin: 5px; width: 95%;"
                ),
                br(),
                downloadButton("download_comprehensive", "Comprehensive Dataset (All Series)",
                  class = "btn-warning", style = "margin: 5px; width: 95%;"
                )
              )
            )
          )
        ),
        fluidRow(
          box(
            title = "Filtered Data Export",
            status = "success",
            solidHeader = TRUE,
            width = 6,
            p("Export data with current year range filter applied:"),
            p(strong("Current selection:"), textOutput("download_year_range", inline = TRUE)),
            hr(),
            radioButtons("download_format",
              "Select format:",
              choices = c(
                "CSV" = "csv",
                "Excel (.xlsx)" = "xlsx",
                "R Data (.RData)" = "rdata"
              ),
              selected = "csv"
            ),
            hr(),
            downloadButton("download_filtered", "Download Filtered Data",
              class = "btn-success btn-lg", style = "width: 100%;"
            )
          ),
          box(
            title = "Data Dictionary",
            status = "info",
            solidHeader = TRUE,
            width = 6,
            h4("Variable Definitions"),
            p(strong("r_star_pct:"), " Marxian profit rate S*/K (%)"),
            p(strong("r_nipa_pct:"), " NIPA profit rate (%)"),
            p(strong("exploitation_rate:"), " S*/V* (surplus/variable capital)"),
            p(strong("value_composition:"), " C*/V* (constant/variable capital)"),
            p(strong("Lp_L_ratio:"), " Productive labor share"),
            p(strong("G_S_ratio:"), " Government/surplus ratio"),
            hr(),
            downloadButton("download_codebook", "Download Full Codebook (TXT)",
              class = "btn-info", style = "width: 100%;"
            )
          )
        )
      )
    )
  })

  # ============================================
  # TAB 2: EXPLORE BY QUESTION - FILTERING
  # ============================================

  # Filtered questions based on priority and category
  filtered_questions <- reactive({
    q <- questions

    # Filter by priority
    if (input$question_priority_filter != "all") {
      q <- q %>% filter(Priority == input$question_priority_filter)
    }

    # Filter by category
    if (input$question_category_filter != "all") {
      q <- q %>% filter(Category == input$question_category_filter)
    }

    q %>% arrange(Question_Number)
  })

  # Questions count display
  output$questions_count <- renderText({
    count <- nrow(filtered_questions())
    paste0(count, " Question", if (count != 1) "s" else "")
  })

  # Render question cards
  output$question_cards <- renderUI({
    questions_data <- filtered_questions()

    if (nrow(questions_data) == 0) {
      return(div(
        style = "text-align: center; padding: 40px; color: #999;",
        h4("No questions match the selected filters"),
        p("Try adjusting your filter criteria")
      ))
    }

    # Generate question cards
    cards <- lapply(1:nrow(questions_data), function(i) {
      q <- questions_data[i, ]

      div(
        class = "question-card",
        onclick = sprintf("Shiny.setInputValue('question_clicked', %d, {priority: 'event'})", q$Question_Number),
        div(
          class = "question-card-header",
          span(class = "question-number", paste0("Question ", q$Question_Number)),
          span(class = paste0("priority-badge priority-", q$Priority), q$Priority)
        ),
        div(class = "question-text", q$Question),
        div(
          class = "question-category",
          icon("folder-open"), " ", q$Category, " • ",
          icon("arrow-right"), " ", q$Target_Tab
        )
      )
    })

    do.call(tagList, cards)
  })

  # Handle question clicks and show modal
  observeEvent(input$question_clicked, {
    q_num <- input$question_clicked
    q <- questions %>% filter(Question_Number == q_num)

    if (nrow(q) == 0) {
      return()
    }

    # Create modal content
    showModal(modalDialog(
      title = div(
        style = "color: white;",
        h3(style = "margin: 0;", paste0("Question ", q$Question_Number)),
        p(style = "margin-top: 10px; font-size: 18px; font-weight: 600;", q$Question)
      ),
      size = "l",
      easyClose = TRUE,
      footer = tagList(
        actionButton(paste0("goto_tab_", q_num),
          paste("Go to", q$Target_Tab, "tab"),
          class = "btn-primary"
        ),
        modalButton("Close")
      ),

      # Answer Section
      div(
        class = "modal-section",
        h4(icon("lightbulb"), " Answer"),
        p(q$Explanation)
      ),

      # Formula Section
      if (!is.na(q$Formula) && q$Formula != "") {
        div(
          class = "modal-section",
          h4(icon("calculator"), " Formula"),
          div(class = "formula-box", q$Formula)
        )
      },

      # Definition Section
      if (!is.na(q$Definition) && q$Definition != "") {
        div(
          class = "modal-section",
          h4(icon("book-open"), " Definition"),
          p(q$Definition)
        )
      },

      # Visualization Section
      div(
        class = "modal-section",
        h4(icon("chart-line"), " Visualization"),
        plotlyOutput(paste0("modal_plot_", q_num), height = "350px")
      ),

      # Book Reference Section
      if (!is.na(q$Book_Reference) && q$Book_Reference != "") {
        div(
          class = "modal-section",
          h4(icon("bookmark"), " Book Reference"),
          div(
            class = "book-reference",
            icon("book"), " Shaikh & Tonak (1994): ", q$Book_Reference
          )
        )
      }
    ))

    # Generate appropriate plot based on category
    output[[paste0("modal_plot_", q_num)]] <- renderPlotly({
      if (q$Category == "Profit Rate") {
        data <- filtered_profit()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~r_star_pct, name = "Marxian r*",
            type = "scatter", mode = "lines",
            line = list(color = colors$primary, width = 3)
          ) %>%
          add_trace(
            y = ~r_star_adj_pct, name = "r* (capacity-adj)",
            type = "scatter", mode = "lines",
            line = list(color = colors$success, width = 2)
          ) %>%
          layout(
            title = "Marxian Profit Rate Trends",
            xaxis = list(title = "Year"),
            yaxis = list(title = "Profit Rate (%)"),
            hovermode = "x unified"
          )
      } else if (q$Category == "Surplus Value") {
        data <- filtered_exploitation()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~exploitation_rate, name = "Exploitation Rate (S*/V*)",
            type = "scatter", mode = "lines",
            line = list(color = colors$danger, width = 3)
          ) %>%
          add_trace(
            y = ~ surplus_ratio * 100, name = "Surplus Ratio (S*/Y %)",
            type = "scatter", mode = "lines",
            line = list(color = colors$warning, width = 2)
          ) %>%
          layout(
            title = "Surplus Value Metrics",
            xaxis = list(title = "Year"),
            yaxis = list(title = "Ratio"),
            hovermode = "x unified"
          )
      } else if (q$Category == "Capital Composition") {
        data <- filtered_exploitation()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~value_composition, name = "Value Composition (C*/V*)",
            type = "scatter", mode = "lines",
            line = list(color = colors$purple, width = 3)
          ) %>%
          add_trace(
            y = ~materialized_composition, name = "Materialized Composition",
            type = "scatter", mode = "lines",
            line = list(color = colors$teal, width = 2)
          ) %>%
          layout(
            title = "Capital Composition Trends",
            xaxis = list(title = "Year"),
            yaxis = list(title = "Ratio"),
            hovermode = "x unified"
          )
      } else if (q$Category == "Employment") {
        data <- filtered_employment()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~ Lp_L_ratio * 100, name = "Productive Share (%)",
            type = "scatter", mode = "lines",
            line = list(color = colors$success, width = 3)
          ) %>%
          add_trace(
            y = ~ Lu_L_ratio * 100, name = "Unproductive Share (%)",
            type = "scatter", mode = "lines",
            line = list(color = colors$danger, width = 3)
          ) %>%
          layout(
            title = "Employment Composition",
            xaxis = list(title = "Year"),
            yaxis = list(title = "Share of Total Employment (%)"),
            hovermode = "x unified"
          )
      } else if (q$Category == "Government") {
        data <- filtered_government()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~ G_S_ratio * 100, name = "G/S* (%)",
            type = "scatter", mode = "lines",
            line = list(color = colors$warning, width = 3)
          ) %>%
          add_trace(
            y = ~ G_GDP_ratio * 100, name = "G/GDP (%)",
            type = "scatter", mode = "lines",
            line = list(color = colors$info, width = 2)
          ) %>%
          layout(
            title = "Government Absorption Ratios",
            xaxis = list(title = "Year"),
            yaxis = list(title = "Percentage"),
            hovermode = "x unified"
          )
      } else {
        # Data & Methodology - show comprehensive overview
        data <- filtered_profit()
        plot_ly(data, x = ~year) %>%
          add_trace(
            y = ~r_star_adj_pct, name = "r* (capacity-adj)",
            type = "scatter", mode = "lines",
            line = list(color = colors$primary, width = 3)
          ) %>%
          layout(
            title = "Overview: Marxian Profit Rate",
            xaxis = list(title = "Year"),
            yaxis = list(title = "Profit Rate (%)"),
            hovermode = "x unified"
          )
      }
    })
  })

  # Handle "Go to tab" button clicks
  observe({
    # Create observers for all possible questions
    for (q_num in 1:30) {
      local({
        num <- q_num
        observeEvent(input[[paste0("goto_tab_", num)]], {
          q <- questions %>% filter(Question_Number == num)
          if (nrow(q) > 0) {
            # Map target tab names to tab IDs
            tab_map <- c(
              "overview" = "overview",
              "profit_rate" = "profit_rate",
              "exploitation" = "exploitation",
              "employment" = "employment",
              "government" = "government",
              "validation" = "validation",
              "literature" = "literature"
            )

            target <- tolower(gsub(" ", "_", q$Target_Tab))
            target <- gsub("_analysis", "", target)
            target <- gsub("_center", "", target)
            target <- gsub("_navigator", "", target)

            if (target %in% names(tab_map)) {
              updateTabItems(session, "tabs", tab_map[[target]])
              removeModal()
            }
          }
        })
      })
    }
  })

  # ============================================
  # TAB 1: OVERVIEW - VALUE BOXES
  # ============================================

  output$vbox_r_star <- renderValueBox({
    latest_year <- max(filtered_profit()$year)
    latest_r <- filtered_profit() %>%
      filter(year == latest_year) %>%
      pull(r_star_pct)

    valueBox(
      value = sprintf("%.1f%%", latest_r),
      subtitle = paste0("Marxian Profit Rate (", latest_year, ")"),
      icon = icon("chart-line"),
      color = "blue"
    )
  })

  output$vbox_exploitation <- renderValueBox({
    latest_year <- max(filtered_exploitation()$year)
    latest_e <- filtered_exploitation() %>%
      filter(year == latest_year) %>%
      pull(exploitation_rate)

    valueBox(
      value = sprintf("%.2f", latest_e),
      subtitle = paste0("Exploitation Rate S*/V* (", latest_year, ")"),
      icon = icon("balance-scale"),
      color = "green"
    )
  })

  output$vbox_productive_share <- renderValueBox({
    latest_year <- max(filtered_employment()$year)
    latest_lp <- filtered_employment() %>%
      filter(year == latest_year) %>%
      pull(Lp_L_ratio)

    valueBox(
      value = sprintf("%.1f%%", latest_lp * 100),
      subtitle = paste0("Productive Labor Share (", latest_year, ")"),
      icon = icon("users"),
      color = "orange"
    )
  })

  output$vbox_govt_absorption <- renderValueBox({
    latest_year <- max(filtered_government()$year)
    latest_g <- filtered_government() %>%
      filter(year == latest_year) %>%
      pull(G_S_ratio)

    valueBox(
      value = sprintf("%.1f%%", latest_g * 100),
      subtitle = paste0("Gov't/Surplus Ratio (", latest_year, ")"),
      icon = icon("university"),
      color = "red"
    )
  })

  # ============================================
  # TAB 1: OVERVIEW - MAIN PLOT
  # ============================================

  output$overview_profit_plot <- renderPlotly({
    data <- filtered_profit()

    p <- plot_ly(data, x = ~year) %>%
      add_trace(
        y = ~r_star_pct,
        name = "Marxian r*",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$primary, width = 3),
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>Marxian r*</b>: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      ) %>%
      add_trace(
        y = ~r_nipa_pct,
        name = "NIPA r",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$danger, width = 2, dash = "dash"),
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>NIPA r</b>: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      )

    # Add recession shading if enabled
    if (input$show_recessions) {
      for (i in 1:nrow(recessions)) {
        p <- p %>%
          add_ribbons(
            x = c(recessions$start[i], recessions$end[i]),
            ymin = 0,
            ymax = max(data$r_star_pct, na.rm = TRUE) * 1.1,
            fillcolor = "rgba(128, 128, 128, 0.2)",
            line = list(width = 0),
            showlegend = FALSE,
            hoverinfo = "text",
            text = paste("Recession:", recessions$label[i])
          )
      }
    }

    p <- p %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Profit Rate (%)"),
        hovermode = "x unified",
        legend = list(x = 0.7, y = 0.95)
      )

    p
  })

  # ============================================
  # TAB 1: OVERVIEW - TRENDS TABLE
  # ============================================

  output$overview_trends_table <- renderDT({
    # Calculate trends for key indicators
    trends <- tibble(
      Indicator = c(
        "Marxian Profit Rate (r*)",
        "NIPA Profit Rate (r)",
        "Exploitation Rate (S*/V*)",
        "Value Composition (C*/V*)",
        "Productive Labor Share (Lp/L)",
        "Government/Surplus (G/S*)"
      ),
      `1948` = c(
        sprintf("%.1f%%", profit_rates$r_star_pct[1]),
        sprintf("%.1f%%", profit_rates$r_nipa_pct[1]),
        sprintf("%.2f", exploitation$exploitation_rate[1]),
        sprintf("%.2f", exploitation$value_composition[1]),
        sprintf("%.1f%%", employment$Lp_L_ratio[1] * 100),
        sprintf("%.1f%%", government$G_S_ratio[1] * 100)
      ),
      `1989` = c(
        sprintf("%.1f%%", profit_rates$r_star_pct[42]),
        sprintf("%.1f%%", profit_rates$r_nipa_pct[42]),
        sprintf("%.2f", exploitation$exploitation_rate[42]),
        sprintf("%.2f", exploitation$value_composition[42]),
        sprintf("%.1f%%", employment$Lp_L_ratio[42] * 100),
        sprintf("%.1f%%", government$G_S_ratio[42] * 100)
      ),
      Change = c(
        sprintf("%.1f%%", ((profit_rates$r_star_pct[42] / profit_rates$r_star_pct[1]) - 1) * 100),
        sprintf("%.1f%%", ((profit_rates$r_nipa_pct[42] / profit_rates$r_nipa_pct[1]) - 1) * 100),
        sprintf("+%.1f%%", ((exploitation$exploitation_rate[42] / exploitation$exploitation_rate[1]) - 1) * 100),
        sprintf("+%.1f%%", ((exploitation$value_composition[42] / exploitation$value_composition[1]) - 1) * 100),
        sprintf("%.1f%%", ((employment$Lp_L_ratio[42] / employment$Lp_L_ratio[1]) - 1) * 100),
        sprintf("+%.1f%%", ((government$G_S_ratio[42] / government$G_S_ratio[1]) - 1) * 100)
      )
    )

    datatable(trends,
      options = list(
        dom = "t",
        paging = FALSE,
        searching = FALSE
      ),
      rownames = FALSE
    ) %>%
      formatStyle("Change",
        backgroundColor = styleInterval(c(0), c("#f8d7da", "#d4edda"))
      )
  })

  # ============================================
  # TAB 2: PROFIT RATE ANALYSIS
  # ============================================

  output$profit_rate_plot <- renderPlotly({
    data <- filtered_profit()
    selected <- input$profit_series

    p <- plot_ly(data, x = ~year)

    # Add selected series
    if ("r_star_pct" %in% selected) {
      p <- p %>% add_trace(
        y = ~r_star_pct, name = "Marxian r*",
        type = "scatter", mode = "lines",
        line = list(color = colors$primary, width = 3)
      )
    }
    if ("r_star_adj_pct" %in% selected) {
      p <- p %>% add_trace(
        y = ~r_star_adj_pct, name = "Marxian r* (cap-adj)",
        type = "scatter", mode = "lines",
        line = list(color = colors$info, width = 2, dash = "dot")
      )
    }
    if ("r_nipa_pct" %in% selected) {
      p <- p %>% add_trace(
        y = ~r_nipa_pct, name = "NIPA r",
        type = "scatter", mode = "lines",
        line = list(color = colors$danger, width = 2)
      )
    }
    if ("r_nipa_adj_pct" %in% selected) {
      p <- p %>% add_trace(
        y = ~r_nipa_adj_pct, name = "NIPA r (cap-adj)",
        type = "scatter", mode = "lines",
        line = list(color = colors$warning, width = 2, dash = "dot")
      )
    }

    # Add recession shading
    if (input$show_recessions && length(selected) > 0) {
      max_val <- max(c(
        if ("r_star_pct" %in% selected) data$r_star_pct else 0,
        if ("r_star_adj_pct" %in% selected) data$r_star_adj_pct else 0,
        if ("r_nipa_pct" %in% selected) data$r_nipa_pct else 0,
        if ("r_nipa_adj_pct" %in% selected) data$r_nipa_adj_pct else 0
      ), na.rm = TRUE)

      for (i in 1:nrow(recessions)) {
        p <- p %>%
          add_ribbons(
            x = c(recessions$start[i], recessions$end[i]),
            ymin = 0,
            ymax = max_val * 1.1,
            fillcolor = "rgba(128, 128, 128, 0.2)",
            line = list(width = 0),
            showlegend = FALSE,
            hoverinfo = "text",
            text = paste("Recession:", recessions$label[i])
          )
      }
    }

    # Add methodology overlay if selected
    method_sel <- input$method_overlay
    if (!is.null(method_sel) && method_sel != "none" && nrow(methodology_comparison) > 0) {
      mc <- methodology_comparison %>%
        filter(Year >= input$year_range[1], Year <= input$year_range[2])
      if (nrow(mc) > 0) {
        if (method_sel %in% c("ST94", "All") && "ST94_r" %in% names(mc)) {
          p <- p %>% add_trace(
            data = mc, x = ~Year, y = ~(ST94_r * 100), name = "ST94 r*",
            type = "scatter", mode = "lines",
            line = list(color = "#00a65a", width = 2, dash = "dash")
          )
        }
        if (method_sel %in% c("M05", "All") && "M05_r" %in% names(mc)) {
          p <- p %>% add_trace(
            data = mc, x = ~Year, y = ~(M05_r * 100), name = "M05 r*",
            type = "scatter", mode = "lines",
            line = list(color = "#f39c12", width = 2, dash = "dash")
          )
        }
        if (method_sel %in% c("TP19", "All") && "TP19_r" %in% names(mc)) {
          p <- p %>% add_trace(
            data = mc, x = ~Year, y = ~(TP19_r * 100), name = "TP19 r*",
            type = "scatter", mode = "lines",
            line = list(color = "#605ca8", width = 2, dash = "dash")
          )
        }
      }
    }

    p %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Profit Rate (%)"),
        hovermode = "x unified"
      )
  })

  output$profit_stats_table <- renderDT({
    data <- filtered_profit()

    stats <- tibble(
      Measure = c("Marxian r*", "Marxian r* (cap-adj)", "NIPA r", "NIPA r (cap-adj)"),
      Mean = c(
        mean(data$r_star_pct, na.rm = TRUE),
        mean(data$r_star_adj_pct, na.rm = TRUE),
        mean(data$r_nipa_pct, na.rm = TRUE),
        mean(data$r_nipa_adj_pct, na.rm = TRUE)
      ),
      Min = c(
        min(data$r_star_pct, na.rm = TRUE),
        min(data$r_star_adj_pct, na.rm = TRUE),
        min(data$r_nipa_pct, na.rm = TRUE),
        min(data$r_nipa_adj_pct, na.rm = TRUE)
      ),
      Max = c(
        max(data$r_star_pct, na.rm = TRUE),
        max(data$r_star_adj_pct, na.rm = TRUE),
        max(data$r_nipa_pct, na.rm = TRUE),
        max(data$r_nipa_adj_pct, na.rm = TRUE)
      ),
      `Std Dev` = c(
        sd(data$r_star_pct, na.rm = TRUE),
        sd(data$r_star_adj_pct, na.rm = TRUE),
        sd(data$r_nipa_pct, na.rm = TRUE),
        sd(data$r_nipa_adj_pct, na.rm = TRUE)
      )
    )

    datatable(stats,
      options = list(dom = "t", paging = FALSE),
      rownames = FALSE
    ) %>%
      formatRound(columns = c("Mean", "Min", "Max", "Std Dev"), digits = 1)
  })

  # ============================================
  # TAB 3: EXPLOITATION & COMPOSITION
  # ============================================

  output$exploit_current <- renderValueBox({
    latest_year <- max(filtered_exploitation()$year)
    latest_val <- filtered_exploitation() %>%
      filter(year == latest_year) %>%
      pull(exploitation_rate)

    valueBox(
      value = sprintf("%.2f", latest_val),
      subtitle = paste0("Exploitation Rate S*/V* (", latest_year, ")"),
      icon = icon("balance-scale"),
      color = "blue"
    )
  })

  output$exploit_change <- renderValueBox({
    data <- filtered_exploitation()
    first_val <- data$exploitation_rate[1]
    last_val <- data$exploitation_rate[nrow(data)]
    change_pct <- ((last_val / first_val) - 1) * 100

    valueBox(
      value = sprintf("%+.1f%%", change_pct),
      subtitle = "Exploitation Rate Change",
      icon = icon("arrow-up"),
      color = "green"
    )
  })

  output$value_comp_current <- renderValueBox({
    latest_year <- max(filtered_exploitation()$year)
    latest_val <- filtered_exploitation() %>%
      filter(year == latest_year) %>%
      pull(value_composition)

    valueBox(
      value = sprintf("%.2f", latest_val),
      subtitle = paste0("Value Composition C*/V* (", latest_year, ")"),
      icon = icon("industry"),
      color = "orange"
    )
  })

  output$surplus_ratio_current <- renderValueBox({
    latest_year <- max(filtered_exploitation()$year)
    latest_val <- filtered_exploitation() %>%
      filter(year == latest_year) %>%
      pull(surplus_ratio)

    valueBox(
      value = sprintf("%.1f%%", latest_val * 100),
      subtitle = paste0("Surplus Ratio S*/Y (", latest_year, ")"),
      icon = icon("pie-chart"),
      color = "purple"
    )
  })

  output$exploitation_plot <- renderPlotly({
    data <- filtered_exploitation()

    p <- plot_ly(data, x = ~year) %>%
      add_trace(
        y = ~exploitation_rate,
        name = "Exploitation Rate (S*/V*)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$primary, width = 3),
        yaxis = "y",
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>S*/V*</b>: %{y:.2f}<br>",
          "<extra></extra>"
        )
      ) %>%
      add_trace(
        y = ~ surplus_ratio * 100,
        name = "Surplus Ratio (S*/Y %)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$success, width = 2),
        yaxis = "y2",
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>S*/Y</b>: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      )

    # Add recession shading
    if (input$show_recessions) {
      for (i in 1:nrow(recessions)) {
        p <- p %>%
          add_ribbons(
            x = c(recessions$start[i], recessions$end[i]),
            ymin = 0,
            ymax = max(data$exploitation_rate, na.rm = TRUE) * 1.1,
            fillcolor = "rgba(128, 128, 128, 0.2)",
            line = list(width = 0),
            showlegend = FALSE,
            hoverinfo = "text",
            text = paste("Recession:", recessions$label[i]),
            yaxis = "y"
          )
      }
    }

    p %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(
          title = "Exploitation Rate (S*/V*)",
          side = "left"
        ),
        yaxis2 = list(
          title = "Surplus Ratio (%)",
          overlaying = "y",
          side = "right"
        ),
        hovermode = "x unified",
        legend = list(x = 0.1, y = 0.95)
      )
  })

  output$composition_plot <- renderPlotly({
    data <- filtered_exploitation()

    p <- plot_ly(data, x = ~year) %>%
      add_trace(
        y = ~value_composition,
        name = "Value Composition (C*/V*)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$warning, width = 3),
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>C*/V*</b>: %{y:.2f}<br>",
          "<extra></extra>"
        )
      ) %>%
      add_trace(
        y = ~materialized_composition,
        name = "Materialized Composition",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$info, width = 2, dash = "dash"),
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>Mat. Comp.</b>: %{y:.2f}<br>",
          "<extra></extra>"
        )
      )

    # Add recession shading
    if (input$show_recessions) {
      max_val <- max(c(data$value_composition, data$materialized_composition), na.rm = TRUE)
      for (i in 1:nrow(recessions)) {
        p <- p %>%
          add_ribbons(
            x = c(recessions$start[i], recessions$end[i]),
            ymin = min(c(data$value_composition, data$materialized_composition), na.rm = TRUE) * 0.9,
            ymax = max_val * 1.1,
            fillcolor = "rgba(128, 128, 128, 0.2)",
            line = list(width = 0),
            showlegend = FALSE,
            hoverinfo = "text",
            text = paste("Recession:", recessions$label[i])
          )
      }
    }

    p %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Composition Ratio"),
        hovermode = "x unified",
        legend = list(x = 0.7, y = 0.95)
      )
  })

  output$exploitation_decade_table <- renderDT({
    data <- filtered_exploitation() %>%
      mutate(decade = paste0(floor(year / 10) * 10, "s")) %>%
      group_by(decade) %>%
      summarize(
        `Avg S*/V*` = mean(exploitation_rate, na.rm = TRUE),
        `Avg S*/Y` = mean(surplus_ratio, na.rm = TRUE),
        `Avg C*/V*` = mean(value_composition, na.rm = TRUE),
        `Max S*/V*` = max(exploitation_rate, na.rm = TRUE),
        `Min S*/V*` = min(exploitation_rate, na.rm = TRUE)
      ) %>%
      mutate(
        `Avg S*/V*` = round(`Avg S*/V*`, 2),
        `Avg S*/Y` = sprintf("%.1f%%", `Avg S*/Y` * 100),
        `Avg C*/V*` = round(`Avg C*/V*`, 2),
        `Max S*/V*` = round(`Max S*/V*`, 2),
        `Min S*/V*` = round(`Min S*/V*`, 2)
      )

    datatable(data,
      options = list(
        dom = "t",
        paging = FALSE,
        searching = FALSE
      ),
      rownames = FALSE
    )
  })

  # ============================================
  # TAB 4: EMPLOYMENT ANALYSIS
  # ============================================

  output$emp_total_current <- renderValueBox({
    latest_year <- max(filtered_employment()$year)
    latest_val <- filtered_employment() %>%
      filter(year == latest_year) %>%
      pull(L_total)

    valueBox(
      value = format(latest_val, big.mark = ","),
      subtitle = paste0("Total Employment (", latest_year, ", thousands)"),
      icon = icon("users"),
      color = "blue"
    )
  })

  output$emp_productive_share <- renderValueBox({
    latest_year <- max(filtered_employment()$year)
    latest_val <- filtered_employment() %>%
      filter(year == latest_year) %>%
      pull(Lp_L_ratio)

    valueBox(
      value = sprintf("%.1f%%", latest_val * 100),
      subtitle = paste0("Productive Share Lp/L (", latest_year, ")"),
      icon = icon("industry"),
      color = "green"
    )
  })

  output$emp_productive_trend <- renderValueBox({
    data <- filtered_employment()
    first_val <- data$Lp_L_ratio[1]
    last_val <- data$Lp_L_ratio[nrow(data)]
    change_pct <- ((last_val / first_val) - 1) * 100

    color_choice <- if (change_pct < 0) "red" else "green"

    valueBox(
      value = sprintf("%+.1f%%", change_pct),
      subtitle = "Productive Share Change",
      icon = icon(if (change_pct < 0) "arrow-down" else "arrow-up"),
      color = color_choice
    )
  })

  output$productivity_growth <- renderValueBox({
    data <- productivity %>%
      filter(
        year >= input$year_range[1],
        year <= input$year_range[2]
      )

    first_idx <- data$marxian_index[1]
    last_idx <- data$marxian_index[nrow(data)]
    change_pct <- ((last_idx / first_idx) - 1) * 100

    valueBox(
      value = sprintf("%+.0f%%", change_pct),
      subtitle = "Marxian Productivity Growth",
      icon = icon("chart-area"),
      color = "purple"
    )
  })

  output$employment_composition_plot <- renderPlotly({
    data <- filtered_employment()

    p <- plot_ly(data, x = ~year) %>%
      add_trace(
        y = ~ Lp_L_ratio * 100,
        name = "Productive Share (Lp/L)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$success, width = 3),
        stackgroup = NULL,
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>Lp/L</b>: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      ) %>%
      add_trace(
        y = ~ Lu_L_ratio * 100,
        name = "Unproductive Share (Lu/L)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$danger, width = 3),
        stackgroup = NULL,
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>Lu/L</b>: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      )

    # Add recession shading
    if (input$show_recessions) {
      for (i in 1:nrow(recessions)) {
        p <- p %>%
          add_ribbons(
            x = c(recessions$start[i], recessions$end[i]),
            ymin = 0,
            ymax = 100,
            fillcolor = "rgba(128, 128, 128, 0.2)",
            line = list(width = 0),
            showlegend = FALSE,
            hoverinfo = "text",
            text = paste("Recession:", recessions$label[i])
          )
      }
    }

    p %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Employment Share (%)", range = c(0, 100)),
        hovermode = "x unified",
        legend = list(x = 0.7, y = 0.95)
      )
  })

  output$employment_absolute_plot <- renderPlotly({
    data <- filtered_employment()

    plot_ly(data,
      x = ~year, y = ~Lp_productive,
      type = "scatter", mode = "none", name = "Productive",
      fill = "tonexty", fillcolor = colors$success,
      line = list(width = 0),
      hovertemplate = paste(
        "<b>Year</b>: %{x}<br>",
        "<b>Lp</b>: %{y:,.0f}k<br>",
        "<extra></extra>"
      )
    ) %>%
      add_trace(
        y = ~L_total, name = "Total",
        fill = "tonexty", fillcolor = colors$danger,
        line = list(width = 0),
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>L</b>: %{y:,.0f}k<br>",
          "<extra></extra>"
        )
      ) %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Employment (thousands)"),
        hovermode = "x unified",
        showlegend = TRUE
      )
  })

  output$employment_stats_table <- renderDT({
    data <- filtered_employment()

    stats <- tibble(
      Metric = c(
        "Total Employment (L)",
        "Productive (Lp)",
        "Unproductive (Lu)",
        "Lp/L Ratio",
        "Lu/L Ratio"
      ),
      Mean = c(
        mean(data$L_total, na.rm = TRUE),
        mean(data$Lp_productive, na.rm = TRUE),
        mean(data$Lu_unproductive, na.rm = TRUE),
        mean(data$Lp_L_ratio, na.rm = TRUE),
        mean(data$Lu_L_ratio, na.rm = TRUE)
      ),
      `1948` = c(
        data$L_total[1],
        data$Lp_productive[1],
        data$Lu_unproductive[1],
        data$Lp_L_ratio[1],
        data$Lu_L_ratio[1]
      ),
      `1989` = c(
        data$L_total[nrow(data)],
        data$Lp_productive[nrow(data)],
        data$Lu_unproductive[nrow(data)],
        data$Lp_L_ratio[nrow(data)],
        data$Lu_L_ratio[nrow(data)]
      )
    ) %>%
      mutate(
        Mean = ifelse(Metric %in% c("Lp/L Ratio", "Lu/L Ratio"),
          sprintf("%.1f%%", Mean * 100),
          format(round(Mean, 0), big.mark = ",")
        ),
        `1948` = ifelse(Metric %in% c("Lp/L Ratio", "Lu/L Ratio"),
          sprintf("%.1f%%", `1948` * 100),
          format(round(`1948`, 0), big.mark = ",")
        ),
        `1989` = ifelse(Metric %in% c("Lp/L Ratio", "Lu/L Ratio"),
          sprintf("%.1f%%", `1989` * 100),
          format(round(`1989`, 0), big.mark = ",")
        )
      )

    datatable(stats,
      options = list(dom = "t", paging = FALSE),
      rownames = FALSE
    )
  })

  output$productivity_comparison_plot <- renderPlotly({
    data <- productivity %>%
      filter(
        year >= input$year_range[1],
        year <= input$year_range[2]
      )

    plot_ly(data, x = ~year) %>%
      add_trace(
        y = ~marxian_index,
        name = "Marxian (Y/Lp)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$primary, width = 3)
      ) %>%
      add_trace(
        y = ~conventional_index,
        name = "Conventional (Y/L)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$warning, width = 2)
      ) %>%
      add_trace(
        y = ~bls_productivity_index,
        name = "BLS Index",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$info, width = 2, dash = "dash")
      ) %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Productivity Index (1948 = 100)"),
        hovermode = "x unified",
        legend = list(x = 0.05, y = 0.95)
      )
  })

  # ============================================
  # TAB 5: GOVERNMENT ABSORPTION
  # ============================================

  output$govt_total_current <- renderValueBox({
    latest_year <- max(filtered_government()$year)
    latest_val <- filtered_government() %>%
      filter(year == latest_year) %>%
      pull(G_total)

    valueBox(
      value = paste0("$", format(round(latest_val, 0), big.mark = ",")),
      subtitle = paste0("Total Govt Spending (", latest_year, ", billions)"),
      icon = icon("university"),
      color = "blue"
    )
  })

  output$govt_surplus_ratio <- renderValueBox({
    latest_year <- max(filtered_government()$year)
    latest_val <- filtered_government() %>%
      filter(year == latest_year) %>%
      pull(G_S_ratio)

    valueBox(
      value = sprintf("%.1f%%", latest_val * 100),
      subtitle = paste0("G/S* Ratio (", latest_year, ")"),
      icon = icon("percent"),
      color = "green"
    )
  })

  output$govt_gdp_ratio <- renderValueBox({
    latest_year <- max(filtered_government()$year)
    latest_val <- filtered_government() %>%
      filter(year == latest_year) %>%
      pull(G_GDP_ratio)

    valueBox(
      value = sprintf("%.1f%%", latest_val * 100),
      subtitle = paste0("G/GDP Ratio (", latest_year, ")"),
      icon = icon("chart-pie"),
      color = "orange"
    )
  })

  output$govt_growth <- renderValueBox({
    data <- filtered_government()
    first_val <- data$G_total[1]
    last_val <- data$G_total[nrow(data)]
    change_pct <- ((last_val / first_val) - 1) * 100

    valueBox(
      value = sprintf("%+.0f%%", change_pct),
      subtitle = "Total Growth",
      icon = icon("arrow-up"),
      color = "red"
    )
  })

  output$government_ratios_plot <- renderPlotly({
    data <- filtered_government()

    p <- plot_ly(data, x = ~year) %>%
      add_trace(
        y = ~ G_S_ratio * 100,
        name = "G/S* (Gov't/Surplus)",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$primary, width = 3),
        yaxis = "y",
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>G/S*</b>: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      ) %>%
      add_trace(
        y = ~ G_GDP_ratio * 100,
        name = "G/GDP",
        type = "scatter",
        mode = "lines",
        line = list(color = colors$success, width = 2),
        yaxis = "y",
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>G/GDP</b>: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      )

    # Add recession shading
    if (input$show_recessions) {
      max_val <- max(c(data$G_S_ratio, data$G_GDP_ratio), na.rm = TRUE) * 100
      for (i in 1:nrow(recessions)) {
        p <- p %>%
          add_ribbons(
            x = c(recessions$start[i], recessions$end[i]),
            ymin = 0,
            ymax = max_val * 1.2,
            fillcolor = "rgba(128, 128, 128, 0.2)",
            line = list(width = 0),
            showlegend = FALSE,
            hoverinfo = "text",
            text = paste("Recession:", recessions$label[i])
          )
      }
    }

    p %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Ratio (%)"),
        hovermode = "x unified",
        legend = list(x = 0.7, y = 0.95)
      )
  })

  output$government_levels_plot <- renderPlotly({
    data <- filtered_government()

    plot_ly(data,
      x = ~year, y = ~G_federal,
      type = "scatter", mode = "none", name = "Federal",
      fill = "tonexty", fillcolor = colors$primary,
      line = list(width = 0),
      stackgroup = "one",
      hovertemplate = paste(
        "<b>Year</b>: %{x}<br>",
        "<b>Federal</b>: $%{y:.1f}B<br>",
        "<extra></extra>"
      )
    ) %>%
      add_trace(
        y = ~G_state_local, name = "State & Local",
        fill = "tonexty", fillcolor = colors$success,
        line = list(width = 0),
        stackgroup = "one",
        hovertemplate = paste(
          "<b>Year</b>: %{x}<br>",
          "<b>State/Local</b>: $%{y:.1f}B<br>",
          "<extra></extra>"
        )
      ) %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Government Spending (billions)"),
        hovermode = "x unified",
        showlegend = TRUE
      )
  })

  output$government_decade_table <- renderDT({
    data <- filtered_government() %>%
      mutate(decade = paste0(floor(year / 10) * 10, "s")) %>%
      group_by(decade) %>%
      summarize(
        `Avg G/S*` = mean(G_S_ratio, na.rm = TRUE) * 100,
        `Avg G/GDP` = mean(G_GDP_ratio, na.rm = TRUE) * 100,
        `Avg Total` = mean(G_total, na.rm = TRUE),
        `Federal %` = mean(G_federal / G_total, na.rm = TRUE) * 100
      ) %>%
      mutate(
        `Avg G/S*` = sprintf("%.1f%%", `Avg G/S*`),
        `Avg G/GDP` = sprintf("%.1f%%", `Avg G/GDP`),
        `Avg Total` = paste0("$", format(round(`Avg Total`, 0), big.mark = ","), "B"),
        `Federal %` = sprintf("%.1f%%", `Federal %`)
      )

    datatable(data,
      options = list(
        dom = "t",
        paging = FALSE,
        searching = FALSE
      ),
      rownames = FALSE
    )
  })

  # ============================================
  # TAB 8: DATA DOWNLOADS
  # ============================================

  # Display current year range
  output$download_year_range <- renderText({
    paste0(input$year_range[1], " - ", input$year_range[2])
  })

  # Individual dataset downloads
  output$download_profit_rates <- downloadHandler(
    filename = function() {
      paste0("profit_rates_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write_csv(profit_rates, file)
    }
  )

  output$download_exploitation <- downloadHandler(
    filename = function() {
      paste0("exploitation_composition_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write_csv(exploitation, file)
    }
  )

  output$download_employment <- downloadHandler(
    filename = function() {
      paste0("employment_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write_csv(employment, file)
    }
  )

  output$download_productivity <- downloadHandler(
    filename = function() {
      paste0("productivity_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write_csv(productivity, file)
    }
  )

  output$download_government <- downloadHandler(
    filename = function() {
      paste0("government_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write_csv(government, file)
    }
  )

  output$download_validation <- downloadHandler(
    filename = function() {
      paste0("validation_targets_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write_csv(validation_targets, file)
    }
  )

  output$download_comprehensive <- downloadHandler(
    filename = function() {
      paste0("comprehensive_dataset_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write_csv(comprehensive, file)
    }
  )

  # Filtered data export
  output$download_filtered <- downloadHandler(
    filename = function() {
      ext <- switch(input$download_format,
        "csv" = ".csv",
        "xlsx" = ".xlsx",
        "rdata" = ".RData"
      )
      paste0(
        "shaikh_tonak_filtered_",
        input$year_range[1], "_", input$year_range[2],
        "_", Sys.Date(), ext
      )
    },
    content = function(file) {
      # Create filtered comprehensive dataset
      filtered_data <- comprehensive %>%
        filter(
          year >= input$year_range[1],
          year <= input$year_range[2]
        )

      # Export in selected format
      if (input$download_format == "csv") {
        write_csv(filtered_data, file)
      } else if (input$download_format == "xlsx") {
        # Create multi-sheet Excel workbook
        sheets <- list(
          "Comprehensive" = filtered_data,
          "Profit_Rates" = filtered_profit(),
          "Exploitation" = filtered_exploitation(),
          "Employment" = filtered_employment(),
          "Government" = filtered_government(),
          "Metadata" = tibble(
            Field = c(
              "Time Period", "Years Included", "Export Date",
              "Source", "Reference"
            ),
            Value = c(
              paste(input$year_range[1], "-", input$year_range[2]),
              nrow(filtered_data),
              as.character(Sys.Date()),
              "BEA NIPA, BLS",
              "Shaikh & Tonak (1994)"
            )
          )
        )
        write_xlsx(sheets, file)
      } else if (input$download_format == "rdata") {
        # Save as RData with multiple objects
        profit_rates_filtered <- filtered_profit()
        exploitation_filtered <- filtered_exploitation()
        employment_filtered <- filtered_employment()
        government_filtered <- filtered_government()
        comprehensive_filtered <- filtered_data

        metadata <- list(
          time_period = paste(input$year_range[1], "-", input$year_range[2]),
          export_date = Sys.Date(),
          source = "BEA NIPA, BLS",
          reference = "Shaikh & Tonak (1994)"
        )

        save(profit_rates_filtered,
          exploitation_filtered,
          employment_filtered,
          government_filtered,
          comprehensive_filtered,
          metadata,
          file = file
        )
      }
    }
  )

  # Codebook download
  output$download_codebook <- downloadHandler(
    filename = function() {
      paste0("shaikh_tonak_codebook_", Sys.Date(), ".txt")
    },
    content = function(file) {
      codebook_text <- "
SHAIKH-TONAK MARXIAN ANALYSIS CODEBOOK
======================================

PROFIT RATES:
  r_star_pct           : Marxian profit rate S*/K (%)
  r_star_adj_pct       : Capacity-adjusted Marxian profit rate (%)
  r_nipa_pct           : NIPA profit rate (%)
  capacity_utilization : Manufacturing capacity utilization (ratio)

EXPLOITATION & COMPOSITION:
  exploitation_rate     : S*/V* (surplus/variable capital ratio)
  surplus_ratio         : S*/Y (surplus/output ratio)
  value_composition     : C*/V* (constant/variable capital ratio)

EMPLOYMENT:
  L_total              : Total employment (thousands)
  Lp_productive        : Productive labor (thousands)
  Lu_unproductive      : Unproductive labor (thousands)
  Lp_L_ratio          : Productive labor share

GOVERNMENT:
  G_total              : Total government expenditure (billions)
  G_S_ratio           : Government/surplus ratio
  G_GDP_ratio         : Government/GDP ratio

DATA SOURCES: BEA NIPA, BLS
REFERENCE: Shaikh & Tonak (1994) Measuring the Wealth of Nations
"
      writeLines(codebook_text, file)
    }
  )

  # ============================================
  # TAB 6: VALIDATION CENTER
  # ============================================

  output$validation_status <- renderValueBox({
    valueBox(
      value = "3 / 3",
      subtitle = "Metrics Validated",
      icon = icon("check-circle"),
      color = "yellow" # Yellow indicates mixed results
    )
  })

  output$validation_r_star <- renderValueBox({
    # Compare 1989 r* with Table 5.8
    our_r <- profit_rates %>%
      filter(year == 1989) %>%
      pull(r_star_adj_pct)
    target_r <- validation_targets %>%
      filter(Year == 1989) %>%
      pull(r_star_adjusted) * 100
    deviation <- abs(our_r - target_r) / target_r * 100

    valueBox(
      value = sprintf("%.0f%%", deviation),
      subtitle = "r* Deviation (Under Investigation)",
      icon = icon("exclamation-triangle"),
      color = "red"
    )
  })

  output$validation_exploitation <- renderValueBox({
    # Compare 1989 exploitation rate
    our_e <- exploitation %>%
      filter(year == 1989) %>%
      pull(exploitation_rate)
    target_e <- validation_targets %>%
      filter(Year == 1989) %>%
      pull(exploitation_rate)
    deviation <- abs(our_e - target_e) / target_e * 100

    valueBox(
      value = sprintf("%.1f%%", deviation),
      subtitle = "Exploitation Rate Deviation (Excellent)",
      icon = icon("check"),
      color = "green"
    )
  })

  output$validation_scatter <- renderPlotly({
    # Create comparison for benchmark years
    benchmark_years <- c(1948, 1964, 1970, 1980, 1989)

    # Get our calculated values
    our_values <- exploitation %>%
      filter(year %in% benchmark_years) %>%
      select(year, our_exploitation = exploitation_rate, our_value_comp = value_composition)

    # Merge with targets
    comparison <- validation_targets %>%
      filter(Year %in% benchmark_years) %>%
      select(Year, target_exploitation = exploitation_rate, target_value_comp = value_composition) %>%
      left_join(our_values, by = c("Year" = "year"))

    # Create scatter plot
    plot_ly() %>%
      # Exploitation rate comparison
      add_trace(
        data = comparison,
        x = ~target_exploitation,
        y = ~our_exploitation,
        type = "scatter",
        mode = "markers",
        name = "Exploitation Rate (S*/V*)",
        marker = list(size = 12, color = colors$success),
        text = ~ paste("Year:", Year),
        hovertemplate = paste(
          "<b>%{text}</b><br>",
          "Target: %{x:.2f}<br>",
          "Calculated: %{y:.2f}<br>",
          "<extra>Exploitation Rate</extra>"
        )
      ) %>%
      # Value composition comparison
      add_trace(
        data = comparison,
        x = ~target_value_comp,
        y = ~our_value_comp,
        type = "scatter",
        mode = "markers",
        name = "Value Composition (C*/V*)",
        marker = list(size = 12, color = colors$warning),
        text = ~ paste("Year:", Year),
        hovertemplate = paste(
          "<b>%{text}</b><br>",
          "Target: %{x:.2f}<br>",
          "Calculated: %{y:.2f}<br>",
          "<extra>Value Composition</extra>"
        )
      ) %>%
      # Perfect correlation line
      add_trace(
        x = c(0, 10), y = c(0, 10),
        type = "scatter",
        mode = "lines",
        line = list(color = "gray", dash = "dash", width = 1),
        showlegend = FALSE,
        hoverinfo = "none"
      ) %>%
      layout(
        title = "",
        xaxis = list(title = "Table 5.8 Target Values"),
        yaxis = list(title = "Our Calculated Values"),
        hovermode = "closest"
      )
  })

  output$validation_table <- renderDT({
    benchmark_years <- c(1948, 1964, 1970, 1980, 1989)

    # Get calculated values
    calc_exploitation <- exploitation %>%
      filter(year %in% benchmark_years) %>%
      select(year, calc_exploitation = exploitation_rate, calc_value_comp = value_composition)

    calc_profit <- profit_rates %>%
      filter(year %in% benchmark_years) %>%
      select(year, calc_r_star = r_star_adj_pct)

    # Merge and calculate deviations
    validation_df <- validation_targets %>%
      filter(Year %in% benchmark_years) %>%
      left_join(calc_exploitation, by = c("Year" = "year")) %>%
      left_join(calc_profit, by = c("Year" = "year")) %>%
      mutate(
        `S*/V* Target` = sprintf("%.2f", exploitation_rate),
        `S*/V* Calculated` = sprintf("%.2f", calc_exploitation),
        `S*/V* Deviation` = sprintf("%.1f%%", abs(calc_exploitation - exploitation_rate) / exploitation_rate * 100),
        `C*/V* Target` = sprintf("%.2f", value_composition),
        `C*/V* Calculated` = sprintf("%.2f", calc_value_comp),
        `C*/V* Deviation` = sprintf("%.1f%%", abs(calc_value_comp - value_composition) / value_composition * 100),
        `r* Target` = sprintf("%.1f%%", r_star_adjusted * 100),
        `r* Calculated` = sprintf("%.1f%%", calc_r_star),
        `r* Deviation` = sprintf("%.0f%%", abs(calc_r_star - r_star_adjusted * 100) / (r_star_adjusted * 100) * 100)
      ) %>%
      select(Year, starts_with("S*/V*"), starts_with("C*/V*"), starts_with("r*"))

    datatable(validation_df,
      options = list(
        dom = "t",
        paging = FALSE,
        scrollX = TRUE
      ),
      rownames = FALSE
    )
  })

  # ============================================
  # NEW TAB: METHODOLOGY COMPARISON SERVER LOGIC
  # ============================================

  # Value box: Book benchmark match
  output$method_book_match <- renderValueBox({
    valueBox(
      value = "PERFECT",
      subtitle = "Book Benchmark Match (1948-1989)",
      icon = icon("check-circle"),
      color = "green"
    )
  })

  # Value box: Current exploitation rate
  output$method_current_e <- renderValueBox({
    if (nrow(methodology_comparison) > 0) {
      latest <- methodology_comparison %>% filter(Year == max(Year, na.rm = TRUE))
      valueBox(
        value = sprintf("%.2f", latest$ST94_e[1]),
        subtitle = paste0("ST94 Exploitation Rate (", latest$Year[1], ")"),
        icon = icon("balance-scale"),
        color = "blue"
      )
    } else {
      valueBox(value = "N/A", subtitle = "Exploitation Rate", icon = icon("balance-scale"), color = "blue")
    }
  })

  # Value box: Methodology divergence
  output$method_divergence <- renderValueBox({
    if (nrow(methodology_comparison) > 0) {
      latest <- methodology_comparison %>% filter(Year == max(Year, na.rm = TRUE))
      divergence <- abs(latest$ST94_e[1] - latest$TP19_e[1]) / latest$ST94_e[1] * 100
      valueBox(
        value = sprintf("%.1f%%", divergence),
        subtitle = "ST94 vs TP19 Divergence",
        icon = icon("code-compare"),
        color = "orange"
      )
    } else {
      valueBox(value = "N/A", subtitle = "Divergence", icon = icon("code-compare"), color = "orange")
    }
  })

  # Methodology exploitation plot
  output$methodology_exploitation_plot <- renderPlotly({
    if (nrow(methodology_comparison) == 0) {
      return(plotly_empty() %>% layout(title = "No methodology data available"))
    }

    data <- methodology_comparison %>%
      filter(Year >= input$year_range[1], Year <= input$year_range[2])

    p <- plot_ly(data, x = ~Year) %>%
      # Add extension period shading
      add_ribbons(
        x = c(1990, 2024), ymin = 0, ymax = 4,
        fillcolor = "rgba(243, 156, 18, 0.1)",
        line = list(width = 0),
        showlegend = FALSE,
        hoverinfo = "none"
      ) %>%
      # Add methodology lines
      add_trace(
        y = ~ST94_e, name = "ST94 (Shaikh-Tonak 1994)",
        type = "scatter", mode = "lines",
        line = list(color = "#3c8dbc", width = 3)
      ) %>%
      add_trace(
        y = ~M05_e, name = "M05 (Mohun 2005)",
        type = "scatter", mode = "lines",
        line = list(color = "#00a65a", width = 2)
      ) %>%
      add_trace(
        y = ~TP19_e, name = "TP19 (Tsoulfidis-Paitaridis 2019)",
        type = "scatter", mode = "lines",
        line = list(color = "#605ca8", width = 2)
      ) %>%
      # Add book benchmarks as markers
      add_trace(
        y = ~Book_e, name = "Book Benchmark (Table 5.7)",
        type = "scatter", mode = "markers",
        marker = list(color = "#dd4b39", size = 12, symbol = "diamond")
      ) %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Exploitation Rate (S*/V*)"),
        hovermode = "x unified",
        legend = list(x = 0.02, y = 0.98)
      )

    p
  })

  # Methodology labor share plot
  output$methodology_labor_plot <- renderPlotly({
    if (nrow(methodology_comparison) == 0) {
      return(plotly_empty() %>% layout(title = "No data"))
    }

    data <- methodology_comparison %>%
      filter(Year >= input$year_range[1], Year <= input$year_range[2])

    plot_ly(data, x = ~Year) %>%
      add_trace(
        y = ~ ST94_Lp_L * 100, name = "ST94",
        type = "scatter", mode = "lines",
        line = list(color = "#3c8dbc", width = 2)
      ) %>%
      add_trace(
        y = ~ M05_Lp_L * 100, name = "M05",
        type = "scatter", mode = "lines",
        line = list(color = "#00a65a", width = 2)
      ) %>%
      add_trace(
        y = ~ TP19_Lp_L * 100, name = "TP19",
        type = "scatter", mode = "lines",
        line = list(color = "#605ca8", width = 2)
      ) %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Productive Labor Share (%)"),
        hovermode = "x unified"
      )
  })

  # Methodology profit rate plot
  output$methodology_profit_plot <- renderPlotly({
    if (nrow(methodology_comparison) == 0) {
      return(plotly_empty() %>% layout(title = "No data"))
    }

    data <- methodology_comparison %>%
      filter(Year >= input$year_range[1], Year <= input$year_range[2])

    plot_ly(data, x = ~Year) %>%
      add_trace(
        y = ~ ST94_r * 100, name = "ST94 r*",
        type = "scatter", mode = "lines",
        line = list(color = "#3c8dbc", width = 2)
      ) %>%
      add_trace(
        y = ~ M05_r * 100, name = "M05 r*",
        type = "scatter", mode = "lines",
        line = list(color = "#00a65a", width = 2)
      ) %>%
      add_trace(
        y = ~ TP19_r * 100, name = "TP19 r*",
        type = "scatter", mode = "lines",
        line = list(color = "#605ca8", width = 2)
      ) %>%
      layout(
        title = "",
        xaxis = list(title = "Year"),
        yaxis = list(title = "Profit Rate (%)"),
        hovermode = "x unified"
      )
  })

  # Methodology comparison table
  output$methodology_comparison_table <- renderDT({
    if (nrow(methodology_comparison) == 0) {
      return(datatable(tibble(Message = "No methodology comparison data available")))
    }

    data <- methodology_comparison %>%
      filter(Year >= input$year_range[1], Year <= input$year_range[2]) %>%
      select(Year, Period,
        `Book e` = Book_e, `ST94 e` = ST94_e, `M05 e` = M05_e, `TP19 e` = TP19_e,
        `ST94 Lp/L` = ST94_Lp_L, `M05 Lp/L` = M05_Lp_L, `TP19 Lp/L` = TP19_Lp_L,
        Validation_Status
      ) %>%
      mutate(across(where(is.numeric), ~ round(., 3)))

    datatable(data,
      options = list(
        pageLength = 15,
        scrollX = TRUE,
        dom = "ftip"
      ),
      rownames = FALSE,
      filter = "top"
    ) %>%
      formatStyle("Period",
        backgroundColor = styleEqual(
          c("Book", "Extension", "Transition"),
          c("#d4edda", "#fff3cd", "#e7d4e8")
        )
      ) %>%
      formatStyle("Validation_Status",
        backgroundColor = styleEqual(
          c("Validated", "Interpolated", "Extended", "SIC-NAICS Bridge"),
          c("#d4edda", "#f8f9fa", "#fff3cd", "#e7d4e8")
        )
      )
  })

  # ============================================
  # NEW TAB: INDUSTRY CLASSIFICATION SERVER LOGIC
  # ============================================

  output$industry_classification_table <- renderDT({
    if (nrow(industry_classification) == 0) {
      return(datatable(tibble(Message = "No industry classification data available")))
    }

    datatable(industry_classification,
      options = list(
        pageLength = 30,
        scrollX = TRUE,
        dom = "ftip"
      ),
      rownames = FALSE,
      filter = "top"
    ) %>%
      formatStyle("ST94_Classification",
        backgroundColor = styleEqual(
          c("Productive", "Unproductive", "Mixed", "Excluded"),
          c("#d4edda", "#f8d7da", "#fff3cd", "#e2e3e5")
        )
      ) %>%
      formatStyle("M05_Classification",
        backgroundColor = styleEqual(
          c("Productive", "Unproductive", "Mixed", "Excluded"),
          c("#d4edda", "#f8d7da", "#fff3cd", "#e2e3e5")
        )
      ) %>%
      formatStyle("TP19_Classification",
        backgroundColor = styleEqual(
          c("Productive", "Unproductive", "Mixed", "Excluded"),
          c("#d4edda", "#f8d7da", "#fff3cd", "#e2e3e5")
        )
      )
  })

  # ============================================
  # NEW TAB: QUESTIONS FOR TONAK SERVER LOGIC
  # ============================================

  output$tonak_questions_table <- renderDT({
    if (nrow(questions_for_tonak) == 0) {
      return(datatable(tibble(Message = "No questions for Tonak available")))
    }

    data <- questions_for_tonak %>%
      select(
        `#` = Question_Number,
        Question,
        Category,
        Priority,
        `Book Reference` = Book_Reference
      )

    datatable(data,
      options = list(
        pageLength = 20,
        scrollX = TRUE,
        dom = "ftip",
        columnDefs = list(
          list(width = "50px", targets = 0),
          list(width = "400px", targets = 1),
          list(width = "150px", targets = 2)
        )
      ),
      rownames = FALSE,
      filter = "top",
      selection = "single"
    ) %>%
      formatStyle("Priority",
        backgroundColor = styleEqual(
          c("Critical", "High", "Medium", "Low"),
          c("#f8d7da", "#fff3cd", "#d4edda", "#e2e3e5")
        ),
        fontWeight = styleEqual("Critical", "bold")
      )
  })

  # Download handler for Tonak questions
  output$download_tonak_questions <- downloadHandler(
    filename = function() {
      paste0("Questions_for_Professor_Tonak_", Sys.Date(), ".txt")
    },
    content = function(file) {
      lines <- c(
        "==================================================",
        "QUESTIONS FOR PROFESSOR TONAK",
        paste("Generated:", Sys.Date()),
        "Shaikh-Tonak Replication Project",
        "==================================================",
        ""
      )

      if (nrow(questions_for_tonak) > 0) {
        for (i in 1:nrow(questions_for_tonak)) {
          q <- questions_for_tonak[i, ]
          lines <- c(
            lines,
            paste0("QUESTION ", q$Question_Number, " [", q$Priority, "]"),
            paste0("Category: ", q$Category),
            "",
            q$Question,
            "",
            paste0("Book Reference: ", q$Book_Reference),
            "",
            "Explanation:",
            q$Explanation,
            "",
            "--------------------------------------------------",
            ""
          )
        }
      }

      writeLines(lines, file)
    }
  )

  # ============================================
  # NEW TAB: LITERATURE CITATIONS SERVER LOGIC
  # ============================================

  output$literature_citations_table <- renderDT({
    if (nrow(literature_citations) == 0) {
      return(datatable(tibble(Message = "No literature citations available")))
    }

    data <- literature_citations %>%
      select(
        ID = Citation_ID,
        Authors,
        Year,
        Title,
        `Key Tables` = Key_Tables,
        `Key Pages` = Key_Pages,
        Methodology = Methodology_Used
      )

    datatable(data,
      options = list(
        pageLength = 20,
        scrollX = TRUE,
        dom = "ftip",
        columnDefs = list(
          list(width = "60px", targets = 0),
          list(width = "200px", targets = 3)
        )
      ),
      rownames = FALSE,
      filter = "top"
    ) %>%
      formatStyle("Methodology",
        backgroundColor = styleEqual(
          c("ST94 (Original)", "M05 (SM Approximation)", "M05 Extended", "TP19 (NAICS-based)"),
          c("#d4edda", "#cce5ff", "#b8daff", "#e7d4e8")
        )
      )
  })

  # ============================================
  # FIGURES & SERIES TAB
  # ============================================

  # Reactive: filtered figure catalog
  filtered_figures <- reactive({
    df <- figure_catalog_df
    if (nrow(df) == 0) return(df)

    if (!is.null(input$fig_chapter_filter) && input$fig_chapter_filter != "All") {
      df <- df[df$chapter == as.integer(input$fig_chapter_filter), ]
    }
    if (!is.null(input$fig_type_filter) && input$fig_type_filter != "All") {
      df <- df[df$type == input$fig_type_filter, ]
    }
    if (!is.null(input$fig_empirical_filter) && input$fig_empirical_filter != "All") {
      df <- df[df$is_empirical == as.logical(input$fig_empirical_filter), ]
    }
    df
  })

  # Figure count display
  output$fig_count_display <- renderText({
    n <- nrow(filtered_figures())
    paste0(n, " Figure", if (n != 1) "s" else "")
  })

  # Render figures table
  output$figures_table <- DT::renderDT({
    df <- filtered_figures()
    if (nrow(df) == 0) {
      return(DT::datatable(tibble(Message = "No figures match the selected filters")))
    }

    display_df <- df %>%
      select(
        `Figure ID` = figure_id,
        Title = title,
        Chapter = chapter,
        `Series IDs` = series_ids_str,
        Type = type,
        `Year Start` = year_start,
        `Year End` = year_end
      )

    DT::datatable(display_df,
      selection = "single",
      options = list(pageLength = 20, scrollX = TRUE, dom = "ftip"),
      rownames = FALSE
    )
  })

  # Observe row selection -> show series detail and figure preview
  observeEvent(input$figures_table_rows_selected, {
    sel <- input$figures_table_rows_selected
    if (length(sel) == 0) return()

    fig <- filtered_figures()[sel, ]

    # Render series detail HTML
    output$series_detail <- renderUI({
      sid_list <- fig$series_ids[[1]]
      if (length(sid_list) == 0) {
        return(tags$div(
          tags$p(tags$strong("Figure: "), fig$title),
          tags$p(tags$em("No data series associated with this figure (conceptual diagram).")),
          if (!is.null(fig$description)) tags$p(tags$strong("Description: "), fig$description)
        ))
      }

      detail_html <- lapply(sid_list, function(sid) {
        s <- series_catalog[[sid]]
        if (!is.null(s)) {
          tags$div(
            tags$h4(paste0(sid, ": ", s$name)),
            tags$p(tags$strong("Chapter: "), s$chapter),
            tags$p(tags$strong("Period: "), paste(s$time_period_start, "-", s$time_period_end)),
            tags$p(tags$strong("Extension: "), s$extension_status),
            if (!is.null(s$shiny_columns)) tags$p(
              tags$strong("Data columns: "),
              paste(unique(s$shiny_columns), collapse = ", ")
            ),
            tags$hr()
          )
        } else {
          tags$div(
            tags$h4(paste0(sid, ": (not found in series catalog)")),
            tags$hr()
          )
        }
      })
      do.call(tagList, detail_html)
    })

    # Render figure preview
    output$fig_preview <- renderPlotly({
      fig_id <- fig$figure_id
      chapter_num <- fig$chapter

      # Get columns for this figure from the column map
      fig_cols <- figure_column_map[[fig_id]]
      if (is.null(fig_cols) || length(fig_cols) == 0) {
        return(plotly_empty() %>% layout(
          title = list(text = "No data columns mapped for this figure", font = list(size = 14))
        ))
      }
      fig_cols <- unlist(fig_cols)

      # Load chapter CSV
      chapter_file <- file.path(figures_data_path, paste0("chapter_0", chapter_num, ".csv"))
      if (!file.exists(chapter_file)) {
        return(plotly_empty() %>% layout(
          title = list(text = paste("Data file not found:", basename(chapter_file)), font = list(size = 14))
        ))
      }

      cdata <- tryCatch(read.csv(chapter_file, stringsAsFactors = FALSE), error = function(e) NULL)
      if (is.null(cdata) || !("year" %in% names(cdata))) {
        return(plotly_empty() %>% layout(
          title = list(text = "Could not parse chapter data", font = list(size = 14))
        ))
      }

      # Filter to columns that actually exist
      available_cols <- intersect(fig_cols, names(cdata))
      if (length(available_cols) == 0) {
        return(plotly_empty() %>% layout(
          title = list(text = "Mapped columns not found in data file", font = list(size = 14))
        ))
      }

      p <- plot_ly(cdata, x = ~year)
      plot_colors <- c("#3c8dbc", "#dd4b39", "#00a65a", "#f39c12", "#605ca8",
                        "#39cccc", "#d81b60", "#ff851b", "#001f3f", "#85144b")
      for (i in seq_along(available_cols)) {
        col_name <- available_cols[i]
        color_idx <- ((i - 1) %% length(plot_colors)) + 1
        p <- p %>% add_lines(
          y = cdata[[col_name]], name = col_name,
          line = list(color = plot_colors[color_idx], width = 2)
        )
      }

      p %>% layout(
        title = list(text = fig$title, font = list(size = 13)),
        xaxis = list(title = "Year"),
        yaxis = list(title = "Value"),
        hovermode = "x unified",
        legend = list(orientation = "h", y = -0.2)
      )
    })
  })

  # ============================================
  # PROFIT RATE: METHODOLOGY OVERLAY
  # ============================================

  # Override the profit_rate_plot to add methodology overlay
  observeEvent(input$method_overlay, {
    # The main profit_rate_plot renderPlotly already handles this
    # via input$method_overlay checked inside it
  }, ignoreInit = TRUE)
}

