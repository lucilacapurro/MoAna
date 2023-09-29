import sys
import time
import csv
import serial

import pyqtgraph
from PyQt5.QtCore import Qt, QTimer, QByteArray, QIODevice, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

import sys
import serial
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pyqtgraph import PlotWidget

#####################################################################################################################

# FUNCTIONS:

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


#####################################################################################################################

# CAMBIAR NOMBRE ARCHIVO!!!
path_archivo_datos = 'DATA.csv'

fieldnames = ["PPG"]

with open(path_archivo_datos, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer.writeheader()

global muestra 
muestra = 0

global ppg 
ppg = 0 

fs = 500

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

        print("Inicio de adquisicion de datos.")

        while self.serial_port and self.serial_port.is_open:
            global prev_data
            if nueva_muestra == 0:
                prev_data = -read_register(self.serial_port, address=[0x32, 0x43])
                nueva_muestra += 1
            else:
                new_data = -read_register(self.serial_port, address=[0x32, 0x43])
                    
                nueva_muestra += 1
                
                if new_data != prev_data:

                    global data
                    data.append(new_data)

                    prev_data = new_data 


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Levantar señales")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Configura la gráfica de PyQtGraph
        self.graph_widget = PlotWidget()
        self.layout.addWidget(self.graph_widget)
        
        self.x_data = []
        self.y_data = []

        self.open_button = QPushButton("Open Serial Port")
        self.open_button.clicked.connect(self.recibir_datos)
        self.layout.addWidget(self.open_button)

        self.close_button = QPushButton("Close Serial Port")
        self.close_button.clicked.connect(self.terminar_recibir_datos)
        self.layout.addWidget(self.close_button)

        fs_graf = 50
        self.time_window = 3*fs_graf
        self.update_interval = int(1000*(1/fs_graf))

        self.serial_communication = SerialCommunication(port="COM6", baudrate=230400)

        self.serial_communication.data_received.connect(self.graficar_datos)


    def recibir_datos(self):
        if self.serial_communication.isRunning():
            self.serial_communication.terminate()
            self.serial_communication.wait()


    def graficar_datos(self, data):
        data = int(data)

        global muestra 
        muestra +=1 

        self.x_data.append(muestra)
        self.y_data.append(data)
        
        # Actualiza el gráfico de PyQtGraph
        self.graph_widget.clear()
        
        self.graph_widget.plot(self.x_data, self.y_data)

        # Ajusta el rango del eje X para mostrar solo la última ventana de 5 segundos
        if muestra > self.time_window:
            self.graph_widget.setXRange(muestra - self.time_window, muestra)

        # Calcula el rango de amplitud para la ventana de 5 segundos
        min_y = min(self.y_data[-int(self.time_window * self.time_window / self.update_interval):])
        max_y = max(self.y_data[-int(self.time_window * self.time_window / self.update_interval):])

        # Ajusta automáticamente el rango del eje Y
        self.graph_widget.setYRange(min_y, max_y)

    def terminar_recibir_datos(self):

        if self.serial_communication.isRunning():
            self.serial_communication.terminate()

        with open(path_archivo_datos, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            csv_writer.writeheader()

            for value in data:
                info = {
                    "PPG": value,
                }
                csv_writer.writerow(info)      

        print("Ya se guardaron los datos en el csv.")  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())







