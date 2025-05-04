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

class DecoderWindow(QWidget):

    LABELS = []
    KEYS = []

    def __init__(self):
        super().__init__()

        self.chiper: chipers.Chiper

        self.setWindowTitle("Расшифровка")
        self.setFixedSize(300, 150)

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


class DecoderTextWindow(DecoderWindow):

    def __init__(self):
        super().__init__()

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

        self._draw_keys_widgets()

        self.centralLayout.addWidget(l1)
        self.centralLayout.addWidget(self.message)
        self.centralLayout.addWidget(l2)
        self.centralLayout.addWidget(self.decoded)
        self.centralLayout.addWidget(self.button)

        self.setLayout(self.centralLayout)

    def decrypt(self):
        keys = self._get_keys()
        text = self.message.text()
        try:
            decoded_text = self.chiper.decrypt(text, keys)
            self.decoded.setText(decoded_text)
        except AssertionError as e:
            self.error = QErrorMessage()
            self.error.showMessage(str(e))


class DecoderFileWindow(DecoderWindow):
    def __init__(self):
        super().__init__()

        self.path = ''

        self.currentFile = QLabel('Выбран файл: ')

        self.selectFileButton = QPushButton("Выбрать файл")
        l2 = QLabel("Имя нового файла: ")
        self.newFileName = QLineEdit()

        self.button = QPushButton()
        self.button.setText("Расшифровать")

        self.selectFileButton.clicked.connect(self.select_file)
        self.button.clicked.connect(self.decrypt)

        self._draw_keys_widgets()

        self.centralLayout.addWidget(self.currentFile)
        self.centralLayout.addWidget(self.selectFileButton)
        self.centralLayout.addWidget(l2)
        self.centralLayout.addWidget(self.newFileName)
        self.centralLayout.addWidget(self.button)

        self.setLayout(self.centralLayout)

    def select_file(self):
        self.path = QFileDialog.getOpenFileName()[0]
        self.currentFile.setText("Выбран файл: " + self.path)
        if self.path.endswith('.igr'):
            self.newFileName.setText(self.path[:-3])
        else:
            self.newFileName.setText(self.path)
    
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

    def decrypt(self):
        keys = self._get_keys()
        if self.path and self.newFileName.text():
            try:
                with open(self.path, 'br') as f:
                    text = f.read()
                    encoded_text = self.chiper.decrypt(text, keys)
                with open(self.newFileName.text(), 'bw') as f:
                    for i in encoded_text:
                        f.write(i.to_bytes())
                self._remove_path()
            except AssertionError as e:
                self.error = QErrorMessage()
                self.error.showMessage(str(e))



class AtbashDecoderWindow(DecoderTextWindow):

    def __init__(self):
        super().__init__()
        self.chiper = chipers.Atbash()

class CaesarDecoderWindow(DecoderTextWindow):

    KEYS = [QSpinBox]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Caesar()


class RishelieDecoderWindow(DecoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)
        self.chiper = chipers.Rishelie()


class GronsfeldDecoderWindow(DecoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Gronsfeld()


class VigenereDecoderWindow(DecoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Vigenere()


class PlayfairDecoderWindow(DecoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.Playfair()

class GammingDecoderWindow(DecoderTextWindow):

    KEYS = [QSpinBox, QSpinBox, QSpinBox, QSpinBox]
    LABELS = ['Сид: ', 'a: ', 'b: ', 'm: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.chiper = chipers.Gamming()


class GammingFileDecoderWindow(DecoderFileWindow):

    KEYS = [QSpinBox, QSpinBox, QSpinBox, QSpinBox]
    LABELS = ['Сид: ', 'a: ', 'b: ', 'm: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.chiper = chipers.GammingFile()

class DESDecoderWindow(DecoderTextWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.DES()
    
    def _get_keys(self):
        return int(self.keys[0].text())

class DESFileDecoderWindow(DecoderFileWindow):

    KEYS = [QLineEdit]
    LABELS = ['Ключ: ']

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.chiper = chipers.DESFile()
    
    def _get_keys(self):
        return int(self.keys[0].text())

