# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6.QtWidgets import (
QComboBox,
QVBoxLayout,
QWidget,
QPushButton,
QLabel,
QLineEdit,
QSpinBox,
QErrorMessage)
import re

class DecoderWindow(QWidget):

    LABELS = []
    KEYS = []
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_BIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    RUSS_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    RUSS_ALPHABET_BIG = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    N = 26
    N_RUSS = 33

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
        self.decoded = QLineEdit()
        self.decoded.setReadOnly(True)

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
            elif i in self.RUSS_ALPHABET:
                ind = self.RUSS_ALPHABET.index(i)
                decrypt_text += self.RUSS_ALPHABET[self.N_RUSS-(ind+1)]
            elif i in self.RUSS_ALPHABET_BIG:
                ind = self.RUSS_ALPHABET_BIG.index(i)
                decrypt_text += self.ALPHABET_BIG[self.N_RUSS-(ind+1)]
            else:
                decrypt_text += i
            self.decoded.setText(decrypt_text)


class CaesarDecoderWindow(DecoderWindow):

    KEYS = [QSpinBox]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.keyLabels[0].setMaximum(self.N_RUSS)


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
            elif i in self.RUSS_ALPHABET:
                ind = self.RUSS_ALPHABET.index(i)
                decrypt_text += self.RUSS_ALPHABET[(ind-key) % self.N_RUSS]
            elif i in self.RUSS_ALPHABET_BIG:
                ind = self.RUSS_ALPHABET_BIG.index(i)
                decrypt_text += self.RUSS_ALPHABET_BIG[(ind-key) % self.N_RUSS]
            else:
                decrypt_text += i
        self.decoded.setText(decrypt_text)


class RishelieDecoderWindow(DecoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)


    def decrypt(self):
        text = self.message.text()
        decrypt_text = ""
        key = self.keyLabels[0].text()
        base_index = 0
        if re.fullmatch(r'(\((\d,?)+\))*', key):
            l = re.split(r'\)\(|\(|\)', key)
            for i in l:
                nums = i.split(',')
                len_nums = len(nums) if nums[-1] != '' else len(nums)-1
                decrypt = list(range(len_nums))
                used_nums = set()
                for i in range(len_nums):
                    number = int(nums[i])-1
                    if 0 <= number < len_nums and base_index+number < len(text) and number not in used_nums:
                        decrypt[number] = text[base_index+i]
                        used_nums.add(number)
                    else:
                        self.error = QErrorMessage()
                        self.error.showMessage('Ваш ключ неверный')
                        return
                base_index += len_nums
                decrypt_text += ''.join(decrypt)
            for i in range(base_index, len(text)):
                decrypt_text += text[i]
        else:
            self.error = QErrorMessage()
            self.error.showMessage('Ваш ключ неверный')
            return
        self.decoded.setText(decrypt_text)


class GronsfeldDecoderWindow(DecoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
    
    def key_is_valid(self, key):
        try:
            assert key.isnumeric(), "Ваш ключ неверный"
        except AssertionException:
            return False
        else:
            return True
        
    def decrypt(self):
        text = self.message.text()
        decrypt_text = ""
        key = self.keyLabels[0].text()
        
        if self.key_is_valid(key):
            ind = 0
            for i in text:
                ind_k = int(key[ind % len(key)])
                if i in self.ALPHABET:
                    ind_i = self.ALPHABET.index(i)
                    decrypt_text += self.ALPHABET[(ind_i - ind_k) % self.N]
                elif i in self.ALPHABET_BIG:
                    ind_i = self.ALPHABET_BIG.index(i)
                    decrypt_text += self.ALPHABET_BIG[(ind_i - ind_k) % self.N]
                elif i in self.RUSS_ALPHABET:
                    ind_i = self.RUSS_ALPHABET.index(i)
                    decrypt_text += self.RUSS_ALPHABET[(ind_i - ind_k) % self.N_RUSS]
                elif i in self.RUSS_ALPHABET_BIG:
                    ind_i = self.RUSS_ALPHABET_BIG.index(i)
                    decrypt_text += self.RUSS_ALPHABET_BIG[(ind_i - ind_k) % self.N_RUSS]
                else:
                    decrypt_text += i
                ind += 1   
        else:
            self.error = QErrorMessage()
            self.error.showMessage('Ваш ключ неверный')
            return
        self.decoded.setText(decrypt_text)

