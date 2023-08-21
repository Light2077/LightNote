最简单的案例

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        # (left, top, width, height)
        self.setGeometry(200, 200, 300, 200)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

```

但是其实用QWidget也行

```python
class Example(QWidget):
    ...
```

这两种方式有什么区别？

在Qt框架中，`QWidget` 和 `QMainWindow` 都是用于创建应用程序窗口的类，但它们有一些不同的特点和用途。

`QWidget`：

- `QWidget` 是所有用户界面对象的基类。它提供了最基础的应用窗口。
- `QWidget` 没有提供状态栏、工具栏或菜单栏等。
- 它主要用于当你想创建一个没有太多预设主题或框架的自定义窗口时。
- `QWidget` 更加轻量级，如果你不需要状态栏、菜单栏等，使用 `QWidget` 将会更加高效。
  

`QMainWindow`：

- `QMainWindow` 是一个用于创建主应用程序窗口的类，它继承自 `QWidget`。
- 除了具有 `QWidget` 的所有功能外，`QMainWindow` 还提供了一系列额外的功能和预设布局，这些可以使你更容易地创建“标准”的应用程序窗口。
- 它有一些预定义的地方（如状态栏、工具栏、菜单栏、停靠窗口等）可以放置这些元素。
  

当你的应用程序需要这些额外的窗口特性（如菜单栏、工具栏、状态栏等）时，使用 `QMainWindow` 会更方便。否则，如果你只需要一个简单的窗口，使用 `QWidget` 就足够了。

### 继承QApplication

也可以直接继承QApplication

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        # (left, top, width, height)
        self.setGeometry(200, 200, 300, 200)
        self.show()

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.window = Example()
        # window = Example()  # 这样会导致窗口一闪就消失的错误

app = App(sys.argv)
sys.exit(app.exec_())
```

