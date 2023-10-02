from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QIODevice, Qt, QByteArray
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QLCDNumber
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy import signal
import pandas as pd
import plotly
import plotly.express as px
import os
import pygame #winsound
from openpyxl import load_workbook
import copy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import pyqtgraph as pg
import csv
import time
import serial

from ProcesamientoOnline import funcEntropiaVentana, funcDetectarEntropia, funcDetectarDesconexion, funcDetectarPicos, funcEliminarPicosSubida, funcEliminarPicosOutliers, funcEliminarDiastolicos, funcDetectarOnsets, funcHBI, funcPPGA, funcSPIi, funcPromedio, funcNormalizarParametro, TF_HBI, TF_PPGA

global fs 
fs = 25

global largo
largo = 3*fs

global muestra
muestra = -1

global muestra_evento
muestra_evento = -largo

global lista_estado
lista_estado = ["-"]

global lista_evento
lista_evento = ["-"]    # es la lista completa para cada SPI que incluye los "-"

global lista_alarma
lista_alarma = ["-"]

global estado
estado = "-"

global evento
evento = "-"

global alarma
alarma = "-"

global alarmas_seteadas
alarmas_seteadas = "-"

global cant_spi_a_prom
cant_spi_a_prom = 4

global spi_promedio
spi_promedio = np.nan

global nuevo_valor_filtrado
nuevo_valor_filtrado = np.nan

global ppg
ppg = 0

global SPI
SPI = np.nan

global ventana_ppg
ventana_ppg = [0]*largo

global lista_individual_HBI
lista_individual_HBI = []

global lista_individual_PPGA
lista_individual_PPGA = []

global TF_HBI_combinada
TF_HBI_combinada = [[],[]]

global TF_PPGA_combinada
TF_PPGA_combinada = [[],[]]

global ventana_SPI
ventana_SPI = int(10 * 60 * 60 * fs / largo) # 10 horas

global tiempo_condicion
tiempo_condicion = 0

global restablecido
restablecido = False

global contador_error_sensor
contador_error_sensor = 0

global ejecutar_alarma_auditiva
ejecutar_alarma_auditiva = True

listaInicioEstados = []
listaEventos = [] # contiene la lista de los eventos ingresados
listaTiemposEventos = [] # contiene la lista de los tiempos de los eventos ingresados

directorio_actual = os.path.abspath(os.path.dirname(__file__))

excel_eventos = 'Registro Eventos.xlsx'
path_excel_eventos = os.path.join(directorio_actual, excel_eventos)
df_lista_eventos = pd.read_excel(path_excel_eventos)
global farmacos
farmacos = df_lista_eventos['farmacos'].dropna().to_list()
global procedimientos
procedimientos = df_lista_eventos['procedimientos'].dropna().to_list()
global intercurrencias
intercurrencias = df_lista_eventos['intercurrencias'].dropna().to_list()


########################################################################################################################################################

# Function to send a message from PC to board
def send_message(ser, hex_bytes):
    data_to_send = bytes(hex_bytes)
    ser.write(QByteArray(data_to_send))

# Function to read a message sent from board to PC
def read_message(ser, n_bytes):
    response = ser.read(n_bytes)
    return response

# Function to write a register
def write_register(ser, address, data):
    message = [0x02, address[0], address[1], data[0], data[1], data[2], data[3], data[4], data[5], 0x0D]
    send_message(ser, message)

# Function to read a register
def read_register(ser, address):
    message = [0x03, address[0], address[1], 0x0D]
    send_message(ser, message)
    data_bytes = read_message(ser, n_bytes=7)
    raw_data = data_bytes[2:5]
    decimal_value = int.from_bytes(raw_data, byteorder='little')
    return decimal_value

global prev_data
prev_data = None

global data
data = []

class SerialCommunication(QThread):

    data_received = pyqtSignal(str)
    
    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None

    def run(self):
        self.serial_port = serial.Serial(self.port, self.baudrate)
        nueva_muestra = 0
        cant_muestras = 0

        print("Inicio de adquisicion de datos.")

        while self.serial_port and self.serial_port.is_open:
            global prev_data
            if nueva_muestra == 0:
                prev_data = -read_register(self.serial_port, address=[0x32, 0x43])
                nueva_muestra += 1
            else:
                new_data = -read_register(self.serial_port, address=[0x32, 0x43])
                    
                nueva_muestra += 1
                
                print("nuevo val")
                if new_data != prev_data:

                    global data
                    data.append(new_data)

                    cant_muestras += 1

                    print(new_data)

                    if cant_muestras%20==0:
                        print("emite señal")
                        self.data_received.emit(str(new_data))

                    prev_data = new_data 


########################################################################################################################################################

class Ui_DisplayPrincipal(object):

    #############################################################################################
    #Funciones para abrir otras ventanas
    def openAjusteVisualizacionGraficaSPI(self):
        from AjustarVisualizacionSPI import Ui_AjusteVisualizacionGraficaSPI
        self.windowAjusteVisualizacionGraficaSPI = QtWidgets.QMainWindow()
        self.ui = Ui_AjusteVisualizacionGraficaSPI()
        self.ui.setupUi(self.windowAjusteVisualizacionGraficaSPI)
        self.windowAjusteVisualizacionGraficaSPI.show()
        # Establecer la posición de la nueva ventana en la pantalla
        self.windowAjusteVisualizacionGraficaSPI.move(320, 345)
        global restablecido
        restablecido = False

    def openSetUpAlarmas(self):
        from SetUpAlarmas import Ui_SetUpAlarmas
        self.windowSetUpAlarmas = QtWidgets.QMainWindow()
        self.ui = Ui_SetUpAlarmas()
        self.ui.setupUi(self.windowSetUpAlarmas)
        self.windowSetUpAlarmas.show() 
        # Establecer la posición de la nueva ventana en la pantalla
        self.windowSetUpAlarmas.move(280, 340)        

    def openOpcionesInforme(self):
        from OpcionesInforme import Ui_OpcionesInforme
        self.windowOpcionesInforme = QtWidgets.QMainWindow()
        self.ui = Ui_OpcionesInforme()
        self.ui.setupUi(self.windowOpcionesInforme)
        self.windowOpcionesInforme.show()

    #############################################################################################

    def setupUi(self, DisplayPrincipal):
        DisplayPrincipal.setObjectName("DisplayPrincipal")
        DisplayPrincipal.resize(1360, 740)
        
        self.centralwidget = QtWidgets.QWidget(DisplayPrincipal)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 1360, 750))
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #000000;")
        
        self.groupBox_TodoPPG = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_TodoPPG.setGeometry(QtCore.QRect(20, 320, 1000, 220))
        self.groupBox_TodoPPG.setAutoFillBackground(False)
        self.groupBox_TodoPPG.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox_TodoPPG.setTitle("")
        self.groupBox_TodoPPG.setObjectName("groupBox_TodoPPG")

        # INICIO FIN CASO:
        self.groupBox_IniciarFinalizar = QtWidgets.QGroupBox(self.groupBox_TodoPPG)
        self.groupBox_IniciarFinalizar.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.groupBox_IniciarFinalizar.setAutoFillBackground(False)
        self.groupBox_IniciarFinalizar.setStyleSheet("\n""background-color: rgb(0, 0, 0);")
        self.groupBox_IniciarFinalizar.setTitle("")
        self.groupBox_IniciarFinalizar.setObjectName("groupBox_IniciarFinalizar")
        
        self.lcdNumber_Principal = QtWidgets.QLCDNumber(self.groupBox_IniciarFinalizar)
        self.lcdNumber_Principal.setGeometry(QtCore.QRect(20, 20, 160, 61))
        self.lcdNumber_Principal.setDigitCount(8)
        self.lcdNumber_Principal.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_Principal.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.lcdNumber_Principal.setObjectName("lcdNumber_Principal")
        
        self.pushButton_IniciarCaso = QtWidgets.QPushButton(self.groupBox_IniciarFinalizar)
        self.pushButton_IniciarCaso.setGeometry(QtCore.QRect(20, 95, 160, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_IniciarCaso.setFont(font)
        self.pushButton_IniciarCaso.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_IniciarCaso.setObjectName("pushButton_IniciarCaso")
        self.pushButton_IniciarCaso.clicked.connect(self.funcIniciarCaso)

        self.pushButton_FinalizarCaso = QtWidgets.QPushButton(self.groupBox_IniciarFinalizar)
        self.pushButton_FinalizarCaso.setGeometry(QtCore.QRect(20, 145, 160, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_FinalizarCaso.setFont(font)
        self.pushButton_FinalizarCaso.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_FinalizarCaso.setObjectName("pushButton_FinalizarCaso")
        self.pushButton_FinalizarCaso.setDisabled(True)
        self.pushButton_FinalizarCaso.clicked.connect(self.funcFinalizarCaso)
        self.pushButton_FinalizarCaso.clicked.connect(self.openOpcionesInforme)
        self.pushButton_FinalizarCaso.clicked.connect(lambda: DisplayPrincipal.close())

        # ESTADOS:
        self.groupBox_TodoEstado = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_TodoEstado.setGeometry(QtCore.QRect(1040, 240, 300, 430))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_TodoEstado.setFont(font)
        self.groupBox_TodoEstado.setAutoFillBackground(False)
        self.groupBox_TodoEstado.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox_TodoEstado.setTitle("")
        self.groupBox_TodoEstado.setObjectName("groupBox_TodoEstado")
        
        self.label_Estado = QtWidgets.QLabel(self.groupBox_TodoEstado)
        self.label_Estado.setGeometry(QtCore.QRect(50, 23, 200, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Estado.setFont(font)
        self.label_Estado.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_Estado.setObjectName("label_Estado")
        
        self.pushButton_Basal = QtWidgets.QPushButton(self.groupBox_TodoEstado)
        self.pushButton_Basal.setGeometry(QtCore.QRect(20, 120, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_Basal.setFont(font)
        self.pushButton_Basal.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_Basal.setObjectName("pushButton_Basal")
        self.pushButton_Basal.setDisabled(True)
        self.pushButton_Basal.clicked.connect(self.funcBasal)

        self.lcdNumber_Basal = QtWidgets.QLCDNumber(self.groupBox_TodoEstado)
        self.lcdNumber_Basal.setGeometry(QtCore.QRect(150, 120, 130, 40))
        self.lcdNumber_Basal.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_Basal.setDigitCount(8)
        self.lcdNumber_Basal.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.lcdNumber_Basal.setObjectName("lcdNumber_Basal")
        
        self.pushButton_InicioAnestesia = QtWidgets.QPushButton(self.groupBox_TodoEstado)
        self.pushButton_InicioAnestesia.setGeometry(QtCore.QRect(20, 180, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_InicioAnestesia.setFont(font)
        self.pushButton_InicioAnestesia.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_InicioAnestesia.setObjectName("pushButton_InicioAnestesia")
        self.pushButton_InicioAnestesia.setDisabled(True)
        self.pushButton_InicioAnestesia.clicked.connect(self.funcInicioAnestesia)

        self.lcdNumber_InicioAnestesia = QtWidgets.QLCDNumber(self.groupBox_TodoEstado)
        self.lcdNumber_InicioAnestesia.setGeometry(QtCore.QRect(150, 180, 130, 40))
        self.lcdNumber_InicioAnestesia.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_InicioAnestesia.setDigitCount(8)
        self.lcdNumber_InicioAnestesia.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.lcdNumber_InicioAnestesia.setObjectName("lcdNumber_InicioAnestesia")

        self.pushButton_InicioCirugia = QtWidgets.QPushButton(self.groupBox_TodoEstado)
        self.pushButton_InicioCirugia.setGeometry(QtCore.QRect(20, 240, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_InicioCirugia.setFont(font)
        self.pushButton_InicioCirugia.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_InicioCirugia.setObjectName("pushButton_InicioCirugia")
        self.pushButton_InicioCirugia.setDisabled(True)
        self.pushButton_InicioCirugia.clicked.connect(self.funcInicioCirugia)

        self.lcdNumber_InicioCirugia = QtWidgets.QLCDNumber(self.groupBox_TodoEstado)
        self.lcdNumber_InicioCirugia.setGeometry(QtCore.QRect(150, 240, 130, 40))
        self.lcdNumber_InicioCirugia.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_InicioCirugia.setDigitCount(8)
        self.lcdNumber_InicioCirugia.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.lcdNumber_InicioCirugia.setObjectName("lcdNumber_InicioCirugia")

        self.pushButton_FinCirugia = QtWidgets.QPushButton(self.groupBox_TodoEstado)
        self.pushButton_FinCirugia.setGeometry(QtCore.QRect(20, 300, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_FinCirugia.setFont(font)
        self.pushButton_FinCirugia.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_FinCirugia.setObjectName("pushButton_FinCirugia")
        self.pushButton_FinCirugia.setDisabled(True)
        self.pushButton_FinCirugia.clicked.connect(self.funcFinCirugia)
        
        self.lcdNumber_FinCirugia = QtWidgets.QLCDNumber(self.groupBox_TodoEstado)
        self.lcdNumber_FinCirugia.setGeometry(QtCore.QRect(150, 300, 130, 40))
        self.lcdNumber_FinCirugia.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_FinCirugia.setDigitCount(8)
        self.lcdNumber_FinCirugia.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.lcdNumber_FinCirugia.setObjectName("lcdNumber_FinCirugia")

        self.pushButton_FinAnestesia = QtWidgets.QPushButton(self.groupBox_TodoEstado)
        self.pushButton_FinAnestesia.setGeometry(QtCore.QRect(20, 360, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_FinAnestesia.setFont(font)
        self.pushButton_FinAnestesia.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_FinAnestesia.setObjectName("pushButton_FinAnestesia")
        self.pushButton_FinAnestesia.setDisabled(True)
        self.pushButton_FinAnestesia.clicked.connect(self.funcFinAnestesia)
        
        self.lcdNumber_FinAnestesia = QtWidgets.QLCDNumber(self.groupBox_TodoEstado)
        self.lcdNumber_FinAnestesia.setGeometry(QtCore.QRect(150, 360, 130, 40))
        self.lcdNumber_FinAnestesia.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_FinAnestesia.setDigitCount(8)
        self.lcdNumber_FinAnestesia.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.lcdNumber_FinAnestesia.setObjectName("lcdNumber_FinAnestesia")
        
        self.textEdit_Estado = QtWidgets.QTextEdit(self.groupBox_TodoEstado)
        self.textEdit_Estado.setGeometry(QtCore.QRect(25, 55, 250, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.textEdit_Estado.setFont(font)
        self.textEdit_Estado.setStyleSheet("background-color: rgb(0, 0, 0);\n""border-color: rgb(255, 0, 0);")
        self.textEdit_Estado.setFrameShape(QtWidgets.QFrame.Panel)
        self.textEdit_Estado.setObjectName("textEdit_Estado")
        self.textEdit_Estado.setReadOnly(True)
        
        self.frame_Estado = QtWidgets.QFrame(self.groupBox_TodoEstado)
        self.frame_Estado.setGeometry(QtCore.QRect(20, 20, 260, 80))
        self.frame_Estado.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.frame_Estado.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Estado.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Estado.setObjectName("frame_Estado")
        
        self.frame_Estado.raise_()
        self.label_Estado.raise_()
        self.pushButton_Basal.raise_()
        self.lcdNumber_Basal.raise_()
        self.pushButton_InicioAnestesia.raise_()
        self.pushButton_InicioCirugia.raise_()
        self.pushButton_FinCirugia.raise_()
        self.pushButton_FinAnestesia.raise_()
        self.lcdNumber_InicioAnestesia.raise_()
        self.lcdNumber_InicioCirugia.raise_()
        self.lcdNumber_FinCirugia.raise_()
        self.lcdNumber_FinAnestesia.raise_()
        self.textEdit_Estado.raise_()
        
        # EVENTOS:
        self.groupBox_Eventos = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Eventos.setGeometry(QtCore.QRect(20, 560, 1000, 110))
        self.groupBox_Eventos.setAutoFillBackground(False)
        self.groupBox_Eventos.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox_Eventos.setTitle("")
        self.groupBox_Eventos.setObjectName("groupBox_Eventos")

        self.label_Eventos = QtWidgets.QLabel(self.groupBox_Eventos)
        self.label_Eventos.setGeometry(QtCore.QRect(200, 5, 600, 20))
        self.label_Eventos.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_Eventos.setObjectName("label_Eventos")
        self.label_Eventos.setAlignment(QtCore.Qt.AlignCenter)

        self.label_FarmacosAnalgesicos = QtWidgets.QLabel(self.groupBox_Eventos)
        self.label_FarmacosAnalgesicos.setGeometry(QtCore.QRect(15, 30, 300, 25))
        self.label_FarmacosAnalgesicos.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_FarmacosAnalgesicos.setObjectName("label_FarmacosAnalgesicos")
        self.label_FarmacosAnalgesicos.setAlignment(QtCore.Qt.AlignCenter)

        self.label_ProcQuirurgico = QtWidgets.QLabel(self.groupBox_Eventos)
        self.label_ProcQuirurgico.setGeometry(QtCore.QRect(325, 30, 350, 25))
        self.label_ProcQuirurgico.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_ProcQuirurgico.setObjectName("label_ProcQuirurgico")
        self.label_ProcQuirurgico.setAlignment(QtCore.Qt.AlignCenter)

        self.label_Intercurrencia = QtWidgets.QLabel(self.groupBox_Eventos)
        self.label_Intercurrencia.setGeometry(QtCore.QRect(685, 30, 300, 25))
        self.label_Intercurrencia.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_Intercurrencia.setObjectName("label_Intercurrencia")
        self.label_Intercurrencia.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_Farmaco = QtWidgets.QComboBox(self.groupBox_Eventos)
        self.comboBox_Farmaco.setGeometry(QtCore.QRect(15, 60, 300, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_Farmaco.setFont(font)
        self.comboBox_Farmaco.setStyleSheet("QComboBox { background-color: rgb(226, 226, 226); color: black; } QComboBox QAbstractItemView { background-color: rgb(226, 226, 226); color: black; }")
        self.comboBox_Farmaco.view().setStyleSheet("background-color: rgb(226, 226, 226); color: black;")
        self.comboBox_Farmaco.setObjectName("comboBox_Farmaco")
        self.comboBox_Farmaco.addItems(farmacos)
        self.comboBox_Farmaco.setMaxVisibleItems(5)
        self.comboBox_Farmaco.setEnabled(False)
        self.comboBox_Farmaco.currentIndexChanged.connect(self.funcNuevoEvento)
        
        self.comboBox_ProcQuirurgico = QtWidgets.QComboBox(self.groupBox_Eventos)
        self.comboBox_ProcQuirurgico.setGeometry(QtCore.QRect(325, 60, 350, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_ProcQuirurgico.setFont(font)
        self.comboBox_ProcQuirurgico.setStyleSheet("QComboBox { background-color: rgb(226, 226, 226); color: black; } QComboBox QAbstractItemView { background-color: rgb(226, 226, 226); color: black; }")
        self.comboBox_ProcQuirurgico.view().setStyleSheet("background-color: rgb(226, 226, 226); color: black;")
        self.comboBox_ProcQuirurgico.setObjectName("comboBox_ProcQuirurgico")
        self.comboBox_ProcQuirurgico.addItems(procedimientos)
        self.comboBox_ProcQuirurgico.setMaxVisibleItems(5)
        self.comboBox_ProcQuirurgico.setEnabled(False)
        self.comboBox_ProcQuirurgico.currentIndexChanged.connect(self.funcNuevoEvento)
        
        self.comboBox_Intercurrencias = QtWidgets.QComboBox(self.groupBox_Eventos)
        self.comboBox_Intercurrencias.setGeometry(QtCore.QRect(685, 60, 300, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_Intercurrencias.setFont(font)
        self.comboBox_Intercurrencias.setStyleSheet("QComboBox { background-color: rgb(226, 226, 226); color: black; } QComboBox QAbstractItemView { background-color: rgb(226, 226, 226); color: black; }")
        self.comboBox_Intercurrencias.view().setStyleSheet("background-color: rgb(226, 226, 226); color: black;")
        self.comboBox_Intercurrencias.setObjectName("comboBox_Intercurrencias")
        self.comboBox_Intercurrencias.addItems(intercurrencias)
        self.comboBox_Intercurrencias.setMaxVisibleItems(5)
        self.comboBox_Intercurrencias.setEnabled(False)
        self.comboBox_Intercurrencias.currentIndexChanged.connect(self.funcNuevoEvento)

        # ALARMAS:
        self.groupBox_Alarmas = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Alarmas.setGeometry(QtCore.QRect(1040, 20, 300, 200))
        self.groupBox_Alarmas.setAutoFillBackground(False)
        self.groupBox_Alarmas.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox_Alarmas.setTitle("")
        self.groupBox_Alarmas.setObjectName("groupBox_Alarmas")

        self.label_Alarmas = QtWidgets.QLabel(self.groupBox_Alarmas)
        self.label_Alarmas.setGeometry(QtCore.QRect(20, 10, 260, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Alarmas.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_Alarmas.setObjectName("label_Alarmas")
        self.label_Alarmas.setAlignment(QtCore.Qt.AlignCenter)
        
        self.label_Alarma_Min = QtWidgets.QLabel(self.groupBox_Alarmas)
        self.label_Alarma_Min.setGeometry(QtCore.QRect(20, 50, 60, 15))
        self.label_Alarma_Min.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_Alarma_Min.setObjectName("label_Alarma_Min")
        self.label_Alarma_Min.setAlignment(QtCore.Qt.AlignCenter)

        self.label_Alarma_Max = QtWidgets.QLabel(self.groupBox_Alarmas)
        self.label_Alarma_Max.setGeometry(QtCore.QRect(80, 50, 60, 15))
        self.label_Alarma_Max.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_Alarma_Max.setObjectName("label_Alarma_Max")
        self.label_Alarma_Max.setAlignment(QtCore.Qt.AlignCenter)

        self.label_Alarma_Tiempo = QtWidgets.QLabel(self.groupBox_Alarmas)
        self.label_Alarma_Tiempo.setGeometry(QtCore.QRect(140, 50, 150, 15))
        self.label_Alarma_Tiempo.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_Alarma_Tiempo.setObjectName("label_Alarma_Tiempo")
        self.label_Alarma_Tiempo.setAlignment(QtCore.Qt.AlignCenter)

        self.textEdit_Alarma_Min = QtWidgets.QTextEdit(self.groupBox_Alarmas)
        self.textEdit_Alarma_Min.setGeometry(QtCore.QRect(20, 70, 60, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit_Alarma_Min.setFont(font)
        self.textEdit_Alarma_Min.setStyleSheet("background-color: rgb(0, 0, 0); color: white; border: 1px solid #808080;")
        self.textEdit_Alarma_Min.setFrameShape(QtWidgets.QFrame.Panel)
        self.textEdit_Alarma_Min.setObjectName("textEdit_Alarma_Min")
        self.textEdit_Alarma_Min.setReadOnly(True)

        self.textEdit_Alarma_Max = QtWidgets.QTextEdit(self.groupBox_Alarmas)
        self.textEdit_Alarma_Max.setGeometry(QtCore.QRect(80, 70, 60, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit_Alarma_Max.setFont(font)
        self.textEdit_Alarma_Max.setStyleSheet("background-color: rgb(0, 0, 0); color: white; border: 1px solid #808080;")
        self.textEdit_Alarma_Max.setFrameShape(QtWidgets.QFrame.Panel)
        self.textEdit_Alarma_Max.setObjectName("textEdit_Alarma_Max")
        self.textEdit_Alarma_Max.setReadOnly(True)

        self.textEdit_Alarma_Tiempo = QtWidgets.QTextEdit(self.groupBox_Alarmas)
        self.textEdit_Alarma_Tiempo.setGeometry(QtCore.QRect(140, 70, 150, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit_Alarma_Tiempo.setFont(font)
        self.textEdit_Alarma_Tiempo.setStyleSheet("background-color: rgb(0, 0, 0); color: black; border: 1px solid #808080;")
        self.textEdit_Alarma_Tiempo.setFrameShape(QtWidgets.QFrame.Panel)
        self.textEdit_Alarma_Tiempo.setObjectName("textEdit_Alarma_Tiempo")
        self.textEdit_Alarma_Tiempo.setReadOnly(True)

        self.pushButton_ConfigurarAlarmas = QtWidgets.QPushButton(self.groupBox_Alarmas)
        self.pushButton_ConfigurarAlarmas.setGeometry(QtCore.QRect(110, 130, 140, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_ConfigurarAlarmas.setFont(font)
        self.pushButton_ConfigurarAlarmas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_ConfigurarAlarmas.setObjectName("pushButton_ConfigurarAlarmas")
        self.pushButton_ConfigurarAlarmas.clicked.connect(self.openSetUpAlarmas)
        self.pushButton_ConfigurarAlarmas.setEnabled(False)

        self.label_ConfigurarAlarmas = QtWidgets.QLabel(self.groupBox_Alarmas)
        self.label_ConfigurarAlarmas.setGeometry(QtCore.QRect(50, 130, 40, 40))
        self.label_ConfigurarAlarmas.setObjectName("label_ConfigurarAlarmas")
        self.imagen_ConfigurarAlarmas = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\ConfigurarAlarmas.png")
        self.imagen_ConfigurarAlarmas = self.imagen_ConfigurarAlarmas.scaled(self.label_ConfigurarAlarmas.size(), QtCore.Qt.KeepAspectRatio)
        self.label_ConfigurarAlarmas.setPixmap(self.imagen_ConfigurarAlarmas)

        self.groupBox_TodoSPI = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_TodoSPI.setGeometry(QtCore.QRect(20, 20, 1000, 280))
        self.groupBox_TodoSPI.setAutoFillBackground(False)
        self.groupBox_TodoSPI.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox_TodoSPI.setTitle("")
        self.groupBox_TodoSPI.setObjectName("groupBox_TodoSPI")
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox_TodoSPI)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(350, 10, 640, 201))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        
        self.verticalLayout_SPI = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_SPI.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_SPI.setObjectName("verticalLayout_SPI")
        
        self.frame_Ajustes = QtWidgets.QFrame(self.groupBox_TodoSPI)
        self.frame_Ajustes.setGeometry(QtCore.QRect(390, 220, 573, 50))
        self.frame_Ajustes.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.frame_Ajustes.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Ajustes.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Ajustes.setObjectName("frame_Ajustes")

        self.pushButton_AjustarVisualizacionSPI = QtWidgets.QPushButton(self.frame_Ajustes)
        self.pushButton_AjustarVisualizacionSPI.setGeometry(QtCore.QRect(10, 5, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_AjustarVisualizacionSPI.setFont(font)
        self.pushButton_AjustarVisualizacionSPI.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.pushButton_AjustarVisualizacionSPI.setAutoDefault(False)
        self.pushButton_AjustarVisualizacionSPI.setDefault(False)
        self.pushButton_AjustarVisualizacionSPI.setFlat(False)
        self.pushButton_AjustarVisualizacionSPI.setObjectName("pushButton_AjustarVisualizacionSPI")
        self.pushButton_AjustarVisualizacionSPI.clicked.connect(self.openAjusteVisualizacionGraficaSPI)
        self.pushButton_AjustarVisualizacionSPI.setDisabled(True)

        self.pushButton_RestablecerVisualizacion = QtWidgets.QPushButton(self.frame_Ajustes)
        self.pushButton_RestablecerVisualizacion.setGeometry(QtCore.QRect(130, 5, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_RestablecerVisualizacion.setFont(font)
        self.pushButton_RestablecerVisualizacion.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.pushButton_RestablecerVisualizacion.setAutoDefault(False)
        self.pushButton_RestablecerVisualizacion.setDefault(False)
        self.pushButton_RestablecerVisualizacion.setFlat(False)
        self.pushButton_RestablecerVisualizacion.setObjectName("pushButton_RestablecerVisualizacion")
        self.pushButton_RestablecerVisualizacion.setDisabled(True)
        self.pushButton_RestablecerVisualizacion.clicked.connect(self.funcRestablecerVisualizacion)

        self.label_VentanaTemporal = QtWidgets.QLabel(self.frame_Ajustes)
        self.label_VentanaTemporal.setGeometry(QtCore.QRect(323, 5, 120, 40))
        self.label_VentanaTemporal.setStyleSheet("background-color: #000000;\n""border-color: (226, 226, 226);")
        self.label_VentanaTemporal.setObjectName("label_VentanaTemporal")
        self.label_VentanaTemporal.setAlignment(QtCore.Qt.AlignCenter)

        self.textEdit_VentanaTemporal = QtWidgets.QTextEdit(self.frame_Ajustes)
        self.textEdit_VentanaTemporal.setGeometry(QtCore.QRect(463, 5, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit_VentanaTemporal.setFont(font)
        self.textEdit_VentanaTemporal.setStyleSheet("background-color: #000000;\n""border-color: (226, 226, 226);")
        self.textEdit_VentanaTemporal.setAlignment(QtCore.Qt.AlignVCenter)
        self.textEdit_VentanaTemporal.setFrameShape(QtWidgets.QFrame.Panel)
        self.textEdit_VentanaTemporal.setObjectName("textEdit_VentanaTemporal")
        self.textEdit_VentanaTemporal.setReadOnly(True)

        self.groupBox_ReferenciaSPI = QtWidgets.QGroupBox(self.groupBox_TodoSPI)
        self.groupBox_ReferenciaSPI.setGeometry(QtCore.QRect(10, 10, 330, 190))
        self.groupBox_ReferenciaSPI.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.groupBox_ReferenciaSPI.setTitle("")
        self.groupBox_ReferenciaSPI.setObjectName("groupBox_ReferenciaSPI")

        self.label_AnalgesiaInsuficiente = QtWidgets.QLabel(self.groupBox_ReferenciaSPI)
        self.label_AnalgesiaInsuficiente.setGeometry(QtCore.QRect(245, 15, 75, 50))
        self.label_AnalgesiaInsuficiente.setStyleSheet("background-color: rgb(255, 0, 0);\n""border-color: rgb(0, 0, 0);")
        self.label_AnalgesiaInsuficiente.setObjectName("label_AnalgesiaInsuficiente")
        
        self.label_AnalgesiaAdecuada = QtWidgets.QLabel(self.groupBox_ReferenciaSPI)
        self.label_AnalgesiaAdecuada.setGeometry(QtCore.QRect(245, 65, 75, 50))
        self.label_AnalgesiaAdecuada.setStyleSheet("background-color: rgb(48, 206, 13);\n""border-color: rgb(0, 0, 0);")
        self.label_AnalgesiaAdecuada.setObjectName("label_AnalgesiaAdecuada")
        
        self.label_AnalgesiaExcesiva = QtWidgets.QLabel(self.groupBox_ReferenciaSPI)
        self.label_AnalgesiaExcesiva.setGeometry(QtCore.QRect(245, 115, 75, 50))
        self.label_AnalgesiaExcesiva.setStyleSheet("background-color: rgb(255, 255, 0);\n""border-color: rgb(0, 0, 0);")
        self.label_AnalgesiaExcesiva.setObjectName("label_AnalgesiaExcesiva")

        self.label_100 = QtWidgets.QLabel(self.groupBox_ReferenciaSPI)
        self.label_100.setGeometry(QtCore.QRect(215, 6, 25, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_100.setFont(font)
        self.label_100.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_100.setObjectName("label_100")

        self.label_50 = QtWidgets.QLabel(self.groupBox_ReferenciaSPI)
        self.label_50.setGeometry(QtCore.QRect(215, 60, 25, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_50.setFont(font)
        self.label_50.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_50.setObjectName("label_50")
        
        self.label_20 = QtWidgets.QLabel(self.groupBox_ReferenciaSPI)
        self.label_20.setGeometry(QtCore.QRect(215, 110, 25, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_20.setObjectName("label_20")
        
        self.label_0 = QtWidgets.QLabel(self.groupBox_ReferenciaSPI)
        self.label_0.setGeometry(QtCore.QRect(215, 160, 21, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_0.setFont(font)
        self.label_0.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_0.setObjectName("label_0")

        self.groupBox_SPI = QtWidgets.QGroupBox(self.groupBox_ReferenciaSPI)
        self.groupBox_SPI.setGeometry(QtCore.QRect(10, 10, 195, 170))
        self.groupBox_SPI.setTitle("")
        self.groupBox_SPI.setObjectName("groupBox_SPI")

        self.label_SPI = QtWidgets.QLabel(self.groupBox_SPI)
        self.label_SPI.setGeometry(QtCore.QRect(5, 30, 185, 40))
        self.label_SPI.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_SPI.setObjectName("label_SPI")
        
        self.textEdit_SPI = QtWidgets.QTextEdit(self.groupBox_SPI)
        self.textEdit_SPI.setGeometry(QtCore.QRect(5, 70, 185, 90))
        self.textEdit_SPI.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit_SPI.setObjectName("textEdit_SPI")
        font = QtGui.QFont()
        font.setPointSize(30)
        self.textEdit_SPI.setFont(font)
        self.textEdit_SPI.setReadOnly(True)
        
        self.frame_AlarmasFisiologicas = QtWidgets.QFrame(self.groupBox_TodoSPI)
        self.frame_AlarmasFisiologicas.setGeometry(QtCore.QRect(10, 205, 330, 65))
        self.frame_AlarmasFisiologicas.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.frame_AlarmasFisiologicas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_AlarmasFisiologicas.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_AlarmasFisiologicas.setObjectName("frame_AlarmasFisiologicas")
        self.frame_AlarmasFisiologicas.hide()

        self.label_AlarmaFisiologicaActiva = QtWidgets.QLabel(self.frame_AlarmasFisiologicas)
        self.label_AlarmaFisiologicaActiva.setGeometry(QtCore.QRect(5, 5, 25, 25))
        self.label_AlarmaFisiologicaActiva.setObjectName("label_AlarmaFisiologicaActiva")
        self.imagen_AlarmaFisiologicaActiva = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\AlarmaActiva.png")
        self.imagen_AlarmaFisiologicaActiva = self.imagen_AlarmaFisiologicaActiva.scaled(self.label_AlarmaFisiologicaActiva.size(), QtCore.Qt.KeepAspectRatio)
        self.label_AlarmaFisiologicaActiva.setPixmap(self.imagen_AlarmaFisiologicaActiva)
        
        self.label_AlarmaFisiologicaSigno = QtWidgets.QLabel(self.frame_AlarmasFisiologicas)
        self.label_AlarmaFisiologicaSigno.setGeometry(QtCore.QRect(35, 5, 25, 25))
        self.label_AlarmaFisiologicaSigno.setObjectName("label_AlarmaFisiologicaSigno")
        self.imagen_AlarmaFisiologicaSigno = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\Signo.jpg")
        self.imagen_AlarmaFisiologicaSigno = self.imagen_AlarmaFisiologicaSigno.scaled(self.label_AlarmaFisiologicaSigno.size(), QtCore.Qt.KeepAspectRatio)
        self.label_AlarmaFisiologicaSigno.setPixmap(self.imagen_AlarmaFisiologicaSigno)

        self.label_MensajeAlarmaFisiologicaMaximo = QtWidgets.QLabel(self.frame_AlarmasFisiologicas)
        self.label_MensajeAlarmaFisiologicaMaximo.setGeometry(QtCore.QRect(65, 5, 200, 25))
        self.label_MensajeAlarmaFisiologicaMaximo.setStyleSheet("background-color: #000000;\n""border-color: #000000;")
        self.label_MensajeAlarmaFisiologicaMaximo.setObjectName("label_MensajeAlarmaFisiologicaMaximo")
        
        self.label_MensajeAlarmaFisiologicaMinimo = QtWidgets.QLabel(self.frame_AlarmasFisiologicas)
        self.label_MensajeAlarmaFisiologicaMinimo.setGeometry(QtCore.QRect(65, 5, 200, 25))
        self.label_MensajeAlarmaFisiologicaMinimo.setStyleSheet("background-color: #000000;\n""border-color: #000000;")
        self.label_MensajeAlarmaFisiologicaMinimo.setObjectName("label_MensajeAlarmaFisiologicaMinimo")

        self.label_AlarmaFisiologicaReconocida = QtWidgets.QLabel(self.frame_AlarmasFisiologicas)
        self.label_AlarmaFisiologicaReconocida.setGeometry(QtCore.QRect(5, 35, 25, 25))
        self.label_AlarmaFisiologicaReconocida.setObjectName("label_AlarmaFisiologicaReconocida")
        self.imagen_AlarmaFisiologicaReconocida = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\AlarmaReconocida.png")
        self.imagen_AlarmaFisiologicaReconocida = self.imagen_AlarmaFisiologicaReconocida.scaled(self.label_AlarmaFisiologicaReconocida.size(), QtCore.Qt.KeepAspectRatio)
        self.label_AlarmaFisiologicaReconocida.setPixmap(self.imagen_AlarmaFisiologicaReconocida)
        self.label_AlarmaFisiologicaReconocida.hide()

        self.radioButton_AlarmaFisiologicaReconocida = QtWidgets.QRadioButton(self.frame_AlarmasFisiologicas)
        self.radioButton_AlarmaFisiologicaReconocida.setGeometry(QtCore.QRect(40, 40, 15, 15))
        self.radioButton_AlarmaFisiologicaReconocida.setObjectName("radioButton_AlarmaFisiologicaReconocida")
        self.radioButton_AlarmaFisiologicaReconocida.setStyleSheet("border: solid #000000;")
        self.radioButton_AlarmaFisiologicaReconocida.toggled.connect(self.funcAlarmaFisiologicaReconocida)

        self.label_TextoAlarmaFisiologicaReconocida = QtWidgets.QLabel(self.frame_AlarmasFisiologicas)
        self.label_TextoAlarmaFisiologicaReconocida.setGeometry(QtCore.QRect(60, 35, 150, 25))
        self.label_TextoAlarmaFisiologicaReconocida.setStyleSheet("background-color: #000000;\n""border-color: #000000;")
        self.label_TextoAlarmaFisiologicaReconocida.setObjectName("label_TextoAlarmaFisiologicaReconocida")
        self.label_TextoAlarmaFisiologicaReconocida.setAlignment(QtCore.Qt.AlignCenter)

        self.frame_AlarmasTecnicas = QtWidgets.QFrame(self.groupBox_TodoPPG)
        self.frame_AlarmasTecnicas.setGeometry(QtCore.QRect(220, 175, 770, 35)) 
        self.frame_AlarmasTecnicas.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #808080;")
        self.frame_AlarmasTecnicas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_AlarmasTecnicas.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_AlarmasTecnicas.setObjectName("frame_AlarmasTecnicas")
        self.frame_AlarmasTecnicas.hide()

        self.label_AlarmaTecnicaActiva = QtWidgets.QLabel(self.frame_AlarmasTecnicas)
        self.label_AlarmaTecnicaActiva.setGeometry(QtCore.QRect(5, 5, 25, 25))
        self.label_AlarmaTecnicaActiva.setObjectName("label_AlarmaTecnicaActiva")
        self.imagen_AlarmaTecnicaActiva = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\AlarmaActiva.png")
        self.imagen_AlarmaTecnicaActiva = self.imagen_AlarmaTecnicaActiva.scaled(self.label_AlarmaTecnicaActiva.size(), QtCore.Qt.KeepAspectRatio)
        self.label_AlarmaTecnicaActiva.setPixmap(self.imagen_AlarmaTecnicaActiva)
        
        self.label_AlarmaTecnicaSigno = QtWidgets.QLabel(self.frame_AlarmasTecnicas)
        self.label_AlarmaTecnicaSigno.setGeometry(QtCore.QRect(35, 5, 25, 25))
        self.label_AlarmaTecnicaSigno.setObjectName("label_AlarmaTecnicaSigno")
        self.imagen_AlarmaTecnicaSigno = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\Signo.jpg")
        self.imagen_AlarmaTecnicaSigno = self.imagen_AlarmaTecnicaSigno.scaled(self.label_AlarmaTecnicaSigno.size(), QtCore.Qt.KeepAspectRatio)
        self.label_AlarmaTecnicaSigno.setPixmap(self.imagen_AlarmaTecnicaSigno)

        self.label_MensajeAlarmaTecnicaMovimiento = QtWidgets.QLabel(self.frame_AlarmasTecnicas)
        self.label_MensajeAlarmaTecnicaMovimiento.setGeometry(QtCore.QRect(70, 5, 300, 25))
        self.label_MensajeAlarmaTecnicaMovimiento.setStyleSheet("background-color: #000000;\n""border-color: #000000;")
        self.label_MensajeAlarmaTecnicaMovimiento.setObjectName("label_MensajeAlarmaTecnicaMovimiento")
        
        self.label_MensajeAlarmaTecnicaDesconexion = QtWidgets.QLabel(self.frame_AlarmasTecnicas)
        self.label_MensajeAlarmaTecnicaDesconexion.setGeometry(QtCore.QRect(70, 5, 300, 25))
        self.label_MensajeAlarmaTecnicaDesconexion.setStyleSheet("background-color: #000000;\n""border-color: #000000;")
        self.label_MensajeAlarmaTecnicaDesconexion.setObjectName("label_MensajeAlarmaTecnicaDesconexion")

        self.label_AlarmaTecnicaReconocida = QtWidgets.QLabel(self.frame_AlarmasTecnicas)
        self.label_AlarmaTecnicaReconocida.setGeometry(QtCore.QRect(585, 5, 25, 25))
        self.label_AlarmaTecnicaReconocida.setObjectName("label_AlarmaTecnicaReconocida")
        self.imagen_AlarmaTecnicaReconocida = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\AlarmaReconocida.png")
        self.imagen_AlarmaTecnicaReconocida = self.imagen_AlarmaTecnicaReconocida.scaled(self.label_AlarmaTecnicaReconocida.size(), QtCore.Qt.KeepAspectRatio)
        self.label_AlarmaTecnicaReconocida.setPixmap(self.imagen_AlarmaTecnicaReconocida)
        self.label_AlarmaTecnicaReconocida.hide()

        self.radioButton_AlarmaTecnicaReconocida = QtWidgets.QRadioButton(self.frame_AlarmasTecnicas)
        self.radioButton_AlarmaTecnicaReconocida.setGeometry(QtCore.QRect(605, 10, 15, 15))
        self.radioButton_AlarmaTecnicaReconocida.setObjectName("radioButton_AlarmaTecnicaReconocida")
        self.radioButton_AlarmaTecnicaReconocida.setStyleSheet("border: solid #000000;")
        self.radioButton_AlarmaTecnicaReconocida.toggled.connect(self.funcAlarmaTecnicaReconocida)

        self.label_TextoAlarmaTecnicaReconocida = QtWidgets.QLabel(self.frame_AlarmasTecnicas)
        self.label_TextoAlarmaTecnicaReconocida.setGeometry(QtCore.QRect(625, 5, 120, 25))
        self.label_TextoAlarmaTecnicaReconocida.setStyleSheet("background-color: #000000;\n""border-color: #000000;")
        self.label_TextoAlarmaTecnicaReconocida.setObjectName("label_TextoAlarmaTecnicaReconocida")
        self.label_TextoAlarmaTecnicaReconocida.setAlignment(QtCore.Qt.AlignCenter)

        self.groupBox_SPI.raise_()
        self.textEdit_SPI.raise_()
        self.groupBox_ReferenciaSPI.raise_()
        self.label_0.raise_()
        self.label_20.raise_()
        self.label_50.raise_()
        self.label_100.raise_()
        self.verticalLayoutWidget.raise_()
        self.label_AnalgesiaInsuficiente.raise_()
        self.label_AnalgesiaAdecuada.raise_()
        self.label_AnalgesiaExcesiva.raise_()
        self.label_SPI.raise_()
        self.pushButton_AjustarVisualizacionSPI.raise_()
        self.frame_Ajustes.raise_()
        self.frame_AlarmasFisiologicas.raise_()
        self.frame_AlarmasTecnicas.raise_()

        self.frame_PPG = QtWidgets.QFrame(self.groupBox_TodoPPG)
        self.frame_PPG.setGeometry(QtCore.QRect(220, 10, 770, 162))
        self.frame_PPG.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #F0F0F0;")
        self.frame_PPG.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_PPG.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_PPG.setObjectName("frame_PPG")
        self.frame_PPG.raise_()
    
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_TodoPPG)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(225, 15, 760, 152))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        
        self.verticalLayout_PPG = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_PPG.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_PPG.setObjectName("verticalLayout_PPG")
        
        # Gráfico
        # Aca se crea el objeto self.plt_PPG y se lo asigna al layout que se va a usar para graficar el PPG
        self.serial_port = None

        # Lectura de datos permanente
        self.update_interval = int(1000*(1/fs))  # Update interval in milliseconds
        self.timer_ppg = QTimer()
        self.timer_ppg.setInterval(self.update_interval)
        self.timer_ppg.setTimerType(Qt.PreciseTimer)
        self.timer_ppg.timeout.connect(self.read_data_periodically)
    
        self.plt_PPG = pg.PlotWidget()
        self.verticalLayout_PPG.addWidget(self.plt_PPG)

        # Aca se crea el objeto self.plt_SPI y se lo asigna al layout que se va a usar para graficar el SPI
        self.plt_SPI = pg.PlotWidget()
        self.verticalLayout_SPI.addWidget(self.plt_SPI)

        #Estética del gráfico PPG
        self.plt_PPG.getPlotItem().hideAxis('bottom')
        self.plt_PPG.getPlotItem().hideAxis('left')
        self.plt_PPG.setBackground('#000000')  # Fondo negro

        #Estética del gráfico SPI
        self.plt_SPI.setLabel('left', 'Evolución SPI')
        axis_pen = pg.mkPen(color = '#FFFFFF')  # Color blanco para los ejes
        self.plt_SPI.getAxis('left').setPen(axis_pen)  # Línea eje y
        self.plt_SPI.getAxis('left').setTextPen(axis_pen) # Números eje y
        self.plt_SPI.setBackground('#000000')  # Fondo negro
        self.plt_SPI.getPlotItem().hideAxis('bottom') # No mostramos eje x
        self.plt_SPI.setYRange(0, 100) # Cambio el rango del eje y que aparece por default
        
        #Grafico lineas en los límites 20 y 50
        self.senal_spi_x = list(np.linspace(0,ventana_SPI,ventana_SPI))
        self.linea_50 = [50] * ventana_SPI
        self.linea_20 = [20] * ventana_SPI
        self.plt_SPI.plot(self.senal_spi_x, self.linea_50, pen=pg.mkPen('#FF0000',width=2, style=QtCore.Qt.DashLine)) # limite de SPI = 50 
        self.plt_SPI.plot(self.senal_spi_x, self.linea_20, pen=pg.mkPen('#FFFF00',width=2, style=QtCore.Qt.DashLine)) # limite de SPI = 20

        self.groupBox_Todo = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Todo.setGeometry(QtCore.QRect(20, 20, 1320, 650))
        self.groupBox_Todo.setStyleSheet("background-color: #000000;\n""border-color: rgb(0, 0, 0);")
        self.groupBox_Todo.setTitle("")
        self.groupBox_Todo.setObjectName("groupBox_Todo")
        
        self.groupBox_Todo.raise_()
        self.groupBox_TodoSPI.raise_()
        self.groupBox_IniciarFinalizar.raise_()
        self.groupBox_TodoEstado.raise_()
        self.groupBox_Eventos.raise_()
        self.groupBox_Alarmas.raise_()
        self.groupBox_TodoPPG.raise_()
        
        DisplayPrincipal.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DisplayPrincipal)
        self.statusbar.setObjectName("statusbar")
        DisplayPrincipal.setStatusBar(self.statusbar)

        # Control connect
        self.serial_communication = SerialCommunication(port="COM6", baudrate=230400)
        self.serial_communication.data_received.connect(self.read_data_periodically)

        # Esto es para el gráfico de PPG
        self.x = list(np.linspace(0,largo,largo))
        self.y = list(np.linspace(0,0,largo))

        # Esto es para el gráfico de SPI
        self.senal_spi_x = list(np.linspace(0,ventana_SPI,ventana_SPI))
        self.senal_spi = list(np.linspace(0,0,ventana_SPI))
        self.senal_spi_promedio = list(np.linspace(0,0,ventana_SPI))
        self.linea_50 = [50] * ventana_SPI
        self.linea_20 = [20] * ventana_SPI
        self.linea_estado = [0] * ventana_SPI

        # Esto es para graficar la vertical del cambio de estado en el gráfico del SPI
        self.senal_estado_x = list(np.linspace(0,ventana_SPI,ventana_SPI))
        self.senal_estado = list(np.linspace(0,0,ventana_SPI))      

        # Archivo csv
        from InputDatosPaciente import path_archivo_datos
        with open(path_archivo_datos, 'w') as csv_file:
            fieldnames = ["muestra", "tiempo", "ppg", "ppg filtrado", "spi", "spi_promedio", "estado", "tipo evento", "evento", "alarma"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

        self.retranslateUi(DisplayPrincipal)
        QtCore.QMetaObject.connectSlotsByName(DisplayPrincipal)

###############################################################################################################################

# FUNCTIONS:

    # Function to send a message from PC to board
    def send_message(self, ser, hex_bytes):
        data_to_send = bytes(hex_bytes)
        ser.write(QByteArray(data_to_send))

    # Function to read a message sent from board to PC
    def read_message(self, ser, n_bytes):
        response = ser.read(n_bytes)
        return response

    # Function to read a register
    def read_register(self, ser, address):
        message = [0x03, address[0], address[1], 0x0D]
        self.send_message(ser, message)
        data_bytes = self.read_message(ser, n_bytes=7)
        raw_data = data_bytes[2:5]
        decimal_value = int.from_bytes(raw_data, byteorder='little')
        return decimal_value

    def read_data_periodically(self, new_value):
        _translate = QtCore.QCoreApplication.translate

        global muestra
        muestra += 1

        global ppg 
        ppg = int(new_value)

        self.funcSetUpAlarmas()
        
        # Filtros
        # @NOTE: BIBLIOGRAFIA: adaptative threshold method for the peak detetction of ppg
        [b_HP,a_HP] = signal.butter(3, 0.85, btype = 'highpass', analog = False, output = 'ba', fs = fs) 
        [b_LP,a_LP] = signal.butter(3, 5, btype = 'lowpass', analog = False, output = 'ba', fs = fs) 

        global ventana_ppg
        aux = ventana_ppg[1:]
        aux.append(ppg)
        ventana_ppg = copy.deepcopy(aux)
            
        if muestra > largo:
            desconexion = funcDetectarDesconexion(ventana_ppg)

            ventana_filtrada_LP = signal.filtfilt(b_LP, a_LP, ventana_ppg)
            ventana_filtrada_HP = signal.filtfilt(b_HP, a_HP, ventana_filtrada_LP)
            
            if muestra%largo == 0:
                if desconexion == False:
                    global alarma

                    try:
                        locs_peaks_ppg = funcDetectarPicos(ventana_filtrada_HP)
                        locs_peaks_ppg_no_subida = funcEliminarPicosSubida(ventana_filtrada_HP, locs_peaks_ppg)
                        locs_peaks_ppg_sistolicos = funcEliminarDiastolicos(ventana_filtrada_HP, locs_peaks_ppg_no_subida)
                        locs_peaks_ppg_sin_outliers = funcEliminarPicosOutliers(locs_peaks_ppg_sistolicos, low_rri = 15, high_rri = 90)
                        locs_onsets_ppg = funcDetectarOnsets(ventana_filtrada_HP, locs_peaks_ppg_sin_outliers)
                        
                        PPGA = funcPPGA(ventana_filtrada_HP, locs_peaks_ppg_sin_outliers, locs_onsets_ppg)
                        HBI = funcHBI(locs_peaks_ppg_sin_outliers)

                        HBI_prom = funcPromedio(HBI)
                        PPGA_prom = funcPromedio(PPGA)
                        
                        global estado
                        if estado == "-": # pre basal usa la normalizacion poblacional
                            HBI_norm = funcNormalizarParametro(TF_HBI, int(HBI_prom))
                            PPGA_norm = funcNormalizarParametro(TF_PPGA, int(PPGA_prom))
                        
                        elif estado == "basal": # basal usa la normalizacion poblacional y crea la distribucion individual
                            global lista_individual_HBI, lista_individual_PPGA
                            lista_individual_HBI.extend(HBI)
                            lista_individual_PPGA.extend(PPGA)

                            HBI_norm = funcNormalizarParametro(TF_HBI, int(HBI_prom))
                            PPGA_norm = funcNormalizarParametro(TF_PPGA, int(PPGA_prom))

                        else: #usa la normalizacion combinada
                            global TF_HBI_combinada, TF_PPGA_combinada
                            HBI_norm = funcNormalizarParametro(TF_HBI_combinada, int(HBI_prom))
                            PPGA_norm = funcNormalizarParametro(TF_PPGA_combinada, int(PPGA_prom))

                        global SPI
                        SPI = funcSPIi(PPGA_norm, HBI_norm)
                        self.textEdit_SPI.setText(str(SPI))
                        self.textEdit_SPI.setAlignment(QtCore.Qt.AlignCenter)
                        self.textEdit_SPI.setStyleSheet("color: black;")
                        self.funcColorSPI()

                        # Como pude calcular el SPI, sé que no hubo un error
                        global ejecutar_alarma_auditiva
                        ejecutar_alarma_auditiva = True # La próxima vez que haya una alarma auditiva quiero que suene

                        # Desactivo alarmas por las dudas en caso de que se hayan activado antes, porque ya no hay condición de alarma 
                        self.radioButton_AlarmaTecnicaReconocida.setChecked(False)
                        self.frame_AlarmasTecnicas.hide()
                        self.frame_PPG.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #F0F0F0;") # Le saco el borde de color al group box
                        self.centralwidget.setStyleSheet("background-color: #000000;")

                        # Si el borde del PPG estaba parpadeando, freno el timer
                        try: 
                            self.timer_border_color_PPG.stop() 
                        except:
                            pass

                        global alarma
                        if alarma == "Desconexión" or alarma == "Movimiento":
                            # Actualizo la variable global 'alarma' porque ya no hay condición de alarma técnica. No afecta si hay una fisiológica porque no entra al if
                            alarma_actual = "-"
                            alarma = alarma_actual

                    except:
                        # Se movió el sensor y no se puede hacer el cálculo del SPI 
                        self.textEdit_SPI.setText("-")
                        self.textEdit_SPI.setAlignment(QtCore.Qt.AlignCenter)
                        self.textEdit_SPI.setStyleSheet("color: black;")
                        self.funcColorSPI()

                        SPI = np.nan

                        # Si había alarma de SPI activa la desactivo porque ahora SPI = "-"
                        self.radioButton_AlarmaFisiologicaReconocida.setChecked(False)
                        self.frame_AlarmasFisiologicas.hide()
                        self.timer_border_color_SPI.stop()
                        self.groupBox_ReferenciaSPI.setStyleSheet("background-color: rgb(0, 0, 0);") # Le saco el borde de color al group box
                        # Actualizo la variable global 'alarma' porque ya no hay condición de alarma
                        alarma_actual = "-"
                        alarma = alarma_actual

                        global contador_error_sensor
                        contador_error_sensor += 1

                        if contador_error_sensor == 3:
                            # Ejecuto la alarma técnica
                            self.funcEjecutarAlarmaTecnica(caso = "Movimiento")
                            contador_error_sensor = 0
                            
                else:
                    # Se detectó desconexión del sensor y no se puede hacer el cálculo del SPI 
                    self.textEdit_SPI.setText("-")
                    self.textEdit_SPI.setAlignment(QtCore.Qt.AlignCenter)
                    self.textEdit_SPI.setStyleSheet("color: black;")
                    self.funcColorSPI()

                    SPI = np.nan
                    
                    # Si había alarma de SPI activa la desactivo porque ahora SPI = "-"
                    self.radioButton_AlarmaFisiologicaReconocida.setChecked(False)
                    self.frame_AlarmasFisiologicas.hide()
                    self.timer_border_color_SPI.stop()
                    self.groupBox_ReferenciaSPI.setStyleSheet("background-color: rgb(0, 0, 0);") # Le saco el borde de color al group boxç
                    self.centralwidget.setStyleSheet("background-color: #000000;")

                    # Ejecuto la alarma técnica
                    self.funcEjecutarAlarmaTecnica(caso = "Desconexión")

        
                self.senal_spi=self.senal_spi[1:]
                self.senal_spi.append(SPI)

                self.senal_a_promediar = self.senal_spi[-cant_spi_a_prom:]
                spi_filtrados = [x for x in self.senal_a_promediar if x != 0 and not np.isnan(x)]
                
                global spi_promedio
                spi_promedio = np.mean(spi_filtrados)

                self.senal_spi_promedio = self.senal_spi_promedio[1:]
                self.senal_spi_promedio.append(spi_promedio)

                # Grafica
                self.plt_SPI.clear()
                self.plt_SPI.plot(self.senal_spi_x, self.senal_spi, pen=pg.mkPen('#333333',width=2)) # señal SPI instantaneo
                self.plt_SPI.plot(self.senal_spi_x, self.linea_50, linestyle = '--', pen=pg.mkPen('#FF0000',width=2, style=QtCore.Qt.DashLine)) # referencia de SPI=50
                self.plt_SPI.plot(self.senal_spi_x, self.linea_20, linestyle = '--', pen=pg.mkPen('#FFFF00',width=2, style=QtCore.Qt.DashLine)) # referencia de SPI=20
                self.plt_SPI.plot(self.senal_spi_x, self.senal_spi_promedio, pen=pg.mkPen('#FFFFFF',width=2)) # señal SPI promedio

                ventana_SPI_visualizada_min = 5
                ventana_SPI_visualizada = 100
                self.plt_SPI.setXRange(ventana_SPI-ventana_SPI_visualizada, ventana_SPI)
                self.textEdit_VentanaTemporal.setPlainText(str(int(ventana_SPI_visualizada_min)) + " min")
                self.textEdit_VentanaTemporal.setStyleSheet("color: white;")
                self.textEdit_VentanaTemporal.setAlignment(QtCore.Qt.AlignCenter)
                
                global restablecido 
                if restablecido == False:
                    from AjustarVisualizacionSPI import ajustes_graf_SPI
                    ajustes_gram_SPI_muestras =  ajustes_graf_SPI * 100 / 5
                    self.plt_SPI.setXRange(ventana_SPI - ajustes_gram_SPI_muestras, ventana_SPI)
                    self.textEdit_VentanaTemporal.setPlainText(str(int(ajustes_graf_SPI)) + " min")
                    self.textEdit_VentanaTemporal.setStyleSheet("color: white;")
                    self.textEdit_VentanaTemporal.setAlignment(QtCore.Qt.AlignCenter)

                #global estado
                lista_estado.append(estado)
                
                self.senal_estado=self.senal_estado[1:]
            
                if lista_estado[-1] != lista_estado[-2]:
                    self.senal_estado.append(100)
                else:
                    self.senal_estado.append(0)
    
                locs_estados = [indice for indice, valor in enumerate(self.senal_estado) if valor == 100]

                if len(locs_estados) > 0:
                    for i in range(len(locs_estados)):
                        x_estado = locs_estados[i]
                        if i == 0:
                            linea_vertical = pg.InfiniteLine(pos=x_estado, angle=90, pen=pg.mkPen('b', width=1))
                            self.plt_SPI.addItem(linea_vertical)
                        elif i == 1:
                            linea_vertical = pg.InfiniteLine(pos=x_estado, angle=90, pen=pg.mkPen('r', width=1))
                            self.plt_SPI.addItem(linea_vertical)
                        elif i == 2:
                            linea_vertical = pg.InfiniteLine(pos=x_estado, angle=90, pen=pg.mkPen('g', width=1))
                            self.plt_SPI.addItem(linea_vertical)
                        elif i == 3:
                            linea_vertical = pg.InfiniteLine(pos=x_estado, angle=90, pen=pg.mkPen('#EE82EE', width=1))
                            self.plt_SPI.addItem(linea_vertical)
                        elif i == 4: 
                            linea_vertical = pg.InfiniteLine(pos=x_estado, angle=90, pen=pg.mkPen('#FFA500', width=1))
                            self.plt_SPI.addItem(linea_vertical)

            global nuevo_valor_filtrado
            nuevo_valor_filtrado = ventana_filtrada_HP[-1]

            self.y=self.y[1:]
            self.y.append(nuevo_valor_filtrado)

            self.plt_PPG.clear()
            self.plt_PPG.plot(self.x, self.y, pen=pg.mkPen('#FFFFFF', width=2))

            global evento
            lista_evento.append(evento)

            if evento != "-":
                tipo_evento = evento[0]
                nombre_evento = evento[1]
                global muestra_evento
                muestra_evento = muestra
            else:
                tipo_evento = "-"
                nombre_evento = "-"
            
            lista_alarma.append(alarma)
            
            if muestra%largo != 0:
                spi_promedio = "-"
            
            from InputDatosPaciente import path_archivo_datos
            with open(path_archivo_datos, 'a') as csv_file:
                fieldnames = ["muestra", "tiempo", "ppg", "ppg filtrado", "spi", "spi_promedio", "estado", "tipo evento", "evento", "alarma"]
                csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)

                info = {
                    "muestra": muestra-largo,
                    "tiempo": (muestra-largo)/fs,
                    "ppg": ppg,
                    "ppg filtrado": nuevo_valor_filtrado,
                    "spi": SPI,
                    "spi_promedio": spi_promedio,
                    "estado": estado,
                    "tipo evento": tipo_evento,
                    "evento": nombre_evento,
                    "alarma": alarma
                }
                csv_writer.writerow(info)

                evento = "-"

                if muestra == muestra_evento + largo:  # mostramos el evento por un período de 1 SPI
                    self.comboBox_Farmaco.setCurrentIndex(0)
                    self.comboBox_ProcQuirurgico.setCurrentIndex(0)
                    self.comboBox_Intercurrencias.setCurrentIndex(0)  


#####################################################################################################################

    def funcDistribGaussiana(self, x, media, desvio):
        coeficiente = 1 / (desvio * np.sqrt(2 * np.pi))
        exponente = -((x - media) ** 2) / (2 * desvio ** 2)
        return coeficiente * np.exp(exponente)

    def funcCombinarNormalizacion(self):  
        directorio_actual = os.path.abspath(os.path.dirname(__file__))
        nombre_excel_normalizacion = 'Curva Normalizacion.xlsx'
        path_normalizacion = os.path.join(directorio_actual, nombre_excel_normalizacion)
        excel_normalizacion = pd.read_excel(path_normalizacion)

        lista_poblacional_HBI = excel_normalizacion['HBI']
        lista_poblacional_PPGA = excel_normalizacion['PPGA']

        nombre_excel_desvios = 'Desvios.xlsx'
        path_desvios = os.path.join(directorio_actual, nombre_excel_desvios)
        excel_desvios = pd.read_excel(path_desvios)

        lista_desvios_HBI = excel_desvios['HBI']
        lista_desvios_PPGA = excel_desvios['PPGA']

        min_poblacional_HBI = np.min(lista_poblacional_HBI)
        max_poblacional_HBI = np.max(lista_poblacional_HBI)
        x_HBI = np.linspace(min_poblacional_HBI, max_poblacional_HBI, max_poblacional_HBI-min_poblacional_HBI+1)
        media_poblacional_HBI = np.mean(lista_poblacional_HBI)
        desvio_poblacional_HBI = np.mean(lista_desvios_HBI) # se hace el promedio de los desvios individuales

        min_poblacional_PPGA = np.min(lista_poblacional_PPGA)
        max_poblacional_PPGA = np.max(lista_poblacional_PPGA)
        x_PPGA = np.linspace(min_poblacional_PPGA, max_poblacional_PPGA, max_poblacional_PPGA-min_poblacional_PPGA+1)
        media_poblacional_PPGA = np.mean(lista_poblacional_PPGA)
        desvio_poblacional_PPGA = np.mean(lista_desvios_PPGA) # se hace el promedio de los desvios individuales

        global lista_individual_HBI, lista_individual_PPGA
        media_individual_HBI = np.mean(np.array(lista_individual_HBI))
        media_individual_PPGA = np.mean(np.array(lista_individual_PPGA))

        peso_individual = (len(lista_individual_HBI)*0.7)/300 # ambas tienen el mismo peso
        if peso_individual > 0.7: 
            peso_individual = 0.7 # pondera: 5 min (= 300 HBI o PPGA) equivale a 70% --> menos tiempo es proporcional, y mayor tiempo satura en 70%
        
        media_combinada_HBI = media_individual_HBI * peso_individual + media_poblacional_HBI * (1-peso_individual)
        media_combinada_PPGA = media_individual_PPGA * peso_individual + media_poblacional_PPGA * (1-peso_individual)

        y_HBI = self.funcDistribGaussiana(x_HBI, media_combinada_HBI, desvio_poblacional_HBI)
        y_PPGA = self.funcDistribGaussiana(x_PPGA, media_combinada_PPGA, desvio_poblacional_PPGA)

        y_HBI = np.cumsum(y_HBI)
        y_HBI = y_HBI.tolist()
        df_TF_HBI = pd.DataFrame({'x HBI': x_HBI, 'y HBI': y_HBI})
        global TF_HBI_combinada
        TF_HBI_combinada = df_TF_HBI.values.tolist()
        TF_HBI_combinada = list(map(lambda x: [int(x[0])] + x[1:], TF_HBI_combinada))

        y_PPGA = np.cumsum(y_PPGA)
        y_PPGA = y_PPGA.tolist()
        df_TF_PPGA = pd.DataFrame({'x PPGA': x_PPGA, 'y PPGA': y_PPGA})
        global TF_PPGA_combinada
        TF_PPGA_combinada = df_TF_PPGA.values.tolist()
        TF_PPGA_combinada = list(map(lambda x: [int(x[0])] + x[1:], TF_PPGA_combinada))


    def funcIniciarCaso(self):
        if not self.serial_communication.isRunning():
            self.serial_communication.start()

        self.pushButton_IniciarCaso.setDisabled(True)
        self.pushButton_Basal.setEnabled(True)
        self.pushButton_AjustarVisualizacionSPI.setEnabled(True)
        self.pushButton_RestablecerVisualizacion.setEnabled(True)
        self.pushButton_ConfigurarAlarmas.setEnabled(True)
        #self.pushButton_ResetAlarmas.setEnabled(True)
        self.comboBox_Farmaco.setEnabled(True)
        self.comboBox_ProcQuirurgico.setEnabled(True)
        self.comboBox_Intercurrencias.setEnabled(True)

        #Configuro el reloj
        self.timer_caso = QTimer()
        self.count_seg = 0
        self.count_min = 0
        self.count_hora = 0
        self.timer_caso.timeout.connect(self.funcLcdNumber_Principal)
        self.timer_caso.start(1000)
        self.funcLcdNumber_Principal()


    def funcLcdNumber_Principal(self):
        #Hago los chequeos de que segundos y minutos no superen 60
        if self.count_seg < 59:
            self.count_seg += 1
        else:
            self.count_seg = 0
            if self.count_min < 59:
                self.count_min += 1
            else:
                self.count_min = 0
                self.count_hora += 1
        
        self.lcdNumber_Principal.setStyleSheet("""QLCDNumber {background-color: rgb(0, 0, 0); color: white; border: 1px solid #808080; }""")
        self.lcdNumber_Principal.display(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))


    def funcNuevoEvento(self):
        farmaco = self.comboBox_Farmaco.currentText()
        procQuirurgico = self.comboBox_ProcQuirurgico.currentText()
        intercurrencia = self.comboBox_Intercurrencias.currentText()

        if farmaco != "-":
            evento_actual = ['Farmaco', farmaco]
        elif procQuirurgico != "-":
            evento_actual = ['ProcQuirurgico', procQuirurgico]
        elif intercurrencia != "-":
            evento_actual = ['Intercurrencia', intercurrencia]
        else:
            evento_actual = "-" # no hay ingreso de evento

        global evento
        evento = evento_actual  

        if evento != "-":
            global listaEventos
            listaEventos.append(evento)
        
            global listaTiemposEventos
            listaTiemposEventos.append(str(self.count_hora) +  ":" + str(self.count_min) + ":" + str(self.count_seg))      


    def funcBasal(self):
        self.pushButton_Basal.setDisabled(True)
        self.pushButton_InicioAnestesia.setEnabled(True)
        self.textEdit_Estado.setPlainText("BASAL")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
        self.lcdNumber_Basal.setStyleSheet("""QLCDNumber {background-color: rgb(0, 0, 0); color: white; border: 1px solid #0000FF; }""")
        self.lcdNumber_Basal.display(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))
    
        global estado
        estado = "basal"

        global listaInicioEstados
        listaInicioEstados.append(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

    def funcInicioAnestesia(self):
        self.pushButton_InicioAnestesia.setDisabled(True)
        self.pushButton_InicioCirugia.setEnabled(True)
        self.textEdit_Estado.setPlainText("INICIO ANESTESIA")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
        QTimer.singleShot(1000, self.funcInduccion)
        self.lcdNumber_InicioAnestesia.setStyleSheet("""QLCDNumber {background-color: rgb(0, 0, 0); color: white; border: 1px solid #FF0000; }""")
        self.lcdNumber_InicioAnestesia.display(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

        global estado 
        estado = "induccion"

        self.funcCombinarNormalizacion()

        global listaInicioEstados
        listaInicioEstados.append(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))


    def funcInduccion(self):
        self.textEdit_Estado.setPlainText("INDUCCION")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")

    def funcInicioCirugia(self):
        self.pushButton_InicioCirugia.setDisabled(True)
        self.pushButton_FinCirugia.setEnabled(True)
        self.textEdit_Estado.setPlainText("INICIO CIRUGIA")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
        QTimer.singleShot(1000, self.funcMantenimiento)
        self.lcdNumber_InicioCirugia.setStyleSheet("""QLCDNumber {background-color: rgb(0, 0, 0); color: white; border: 1px solid #00FF00; }""")
        self.lcdNumber_InicioCirugia.display(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

        global estado
        estado = "mantenimiento"

        global listaInicioEstados
        listaInicioEstados.append(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))


    def funcMantenimiento(self):
        self.textEdit_Estado.setPlainText("MANTENIMIENTO")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")

    def funcFinCirugia(self):
        self.pushButton_FinCirugia.setDisabled(True)
        self.pushButton_FinAnestesia.setEnabled(True)
        self.textEdit_Estado.setPlainText("FIN CIRUGIA")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
        QTimer.singleShot(1000, self.funcDespertar)
        self.lcdNumber_FinCirugia.setStyleSheet("""QLCDNumber {background-color: rgb(0, 0, 0); color: white; border: 1px solid #EE82EE; }""")
        self.lcdNumber_FinCirugia.display(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

        global estado 
        estado = "despertar"

        global listaInicioEstados
        listaInicioEstados.append(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

    def funcDespertar(self):
        self.textEdit_Estado.setPlainText("DESPERTAR")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")

    def funcFinAnestesia(self):
        self.pushButton_FinAnestesia.setDisabled(True)
        self.pushButton_FinalizarCaso.setEnabled(True)
        self.textEdit_Estado.setPlainText("FIN ANESTESIA")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
        QTimer.singleShot(1000, self.funcRecuperacion)
        self.lcdNumber_FinAnestesia.setStyleSheet("""QLCDNumber {background-color: rgb(0, 0, 0); color: white; border: 1px solid #FFA500; }""")
        self.lcdNumber_FinAnestesia.display(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

        global estado
        estado = "recuperacion"

        global listaInicioEstados
        listaInicioEstados.append(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

    def funcRecuperacion(self):
        self.textEdit_Estado.setPlainText("RECUPERACION")
        self.textEdit_Estado.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_Estado.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")


    def funcFinalizarCaso(self):
        
        if self.serial_communication.isRunning():
            self.serial_communication.terminate()
            self.serial_communication.wait()
    
        self.pushButton_FinalizarCaso.setDisabled(True)
        self.pushButton_IniciarCaso.setEnabled(True)
        self.pushButton_RestablecerVisualizacion.setDisabled(True)
        self.textEdit_Estado.setPlainText("")

        global listaInicioEstados
        listaInicioEstados.append(str(self.count_hora) +  ":" + str(self.count_min) + ":" +str(self.count_seg))

        # Paro el reloj porque ya finalizó el caso.
        self.funcStopTimer()

        pop_up = QMessageBox()
        pop_up.setIcon(QMessageBox.Warning)
        pop_up.setWindowTitle("Alerta")
        pop_up.setText("El display principal se cerrará pero la información permanecerá guardada en el informe.")
        pop_up.setStandardButtons(QMessageBox.Ok)
        pop_up.move(350, 400)
        pop_up.exec_()

        #Agrego este monitoreo al registro de monitoreos
        nombre_excel_registros = 'Registro Pacientes.xlsx'
        path_registros = os.path.join(directorio_actual, nombre_excel_registros)
        excel_registros = load_workbook(path_registros)
        hoja_excel_registros = excel_registros["Hoja1"]

        # Para adquirir ID y nombre
        from InputDatosPaciente import listaDatosPaciente, id_global_principal, nombre_archivo_datos, fecha, hora
        nombre = listaDatosPaciente[0]
        apellido = listaDatosPaciente[1]
        id = listaDatosPaciente[2]

        nombre_archivo_informe = 'Informe ' + id_global_principal + '.pdf'

        nuevo_registro = [fecha, hora, id, nombre, apellido, nombre_archivo_informe, nombre_archivo_datos]
        
        hoja_excel_registros.append(nuevo_registro)
        excel_registros.save(path_registros)


        #Ejecuto GraficoSPI.py
        nombre_archivo_ejecutar_GraficoSPI = 'GraficoSPI.py'
        path_archivo_ejecutar_GraficoSPI = os.path.join(directorio_actual, nombre_archivo_ejecutar_GraficoSPI)
        exec(open(path_archivo_ejecutar_GraficoSPI).read())

        #Ejecuto PDF.py
        nombre_archivo_ejecutar_PDF = 'PDF.py'
        path_archivo_ejecutar_PDF = os.path.join(directorio_actual, nombre_archivo_ejecutar_PDF)
        with open(path_archivo_ejecutar_PDF, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        exec(file_contents)


    def funcStopTimer(self):
        self.timer_caso.stop()
        
    def funcRestablecerVisualizacion(self):
        ventana_SPI_visualizada = 100
        self.plt_SPI.setXRange(ventana_SPI-ventana_SPI_visualizada, ventana_SPI)

        global restablecido
        restablecido = True
     

    def funcColorSPI(self):
        from SetUpAlarmas import alarmas
        try:
            SPIValue = int(self.textEdit_SPI.toPlainText())
        except:
            SPIValue = -10

        # No hago los chequeos de >100 o <0 porque es un valor que ponemos nosotras, no lo edita el usuario.
        if SPIValue >= 50:
            self.groupBox_SPI.setStyleSheet("\n""background-color: rgb(255, 0, 0);")
            self.textEdit_SPI.setStyleSheet("\n""background-color: rgb(255, 0, 0);")
            self.label_SPI.setStyleSheet("\n""background-color: rgb(255, 0, 0);")
        elif SPIValue >= 20:
            self.groupBox_SPI.setStyleSheet("\n""background-color: rgb(48, 206, 13);")
            self.textEdit_SPI.setStyleSheet("\n""background-color: rgb(48, 206, 13);")
            self.label_SPI.setStyleSheet("\n""background-color: rgb(48, 206, 13);")        
        elif SPIValue >= 0:
            self.groupBox_SPI.setStyleSheet("\n""background-color: rgb(255, 255, 0);")
            self.textEdit_SPI.setStyleSheet("\n""background-color: rgb(255, 255, 0);")
            self.label_SPI.setStyleSheet("\n""background-color: rgb(255, 255, 0);")
        else:
            self.groupBox_SPI.setStyleSheet("\n""background-color: #F0F0F0;")
            self.textEdit_SPI.setStyleSheet("\n""background-color: #F0F0F0;")
            self.label_SPI.setStyleSheet("\n""background-color: #F0F0F0;")
        
        if alarmas != []:
            SPIMax = alarmas[0]
            SPIMin = alarmas[1]
            TiempoPermanencia = alarmas[2]
            
            global tiempo_condicion
            if SPIValue > SPIMax or SPIValue < SPIMin:
                tiempo_condicion += (largo / fs) # En un contador sería += 1 pero cada spi corresponde a largo / fs segundos (3 segundos)
                
                if (tiempo_condicion >= TiempoPermanencia):
                    if SPIValue > SPIMax:
                        self.funcEjecutarAlarmaFisiologica(caso = "Maximo")
                    elif SPIValue < SPIMin:
                        self.funcEjecutarAlarmaFisiologica(caso = "Minimo")
                    tiempo_condicion = 0

            else: # En este caso no tiene que sonar la alarma
                tiempo_condicion = 0
                self.radioButton_AlarmaFisiologicaReconocida.setChecked(False)
                self.frame_AlarmasFisiologicas.hide()
                self.timer_border_color_SPI.stop() # Freno el timer para que deje de parpadear
                self.groupBox_ReferenciaSPI.setStyleSheet("background-color: rgb(0, 0, 0);") # Le saco el borde de color al group box
                global alarma
                if alarma == "Maximo" or alarma == "Minimo":
                    alarma_actual = "-"
                    alarma = alarma_actual # Actualizo la alarma porque ya no hay condición de alarma


    def funcSetUpAlarmas(self):
        from SetUpAlarmas import alarmas
        if alarmas != []:
            SPIMax = alarmas[0]
            SPIMin = alarmas[1]
            TiempoPermanencia = alarmas[2]

            self.textEdit_Alarma_Max.setPlainText(str(SPIMax))
            self.textEdit_Alarma_Min.setPlainText(str(SPIMin))
            self.textEdit_Alarma_Tiempo.setPlainText(str(TiempoPermanencia) + " seg.")
            self.textEdit_Alarma_Max.setAlignment(QtCore.Qt.AlignCenter)
            self.textEdit_Alarma_Min.setAlignment(QtCore.Qt.AlignCenter)
            self.textEdit_Alarma_Tiempo.setAlignment(QtCore.Qt.AlignCenter)
            self.textEdit_Alarma_Max.setStyleSheet("background-color: rgb(0, 0, 0); color: white; border: 1px solid #808080;")
            self.textEdit_Alarma_Min.setStyleSheet("background-color: rgb(0, 0, 0); color: white; border: 1px solid #808080;")
            self.textEdit_Alarma_Tiempo.setStyleSheet("background-color: rgb(0, 0, 0); color: white; border: 1px solid #808080;")

            global alarmas_seteadas
            if alarmas != alarmas_seteadas:
                # Tengo que reiniciar el frame y el parpadeo de las alarmas fisiológicas porque ahora no sé si se está cumpliendo la condición. Se reincia hasta que chequee
                self.radioButton_AlarmaFisiologicaReconocida.setChecked(False)
                self.frame_AlarmasFisiologicas.hide()
                self.groupBox_ReferenciaSPI.setStyleSheet("background-color: rgb(0, 0, 0);") # Le saco el borde de color al group box
                try:
                    self.timer_border_color_SPI.stop()
                except:
                    pass        
                # Actualizo la variable global 'alarma' porque ya no hay condición de alarma
                global alarma
                alarma_actual = "-"
                alarma = alarma_actual
                # Actualizo alarmas_seteadas
                alarmas_seteadas = alarmas

    def funcEjecutarAlarmaFisiologica(self, caso):
        self.frame_AlarmasFisiologicas.show()

        if caso == "Maximo":
            self.label_MensajeAlarmaFisiologicaMaximo.show()
            self.label_MensajeAlarmaFisiologicaMinimo.hide()
        elif caso == "Minimo":
            self.label_MensajeAlarmaFisiologicaMinimo.show()
            self.label_MensajeAlarmaFisiologicaMaximo.hide()

        # Actualizo la variable global 'alarma' porque tengo una condición de alarma fisiológica
        alarma_actual = caso
        global alarma
        alarma = alarma_actual

        # Si no está marcada como reconocida, la ejecuto
        if not self.radioButton_AlarmaFisiologicaReconocida.isChecked():
            # Inicializar variables para el parpadeo
            self.border_colors_SPI = [QColor(255, 165, 0), QColor(255, 255, 255)]  # Naranja y blanco
            self.border_color_index_SPI = 0

            # Crear un temporizador para cambiar el color del borde
            self.timer_border_color_SPI = QTimer()
            self.timer_border_color_SPI.timeout.connect(self.funcCambiarColorFrameSPI)
            self.timer_border_color_SPI.start(500)  # Cambiar cada 0.5 segundos

            # Alarma auditiva
            #self.funcAlarmaAuditiva(caso)

    def funcCambiarColorFrameSPI(self):
        self.border_color_index_SPI = (self.border_color_index_SPI + 1) % len(self.border_colors_SPI)
        color = self.border_colors_SPI[self.border_color_index_SPI]
        self.groupBox_ReferenciaSPI.setStyleSheet(f"#groupBox_ReferenciaSPI {{ border: 6px solid {color.name()}; }}")

    def funcAlarmaFisiologicaReconocida(self):
        if self.radioButton_AlarmaFisiologicaReconocida.isChecked():
            self.label_AlarmaFisiologicaReconocida.show()
            self.timer_border_color_SPI.stop() # Freno el timer para que deje de parpadear
            self.groupBox_ReferenciaSPI.setStyleSheet("background-color: rgb(0, 0, 0);") # Le saco el borde de color al group box
        else:
            self.label_AlarmaFisiologicaReconocida.hide()    

    def funcEjecutarAlarmaTecnica(self, caso):
        self.frame_AlarmasTecnicas.show()

        if caso == "Movimiento":
            self.label_MensajeAlarmaTecnicaMovimiento.show()
            self.label_MensajeAlarmaTecnicaDesconexion.hide()
        elif caso == "Desconexión":
            self.label_MensajeAlarmaTecnicaDesconexion.show()
            self.label_MensajeAlarmaTecnicaMovimiento.hide()

        # Actualizo la variable global 'alarma' porque tengo una condición de alarma técnica
        alarma_actual = caso
        global alarma
        alarma = alarma_actual

        # Si no está marcada como reconocida, la ejecuto
        if not self.radioButton_AlarmaTecnicaReconocida.isChecked():
            # Inicializar variables para el parpadeo
            self.border_colors_PPG = [QColor(255, 165, 0), QColor(255, 255, 255)]  # Naranja y rojo
            self.border_color_index_PPG = 0

            # Crear un temporizador para cambiar el color del borde
            self.timer_border_color_PPG = QTimer()
            self.timer_border_color_PPG.timeout.connect(self.funcCambiarColorFramePPG)
            self.timer_border_color_PPG.start(500) # Le cambio el color cada 0.5 segundos

            global ejecutar_alarma_auditiva
            if ejecutar_alarma_auditiva == True:
                self.funcAlarmaAuditiva(caso)
                ejecutar_alarma_auditiva = False


    def funcAlarmaAuditiva(self, caso):
        directorio_actual = os.path.abspath(os.path.dirname(__file__))
        if caso == "Movimiento" or caso == "Desconexión": # En realidad si no vamos a hacer alarmas auditivas por SPI esto se puede ir
            nombre_alarma = 'pulso_personalizado_tecnica.wav'
        elif caso == "Maximo" or caso == "Minimo":
            nombre_alarma = 'pulso_personalizado_fisiologica.wav'
        path = os.path.join(directorio_actual, nombre_alarma)
        # Reproducir el archivo de audio con pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        # Esperar hasta que se termine de reproducir
        pygame.time.wait(int(0.2 * 1000))  # Esperar según la duración del pulso en milisegundos --> duración de 0.2s para ambos
        # Detener la reproducción
        pygame.mixer.music.stop()
    

    def funcCambiarColorFramePPG(self):
        self.border_color_index_PPG = (self.border_color_index_PPG + 1) % len(self.border_colors_PPG)
        color = self.border_colors_PPG[self.border_color_index_PPG]
        self.frame_PPG.setStyleSheet(f"#frame_PPG {{ border: 6px solid {color.name()}; }}")
        self.centralwidget.setStyleSheet(f"background-color: {color.name()};")

    def funcAlarmaTecnicaReconocida(self):
        if self.radioButton_AlarmaTecnicaReconocida.isChecked():
            self.label_AlarmaTecnicaReconocida.show()
            self.timer_border_color_PPG.stop() # Freno el timer para que deje de parpadear
            self.frame_PPG.setStyleSheet("background-color: rgb(0, 0, 0); border: 1px solid #F0F0F0;") # Le saco el borde de color al group box
        else:
            self.label_AlarmaTecnicaReconocida.hide()        





###############################################################################################################################
    
    def retranslateUi(self, DisplayPrincipal):
        _translate = QtCore.QCoreApplication.translate
        DisplayPrincipal.setWindowTitle(_translate("DisplayPrincipal", "MainWindow"))
        self.pushButton_IniciarCaso.setText(_translate("DisplayPrincipal", "Iniciar Caso"))
        self.pushButton_FinalizarCaso.setText(_translate("DisplayPrincipal", "Finalizar Caso"))
        self.label_Estado.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"center\"><span style=\"font-size: 14pt; color: WHITE;\">ESTADO</span></p></body></html>"))
        self.label_VentanaTemporal.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 10pt; color: white;\">Ventana temporal <br> visualizada:</span></p></body></html>"))
        self.label_Alarmas.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"center\"><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 14pt; color: white;\">ALARMAS</span></p></body></html>"))
        self.label_Alarma_Max.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 9pt; color: white;\">Máx.</span></p></body></html>"))
        self.label_Alarma_Min.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 9pt; color: white;\">Mín.</span></p></body></html>"))
        self.label_Alarma_Tiempo.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 9pt; color: white;\">Permanencia</span></p></body></html>"))
        self.label_TextoAlarmaFisiologicaReconocida.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\">Alarma reconocida</span></p></body></html>"))
        self.label_TextoAlarmaTecnicaReconocida.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\">Alarma reconocida</span></p></body></html>"))
        self.label_MensajeAlarmaTecnicaMovimiento.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\"><b>Sensor colocado incorrectamente</b></span></p></body></html>"))
        self.label_MensajeAlarmaTecnicaDesconexion.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\"><b>Sensor desconectado</b></span></p></body></html>"))
        self.label_MensajeAlarmaFisiologicaMaximo.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\"><b>SPI &gt; SPI_Max</b></span></p></body></html>"))
        self.label_MensajeAlarmaFisiologicaMinimo.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\"><b>SPI &lt; SPI_Min</b></span></p></body></html>"))
        self.label_Eventos.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"center\"><span style=\"font-size: 14pt; color: WHITE;\">INGRESO DE EVENTOS</span></p></body></html>"))
        self.label_FarmacosAnalgesicos.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\">Fármaco analgésico</span></p></body></html>"))
        self.label_ProcQuirurgico.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\">Procedimiento quirúrgico</span></p></body></html>"))
        self.label_Intercurrencia.setText(_translate("DisplayPrincipal", "<html><head/><body><p><span style=\"font-family: 'MS Shell Dlg 2'; font-size: 11pt; color: white;\">Intercurrencia</span></p></body></html>"))        
        self.pushButton_Basal.setText(_translate("DisplayPrincipal", "Basal"))
        self.pushButton_InicioAnestesia.setText(_translate("DisplayPrincipal", "Inicio Anestesia"))
        self.pushButton_InicioCirugia.setText(_translate("DisplayPrincipal", "Inicio Cirugía"))
        self.pushButton_FinCirugia.setText(_translate("DisplayPrincipal", "Fin Cirugía"))
        self.pushButton_FinAnestesia.setText(_translate("DisplayPrincipal", "Fin Anestesia"))
        self.textEdit_Estado.setHtml(_translate("DisplayPrincipal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n""<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_VentanaTemporal.setHtml(_translate("DisplayPrincipal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n""<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_Alarma_Max.setHtml(_translate("DisplayPrincipal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n""<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_Alarma_Min.setHtml(_translate("DisplayPrincipal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n""<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_Alarma_Tiempo.setHtml(_translate("DisplayPrincipal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n""<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_ConfigurarAlarmas.setText(_translate("DisplayPrincipal", "Configurar Alarmas"))
        #self.pushButton_ResetAlarmas.setText(_translate("DisplayPrincipal", "Reset Alarmas"))
        self.pushButton_AjustarVisualizacionSPI.setText(_translate("DisplayPrincipal", "Ajustar \n""Visualización"))
        self.pushButton_RestablecerVisualizacion.setText(_translate("DisplayPrincipal", "Restablecer \n""Visualización"))
        self.label_AnalgesiaInsuficiente.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"center\" style style=\"line-height: 20%\" >Analgesia</p><p% align=\"center\">Insuficiente</p></body></html>\n"""))
        self.label_AnalgesiaAdecuada.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"center\" style style=\"line-height: 20%\" >Analgesia</p><p% align=\"center\">Adecuada</p></body></html>\n"""))
        self.label_AnalgesiaExcesiva.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"center\" style style=\"line-height: 20%\" >Analgesia</p><p% align=\"center\">Excesiva</p></body></html>\n"""))
        self.label_50.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"right\" style=\"color: white;\">50 </p></body></html>"))
        self.label_0.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"right\" style=\"color: white;\">0 </p></body></html>"))
        self.label_20.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"right\" style=\"color: white;\">20 </p><p align=\"right\"><br/></p></body></html>"))
        self.label_SPI.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"center\"><span style=\"font-size:24pt; color: black;\">SPI</span></p></body></html>"))
        self.label_100.setText(_translate("DisplayPrincipal", "<html><head/><body><p align=\"right\" style=\"color: white;\">100 </p></body></html>"))
        self.textEdit_SPI.setHtml(_translate("DisplayPrincipal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:30pt; font-weight:400; font-style:normal;\">\n""<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br />-</p></body></html>"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DisplayPrincipal = QtWidgets.QMainWindow()
    ui = Ui_DisplayPrincipal()
    ui.setupUi(DisplayPrincipal)
    DisplayPrincipal.showMaximized()
    sys.exit(app.exec_())
