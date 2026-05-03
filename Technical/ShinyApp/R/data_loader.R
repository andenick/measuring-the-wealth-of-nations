# ============================================
# data_loader.R — Chapter 5 Series Mapping & Metadata Layer
# ============================================
# Provides CH5_SERIES_MAPPING and helper functions for the 16 T5xx series.
# This is a metadata layer; it does not replace the inline data loading in app.R.
# Full data loading migration is a future refactor.
#
# Anu Standard v2.0 — Series Mapping Component
# Created: 2026-02-24 (Session 7 — Gap Remediation G003)
# ============================================

# ============================================
# CH5_SERIES_MAPPING — Named list of all 16 T5xx series
# ============================================

CH5_SERIES_MAPPING <- list(

  T501 = list(
    name = "Total Product (TP*)",
    description = "Gross output of productive and trading sectors",
    formula = "TP* = GO_p + GO_t",
    data_patterns = c("ST_Chopped/ch05/TableE2_RevenueAccounts.csv"),
    subsources = c("NIPA 1.7.5", "BEA IO tables"),
    shaikh_finding = "TP* ~ 82% of IO gross product; ~1.5x GNP",
    book_table = "E.2",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T502 = list(
    name = "Constant Capital — Materials (C*_m)",
    description = "Intermediate inputs of productive sectors",
    formula = "C*_m = intermediate inputs of productive sectors",
    data_patterns = c("ST_Chopped/ch05/TableE2_RevenueAccounts.csv"),
    subsources = c("NIPA 1.7.5", "BEA IO benchmark tables"),
    shaikh_finding = "Material constant capital; basis for value composition",
    book_table = "E.2",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T503 = list(
    name = "Gross Final Product (GFP = TP* - C*_m)",
    description = "Marxian value added: total product minus material inputs",
    formula = "GFP = TP* - C*_m = T501 - T502",
    data_patterns = c("ST_Chopped/ch05/TableE2_RevenueAccounts.csv"),
    subsources = c("Derived from T501, T502"),
    shaikh_finding = "Marxian VA* differs from conventional value added by sector classification",
    book_table = "E.2",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T504 = list(
    name = "Variable Capital (V*)",
    description = "Compensation of productive workers",
    formula = "V* = W x (V*/W) = W x (Lp/L) x (ec_u/ec_p)",
    data_patterns = c(
      "ST_Chopped/ch05/ExploitationComposition_1948_1989.csv",
      "data/exploitation_composition_1948_2024.csv"
    ),
    subsources = c("NIPA 6.2D", "BLS CES production worker ratios"),
    shaikh_finding = "V* = productive worker wages; denominator of exploitation rate",
    book_table = "5.5",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T505 = list(
    name = "Surplus Value (S*)",
    description = "Marxian surplus: value added minus variable capital",
    formula = "S* = VA* - V* = T503 - T504",
    data_patterns = c(
      "ST_Chopped/ch05/ExploitationComposition_1948_1989.csv",
      "data/exploitation_composition_1948_2024.csv"
    ),
    subsources = c("Derived from T503, T504"),
    shaikh_finding = "S* ~ 2x conventional profit-type income",
    book_table = "5.5",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T506 = list(
    name = "Rate of Exploitation (e = S*/V*)",
    description = "Ratio of surplus value to variable capital",
    formula = "e = S*/V* = T505/T504",
    data_patterns = c(
      "ST_Chopped/ch05/Table5_7_KeyRatios.csv",
      "ST_Chopped/ch05/Table5_7_Extended.csv",
      "data/exploitation_composition_1948_2024.csv"
    ),
    subsources = c("Derived from T504, T505"),
    shaikh_finding = "e rose from 1.70 (1948) to 2.44 (1989); far exceeds conventional profit/wage ratio",
    book_table = "5.7",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = TRUE
  ),

  T507 = list(
    name = "Surplus Ratio (S*/Y)",
    description = "Share of surplus value in Marxian gross final product",
    formula = "S*/(S* + V*)",
    data_patterns = c("ST_Chopped/ch05/ExploitationComposition_1948_1989.csv"),
    subsources = c("Derived from T504, T505"),
    shaikh_finding = "Rising surplus share reflects increasing exploitation",
    book_table = "5.7",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T508 = list(
    name = "Productive Consumption (CON*)",
    description = "Consumption of productive workers adjusted for royalties",
    formula = "CON* = CON - GVA_ir - RY_con + HH_con - ROW_con",
    data_patterns = c("ST_Chopped/ch05/TableE2_RevenueAccounts.csv"),
    subsources = c("NIPA 1.1.5 line 2", "Appendix D/E adjustments"),
    shaikh_finding = "Marxian consumption excludes fictitious income imputations",
    book_table = "E.2",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T509 = list(
    name = "Productive Investment (IG*)",
    description = "Gross investment adjusted for royalties and building rent",
    formula = "IG* = IG - RY_i + ABR",
    data_patterns = c("ST_Chopped/ch05/TableE2_RevenueAccounts.csv"),
    subsources = c("NIPA 1.1.5 line 6", "Appendix D/E adjustments"),
    shaikh_finding = "Marxian investment removes fictitious rental imputations",
    book_table = "E.2",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T510 = list(
    name = "Value Composition of Capital (C*/V*)",
    description = "Ratio of constant capital to variable capital",
    formula = "C*/V* = T502/T504",
    data_patterns = c("ST_Chopped/ch05/ExploitationComposition_1948_1989.csv"),
    subsources = c("Derived from T502, T504"),
    shaikh_finding = "C*/V* ~ 245% of conventional capital/labor ratio; +23% change 1948-1989",
    book_table = "5.7",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T511 = list(
    name = "Productive Labor Share (Lp/L)",
    description = "Share of productive workers in total employment",
    formula = "Lp/L = productive employment / total employment",
    data_patterns = c(
      "ST_Chopped/ch05/Table5_7_KeyRatios.csv",
      "ST_Chopped/ch05/Table5_7_Extended.csv",
      "data/employment_1948_2024.csv"
    ),
    subsources = c("NIPA 6.4D/6.5D", "BLS CES production worker ratios"),
    shaikh_finding = "Lp/L fell from 0.57 (1948) to 0.36 (1989); 37% decline",
    book_table = "5.7",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = TRUE
  ),

  T512 = list(
    name = "Productive Wage Share (V*/W)",
    description = "Share of variable capital in total compensation",
    formula = "V*/W = (Lp/L) x (ec_u/ec_p) ~ Lp/L when ec_u/ec_p ~ 1",
    data_patterns = c(
      "ST_Chopped/ch05/Table5_7_KeyRatios.csv",
      "ST_Chopped/ch05/Table5_7_Extended.csv",
      "data/exploitation_composition_1948_2024.csv"
    ),
    subsources = c("NIPA 6.2D", "BLS CES", "IO classification"),
    shaikh_finding = "V*/W ~ Lp/L empirically; 33% decline 1948-1989",
    book_table = "5.7",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = TRUE
  ),

  T513 = list(
    name = "Marxian Profit Rate (r* = S*/K)",
    description = "Rate of profit using surplus value over capital stock",
    formula = "r* = S* / K",
    data_patterns = c(
      "data/profit_rates_1948_1989.csv",
      "data/profit_rates_1948_2024.csv"
    ),
    subsources = c("T505 (S*)", "NIPA Fixed Assets Table 4.1", "FRED TCU"),
    shaikh_finding = "Secular decline in profit rate; known DIV-001 (total K vs productive K*)",
    book_table = "5.11",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = TRUE
  ),

  T514 = list(
    name = "Capacity-Adjusted Profit Rate (r*_adj)",
    description = "Profit rate adjusted for capacity utilization",
    formula = "r*_adj = r* x (1/TCU)",
    data_patterns = c(
      "data/profit_rates_1948_1989.csv",
      "data/profit_rates_1948_2024.csv"
    ),
    subsources = c("T513 (r*)", "FRED TCU capacity utilization"),
    shaikh_finding = "Capacity adjustment amplifies cyclical swings but preserves secular decline",
    book_table = "5.11",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T515 = list(
    name = "Productive Employment (Lp)",
    description = "Total number of productive workers across sectors",
    formula = "Lp = Sum of productive workers by sector",
    data_patterns = c(
      "ST_Chopped/ch05/Employment_1948_1989.csv",
      "data/employment_1948_2024.csv"
    ),
    subsources = c("NIPA 6.10B", "BLS CES production worker ratios"),
    shaikh_finding = "Lp grew from 33K (1948) to 41K (1988) in absolute terms",
    book_table = "E.3",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T516 = list(
    name = "Unproductive Employment (Lu)",
    description = "Total number of unproductive workers",
    formula = "Lu = L - Lp",
    data_patterns = c(
      "ST_Chopped/ch05/Employment_1948_1989.csv",
      "data/employment_1948_2024.csv"
    ),
    subsources = c("NIPA 6.10B", "BLS CES", "Derived from T515"),
    shaikh_finding = "Lu/Lp ratio rose 138% over postwar period",
    book_table = "E.3",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  )
)

# ============================================
# HELPER FUNCTIONS
# ============================================

#' Get series mapping for a given chapter
#' @param chapter Integer chapter number (e.g., 5)
#' @return Named list of series mappings for that chapter
get_chapter_series <- function(chapter) {
  if (chapter == 5) {
    return(CH5_SERIES_MAPPING)
  }
  if (chapter == 6) {
    return(CH6_SERIES_MAPPING)
  }
  if (chapter == 9) {
    return(CH9_SERIES_MAPPING)
  }
  # For future chapters, search all mappings by prefix
  prefix <- paste0("^T", chapter)
  all_mappings <- c(CH5_SERIES_MAPPING, CH6_SERIES_MAPPING, CH9_SERIES_MAPPING)
  matches <- grep(prefix, names(all_mappings))
  all_mappings[matches]
}

#' Get metadata for a single series
#' @param series_id Character series ID (e.g., "T506")
#' @return List of metadata fields, or NULL if not found
get_series_metadata <- function(series_id) {
  if (series_id %in% names(CH5_SERIES_MAPPING)) {
    return(CH5_SERIES_MAPPING[[series_id]])
  }
  if (series_id %in% names(CH6_SERIES_MAPPING)) {
    return(CH6_SERIES_MAPPING[[series_id]])
  }
  if (series_id %in% names(CH9_SERIES_MAPPING)) {
    return(CH9_SERIES_MAPPING[[series_id]])
  }
  NULL
}

#' Load data for a series from its data_patterns
#' @param series_id Character series ID (e.g., "T506")
#' @return Data frame from the first available data pattern, or NULL
get_series_data <- function(series_id) {
  meta <- get_series_metadata(series_id)
  if (is.null(meta)) {
    warning(paste("Series", series_id, "not found in series mappings"))
    return(NULL)
  }

  for (pattern in meta$data_patterns) {
    # Try relative to ShinyApp root first
    path <- file.path(here::here(), pattern)
    if (file.exists(path)) {
      return(readr::read_csv(path, show_col_types = FALSE))
    }
    # Try relative to Inputs root
    path2 <- file.path(AS2_PATHS$inputs_root, pattern)
    if (file.exists(path2)) {
      return(readr::read_csv(path2, show_col_types = FALSE))
    }
    # Try relative to Technical root
    path3 <- file.path(here::here(".."), pattern)
    if (file.exists(path3)) {
      return(readr::read_csv(path3, show_col_types = FALSE))
    }
  }

  warning(paste("No data file found for series", series_id))
  NULL
}

#' Check if a series has extension data
#' @param series_id Character series ID
#' @return Logical
is_extended_series <- function(series_id) {
  meta <- get_series_metadata(series_id)
  if (is.null(meta)) return(FALSE)
  isTRUE(meta$is_extended)
}

#' Check if a series ID belongs to Chapter 5
#' @param series_id Character series ID
#' @return Logical
is_chapter5_series <- function(series_id) {
  grepl("^T5\\d{2}$", series_id)
}

#' Get all extended series IDs
#' @return Character vector of series IDs with is_extended = TRUE
get_extended_series <- function() {
  ids <- names(CH5_SERIES_MAPPING)
  ids[vapply(CH5_SERIES_MAPPING, function(x) isTRUE(x$is_extended), logical(1))]
}

#' Get all key series IDs
#' @return Character vector of series IDs with is_key_series = TRUE
get_key_series <- function() {
  ids <- names(CH5_SERIES_MAPPING)
  ids[vapply(CH5_SERIES_MAPPING, function(x) isTRUE(x$is_key_series), logical(1))]
}

# ============================================
# CH6_SERIES_MAPPING — Named list of all 9 T6xx series
# ============================================

CH6_SERIES_MAPPING <- list(

  T601 = list(
    name = "Personal Tax on Workers (T_w_personal)",
    description = "Personal income tax allocated to workers proportional to wage share",
    formula = "IT_w = Personal income tax x (Compensation / Personal Income)",
    data_patterns = c(
      "ST_Chopped/ch06/Table6_1_TaxAccounts.csv",
      "data/nsw_1952_1989.csv"
    ),
    subsources = c("NIPA 3.1 line 3", "NIPA 3.2 line 3", "NIPA 3.3 line 3", "NIPA 2.1 lines 1-2"),
    shaikh_finding = "Income taxes allocated proportional to worker wage share of total personal income",
    book_table = "6.1",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T602 = list(
    name = "Social Insurance Tax on Workers (T_w_social)",
    description = "Employee contributions for government social insurance (FICA)",
    formula = "SI_w = NIPA 3.1 line 8 (contributions from persons)",
    data_patterns = c(
      "ST_Chopped/ch06/Table6_1_TaxAccounts.csv",
      "data/nsw_1952_1989.csv"
    ),
    subsources = c("NIPA 3.1 line 8", "NIPA 3.2 lines 10-11"),
    shaikh_finding = "Social insurance directly identifiable as worker contribution; no allocation needed",
    book_table = "6.1",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T603 = list(
    name = "Property Tax on Workers (T_w_property)",
    description = "Property taxes allocated to workers by homeownership share",
    formula = "PT_w = Property tax x 0.5 (worker homeownership share)",
    data_patterns = c(
      "ST_Chopped/ch06/Table6_1_TaxAccounts.csv",
      "data/nsw_1952_1989.csv"
    ),
    subsources = c("NIPA 3.3 line 9"),
    shaikh_finding = "Property taxes split 50/50 between workers and capitalists as baseline assumption",
    book_table = "6.1",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T604 = list(
    name = "Total Tax on Workers (T_w)",
    description = "Sum of all tax components paid by workers",
    formula = "T_w = T601 + T602 + T603 + indirect_tax_workers",
    data_patterns = c(
      "ST_Chopped/ch06/Table6_1_TaxAccounts.csv",
      "data/nsw_1952_1989.csv"
    ),
    subsources = c("Derived from T601, T602, T603 + NIPA 3.1 line 4"),
    shaikh_finding = "Total tax burden on workers rose from T/EC=0.18 (1952) to 0.32 (1988)",
    book_table = "6.1",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T605 = list(
    name = "Government Benefits to Workers (B_w)",
    description = "Transfer payments and social benefits flowing to workers",
    formula = "B_w = Social Security + Medicare + Medicaid + UI + Veterans + Other",
    data_patterns = c(
      "ST_Chopped/ch06/Table6_2_BenefitAccounts.csv",
      "data/nsw_1952_1989.csv"
    ),
    subsources = c("NIPA 2.1 lines 17-23"),
    shaikh_finding = "Benefit rate B/EC rose from 0.11 (1952) to 0.28 (1988) — 155% increase",
    book_table = "6.2",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T606 = list(
    name = "Government Services Consumed by Workers (G_w)",
    description = "Government expenditure on worker-benefiting services (education, health, infrastructure)",
    formula = "G_w = (state_local_consumption + 0.6*federal_consumption) x worker_share",
    data_patterns = c(
      "ST_Chopped/ch06/Table6_2_BenefitAccounts.csv",
      "data/nsw_1952_1989.csv"
    ),
    subsources = c("NIPA 3.1 line 21", "NIPA 3.2 line 25", "NIPA 3.3 line 24"),
    shaikh_finding = "Government services allocated by worker share; excludes military/police/courts",
    book_table = "6.2",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  ),

  T607 = list(
    name = "Net Social Wage (NSW = B_w + G_w - T_w)",
    description = "Net fiscal benefit to workers from the state",
    formula = "NSW = T605 + T606 - T604",
    data_patterns = c(
      "ST_Chopped/ch06/Table6_3_NetSocialWage.csv",
      "data/nsw_1952_1989.csv",
      "data/nsw_1952_2025.csv"
    ),
    subsources = c("Derived from T604, T605, T606"),
    shaikh_finding = "NSW predominantly negative (35/38 years); positive during deep recessions (1975, 1976, 1983) when countercyclical benefits temporarily exceeded tax burden",
    book_table = "6.3",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = TRUE
  ),

  T608 = list(
    name = "NSW/V* Ratio",
    description = "Net social wage as share of variable capital",
    formula = "NSW/V* = T607 / T504",
    data_patterns = c("data/nsw_1952_1989.csv"),
    subsources = c("Derived from T607, T504 (Chapter 5)"),
    shaikh_finding = "NSW/V* trending more negative; true exploitation rate higher than apparent",
    book_table = "6.4",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = TRUE
  ),

  T609 = list(
    name = "NSW as Share of National Income",
    description = "Net social wage normalized by national income",
    formula = "NSW/NI = T607 / Personal Income",
    data_patterns = c("data/nsw_1952_1989.csv"),
    subsources = c("Derived from T607, NIPA 2.1 line 1"),
    shaikh_finding = "Scale-normalized NSW measure showing persistent negative transfer",
    book_table = "6.4",
    is_extended = FALSE,
    is_conceptual = FALSE,
    is_key_series = FALSE
  )
)

# ============================================
# CH9_SERIES_MAPPING — Named list of T9xx series (Chapter 9: Summary)
# ============================================

CH9_SERIES_MAPPING <- list(

  T901 = list(
    name = "Summary Table (Key Indicators)",
    description = "Aggregated key Marxian indicators from Chapters 5 and 6",
    formula = "Assembly of T506, T511, T512, T513, T514, T608",
    data_patterns = c(
      "data/summary_indicators_1948_1989.csv",
      "data/summary_indicators_1948_2024.csv"
    ),
    subsources = c("T506 (Ch5)", "T511 (Ch5)", "T512 (Ch5)", "T513 (Ch5)", "T514 (Ch5)", "T608 (Ch6)"),
    shaikh_finding = "Marxian categories reveal fundamentally different trends than orthodox measures: e rose 44%, Lp/L fell 37%, S* ~ 2x profit-type income",
    book_table = "9.1",
    is_extended = TRUE,
    is_conceptual = FALSE,
    is_key_series = TRUE
  )
)

# ============================================
# UNIFIED HELPERS — Support Ch5, Ch6, and Ch9
# ============================================

#' Check if a series ID belongs to Chapter 6
#' @param series_id Character series ID
#' @return Logical
is_chapter6_series <- function(series_id) {
  grepl("^T6\\d{2}$", series_id)
}

#' Check if a series ID belongs to Chapter 9
#' @param series_id Character series ID
#' @return Logical
is_chapter9_series <- function(series_id) {
  grepl("^T9\\d{2}$", series_id)
}

# ============================================
# VALIDATION (run at source time)
# ============================================

.validate_mapping <- function(mapping, prefix, count) {
  expected_ids <- paste0(prefix, sprintf("%02d", 1:count))
  actual_ids <- names(mapping)

  missing <- setdiff(expected_ids, actual_ids)
  if (length(missing) > 0) {
    warning(paste0(deparse(substitute(mapping)), " missing series: "),
            paste(missing, collapse = ", "))
  }

  required_fields <- c("name", "description", "formula", "data_patterns",
                        "is_extended", "is_conceptual", "is_key_series")
  for (id in actual_ids) {
    entry <- mapping[[id]]
    for (field in required_fields) {
      if (is.null(entry[[field]])) {
        warning(paste("Series", id, "missing required field:", field))
      }
    }
  }
}

.validate_mapping(CH5_SERIES_MAPPING, "T5", 16)
.validate_mapping(CH6_SERIES_MAPPING, "T6", 9)
.validate_mapping(CH9_SERIES_MAPPING, "T9", 1)
