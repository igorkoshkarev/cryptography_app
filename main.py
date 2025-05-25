import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton, QSizePolicy
import EncoderWindow
import DecoderWindow
from freq_analyzer_window import FreqAnalyzeWindow


class MainWindow(QMainWindow):

    ENCODER_WINDOWS = [EncoderWindow.AtbashEncoderWindow, 
    EncoderWindow.CaesarEncoderWindow, 
    EncoderWindow.RishelieEncoderWindow, 
    EncoderWindow.GronsfeldEncoderWindow, 
    EncoderWindow.VigenereEncoderWindow, 
    EncoderWindow.PlayfairEncoderWindow,
    EncoderWindow.GammingEncoderWindow,
    EncoderWindow.GammingFileEncoderWindow,
    EncoderWindow.DESEncoderWindow,
    EncoderWindow.DESFileEncoderWindow,
    EncoderWindow.RSAEncoderWindow,
    EncoderWindow.DHEncoderWindow]
    DECODER_WINDOWS = [
    DecoderWindow.AtbashDecoderWindow, 
    DecoderWindow.CaesarDecoderWindow, 
    DecoderWindow.RishelieDecoderWindow, 
    DecoderWindow.GronsfeldDecoderWindow, 
    DecoderWindow.VigenereDecoderWindow,
    DecoderWindow.PlayfairDecoderWindow,
    DecoderWindow.GammingDecoderWindow,
    DecoderWindow.GammingFileDecoderWindow,
    DecoderWindow.DESDecoderWindow,
    DecoderWindow.DESFileDecoderWindow,
    DecoderWindow.RSADecoderWindow,
    DecoderWindow.DHDecoderWindow]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Шифры")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.ciphers = QComboBox()
        self.ciphers.addItems([
            'Шифр Атбаша', 
            'Шифр Цезаря', 
            'Шифр Решилье', 
            'Шифр Гронсфельда', 
            'Шифр Виженера',
            'Шифр Плейфейра',
            'Гаммирование',
            'Гаммирование файла',
            'DES текста',
            'DES файла',
            'RSA',
            'Диффи-Хеллман'])

        encode_button = QPushButton("Зашифровать")
        decode_button = QPushButton("Расшифровать")
        freq_analyze_button = QPushButton("Частотный анализ")
        encode_button.clicked.connect(self.encrypt)
        decode_button.clicked.connect(self.decrypt)
        freq_analyze_button.clicked.connect(self.freq_analyze)

        layout.addWidget(self.ciphers)
        layout.addWidget(encode_button)
        layout.addWidget(decode_button)
        layout.addWidget(freq_analyze_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def encrypt(self):
        ind = self.ciphers.currentIndex()
        self.w = self.ENCODER_WINDOWS[ind]()
        self.w.show()

    def decrypt(self):
        ind = self.ciphers.currentIndex()
        self.w = self.DECODER_WINDOWS[ind]()
        self.w.show()
    
    def freq_analyze(self):
        self.w = FreqAnalyzeWindow()
        self.w.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec())
