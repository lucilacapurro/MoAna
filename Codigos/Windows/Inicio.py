from PyQt5 import QtCore, QtWidgets
import PyQt5.QtWebEngineWidgets

##############################################################################################

class Ui_MainWindow(object):

    # Funciones para abrir otras ventanas:
    
    # Función para abrir la ventana de ingreso de datos del paciente
    def openInputDatosPaciente(self):
        from InputDatosPaciente import Ui_InputDatosPaciente
        self.windowInputDatosPaciente = QtWidgets.QMainWindow()
        self.ui = Ui_InputDatosPaciente()
        self.ui.setupUi(self.windowInputDatosPaciente)
        self.windowInputDatosPaciente.show()

    # Función para abrir la ventana de búsqueda de registros previos
    def openBusquedaPaciente(self):
        from BusquedaPaciente import Ui_BusquedaPacientes
        self.windowBusquedaPaciente = QtWidgets.QMainWindow()
        self.ui = Ui_BusquedaPacientes()
        self.ui.setupUi(self.windowBusquedaPaciente)
        self.windowBusquedaPaciente.show()

    # Función para abrir la ventana de personalización de eventos
    def openConfiguraciones(self):
        from Configuraciones import Ui_Configuraciones
        self.windowConfiguraciones = QtWidgets.QMainWindow()
        self.ui = Ui_Configuraciones()
        self.ui.setupUi(self.windowConfiguraciones)
        self.windowConfiguraciones.show()

##############################################################################################

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1360, 700)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #self.frame2 = QtWidgets.QFrame(self.centralwidget)
        #self.frame2.setGeometry(QtCore.QRect(389, 169, 592, 362))
        #self.frame2.setStyleSheet("background-color: rgb(226, 226, 226);")
        #self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame2.setObjectName("frame2")
        #self.frame2.raise_()
          
        self.groupBox_Inicio = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Inicio.setGeometry(QtCore.QRect(0, 0, 1360, 700))
        self.groupBox_Inicio.setStyleSheet("background-color: rgb(255, 255, 255);\n" "font: 14pt \"MS Shell Dlg 2\";")
        self.groupBox_Inicio.setObjectName("groupBox_Inicio")
        
        self.frame = QtWidgets.QFrame(self.groupBox_Inicio)
        self.frame.setGeometry(QtCore.QRect(10, 30, 1340, 640))
        self.frame.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Botón para iniciar un nuevo monitoreo y abrir la ventana de ingreso de datos del paciente
        self.pushButton_IniciarNuevoMonitoreo = QtWidgets.QPushButton(self.frame)
        self.pushButton_IniciarNuevoMonitoreo.setGeometry(QtCore.QRect(270, 280, 200, 80))
        self.pushButton_IniciarNuevoMonitoreo.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n" "background-color: rgb(132, 132, 132);\n" "color: rgb(255, 255, 255);")
        self.pushButton_IniciarNuevoMonitoreo.setObjectName("pushButton_IniciarNuevoMonitoreo")
        self.pushButton_IniciarNuevoMonitoreo.clicked.connect(self.openInputDatosPaciente)
        self.pushButton_IniciarNuevoMonitoreo.clicked.connect(lambda: MainWindow.close())

        # Botón para abrir la ventana de historial de pacientes
        self.pushButton_HistorialDePacientes = QtWidgets.QPushButton(self.frame)
        self.pushButton_HistorialDePacientes.setGeometry(QtCore.QRect(570, 280, 200, 80))
        self.pushButton_HistorialDePacientes.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n" "background-color: rgb(132, 132, 132);\n" "color: rgb(255, 255, 255);")
        self.pushButton_HistorialDePacientes.setObjectName("pushButton_HistorialDePacientes")
        self.pushButton_HistorialDePacientes.clicked.connect(self.openBusquedaPaciente)
        self.pushButton_HistorialDePacientes.clicked.connect(lambda: MainWindow.close())

        # Botón para abrir la ventana de personalización de eventos
        self.pushButton_Configuraciones = QtWidgets.QPushButton(self.frame)
        self.pushButton_Configuraciones.setGeometry(QtCore.QRect(870, 280, 200, 80))
        self.pushButton_Configuraciones.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n" "background-color: rgb(132, 132, 132);\n" "color: rgb(255, 255, 255);")
        self.pushButton_Configuraciones.setObjectName("pushButton_Configuraciones")
        self.pushButton_Configuraciones.clicked.connect(self.openConfiguraciones)
        self.pushButton_Configuraciones.clicked.connect(lambda: MainWindow.close())

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

##############################################################################################

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_Inicio.setTitle(_translate("MainWindow", "Inicio"))
        self.pushButton_IniciarNuevoMonitoreo.setText(_translate("MainWindow", "Iniciar nuevo \n"" monitoreo "))
        self.pushButton_HistorialDePacientes.setText(_translate("MainWindow", "Historial de \n"" pacientes "))
        self.pushButton_Configuraciones.setText(_translate("MainWindow", "Configuraciones"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
