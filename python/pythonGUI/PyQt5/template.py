import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel
)
from PyQt5 import QtCore

class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(600, 300, 400, 300)
        self.setWindowTitle('demo')
        self.show()

def main():
    app = QApplication(sys.argv)
    w = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()