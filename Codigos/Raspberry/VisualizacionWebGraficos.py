from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.graph_objs as go
import os
from GraficoSPI import SPIEstados, SPIFranjas, PorcentajesSPI

####################################################################################################################################

global directorio_actual
directorio_actual = os.path.abspath(os.path.dirname(__file__))

####################################################################################################################################

class Ui_VisualizacionGraficos(object):
    def setupUi(self, VisualizacionGraficos):
        VisualizacionGraficos.setObjectName("VisualizacionGraficos")
        VisualizacionGraficos.resize(1360, 700)

        self.centralwidget = QtWidgets.QWidget(VisualizacionGraficos)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 81, 1340, 609))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Botón para acceder al gráfico con las referencias de las franjas de interpretación del índice
        self.pushButton_GraficarSPIFranjas = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_GraficarSPIFranjas.setGeometry(QtCore.QRect(378, 10, 121, 61))
        self.pushButton_GraficarSPIFranjas.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n" "background-color: rgb(132, 132, 132);\n" "color: rgb(255, 255, 255);")
        self.pushButton_GraficarSPIFranjas.setObjectName("pushButton_GraficarSPIFranjas")
        self.pushButton_GraficarSPIFranjas.clicked.connect(self.funcGraficarFranjasSPI)

        # Botón para acceder al gráfico por estados
        self.pushButton_GraficarSPIEstados = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_GraficarSPIEstados.setGeometry(QtCore.QRect(620, 10, 121, 61))
        self.pushButton_GraficarSPIEstados.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n" "background-color: rgb(132, 132, 132);\n" "color: rgb(255, 255, 255);")
        self.pushButton_GraficarSPIEstados.setObjectName("pushButton_GraficarSPIEstados")
        self.pushButton_GraficarSPIEstados.clicked.connect(self.funcGraficarEstadosSPI)

        # Botón para acceder al gráfico de los porcentajes por franjas por estados 
        self.pushButton_GraficarSPIPorcentajes = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_GraficarSPIPorcentajes.setGeometry(QtCore.QRect(862, 10, 121, 61))
        self.pushButton_GraficarSPIPorcentajes.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n" "background-color: rgb(132, 132, 132);\n" "color: rgb(255, 255, 255);")
        self.pushButton_GraficarSPIPorcentajes.setObjectName("pushButton_GraficarSPIPorcentajes")
        self.pushButton_GraficarSPIPorcentajes.clicked.connect(self.funcGraficarPorcentajesSPI)

        # Crea el QWebEngineView dentro del contenedor
        self.webView = QtWebEngineWidgets.QWebEngineView(self.verticalLayoutWidget)
        self.webView.setGeometry(QtCore.QRect(10, 10, 521, 281))

        self.verticalLayout.addWidget(self.webView)
        VisualizacionGraficos.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(VisualizacionGraficos)
        self.statusbar.setObjectName("statusbar")
        VisualizacionGraficos.setStatusBar(self.statusbar)

        self.retranslateUi(VisualizacionGraficos)
        QtCore.QMetaObject.connectSlotsByName(VisualizacionGraficos)

####################################################################################################################################
# FUNCIONES: 
    # Función para hacer el gráfico por estados 
    def funcGraficarEstadosSPI(self):
        # Convertir el objeto SPIEstados a contenido HTML
        html_nombre = "SPIEstados.html"
        path_relativo = os.path.join(directorio_actual, html_nombre)
        html_content = SPIEstados.write_html(path_relativo)
        self.webView.load(QtCore.QUrl().fromLocalFile(path_relativo))

    # Función para hacer el gráfico por franjas
    def funcGraficarFranjasSPI(self):
        # Convertir el objeto SPIFranjas a contenido HTML
        html_nombre = "SPIFranjas.html"
        path_relativo = os.path.join(directorio_actual, html_nombre)
        html_content = SPIFranjas.write_html(path_relativo)
        self.webView.load(QtCore.QUrl().fromLocalFile(path_relativo))

    # Función para hacer el gráfico de porcentajes
    def funcGraficarPorcentajesSPI(self):
        # Convertir el objeto SPIProcentajes a contenido HTML
        html_nombre = "SPIPorcentajes.html"
        path_relativo = os.path.join(directorio_actual, html_nombre)
        html_content = PorcentajesSPI.write_html(path_relativo)
        self.webView.load(QtCore.QUrl().fromLocalFile(path_relativo))

####################################################################################################################################
  
    def retranslateUi(self, VisualizacionGraficos):
        _translate = QtCore.QCoreApplication.translate
        VisualizacionGraficos.setWindowTitle(_translate("VisualizacionGraficos", "MainWindow"))
        self.pushButton_GraficarSPIFranjas.setText(_translate("VisualizacionGraficos", "Evolución SPI "))
        self.pushButton_GraficarSPIEstados.setText(_translate("VisualizacionGraficos", "Evolución SPI \n"" por Estado "))
        self.pushButton_GraficarSPIPorcentajes.setText(_translate("VisualizacionGraficos", "Porcentajes SPI \n"" por Estado "))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VisualizacionGraficos = QtWidgets.QMainWindow()
    ui = Ui_VisualizacionGraficos()
    ui.setupUi(VisualizacionGraficos)
    VisualizacionGraficos.show()
    sys.exit(app.exec_())
