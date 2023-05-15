

写代码有一段时间了，逐步感受到规范的重要性，先初步制定一套我个人的代码组织结构，如果以后觉得不好用，或者有更好的方案再改。（2023.03.03）

```
├── project_name
  ├── src  # 代码文件夹
  │   ├── __init__.py
  │   └── main.py
  │
  ├─ pkgs  # 环境依赖包
  │   ├── windows  # 不同环境应该区分开
  │   └── linux
  │
  ├── data  # 分析中用到的数据文件夹
  ├── docs  # 说明文档，分析报告文件夹
  ├── output  # 程序输出文件夹
  ├── .venv  # 虚拟环境目录
  ├── .config  # 配置文件夹
  │   └── config.json  # 配置文件
  │
  ├── README.md
  ├── .gitignore
  └── .env  # 环境变量
```

https://guicommits.com/organize-python-code-like-a-pro/

之前老是觉得src文件夹很冗余，看到了上面的这篇文章，发现在一个项目有多个模块时用src文件夹放所有的代码文件也不错，比如这个模块既有正常的代码文件，又有gui页面时。

```
<myproject>
├── src/
│  ├── myproject/
│  ├── gui/
│  └── tests/
│
└── README.md
```

> 这种情况又该怎么用pyinstaller打包项目呢？

不过感觉还是得分情况，如果包里面只有一个模块，感觉可以不需要src文件夹

```
<project>
├── src
│   ├── <module>/*
│   │    ├── __init__.py
│   │    └── many_files.py
│   │
│   └── tests/*
│        └── many_tests.py
│
├── .gitignore
├── pyproject.toml
└── README.md
```

### 测试

关于一种项目结构的测试

这里的场景是，我的项目创建了一个包，然后我有一个scripts文件夹，这里边包含了一些利用`example_project`包编写的脚本。希望是运行`run.py`能直接调用`examle_project`包里面的相关方法。

创建内外两个`run.py`，内容都一样，用于对比

```
example_project
├── example_project
│   ├── __init__.py
│   └── tools.py
├── run.py  # x 用于对比
│
└── scripts
    └── run.py
```

其中`tools.py`

```python
def say_hello():
    print("hello")
```

`run.py`

```python
from example_project.tools import say_hello

say_hello()
```

在`example_project`目录下运行

运行内部的`run.py`

```
python scripts/run.py
```

```
Traceback (most recent call last):
  File "..\example_project\scripts\run.py", line 1, in <module>
    from example_project.tools import say_hello
ModuleNotFoundError: No module named 'example_project'
```

运行外边的`run.py`

```
python run.py
```

```
hello
```

要想运行`scripts`文件夹下的脚本，需要先设置python path

```
$ set PYTHONPATH=E:\projects\example_project
$ python scripts/run.py
```

写成一行

```
set PYTHONPATH=E:\projects\example_project & python scripts/run.py
```

如果是linux

```
export PYTHONPATH=/projects/example_project ; python scripts/run.py
```

