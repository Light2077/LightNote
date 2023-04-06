import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QPushButton


class Example(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle("MessageBox")
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        btn1 = QPushButton("infomation", self)
        btn2 = QPushButton("warning", self)
        btn3 = QPushButton("critical", self)
        btn4 = QPushButton("question", self)

        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)

        btn1.clicked.connect(self.show_information)
        btn2.clicked.connect(self.show_warning)
        btn3.clicked.connect(self.show_critical)
        btn4.clicked.connect(self.show_question)
        # self.btn4.clicked.connect(self.show_question)
        self.show()

    def show_information(self):
        QMessageBox.information(self, "info", "This is information box.")

    def show_warning(self):
        QMessageBox.warning(self, "warning", "This is warning box.")

    def show_critical(self):
        QMessageBox.critical(self, "critical", "This is critical box.")

    def show_question(self):
        QMessageBox.question(
            self,
            "question",  # 窗口标题
            "This is question box.",  # 窗口内容
            QMessageBox.Yes | QMessageBox.No,  # 按钮
            QMessageBox.No,  # 默认按钮
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
