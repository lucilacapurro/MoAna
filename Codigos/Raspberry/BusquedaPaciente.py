from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import plotly
import plotly.express as px
import pandas as pd 
import os

###########################################################################################################

global id_global_busqueda
id_global_busqueda = ""

###########################################################################################################
class Ui_BusquedaPacientes(object):

    # Funciones para abrir otras ventanas:

    # Ventana de inicio
    def openInicio(self):
        from Inicio import Ui_MainWindow
        self.windowInicio = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.windowInicio)
        self.windowInicio.showMaximized()
    
    # Ventana de opciones de informe para el registro seleccionado
    def openOpcionesInforme(self):
        from OpcionesInforme import Ui_OpcionesInforme
        self.windowOpcionesInforme = QtWidgets.QMainWindow()
        self.ui = Ui_OpcionesInforme()
        self.ui.setupUi(self.windowOpcionesInforme)
        self.windowOpcionesInforme.showMaximized()


    # Funciones para abrir los teclados:

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit Nombre
    def openTecladoVirtual_Nombre(self, target_edit):
        from TecladoVirtual import VirtualKeyboard 
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Nombre)
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(515, 450)

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit Apellido
    def openTecladoVirtual_Apellido(self, target_edit):
        from TecladoVirtual import VirtualKeyboard  
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Apellido) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(515, 485)
    
    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit ID
    def openTecladoVirtual_ID(self, target_edit):
        from TecladoVirtual import VirtualKeyboard 
        self.virtual_keyboard = VirtualKeyboard(target_edit) 
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_ID) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(515, 525)
    
    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit Dia
    def openTecladoVirtual_Dia(self, target_edit):
        from TecladoVirtual import VirtualKeyboard  
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Dia)  
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(515, 575)

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit Mes
    def openTecladoVirtual_Mes(self, target_edit):
        from TecladoVirtual import VirtualKeyboard  
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Mes)  
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(515, 575)
    
    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit Año
    def openTecladoVirtual_Ao(self, target_edit):
        from TecladoVirtual import VirtualKeyboard  
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Ao)  
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(515, 575)


###########################################################################################################

    def setupUi(self, BusquedaPacientes):
        BusquedaPacientes.setObjectName("BusquedaPacientes")
        # Obtiene el tamaño de la pantalla
        desktop = QtWidgets.QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        BusquedaPacientes.setGeometry(screen_rect)
        
        self.centralwidget = QtWidgets.QWidget(BusquedaPacientes)
        self.centralwidget.setObjectName("centralwidget")
        
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(294, 104, 772, 492))
        frame_width = 772
        frame_height = 492
        center_x = (BusquedaPacientes.width() - frame_width) // 2
        center_y = (BusquedaPacientes.height() - frame_height) // 2
        self.frame.setGeometry(QtCore.QRect(center_x, center_y, frame_width, frame_height))
        self.frame.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.groupBox_BusquedaPaciente = QtWidgets.QGroupBox(self.frame)
        self.groupBox_BusquedaPaciente.setGeometry(QtCore.QRect(10, 10, 632, 472))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_BusquedaPaciente.setFont(font)
        self.groupBox_BusquedaPaciente.setAutoFillBackground(False)
        self.groupBox_BusquedaPaciente.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_BusquedaPaciente.setObjectName("groupBox_BusquedaPaciente")
        
        # Sección buscar Nombre 
        self.label_BuscarNombre = QtWidgets.QLabel(self.groupBox_BusquedaPaciente)
        self.label_BuscarNombre.setGeometry(QtCore.QRect(10, 40, 57, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_BuscarNombre.setFont(font)
        self.label_BuscarNombre.setObjectName("label_BuscarNombre")
        
        self.lineEdit_BuscarNombre = QtWidgets.QLineEdit(self.groupBox_BusquedaPaciente)
        self.lineEdit_BuscarNombre.setGeometry(QtCore.QRect(80, 50, 541, 29))
        self.lineEdit_BuscarNombre.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_BuscarNombre.setFrame(False)
        self.lineEdit_BuscarNombre.setObjectName("lineEdit_BuscarNombre")

        # Sección buscar Apellido 
        self.label_BuscarApellido = QtWidgets.QLabel(self.groupBox_BusquedaPaciente)
        self.label_BuscarApellido.setGeometry(QtCore.QRect(10, 85, 57, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_BuscarApellido.setFont(font)
        self.label_BuscarApellido.setObjectName("label_BuscarApellido")
        
        self.lineEdit_BuscarApellido = QtWidgets.QLineEdit(self.groupBox_BusquedaPaciente)
        self.lineEdit_BuscarApellido.setGeometry(QtCore.QRect(80, 95, 541, 29))
        self.lineEdit_BuscarApellido.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_BuscarApellido.setFrame(False)
        self.lineEdit_BuscarApellido.setObjectName("lineEdit_BuscarApellido")

        # Sección buscar ID
        self.label_BuscarID = QtWidgets.QLabel(self.groupBox_BusquedaPaciente)
        self.label_BuscarID.setGeometry(QtCore.QRect(10, 130, 26, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_BuscarID.setFont(font)
        self.label_BuscarID.setObjectName("label_BuscarID")
    
        self.lineEdit_BuscarID = QtWidgets.QLineEdit(self.groupBox_BusquedaPaciente)
        self.lineEdit_BuscarID.setGeometry(QtCore.QRect(80, 140, 541, 29))
        self.lineEdit_BuscarID.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_BuscarID.setFrame(False)
        self.lineEdit_BuscarID.setObjectName("lineEdit_BuscarID")
        
        # Sección buscar Fecha: día / mes / año
        self.label_BuscarFecha = QtWidgets.QLabel(self.groupBox_BusquedaPaciente)
        self.label_BuscarFecha.setGeometry(QtCore.QRect(11, 175, 49, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_BuscarFecha.setFont(font)
        self.label_BuscarFecha.setObjectName("label_BuscarFecha")
        # Dia
        self.lineEdit_BuscarDia = QtWidgets.QLineEdit(self.groupBox_BusquedaPaciente)
        self.lineEdit_BuscarDia.setGeometry(QtCore.QRect(80, 185, 41, 29))
        self.lineEdit_BuscarDia.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_BuscarDia.setFrame(False)
        self.lineEdit_BuscarDia.setObjectName("lineEdit_BuscarDia")
        # /
        self.label_Barra = QtWidgets.QLabel(self.groupBox_BusquedaPaciente)
        self.label_Barra.setGeometry(QtCore.QRect(130, 175, 16, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_Barra.setFont(font)
        self.label_Barra.setObjectName("label_Barra")
        # Mes
        self.lineEdit_BuscarMes = QtWidgets.QLineEdit(self.groupBox_BusquedaPaciente)
        self.lineEdit_BuscarMes.setGeometry(QtCore.QRect(150, 185, 41, 29))
        self.lineEdit_BuscarMes.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_BuscarMes.setFrame(False)
        self.lineEdit_BuscarMes.setObjectName("lineEdit_BuscarMes")
        # /
        self.label_Barra_2 = QtWidgets.QLabel(self.groupBox_BusquedaPaciente)
        self.label_Barra_2.setGeometry(QtCore.QRect(200, 175, 16, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_Barra_2.setFont(font)
        self.label_Barra_2.setObjectName("label_Barra_2")
        # Año
        self.lineEdit_BuscarAo = QtWidgets.QLineEdit(self.groupBox_BusquedaPaciente)
        self.lineEdit_BuscarAo.setGeometry(QtCore.QRect(220, 185, 61, 29))
        self.lineEdit_BuscarAo.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_BuscarAo.setFrame(False)
        self.lineEdit_BuscarAo.setObjectName("lineEdit_BuscarAo")
        
        # Listado de registros 
        self.listWidget_ListadoPacientes = QtWidgets.QListWidget(self.groupBox_BusquedaPaciente)
        self.listWidget_ListadoPacientes.setGeometry(QtCore.QRect(10, 260, 611, 155))
        self.listWidget_ListadoPacientes.setObjectName("listWidget_ListadoPacientes")
        self.listWidget_ListadoPacientes.itemSelectionChanged.connect(self.funcSeleccionarRegistro)
        
        # Botón para buscar 
        self.pushButton_BuscarPaciente = QtWidgets.QPushButton(self.groupBox_BusquedaPaciente)
        self.pushButton_BuscarPaciente.setGeometry(QtCore.QRect(540, 220, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_BuscarPaciente.setFont(font)
        self.pushButton_BuscarPaciente.setAutoFillBackground(False)
        self.pushButton_BuscarPaciente.setStyleSheet("background-color: rgb(243, 243, 243);\n""")
        self.pushButton_BuscarPaciente.setAutoDefault(False)
        self.pushButton_BuscarPaciente.setObjectName("pushButton_BuscarPaciente")
        self.pushButton_BuscarPaciente.clicked.connect(self.funcBusquedaRegistros)
        
        # Botón para seleccionar un registro
        self.pushButton_SeleccionarPaciente = QtWidgets.QPushButton(self.groupBox_BusquedaPaciente)
        self.pushButton_SeleccionarPaciente.setGeometry(QtCore.QRect(540, 425, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_SeleccionarPaciente.setFont(font)
        self.pushButton_SeleccionarPaciente.setAutoFillBackground(False)
        self.pushButton_SeleccionarPaciente.setStyleSheet("background-color: rgb(243, 243, 243);\n""")
        self.pushButton_SeleccionarPaciente.setAutoDefault(False)
        self.pushButton_SeleccionarPaciente.setObjectName("pushButton_SeleccionarPaciente")
        self.pushButton_SeleccionarPaciente.setEnabled(False)
        self.pushButton_SeleccionarPaciente.clicked.connect(self.funcHacerGraficosRegistro)
        self.pushButton_SeleccionarPaciente.clicked.connect(self.openOpcionesInforme)
        self.pushButton_SeleccionarPaciente.clicked.connect(lambda: BusquedaPacientes.close())

        # Botón para volver a la ventana de inicio 
        self.pushButton_VolverBusquedaPaciente = QtWidgets.QPushButton(self.frame)
        self.pushButton_VolverBusquedaPaciente.setGeometry(QtCore.QRect(frame_width - 121, frame_height - 51, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_VolverBusquedaPaciente.setFont(font)
        self.pushButton_VolverBusquedaPaciente.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_VolverBusquedaPaciente.setObjectName("pushButton_VolverBusquedaPaciente")
        self.pushButton_VolverBusquedaPaciente.clicked.connect(self.openInicio)
        self.pushButton_VolverBusquedaPaciente.clicked.connect(lambda: BusquedaPacientes.close())

        # Conecta la señal selectionChanged del QLineEdit para abrir el teclado virtual para cada campo de búsqueda
        self.lineEdit_BuscarNombre.selectionChanged.connect(lambda: self.openTecladoVirtual_Nombre(self.lineEdit_BuscarNombre))
        self.lineEdit_BuscarApellido.selectionChanged.connect(lambda: self.openTecladoVirtual_Apellido(self.lineEdit_BuscarApellido))
        self.lineEdit_BuscarID.selectionChanged.connect(lambda: self.openTecladoVirtual_ID(self.lineEdit_BuscarID))
        self.lineEdit_BuscarDia.selectionChanged.connect(lambda: self.openTecladoVirtual_Dia(self.lineEdit_BuscarDia))
        self.lineEdit_BuscarMes.selectionChanged.connect(lambda: self.openTecladoVirtual_Mes(self.lineEdit_BuscarMes))
        self.lineEdit_BuscarAo.selectionChanged.connect(lambda: self.openTecladoVirtual_Ao(self.lineEdit_BuscarAo))
        
        self.frame.raise_()
        self.groupBox_BusquedaPaciente.raise_()
        self.pushButton_VolverBusquedaPaciente.raise_()
        BusquedaPacientes.setCentralWidget(self.centralwidget)

        self.retranslateUi(BusquedaPacientes)
        QtCore.QMetaObject.connectSlotsByName(BusquedaPacientes)

###########################################################################################################
# FUNCIONES:

    # Funciones para actualizar los QLineEdit con el texto ingresado desde el teclado virtual
    def update_line_edit_Nombre(self, char):
        current_text = self.lineEdit_BuscarNombre.text()
        self.lineEdit_BuscarNombre.setText(current_text + char)
    
    def update_line_edit_Apellido(self, char):
        current_text = self.lineEdit_BuscarApellido.text()
        self.lineEdit_BuscarApellido.setText(current_text + char)

    def update_line_edit_ID(self, char):
        current_text = self.lineEdit_BuscarID.text()
        self.lineEdit_BuscarID.setText(current_text + char)
    
    def update_line_edit_Dia(self, char):
        current_text = self.lineEdit_BuscarDia.text()  
        self.lineEdit_BuscarDia.setText(current_text + char)
    
    def update_line_edit_Mes(self, char):
        current_text = self.lineEdit_BuscarMes.text()
        self.lineEdit_BuscarMes.setText(current_text + char)

    def update_line_edit_Ao(self, char):
        current_text = self.lineEdit_BuscarAo.text()
        self.lineEdit_BuscarAo.setText(current_text + char)


    # Función para realizar la búsqueda de registros según los filtros aplicados a los campos de búsqueda
    def funcBusquedaRegistros(self):
        self.lineEdit_BuscarNombre.setEnabled(False)
        self.lineEdit_BuscarApellido.setEnabled(False)
        self.lineEdit_BuscarID.setEnabled(False)
        self.lineEdit_BuscarDia.setEnabled(False)
        self.lineEdit_BuscarMes.setEnabled(False)
        self.lineEdit_BuscarAo.setEnabled(False)

        # primero borra todo lo que haya en la list widget, por las dudas de que haya hecho una búsqueda previa
        self.listWidget_ListadoPacientes.clear()

        # levanta los filtros ingresados
        nombre = self.lineEdit_BuscarNombre.text()
        apellido = self.lineEdit_BuscarApellido.text()
        id = self.lineEdit_BuscarID.text()
        ano = self.lineEdit_BuscarAo.text()
        mes = self.lineEdit_BuscarMes.text()
        dia = self.lineEdit_BuscarDia.text()
        fecha = ''

        # Obtiene los registros de la base de datos
        directorio_actual = os.path.abspath(os.path.dirname(__file__))
        excel_registros = 'Registro Pacientes.xlsx'
        path_excel_registros = os.path.join(directorio_actual, excel_registros)
        df_lista_busqueda = pd.read_excel(path_excel_registros)

        # Hace los chequeos de errores de los ingresos y aplica los filtros
        if ano!='' or mes!='' or dia!='':
            if ano!='':
                try: 
                    ano = int(ano)
                    if ano<1000:
                        pop_up = QMessageBox()
                        pop_up.setIcon(QMessageBox.Critical)
                        pop_up.setWindowTitle("Alerta")
                        pop_up.setText("El año ingresado es inválido. Reingréselo.")
                        pop_up.exec_()
                        self.lineEdit_BuscarNombre.setEnabled(True)
                        self.lineEdit_BuscarApellido.setEnabled(True)
                        self.lineEdit_BuscarID.setEnabled(True)
                        self.lineEdit_BuscarDia.setEnabled(True)
                        self.lineEdit_BuscarMes.setEnabled(True)
                        self.lineEdit_BuscarAo.setEnabled(True)
                    else:
                        if df_lista_busqueda.shape[0]!=0:
                            filtro_ano = df_lista_busqueda['fecha'].apply(lambda x: str(x.year)).str.contains(str(ano))
                            df_lista_busqueda = df_lista_busqueda[filtro_ano]
                except:
                    pop_up = QMessageBox()
                    pop_up.setIcon(QMessageBox.Critical)
                    pop_up.setWindowTitle("Alerta")
                    pop_up.setText("El año ingresado es incorrecto. Reingréselo.")
                    pop_up.exec_()  
                    self.lineEdit_BuscarNombre.setEnabled(True)
                    self.lineEdit_BuscarApellido.setEnabled(True)
                    self.lineEdit_BuscarID.setEnabled(True)
                    self.lineEdit_BuscarDia.setEnabled(True)
                    self.lineEdit_BuscarMes.setEnabled(True)
                    self.lineEdit_BuscarAo.setEnabled(True)
            if mes!='':
                try: 
                    mes = int(mes)
                    if mes<=0 or mes>12:
                        pop_up = QMessageBox()
                        pop_up.setIcon(QMessageBox.Critical)
                        pop_up.setWindowTitle("Alerta")
                        pop_up.setText("El mes ingresado es inválido. Reingréselo.")
                        pop_up.exec_()
                        self.lineEdit_BuscarNombre.setEnabled(True)
                        self.lineEdit_BuscarApellido.setEnabled(True)
                        self.lineEdit_BuscarID.setEnabled(True)
                        self.lineEdit_BuscarDia.setEnabled(True)
                        self.lineEdit_BuscarMes.setEnabled(True)
                        self.lineEdit_BuscarAo.setEnabled(True)
                    else:
                        mes = str(mes)
                        if df_lista_busqueda.shape[0]!=0:
                            filtro_mes = df_lista_busqueda['fecha'].apply(lambda x: str(x.month)).str.contains(mes)
                            df_lista_busqueda = df_lista_busqueda[filtro_mes]
                except:
                    pop_up = QMessageBox()
                    pop_up.setIcon(QMessageBox.Critical)
                    pop_up.setWindowTitle("Alerta")
                    pop_up.setText("El mes ingresado es incorrecto. Reingréselo.")
                    pop_up.exec_() 
                    self.lineEdit_BuscarNombre.setEnabled(True)
                    self.lineEdit_BuscarApellido.setEnabled(True)
                    self.lineEdit_BuscarID.setEnabled(True)
                    self.lineEdit_BuscarDia.setEnabled(True)
                    self.lineEdit_BuscarMes.setEnabled(True)
                    self.lineEdit_BuscarAo.setEnabled(True)
            if dia!='':
                try: 
                    dia = int(dia)
                    if dia<=0 or 31<dia:
                        pop_up = QMessageBox()
                        pop_up.setIcon(QMessageBox.Critical)
                        pop_up.setWindowTitle("Alerta")
                        pop_up.setText("El día ingreso es inválido. Reingréselo.")
                        pop_up.exec_()
                        self.lineEdit_BuscarNombre.setEnabled(True)
                        self.lineEdit_BuscarApellido.setEnabled(True)
                        self.lineEdit_BuscarID.setEnabled(True)
                        self.lineEdit_BuscarDia.setEnabled(True)
                        self.lineEdit_BuscarMes.setEnabled(True)
                        self.lineEdit_BuscarAo.setEnabled(True)
                    else:
                        dia = str(dia)
                        if df_lista_busqueda.shape[0]!=0:
                            filtro_dia = df_lista_busqueda['fecha'].apply(lambda x: str(x.day)).str.contains(dia)
                            df_lista_busqueda = df_lista_busqueda[filtro_dia]
                except:
                    pop_up = QMessageBox()
                    pop_up.setIcon(QMessageBox.Critical)
                    pop_up.setWindowTitle("Alerta")
                    pop_up.setText("El dia ingresado es incorrecto. Reingréselo.")
                    pop_up.exec_() 
                    self.lineEdit_BuscarNombre.setEnabled(True)
                    self.lineEdit_BuscarApellido.setEnabled(True)
                    self.lineEdit_BuscarID.setEnabled(True)
                    self.lineEdit_BuscarDia.setEnabled(True)
                    self.lineEdit_BuscarMes.setEnabled(True)
                    self.lineEdit_BuscarAo.setEnabled(True)
            
        if nombre!='':
            filtro_nombre = df_lista_busqueda['nombre'].str.contains(nombre) 
            df_lista_busqueda = df_lista_busqueda[filtro_nombre]
        
        if apellido!='':
            filtro_apellido = df_lista_busqueda['apellido'].str.contains(apellido) 
            df_lista_busqueda = df_lista_busqueda[filtro_apellido]

        if id!='':
            id = str(id)
            df_lista_busqueda = df_lista_busqueda[df_lista_busqueda.id == id]

        # Si no se encuentran resultados para la búsqueda
        if df_lista_busqueda.shape[0]==0:
            pop_up = QMessageBox()
            pop_up.setIcon(QMessageBox.Information)
            pop_up.setWindowTitle("Alerta")
            pop_up.setText("No se encontraron resultados para su búsqueda.")
            pop_up.exec_() 
            self.lineEdit_BuscarNombre.setEnabled(True)
            self.lineEdit_BuscarApellido.setEnabled(True)
            self.lineEdit_BuscarID.setEnabled(True)
            self.lineEdit_BuscarDia.setEnabled(True)
            self.lineEdit_BuscarMes.setEnabled(True)
            self.lineEdit_BuscarAo.setEnabled(True)
        # Lista los resultados para la búsqueda
        else:
            for index, row in df_lista_busqueda.iterrows():
                nombre = row['nombre']
                apellido = row['apellido']
                id = str(row['id'])
                subconjuntos_id = id.split(".")
                id = subconjuntos_id[0]
                fecha = str(row['fecha'])[:10]
                hora = str(row['hora'])[:8]
                self.listWidget_ListadoPacientes.addItem(nombre + "      " + apellido + "      " + id + "      " + fecha + "      " + hora)
                self.lineEdit_BuscarNombre.setEnabled(True)
                self.lineEdit_BuscarApellido.setEnabled(True)
                self.lineEdit_BuscarID.setEnabled(True)
                self.lineEdit_BuscarDia.setEnabled(True)
                self.lineEdit_BuscarMes.setEnabled(True)
                self.lineEdit_BuscarAo.setEnabled(True)

    # Función para seleccionar un registro
    def funcSeleccionarRegistro(self):
        registro_seleccionado = self.listWidget_ListadoPacientes.currentItem().text()
        subcadenas_registro = registro_seleccionado.split("      ")
        id = subcadenas_registro[2]
        fecha = subcadenas_registro[3]
        hora = subcadenas_registro[4]

        partes_hora = str(hora).split(":")
        hora_id = str(partes_hora[0])+"."+str(partes_hora[1])

        global id_global_busqueda
        id_global_busqueda = id+" "+str(fecha)+" "+hora_id

        self.pushButton_SeleccionarPaciente.setEnabled(True)
    
    # Función para hacer los gráficos del registro seleccionado
    def funcHacerGraficosRegistro(self):
        directorio_actual = os.path.abspath(os.path.dirname(__file__))
        nombre_archivo_ejecutar_GraficoSPI = 'GraficoSPI.py'
        path_archivo_ejecutar_GraficoSPI = os.path.join(directorio_actual, nombre_archivo_ejecutar_GraficoSPI)
        exec(open(path_archivo_ejecutar_GraficoSPI).read())


###########################################################################################################
    def retranslateUi(self, BusquedaPacientes):
        _translate = QtCore.QCoreApplication.translate
        BusquedaPacientes.setWindowTitle(_translate("BusquedaPacientes", "MainWindow"))
        self.groupBox_BusquedaPaciente.setTitle(_translate("BusquedaPacientes", "Búsqueda de Paciente"))
        self.pushButton_BuscarPaciente.setText(_translate("BusquedaPacientes", "Buscar"))
        self.pushButton_SeleccionarPaciente.setText(_translate("BusquedaPacientes", "Seleccionar"))
        self.lineEdit_BuscarMes.setPlaceholderText(_translate("BusquedaPacientes", "MM"))
        self.lineEdit_BuscarAo.setPlaceholderText(_translate("BusquedaPacientes", "AAAA"))
        self.label_Barra.setText(_translate("BusquedaPacientes", "/"))
        self.label_Barra_2.setText(_translate("BusquedaPacientes", "/"))
        self.label_BuscarFecha.setText(_translate("BusquedaPacientes", "Fecha: "))
        self.lineEdit_BuscarDia.setPlaceholderText(_translate("BusquedaPacientes", "DD"))
        self.label_BuscarID.setText(_translate("BusquedaPacientes", "ID: "))
        self.label_BuscarNombre.setText(_translate("BusquedaPacientes", "Nombre:"))
        self.label_BuscarApellido.setText(_translate("BusquedaPacientes", "Apellido:"))
        self.pushButton_VolverBusquedaPaciente.setText(_translate("BusquedaPacientes", "Volver al \n""Menú Principal"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BusquedaPacientes = QtWidgets.QMainWindow()
    ui = Ui_BusquedaPacientes()
    ui.setupUi(BusquedaPacientes)
    BusquedaPacientes.show()
    sys.exit(app.exec_())
