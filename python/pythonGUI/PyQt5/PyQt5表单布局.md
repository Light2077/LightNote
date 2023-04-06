https://blog.csdn.net/gixome/article/details/121008868

```python
import sys
 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QMessageBox, QApplication, QVBoxLayout, QWidget, \
    QLabel, QGridLayout, QLineEdit, QTextEdit, QFormLayout
 
'''
PyQt5直接用代码布局 -表单布局表单设计(QFormdLayout)
'''
 
 
class FormFormDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        # 设置定位和左上角坐标
        self.setGeometry(300, 300, 360, 260)
        # 设置窗口标题
        self.setWindowTitle('表单布局表单设计 的演示')
        # 设置窗口图标
        # self.setWindowIcon(QIcon('../web.ico'))
 
        titleLabel = QLabel('标题')
        authorLabel = QLabel('姓名')
        contentLabel = QLabel('论文')
 
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        contentEdit = QTextEdit()
 
        formLayout = QFormLayout()
        formLayout.setSpacing(10)
 
        formLayout.addRow(titleLabel,titleEdit)
        formLayout.addRow(authorLabel,authorEdit)
        formLayout.addRow(contentLabel,contentEdit)
 
        self.setLayout(formLayout)
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用图标
    w = FormFormDemo()
    sys.exit(app.exec_())
```

