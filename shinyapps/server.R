#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(readr)
library(DT)
library(RMySQL)
library(lubridate)
library(ggplot2)

drv = dbDriver("MySQL")
db = dbConnect(drv,user='test',password = 'test123',host = 'db',dbname = 'covid')

confirmed = dbGetQuery(db,statement = ('SELECT * FROM confirmed;'))
deaths = dbGetQuery(db,statement = ('SELECT * FROM deaths;'))
recovered = dbGetQuery(db,statement = ('SELECT * FROM recovered;'))


# Define server logic required to draw a histogram
shinyServer(function(input, output) {
    
    output$DT_table_confirmed <- renderDT({
        confirmed
    })
    
    output$DT_table_deaths <- renderDT({
        deaths
    })

    output$DT_table_recovered <- renderDT({
        recovered
    })
    
})