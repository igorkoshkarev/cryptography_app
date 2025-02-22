# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtWidgets import (
QComboBox,
QVBoxLayout,
QWidget,
QPushButton,
QLabel,
QLineEdit,
QSpinBox)

class DecoderWindow(QWidget):

    LABELS = []
    KEYS = []

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

        self.keyLabels = []

        for i in range(len(self.KEYS)):
            l = QLabel()
            l.setText(self.LABELS[i])
            layout.addWidget(l)
            self.keyLabels.append(self.KEYS[i]())
            layout.addWidget(self.keyLabels[i])

        layout.addWidget(l1)
        layout.addWidget(self.message)
        layout.addWidget(l2)
        layout.addWidget(self.decoded)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def decrypt(self):
        pass


class AtbashDecoderWindow(DecoderWindow):

    LABELS = []
    KEYS = []
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


class CaesarDecoderWindow(DecoderWindow):

    KEYS = [QSpinBox]
    LABELS = ['Ключ: ']
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_BIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    N = 26

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)
        self.keyLabels[0].setMaximum(self.N)


    def decrypt(self):
        text = self.message.text()
        decrypt_text = ""
        key = self.keyLabels[0].value()
        for i in text:
            if i in self.ALPHABET:
                ind = self.ALPHABET.index(i)
                decrypt_text += self.ALPHABET[(ind-key) % self.N]
            elif i in self.ALPHABET_BIG:
                ind = self.ALPHABET_BIG.index(i)
                decrypt_text += self.ALPHABET_BIG[(ind-key) % self.N]
            else:
                decrypt_text += i
        self.decoded.setText(decrypt_text)

