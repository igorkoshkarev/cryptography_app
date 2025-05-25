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
import keys


class KeyGeneratorWindow(QWidget):

    INIT_KEYS = []
    INIT_LABELS = []

    KEYS = []
    LABELS = []

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Генератор ключей")
        self.setFixedSize(300, 150)

        self.generator: keys.Key

        self.centralLayout = QVBoxLayout()

        self._draw_init_keys_widgets()
        self._draw_keys_widgets()

        self.button_init = QPushButton()
        self.button_init.setText("Сгенерировать начальные значения")

        self.button = QPushButton()
        self.button.setText("Сгенерировать ключи")

        self.button_init.clicked.connect(self.gen_init)
        self.button.clicked.connect(self.gen)

        self.centralLayout.addWidget(self.button_init)
        self.centralLayout.addWidget(self.button)

        self.setLayout(self.centralLayout)

    
    def _draw_init_keys_widgets(self):
        self.init_keys = []
        for i in range(len(self.INIT_KEYS)):
            l = QLabel()
            l.setText(self.INIT_LABELS[i])
            self.centralLayout.addWidget(l)
            self.init_keys.append(self.INIT_KEYS[i]())
            self.centralLayout.addWidget(self.init_keys[i])
    
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
        for key in self.init_keys:
            if isinstance(key, QLineEdit):
                keys.append(int(key.text()))
            elif isinstance(key, QSpinBox):
                keys.append(key.value())
        return keys[0] if len(keys) == 1 else keys

    def gen(self):
        try:
            keys = self.generator.gen(self._get_keys())
            for i, v in enumerate(keys):
                self.keys[i].setText(str(v))
        except AssertionError as e:
            self.error = QErrorMessage()
            self.error.showMessage(str(e))
    
    def gen_init(self):
        try:
            keys = self.generator.gen_init()
            for i, v in enumerate(keys):
                self.init_keys[i].setText(str(v))
        except AssertionError as e:
            self.error = QErrorMessage()
            self.error.showMessage(str(e))


class RSAKeyGeneratorWindow(KeyGeneratorWindow):
    INIT_KEYS = [QLineEdit, QLineEdit, QLineEdit]
    INIT_LABELS = ['p', 'q', 'e']

    KEYS = [QLineEdit, QLineEdit, QLineEdit]
    LABELS = ['n', 'e', 'd']
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.generator = keys.RSAKey()


class DHKeyGeneratorWindow(KeyGeneratorWindow):
    INIT_KEYS = [QLineEdit, QLineEdit, QLineEdit, QLineEdit]
    INIT_LABELS = ['p', 'g', 'a', 'b']

    KEYS = [QLineEdit, QLineEdit]
    LABELS = ['A', 'B']
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 400)
        self.generator = keys.DHKey()