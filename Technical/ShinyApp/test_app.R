# Test script to verify app loads correctly
library(shiny)
library(shinydashboard)
library(tidyverse)
library(plotly)
library(DT)
library(scales)
library(writexl)
library(zip)

# Load the app
tryCatch({
  source('app.R', echo = FALSE)
  cat('\n=================================\n')
  cat('✅ APP LOADED SUCCESSFULLY!\n')
  cat('=================================\n')
  cat('Total lines:', length(readLines('app.R')), '\n')
  cat('Questions loaded:', nrow(questions), '\n')
  cat('All data files loaded successfully\n')
  cat('=================================\n\n')
}, error = function(e) {
  cat('\n=================================\n')
  cat('❌ ERROR LOADING APP\n')
  cat('=================================\n')
  cat('Error message:', e$message, '\n')
  cat('=================================\n\n')
  stop(e)
})
