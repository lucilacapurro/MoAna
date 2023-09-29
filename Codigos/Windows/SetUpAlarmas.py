from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSpinBox
from PyQt5.QtGui import QPixmap

global alarmas
alarmas = [50, 20, 15] #seteamos los valores default de las alarmas

class Ui_SetUpAlarmas(object):
    def setupUi(self, SetUpAlarmas):
        SetUpAlarmas.setObjectName("SetUpAlarmas")
        SetUpAlarmas.resize(632, 274)
        
        self.centralwidget = QtWidgets.QWidget(SetUpAlarmas)
        self.centralwidget.setObjectName("centralwidget")
        
        self.groupBox_SetUpAlarmas = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_SetUpAlarmas.setGeometry(QtCore.QRect(10, 10, 611, 231))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox_SetUpAlarmas.setFont(font)
        self.groupBox_SetUpAlarmas.setAutoFillBackground(False)
        self.groupBox_SetUpAlarmas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_SetUpAlarmas.setObjectName("groupBox_SetUpAlarmas") 
        
        self.label_LimiteMaximo = QtWidgets.QLabel(self.groupBox_SetUpAlarmas)
        self.label_LimiteMaximo.setGeometry(QtCore.QRect(11, 40, 31, 31))
        self.label_LimiteMaximo.setObjectName("label_AlarmaTecnicaReconocida")
        self.imagen_LimiteMaximo = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\LimiteMaximo.png")
        self.imagen_LimiteMaximo = self.imagen_LimiteMaximo.scaled(self.label_LimiteMaximo.size(), QtCore.Qt.KeepAspectRatio)
        self.label_LimiteMaximo.setPixmap(self.imagen_LimiteMaximo)

        self.label_MaxSPI = QtWidgets.QLabel(self.groupBox_SetUpAlarmas)
        self.label_MaxSPI.setGeometry(QtCore.QRect(51, 40, 95, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_MaxSPI.setFont(font)
        self.label_MaxSPI.setObjectName("label_MaxSPI")
        
        self.spinBox_MaxSPI = QSpinBox(self.groupBox_SetUpAlarmas)
        self.spinBox_MaxSPI.setGeometry(QtCore.QRect(154, 40, 446, 31))
        self.spinBox_MaxSPI.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.spinBox_MaxSPI.setObjectName("spinBox_MaxSPI")
        self.spinBox_MaxSPI.setMinimum(0)
        self.spinBox_MaxSPI.setMaximum(100)
        self.spinBox_MaxSPI.setValue(alarmas[0])
        self.spinBox_MaxSPI.setSingleStep(5)
        font = self.spinBox_MaxSPI.font()
        font.setPointSize(11)
        self.spinBox_MaxSPI.setFont(font)
    
        self.label_LimiteMinimo = QtWidgets.QLabel(self.groupBox_SetUpAlarmas)
        self.label_LimiteMinimo.setGeometry(QtCore.QRect(11, 90, 31, 31))
        self.label_LimiteMinimo.setObjectName("label_AlarmaTecnicaReconocida")
        self.imagen_LimiteMinimo = QPixmap(r"C:\Users\Zakie Assad\Proyecto Final\Git\MoAna\Codigos\Windows\LimiteMinimo.png")
        self.imagen_LimiteMinimo = self.imagen_LimiteMinimo.scaled(self.label_LimiteMinimo.size(), QtCore.Qt.KeepAspectRatio)
        self.label_LimiteMinimo.setPixmap(self.imagen_LimiteMinimo)

        self.label_MinSPI = QtWidgets.QLabel(self.groupBox_SetUpAlarmas)
        self.label_MinSPI.setGeometry(QtCore.QRect(51, 90, 90, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_MinSPI.setFont(font)
        self.label_MinSPI.setObjectName("label_MinSPI")
        
        self.spinBox_MinSPI = QSpinBox(self.groupBox_SetUpAlarmas)
        self.spinBox_MinSPI.setGeometry(QtCore.QRect(154, 88, 446, 31))
        self.spinBox_MinSPI.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.spinBox_MinSPI.setObjectName("spinBox_MinSPI")
        self.spinBox_MinSPI.setMinimum(0)
        self.spinBox_MinSPI.setMaximum(100)
        self.spinBox_MinSPI.setValue(alarmas[1])
        self.spinBox_MinSPI.setSingleStep(5)
        font = self.spinBox_MinSPI.font()
        font.setPointSize(11)
        self.spinBox_MinSPI.setFont(font)
        
        self.label_TiempoPermanencia = QtWidgets.QLabel(self.groupBox_SetUpAlarmas)
        self.label_TiempoPermanencia.setGeometry(QtCore.QRect(11, 137, 170, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_TiempoPermanencia.setFont(font)
        self.label_TiempoPermanencia.setObjectName("label_TiempoPermanencia")
        
        self.comboBox_TiempoPermanencia = QtWidgets.QComboBox(self.groupBox_SetUpAlarmas)
        self.comboBox_TiempoPermanencia.setGeometry(QtCore.QRect(193, 140, 407, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_TiempoPermanencia.setFont(font)
        self.comboBox_TiempoPermanencia.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.comboBox_TiempoPermanencia.setObjectName("comboBox_TiempoPermanencia")
        self.comboBox_TiempoPermanencia.addItem("")
        self.comboBox_TiempoPermanencia.addItem("")
        self.comboBox_TiempoPermanencia.addItem("")
        self.comboBox_TiempoPermanencia.addItem("")
        self.comboBox_TiempoPermanencia.addItem("")
        
        self.pushButton_GuardarAlarmas = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_GuardarAlarmas.setGeometry(QtCore.QRect(530, 200, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_GuardarAlarmas.setFont(font)
        self.pushButton_GuardarAlarmas.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.pushButton_GuardarAlarmas.setObjectName("pushButton_GuardarAlarmas")
        self.pushButton_GuardarAlarmas.clicked.connect(self.funcChequearAlarmas)

        self.label_Obligatorio = QtWidgets.QLabel(self.groupBox_SetUpAlarmas)
        self.label_Obligatorio.setGeometry(QtCore.QRect(493, 12, 110, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_Obligatorio.setFont(font)
        self.label_Obligatorio.setObjectName("label_Obligatorio")
        self.label_Obligatorio.raise_()

        SetUpAlarmas.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SetUpAlarmas)
        self.statusbar.setObjectName("statusbar")
        SetUpAlarmas.setStatusBar(self.statusbar)

        self.retranslateUi(SetUpAlarmas)
        QtCore.QMetaObject.connectSlotsByName(SetUpAlarmas)

##############################################################################################################################
#FUNCIONES
    def funcChequearAlarmas(self): # VERIFICAR LOS CHEQUEOS EN CASO DE PERSONALIZAR LAS OPCIONES DE TIEMPO DE PERMANENCIA
        SPIMax = int(self.spinBox_MaxSPI.value())
        SPIMin = int(self.spinBox_MinSPI.value())

        if SPIMin > SPIMax:
            pop_up = QMessageBox()
            pop_up.setIcon(QMessageBox.Critical)
            pop_up.setWindowTitle("Alerta")
            pop_up.setText("El valor 'Mínimo SPI' ingresado es mayor al valor 'Máximo SPI' ingresado. Reingréselos.")
            pop_up.move(350, 420)
            pop_up.exec_()

        else:
            TiempoPermanencia = int(self.comboBox_TiempoPermanencia.currentText().split(" ")[0])
            if TiempoPermanencia < 4: # solo 15 o 30 son segundos y 1, 2 o 3 son minutos 
                TiempoPermanencia = TiempoPermanencia * 60
            global alarmas 
            alarmas = [SPIMax, SPIMin, TiempoPermanencia]

            pop_up = QMessageBox()
            pop_up.setIcon(QMessageBox.Information)
            pop_up.setWindowTitle("Alarma configurada")
            pop_up.setText("La alarma fue configurada correctamente. Puede cerrar la ventana de configuración.")
            pop_up.setStandardButtons(QMessageBox.Ok)
            pop_up.move(350, 420)
            pop_up.exec_()

#############################################################################################################################

    def retranslateUi(self, SetUpAlarmas):
        _translate = QtCore.QCoreApplication.translate
        SetUpAlarmas.setWindowTitle(_translate("SetUpAlarmas", "MainWindow"))
        self.groupBox_SetUpAlarmas.setTitle(_translate("SetUpAlarmas", "Set Up Alarmas Auditivas"))
        self.label_Obligatorio.setText(_translate("SetUpAlarmas", "* Campos obligatorios")) 
        self.label_MaxSPI.setText(_translate("SetUpAlarmas", "Máximo SPI*:                "))
        self.label_MinSPI.setText(_translate("SetUpAlarmas", "Mínimo SPI*:                  "))
        self.label_TiempoPermanencia.setText(_translate("SetUpAlarmas", "Tiempo de permanencia*:"))
        self.comboBox_TiempoPermanencia.setItemText(0, _translate("SetUpAlarmas", "15 segundos"))
        self.comboBox_TiempoPermanencia.setItemText(1, _translate("SetUpAlarmas", "30 segundos"))
        self.comboBox_TiempoPermanencia.setItemText(2, _translate("SetUpAlarmas", "1 minuto"))
        self.comboBox_TiempoPermanencia.setItemText(3, _translate("SetUpAlarmas", "2 minutos"))
        self.comboBox_TiempoPermanencia.setItemText(4, _translate("SetUpAlarmas", "3 minutos"))
        self.pushButton_GuardarAlarmas.setText(_translate("SetUpAlarmas", "Guardar"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SetUpAlarmas = QtWidgets.QMainWindow()
    ui = Ui_SetUpAlarmas()
    ui.setupUi(SetUpAlarmas)
    SetUpAlarmas.show()
    sys.exit(app.exec_())
