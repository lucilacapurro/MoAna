from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

global ajustes_graf_SPI
ajustes_graf_SPI = 5

class Ui_AjusteVisualizacionGraficaSPI(object):
    def setupUi(self, AjusteVisualizacionGraficaSPI):
        AjusteVisualizacionGraficaSPI.setObjectName("AjusteVisualizacionGraficaSPI")
        AjusteVisualizacionGraficaSPI.resize(532, 170)
        
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
        
        self.label_VentanaTiempoSPI = QtWidgets.QLabel(self.groupBox_AjusteVisualizacionSPI)
        self.label_VentanaTiempoSPI.setGeometry(QtCore.QRect(12, 50, 140, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_VentanaTiempoSPI.setFont(font)
        self.label_VentanaTiempoSPI.setObjectName("label_VentanaTiempoSPI")
        
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

        self.label_Obligatorio = QtWidgets.QLabel(self.groupBox_AjusteVisualizacionSPI)
        self.label_Obligatorio.setGeometry(QtCore.QRect(395, 12, 110, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_Obligatorio.setFont(font)
        self.label_Obligatorio.setObjectName("label_Obligatorio")
        self.label_Obligatorio.raise_()

        AjusteVisualizacionGraficaSPI.setCentralWidget(self.centralwidget)
        
        self.statusbar = QtWidgets.QStatusBar(AjusteVisualizacionGraficaSPI)
        self.statusbar.setObjectName("statusbar")
        
        AjusteVisualizacionGraficaSPI.setStatusBar(self.statusbar)

        self.retranslateUi(AjusteVisualizacionGraficaSPI)
        QtCore.QMetaObject.connectSlotsByName(AjusteVisualizacionGraficaSPI)

##############################################################################################################################
#FUNCIONES
    def funcChequearAjustesSPI(self): 
        VentanaTiempoSPI = int(self.comboBox_VentanaTiempoSPI.currentText().split(" ")[0])

        if VentanaTiempoSPI not in [5, 15, 30, 45]:
            VentanaTiempoSPI *= 60 # pasamos las horas a minutos 

        print(VentanaTiempoSPI)
        global ajustes_graf_SPI
        ajustes_graf_SPI = VentanaTiempoSPI 

        pop_up = QMessageBox()
        pop_up.setIcon(QMessageBox.Information)
        pop_up.setWindowTitle("Ajustes configurados")
        pop_up.setText("Los ajustes del gráfico de SPI fueron configurados correctamente. Puede cerrar la ventana de configuración.")
        pop_up.setStandardButtons(QMessageBox.Ok)
        pop_up.move(600, 600)
        pop_up.exec_()

#############################################################################################################################

    def retranslateUi(self, AjusteVisualizacionGraficaSPI):
        _translate = QtCore.QCoreApplication.translate
        AjusteVisualizacionGraficaSPI.setWindowTitle(_translate("AjusteVisualizacionGraficaSPI", "MainWindow"))
        self.groupBox_AjusteVisualizacionSPI.setTitle(_translate("AjusteVisualizacionGraficaSPI", "Ajuste visualización gráfica SPI"))
        self.pushButton_GuardarAjusteVisualizacionSPI.setText(_translate("AjusteVisualizacionGraficaSPI", "Guardar"))
        self.label_Obligatorio.setText(_translate("AjusteVisualizacionGraficaSPI", "* Campos obligatorios"))
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
    
     # Center the window on the screen
    screen_rect = app.desktop().availableGeometry(AjusteVisualizacionGraficaSPI)
    window_rect = AjusteVisualizacionGraficaSPI.frameGeometry()
    center_x = (screen_rect.width() - window_rect.width()) // 2
    center_y = (screen_rect.height() - window_rect.height()) // 2
    AjusteVisualizacionGraficaSPI.move(center_x, center_y)
    
    AjusteVisualizacionGraficaSPI.show()
    sys.exit(app.exec_())
