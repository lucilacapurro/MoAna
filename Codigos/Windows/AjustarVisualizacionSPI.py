from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

#############################################################################################################################

global ajustes_graf_SPI
ajustes_graf_SPI = 5

global index_actual 
index_actual = 0
#############################################################################################################################

class Ui_AjusteVisualizacionGraficaSPI(object):
    def setupUi(self, AjusteVisualizacionGraficaSPI):
        AjusteVisualizacionGraficaSPI.setObjectName("AjusteVisualizacionGraficaSPI")
        AjusteVisualizacionGraficaSPI.resize(532, 170)
    
        # Almaceno la instancia de la ventana para después poder cerrar la ventana al guardar la configuración
        self.ventana = AjusteVisualizacionGraficaSPI

        self.centralwidget = QtWidgets.QWidget(AjusteVisualizacionGraficaSPI)
        self.centralwidget.setObjectName("centralwidget")
        
        self.groupBox_AjusteVisualizacionSPI = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_AjusteVisualizacionSPI.setGeometry(QtCore.QRect(10, 10, 511, 141))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_AjusteVisualizacionSPI.setFont(font)
        self.groupBox_AjusteVisualizacionSPI.setAutoFillBackground(False)
        self.groupBox_AjusteVisualizacionSPI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_AjusteVisualizacionSPI.setObjectName("groupBox_AjusteVisualizacionSPI")
        
        self.label_VentanaTiempoSPI = QtWidgets.QLabel(self.groupBox_AjusteVisualizacionSPI)
        self.label_VentanaTiempoSPI.setGeometry(QtCore.QRect(12, 50, 140, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_VentanaTiempoSPI.setFont(font)
        self.label_VentanaTiempoSPI.setObjectName("label_VentanaTiempoSPI")
        
        # Combo Box de opciones de ventanas de tiempo disponibles para seleccionar
        self.comboBox_VentanaTiempoSPI = QtWidgets.QComboBox(self.groupBox_AjusteVisualizacionSPI)
        self.comboBox_VentanaTiempoSPI.setGeometry(QtCore.QRect(160, 50, 250, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_VentanaTiempoSPI.setFont(font)
        self.comboBox_VentanaTiempoSPI.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.comboBox_VentanaTiempoSPI.setObjectName("comboBox_VentanaTiempoSPI")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        self.comboBox_VentanaTiempoSPI.addItem("")
        # Hago que siempre inicie en la última opción que haya tenido
        self.comboBox_VentanaTiempoSPI.setCurrentIndex(index_actual)

        # Botón para Guardar Ajuste de visualizacion seleccionado
        self.pushButton_GuardarAjusteVisualizacionSPI = QtWidgets.QPushButton(self.groupBox_AjusteVisualizacionSPI)
        self.pushButton_GuardarAjusteVisualizacionSPI.setGeometry(QtCore.QRect(420, 100, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_GuardarAjusteVisualizacionSPI.setFont(font)
        self.pushButton_GuardarAjusteVisualizacionSPI.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_GuardarAjusteVisualizacionSPI.setObjectName("pushButton_GuardarAjusteVisualizacionSPI")
        self.pushButton_GuardarAjusteVisualizacionSPI.clicked.connect(self.funcChequearAjustesSPI)
        
        AjusteVisualizacionGraficaSPI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AjusteVisualizacionGraficaSPI)
        self.statusbar.setObjectName("statusbar")
        AjusteVisualizacionGraficaSPI.setStatusBar(self.statusbar)
        self.retranslateUi(AjusteVisualizacionGraficaSPI)
        QtCore.QMetaObject.connectSlotsByName(AjusteVisualizacionGraficaSPI)

##############################################################################################################################
#FUNCIONES
    # Función que trasforma las frases "x minutos u horas" a cantidad de minutos y ajusta el eje del gráfico
    def funcChequearAjustesSPI(self): 
        VentanaTiempoSPI = int(self.comboBox_VentanaTiempoSPI.currentText().split(" ")[0])
        global index_actual
        index_actual = self.comboBox_VentanaTiempoSPI.currentIndex()

        if VentanaTiempoSPI not in [5, 15, 30, 45]:
            VentanaTiempoSPI *= 60 # pasamos las horas a minutos 

        global ajustes_graf_SPI
        ajustes_graf_SPI = VentanaTiempoSPI 

        self.ventana.close()

#############################################################################################################################

    def retranslateUi(self, AjusteVisualizacionGraficaSPI):
        _translate = QtCore.QCoreApplication.translate
        AjusteVisualizacionGraficaSPI.setWindowTitle(_translate("AjusteVisualizacionGraficaSPI", "MainWindow"))
        self.groupBox_AjusteVisualizacionSPI.setTitle(_translate("AjusteVisualizacionGraficaSPI", "Ajuste visualización gráfica SPI"))
        self.pushButton_GuardarAjusteVisualizacionSPI.setText(_translate("AjusteVisualizacionGraficaSPI", "Guardar"))
        self.label_VentanaTiempoSPI.setText(_translate("AjusteVisualizacionGraficaSPI", "Ventana de tiempo*: ")) 
        self.comboBox_VentanaTiempoSPI.setItemText(0, _translate("AjusteVisualizacionGraficaSPI", "5 minutos"))
        self.comboBox_VentanaTiempoSPI.setItemText(1, _translate("AjusteVisualizacionGraficaSPI", "15 minutos"))
        self.comboBox_VentanaTiempoSPI.setItemText(2, _translate("AjusteVisualizacionGraficaSPI", "30 minutos"))
        self.comboBox_VentanaTiempoSPI.setItemText(3, _translate("AjusteVisualizacionGraficaSPI", "45 minutos"))
        self.comboBox_VentanaTiempoSPI.setItemText(4, _translate("AjusteVisualizacionGraficaSPI", "1 hora"))
        self.comboBox_VentanaTiempoSPI.setItemText(5, _translate("AjusteVisualizacionGraficaSPI", "2 horas"))
        self.comboBox_VentanaTiempoSPI.setItemText(6, _translate("AjusteVisualizacionGraficaSPI", "3 horas"))
        self.comboBox_VentanaTiempoSPI.setItemText(7, _translate("AjusteVisualizacionGraficaSPI", "4 horas"))
        self.comboBox_VentanaTiempoSPI.setItemText(8, _translate("AjusteVisualizacionGraficaSPI", "6 horas"))
        self.comboBox_VentanaTiempoSPI.setItemText(9, _translate("AjusteVisualizacionGraficaSPI", "8 horas"))
        self.comboBox_VentanaTiempoSPI.setItemText(10, _translate("AjusteVisualizacionGraficaSPI", "10 horas"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AjusteVisualizacionGraficaSPI = QtWidgets.QMainWindow()
    ui = Ui_AjusteVisualizacionGraficaSPI()
    ui.setupUi(AjusteVisualizacionGraficaSPI)
    AjusteVisualizacionGraficaSPI.show()
    sys.exit(app.exec_())
