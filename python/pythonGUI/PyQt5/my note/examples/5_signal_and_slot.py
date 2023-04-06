import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QLineEdit,
)


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.number = 0
        btn = QPushButton("按钮", self)
        self.label = QLabel(str(self.number), self)

        btn.move(90, 20)
        self.label.move(90, 50)
        btn.clicked.connect(self.add_number)

        self.setGeometry(300, 300, 280, 100)
        self.show()

    def add_number(self):
        self.number += 1
        self.label.setText(str(self.number))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
