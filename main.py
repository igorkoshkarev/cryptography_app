import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton, QSizePolicy
import EncoderWindow
import DecoderWindow


class MainWindow(QMainWindow):

    ENCODER_WINDOWS = [EncoderWindow.AtbashEncoderWindow, 
    EncoderWindow.CaesarEncoderWindow, 
    EncoderWindow.RishelieEncoderWindow, 
    EncoderWindow.GronsfeldEncoderWindow, 
    EncoderWindow.VigenereEncoderWindow, 
    EncoderWindow.PlayfairEncoderWindow,
    EncoderWindow.GammingEncoderWindow,
    EncoderWindow.GammingFileEncoderWindow]
    DECODER_WINDOWS = [
    DecoderWindow.AtbashDecoderWindow, 
    DecoderWindow.CaesarDecoderWindow, 
    DecoderWindow.RishelieDecoderWindow, 
    DecoderWindow.GronsfeldDecoderWindow, 
    DecoderWindow.VigenereDecoderWindow,
    DecoderWindow.PlayfairDecoderWindow,
    DecoderWindow.GammingDecoderWindow,
    DecoderWindow.GammingFileDecoderWindow]

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
            'Гаммирование файла'])

        encode_button = QPushButton()
        decode_button = QPushButton()
        encode_button.setText("Зашифровать")
        decode_button.setText("Расшифровать")
        encode_button.clicked.connect(self.encrypt)
        decode_button.clicked.connect(self.decrypt)

        layout.addWidget(self.ciphers)
        layout.addWidget(encode_button)
        layout.addWidget(decode_button)

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec())
