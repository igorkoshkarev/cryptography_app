# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtWidgets import (
QComboBox,
QVBoxLayout,
QWidget,
QPushButton,
QLabel,
QLineEdit)

class DecoderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Расшифровка")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        l1 = QLabel()
        l1.setText("Введите шифротекст: ")

        self.message = QLineEdit()

        l2 = QLabel()
        l2.setText("Расшифрованное сообщение: ")
        self.encoded = QLabel()

        self.button = QPushButton()
        self.button.setText("Расшифровать")

        layout.addWidget(l1)
        layout.addWidget(self.message)
        layout.addWidget(l2)
        layout.addWidget(self.encoded)
        layout.addWidget(self.button)

        self.setLayout(layout)
