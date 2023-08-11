import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from openpyxl import load_workbook

#########################################################################################################################
# FUNCIONES: 

# Función que genera la distribución gaussiana con una media y desvío dados 
def funcDistribGaussiana(x, media, desvio):
    coeficiente = 1 / (desvio * np.sqrt(2 * np.pi))
    exponente = -((x - media) ** 2) / (2 * desvio ** 2)
    return coeficiente * np.exp(exponente)

#########################################################################################################################
# CREACIÓN DE LAS TRANSFORMACIONES Y LAS GUARDA:

# Obtiene las listas de los valores de los parámetros registrados del excel
directorio_actual = os.path.abspath(os.path.dirname(__file__))
nombre_excel_normalizacion = 'Curva Normalizacion.xlsx'
path_normalizacion = os.path.join(directorio_actual, nombre_excel_normalizacion)
excel_normalizacion = pd.read_excel(path_normalizacion)
# Obtiene las listas 
# HBI
lista_poblacional_HBI = excel_normalizacion['HBI']
# PPGA 
lista_poblacional_PPGA = excel_normalizacion['PPGA']

# Obtiene los valores mínimo y máximo de los parámetros para generar los vectores de entrada y calcular los de salida mediante la función de distribución gaussiana
# HBI
min_poblacional_HBI = np.min(lista_poblacional_HBI)
max_poblacional_HBI = np.max(lista_poblacional_HBI)
x_HBI = np.linspace(min_poblacional_HBI, max_poblacional_HBI, max_poblacional_HBI-min_poblacional_HBI+1)
media_poblacional_HBI = np.mean(lista_poblacional_HBI)
desvio_poblacional_HBI = np.std(lista_poblacional_HBI)
y_HBI = funcDistribGaussiana(x_HBI, media_poblacional_HBI, desvio_poblacional_HBI)
# PPGA
min_poblacional_PPGA = np.min(lista_poblacional_PPGA)
max_poblacional_PPGA = np.max(lista_poblacional_PPGA)
x_PPGA = np.linspace(min_poblacional_PPGA, max_poblacional_PPGA, max_poblacional_PPGA-min_poblacional_PPGA+1)
media_poblacional_PPGA = np.mean(lista_poblacional_PPGA)
desvio_poblacional_PPGA = np.std(lista_poblacional_PPGA)
y_PPGA = funcDistribGaussiana(x_PPGA, media_poblacional_PPGA, desvio_poblacional_PPGA)

# Guarda las distribuciones en los excels:
nombre_excel_distribuciones = 'Curva Normalizacion Gaussiana.xlsx'
path_excel_distribuciones = os.path.join(directorio_actual, nombre_excel_distribuciones)
excel_distribuciones = load_workbook(path_excel_distribuciones)

y_HBI = y_HBI.tolist()
y_PPGA = y_PPGA.tolist()
max_length = max(len(y_HBI), len(y_PPGA))
y_HBI += [None] * (max_length - len(y_HBI))
y_PPGA += [None] * (max_length - len(y_PPGA))
df_distribuciones = pd.DataFrame({'HBI': y_HBI, 'PPGA': y_PPGA})
df_distribuciones.to_excel(path_excel_distribuciones, index=False, header=True)


#########################################################################################################################
# GRÁFICOS: 

# Crea las gráficas
# HBI
plt.plot(x_HBI, y_HBI, label='Distribución Normal')
plt.xlabel('x')
plt.ylabel('Probabilidad')
plt.title('Distribución Normal con Media y Desviación Estándar poblacionales')
plt.legend()
plt.grid(True)
plt.show()
# PPAG 
plt.plot(x_PPGA, y_PPGA, label='Distribución Normal')
plt.xlabel('x')
plt.ylabel('Probabilidad')
plt.title('Distribución Normal con Media y Desviación Estándar 1 poblacionales')
plt.legend()
plt.grid(True)
plt.show()

