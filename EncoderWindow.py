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
import numpy as np


class EncoderWindow(QWidget):

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_BIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    RUSS_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    RUSS_ALPHABET_BIG = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    ALL_LETTERS = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    N = 26
    N_RUSS = 33
    N_ALL = 118
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
        self.setFixedSize(300, 200)
    
    def key_is_valid(self, key):
        try:
            assert key.isnumeric(), "Ваш ключ неверный"
        except AssertionError:
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


class VigenereEncoderWindow(EncoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
    
    def key_is_valid(self, key):
        try:
            assert key.isalpha(), "Ваш ключ неверный"
        except AssertionError:
            return False
        else:
            return True
        
    def encrypt(self):
        text = self.message.text()
        encrypt_text = ""
        key = self.keyLabels[0].text()
        
        if self.key_is_valid(key):
            ind = 0
            for i in text:
                ind_k = self.ALL_LETTERS.index(key[ind % len(key)])
                if i in self.ALL_LETTERS:
                    ind_i = self.ALL_LETTERS.index(i)
                    encrypt_text += self.ALL_LETTERS[(ind_i + ind_k) % self.N_ALL]
                else:
                    encrypt_text += i
                ind += 1   
        else:
            self.error = QErrorMessage()
            self.error.showMessage('Ваш ключ неверный')
            return
        self.encoded.setText(encrypt_text)


class PlayfairEncoderWindow(EncoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)

    def get_string_lang(self, string):
        if not string:
            return "both"
        is_english = False
        is_russian = False
        for i in string:
            if i in self.ALPHABET:
                is_english = True
            elif i in self.RUSS_ALPHABET:
                is_russian = True
            if is_english and is_russian:
                return "both"
        return "english" if is_english else "russian"

    def key_is_valid(self, key):
        try:
            key = key.lower()
            assert key.isalpha(), "Ваш ключ неверный"
            assert len(key) == len(set(key)), "Ваш ключ имеет повторяющиеся символы"
            assert self.get_string_lang(key) != 'both', "Ваш ключ должен содержать символы одного языка"
        except AssertionError:
            return False
        else:
            return True
    
    def create_playfair_matrix(self, key):
        lang = self.get_string_lang(key)
        if lang == 'english':
            alphabet = self.ALPHABET
            shape = (5,5)
        elif lang == 'russian':
            alphabet = self.RUSS_ALPHABET
            shape = (4,8)
        key_s = set(key)
        chiper_matrix = np.array(list(key) + sorted(set(alphabet) - set(key)))
        chiper_matrix.reshape(shape)
        return chiper_matrix

    def text_is_valid(self, text):
        try:
            text = text.replace(' ', '')
            assert text.isalpha(), "Ваш ключ неверный"
        except AssertionError:
            return False
        else:
            return True
    

    def get_bigram(self, text):
        text = text.replace(' ', '')
        error = True
        bigrams = []
        base_index = 0
        while error:
            for i in range(base_index, len(text), 2):
                if i == len(text)-1:
                    bigram = text[i] + 'x'
                elif text[i] == text[i+1]:
                    bigram = text[i] + 'x'
                    text = text[:i+1] + 'x' + text[i+1:]
                    error = True
                else:
                    bigram = text[i] + text[i+1]
                
                base_index += 2
                bigrams.append(bigram)
                if error:
                    break
        return bigrams


    def encode(self):
        text = self.message.text()
        encrypt_text = ""
        key = self.keyLabels[0].text()
        
        if self.key_is_valid(key) and self.text_is_valid(text) and self.get_string_lang(key) == self.get_string_lang(text):
            matrix = self.create_playfair_matrix(key)
            bigram = self.get_bigram(text)
