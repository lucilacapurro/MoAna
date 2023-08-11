import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy import signal
from openpyxl import load_workbook
import os
from numpy.core.function_base import linspace

############################################################################################################################################
# FUNCIONES

# Función para obtener la señal de PPG a partir de los valores de R e IR 
def funcLevantarSenal(path_ppg):
  df_ppg = pd.read_csv(path_ppg)
  t_ppg = df_ppg['Tiempo']
  senal_ppg_R = -df_ppg['redVal']
  senal_ppg_IR = -df_ppg['irVal']
  # PPG(t) = Absorción de luz roja(t) - Absorción de luz infrarroja(t)
  senal_ppg = senal_ppg_R-senal_ppg_IR
  return senal_ppg

# Función para visualizar la señal de PPG 
def funcVisualizar(senal, fs, label, scatterX = 0, scatterY = 0, scatter = False): # scatterX está en muestras --> genera vector tiempos = muestras/fs 
  L = len(senal)
  t = np.linspace(0,L/fs,L)
  plt.figure(figsize=(25,5))
  plt.plot(t,senal, 'y')
  if (scatter == True): 
    plt.scatter(scatterX/fs, scatterY)
  plt.ylabel('Amplitud', fontsize=14)
  plt.xlabel('Tiempo [s]', fontsize=14)
  plt.title(label, fontsize=14)
  plt.show()

# Función para filtrar la señal con un filtro pasa bajos 
def funcFiltroLP(senal, orden, fc, fs):
  [b,a] = signal.butter(orden, fc, btype = 'lowpass', analog = False, output = 'ba', fs = fs)
  senalLP = signal.filtfilt(b, a, senal)
  return senalLP

# Función para filtrar la señal con un filtro pasa altos
def funcFiltroHP(senal, orden, fc, fs):
  [b,a] = signal.butter(orden, fc, btype = 'highpass', analog = False, output = 'ba', fs = fs)
  senalHP = signal.filtfilt(b, a, senal)
  return senalHP

# Función para detectar picos 
def funcDetectarPicos(senal_ppg_filtrada):
  picos = signal.find_peaks(senal_ppg_filtrada)[0]
  return picos

# Función para eliminar picos erróneos 
def funEliminarPicosSubida(senal_ppg, locs_peaks_ppg):
  locs_peaks_ppg_correctos = []
  locs_peaks_ppg_correctos.append(locs_peaks_ppg[0])
  for loc in range(1, len(locs_peaks_ppg)):
    if (locs_peaks_ppg[loc]+30) < len(senal_ppg):
        if senal_ppg[locs_peaks_ppg[loc]+30] < senal_ppg[locs_peaks_ppg[loc]]:
            locs_peaks_ppg_correctos.append(locs_peaks_ppg[loc])
    else:
        locs_peaks_ppg_correctos.append(locs_peaks_ppg[loc])
  return np.array(locs_peaks_ppg_correctos)

# Función para eliminar picos erróneos 
def funcEliminarPicosOutliers(locs_peaks_ppg, low_rri, high_rri):
  locs_peaks_ppg_limpio = []
  locs_peaks_ppg_limpio.append(locs_peaks_ppg[0])
  for i in range(1,len(locs_peaks_ppg)):
    intervalo = locs_peaks_ppg[i]-locs_peaks_ppg_limpio[-1]
    if high_rri >= intervalo >= low_rri:
      locs_peaks_ppg_limpio.append(locs_peaks_ppg[i])
  return np.array(locs_peaks_ppg_limpio)

# Función para eliminar picos distólicos
def funcEliminarDiastolicos(senal_ppg, locs_peaks_ppg):
  locs_peaks_ppg_sistolicos = []
  locs_peaks_ppg_sistolicos.append(locs_peaks_ppg[0])
  for loc in range(1, len(locs_peaks_ppg)):
    if senal_ppg[locs_peaks_ppg[loc]-30] < senal_ppg[locs_peaks_ppg[loc]]:
      locs_peaks_ppg_sistolicos.append(locs_peaks_ppg[loc])
  return np.array(locs_peaks_ppg_sistolicos)

# Función para detectar onsets
def funcDetectarOnsets(senal_ppg, locs_peaks_ppg):
  locs_onsets_ppg = []
  for i in range(len(locs_peaks_ppg)-1):
    locs_onsets_ppg.append(np.argmin(senal_ppg[locs_peaks_ppg[i]:locs_peaks_ppg[i+1]])+locs_peaks_ppg[i])
  return np.array(locs_onsets_ppg)

# Función para calcular el parámetro HBI como la diferencia temporal entre picos consecutivos
def funcHBI(locs_peaks_ppg_limpios):
  HBI = [j-i for i,j in zip(locs_peaks_ppg_limpios[0:-1], locs_peaks_ppg_limpios[1:])]
  return HBI

# Función para calcular el parámetro PPGA como la diferencia de amplitud entre onset y pico consecutivos 
def funcPPGA(senal_ppg, locs_peaks, locs_onsets):
  if locs_onsets[0]>locs_peaks[0]:
    locs_peaks = locs_peaks[1:]
  PPGA = [int(senal_ppg[peak]-senal_ppg[onset]) for peak,onset in zip(locs_peaks, locs_onsets)]
  return PPGA


############################################################################################################################################

# CAMBIAR NOMBRE DEL ARCHIVO CSV DE LOS DATOS A UTILIZAR
nombre_csv = 'datavicky2.csv'

directorio_actual = os.path.abspath(os.path.dirname(__file__))
nombre_csv_senal_ppg = nombre_csv
path_csv_ppg = os.path.join(directorio_actual, nombre_csv_senal_ppg)
senal_ppg = funcLevantarSenal(path_csv_ppg)

# CAMBIAR LA PORCIÓN DE LA SEÑAL A UTILIZAR 
senal_ppg = senal_ppg[50:8200]

fs=100

# Filtra la señal 
senal_ppg_HP = funcFiltroHP(senal = senal_ppg, orden = 3, fc = 0.35, fs = fs)
senal_ppg_LP = funcFiltroLP(senal = senal_ppg_HP, orden = 3, fc = 5, fs = fs)

# Detecta y limpia los picos 
locs_peaks_ppg = funcDetectarPicos(senal_ppg_LP)
locs_peaks_ppg_no_subida = funEliminarPicosSubida(senal_ppg_LP, locs_peaks_ppg)
locs_peaks_ppg_sistolicos = funcEliminarDiastolicos(senal_ppg_LP, locs_peaks_ppg_no_subida)
locs_peaks_ppg_sin_outliers = funcEliminarPicosOutliers(locs_peaks_ppg_sistolicos, low_rri = 40, high_rri = 180)
locs_onsets_ppg = funcDetectarOnsets(senal_ppg_LP, locs_peaks_ppg_sin_outliers)

# Calcula los parámetros HBI y PPGA 
PPGA = funcPPGA(senal_ppg_LP, locs_peaks_ppg_sin_outliers, locs_onsets_ppg)
HBI = funcHBI(locs_peaks_ppg_sin_outliers)

# Agrega los valores al excel de valores 
directorio_actual = os.path.abspath(os.path.dirname(__file__))
nombre_excel_normalizacion = 'Curva Normalizacion.xlsx'
path_normalizacion = os.path.join(directorio_actual, nombre_excel_normalizacion)
excel_normalizacion = load_workbook(path_normalizacion)
hoja_excel_normalizacion = excel_normalizacion['Hoja1']
for i in range(len(HBI)):
    nueva_medicion = [HBI[i], PPGA[i]]
    hoja_excel_normalizacion.append(nueva_medicion)

# Guarda el excel 
excel_normalizacion.save(path_normalizacion)