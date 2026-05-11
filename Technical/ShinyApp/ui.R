# =============================================================================
# UI DEFINITION
# =============================================================================
# Main UI object for the Shiny dashboard
# Tab definitions are in R/ui_tabs.R
# =============================================================================

# Source tab definitions
source("R/ui_tabs.R")

# Define UI
ui <- dashboardPage(
  title = "Shaikh-Tonak Marxian Analysis 1948-2024 - Professor Tonak Presentation",

  # ============================================
  # HEADER
  # ============================================
  dashboardHeader(
    title = "Shaikh-Tonak Analysis",
    titleWidth = 300
  ),

  # ============================================
  # SIDEBAR
  # ============================================
  ui_sidebar(),

  # ============================================
  # BODY
  # ============================================
  dashboardBody(
    # Custom CSS
    tags$head(
      tags$style(HTML("
        .info-box {
          min-height: 90px;
        }
        .info-box-icon {
          height: 90px;
          line-height: 90px;
        }
        .info-box-content {
          padding: 5px 10px;
          margin-left: 90px;
        }
        .small-box {
          border-radius: 5px;
        }
        .box {
          border-top: 3px solid #d2d6de;
        }
        .box.box-primary {
          border-top-color: #3c8dbc;
        }
        .box.box-success {
          border-top-color: #00a65a;
        }
        .box.box-warning {
          border-top-color: #f39c12;
        }
        .box.box-danger {
          border-top-color: #dd4b39;
        }

        /* Question Card Styles */
        .question-card {
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 15px;
          margin-bottom: 15px;
          background: white;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .question-card:hover {
          box-shadow: 0 4px 12px rgba(0,0,0,0.2);
          transform: translateY(-2px);
          border-color: #3c8dbc;
        }
        .question-card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 10px;
        }
        .question-number {
          font-size: 14px;
          font-weight: bold;
          color: #666;
        }
        .priority-badge {
          display: inline-block;
          padding: 3px 10px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: bold;
          text-transform: uppercase;
        }
        .priority-CRITICAL {
          background-color: #dd4b39;
          color: white;
        }
        .priority-HIGH {
          background-color: #f39c12;
          color: white;
        }
        .priority-MEDIUM {
          background-color: #00a65a;
          color: white;
        }
        .priority-LOW {
          background-color: #d2d6de;
          color: #666;
        }
        .question-text {
          font-size: 16px;
          font-weight: 600;
          color: #333;
          margin-bottom: 8px;
        }
        .question-category {
          font-size: 12px;
          color: #999;
          font-style: italic;
        }

        /* Modal Styles */
        .modal-content {
          border-radius: 8px;
        }
        .modal-header {
          background-color: #3c8dbc;
          color: white;
          border-radius: 8px 8px 0 0;
        }
        .modal-section {
          margin-bottom: 20px;
        }
        .modal-section h4 {
          color: #3c8dbc;
          border-bottom: 2px solid #3c8dbc;
          padding-bottom: 5px;
          margin-bottom: 10px;
        }
        .formula-box {
          background-color: #f4f4f4;
          border-left: 4px solid #3c8dbc;
          padding: 10px 15px;
          margin: 10px 0;
          font-family: 'Courier New', monospace;
          font-size: 14px;
        }
        .book-reference {
          background-color: #fffacd;
          border-left: 4px solid #f39c12;
          padding: 10px 15px;
          margin: 10px 0;
          font-style: italic;
        }
      "))
    ),
    tabItems(
      # Use tab functions from R/ui_tabs.R
      ui_tab_overview(),
      ui_tab_questions(),
      ui_tab_methodology(),
      ui_tab_figures_series(),
      ui_tab_profit_rate(),
      ui_tab_exploitation(),
      ui_tab_employment(),
      ui_tab_government(),
      ui_tab_io_analysis(),
      ui_tab_labor_values(),
      ui_tab_cross_study(),
      ui_tab_international(),
      ui_tab_validation(),
      ui_tab_literature(),
      ui_tab_downloads()
    )
  )
)
