import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setGeometry(200, 200, 300, 150)
        self.setWindowTitle("HBox")

        hbox = QHBoxLayout()

        btn1 = QPushButton("D", self)
        btn2 = QPushButton("E", self)
        btn3 = QPushButton("F", self)

        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)

        w = QWidget()
        self.setCentralWidget(w)
        w.setLayout(hbox)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
