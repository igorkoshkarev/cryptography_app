from PySide6.QtWidgets import (
QVBoxLayout,
QWidget,
QPushButton,
QLabel,
QLineEdit,
QSpinBox,
QErrorMessage,
QFileDialog)
import chipers


class EncoderWindow(QWidget):

    KEYS = []
    LABELS = []

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Шифр")
        self.setFixedSize(300, 150)

        self.chiper: chipers.Chiper

        self.centralLayout = QVBoxLayout()
    
    def _draw_keys_widgets(self):
        self.keys = []
        for i in range(len(self.KEYS)):
            l = QLabel()
            l.setText(self.LABELS[i])
            self.centralLayout.addWidget(l)
            self.keys.append(self.KEYS[i]())
            self.centralLayout.addWidget(self.keys[i])

    def _get_keys(self):
        keys = []
        for key in self.keys:
            if isinstance(key, QLineEdit):
                keys.append(key.text())
            elif isinstance(key, QSpinBox):
                keys.append(key.value())
        return keys[0] if len(keys) == 1 else keys

    def encrypt(self):
        pass


class EncoderTextWindow(EncoderWindow):

    KEYS = []
    LABELS = []

    def __init__(self):
        super().__init__()

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

        self._draw_keys_widgets()

        self.centralLayout.addWidget(l1)
        self.centralLayout.addWidget(self.message)
        self.centralLayout.addWidget(l2)
        self.centralLayout.addWidget(self.encoded)
        self.centralLayout.addWidget(self.button)

        self.setLayout(self.centralLayout)
    
    def encrypt(self):
        keys = self._get_keys()
        text = self.message.text()
        try:
            encoded_text = self.chiper.encrypt(text, keys)
            self.encoded.setText(encoded_text)
        except AssertionError as e:
            self.error = QErrorMessage()
            self.error.showMessage(str(e))


class EncoderFileWindow(EncoderWindow):
    def __init__(self):
        super().__init__()

        self.path = ''

        self.currentFile = QLabel('Выбран файл: ')

        self.selectFileButton = QPushButton("Выбрать файл")
        l2 = QLabel("Имя нового файла: ")
        self.newFileName = QLineEdit()

        self.button = QPushButton()
        self.button.setText("Зашифровать")

        self.selectFileButton.clicked.connect(self.select_file)
        self.button.clicked.connect(self.encrypt)

        self._draw_keys_widgets()

        self.centralLayout.addWidget(self.currentFile)
        self.centralLayout.addWidget(self.selectFileButton)
        self.centralLayout.addWidget(l2)
        self.centralLayout.addWidget(self.newFileName)
        self.centralLayout.addWidget(self.button)

        self.setLayout(self.centralLayout)

    def select_file(self):
        self.path = QFileDialog.getOpenFileName()[0]
        self.update_path_widgets()
    
    def _remove_path(self):
        self.path = ''
        self.clear_path_widgets()

    def update_path_widgets(self):
        self.currentFile.setText("Выбран файл: " + self.path)
        self.newFileName.setText(self.path + '.igr')
    
    def clear_path_widgets(self):
        self.currentFile.setText("Выбран файл: ")
        self.newFileName.setText("")

    def encrypt(self):
        keys = self._get_keys()
        if self.path and self.newFileName.text():
            try:
                with open(self.path, 'br') as f:
                    text = f.read()
                    encoded_text = self.chiper.encrypt(text, keys)
                with open(self.newFileName.text(), 'bw') as f:
                    for i in encoded_text:
                        f.write(i.to_bytes())
                self._remove_path()
            except AssertionError as e:
                self.error = QErrorMessage()
                self.error.showMessage(str(e))

class AtbashEncoderWindow(EncoderTextWindow):

    def __init__(self):
        super().__init__()
        self.chiper = chipers.Atbash()


class CaesarEncoderWindow(EncoderTextWindow):

    KEYS = [QSpinBox]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Caesar()


class RishelieEncoderWindow(EncoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)
        self.chiper = chipers.Rishelie()


class GronsfeldEncoderWindow(EncoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Gronsfeld()


class VigenereEncoderWindow(EncoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Vigenere()


class PlayfairEncoderWindow(EncoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Playfair()

class GammingEncoderWindow(EncoderTextWindow):

    KEYS = [QSpinBox, QSpinBox, QSpinBox, QSpinBox]
    LABELS = ['Сид: ', 'a: ', 'b: ', 'm: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.chiper = chipers.Gamming()

class GammingFileEncoderWindow(EncoderFileWindow):

    KEYS = [QSpinBox, QSpinBox, QSpinBox, QSpinBox]
    LABELS = ['Сид: ', 'a: ', 'b: ', 'm: ']

    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 400)
        self.chiper = chipers.GammingFile()
