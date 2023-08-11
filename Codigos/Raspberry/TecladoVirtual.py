import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import pyqtSignal

########################################################################################################
class VirtualKeyboard(QWidget):
    # Señal personalizada para enviar el texto ingresado
    textEntered = pyqtSignal(str) 

    # Define el target edit que lo llama 
    def __init__(self, target_edit):
        super().__init__()
        self.target_edit = target_edit
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Teclado')
        # Centra la ventana en la pantalla
        center_x = 515 
        center_y = 450
        window_width = 400
        window_height = 200
        self.setGeometry(center_x, center_y, window_width, window_height)
        layout = QVBoxLayout()

        # Crea los botones del teclado
        buttons_layout = QVBoxLayout()
        rows = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]

        for row in rows:
            row_layout = QHBoxLayout()
            for char in row:
                button = QPushButton(char)
                button.clicked.connect(lambda checked, ch=char: self.on_button_click(ch))
                row_layout.addWidget(button)
            buttons_layout.addLayout(row_layout)

        # Botón de espacio
        btn_space = QPushButton('Espacio')
        btn_space.clicked.connect(lambda checked, ch=' ': self.on_button_click(ch))
        buttons_layout.addWidget(btn_space)

        # Botón de borrar para el último elemento
        btn_backspace = QPushButton('Borrar')
        btn_backspace.clicked.connect(self.on_backspace_click)
        buttons_layout.addWidget(btn_backspace)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    # Emite el char al clickear
    def on_button_click(self, char):
        self.textEntered.emit(char)

    # Escribe el texto en el line Edit que corresponde 
    def on_backspace_click(self):
        current_text = self.target_edit.text()
        self.target_edit.setText(current_text[:-1])

########################################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VirtualKeyboard(None)
    window.show()
    sys.exit(app.exec_())
