library(shiny)
library(openxlsx)

ui <- fluidPage(
  tags$head(
    tags$style(HTML("
      .custom-title {
        background-color: #ddd7f1;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 20px;
        font-weight: bold;
        border-bottom: 3px solid #1a09f9;
      }
    "))
  ),
  titlePanel(
    div(class = "custom-title", "Calculadora de Préstamos")),
  sidebarLayout(
    sidebarPanel(
      numericInput("monto", "Monto del Préstamo:", value = 10000, step = 1000),
      numericInput("cuotas", "Cuotas (en meses):", value = 12),
      sliderInput("tasa", "Tasa de Interés Anual (%):",min = 5, max = 80, value = 15),
      actionButton("calcular", "Calcular Tabla de Amortización")
    ),
    mainPanel(
      tableOutput("resumen"),
      tableOutput("tabla"),
      downloadButton("descargar", "Descargar Tabla de Amortización")
    )
  )
)

server <- function(input, output) {
  observeEvent(input$calcular, {
    monto <- input$monto
    cuotas <- input$cuotas
    tasa <- input$tasa / 100 / 12  # Convertir la tasa de interés anual a mensual
    cuota_mensual <- (monto * tasa) / (1 - (1 + tasa)^(-cuotas))  # Cálculo de la cuota mensual
    
    # Crear la tabla de amortización
    saldo_pendiente <- monto
    intereses_total <- 0
    datos_amortizacion <- data.frame()
    
    for (mes in 1:cuotas) {
      intereses <- saldo_pendiente * tasa
      capital <- cuota_mensual - intereses
      saldo_pendiente <- saldo_pendiente - capital
      intereses_total <- intereses_total + intereses
      
      datos_amortizacion <- rbind(datos_amortizacion, c(mes, cuota_mensual, intereses, capital, saldo_pendiente))
    }
    
    colnames(datos_amortizacion) <- c("Mes", "Cuota Mensual", "Intereses", "Capital", "Saldo Pendiente")
    
    output$tabla <- renderTable({
      datos_amortizacion |> 
        dplyr::mutate(
        dplyr::across(dplyr::everything(), round)) |> 
        tail(n = 12)
    })
    
    output$resumen <- renderTable({
      datos_amortizacion |> 
        dplyr::summarise(
          `Total intereses` = sum(Intereses),
          `Total de capital` = sum(Capital),
          `Capital e intereses` = sum(`Total intereses`, `Total de capital`)) |> 
        dplyr::mutate(
          dplyr::across(dplyr::everything(), ~format(.,big.mark = ",", nsmall = 2)),
          dplyr::across(dplyr::everything(), \(x){paste0("RD$", x)})) |> gt::gt()
        
    })
    
    output$descargar <- downloadHandler(
      filename = function() {
        "tabla_amortizacion.xlsx"
      },
      content = function(file) {
        write.xlsx(datos_amortizacion, file, row.names = FALSE)
      }
    )
  })
}

shinyApp(ui, server)
