from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import os

##############################################################################################

global listaDatosPaciente
listaDatosPaciente = []

global fecha
fecha = ''

global hora 
hora = ''

global nombre_archivo_datos
nombre_archivo_datos = ''

global path_archivo_datos
path_archivo_datos = ''

global id_global_principal
id_global_principal = ''

##############################################################################################

class Ui_InputDatosPaciente(object):

    #Funciones para abrir otras ventanas:

    # Abrir la ventana del monitoreo una vez ingresados los datos
    def openPrincipal(self):
        from Principal import Ui_DisplayPrincipal
        self.windowPrincipal = QtWidgets.QMainWindow()
        self.ui = Ui_DisplayPrincipal()
        self.ui.setupUi(self.windowPrincipal)
        self.windowPrincipal.show()

    # Volver a la ventana de inicio
    def openInicio(self):
        from Inicio import Ui_MainWindow
        self.windowInicio = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.windowInicio)
        self.windowInicio.show()


    # Funciones para abrir los teclados:

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit Nombre
    def openTecladoVirtual_Nombre(self, target_edit):
        from TecladoVirtual import VirtualKeyboard 
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Nombre) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(277, 345)

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit Apellido
    def openTecladoVirtual_Apellido(self, target_edit):
        from TecladoVirtual import VirtualKeyboard 
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Apellido) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(277, 397)
    
    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit ID
    def openTecladoVirtual_ID(self, target_edit):
        from TecladoVirtual import VirtualKeyboard 
        self.virtual_keyboard = VirtualKeyboard(target_edit)  
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_ID) 
        self.virtual_keyboard.show()
        self.virtual_keyboard.move(277, 445)

##############################################################################################

    def setupUi(self, InputDatosPaciente):
        InputDatosPaciente.setObjectName("InputDatosPaciente")
        InputDatosPaciente.resize(1360, 800)
 
        self.centralwidget = QtWidgets.QWidget(InputDatosPaciente)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1360, 800))
        self.frame.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Botón para volver a la ventana de inicio
        self.pushButton_VolverInputDatosPaciente = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_VolverInputDatosPaciente.setGeometry(QtCore.QRect(1200, 620, 140, 50))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_VolverInputDatosPaciente.setFont(font)
        self.pushButton_VolverInputDatosPaciente.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_VolverInputDatosPaciente.setObjectName("pushButton_VolverInputDatosPaciente")
        self.pushButton_VolverInputDatosPaciente.clicked.connect(lambda: InputDatosPaciente.close())
        self.pushButton_VolverInputDatosPaciente.clicked.connect(self.openInicio)

        self.groupBox_InputDatosPaciente = QtWidgets.QGroupBox(self.frame)
        self.groupBox_InputDatosPaciente.setGeometry(QtCore.QRect(20, 20, 1320, 580))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_InputDatosPaciente.setFont(font)
        self.groupBox_InputDatosPaciente.setAutoFillBackground(False)
        self.groupBox_InputDatosPaciente.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_InputDatosPaciente.setObjectName("groupBox_InputDatosPaciente")

        # Botón para guardar los datos una vez ingresados todos los campos (obligatorios)
        self.pushButton_GuardarInputDatosPaciente = QtWidgets.QPushButton(self.groupBox_InputDatosPaciente)
        self.pushButton_GuardarInputDatosPaciente.setGeometry(QtCore.QRect(700, 450, 140, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_GuardarInputDatosPaciente.setFont(font)
        self.pushButton_GuardarInputDatosPaciente.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_GuardarInputDatosPaciente.setObjectName("pushButton_GuardarInputDatosPaciente")
        self.pushButton_GuardarInputDatosPaciente.clicked.connect(self.funcInputIDyNombre)

        # Botón para iniciar el monitoreo una vez guardados los datos
        self.pushButton_IniciarInputDatosPaciente = QtWidgets.QPushButton(self.groupBox_InputDatosPaciente)
        self.pushButton_IniciarInputDatosPaciente.setGeometry(QtCore.QRect(860, 450, 140, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_IniciarInputDatosPaciente.setFont(font)
        self.pushButton_IniciarInputDatosPaciente.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_IniciarInputDatosPaciente.setObjectName("pushButton_IniciarInputDatosPaciente")
        self.pushButton_IniciarInputDatosPaciente.clicked.connect(self.funcInicioMonitoreo)
        self.pushButton_IniciarInputDatosPaciente.clicked.connect(self.openPrincipal)
        self.pushButton_IniciarInputDatosPaciente.clicked.connect(lambda: InputDatosPaciente.close())
        self.pushButton_IniciarInputDatosPaciente.setEnabled(False)     

        # Sección de ingreso de datos 

        #Nombre
        self.label_Nombre = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_Nombre.setGeometry(QtCore.QRect(300, 160, 71, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_Nombre.setFont(font)
        self.label_Nombre.setObjectName("label_Nombre")

        self.lineEdit_Nombre = QtWidgets.QLineEdit(self.groupBox_InputDatosPaciente)
        self.lineEdit_Nombre.setGeometry(QtCore.QRect(400, 160, 600, 40))
        self.lineEdit_Nombre.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_Nombre.setText("")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Nombre.setFont(font)
        self.lineEdit_Nombre.setFrame(False)
        self.lineEdit_Nombre.setObjectName("lineEdit_Nombre")

        # Apellido
        self.label_Apellido = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_Apellido.setGeometry(QtCore.QRect(300, 250, 90, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_Apellido.setFont(font)
        self.label_Apellido.setObjectName("label_Apellido")

        self.lineEdit_Apellido = QtWidgets.QLineEdit(self.groupBox_InputDatosPaciente)
        self.lineEdit_Apellido.setGeometry(QtCore.QRect(400, 250, 600, 40))
        self.lineEdit_Apellido.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_Apellido.setText("")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Apellido.setFont(font)
        self.lineEdit_Apellido.setFrame(False)
        self.lineEdit_Apellido.setObjectName("lineEdit_Apellido")

        # ID
        self.label_ID = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_ID.setGeometry(QtCore.QRect(300, 340, 30, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_ID.setFont(font)
        self.label_ID.setObjectName("label_ID")

        self.lineEdit_ID = QtWidgets.QLineEdit(self.groupBox_InputDatosPaciente)
        self.lineEdit_ID.setGeometry(QtCore.QRect(400, 340, 600, 40))
        self.lineEdit_ID.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_ID.setText("")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_ID.setFont(font)
        self.lineEdit_ID.setFrame(False)
        self.lineEdit_ID.setObjectName("lineEdit_ID")
  

        # Señal de aviso que los tres campos (nombre, apellido y ID) son obligatorios para poder guardar e iniciar el monitoreo
        self.label_Obligatorio = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_Obligatorio.setGeometry(QtCore.QRect(1180, 12, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_Obligatorio.setFont(font)
        self.label_Obligatorio.setObjectName("label_Obligatorio")

        # Conecta la señal selectionChanged del QLineEdit para abrir el teclado virtual
        self.lineEdit_Nombre.selectionChanged.connect(lambda: self.openTecladoVirtual_Nombre(self.lineEdit_Nombre))
        self.lineEdit_Apellido.selectionChanged.connect(lambda: self.openTecladoVirtual_Apellido(self.lineEdit_Apellido))
        self.lineEdit_ID.selectionChanged.connect(lambda: self.openTecladoVirtual_ID(self.lineEdit_ID))

        self.label_Obligatorio.raise_()
        self.lineEdit_Nombre.raise_()
        self.label_Nombre.raise_()
        self.lineEdit_Apellido.raise_()
        self.label_Apellido.raise_()
        self.lineEdit_ID.raise_()
        self.label_ID.raise_()
        self.pushButton_GuardarInputDatosPaciente.raise_()
        self.frame.raise_()
        self.pushButton_VolverInputDatosPaciente.raise_()

        InputDatosPaciente.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(InputDatosPaciente)
        self.statusbar.setObjectName("statusbar")
        InputDatosPaciente.setStatusBar(self.statusbar)
        self.retranslateUi(InputDatosPaciente)
        QtCore.QMetaObject.connectSlotsByName(InputDatosPaciente)


###############################################################################################################################
#FUNCIONES
    # Función para chequear que se ingresen los tres campos obligatorios al querer guardar los datos del paciente
    def funcInputIDyNombre(self):
        # Se inhabilita la edición de los campos 
        self.lineEdit_Nombre.setEnabled(False)
        self.lineEdit_Apellido.setEnabled(False)
        self.lineEdit_ID.setEnabled(False)

        # Se verifica que se hayan ingresado correctamente los tres campos: nombre, apellido, ID 
        nombre = self.lineEdit_Nombre.text()
        apellido = self.lineEdit_Apellido.text()
        ID = self.lineEdit_ID.text()
        # En caso de no haber ingresado alguno de los campos, se muestran los mensajes de error correspondientes y se vuelven a habilitar los campos de edición 
        if nombre == "" or apellido == "" or ID == "":
            if nombre == "":
                pop_up = QMessageBox()
                pop_up.setIcon(QMessageBox.Critical)
                pop_up.setWindowTitle("Alerta")
                pop_up.setText("Es necesario ingresar el nombre del paciente.")
                pop_up.exec_()
                self.lineEdit_Nombre.setEnabled(True)
                self.lineEdit_Apellido.setEnabled(True)
                self.lineEdit_ID.setEnabled(True)
            if apellido == "":
                pop_up = QMessageBox()
                pop_up.setIcon(QMessageBox.Critical)
                pop_up.setWindowTitle("Alerta")
                pop_up.setText("Es necesario ingresar el apellido del paciente.")
                pop_up.exec_()
                self.lineEdit_Nombre.setEnabled(True)
                self.lineEdit_Apellido.setEnabled(True)
                self.lineEdit_ID.setEnabled(True)
            if ID == "":
                pop_up = QMessageBox()
                pop_up.setIcon(QMessageBox.Critical)
                pop_up.setWindowTitle("Alerta")
                pop_up.setText("Es necesario ingresar el ID del paciente.")
                pop_up.exec_()
                self.lineEdit_Nombre.setEnabled(True)
                self.lineEdit_Apellido.setEnabled(True)
                self.lineEdit_ID.setEnabled(True)
        # En caso de que los tres campos estén ingresados, se guardan los datos del paciente 
        else:
            self.funcGuardarDatosPaciente()

    # Función para guardar los datos del paciente una vez completados y habilitar el botón de iniciar el monitoreo
    def funcGuardarDatosPaciente(self):
        nombre = self.lineEdit_Nombre.text()
        apellido = self.lineEdit_Apellido.text()
        ID = self.lineEdit_ID.text()
        
        #Creo una lista con todos los datos del paciente
        global listaDatosPaciente
        listaDatosPaciente = [nombre, apellido, ID]

        pop_up = QMessageBox()
        pop_up.setIcon(QMessageBox.Information)
        pop_up.setWindowTitle("Datos guardados correctamente")
        pop_up.setText("Los datos del paciente han sido guardados correctamente. Ya puede iniciar el monitoreo")
        pop_up.exec_()              

        # Deshabilita el botón de guardar los datos y habilita el botón de iniciar el monitoreo
        self.pushButton_IniciarInputDatosPaciente.setEnabled(True)
        self.pushButton_GuardarInputDatosPaciente.setEnabled(False)     


    def funcInicioMonitoreo(self):
        # Creamos el id global
        # Para levantar fecha y hora
        import datetime
        global fecha
        fecha = datetime.date.today()
        global hora
        hora = datetime.datetime.now().time()
        partes_hora = str(hora).split(":")
        hora_id = str(partes_hora[0])+"."+str(partes_hora[1])
        # Para adquirir ID y nombre
        id = listaDatosPaciente[2]

        global id_global_principal
        id_global_principal = id+" "+str(fecha)+" "+hora_id

        global nombre_archivo_datos
        nombre_archivo_datos =  'Datos ' + id_global_principal + '.csv'

        directorio_actual = os.path.abspath(os.path.dirname(__file__))
        global path_archivo_datos
        path_archivo_datos =  os.path.join(directorio_actual, nombre_archivo_datos)


    # Funciones para actualizar los QLineEdit con el texto ingresado desde el teclado virtual
    def update_line_edit_Nombre(self, char):
        current_text = self.lineEdit_Nombre.text()  
        self.lineEdit_Nombre.setText(current_text + char)
    
    def update_line_edit_Apellido(self, char):
        current_text = self.lineEdit_Apellido.text()  
        self.lineEdit_Apellido.setText(current_text + char)

    def update_line_edit_ID(self, char):
        current_text = self.lineEdit_ID.text()  
        self.lineEdit_ID.setText(current_text + char)
    

###############################################################################################################################

    def retranslateUi(self, InputDatosPaciente):
        _translate = QtCore.QCoreApplication.translate
        InputDatosPaciente.setWindowTitle(_translate("InputDatosPaciente", "MainWindow"))
        self.label_Obligatorio.setText(_translate("InputDatosPaciente", "* Campos obligatorios")) 
        self.pushButton_VolverInputDatosPaciente.setText(_translate("InputDatosPaciente", "Volver al \n""Menú Principal"))
        self.groupBox_InputDatosPaciente.setTitle(_translate("InputDatosPaciente", "Ingreso Datos Paciente"))
        self.pushButton_IniciarInputDatosPaciente.setText(_translate("InputDatosPaciente", "Iniciar Monitoreo"))
        self.pushButton_GuardarInputDatosPaciente.setText(_translate("InputDatosPaciente", "Guardar"))
        self.label_Nombre.setText(_translate("InputDatosPaciente", "Nombre*:"))
        self.label_Apellido.setText(_translate("InputDatosPaciente", "Apellido*:"))
        self.label_ID.setText(_translate("InputDatosPaciente", "ID*:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InputDatosPaciente = QtWidgets.QMainWindow()
    ui = Ui_InputDatosPaciente()
    ui.setupUi(InputDatosPaciente)
    InputDatosPaciente.showMaximized()
    sys.exit(app.exec_())
