from PySide6.QtWidgets import (
QVBoxLayout,
QWidget,
QPushButton,
QLabel,
QLineEdit,
QSpinBox,
QErrorMessage)
import chipers

class DecoderWindow(QWidget):

    LABELS = []
    KEYS = []

    def __init__(self):
        super().__init__()

        self.chiper: chipers.Chiper

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

        self.keys = []
        for i in range(len(self.KEYS)):
            l = QLabel()
            l.setText(self.LABELS[i])
            layout.addWidget(l)
            self.keys.append(self.KEYS[i]())
            layout.addWidget(self.keys[i])

        layout.addWidget(l1)
        layout.addWidget(self.message)
        layout.addWidget(l2)
        layout.addWidget(self.decoded)
        layout.addWidget(self.button)

        self.setLayout(layout)
    
    def _get_keys(self):
        keys = []
        for key in self.keys:
            if isinstance(key, QLineEdit):
                keys.append(key.text())
            elif isinstance(key, QSpinBox):
                keys.append(key.value())
        return keys[0] if len(keys) == 1 else keys

    def decrypt(self):
        keys = self._get_keys()
        text = self.message.text()
        try:
            decoded_text = self.chiper.decrypt(text, keys)
            self.decoded.setText(decoded_text)
        except AssertionError as e:
            self.error = QErrorMessage()
            self.error.showMessage(str(e))



class AtbashDecoderWindow(DecoderWindow):

    def __init__(self):
        super().__init__()
        self.chiper = chipers.Atbash()

class CaesarDecoderWindow(DecoderWindow):

    KEYS = [QSpinBox]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Caesar()


class RishelieDecoderWindow(DecoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)
        self.chiper = chipers.Rishelie()


class GronsfeldDecoderWindow(DecoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Gronsfeld()


class VigenereDecoderWindow(DecoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Vigenere()


class PlayfairDecoderWindow(DecoderWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Playfair()