QFileDialog

选择文件目录的示例代码

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog

class DirectorySelector(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 定义窗口的初始位置和大小
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('选择文件目录')

        # 设置窗口的布局为垂直布局
        layout = QVBoxLayout()

        # 创建"选择文件目录"按钮并连接到slot
        self.btn = QPushButton('选择文件目录', self)
        self.btn.clicked.connect(self.show_directory_dialog)

        # 创建一个文本输入框
        self.line_edit = QLineEdit(self)

        # 将按钮和文本输入框添加到布局中
        layout.addWidget(self.btn)
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

    def show_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "选择文件目录")
        if directory:
            self.line_edit.setText(directory)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DirectorySelector()
    ex.show()
    sys.exit(app.exec_())

```

