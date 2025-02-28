# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
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


class EncoderWindow(QWidget):

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_BIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    RUSS_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    RUSS_ALPHABET_BIG = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    N = 26
    N_RUSS = 33
    KEYS = []
    LABELS = []

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
        self.encoded = QLineEdit()
        self.encoded.setReadOnly(True)

        self.button = QPushButton()
        self.button.setText("Зашифровать")

        self.button.clicked.connect(self.encrypt)

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
        layout.addWidget(self.encoded)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def encrypt(self):
        print('Encrypt')



class AtbashEncoderWindow(EncoderWindow):

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
            elif i in self.RUSS_ALPHABET:
                ind = self.RUSS_ALPHABET.index(i)
                encrypt_text += self.RUSS_ALPHABET[self.N_RUSS-(ind+1)]
            elif i in self.RUSS_ALPHABET_BIG:
                ind = self.RUSS_ALPHABET_BIG.index(i)
                encrypt_text += self.RUSS_ALPHABET_BIG[self.N_RUSS-(ind+1)]
            else:
                encrypt_text += i
        self.encoded.setText(encrypt_text)


class CaesarEncoderWindow(EncoderWindow):

    KEYS = [QSpinBox]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.keyLabels[0].setMaximum(self.N_RUSS)


    def encrypt(self):
        text = self.message.text()
        encrypt_text = ""
        key = self.keyLabels[0].value()
        for i in text:
            if i in self.ALPHABET:
                ind = self.ALPHABET.index(i)
                encrypt_text += self.ALPHABET[(ind+key) % self.N]
            elif i in self.ALPHABET_BIG:
                ind = self.ALPHABET_BIG.index(i)
                encrypt_text += self.ALPHABET_BIG[(ind+key) % self.N]
            elif i in self.RUSS_ALPHABET:
                ind = self.RUSS_ALPHABET.index(i)
                encrypt_text += self.RUSS_ALPHABET[(ind+key) % self.N_RUSS]
            elif i in self.RUSS_ALPHABET_BIG:
                ind = self.RUSS_ALPHABET_BIG.index(i)
                encrypt_text += self.RUSS_ALPHABET_BIG[(ind+key) % self.N_RUSS]
            else:
                encrypt_text += i
        self.encoded.setText(encrypt_text)


class RishelieEncoderWindow(EncoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)


    def encrypt(self):
        text = self.message.text()
        encrypt_text = ""
        key = self.keyLabels[0].text()
        base_index = 0
        if re.fullmatch(r'(\((\d,?)+\))*', key):
            l = re.split(r'\)\(|\(|\)', key)
            for i in l:
                nums = i.split(',')
                len_nums = len(nums) if nums[-1] != '' else len(nums)-1
                used_nums = set()
                for i in range(len_nums):
                    number = int(nums[i])-1
                    if 0 <= number < len_nums and base_index+number < len(text) and number not in used_nums:
                        encrypt_text += text[base_index+number]
                        used_nums.add(number)
                    else:
                        self.error = QErrorMessage()
                        self.error.showMessage('Ваш ключ неверный')
                        return
                base_index += len_nums
            for i in range(base_index, len(text)):
                encrypt_text += text[i]
        else:
            self.error = QErrorMessage()
            self.error.showMessage('Ваш ключ неверный')
            return
        self.encoded.setText(encrypt_text)


class GronsfeldEncoderWindow(EncoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)
    
    def key_is_valid(self, key):
        try:
            assert key.isnumeric(), "Ваш ключ неверный"
        except AssertionException:
            return False
        else:
            return True
        
    def encrypt(self):
        text = self.message.text()
        encrypt_text = ""
        key = self.keyLabels[0].text()
        
        if key_is_valid(key):
            ind = 0
            for i in text:
                ind_k = int(key[ind % len(key)])
                if i in self.ALPHABET:
                    ind_i = self.ALPHABET.index(i)
                    encrypt_text += self.ALPHABET[(ind_i + ind_k) % self.N]
                elif i in self.ALPHABET_BIG:
                    ind_i = self.ALPHABET_BIG.index(i)
                    encrypt_text += self.ALPHABET_BIG[(ind_i + ind_k) % self.N]
                elif i in self.RUSS_ALPHABET:
                    ind_i = self.RUSS_ALPHABET.index(i)
                    encrypt_text += self.RUSS_ALPHABET[(ind_i + ind_k) % self.N]
                elif i in self.RUSS_ALPHABET_BIG:
                    ind_i = self.RUSS_ALPHABET_BIG.index(i)
                    encrypt_text += self.RUSS_ALPHABET_BIG[(ind_i + ind_k) % self.N]
                else:
                    encrypt_text += i
                ind += 1   
        else:
            self.error = QErrorMessage()
            self.error.showMessage('Ваш ключ неверный')
            return
        self.encoded.setText(encrypt_text)
