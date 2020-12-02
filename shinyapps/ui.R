#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(DT)
library(RMySQL)
library(lubridate)
library(ggplot2)


# Define UI for application that draws a histogram
shinyUI(fluidPage(
    
    # Application title
    titlePanel("Covid 19"),
    
    h4("Product Development: Project"),
    h6("José Sebastián Rodríguez Velásquez"),
    h6("Diego Fernando Valle Morales"),
    h6("Juan Pablo Carranza Hurtado"),
    h6("José Alberto Ligorría Taracena"),
    
    
    # Sidebar with a slider input for number of bins
    
    tabsetPanel(
        tabPanel("Tab 1",
                sidebarLayout(
                     sidebarPanel(
                         h4(strong("Selecciona los filtros que construyas"))
                     ),
                     mainPanel(
                         fluidRow(
                             column(6,DT::DTOutput('DT_table_confirmed')),
                             column(6,DT::DTOutput('DT_table_deaths')),
                             column(6,DT::DTOutput('DT_table_recovered'))
                             )
                         
                     )
                 )
                 
            )
                 
                 
        )
                 

    
    
))