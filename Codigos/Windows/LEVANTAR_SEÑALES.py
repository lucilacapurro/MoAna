import sys
import time
import csv

import pyqtgraph as pg
from PyQt5.QtCore import Qt, QTimer, QByteArray, QIODevice
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

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

path_archivo_datos = 'DATA_YASSEF1.csv'

fieldnames = ["Muestra", "Tiempo", "PPG"]

with open(path_archivo_datos, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer.writeheader()

global muestra 
muestra = 0

global ppg 
ppg = 0 

fs = 50


class SerialPortExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serial Port Example")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Configura la gráfica de PyQtGraph
        self.graph_widget = pg.PlotWidget()
        self.layout.addWidget(self.graph_widget)
        self.plot = self.graph_widget.plot()
        self.x_data = []
        self.y_data = []

        self.open_button = QPushButton("Open Serial Port")
        self.open_button.clicked.connect(self.open_serial_port)
        self.layout.addWidget(self.open_button)

        self.close_button = QPushButton("Close Serial Port")
        self.close_button.clicked.connect(self.close_serial_port)
        self.layout.addWidget(self.close_button)

        self.serial_port = None  # Serial port instance
        self.data = []  # Data storage list

        self.update_interval = int(1000*(1/fs))  # Update interval in milliseconds (adjust as needed)
        self.time_window = 3.0  # Time window to display in seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_data_periodically)
        self.start_time = time.time()  # Time when the plot started

    def open_serial_port(self):
        port_name = "COM6"  # Replace with your port name
        baud_rate = 230400  # Replace with your desired baud rate

        if self.serial_port is None:
            self.serial_port = QSerialPort(self)
            self.serial_port.setPortName(port_name)
            self.serial_port.setBaudRate(baud_rate)

            if self.serial_port.open(QSerialPort.ReadWrite):
                print(f"Serial port {port_name} opened successfully.")
                self.timer.start(self.update_interval)
            else:
                print(f"Failed to open serial port {port_name}.")
        else:
            print("Serial port is already open.")

    def close_serial_port(self):
        if self.serial_port is not None:
            self.timer.stop()
            self.serial_port.close()
            print("Serial port closed.")
            self.serial_port = None
        else:
            print("Serial port is not open.")

    def read_data_periodically(self):
        if self.serial_port is not None:
            try:
                new_data = -read_register(self.serial_port, address=[0x32, 0x43])
                self.data.append(new_data)
                print(f"Received data: {new_data}")

                global muestra 
                muestra += 1

                global ppg
                if muestra == 3:
                    ppg = new_data

                elif muestra > 3 and abs(new_data - ppg) < 100000: 
                    ppg = new_data
                
                    # Agrega nuevos datos a las listas de valores x e y
                    elapsed_time = time.time() - self.start_time
                    self.x_data.append(elapsed_time)
                    self.y_data.append(-ppg)

                    # Actualiza el gráfico de PyQtGraph
                    self.plot.setData(self.x_data, self.y_data)

                    # Ajusta el rango del eje X para mostrar solo la última ventana de 5 segundos
                    if elapsed_time > self.time_window:
                        self.graph_widget.setXRange(elapsed_time - self.time_window, elapsed_time)

                    # Calcula el rango de amplitud para la ventana de 5 segundos
                    min_y = min(self.y_data[-int(self.time_window * 1000 / self.update_interval):])
                    max_y = max(self.y_data[-int(self.time_window * 1000 / self.update_interval):])

                    # Ajusta automáticamente el rango del eje Y
                    self.graph_widget.setYRange(min_y, max_y)
                
                    with open(path_archivo_datos, 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)

                        info = {
                            "Muestra": muestra,
                            "Tiempo": (muestra)/fs,
                            "PPG": ppg,
                        }

                        csv_writer.writerow(info)


            except Exception as e:
                print(f"Error reading data: {e}")
        else:
            print("Serial port is not open.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialPortExample()
    window.show()
    sys.exit(app.exec_())
