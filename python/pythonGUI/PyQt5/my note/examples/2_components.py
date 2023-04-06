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
        btn = QPushButton("按钮", self)
        label = QLabel("标签", self)
        line_edit = QLineEdit(self)

        btn.move(90, 20)
        label.move(90, 50)
        line_edit.move(90, 80)

        self.setGeometry(300, 300, 280, 130)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
