import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import plotly
import plotly.express as px
import os
from openpyxl import Workbook

##############################################################################################
#FUNCIONES:

# Función para obtener el archivo csv de datos del paciente 
def funcObtenerCSV(directorio_actual, id_global):
    from InputDatosPaciente import id_global_principal
    from BusquedaPaciente import id_global_busqueda
    if id_global_principal != "":
        id_global = id_global_principal
    elif id_global_busqueda != "":
        id_global = id_global_busqueda
    nombre_excel = 'Datos ' + id_global + '.csv'
    path = os.path.join(directorio_actual, nombre_excel)
    return path, id_global

# Función para pasar el tiempo de formato HH:MM:SS a segundos 
def strtiempo_a_segundos(str_tiempo):
    partes = str_tiempo.split(':')  # Dividir el tiempo en partes: horas, minutos, segundos
    horas = int(partes[0])
    minutos = int(partes[1])
    segundos = int(partes[2])
    segs_tiempo = horas * 3600 + minutos * 60 + segundos  # Calcular el total de segundos
    return segs_tiempo

# Función para calcular los porcentaje del tiempo del estado en que se encuentra el valor del SPI en cada franja 
def PorcentajesEstado(valsSPIestado):
    tiempo = len(valsSPIestado)
    insuficiente = 0
    adecuado = 0
    excesivo = 0
    for spi in valsSPIestado:
        if spi > 50:
            insuficiente += 1
        elif spi > 20:
            adecuado += 1
        elif spi > -1: 
            excesivo += 1
    porcentaje_excesivo = (excesivo/tiempo)*100
    porcentaje_adecuado = (adecuado/tiempo)*100
    porcentaje_insuficiente = (insuficiente/tiempo)*100
    if porcentaje_excesivo == 0:
        porcentaje_excesivo = 0.01
    if porcentaje_adecuado == 0:
        porcentaje_adecuado = 0.01
    if porcentaje_insuficiente == 0:
        porcentaje_insuficiente = 0.01
    porcentajes = [porcentaje_insuficiente, porcentaje_adecuado, porcentaje_excesivo]
    return porcentajes

##############################################################################################

#global id_global
id_global = ""

# Obtiene el CSV del paciente y levanta los datos 
directorio_actual = os.path.abspath(os.path.dirname(__file__))
path, id_global = funcObtenerCSV(directorio_actual, id_global)
df = pd.read_csv(path, encoding='latin-1')
# Pasamos los spi = "-" a np.nan
df['spi'] = df['spi'].replace('nan', np.nan)
df['spi_promedio'] = df['spi_promedio'].replace('nan', np.nan)
t = df['tiempo']
spi = df['spi']
spi_promedio = df["spi_promedio"]
estados = df['estado']
eventos = df['evento']
#alarmas = df['alarma']

##############################################################################################
# GRAFICO INTERACTIVO EVOLUCION SPI - POR ESTADOS:

pre_basal = df[df.estado == "-"]
basal = df[df.estado == "basal"]
induccion = df[df.estado == "induccion"]
mantenimiento = df[df.estado == "mantenimiento"]
despertar = df[df.estado == "despertar"]
recuperacion = df[df.estado == "recuperacion"]
hayeventos = df[df.evento != "-"]
haypromedio = df[df.spi_promedio != "-"]

SPIEstados = plotly.graph_objs.Figure()
PreBasal = plotly.graph_objs.Scatter(x=(pre_basal.tiempo)/60, y=pre_basal.spi, fill='none', mode='lines', line = {'color' : 'rgb(100, 138, 196)', 'shape': 'spline'}, name="Pre Basal", hovertemplate = "<br>SPI: %{y}<br>")
Basal = plotly.graph_objs.Scatter(x=(basal.tiempo)/60, y=basal.spi, fill='none', marker = {'color' : 'rgb(47, 138, 196)'}, name="Basal", hovertemplate = "<br>SPI: %{y}<br>")
Induccion = plotly.graph_objs.Scatter(x=(induccion.tiempo)/60, y=induccion.spi, fill='none', marker = {'color' : 'rgb(231, 41, 138)'}, name="Inducción", hovertemplate = "<br>SPI: %{y}<br>")
Mantenimiento = plotly.graph_objs.Scatter(x=(mantenimiento.tiempo)/60, y=mantenimiento.spi, fill='none', marker = {'color' : 'rgb(27, 158, 119)'}, name="Mantenimiento", hovertemplate = "<br>SPI: %{y}<br>")
Despertar = plotly.graph_objs.Scatter(x=(despertar.tiempo)/60, y=despertar.spi, fill='none', marker = {'color' : 'rgb(118, 78, 150)'}, name="Despertar", hovertemplate = "<br>SPI: %{y}<br>")
Recuperacion = plotly.graph_objs.Scatter(x=(recuperacion.tiempo)/60, y=recuperacion.spi, fill='none', marker = {'color' : 'rgb(255, 127, 0)'}, name="Recuperación", hovertemplate = "<br>SPI: %{y}<br>")
SPI_promedio = plotly.graph_objs.Scatter(x=(haypromedio.tiempo)/60, y=haypromedio.spi_promedio, name="SPI Promedio", mode='lines', line = {'color' : 'rgb(0, 0, 0)'}, hovertemplate = "<br>Valor: %{y:.1f}<br>")
Eventos = plotly.graph_objs.Scatter(x=(hayeventos.tiempo)/60, y=hayeventos.spi, name="Eventos", mode='markers', line=dict(color='black'), text=hayeventos.evento, hovertemplate = "<br>%{text}")

SPIEstados.add_trace(PreBasal)
SPIEstados.add_trace(Basal)
SPIEstados.add_trace(Induccion)
SPIEstados.add_trace(Mantenimiento)
SPIEstados.add_trace(Despertar)
SPIEstados.add_trace(Recuperacion)
SPIEstados.add_trace(SPI_promedio)
SPIEstados.add_trace(Eventos)

SPIEstados.update_layout(title="Evolución SPI con identificación de estados", legend_title_text = "Referencias:")
SPIEstados.update_xaxes(title_text="Tiempo (minutos)", hoverformat=".2f")
SPIEstados.update_yaxes(title_text="SPI", range=(0, 100))
SPIEstados.update_layout(hovermode="x unified")

inic_basal = (basal.tiempo.iloc[0])/60
fin_basal = (basal.tiempo.iloc[-1])/60
inic_induccion = (induccion.tiempo.iloc[0])/60
fin_induccion = (induccion.tiempo.iloc[-1])/60
inic_mantenimiento = (mantenimiento.tiempo.iloc[0])/60
fin_mantenimiento = (mantenimiento.tiempo.iloc[-1])/60
inic_despertar = (despertar.tiempo.iloc[0])/60
fin_despertar = (despertar.tiempo.iloc[-1])/60
inic_recuperacion = (recuperacion.tiempo.iloc[0])/60
fin_recuperacion = (recuperacion.tiempo.iloc[-1])/60

# basal: 190, 213, 242  azul
# induccion: 244, 202, 225 rosa
# mantenimiento: 179, 236, 225  turquesa
# despertar: 232, 203, 248  violeta
# recuperacion: 253, 205, 152  naranja

colors = ['rgb(190, 213, 242)', 'rgb(244, 202, 225)', 'rgb(179, 236, 225)', 'rgb(232, 203, 248)', 'rgb(253, 205, 152)']
shapes = []
bgs = [[inic_basal, fin_basal], [inic_induccion, fin_induccion], [inic_mantenimiento, fin_mantenimiento], [inic_despertar, fin_despertar], [inic_recuperacion, fin_recuperacion]]
for i, b in enumerate(bgs):
    shapes.append(dict(type="rect", xref="x", yref="paper", x0=b[0], y0=0, x1=b[1], y1=1, fillcolor=colors[i], opacity=0.8, layer="below", line_width=0))
SPIEstados.update_layout(yaxis=dict(showgrid=False), shapes=shapes)

# Guarda la imagen estática del gráfico dinámico
SPIEstados.write_image(f"{directorio_actual}/{'figSPIEstados.jpg'}")


##############################################################################################

# GRAFICO INTERACTIVO EVOLUCION SPI - POR FRANJAS:

SPIFranjas = plotly.graph_objs.Figure()
PreBasal = plotly.graph_objs.Scatter(x=(pre_basal.tiempo)/60, y=pre_basal.spi, fill='none', marker = {'color' : '#f0f0f0'}, name="Pre Basal", hovertemplate = "<br>SPI: %{y}<br>")
Basal = plotly.graph_objs.Scatter(x=(basal.tiempo)/60, y=basal.spi, fill='none', marker = {'color' : '#f0f0f0'}, name="Basal", hovertemplate = "<br>SPI: %{y}<br>")
Induccion = plotly.graph_objs.Scatter(x=(induccion.tiempo)/60, y=induccion.spi, fill='none', marker = {'color' : '#f0f0f0'}, name="Inducción", hovertemplate = "<br>SPI: %{y}<br>")
Mantenimiento = plotly.graph_objs.Scatter(x=(mantenimiento.tiempo)/60, y=mantenimiento.spi, fill='none', marker = {'color' : '#f0f0f0'}, name="Mantenimiento", hovertemplate = "<br>SPI: %{y}<br>")
Despertar = plotly.graph_objs.Scatter(x=(despertar.tiempo)/60, y=despertar.spi, fill='none', marker = {'color' : '#f0f0f0'}, name="Despertar", hovertemplate = "<br>SPI: %{y}<br>")
Recuperacion = plotly.graph_objs.Scatter(x=(recuperacion.tiempo)/60, y=recuperacion.spi, fill='none', marker = {'color' : '#f0f0f0'}, name="Recuperación", hovertemplate = "<br>SPI: %{y}<br>")
SPI_promedio = plotly.graph_objs.Scatter(x=(haypromedio.tiempo)/60, y=haypromedio.spi_promedio, name="SPI Promedio", mode='lines', line = {'color' : 'rgb(0, 0, 0)'}, hovertemplate = "<br>Valor: %{y:.1f}<br>")
Eventos = plotly.graph_objs.Scatter(x=(hayeventos.tiempo)/60, y=hayeventos.spi, name="Eventos", mode='markers', line=dict(color='black'), text=hayeventos.evento, hovertemplate = "%{text}")

SPIFranjas.add_trace(PreBasal)
SPIFranjas.add_trace(Basal)
SPIFranjas.add_trace(Induccion)
SPIFranjas.add_trace(Mantenimiento)
SPIFranjas.add_trace(Despertar)
SPIFranjas.add_trace(Recuperacion)
SPIFranjas.add_trace(SPI_promedio)
SPIFranjas.add_trace(Eventos)

SPIFranjas.update_traces(showlegend=False, selector=dict(name="Pre Basal"))
SPIFranjas.update_traces(showlegend=False, selector=dict(name="Basal"))
SPIFranjas.update_traces(showlegend=False, selector=dict(name="Inducción"))
SPIFranjas.update_traces(showlegend=False, selector=dict(name="Mantenimiento"))
SPIFranjas.update_traces(showlegend=False, selector=dict(name="Despertar"))
SPIFranjas.update_traces(showlegend=False, selector=dict(name="Recuperación"))

SPIFranjas.update_layout(title="Evolución SPI", legend_title_text = "Referencias:")
SPIFranjas.update_xaxes(title_text="Tiempo (minutos)", hoverformat=".2f")
SPIFranjas.update_yaxes(title_text="SPI", range=(0, 100))
SPIFranjas.update_layout(hovermode="x unified") 

colors = ['#fff977', '#87ec55', '#ff715f']
shapes = []
bgs = [[0, 20], [20, 50], [50, 100]]
for i, b in enumerate(bgs):
    shapes.append(dict(type="rect", xref="paper", yref="y", x0=0, y0=b[0], x1=1, y1=b[1], fillcolor=colors[i], opacity=0.9, layer="below", line_width=0))
SPIFranjas.update_layout(xaxis=dict(showgrid=False), shapes=shapes)

# Guarda la imagen estática del gráfico dinámico
SPIFranjas.write_image(f"{directorio_actual}/{'figSPIFranjas.jpg'}")


##############################################################################################
# GRAFICO INTERACTIVO EVOLUCION SPI - PORCENTAJES:

porcentajes_basal = PorcentajesEstado(basal.spi)
porcentajes_induccion = PorcentajesEstado(induccion.spi)
porcentajes_mantenimiento = PorcentajesEstado(mantenimiento.spi)
porcentajes_despertar = PorcentajesEstado(despertar.spi)
porcentajes_recuperacion = PorcentajesEstado(recuperacion.spi)

porcentajes = [porcentajes_basal, porcentajes_induccion, porcentajes_mantenimiento, porcentajes_despertar, porcentajes_recuperacion]

PorcentajesSPI = plotly.graph_objs.Figure(layout=dict(yaxis=dict(range=[0, 100])))
insuficientes = plotly.graph_objs.Bar(x=["basal", "induccion", "mantenimiento", "despertar", "recuperacion"], y=[porcentajes_basal[0], porcentajes_induccion[0], porcentajes_mantenimiento[0], porcentajes_despertar[0], porcentajes_recuperacion[0]], marker_color="rgb(230, 80, 80)", name="Insuficiente", offsetgroup="Insuficiente", legendgroup="Insuficiente", hovertemplate = "<br>Estado: %{x} <br>Porcentaje: %{y:.2f} %")
adecuados = plotly.graph_objs.Bar(x=["basal", "induccion", "mantenimiento", "despertar", "recuperacion"], y=[porcentajes_basal[1], porcentajes_induccion[1], porcentajes_mantenimiento[1], porcentajes_despertar[1], porcentajes_recuperacion[1]], marker_color="rgb(166, 216, 84)", name="Adecuado", offsetgroup="Adecuado", legendgroup="Adecuado", hovertemplate = "<br>Estado: %{x} <br>Porcentaje: %{y:.2f} %")
excesivos = plotly.graph_objs.Bar(x=["basal", "induccion", "mantenimiento", "despertar", "recuperacion"], y=[porcentajes_basal[2], porcentajes_induccion[2], porcentajes_mantenimiento[2], porcentajes_despertar[2], porcentajes_recuperacion[2]], marker_color="rgb(255, 217, 47)", name="Excesivo", offsetgroup="Excesivo", legendgroup="Excesivo", hovertemplate = "<br>Estado: %{x} <br>Porcentaje: %{y:.2f} %")
PorcentajesSPI.add_trace(insuficientes)
PorcentajesSPI.add_trace(adecuados)
PorcentajesSPI.add_trace(excesivos)
PorcentajesSPI.update_layout(title="Porcentajes SPI por estado", legend_title_text = "Referencias:")
PorcentajesSPI.update_yaxes(title_text="% SPI")
PorcentajesSPI.update_xaxes(range=(-0.5, 4.5))

colors = ['rgb(190, 213, 242)', 'rgb(244, 202, 225)', 'rgb(179, 236, 225)', 'rgb(232, 203, 248)', 'rgb(253, 205, 152)']#
shapes = []
bgs = [[-0.5, 0.5], [0.5, 1.5], [1.5, 2.5], [2.5, 3.5], [3.5, 4.5]]
for i, b in enumerate(bgs):
    shapes.append(dict(type="rect", xref="x", yref="paper", x0=b[0], y0=0, x1=b[1], y1=1, fillcolor=colors[i], opacity=0.8, layer="below", line_width=0))
PorcentajesSPI.update_layout(yaxis=dict(showgrid=False), shapes=shapes)

# Guarda la imagen estática del gráfico dinámico
PorcentajesSPI.write_image(f"{directorio_actual}/{'figPorcentajesSPI.jpg'}")

