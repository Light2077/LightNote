使用 PyQt5 创建一个文件目录查看器是非常可行的。下面是一个简单的示例代码，演示了如何实现这个功能。本例使用了 `QFileDialog` 来让用户选择一个目录，使用 `QTreeWidget` 来显示目录结构，以及使用 `QLineEdit` 来显示被双击的 CSV 文件名。

首先，确保已经安装了 PyQt5：

```bash
pip install PyQt5
```

接着，你可以尝试以下代码：

```python
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt

class FileExplorer(QWidget):
    def __init__(self):
        super(FileExplorer, self).__init__()
        layout = QVBoxLayout()

        self.pathLineEdit = QLineEdit()
        self.pathLineEdit.setPlaceholderText("选择的目录路径...")
        layout.addWidget(self.pathLineEdit)

        self.openDirBtn = QPushButton("选择目录")
        self.openDirBtn.clicked.connect(self.open_directory)
        layout.addWidget(self.openDirBtn)

        self.fileTree = QTreeWidget()
        self.fileTree.setHeaderLabel("文件名")
        self.fileTree.itemDoubleClicked.connect(self.on_item_double_click)
        layout.addWidget(self.fileTree)

        self.fileNameLineEdit = QLineEdit()
        self.fileNameLineEdit.setPlaceholderText("双击显示文件名...")
        layout.addWidget(self.fileNameLineEdit)

        self.setLayout(layout)

    def open_directory(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择目录")
        if folder_path:
            self.pathLineEdit.setText(folder_path)
            self.populate_tree(folder_path)

    def populate_tree(self, folder_path):
        self.fileTree.clear()
        self.add_files_to_tree(folder_path, self.fileTree.invisibleRootItem())

    def add_files_to_tree(self, folder_path, parent_item):
        for filename in os.listdir(folder_path):
            path = os.path.join(folder_path, filename)
            is_dir = os.path.isdir(path)
            if is_dir or filename.endswith('.csv'):
                item = QTreeWidgetItem([filename])
                parent_item.addChild(item)
                if is_dir:
                    self.add_files_to_tree(path, item)

    def on_item_double_click(self, item):
        if item.text(0).endswith('.csv'):
            self.fileNameLineEdit.setText(item.text(0))

if __name__ == '__main__':
    app = QApplication([])
    window = FileExplorer()
    window.show()
    app.exec_()
```

在这个例子中：

- 点击“选择目录”按钮将打开一个目录选择对话框。
- 选择一个目录后，该目录（包括其所有子目录）下的所有 CSV 文件将显示在一个 `QTreeWidget` 中。
- 双击一个 CSV 文件名将在下方的 `QLineEdit` 中显示该文件名。

希望这能帮助你实现你需要的功能！



自己写的

```python
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QTreeWidget,
    QWidget,
    QVBoxLayout,
    QTreeWidgetItem,
)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 200)
        self.init_ui()
        self.show()

    def init_ui(self):
        layout = QVBoxLayout()
        tree = QTreeWidget()
        tree.setHeaderLabel(["列名"])

        self.set_tree(tree)
        layout.addWidget(tree)

        self.setLayout(layout)

    def set_tree(self, tree: QTreeWidget):
        # item = QTreeWidgetItem([filename])
        # parent_item.addChild(item)
        root = tree.invisibleRootItem()
        item1 = QTreeWidgetItem(["child1"])
        item1_1 = QTreeWidgetItem(["child1_1"])
        item1_2 = QTreeWidgetItem(["child1_2"])
        item1_3 = QTreeWidgetItem(["child1_3"])

        item1.addChild(item1_1)
        item1.addChild(item1_2)
        item1.addChild(item1_3)

        item2 = QTreeWidgetItem(["child2"])
        item3 = QTreeWidgetItem(["child3"])

        root.addChild(item1)
        root.addChild(item2)
        root.addChild(item3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

```

生成一个树

```python
tree = QTreeWidget()
```

初始化树的列名，如果这里传入多个元素的list，那么QTreeWidget窗口就会是多列的

```python
tree.setHeaderLabel(["列名"])
```

创建一个结点，同理，列表里的是列元素的名字，一般一个就行。

```python
item1 = QTreeWidgetItem(["child1"])
```

添加子结点

```python
root.addChild(item1)
```

