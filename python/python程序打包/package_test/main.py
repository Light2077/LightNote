import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from food import bread
from fruit.apple import apple


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # (left, top, width, height)
        name1 = bread.get_name()
        name2 = apple.get_name()
        self.label1 = QLabel(name1, self)
        self.label2 = QLabel(name2, self)

        self.label1.move(50, 50)
        self.label2.move(50, 100)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Icon")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
