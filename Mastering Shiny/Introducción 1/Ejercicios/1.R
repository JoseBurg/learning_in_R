library(shiny)

ui <- fluidPage(
  textInput("name", "What's your name?"),
  textOutput("greeting"),
  numericInput("age", "How old are you?", value = NA),
  plotOutput("histogram")
)

server <- function(input, output, session) {
  output$greeting <- renderText({
    paste0("Hello ", input$name, ", how are you?")
  })
  output$histogram <- renderPlot({
    hist(rnorm(input$age))
  }, res = 96)
  
}

shinyApp(ui, server)