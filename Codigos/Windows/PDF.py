import os
from reportlab.pdfgen.canvas import Canvas
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib.utils import ImageReader

from InputDatosPaciente import listaDatosPaciente, id_global_principal, fecha, hora
from Principal import listaInicioEstados, listaTiemposEventos, listaEventos
from Principal import porcentajes

###############################################################################################################

# Obtén la ruta absoluta del directorio actual
directorio_actual = os.path.abspath(os.path.dirname(__file__))
nombrepdf = 'Informe ' + id_global_principal + '.pdf'

# Crea el canvas para el informe
pdf = Canvas(os.path.join(directorio_actual, nombrepdf), pagesize=(612.0, 792.0))

# Se definen los formatos de texto
font_size_titulo_principal = 21
font_size_titulo_secundario = 18
font_size_subtitulo = 14
font_size_enumerado = 12
font_size_texto = 10

pdf.setFont("Times-Roman", font_size_texto)

renglon = 750
interlineado = 15
sangria_informe = 40
sangria_bullets = 50
sangria_texto = 70

# Contador de renglones para ir seteando las ubicaciones de los textos y hacer los saltos de página
global n_renglones
n_renglones = 0

###############################################################################################################
# FECHA Y HORA
# Escribe la fecha y hora del inicio del monitoreo en el pdf
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Fecha monitoreo: " + fecha.strftime("%Y-%m-%d"))
n_renglones += 1
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Hora inicio monitoreo: " + hora.strftime("%H:%M:%S"))
n_renglones += 1
pdf.line(sangria_informe, renglon-interlineado*n_renglones, 612-sangria_informe, renglon-interlineado*n_renglones)
n_renglones += 1

###############################################################################################################
# TITULO
# Escribe como título del informe el ID del paciente 
n_renglones += 1
id = listaDatosPaciente[2]
pdf.setFont("Times-Roman", font_size_titulo_principal)
pdf.drawCentredString(300, renglon-interlineado*n_renglones, "Informe de Monitoreo de Nocicepcion - " + id)

###############################################################################################################
# DATOS DEL PACIENTE
# Escribe los datos del paciente: nombre, apellido y ID
n_renglones += 2
nombre = listaDatosPaciente[0]
apellido = listaDatosPaciente[1]

pdf.setFont("Times-Roman", font_size_subtitulo)
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Datos del paciente:")

n_renglones += 2
pdf.setFont("Times-Roman", font_size_texto)
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Nombre: " + nombre)
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Apellido: " + apellido)
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - ID: " + id)
n_renglones += 1

###############################################################################################################
# ESTADOS DEL PACIENTE
# Escribe los tiempos de inicio de los distintos estados del paciente y el tiempo total de duración del monitoreo
n_renglones += 2
hora_basal = listaInicioEstados[0]
hora_inic_anest = listaInicioEstados[1]
hora_inic_cirug = listaInicioEstados[2]
hora_fin_cirug = listaInicioEstados[3]
hora_fin_anest = listaInicioEstados[4]
duracion = listaInicioEstados[5]

pdf.setFont("Times-Roman", font_size_subtitulo)
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Tiempos de cambios de estado del paciente:")
n_renglones += 1

pdf.setFont("Times-Roman", font_size_texto)
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Basal: " + hora_basal)
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Inicio anestesia: " + hora_inic_anest)
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Inicio cirugia: " + hora_inic_cirug)
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Fin cirugia: " + hora_fin_cirug)
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Fin anestesia: " + hora_fin_anest)
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Duracion total de monitoreo: " + duracion)
n_renglones += 1

###############################################################################################################
# EVENTOS
# Escribe los eventos con sus tiempos de ocurrencia separador por el tipo de evento: suministro de fármacos analgésicos, procedimientos quirúrgicos e intercurrencias
n_renglones += 2

lista_farmaco = []
lista_procQuirurgico = []
lista_Intercurrencia = []

for i in range (len(listaEventos)):
    if listaEventos[i][0] == "Farmaco":
        lista_farmaco.append([listaEventos[i], listaTiemposEventos[i]])
    elif listaEventos[i][0] == "ProcQuirurgico":    
        lista_procQuirurgico.append([listaEventos[i], listaTiemposEventos[i]])
    elif listaEventos[i][0] == "Intercurrencia":    
        lista_Intercurrencia.append([listaEventos[i], listaTiemposEventos[i]])

pdf.setFont("Times-Roman", font_size_subtitulo)
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Eventos ingresados:")
n_renglones += 1

pdf.setFont("Times-Roman", font_size_enumerado)
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Farmacos analgesicos:")
n_renglones += 1

# Función que chequea si se supera la cantidad de renglones disponibles en una página, y en ese caso crea una página nueva 
def funcChequearRenglones(interlineado = 15):
    global n_renglones
    if n_renglones*interlineado >= 792.0:
        pdf.showPage()
        pdf.setFont("Times-Roman", font_size_texto)
        interlineado = 15
        n_renglones = 2

pdf.setFont("Times-Roman", font_size_texto)

for i in range(len(lista_farmaco)):
    funcChequearRenglones()
    pdf.drawString(sangria_texto, renglon-interlineado*n_renglones, "         - " + lista_farmaco[i][1] + " - " + lista_farmaco[i][0][1])
    n_renglones += 1

n_renglones += 1

funcChequearRenglones()
pdf.setFont("Times-Roman", font_size_enumerado)
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Procedimientos quirurgicos:")
n_renglones += 1

pdf.setFont("Times-Roman", font_size_texto)

for i in range(len(lista_procQuirurgico)):
    funcChequearRenglones()
    pdf.drawString(sangria_texto, renglon-interlineado*n_renglones, "         - " + lista_procQuirurgico[i][1] + " - " + lista_procQuirurgico[i][0][1])
    n_renglones += 1

n_renglones += 1

funcChequearRenglones()
pdf.setFont("Times-Roman", font_size_enumerado)
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "   - Intercurrencias:")
n_renglones += 1

pdf.setFont("Times-Roman", font_size_texto)

for i in range(len(lista_Intercurrencia)):
    funcChequearRenglones()
    pdf.drawString(sangria_texto, renglon-interlineado*n_renglones, "         - " + lista_Intercurrencia[i][1] + " - " + lista_Intercurrencia[i][0][1])
    n_renglones += 1

n_renglones += 1

pdf.showPage()

###############################################################################################################
# NUEVA PÁGINA: Gráficos de evolución del índice de nocicepción SPI durante el monitoreo 
# Título
renglon = 750
interlineado = 15
n_renglones = 2
pdf.setFont("Times-Roman", font_size_titulo_secundario)
pdf.drawCentredString(300, renglon-interlineado*n_renglones, "Evolucion del indice de nocicepcion durante el monitoreo")
n_renglones += 3

# Referecia de interpretación del índice
pdf.setFont("Times-Roman", font_size_enumerado)
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Referencia de interpretacion del indice SPI:")
n_renglones += 2

pdf.setFont("Times-Roman", font_size_texto)
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "         - Analgesia insuficiente:  50 < SPI")
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "         - Analgesia adecuada:  20 < SPI < 50")
n_renglones += 1
pdf.drawString(sangria_bullets, renglon-interlineado*n_renglones, "         - Analgesia excesiva:  SPI < 20")
n_renglones += 1

n_renglones += 2

# Gráficos de evolución del índice: por franjas de interpretación y por estados
pdf.setFont("Times-Roman", font_size_enumerado)
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Graficos de evolucion del indice SPI en el tiempo:")

n_renglones += 18

# Imagen grafico evolucion SPI por franjas
# Ruta relativa de la imagen
ruta_relativa = os.path.join(directorio_actual, 'figSPIFranjas.jpg')
figSPIFranjas = ImageReader(ruta_relativa)
pdf.drawImage(figSPIFranjas, x=45, y=renglon-interlineado*n_renglones, width=500, height=255)

n_renglones += 17

# Imagen grafico evolucion SPI por estados 
# Ruta relativa de la imagen
ruta_relativa = os.path.join(directorio_actual, 'figSPIEstados.jpg')
figSPIEstados = ImageReader(ruta_relativa)
pdf.drawImage(figSPIEstados, x=40, y=renglon-interlineado*n_renglones, width=550, height=255)

pdf.showPage()

###############################################################################################################
# NUEVA PÁGINA: de tiempo por estado en el que el indice se encontro en cada franja de valores de SPI
renglon = 750
interlineado = 15
n_renglones = 3

pdf.setFont("Times-Roman", font_size_enumerado)
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Porcentajes por estado:")
n_renglones += 2

pdf.setFont("Times-Roman", font_size_texto)
pdf.drawString(sangria_informe, renglon-interlineado*n_renglones, "Porcentaje de tiempo por estado en el que el indice se encontro en cada franja de valores de SPI.")
n_renglones += 2

# En formato de tabla 
data = [
    [' Estado \ SPI ', ' 50 < ', ' 20 < & < 50 ', ' < 20 '],
    ['Basal', str(round(porcentajes[0][0]))+'%', str(round(porcentajes[0][1]))+'%', str(round(porcentajes[0][2]))+'%'],
    ['Induccion', str(round(porcentajes[1][0]))+'%', str(round(porcentajes[1][1]))+'%', str(round(porcentajes[1][2]))+'%'],
    ['Mantenimiento', str(round(porcentajes[2][0]))+'%', str(round(porcentajes[2][1]))+'%', str(round(porcentajes[2][2]))+'%'],
    ['Despertar', str(round(porcentajes[3][0]))+'%', str(round(porcentajes[3][1]))+'%', str(round(porcentajes[3][2]))+'%'],
    ['Recuperacion', str(round(porcentajes[4][0]))+'%', str(round(porcentajes[4][1]))+'%', str(round(porcentajes[4][2]))+'%'],
]

width, height = letter
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightseagreen),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
]))
tw, th, = table.wrapOn(pdf, width, height)
x = sangria_informe + 150
y = renglon-interlineado*n_renglones

table.drawOn(pdf, x, y-th)

n_renglones += 30

# Imagen de gráfico de porcentajes
# Ruta relativa de la imagen
ruta_relativa = os.path.join(directorio_actual, 'figPorcentajesSPI.jpg')
figPorcentajesSPI = ImageReader(ruta_relativa)
pdf.drawImage(figPorcentajesSPI, x=105, y=renglon-interlineado*n_renglones, width=400, height=300)

pdf.showPage()

###############################################################################################################
# Guarda el informe
pdf.save()
