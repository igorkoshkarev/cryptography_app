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
import numpy as np

class DecoderWindow(QWidget):

    LABELS = []
    KEYS = []
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    ALPHABET_BIG = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    RUSS_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    RUSS_ALPHABET_BIG = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    ALL_LETTERS = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    N = 26
    N_RUSS = 33
    N_ALL = 118

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
        except AssertionError:
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


class VigenereDecoderWindow(DecoderWindow):

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
        
    def decrypt(self):
        text = self.message.text()
        decrypt_text = ""
        key = self.keyLabels[0].text()
        
        if self.key_is_valid(key):
            ind = 0
            for i in text:
                ind_k = self.ALL_LETTERS.index(key[ind % len(key)])
                if i in self.ALL_LETTERS:
                    ind_i = self.ALL_LETTERS.index(i)
                    decrypt_text += self.ALL_LETTERS[(ind_i - ind_k) % self.N_ALL]
                else:
                    decrypt_text += i
                ind += 1   
        else:
            self.error = QErrorMessage()
            self.error.showMessage('Ваш ключ неверный')
            return
        self.decoded.setText(decrypt_text)


class PlayfairDecoderWindow(DecoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']
    ALPHABET = "abcdefghiklmnopqrstuvwxyz"
    RUSS_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

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
        text = text.replace('j', 'i')
        text = text.replace('ё', 'е')
        lang = self.get_string_lang(key)
        if lang == 'english':
            alphabet = self.ALPHABET
            shape = (5,5)
        elif lang == 'russian':
            alphabet = self.RUSS_ALPHABET
            shape = (4,8)
        key_s = set(key)
        chiper_matrix = np.array(list(key) + sorted(set(alphabet) - set(key)))
        chiper_matrix = chiper_matrix.reshape(shape)
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
        text = text.lower()
        text = text.replace(' ', '')
        text = text.replace('j', 'i')
        text = text.replace('ё', 'е')
        if self.get_string_lang(text) == 'engilsh':
            spacer = 'x'
            another_spacer = 'q'
        else:
            spacer = 'ъ'
            another_spacer = 'ь'
        error = True
        bigram = []
        base_index = 0
        while error:
            error = False
            for i in range(base_index, len(text), 2):
                if i == len(text)-1:
                    if text[i] != spacer:
                        b = text[i] + spacer
                    else:
                        b = text[i] + another_spacer
                elif text[i] == text[i+1]:
                    if text[i] != spacer:
                        b = text[i] + spacer
                        text = text[:i+1] + spacer + text[i+1:]
                    else:
                        b = text[i] + another_spacer
                        text = text[:i+1] + another_spacer + text[i+1:]
                    error = True
                else:
                    b = text[i] + text[i+1]
                
                base_index += 2
                bigram.append(b)
                if error:
                    break
        return bigram


    def decrypt(self):
        text = self.message.text()
        decrypt_text = ""
        key = self.keyLabels[0].text()
        
        if self.key_is_valid(key) and self.text_is_valid(text) and self.get_string_lang(key) == self.get_string_lang(text):
            matrix = self.create_playfair_matrix(key)
            print(matrix)
            bigram = self.get_bigram(text)
            print(bigram)
            for i in bigram:
                s = matrix.shape
                first = i[0]
                second = i[1]
                pos_first = np.where(matrix == first)
                pos_first = (pos_first[0], pos_first[1])
                pos_second = np.where(matrix == second)
                pos_second = (pos_second[0], pos_second[1])
                if pos_first[0] == pos_second[0]:
                    pos_first, pos_second = (pos_first[0], (pos_first[1]-1) % s[1]), (pos_second[0], (pos_second[1]-1) % s[1])
                elif pos_first[1] == pos_second[1]:
                    pos_first, pos_second = ((pos_first[0]-1) % s[0], pos_first[1]), ((pos_second[0]-1) % s[0], pos_second[1])
                else:
                    pos_first, pos_second = (pos_first[0], pos_second[1]), (pos_second[0], pos_first[1])
                print(pos_first, pos_second)
                decrypt_text += matrix[int(pos_first[0])][int(pos_first[1])]
                decrypt_text += matrix[int(pos_second[0])][int(pos_second[1])]
        else:
            self.error = QErrorMessage()
            self.error.showMessage('Ваш ключ неверный')
            return
        self.decoded.setText(decrypt_text)
            