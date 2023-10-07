要为`QMessageBox`添加自定义按钮并执行自定义操作，你可以使用`QMessageBox`的`addButton`方法。当用户点击按钮时，你可以连接到一个自定义槽来执行所需的操作。下面是一个简单的示例，展示如何做到这一点：

```python
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

class CustomMessageBox:
    def __init__(self, target_dir):
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle("Title")
        self.msg_box.setText("Text")

        # 创建一个自定义按钮
        open_dir_btn = self.msg_box.addButton("打开目标文件目录", QMessageBox.ActionRole)
        open_dir_btn.clicked.connect(lambda: self.open_directory(target_dir))

        self.msg_box.exec()

    def open_directory(self, directory_path):
        """打开指定的目录"""
        QDesktopServices.openUrl(QUrl.fromLocalFile(directory_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    target_directory = "target_dir"  # 更改为你的目标目录
    CustomMessageBox(target_directory)

    sys.exit(app.exec_())
```

在这个示例中，我们首先创建了一个自定义的`QMessageBox`，然后为它添加了一个名为“打开目标文件目录”的按钮。点击此按钮时，会调用`open_directory`方法，该方法使用`QDesktopServices`来打开指定的文件夹目录。

你可以将`target_directory`的值替换为你要打开的实际目录。