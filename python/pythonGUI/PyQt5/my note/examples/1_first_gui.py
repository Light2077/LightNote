import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 设置窗口位置和宽高
        self.setGeometry(200, 200, 300, 200)
        # 设置窗口标题
        self.setWindowTitle("Example")
        # 设置窗口图标
        img_path = "cat.png"
        self.setWindowIcon(QIcon(img_path))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
