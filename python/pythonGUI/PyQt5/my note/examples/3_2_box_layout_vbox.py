import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setGeometry(200, 200, 300, 150)
        self.setWindowTitle("VBox")
        vbox = QVBoxLayout()

        btn1 = QPushButton("A", self)
        btn2 = QPushButton("B", self)
        btn3 = QPushButton("C", self)

        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        w = QWidget()
        self.setCentralWidget(w)
        w.setLayout(vbox)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
