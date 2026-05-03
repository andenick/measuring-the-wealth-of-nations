# config.R - Centralized path configuration for AS2 Shiny App
# All paths are relative to the ShinyApp root via here().
# This is the SINGLE SOURCE OF TRUTH for path resolution in AS2.
# Modeled on CD2/Technical/ShinyApp/R/config.R

library(here)

AS2_PATHS <- list(
  # ShinyApp root
  shiny_root     = here(),

  # Core data (Shiny app local data)
  data_root      = here("data"),

  # Inputs (project-level)
  inputs_root    = here("..", "..", "Inputs"),
  book_tables    = here("..", "..", "Inputs", "BookTables"),
  st_chopped     = here("..", "..", "Inputs", "ST_Chopped"),
  api_data       = here("..", "..", "Inputs", "API_Data"),
  io_matrices    = here("..", "..", "Inputs", "IO_Matrices"),
  concordances   = here("..", "..", "Inputs", "Concordances"),

  # Knowledge Base
  knowledge_base = here("..", "Knowledge_Base"),
  kb_tables      = here("..", "Knowledge_Base", "tables"),
  kb_equations   = here("..", "Knowledge_Base", "equations"),
  kb_text        = here("..", "Knowledge_Base", "text"),

  # Catalogs
  t_series_catalog   = here("..", "T_SERIES_CATALOG.json"),
  chopped_catalog    = here("..", "..", "Inputs", "ANU_CHOPPED_CATALOG.json"),

  # Outputs
  complete_db    = here("..", "..", "Outputs", "Data", "COMPLETE_DATABASE"),
  extenbooks     = here("..", "..", "Outputs", "Anu_Extenbooks"),
  figures_out    = here("..", "..", "Outputs", "Figures"),

  # Documentation
  docs_series    = here("..", "docs", "series"),
  docs_chapters  = here("..", "docs", "chapters")
)

# Verify critical paths exist at startup
.verify_as2_paths <- function() {
  critical <- c("data_root", "inputs_root", "knowledge_base")
  missing <- character(0)
  for (name in critical) {
    path <- AS2_PATHS[[name]]
    if (!file.exists(path)) {
      missing <- c(missing, paste0("  ", name, ": ", path))
    }
  }
  if (length(missing) > 0) {
    warning("AS2 config: missing critical paths:\n", paste(missing, collapse = "\n"))
  }
}

.verify_as2_paths()
