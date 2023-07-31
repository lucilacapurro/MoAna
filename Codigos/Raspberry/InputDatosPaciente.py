from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import os


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

class Ui_InputDatosPaciente(object):
    #############################################################################################
    #Funciones para abrir otras ventanas
    def openPrincipal(self):
        from Principal import Ui_DisplayPrincipal
        self.windowPrincipal = QtWidgets.QMainWindow()
        self.ui = Ui_DisplayPrincipal()
        self.ui.setupUi(self.windowPrincipal)
        self.windowPrincipal.showMaximized()

    def openInicio(self):
        from Inicio import Ui_MainWindow
        self.windowInicio = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.windowInicio)
        self.windowInicio.showMaximized()

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit
    def openTecladoVirtual_Nombre(self, target_edit):
        from TecladoVirtual import VirtualKeyboard  # Importa el módulo VirtualKeyboard
        self.virtual_keyboard = VirtualKeyboard(target_edit)  # Pasa el QLineEdit como argumento
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Nombre)  # Conecta la señal al slot de la MainWindow
        self.virtual_keyboard.show()
        # Establecer la posición de la nueva ventana en la pantalla
        self.virtual_keyboard.move(277, 345)

    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit
    def openTecladoVirtual_Apellido(self, target_edit):
        from TecladoVirtual import VirtualKeyboard  # Importa el módulo VirtualKeyboard
        self.virtual_keyboard = VirtualKeyboard(target_edit)  # Pasa el QLineEdit como argumento
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_Apellido)  # Conecta la señal al slot de la MainWindow
        self.virtual_keyboard.show()
        # Establecer la posición de la nueva ventana en la pantalla
        self.virtual_keyboard.move(277, 397)
    
    # Función para abrir el teclado virtual y conectar la señal textEntered al QLineEdit
    def openTecladoVirtual_ID(self, target_edit):
        from TecladoVirtual import VirtualKeyboard  # Importa el módulo VirtualKeyboard
        self.virtual_keyboard = VirtualKeyboard(target_edit)  # Pasa el QLineEdit como argumento
        self.virtual_keyboard.textEntered.connect(self.update_line_edit_ID)  # Conecta la señal al slot de la MainWindow
        self.virtual_keyboard.show()
        # Establecer la posición de la nueva ventana en la pantalla
        self.virtual_keyboard.move(277, 445)

    ############################################################################################

    def setupUi(self, InputDatosPaciente):
        InputDatosPaciente.setObjectName("InputDatosPaciente")
        #InputDatosPaciente.resize(774, 471)
        InputDatosPaciente.resize(1360, 700)
 
        self.centralwidget = QtWidgets.QWidget(InputDatosPaciente)
        self.centralwidget.setObjectName("centralwidget")
        
        self.pushButton_VolverInputDatosPaciente = QtWidgets.QPushButton(self.centralwidget)
        #self.pushButton_VolverInputDatosPaciente.setGeometry(QtCore.QRect(640, 390, 111, 41))
        self.pushButton_VolverInputDatosPaciente.setGeometry(QtCore.QRect(935, 513, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_VolverInputDatosPaciente.setFont(font)
        self.pushButton_VolverInputDatosPaciente.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_VolverInputDatosPaciente.setObjectName("pushButton_VolverInputDatosPaciente")
        self.pushButton_VolverInputDatosPaciente.clicked.connect(lambda: InputDatosPaciente.close())
        self.pushButton_VolverInputDatosPaciente.clicked.connect(self.openInicio)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(304, 134, 752, 432))
        self.frame.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.groupBox_InputDatosPaciente = QtWidgets.QGroupBox(self.frame)
        self.groupBox_InputDatosPaciente.setGeometry(QtCore.QRect(70, 50, 611, 301))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_InputDatosPaciente.setFont(font)
        self.groupBox_InputDatosPaciente.setAutoFillBackground(False)
        self.groupBox_InputDatosPaciente.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_InputDatosPaciente.setObjectName("groupBox_InputDatosPaciente")
        
        self.pushButton_IniciarInputDatosPaciente = QtWidgets.QPushButton(self.groupBox_InputDatosPaciente)
        self.pushButton_IniciarInputDatosPaciente.setGeometry(QtCore.QRect(470, 250, 120, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_IniciarInputDatosPaciente.setFont(font)
        self.pushButton_IniciarInputDatosPaciente.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_IniciarInputDatosPaciente.setObjectName("pushButton_IniciarInputDatosPaciente")
        self.pushButton_IniciarInputDatosPaciente.clicked.connect(self.funcInicioMonitoreo)
        self.pushButton_IniciarInputDatosPaciente.clicked.connect(self.openPrincipal)
        self.pushButton_IniciarInputDatosPaciente.clicked.connect(lambda: InputDatosPaciente.close())
        self.pushButton_IniciarInputDatosPaciente.setEnabled(False)     

        self.pushButton_GuardarInputDatosPaciente = QtWidgets.QPushButton(self.groupBox_InputDatosPaciente)
        self.pushButton_GuardarInputDatosPaciente.setGeometry(QtCore.QRect(380, 250, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_GuardarInputDatosPaciente.setFont(font)
        self.pushButton_GuardarInputDatosPaciente.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_GuardarInputDatosPaciente.setObjectName("pushButton_GuardarInputDatosPaciente")
        self.pushButton_GuardarInputDatosPaciente.clicked.connect(self.funcInputIDyNombre)
        
        self.label_Nombre = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_Nombre.setGeometry(QtCore.QRect(21, 90, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Nombre.setFont(font)
        self.label_Nombre.setObjectName("label_Nombre")

        self.lineEdit_Nombre = QtWidgets.QLineEdit(self.groupBox_InputDatosPaciente)
        self.lineEdit_Nombre.setGeometry(QtCore.QRect(91, 90, 492, 31))
        self.lineEdit_Nombre.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_Nombre.setText("")
        self.lineEdit_Nombre.setFrame(False)
        self.lineEdit_Nombre.setObjectName("lineEdit_Nombre")

        self.label_Apellido = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_Apellido.setGeometry(QtCore.QRect(21, 140, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Apellido.setFont(font)
        self.label_Apellido.setObjectName("label_Apellido")

        self.lineEdit_Apellido = QtWidgets.QLineEdit(self.groupBox_InputDatosPaciente)
        self.lineEdit_Apellido.setGeometry(QtCore.QRect(91, 140, 492, 31))
        self.lineEdit_Apellido.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_Apellido.setText("")
        self.lineEdit_Apellido.setFrame(False)
        self.lineEdit_Apellido.setObjectName("lineEdit_Apellido")

        self.label_ID = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_ID.setGeometry(QtCore.QRect(20, 190, 30, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_ID.setFont(font)
        self.label_ID.setObjectName("label_ID")

        self.lineEdit_ID = QtWidgets.QLineEdit(self.groupBox_InputDatosPaciente)
        self.lineEdit_ID.setGeometry(QtCore.QRect(60, 190, 523, 31))
        self.lineEdit_ID.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.lineEdit_ID.setFrame(False)
        self.lineEdit_ID.setObjectName("lineEdit_ID")
  
        self.label_Obligatorio = QtWidgets.QLabel(self.groupBox_InputDatosPaciente)
        self.label_Obligatorio.setGeometry(QtCore.QRect(483, 12, 110, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
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
    # HAGO FUNCION PARA CHEQUEAR QUE PONGAN ID y NOMBRE
    def funcInputIDyNombre(self): # se debe llamar a esta funcion cuando se quieren guardar los datos del paciente
        self.lineEdit_Nombre.setEnabled(False)
        self.lineEdit_Apellido.setEnabled(False)
        self.lineEdit_ID.setEnabled(False)

        nombre = self.lineEdit_Nombre.text()
        apellido = self.lineEdit_Apellido.text()
        ID = self.lineEdit_ID.text()
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
        else:
            self.funcGuardarDatosPaciente()


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
        current_text = self.lineEdit_Nombre.text()  # El sender es el QLineEdit que emitió la señal
        self.lineEdit_Nombre.setText(current_text + char)
    
    def update_line_edit_Apellido(self, char):
        current_text = self.lineEdit_Apellido.text()  # El sender es el QLineEdit que emitió la señal
        self.lineEdit_Apellido.setText(current_text + char)

    def update_line_edit_ID(self, char):
        current_text = self.lineEdit_ID.text()  # El sender es el QLineEdit que emitió la señal
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
    InputDatosPaciente.show()
    sys.exit(app.exec_())
