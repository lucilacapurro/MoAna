from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import os
import pandas as pd
from TecladoVirtual import VirtualKeyboard  

global habilitar_teclado
habilitar_teclado = True


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


#########################################################################################################################
class Ui_Configuraciones(object):
    
    def openInicio(self):
        from Inicio import Ui_MainWindow
        self.windowInicio = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.windowInicio)
        self.windowInicio.show()

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit
    def openTecladoVirtual_Farmaco(self, target_edit):
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Farmaco) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(277, 325)
        self.pushButton_AgregarFarmaco.setEnabled(True)

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit
    def openTecladoVirtual_ProcQuirurgico(self, target_edit):
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_ProcQuirurgico) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(277, 425)
        self.pushButton_AgregarProcQuirurgico.setEnabled(True)
    
    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit
    def openTecladoVirtual_Intercurrencia(self, target_edit):
        self.virtual_keyboard = VirtualKeyboard(target_edit)
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Intercurrencia) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(277, 200)
        self.pushButton_AgregarIntercurrencia.setEnabled(True)

    #################################################################################################################################
    def setupUi(self, Configuraciones):
        Configuraciones.setObjectName("Configuraciones")
        Configuraciones.resize(1360, 700)

        self.centralwidget = QtWidgets.QWidget(Configuraciones)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(304, 134, 751, 431))
        self.frame.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.groupBox_Configuraciones = QtWidgets.QGroupBox(self.frame)
        self.groupBox_Configuraciones.setGeometry(QtCore.QRect(20, 10, 601, 411))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_Configuraciones.setFont(font)
        self.groupBox_Configuraciones.setAutoFillBackground(False)
        self.groupBox_Configuraciones.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_Configuraciones.setObjectName("groupBox_Configuraciones")

        self.pushButton_GuardarConfiguraciones = QtWidgets.QPushButton(self.groupBox_Configuraciones)
        self.pushButton_GuardarConfiguraciones.setGeometry(QtCore.QRect(510, 370, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_GuardarConfiguraciones.setFont(font)
        self.pushButton_GuardarConfiguraciones.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_GuardarConfiguraciones.setObjectName("pushButton_GuardarConfiguraciones")
        self.pushButton_GuardarConfiguraciones.clicked.connect(self.funcGuardarEventos)

        self.label_Configuraciones = QtWidgets.QLabel(self.groupBox_Configuraciones)
        self.label_Configuraciones.setGeometry(QtCore.QRect(170, 20, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_Configuraciones.setFont(font)
        self.label_Configuraciones.setObjectName("label_Configuraciones")

        self.label_Farmaco = QtWidgets.QLabel(self.groupBox_Configuraciones)
        self.label_Farmaco.setGeometry(QtCore.QRect(10, 70, 581, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Farmaco.setFont(font)
        self.label_Farmaco.setStyleSheet("background-color: rgb(132, 132, 132);\n""color: rgb(255, 255, 255);")
        self.label_Farmaco.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Farmaco.setObjectName("label_Farmaco")

        self.comboBoxFarmaco = QtWidgets.QComboBox(self.groupBox_Configuraciones)
        self.comboBoxFarmaco.setGeometry(QtCore.QRect(10, 110, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBoxFarmaco.setFont(font)
        self.comboBoxFarmaco.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.comboBoxFarmaco.setEditable(True)
        self.comboBoxFarmaco.setMaxVisibleItems(7)
        self.comboBoxFarmaco.setObjectName("comboBoxFarmaco")
        self.comboBoxFarmaco.addItems(farmacos)

        self.lineEdit_Farmaco = QtWidgets.QLineEdit(self.groupBox_Configuraciones)
        self.lineEdit_Farmaco.setGeometry(QtCore.QRect(180, 110, 341, 31))
        self.lineEdit_Farmaco.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_Farmaco.setText("")
        self.lineEdit_Farmaco.setFrame(False)
        self.lineEdit_Farmaco.setObjectName("lineEdit_Farmaco")

        self.pushButton_AgregarFarmaco = QtWidgets.QPushButton(self.groupBox_Configuraciones)
        self.pushButton_AgregarFarmaco.setGeometry(QtCore.QRect(530, 110, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_AgregarFarmaco.setFont(font)
        self.pushButton_AgregarFarmaco.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_AgregarFarmaco.setObjectName("pushButton_AgregarFarmaco")
        self.pushButton_AgregarFarmaco.setEnabled(False)
        self.pushButton_AgregarFarmaco.clicked.connect(self.funcAgregarFarmacos)

        self.lineEdit_ProcQuirurgico = QtWidgets.QLineEdit(self.groupBox_Configuraciones)
        self.lineEdit_ProcQuirurgico.setGeometry(QtCore.QRect(180, 210, 341, 31))
        self.lineEdit_ProcQuirurgico.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_ProcQuirurgico.setText("")
        self.lineEdit_ProcQuirurgico.setFrame(False)
        self.lineEdit_ProcQuirurgico.setObjectName("lineEdit_ProcQuirurgico")

        self.label_ProcQuirurgico = QtWidgets.QLabel(self.groupBox_Configuraciones)
        self.label_ProcQuirurgico.setGeometry(QtCore.QRect(10, 170, 581, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_ProcQuirurgico.setFont(font)
        self.label_ProcQuirurgico.setStyleSheet("background-color: rgb(132, 132, 132);\n""color: rgb(255, 255, 255);")
        self.label_ProcQuirurgico.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ProcQuirurgico.setObjectName("label_ProcQuirurgico")

        self.comboBox_ProcQuirurgico = QtWidgets.QComboBox(self.groupBox_Configuraciones)
        self.comboBox_ProcQuirurgico.setGeometry(QtCore.QRect(10, 210, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_ProcQuirurgico.setFont(font)
        self.comboBox_ProcQuirurgico.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.comboBox_ProcQuirurgico.setEditable(True)
        self.comboBox_ProcQuirurgico.setMaxVisibleItems(7)
        self.comboBox_ProcQuirurgico.setObjectName("comboBox_ProcQuirurgico")
        self.comboBox_ProcQuirurgico.addItems(procedimientos)

        self.pushButton_AgregarProcQuirurgico = QtWidgets.QPushButton(self.groupBox_Configuraciones)
        self.pushButton_AgregarProcQuirurgico.setGeometry(QtCore.QRect(530, 210, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_AgregarProcQuirurgico.setFont(font)
        self.pushButton_AgregarProcQuirurgico.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_AgregarProcQuirurgico.setObjectName("pushButton_AgregarProcQuirurgico")
        self.pushButton_AgregarProcQuirurgico.setEnabled(False)
        self.pushButton_AgregarProcQuirurgico.clicked.connect(self.funcAgregarProcQuirurgico)
        
        self.lineEdit_Intercurrencia = QtWidgets.QLineEdit(self.groupBox_Configuraciones)
        self.lineEdit_Intercurrencia.setGeometry(QtCore.QRect(180, 310, 341, 31))
        self.lineEdit_Intercurrencia.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_Intercurrencia.setText("")
        self.lineEdit_Intercurrencia.setFrame(False)
        self.lineEdit_Intercurrencia.setObjectName("lineEdit_Intercurrencia")

        self.label_Intercurrencia = QtWidgets.QLabel(self.groupBox_Configuraciones)
        self.label_Intercurrencia.setGeometry(QtCore.QRect(10, 270, 581, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Intercurrencia.setFont(font)
        self.label_Intercurrencia.setStyleSheet("background-color: rgb(132, 132, 132);\n""color: rgb(255, 255, 255);")
        self.label_Intercurrencia.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Intercurrencia.setObjectName("label_Intercurrencia")

        self.comboBox_Intercurrencia = QtWidgets.QComboBox(self.groupBox_Configuraciones)
        self.comboBox_Intercurrencia.setGeometry(QtCore.QRect(10, 310, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_Intercurrencia.setFont(font)
        self.comboBox_Intercurrencia.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.comboBox_Intercurrencia.setEditable(True)
        self.comboBox_Intercurrencia.setMaxVisibleItems(7)
        self.comboBox_Intercurrencia.setObjectName("comboBox_Intercurrencia")
        self.comboBox_Intercurrencia.addItems(intercurrencias)

        self.pushButton_AgregarIntercurrencia = QtWidgets.QPushButton(self.groupBox_Configuraciones)
        self.pushButton_AgregarIntercurrencia.setGeometry(QtCore.QRect(530, 310, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_AgregarIntercurrencia.setFont(font)
        self.pushButton_AgregarIntercurrencia.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_AgregarIntercurrencia.setObjectName("pushButton_AgregarIntercurrencia")
        self.pushButton_AgregarIntercurrencia.setEnabled(False)
        self.pushButton_AgregarIntercurrencia.clicked.connect(self.funcAgregarIntercurrencia)

        self.lineEdit_Farmaco.raise_()
        self.label_Configuraciones.raise_()
        self.label_Farmaco.raise_()
        self.pushButton_GuardarConfiguraciones.raise_()
        self.pushButton_AgregarFarmaco.raise_()
        self.lineEdit_ProcQuirurgico.raise_()
        self.label_ProcQuirurgico.raise_()
        self.comboBox_ProcQuirurgico.raise_()
        self.pushButton_AgregarProcQuirurgico.raise_()
        self.lineEdit_Intercurrencia.raise_()
        self.label_Intercurrencia.raise_()
        self.comboBox_Intercurrencia.raise_()
        self.pushButton_AgregarIntercurrencia.raise_()
        self.comboBoxFarmaco.raise_()

        # Conecta la señal selectionChanged del QLineEdit para abrir el teclado virtual
        self.lineEdit_Farmaco.selectionChanged.connect(self.funcAbrirTecladoFarmaco)
        self.lineEdit_ProcQuirurgico.selectionChanged.connect(self.funcAbrirTecladoProcQuirurgico)
        self.lineEdit_Intercurrencia.selectionChanged.connect(self.funcAbrirTecladoIntercurrencia)

        self.pushButton_VolverConfiguraciones = QtWidgets.QPushButton(self.frame)
        self.pushButton_VolverConfiguraciones.setGeometry(QtCore.QRect(630, 380, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_VolverConfiguraciones.setFont(font)
        self.pushButton_VolverConfiguraciones.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_VolverConfiguraciones.setObjectName("pushButton_VolverConfiguraciones")
        self.pushButton_VolverConfiguraciones.clicked.connect(lambda: Configuraciones.close())
        self.pushButton_VolverConfiguraciones.clicked.connect(self.openInicio)

        Configuraciones.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Configuraciones)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 21))
        self.menubar.setObjectName("menubar")
        Configuraciones.setMenuBar(self.menubar)

        self.retranslateUi(Configuraciones)
        self.comboBox_ProcQuirurgico.setCurrentIndex(0)
        self.comboBox_Intercurrencia.setCurrentIndex(0)
        self.comboBoxFarmaco.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Configuraciones)

    #############################################################################################################################
    #FUNCIONES: 
    def funcAbrirTecladoFarmaco(self):
        global habilitar_teclado
        if habilitar_teclado == True:
            # Conecta la señal selectionChanged del QLineEdit para abrir el teclado virtual
            self.openTecladoVirtual_Farmaco(self.lineEdit_Farmaco)
        
    def funcAbrirTecladoProcQuirurgico(self):
        global habilitar_teclado
        if habilitar_teclado == True:
            # Conecta la señal selectionChanged del QLineEdit para abrir el teclado virtual
            self.openTecladoVirtual_ProcQuirurgico(self.lineEdit_ProcQuirurgico)

    def funcAbrirTecladoIntercurrencia(self):
        global habilitar_teclado
        if habilitar_teclado == True:
            # Conecta la señal selectionChanged del QLineEdit para abrir el teclado virtual
            self.openTecladoVirtual_Intercurrencia(self.lineEdit_Intercurrencia)

    # Funciones para actualizar los QLineEdit con el texto ingresado desde el teclado virtual
    def update_line_edit_Farmaco(self, char):
        current_text = self.lineEdit_Farmaco.text()  
        self.lineEdit_Farmaco.setText(current_text + char)
    
    def update_line_edit_ProcQuirurgico(self, char):
        current_text = self.lineEdit_ProcQuirurgico.text()  
        self.lineEdit_ProcQuirurgico.setText(current_text + char)

    def update_line_edit_Intercurrencia(self, char):
        current_text = self.lineEdit_Intercurrencia.text()  
        self.lineEdit_Intercurrencia.setText(current_text + char)

    def funcAgregarFarmacos(self):
        self.comboBoxFarmaco.addItem(self.lineEdit_Farmaco.text())
        global farmacos
        farmacos.append(self.lineEdit_Farmaco.text())
        global habilitar_teclado
        habilitar_teclado = False
        self.lineEdit_Farmaco.clear()
        habilitar_teclado = True

    def funcAgregarProcQuirurgico(self):
        self.comboBox_ProcQuirurgico.addItem(self.lineEdit_ProcQuirurgico.text())
        global procedimientos
        procedimientos.append(self.lineEdit_ProcQuirurgico.text())
        global habilitar_teclado
        habilitar_teclado = False
        self.lineEdit_ProcQuirurgico.clear()
        habilitar_teclado = True

    def funcAgregarIntercurrencia(self):
        self.comboBox_Intercurrencia.addItem(self.lineEdit_Intercurrencia.text())
        global intercurrencias
        intercurrencias.append(self.lineEdit_Intercurrencia.text())
        global habilitar_teclado
        habilitar_teclado = False
        self.lineEdit_Intercurrencia.clear()
        habilitar_teclado = True

    def funcGuardarEventos(self):
        global farmacos, procedimientos, intercurrencias
        farmacos.sort()
        procedimientos.sort()
        intercurrencias.sort()

        max_length = max(len(farmacos), len(procedimientos), len(intercurrencias))
        farmacos += [None] * (max_length - len(farmacos))
        procedimientos += [None] * (max_length - len(procedimientos))
        intercurrencias += [None] * (max_length - len(intercurrencias))

        # Redefino el df con los eventos ingresados
        df_lista_eventos = pd.DataFrame({'farmacos': farmacos, 'procedimientos': procedimientos, 'intercurrencias': intercurrencias})

        # Guarda el DataFrame modificado de nuevo en el archivo Excel
        df_lista_eventos.to_excel(path_excel_eventos, index=False)

        pop_up = QMessageBox()
        pop_up.setIcon(QMessageBox.Information)
        pop_up.setWindowTitle("Eventos configurados correctamente")
        pop_up.setText("Los eventos han sido configurados correctamente.")
        pop_up.exec_()       

    #############################################################################################################################
    def retranslateUi(self, Configuraciones):
        _translate = QtCore.QCoreApplication.translate
        Configuraciones.setWindowTitle(_translate("Configuraciones", "MainWindow"))
        self.groupBox_Configuraciones.setTitle(_translate("Configuraciones", "Configuraciones"))
        self.pushButton_GuardarConfiguraciones.setText(_translate("Configuraciones", "Guardar"))
        self.lineEdit_Farmaco.setPlaceholderText(_translate("Configuraciones", "Ingrese un nuevo fármaco analgésico"))
        self.label_Configuraciones.setText(_translate("Configuraciones", "Personalización de eventos"))
        self.label_Farmaco.setText(_translate("Configuraciones", "Fármaco analgésicos"))
        self.pushButton_AgregarFarmaco.setText(_translate("Configuraciones", "Agregar"))
        self.lineEdit_ProcQuirurgico.setPlaceholderText(_translate("Configuraciones", "Ingrese un nuevo procedimiento quirúrgico"))
        self.label_ProcQuirurgico.setText(_translate("Configuraciones", "Procedimientos quirúrgicos"))
        self.pushButton_AgregarProcQuirurgico.setText(_translate("Configuraciones", "Agregar"))
        self.lineEdit_Intercurrencia.setPlaceholderText(_translate("Configuraciones", "Ingrese una nueva intercurrencia"))
        self.label_Intercurrencia.setText(_translate("Configuraciones", "Intercurrencias"))
        self.pushButton_AgregarIntercurrencia.setText(_translate("Configuraciones", "Agregar"))
        self.pushButton_VolverConfiguraciones.setText(_translate("Configuraciones", "Volver al \n""Menú Principal"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Configuraciones = QtWidgets.QMainWindow()
    ui = Ui_Configuraciones()
    ui.setupUi(Configuraciones)
    Configuraciones.show()
    sys.exit(app.exec_())
