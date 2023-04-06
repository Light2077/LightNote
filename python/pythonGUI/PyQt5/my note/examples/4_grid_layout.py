import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QFormLayout,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        # 设置定位和左上角坐标
        self.setGeometry(300, 300, 360, 260)
        self.setWindowTitle("Form Layout")
        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")

        title_edit = QLineEdit()
        author_edit = QLineEdit()
        review_edit = QTextEdit()

        layout = QFormLayout()
        layout.setSpacing(10)

        layout.addRow(title, title_edit)
        layout.addRow(author, author_edit)
        layout.addRow(review, review_edit)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Example()
    sys.exit(app.exec_())
