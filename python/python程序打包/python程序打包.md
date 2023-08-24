:book:官方文档：https://pyinstaller.readthedocs.io/en/stable/index.html

https://blog.csdn.net/tangfreeze/article/details/112240342

参考https://www.cnblogs.com/paisenpython/p/10329882.html

## 简明的程序打包方法

1.以单文件形式打包

```shell
pyinstaller -F -w -i favicon.ico main.py
```

- `-F`：表示以单文件形式打包
- `-w`：运行时不显示终端窗口（对于PyQt5这样的程序比较有用）
- `-i`：设置程序图标，后接图标文件路径

2.分散文件打包

```shell
pyinstaller -D -w -i favicon.ico main.py
```

3.先创建spec文件再打包


```shell
pyi-makespec -D -w -i favicon.ico main.py
```

会生成一个`main.spec`文件，按需要修改这个文件后运行

```shell
pyinstaller main.spec
```

对于简单的单py文件的程序，直接使用方式1或方式2打包即可，对于包含多个模块、多个资源的更复杂的程序，则需要通过方式3先创建spec文件，然后按照需求定制spec文件，再进行打包。

下面通过具体案例讲解实现

## 准备工作

先用conda创建好虚拟环境

```
conda create -n pypackage python=3.9
```

进入安装好的虚拟环境

```
conda activate pypackage
```

安装需要的库，这里以打包pyqt5程序为例

```
pip install pyqt5
pip install pyinstaller
```

创建一个文件夹，目录如下

```
|-package_test
  |-main.py
```

在`main.py`中编写简单的PyQt5应用

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # (left, top, width, height)
        self.setGeometry(300, 300, 300, 150)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
```

进入`package_test`目录，在命令行输入

```
python main.py
```

查看上面编写好的GUI界面



## 开始打包第一个程序

以最简单的打包单文件的例子开始

最稳妥的方式是先生成spec文件，如下

> main.py 和 main.spec 最好在一个目录下。

```
pyi-makespec -D -w main.py
```

如果希望打包单文件

```
pyi-makespec -F -w main.py
```

### 指定dist 和 build的目录位置

指定目录位置，更好地管理项目结构。

在src目录（目录下有main.spec）中：

```
pyinstaller --distpath ../dist --workpath ../build main.spec
```



`-D`表示生成包含多个文件的目录，其中有一个可执行程序

`-w`表示程序运行时不显示命令行窗口

运行完毕后可以看到目录下多了一个`main.spec`文件

```
|-package_test
  |-main.py
  |-main.spec
```

在这个最简单的例子中，不需要修改这个spec文件，直接运行下面的命令打包程序即可

```
pyinstaller main.spec
```



打包完毕后，文件目录变成

```
  |- package_test
    |- build
    |- dist
    |- main.py
    |- main.spec
```

执行`dist/main/main.exe`就可以看到我们创建的程序的页面了。

同时可以看到`dist/main`文件夹的大小为88mb。这么一个没有任何功能的小程序体积都那么大，真是离谱。

那如果换成单文件打包呢，首先删除之前生产的build和dist文件夹，下面的步骤省略了创建spec的部分。

```
pyinstaller -F -w main.py
```

程序缩小为35mb了。说实话还是挺大的。

用虚拟环境打包的结果跟之前也没什么区别。

## 打包多个包的程序

创建几个包使文件目录变成

```
|-package_test
  |-food
    |-__init__.py
    |-bread.py
  |-fruit
    |-apple
      |-__init__.py
      |-apple.py
    |-__init__.py
  |-main.py
  |-main.spec
```

其中`bread.py`的代码为

```python
def get_name():
    return "bread"
```

`apple/apple.py`的代码为

```python
def get_name():
    return "apple"
```

修改`main.py`

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from food import bread
from fruit.apple import apple

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # (left, top, width, height)
        name1 = bread.get_name()
        name2 = apple.get_name()
        self.label1 = QLabel(name1)
        self.label2 = QLabel(name2)
        
        self.label1.move(50, 50)
        self.label2.move(50, 100)
        self.setGeometry(300, 300, 300, 150)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
```



首先尝试直接打包

```shell
pyinstaller -D -w main.py
```

发现也能自动识别要导入的包，直接解决问题了。

## 打包带有资源文件的程序

在main.spec中修改

```python
a = Analysis(
    ...
    datas=[('icon.png', '.'),
           ('style.qss', '.')],
    ...
)
```

## 打包时排除某个包



## 参数说明

#

| -h，--help                  | 查看该模块的帮助信息                                         |
| --------------------------- | ------------------------------------------------------------ |
| -F，-onefile                | 产生单个的可执行文件                                         |
| -D，--onedir                | 产生一个目录（包含多个文件）作为可执行程序                   |
| -a，--ascii                 | 不包含 Unicode 字符集支持                                    |
| -d，--debug                 | 产生 debug 版本的可执行文件                                  |
| -w，--windowed，--noconsolc | 指定程序运行时不显示命令行窗口（仅对 Windows 有效）          |
| -c，--nowindowed，--console | 指定使用命令行窗口运行程序（仅对 Windows 有效）              |
| -o DIR，--out=DIR           | 指定 spec 文件的生成目录。如果没有指定，则默认使用当前目录来生成 spec 文件 |
| -p DIR，--path=DIR          | 设置 Python 导入模块的路径（和设置 PYTHONPATH 环境变量的作用相似）。也可使用路径分隔符（Windows 使用分号，Linux 使用冒号）来分隔多个路径 |
| -n NAME，--name=NAME        | 指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字 |

