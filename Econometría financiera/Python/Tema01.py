# -*- coding: utf-8 -*-
"""
Diplomado: Econometría aplicada / aplicada a la investigación
Modulo: Econometría Financiera
Sesión: 02
Tema: Análisis de una serie de tiempo financiera
Docente: Alexis Adonai Morales Alberto
GEM
"""

"""
Librerias a utilizar
"""

import yfinance as yahooFinance
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")
from siuba import _, select, filter, group_by, summarize
import siuba

"""
Importar datos financieros
"""

# Método 1: Usando la librerías/modulo yfinance

## Se hace fallamado de la información mediante yfinance 
## con la etiqueta del indice S&P500

GetSP500information = yahooFinance.Ticker("^GSPC")

## Se revisa mediante print la obtención histórica máxima
## de los registros del índice S&P 500

print(GetSP500information.history(period="max"))

## Se convierten los datos en DataFrame

SP500 = GetSP500information.history(period="max")

"""
Gráfico de serie de tiempo sobre los activos financieros
"""

plt.grid(True)
plt.plot(SP500["Close"])
plt.show()

# Método 2: Importando datos desde CSV 

## Lectura de información ruta + nombre de archivo

ruta = "D:/GEM/Diplomado Econometría Aplicada/Econometría financiera/Clases agosto 2023/Bases"

EUR_USD = pd.read_csv(ruta+"/EURUSD=X.csv")

## Se genera vector de fechas con su respectiva frecuencia 

EUR_USD['Fecha'] = pd.date_range(start="2018-08-13",
                                 end = "2023-08-11",
                                 freq="B")

## Se seleccionana columnas de interés

EUR_USD2 = EUR_USD >> select(_.Fecha, _.Close)

## Se asgina la fecha como indice 

EUR_USD2['Fecha'] = pd.to_datetime(EUR_USD2["Fecha"])
EUR_USD2 = EUR_USD2.set_index("Fecha")

## Transformar a serie para simular una serie de tiempo 

EUR_USD_ts = pd.Series(EUR_USD2.Close, index = EUR_USD2.index)

## Gráfico temporal 

plt.grid(True)
plt.plot(EUR_USD_ts)
plt.show()

# Gráficos temporales 

plt.style.use('seaborn')
gf=EUR_USD2.plot()
gf.set_title("Tipo de cambio EUR/USD, del 2018-2023")
plt.show()

## Función para gráficar 

def plot_df(datos, x, y, title="", xlabel="Fecha",
            ylabel="Kilogramos", dpi=300):
    plt.figure(figsize=(12,5), dpi=dpi)
    plt.plot(x,y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel,
    ylabel=ylabel)
    plt.show()


plot_df(SP500, x=SP500.index, y=SP500.Close,
        title = "S&P 500 de 1927-2023",
        ylabel="Indice")

SP5002 = (SP500
    >> filter(_.index>='2000-01-01 00:00:00-04:00')
   )

plot_df(SP5002, x=SP5002.index, y=SP5002.Close,
        title = "S&P 500 de 2000-2023",
        ylabel="Indice")

plot_df(EUR_USD2, x=EUR_USD2.index, y=EUR_USD2.Close,
        title = "Tipo de cambio EUR/USD del 2018-2023",
        ylabel="EUR/USD")

# Función de resumen estadístico 

def Resumen_estadistico(x):
    # Definción de media
    def Media(x):
        md=sum(x)/len(x)
        return md
    # Definción de mediana
    def Mediana(x):
        n = len(x)
        if n % 2:
            mediana = sorted(x)[round(0.5)*(n-1)]
        else: 
            x_ord, index=sorted(x), round(0.5*n)
            mediana = 0.5*(x_ord[index-1]+x_ord[index])
        return mediana
    # Definición de moda 
    def Moda(x):
        y={}
        for a in x:
            if not a in y:
                y[a]=1
            else:
                y[a]+=1
        return [g for g,l in y.items() if l==max(y.values())]
    # Varianza
    def varianza(x):
        n = len(x)
        media1 = Media(x)
        Desviaciones = [(x-media1)**2 for x in x]
        sigma2=sum(Desviaciones) / (n-1)
        return sigma2
    # Desviación típica
    def desviacion(x):
        sigma2=varianza(x)
        des = math.sqrt(sigma2)
        return des
    # Calculo de cuartiles
    def cuartil(x, q=0.5):
        Q = np.quantile(x, q)
        return Q
    # Calculo de valores 
    Med=Media(x)
    Median = Mediana(x)
    Mode = Moda(x)
    Varianza = varianza(x)
    Des_std = desviacion(x)
    Primer_cuartil = cuartil(x, q=0.25)
    Tercer_cuartil = cuartil(x, q=0.75)
    RIQ = Tercer_cuartil-Primer_cuartil
    Atipicos = sum((x<(Primer_cuartil-1.5*RIQ))|(x>(Tercer_cuartil+1.5*RIQ)))
    Asimetria = sum((x-Med)**3)/(len(x)*Des_std**3)
    Curtosis = sum((x-Med)**4)/(len(x)*Des_std**4)
    # Construcción de salida
    Salida = pd.DataFrame({'Estadísticos': ["Media",
                                            "Mediana",
                                            "Moda",
                                            "Varianza",
                                            "Desviación",
                                            "Primer cuartil",
                                            "Tercer cuartil",
                                            "RIQ",
                                            "Atípicos",
                                            "Asimetría",
                                            "Curtosis"],
                           'Valores':[Med, Median, Mode, Varianza,
                                      Des_std, Primer_cuartil,
                                      Tercer_cuartil, RIQ,
                                      Atipicos, Asimetria,
                                      Curtosis]})
    return Salida

RE_SP500 = Resumen_estadistico(SP500.Close)

EUR_USD=EUR_USD.dropna()
RE_EUR_USD = Resumen_estadistico(EUR_USD.Close)


# Maniuplaciones temporales 

## Crear columna de años 

SP500['año'] = [d.year for d in SP500.index]

## Se crea la columnas de meses 

SP500['mes'] = [d.strftime('%b') for d in SP500.index]

## Gráfico de promedios por año 

plt.bar(SP500.año, SP500.Close)
plt.ylabel("Índice S&P500")
plt.xlabel("Año")
plt.title("S&P 500 anual promedio 1927-2023")
plt.show()

## Gráfico por año y mes 

### 2022 

in_2022 = SP500['año']==2022
SP500_2022 = SP500[in_2022]

SP500_2020 = SP500 >> filter(_.año == 2022)

plt.bar(SP500_2020.mes, SP500_2020.Close)
plt.ylabel("Índice S&P500")
plt.xlabel("Año = 2022")
plt.title("S&P 500 mensual para el año 2022")
plt.show()


plt.plot(SP500_2020.index, SP500_2020.Close)
plt.ylabel("Índice S&P500")
plt.xlabel("Año = 2022")
plt.title("S&P 500 mensual para el año 2022")
plt.show()

SP500_2020_prom = (SP500
    >> filter(_.año==2022)
    >> group_by(_.mes)
    >> summarize(
        promedio = _.Close.mean()
        ))

Meses = ["Jan", "Feb", "Mar", "Apr",
         "May", "Jun", "Jul", "Aug", 
         "Sep", "Oct", "Nov", "Dec"]

SP500_2020_prom = SP500_2020_prom.set_index('mes')
SP500_2020_prom=SP500_2020_prom.loc[Meses]
SP500_2020_prom=SP500_2020_prom.reindex(Meses)
SP500_2020_prom = SP500_2020_prom.reset_index()

plt.plot(SP500_2020_prom.mes, SP500_2020_prom.promedio)
plt.ylabel("Índice S&P500")
plt.xlabel("Año = 2022")
plt.title("S&P 500 mensual para el año 2022")
plt.show()


# Histograma 

plt.figure(figsize=(12,5), dpi=300)
plt.hist(x=SP500.Close, color="blue", rwidth=0.85)
plt.xlabel("Índice S&P500")
plt.ylabel("Frecuencia")
plt.title("Histograma del Índice S&P 500")
plt.show()

plt.figure(figsize=(12,5), dpi=300)
plt.hist(x=SP5002.Close, color="blue", rwidth=0.85)
plt.xlabel("Índice S&P500")
plt.ylabel("Frecuencia")
plt.title("Histograma del Índice S&P 500")
plt.show()
