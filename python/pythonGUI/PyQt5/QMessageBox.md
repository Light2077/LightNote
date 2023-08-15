在PyQt5中，您可以使用`QMessageBox`来弹出一个信息提示框。以下是一个简单的示例：

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Info Box Example")
        self.setGeometry(100, 100, 600, 400)

        btn = QPushButton("Show Info Box", self)
        btn.clicked.connect(self.show_info_box)
        btn.move(250, 180)

    def show_info_box(self):
        QMessageBox.information(self, "Information", "This is an information box!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

在上述代码中，我们创建了一个主窗口，其中有一个按钮。当您点击这个按钮时，它会弹出一个信息提示框。您可以使用`QMessageBox.information()`方法来显示这个提示框。