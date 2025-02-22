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
        self.decoded = QLabel()

        self.button = QPushButton()
        self.button.setText("Расшифровать")

        self.button.clicked.connect(self.decrypt)

        layout.addWidget(l1)
        layout.
        layout.addWidget(self.message)
        layout.addWidget(l2)
        layout.addWidget(self.decoded)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def decrypt(self):
        print("decrypt")


class AtbashDecoderWindow(DecoderWindow):

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_BIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    N = 26

    def decrypt(self):
        text = self.message.text()
        decrypt_text = ""
        for i in text:
            if i in self.ALPHABET:
                ind = self.ALPHABET.index(i)

                decrypt_text += self.ALPHABET[self.N-(ind+1)]
            elif i in self.ALPHABET_BIG:
                ind = self.ALPHABET_BIG.index(i)
                decrypt_text += self.ALPHABET_BIG[self.N-(ind+1)]
            else:
                decrypt_text += i
            self.decoded.setText(decrypt_text)

