from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import os
import win32file
import win32api
import shutil

#########################################################################################################################

# Obtén la ruta absoluta del directorio actual
directorio_actual = os.path.abspath(os.path.dirname(__file__))

global id_seleccionado
id_seleccionado = ""

#########################################################################################################################

class Ui_DescargarInforme(object):

    # Función para volver a la ventana de opciones informe 
    def openOpcionesInforme(self):
        from OpcionesInforme import Ui_OpcionesInforme
        self.windowOpcionesInforme = QtWidgets.QMainWindow()
        self.ui = Ui_OpcionesInforme()
        self.ui.setupUi(self.windowOpcionesInforme)
        self.windowOpcionesInforme.showMaximized()

#########################################################################################################################

    def setupUi(self, DescargarInforme):
        DescargarInforme.setObjectName("DescargarInforme")
        DescargarInforme.resize(1360, 720)
        
        self.centralwidget = QtWidgets.QWidget(DescargarInforme)
        self.centralwidget.setObjectName("centralwidget")
        
        self.frame_DescargarInforme = QtWidgets.QFrame(self.centralwidget)
        self.frame_DescargarInforme.setGeometry(QtCore.QRect(0, 0, 1360, 720))
        self.frame_DescargarInforme.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.frame_DescargarInforme.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_DescargarInforme.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_DescargarInforme.setObjectName("frame_DescargarInforme")
        
        self.groupBox_DescargarInforme = QtWidgets.QGroupBox(self.frame_DescargarInforme)
        self.groupBox_DescargarInforme.setGeometry(QtCore.QRect(20, 20, 1150, 640))
        self.groupBox_DescargarInforme.setStyleSheet("background-color: rgb(255, 255, 255);\n""font: 14pt \"MS Shell Dlg 2\";")
        self.groupBox_DescargarInforme.setObjectName("groupBox_DescargarInforme")
        
        self.label_DescargarInforme = QtWidgets.QLabel(self.groupBox_DescargarInforme)
        self.label_DescargarInforme.setGeometry(QtCore.QRect(200, 100, 250, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_DescargarInforme.setFont(font)
        self.label_DescargarInforme.setObjectName("label_DescargarInforme")
        
        # Listado de memorias externas disponibles
        self.listWidget_DescargarInforme = QtWidgets.QListWidget(self.groupBox_DescargarInforme)
        self.listWidget_DescargarInforme.setGeometry(QtCore.QRect(200, 150, 750, 350))
        self.listWidget_DescargarInforme.setObjectName("listWidget_DescargarInforme")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.listWidget_DescargarInforme.setFont(font)
        self.listWidget_DescargarInforme.itemClicked.connect(self.funcPendriveSeleccionado)

        # Botón para descargar los archivos en la memoria externa seleccionada
        self.pushButton_Descargar_DescargarInforme = QtWidgets.QPushButton(self.groupBox_DescargarInforme)
        self.pushButton_Descargar_DescargarInforme.setGeometry(QtCore.QRect(830, 530, 120, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_Descargar_DescargarInforme.setFont(font)
        self.pushButton_Descargar_DescargarInforme.setStyleSheet("background-color: rgb(243, 243, 243);\n""font: 11pt \"MS Shell Dlg 2\";")
        self.pushButton_Descargar_DescargarInforme.setObjectName("pushButton_Descargar_DescargarInforme")
        self.pushButton_Descargar_DescargarInforme.setEnabled(False)
        self.pushButton_Descargar_DescargarInforme.clicked.connect(self.descargar_pdf_a_pendrive)
        self.pushButton_Descargar_DescargarInforme.clicked.connect(lambda: DescargarInforme.close())

        # Botón para volver a la ventana de opciones de informe 
        self.pushButton_Cancelar_DescargarInforme = QtWidgets.QPushButton(self.frame_DescargarInforme)
        self.pushButton_Cancelar_DescargarInforme.setGeometry(QtCore.QRect(1210, 620, 120, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_Cancelar_DescargarInforme.setFont(font)
        self.pushButton_Cancelar_DescargarInforme.setStyleSheet("background-color: rgb(243, 243, 243);\n""font: 11pt \"MS Shell Dlg 2\";")
        self.pushButton_Cancelar_DescargarInforme.setObjectName("pushButton_Cancelar_DescargarInforme")
        self.pushButton_Cancelar_DescargarInforme.clicked.connect(lambda: DescargarInforme.close())
        self.pushButton_Cancelar_DescargarInforme.clicked.connect(self.openOpcionesInforme)
        
        DescargarInforme.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DescargarInforme)
        self.statusbar.setObjectName("statusbar")
        DescargarInforme.setStatusBar(self.statusbar)

        self.retranslateUi(DescargarInforme)
        QtCore.QMetaObject.connectSlotsByName(DescargarInforme)

        # Llama a la función para detectar las memorias externas 
        self.detectar_pendrive_windows()

#####################################################################################################################
#FUNCIONES

    # Función para detectar las memorias externas y listarlas en la list widget
    def detectar_pendrive_windows(self):
        drive_list = []
        drive_types = win32api.GetLogicalDriveStrings()
        drives = drive_types.split('\000')[:-1]

        for drive in drives:
            drive_type = win32file.GetDriveType(drive)
            if drive_type == win32file.DRIVE_REMOVABLE:
                drive_info = win32api.GetVolumeInformation(drive)
                drive_name = drive_info[0]
                drive_list.append((drive_name, drive))

        # Agrego la lista de pendrives detectados a la list widget
        for pendrive in drive_list:
            self.listWidget_DescargarInforme.addItem(pendrive[0] + " - Ruta: " + pendrive[1])
        
        return drive_list


    # Función que habilita el botón de Descargar una vez seleccionada una memoria externa
    def funcPendriveSeleccionado(self):
        self.pushButton_Descargar_DescargarInforme.setEnabled(True)


    # Función para descargar los archivos (datos e informe) a la memoria externa una vez presionado el botón Descargar
    def descargar_pdf_a_pendrive(self):
        from InputDatosPaciente import id_global_principal
        from BusquedaPaciente import id_global_busqueda
        
        if id_global_principal != "":
            id_seleccionado = id_global_principal

        elif id_global_busqueda != "":
            id_seleccionado = id_global_busqueda

        pendrive = self.listWidget_DescargarInforme.currentItem().text()
        ruta_pendrive = pendrive.split("Ruta: ")[1] 

        #Busco en los directorios los archivos que quiero guardar en el pendrive
        nombre_pdf = 'Informe ' + id_seleccionado + '.pdf'
        nombre_csv = 'Datos '+ id_seleccionado + '.csv'
        ruta_archivo_pdf = os.path.join(directorio_actual, nombre_pdf)
        ruta_archivo_csv = os.path.join(directorio_actual, nombre_csv)

        shutil.copy2(ruta_archivo_pdf, ruta_pendrive)
        shutil.copy2(ruta_archivo_csv, ruta_pendrive)

        pop_up = QMessageBox()
        pop_up.setWindowTitle("Descarga Completada")
        pop_up.setText("El informe y los datos se ha descargado correctamente.")
        pop_up.setStandardButtons(QMessageBox.Ok)
        pop_up.exec_()

#####################################################################################################################

    def retranslateUi(self, DescargarInforme):
        _translate = QtCore.QCoreApplication.translate
        DescargarInforme.setWindowTitle(_translate("DescargarInforme", "MainWindow"))
        self.groupBox_DescargarInforme.setTitle(_translate("DescargarInforme", "Descargar Informe"))
        self.label_DescargarInforme.setText(_translate("DescargarInforme", "Puertos USB Disponibles:"))
        self.pushButton_Descargar_DescargarInforme.setText(_translate("DescargarInforme", "Descargar"))
        self.pushButton_Cancelar_DescargarInforme.setText(_translate("DescargarInforme", "Cancelar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DescargarInforme = QtWidgets.QMainWindow()
    ui = Ui_DescargarInforme()
    ui.setupUi(DescargarInforme)
    DescargarInforme.showMaximized()
    sys.exit(app.exec_())
