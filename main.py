import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton, QSizePolicy
import EncoderWindow
import DecoderWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Шифры")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        ciphers = QComboBox()
        ciphers.addItems(['Шифр Адбаша', 'Шифр Цезаря', 'Шифр Решилье'])

        encode_button = QPushButton()
        decode_button = QPushButton()
        encode_button.setText("Зашифровать")
        decode_button.setText('Расшифровать')

        layout.addWidget(ciphers)
        layout.addWidget(encode_button)
        layout.addWidget(decode_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindow()
    e = EncoderWindow.AtbashEncoderWindow()
    d = DecoderWindow.AtbashDecoderWindow()
    e.show()
    m.show()
    d.show()
    sys.exit(app.exec())
