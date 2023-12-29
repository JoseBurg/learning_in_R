library(shiny)

ui <- fluidPage(
  titlePanel("Nuestra App"),
  sidebarLayout(
    sidebarPanel = sidebarPanel(
      wellPanel(
        h2("Muestra 1"),
        fluidRow(
          column(width = 6, numericInput("size", label = "Sample size", value = 100)),
          column(width = 6, numericInput("sd", label = "Standar Dev", value = 5))
        )
      ),
      wellPanel(
        h2("Muestra 2"),
        fluidRow(
          column(width = 6, numericInput("size2", label = "Sample size", value = 100)),
          column(width = 6, numericInput("sd2", label = "Standar Dev", value = 5))
        )
      )
    ),
    mainPanel = mainPanel(
      fluidRow(
        column(
          width = 6,
          h3("Histograma sample 1"),
          plotOutput("hist_sample1")
          ),
        column(
          width = 6,
          h3("Density sample 1"),
          plotOutput("density_sample1")
        )
      ),
      fluidRow(
        column(
          width = 6,
          h3("Histograma sample 2"),
          plotOutput("hist_sample2")
          ),
        column(
          width = 6,
          h3("Density sample 2"),
          plotOutput("density_sample2")
        )
      )
    )
  )
)
server <- function(input, output, session) {
  sample1 <- reactive({
    set.seed(123)
    rnorm(n = input$size, sd = input$sd, mean = 16)
  })
  sample2 <- reactive({
    req(input$size2, input$sd2)
    set.seed(123)
    rnorm(n = input$size2, sd = input$sd2, mean = 22)
  })
  output$hist_sample1 <- renderPlot({
    hist(sample1())
  })
  output$density_sample1 <- renderPlot({
    plot(density(sample1()))
  })
  output$hist_sample2 <- renderPlot({
    hist(sample2())
  })
  output$density_sample2 <- renderPlot({
    plot(density(sample2()))
  })
}

shinyApp(ui, server)
