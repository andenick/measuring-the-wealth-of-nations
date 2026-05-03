# =============================================================================
# SERVER DEFINITION
# =============================================================================
# Main server function for the Shiny dashboard
# Server logic is in R/server_logic.R
# =============================================================================

# Source server logic
source("R/server_logic.R")

# Define server function
server <- function(input, output, session) {
  app_server(input, output, session)
}
