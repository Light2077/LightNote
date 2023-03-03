可以使用 QPalette 类。QPalette 是一个包含了所有窗口部件的颜色集合的类，可以通过它来设置背景颜色。

```python
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 创建一个 QLabel
        label = QLabel("Hello World", self)

        # 创建 QPalette
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 0, 0))

        # 设置 QLabel 的背景颜色
        label.setAutoFillBackground(True)
        label.setPalette(palette)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("QLabel Example")
        self.show()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
```





## 文本对齐方式

```python
label.setAlignment(QtCore.Qt.AlignCenter)
```

除了 `QtCore.Qt.AlignCenter` 对齐方式之外，PyQt5 中还有很多其他的对齐方式可供选择。下面列出了一些常用的对齐方式：

- `QtCore.Qt.AlignLeft`：左对齐
- `QtCore.Qt.AlignRight`：右对齐
- `QtCore.Qt.AlignHCenter`：水平居中对齐
- `QtCore.Qt.AlignTop`：上对齐
- `QtCore.Qt.AlignBottom`：下对齐
- `QtCore.Qt.AlignVCenter`：垂直居中对齐
- `QtCore.Qt.AlignCenter`：水平和垂直居中对齐（默认）

对于上述的对齐方式，可以通过按位或（|）运算符将它们组合起来。例如，以下代码将设置 QLabel 的对齐方式为水平和垂直居中对齐：

```
pythonCopy code
label.setAlignment(QtCore.Qt.AlignCenter)
```

如果要将 QLabel 的对齐方式设置为左对齐和上对齐，可以使用以下代码：

```
pythonCopy code
label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
```

在实际的使用中，根据需要选择不同的对齐方式可以使布局更加灵活和美观。