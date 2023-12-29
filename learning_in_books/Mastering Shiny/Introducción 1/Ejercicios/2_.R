library("shiny")
library("shinyWidgets")


ui <- fluidPage(
  textInput("name", label = " ", placeholder = "Your name"),
  sliderInput("date", label = "When should we deliver?", value = as.Date("2020-09-17"),
              min = as.Date("2020-09-16"), max = as.Date("2020-09-23")),
  sliderInput("value", label = "Valores", min = 0, max = 100, value = 50,
              step = 5),
  switchInput(inputId = "id", value = TRUE)
  
)

server <- function(input, output, session) {
  
}

shinyApp(ui, server)