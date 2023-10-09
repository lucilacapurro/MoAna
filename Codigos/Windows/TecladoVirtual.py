import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class VirtualKeyboard(QWidget):
    textEntered = pyqtSignal(str)  # Señal personalizada para enviar el texto ingresado

    def __init__(self, target_edit):
        super().__init__()

        self.target_edit = target_edit

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Teclado')
        self.setGeometry(200, 200, 900, 200)

        layout = QVBoxLayout()

        # Crea los botones del teclado
        buttons_layout = QVBoxLayout()
        rows = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],  # Nueva fila de números
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

        # Agrega el botón de espacio
        btn_space = QPushButton('Espacio')
        btn_space.clicked.connect(lambda checked, ch=' ': self.on_button_click(ch))
        buttons_layout.addWidget(btn_space)

        # Agrega el botón de borrar el último elemento
        btn_backspace = QPushButton('Borrar')
        btn_backspace.clicked.connect(self.on_backspace_click)
        buttons_layout.addWidget(btn_backspace)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def on_button_click(self, char):
        self.textEntered.emit(char)

    def on_backspace_click(self):
        current_text = self.target_edit.text()
        self.target_edit.setText(current_text[:-1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VirtualKeyboard(None)  # Target_edit se define en el código de main.py
    window.show()
    sys.exit(app.exec_())