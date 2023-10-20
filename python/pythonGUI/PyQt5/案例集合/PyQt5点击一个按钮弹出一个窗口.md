主窗口

```python
# main_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

from sub_window import ExampleDialog
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        
        btn = QPushButton("打开子窗口", self)
        btn.move(50, 50)
        self.setGeometry(200, 200, 300, 200)

        self.child = ExampleDialog()
        self.show()
        btn.clicked.connect(self.show_dialog)
    def show_dialog(self):
        self.child.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
```



子窗口

```python
# sub_window.py
import sys
from PyQt5.QtWidgets import QDialog, QLabel, QApplication


class ExampleDialog(QDialog):
    def __init__(self):
        super().__init__()

        label = QLabel("子窗口", self)
        label.move(50, 50)
        self.setGeometry(300, 300, 300, 200)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExampleDialog()
    ex.show()
    sys.exit(app.exec_())
```



