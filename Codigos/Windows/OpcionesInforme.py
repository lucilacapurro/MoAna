from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.QtWebEngineWidgets
import os 

from DescargarInforme import Ui_DescargarInforme
from GraficoSPI import SPIEstados, SPIFranjas, PorcentajesSPI

#############################################################################################

global id_seleccionado
id_seleccionado = ""

global ruta_relativa_informe
ruta_relativa_informe = ""

#############################################################################################

class Ui_OpcionesInforme(object):
    
    # Funciones para abrir otras ventanas: 

    # Abrir la ventana de descarga del informe
    def openDescargarInforme(self):
        self.windowDescargarInforme = QtWidgets.QMainWindow()
        self.ui = Ui_DescargarInforme()
        self.ui.setupUi(self.windowDescargarInforme)
        self.windowDescargarInforme.show()

    # Volver a la ventana de inicio
    def openInicio(self):
        from Inicio import Ui_MainWindow
        self.windowInicio = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.windowInicio)
        self.windowInicio.show()

    # Abrir la ventana de visualizaciones de gráficos
    def openVisualizacionWebGraficos(self):
        from VisualizacionWebGraficos import Ui_VisualizacionGraficos
        self.windowVisualizarWeb = QtWidgets.QMainWindow()
        self.ui = Ui_VisualizacionGraficos()
        self.ui.setupUi(self.windowVisualizarWeb)
        self.windowVisualizarWeb.show()

#############################################################################################

    def setupUi(self, OpcionesInforme):
        OpcionesInforme.setObjectName("OpcionesInforme")
        OpcionesInforme.resize(1360, 700)

        self.centralwidget = QtWidgets.QWidget(OpcionesInforme)
        self.centralwidget.setObjectName("centralwidget")
        
        self.groupBox_OpcionesInforme = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_OpcionesInforme.setGeometry(QtCore.QRect(0, 0, 1360, 700))
        self.groupBox_OpcionesInforme.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 14pt \"MS Shell Dlg 2\";")
        self.groupBox_OpcionesInforme.setObjectName("groupBox_OpcionesInforme")

        #self.frame = QtWidgets.QFrame(self.groupBox_OpcionesInforme)
        #self.frame.setGeometry(QtCore.QRect(10, 30, 1340, 640))
        #self.frame.setStyleSheet("background-color: rgb(226, 226, 226);")
        #self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame.setObjectName("frame")

        self.frame_OpcionesInforme = QtWidgets.QFrame(self.groupBox_OpcionesInforme)
        self.frame_OpcionesInforme.setGeometry(QtCore.QRect(10, 30, 1340, 560))
        self.frame_OpcionesInforme.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.frame_OpcionesInforme.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_OpcionesInforme.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_OpcionesInforme.setObjectName("frame_OpcionesInforme")

        # Botón para abrir la ventana de visualizaciones de gráficos
        self.pushButton_VisualizarSPI = QtWidgets.QPushButton(self.frame_OpcionesInforme)
        self.pushButton_VisualizarSPI.setGeometry(QtCore.QRect(270, 280, 200, 80))
        self.pushButton_VisualizarSPI.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";\n""background-color: rgb(132, 132, 132);\n""color: rgb(255, 255, 255);")
        self.pushButton_VisualizarSPI.setObjectName("pushButton_VisualizarSPI")
        self.pushButton_VisualizarSPI.clicked.connect(self.openVisualizacionWebGraficos)

        # Botón para abrir el informe
        self.pushButton_VisualizarInforme = QtWidgets.QPushButton(self.frame_OpcionesInforme)
        self.pushButton_VisualizarInforme.setGeometry(QtCore.QRect(570, 280, 200, 80))
        self.pushButton_VisualizarInforme.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";\n""background-color: rgb(132, 132, 132);\n""color: rgb(255, 255, 255);")
        self.pushButton_VisualizarInforme.setObjectName("pushButton_VisualizarInforme")
        self.pushButton_VisualizarInforme.clicked.connect(self.funcVisualizarInforme)

        # Botón para abrir la ventana de descarga de los archivos (datos e informe)
        self.pushButton_DescargarInforme_OpcionesInforme = QtWidgets.QPushButton(self.frame_OpcionesInforme)
        self.pushButton_DescargarInforme_OpcionesInforme.setGeometry(QtCore.QRect(870, 280, 200, 80))
        self.pushButton_DescargarInforme_OpcionesInforme.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";\n""background-color: rgb(132, 132, 132);\n""color: rgb(255, 255, 255);")
        self.pushButton_DescargarInforme_OpcionesInforme.setObjectName("pushButton_DescargarInforme_OpcionesInforme")
        self.pushButton_DescargarInforme_OpcionesInforme.clicked.connect(self.openDescargarInforme)

        # Botón para volver a la ventana de inicio
        self.pushButton_VolverOpcionesInforme = QtWidgets.QPushButton(self.groupBox_OpcionesInforme)
        self.pushButton_VolverOpcionesInforme.setGeometry(QtCore.QRect(1150, 610, 140, 50))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_VolverOpcionesInforme.setFont(font)
        self.pushButton_VolverOpcionesInforme.setStyleSheet("background-color: rgb(243, 243, 243);\n""font: 11pt \"MS Shell Dlg 2\";")
        self.pushButton_VolverOpcionesInforme.setObjectName("pushButton_VolverOpcionesInforme")
        self.pushButton_VolverOpcionesInforme.clicked.connect(lambda: OpcionesInforme.close())
        self.pushButton_VolverOpcionesInforme.clicked.connect(self.openInicio)

        OpcionesInforme.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(OpcionesInforme)
        self.statusbar.setObjectName("statusbar")
        OpcionesInforme.setStatusBar(self.statusbar)

        self.retranslateUi(OpcionesInforme)
        QtCore.QMetaObject.connectSlotsByName(OpcionesInforme)

###################################################################################################################
#FUNCIONES
    # Función para visualizar el informe 
    def funcVisualizarInforme(self):
        from InputDatosPaciente import id_global_principal
        from BusquedaPaciente import id_global_busqueda
        
        if id_global_principal != "":
            id_seleccionado = id_global_principal

        elif id_global_busqueda != "":
            id_seleccionado = id_global_busqueda

        # Obtén la ruta absoluta del directorio actual
        directorio_actual = os.path.abspath(os.path.dirname(__file__))

        # Construye la ruta relativa usando os.path.join()
        nombrepdf = 'Informe ' + id_seleccionado + '.pdf'
        
        global ruta_relativa_informe
        ruta_relativa_informe = os.path.join(directorio_actual, nombrepdf)

        pdf = os.startfile(ruta_relativa_informe)


###################################################################################################################

    def retranslateUi(self, OpcionesInforme):
        _translate = QtCore.QCoreApplication.translate
        OpcionesInforme.setWindowTitle(_translate("OpcionesInforme", "MainWindow"))
        self.groupBox_OpcionesInforme.setTitle(_translate("OpcionesInforme", "Opciones Informe"))
        self.pushButton_VisualizarSPI.setText(_translate("OpcionesInforme", "Visualizar \n"" Evolución del SPI"))
        self.pushButton_VisualizarInforme.setText(_translate("OpcionesInforme", "Visualizar \n"" Informe"))
        self.pushButton_DescargarInforme_OpcionesInforme.setText(_translate("OpcionesInforme", "Descargar \n"" Informe"))
        self.pushButton_VolverOpcionesInforme.setText(_translate("OpcionesInforme", "Volver al \n""Menú Principal"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpcionesInforme = QtWidgets.QMainWindow()
    ui = Ui_OpcionesInforme()
    ui.setupUi(OpcionesInforme)
    OpcionesInforme.show()
    sys.exit(app.exec_())
