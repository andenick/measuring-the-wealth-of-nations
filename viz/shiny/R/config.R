# RMWND Shiny — Path Configuration
# Paths are relative to the shiny/ directory

VIZ_DIR <- normalizePath(file.path(".."), mustWork = FALSE) # Technical/viz/

RMWND_PATHS <- list(
  config             = file.path(VIZ_DIR, "config", "app_config.json"),
  style              = file.path(VIZ_DIR, "viz_style.json"),
  registry           = normalizePath(file.path(VIZ_DIR, "..", "series_registry.json"), mustWork = FALSE),
  chopped_dir        = normalizePath(file.path(VIZ_DIR, "..", "chopped"), mustWork = FALSE),
  catalog            = file.path(VIZ_DIR, "data", "catalogs", "DEFINITIVE_SERIES_CATALOG.json"),
  subsource_metadata = file.path(VIZ_DIR, "data", "catalogs", "SUBSOURCE_METADATA.json"),
  series_linkage     = file.path(VIZ_DIR, "data", "catalogs", "SERIES_SOURCE_LINKAGE.json"),
  quotes             = file.path(VIZ_DIR, "data", "catalogs", "RMWND_QUOTES_MASTER.json"),
  manifest           = file.path(VIZ_DIR, "data", "DATA_MANIFEST.json"),
  pipeline_state     = normalizePath(file.path(VIZ_DIR, "..", "PIPELINE_STATE.json"), mustWork = FALSE),
  ledger             = normalizePath(file.path(VIZ_DIR, "..", "ANU_LEDGER.json"), mustWork = FALSE),
  step_log           = normalizePath(file.path(VIZ_DIR, "..", "Build", "STEP_LOG.jsonl"), mustWork = FALSE)
)
