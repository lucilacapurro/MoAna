import csv
import time
import serial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import copy
import os
from scipy.stats import entropy

############################################################################################################################################
# FUNCIONES

def funcLevantarSenal(path_ppg):
  df_ppg = pd.read_csv(path_ppg)
  senal_ppg = df_ppg['PPG']
  return senal_ppg

def funcEntropiaVentana(ventana_senal):
  value, counts = np.unique(ventana_senal, return_counts = True)
  return entropy(counts)

def funcDetectarEntropia(ventana_senal, umbral):
  entropia_ventana = funcEntropiaVentana(ventana_senal)
  if entropia_ventana < umbral:
    return True
  else:
    return False
  
def funcDetectarDesconexionSensor(ventana_senal, umbral = 80):
  largo_ventana = len(ventana_senal)
  cant_muestras_ruido = sum(1 for muestra in ventana_senal if abs(muestra) > 16000000)
  porcentaje_ruido = (cant_muestras_ruido / largo_ventana) * 100
  if porcentaje_ruido > umbral:
    return True
  else:
    return False

def funcDetectarDesconexionDedo(ventana_senal, umbral = 80):
  largo_ventana = len(ventana_senal)
  cant_muestras_ruido = sum(1 for muestra in ventana_senal if abs(muestra) == 2096921)
  porcentaje_ruido = (cant_muestras_ruido / largo_ventana) * 100
  if porcentaje_ruido > umbral:
    return True
  else:
    return False
  
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

def funcFiltroBP(senal, orden, f1, f2, fs):
  frecscorte = [f1,f2]
  [b,a] = signal.butter(orden, frecscorte, btype = 'bandpass', analog = False, output = 'ba', fs = fs)
  senalBP = signal.filtfilt(b, a, senal)
  return senalBP

def funcFiltroLP(senal, orden, fc, fs):
  [b,a] = signal.butter(orden, fc, btype = 'lowpass', analog = False, output = 'ba', fs = fs)
  senalLP = signal.filtfilt(b, a, senal)
  return senalLP

def funcFiltroHP(senal, orden, fc, fs):
  [b,a] = signal.butter(orden, fc, btype = 'highpass', analog = False, output = 'ba', fs = fs)
  senalHP = signal.filtfilt(b, a, senal)
  return senalHP

def funcEncontrarPosicion(array, valor):
  for i, elemento in enumerate(array):
    if elemento >= valor:
      return i
    
def funcFiltrar(senal_ppg, fs, HR, orden=3):
  if HR < 60:
    fmin = 0.1
    fmax = 1.5
  elif HR < 100:
    fmin = 0.35
    fmax = 2.5
  elif HR < 180:
    fmin = 0.5
    fmax = 3.5
  else:
    fmin = 1
    fmax = 4.5
  senal_ppg_HP = funcFiltroHP(senal = senal_ppg, orden = orden, fc = fmin, fs = fs)
  senal_ppg_LP = funcFiltroLP(senal = senal_ppg_HP, orden = orden, fc = fmax, fs = fs)
  return senal_ppg_LP

def funcObtenerHR(senal_ppg, f1, f2, fs):
  senal_ppg_BP = funcFiltroBP(senal=senal_ppg, orden=3, f1=f1, f2=f2, fs=fs) # de 30bpm a 240 bpm tengo de 0.5 a 4 Hz --> doy margen y filtro de 0.1 a 6 
  # Aplica la FFT a la señal de PPG
  fft_result = np.fft.fft(senal_ppg_BP)
  fft_freqs = np.fft.fftfreq(len(senal_ppg_BP), 1/fs)
  # Encuentra el pico dominante en la FFT (frecuencia cardíaca)
  x_min = funcEncontrarPosicion(fft_freqs, 0.5)
  x_max = funcEncontrarPosicion(fft_freqs, 5) # limito que cubra de 0,5 a 5 Hz = 30 a 300 latidos por min
  positive_freqs = fft_freqs[:len(fft_freqs)//2][x_min:x_max]
  positive_result = fft_result[:len(fft_result)//2][x_min:x_max]
  magnitude_spectrum = np.abs(positive_result)
  max_peak_index = np.argmax(magnitude_spectrum)
  # Encuentra la frecuencia cardíaca dominante
  dominant_freq = positive_freqs[max_peak_index]
  heart_rate = dominant_freq * 60  # Convierte de Hz a latidos por minuto
  '''
  # Grafica la FFT y el pico dominante
  plt.subplot(2, 1, 2)
  plt.plot(positive_freqs, magnitude_spectrum)
  plt.plot(positive_freqs[max_peak_index], magnitude_spectrum[max_peak_index], 'ro')
  plt.title(f"FFT - Frecuencia Cardíaca: {heart_rate:.2f} bpm")
  plt.xlabel("Frecuencia (Hz)")
  plt.grid()
  plt.xlim(0.5, 5)
  plt.ylim(0, 10000000)
  plt.tight_layout()
  plt.show()
  '''
  print(f"Frecuencia Cardíaca estimada: {heart_rate:.2f} bpm")
  return heart_rate


def funcDetectarPicos(senal_ppg_filtrada):
  picos = signal.find_peaks(senal_ppg_filtrada)[0]
  return picos

def funcEliminarPicosSubida(senal_ppg, locs_peaks_ppg, HR, fs):
  umbral = int((60/HR)*fs/4)
  locs_peaks_ppg_correctos = []
  locs_peaks_ppg_correctos.append(locs_peaks_ppg[0])
  for loc in range(1, len(locs_peaks_ppg)):
    if (locs_peaks_ppg[loc]+umbral) < len(senal_ppg):
        if senal_ppg[locs_peaks_ppg[loc]+umbral] < senal_ppg[locs_peaks_ppg[loc]]:
            locs_peaks_ppg_correctos.append(locs_peaks_ppg[loc])
    else:
        locs_peaks_ppg_correctos.append(locs_peaks_ppg[loc])
  return np.array(locs_peaks_ppg_correctos)

def funcEliminarPicosOutliers(locs_peaks_ppg, low_rri, high_rri):
  locs_peaks_ppg_limpio = []
  locs_peaks_ppg_limpio.append(locs_peaks_ppg[0])
  for i in range(1,len(locs_peaks_ppg)):
    intervalo = locs_peaks_ppg[i]-locs_peaks_ppg_limpio[-1]
    if high_rri >= intervalo >= low_rri:
      locs_peaks_ppg_limpio.append(locs_peaks_ppg[i])
  return np.array(locs_peaks_ppg_limpio)

def funcEliminarDiastolicos(senal_ppg, locs_peaks_ppg, HR, fs): # "funEliminarPicosBajada"
  umbral = int((60/HR)*fs/4)
  locs_peaks_ppg_sistolicos = []
  locs_peaks_ppg_sistolicos.append(locs_peaks_ppg[0])
  for loc in range(1, len(locs_peaks_ppg)):
    if senal_ppg[locs_peaks_ppg[loc]-umbral] < senal_ppg[locs_peaks_ppg[loc]]:
      locs_peaks_ppg_sistolicos.append(locs_peaks_ppg[loc])  
  return np.array(locs_peaks_ppg_sistolicos)

def funcDetectarOnsets(senal_ppg, locs_peaks_ppg):
  locs_onsets_ppg = []
  for i in range(len(locs_peaks_ppg)-1):
    locs_onsets_ppg.append(np.argmin(senal_ppg[locs_peaks_ppg[i]:locs_peaks_ppg[i+1]])+locs_peaks_ppg[i])
  return np.array(locs_onsets_ppg)

def funcHBI(locs_peaks_ppg_limpios):
  HBI = [j-i for i,j in zip(locs_peaks_ppg_limpios[0:-1], locs_peaks_ppg_limpios[1:])]
  return HBI

def funcPPGA(senal_ppg, locs_peaks, locs_onsets):
  if locs_onsets[0]>locs_peaks[0]:
    locs_peaks = locs_peaks[1:]
  PPGA = [int(senal_ppg[peak]-senal_ppg[onset]) for peak,onset in zip(locs_peaks, locs_onsets)]
  return PPGA


def funcProcesamiento(senal_ppg, fs, HR):
  locs_peaks_ppg = funcDetectarPicos(senal_ppg)
  locs_peaks_ppg_no_subida = funcEliminarPicosSubida(senal_ppg, locs_peaks_ppg, HR, fs)
  locs_peaks_ppg_sistolicos = funcEliminarDiastolicos(senal_ppg, locs_peaks_ppg_no_subida, HR, fs)
  #funcVisualizar(senal_ppg, fs, "Detección de picos", locs_peaks_ppg_sistolicos, senal_ppg[locs_peaks_ppg_sistolicos], scatter = True)
  locs_onsets_ppg = funcDetectarOnsets(senal_ppg, locs_peaks_ppg_sistolicos)
  #funcVisualizar(senal_ppg, fs, "Detección de onsets", locs_onsets_ppg, senal_ppg[locs_onsets_ppg], scatter = True)
  PPGA = funcPPGA(senal_ppg, locs_peaks_ppg_sistolicos, locs_onsets_ppg)
  HBI = funcHBI(locs_peaks_ppg_sistolicos)
  return PPGA, HBI


def funcSPIi(PPGAi_norm, HBIi_norm):
  SPIi = 100 - (0.67*PPGAi_norm+0.33*HBIi_norm)*100
  return int(SPIi)

def funcPromedio(vector_valores):
  prom = np.mean(vector_valores)
  return int(prom)

def funcNormalizarParametro(TF_normalizacion, parametro):
  parametro = int(parametro)
  min = TF_normalizacion[0][0]
  parametro_norm = TF_normalizacion[parametro-min][1]
  return parametro_norm


# Levantamos las funciones de normalizacion 

directorio_actual = os.path.abspath(os.path.dirname(__file__))
nombre_excel_TF_HBI = 'TF_HBI_Gaussiana.xlsx'
path_excel_TF_HBI = os.path.join(directorio_actual, nombre_excel_TF_HBI)
df_TF_HBI = pd.read_excel(path_excel_TF_HBI)
TF_HBI = df_TF_HBI.values.tolist()
TF_HBI = list(map(lambda x: [int(x[0])] + x[1:], TF_HBI))

nombre_excel_TF_PPGA = 'TF_PPGA_Gaussiana.xlsx'
path_excel_TF_PPGA = os.path.join(directorio_actual, nombre_excel_TF_PPGA)
path_excel_TF_PPGA = os.path.join(directorio_actual, nombre_excel_TF_PPGA)
df_TF_PPGA = pd.read_excel(path_excel_TF_PPGA)
TF_PPGA = df_TF_PPGA.values.tolist()
TF_PPGA = list(map(lambda x: [int(x[0])] + x[1:], TF_PPGA))

############################################################################################################################################