QFrame

:book:[官方文档](https://doc.qt.io/qtforpython/)

最简单的案例

https://doc.qt.io/qtforpython/PySide6/QtWidgets/QFrame.html

https://blog.csdn.net/Dontla/article/details/105573337

https://blog.csdn.net/weixin_43496130/article/details/104242882

### 基本示例

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        # (left, top, width, height)
        label = QLabel("QFrame test")
        label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        label.setLineWidth(2)
        self.setCentralWidget(label)
        self.setGeometry(200, 200, 300, 200)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

```

![frames](images/frames.png)

### 两个Frame

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QPalette, QColor

class DemoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label1 = QLabel("区域 1 的内容")
        frame1 = QFrame(self)
        frame1.setFrameShape(QFrame.StyledPanel)
        frame1.setLineWidth(2)
        frame1.setPalette(QPalette(QColor(200, 200, 200)))
        frame1.setAutoFillBackground(True)
        frame1_layout = QVBoxLayout()
        frame1_layout.addWidget(label1)
        frame1.setLayout(frame1_layout)
        
        label2 = QLabel("区域 2 的内容")
        frame2 = QFrame(self)
        frame2.setFrameShape(QFrame.StyledPanel)
        frame2.setLineWidth(2)
        frame2.setPalette(QPalette(QColor(230, 230, 230)))
        frame2.setAutoFillBackground(True)
        frame2_layout = QVBoxLayout()
        frame2_layout.addWidget(label2)
        frame2.setLayout(frame2_layout)

        layout.addWidget(frame1)
        layout.addWidget(frame2)

        self.setLayout(layout)
        self.setWindowTitle('QFrame 示例')
        self.setGeometry(300, 300, 300, 200)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DemoApp()
    demo.show()
    sys.exit(app.exec_())

```

<img src="images/image-20230814142708512.png" alt="image-20230814142708512" style="zoom:67%;" />

### QGroupBox

```python
```



### 创建带颜色的QLabel

```python
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QLabel,
    QFrame,
)
from PyQt5.QtGui import QPalette, QColor


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 创建 QFrame
        frame = QFrame(self)
        frame.setFrameStyle(QFrame.Box)
        frame.setLineWidth(4)
        # 创建标签
        label1 = QLabel("Label 1", self)
        label2 = QLabel("Label 2", self)
        label3 = QLabel("Label 3", self)
        # 创建 QPalette
        palette1 = QPalette()
        palette1.setColor(QPalette.Background, QColor(220, 150, 150))

        palette2 = QPalette()
        palette2.setColor(QPalette.Background, QColor(150, 220, 150))

        palette3 = QPalette()
        palette3.setColor(QPalette.Background, QColor(150, 150, 220))

        # 设置 QLabel 的背景颜色
        label1.setAutoFillBackground(True)
        label1.setPalette(palette1)
        label2.setAutoFillBackground(True)
        label2.setPalette(palette2)
        label3.setAutoFillBackground(True)
        label3.setPalette(palette3)

        # 创建布局
        hbox = QHBoxLayout()
        hbox.addWidget(label1)
        hbox.addWidget(label2)
        hbox.addWidget(label3)
        frame.setLayout(hbox)

        self.setCentralWidget(frame)
        # self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("QFrame Example")
        self.show()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

```



加入文本对齐

```python
label1.setAlignment(QtCore.Qt.AlignCenter)
label2.setAlignment(QtCore.Qt.AlignCenter)
label3.setAlignment(QtCore.Qt.AlignCenter)
```

