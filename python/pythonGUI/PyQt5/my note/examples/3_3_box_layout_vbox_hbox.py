import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setGeometry(200, 200, 300, 150)
        self.setWindowTitle("VBox+HBox")

        vbox = QVBoxLayout()
        btn1 = QPushButton("A", self)
        btn2 = QPushButton("B", self)
        btn3 = QPushButton("C", self)
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        hbox = QHBoxLayout()
        btn4 = QPushButton("D", self)
        btn5 = QPushButton("E", self)
        btn6 = QPushButton("F", self)
        hbox.addWidget(btn4)
        hbox.addWidget(btn5)
        hbox.addWidget(btn6)

        vbox.addLayout(hbox)

        w = QWidget()
        self.setCentralWidget(w)
        w.setLayout(vbox)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
