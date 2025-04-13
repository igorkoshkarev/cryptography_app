import sys
from collections import namedtuple
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QTextEdit, QHBoxLayout, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt

Alphabet = namedtuple("Alphabet", ['name', 'letters', 'length', 'freq'])

ENGLISH = Alphabet('eng', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 26, {'E': 0.123,'L': 0.040,'B': 0.016,'T': 0.096,'D': 0.036,'G': 0.016,'A': 0.081,'C': 0.032,'V': 0.009,'O': 0.079,'U': 0.031,'K': 0.005,'N': 0.072,'P': 0.023,'Q': 0.002,'I': 0.071,'F': 0.023,'X': 0.002,'S': 0.066,'M': 0.022,'J': 0.001,'R': 0.060,'W': 0.020,'Z': 0.001,'H': 0.051,'Y': 0.019})
RUSSIAN = Alphabet('rus', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 33, {' ': 0.175,'Р': 0.040,'Я': 0.018,'Х': 0.009,'О': 0.090,'В': 0.038,'Ы': 0.016,'Ж': 0.007,'Е': 0.072,'Л': 0.035,'З': 0.016,'Ю': 0.006,'А': 0.062,'К': 0.028,'Ъ': 0.014,'Ш': 0.006,'И': 0.062,'М': 0.026,'Б': 0.014,'Ц': 0.004,'Н': 0.053,'Д': 0.025,'Г': 0.013,'Щ': 0.003,'Т': 0.053,'П': 0.023,'Ч': 0.012,'Э': 0.003,'С': 0.045,'У': 0.021,'Й': 0.010,'Ф': 0.002})

class FreqAnalyzeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Частотный анализатор")
        self.setMinimumSize(300, 150)

        self.change_table = {}

        text_layout = QHBoxLayout()
        text_widget = QWidget()
        buttons_layout = QVBoxLayout()
        button_widget = QWidget()

        self.encrypted_text = QTextEdit()
        self.decrypted_text = QTextEdit()
        self.decrypted_text.setReadOnly(True)

        text_layout.addWidget(self.encrypted_text)
        text_layout.addWidget(self.decrypted_text)

        text_widget.setLayout(text_layout)

        decode_button = QPushButton("Расшифровать")
        decode_button.clicked.connect(self.decrypt_text)
        self.from_box = QComboBox()
        l = QLabel("на")
        l.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.to_box = QComboBox()
        change_table_button = QPushButton("Поменять")
        change_table_button.clicked.connect(self.change_symb_on_table)
        hist_button = QPushButton("Нарисовать гистограмму")
        file_button = QPushButton("Загрузить файл")
        hist_button.clicked.connect(self.draw_hist)
        file_button.clicked.connect(self.load_file)

        self.table_label = QTextEdit()
        self.table_label.setReadOnly(True)

        buttons_layout.addWidget(decode_button)
        buttons_layout.addWidget(self.from_box)
        buttons_layout.addWidget(l)
        buttons_layout.addWidget(self.to_box)
        buttons_layout.addWidget(change_table_button)
        buttons_layout.addWidget(hist_button)
        buttons_layout.addWidget(file_button)
        buttons_layout.addWidget(self.table_label)

        button_widget.setLayout(buttons_layout)

        central_layout = QVBoxLayout()
        central_widget = QWidget()
        central_layout.addWidget(text_widget)
        central_layout.addWidget(button_widget)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

    def get_lang(self, text):
        text = text.upper()
        if not text:
            return ENGLISH.name
        is_english = False
        is_russian = False
        for i in text:
            if i in ENGLISH.letters:
                is_english = True
            elif i in RUSSIAN.letters:
                is_russian = True
            if is_english and is_russian:
                return None
        return ENGLISH if is_english else RUSSIAN

    def get_freq_table_for_text(self, alphabet, text):
        text = text.upper()
        table = {}
        text_len = 0
        for i in alphabet.freq.keys():
            text_len += text.count(i)
        for i in alphabet.freq.keys():
            table[i] = text.count(i) / len(text)
        return table
    
    def get_change_table(self, freq1, freq2):
        table = {}
        a = sorted(freq1.items(), key=lambda x: x[1])
        b = sorted(freq2.items(), key=lambda x: x[1])
        for i in range(len(freq1)):
            table[a[i][0]] = b[i][0]
        return table
    
    def fill_combobox(self, lang):
        self.from_box.clear()
        self.to_box.clear()
        for i in lang.letters:
            self.from_box.addItem(i)
            self.to_box.addItem(i)
    
    def decrypt_text(self):
        lang = self.get_lang(self.encrypted_text.toPlainText())
        if lang is None:
            return 0
        self.fill_combobox(lang)
        freq2 = self.get_freq_table_for_text(lang, self.encrypted_text.toPlainText())
        self.table = self.get_change_table(freq2, lang.freq)
        self.print_change_table()
        print(self.table)
        decrypted_text = self.change_symbols_in_text_on_table(self.encrypted_text.toPlainText())
        self.decrypted_text.setPlainText(decrypted_text)
    
    def change_symbols_in_text_on_table(self, text):
        decrypted_text = ''
        for i in text.upper():
            decrypted_text += self.table.get(i, i)
        return decrypted_text

    def change_symb_on_table(self):
        from_symbol = self.from_box.currentText()
        to_symbol = self.to_box.currentText()
        print(from_symbol, to_symbol)
        b_symbol = self.table[from_symbol]
        for i in self.table.keys():
            if self.table[i] == to_symbol:
                self.table[i] = b_symbol
                break
        self.table[from_symbol] = to_symbol
        print(self.table)
        self.print_change_table()
        decrypted_text = self.change_symbols_in_text_on_table(self.encrypted_text.toPlainText())
        self.decrypted_text.setPlainText(decrypted_text)
    
    def draw_hist(self):
        freq_lang = self.get_lang(self.encrypted_text.toPlainText())
        if freq_lang is None:
            return 0
        freq_text = self.get_freq_table_for_text(freq_lang, self.encrypted_text.toPlainText())

        ordered_y = sorted(freq_lang.freq.values(), reverse=True)
        ordered_x = sorted(freq_lang.freq.keys(), key= lambda x: freq_lang.freq[x], reverse=True)

        ordered_y2 = sorted(freq_text.values(), reverse=True)
        ordered_x2 = sorted(freq_text.keys(), key= lambda x: freq_text[x], reverse=True)

        sbplt, (ax1, ax2) = plt.subplots(1, 2)

        ax1.bar(ordered_x, ordered_y)
        ax2.bar(ordered_x2, ordered_y2)

        plt.show()
    
    def load_file(self):
        path = QFileDialog.getOpenFileName(filter='*.txt')
        path = path[0]
        with open(path) as f:
            text = f.read()
            self.encrypted_text.setPlainText(text)
        self.decrypt_text()
    
    def print_change_table(self):
        l = " ".join([f"{i}->{v};\t" for i, v in self.table.items()])
        self.table_label.setPlainText(l)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec())

