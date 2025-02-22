# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
QComboBox,
QVBoxLayout,
QWidget,
QPushButton,
QLabel,
QLineEdit)


class EncoderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Шифр")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        l1 = QLabel()
        l1.setText("Введите ссобщение: ")

        self.message = QLineEdit()
        l2 = QLabel()
        l2.setText("Зашифрованное сообщение: ")
        self.encoded = QLabel()

        self.button = QPushButton()
        self.button.setText("Зашифровать")

        self.button.clicked.connect(self.encrypt)

        layout.addWidget(l1)
        layout.addWidget(self.message)
        layout.addWidget(l2)
        layout.addWidget(self.encoded)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def encrypt(self):
        print('Encrypt')



class AtbashEncoderWindow(EncoderWindow):

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_BIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    N = 26

    def encrypt(self):
        text = self.message.text()
        encrypt_text = ""
        for i in text:
            if i in self.ALPHABET:
                ind = self.ALPHABET.index(i)
                encrypt_text += self.ALPHABET[self.N-(ind+1)]
            elif i in self.ALPHABET_BIG:
                ind = self.ALPHABET_BIG.index(i)
                encrypt_text += self.ALPHABET_BIG[self.N-(ind+1)]
            else:
                encrypt_text += i
        self.encoded.setText(encrypt_text)

