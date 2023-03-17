

写代码有一段时间了，逐步感受到规范的重要性，先初步制定一套我个人的代码组织结构，如果以后觉得不好用，或者有更好的方案再改。（2023.03.03）

```
|=project_name
  |=src  # 代码文件夹
    |-__init__.py
    |-main.py
  |=pkgs  # 环境依赖包
    |=windows  # 不同环境应该区分开
    |=linux
  |=data  # 分析中用到的数据
  |=docs  # 说明文档，分析报告等
  |=output  # 程序输出的文件
  |=.venv  # 虚拟环境目录
  |=.config  # 配置文件夹
    |-config.json  # 配置文件
  |-README.md
  |-.gitignore
  |-.env  # 环境变量
```

https://guicommits.com/organize-python-code-like-a-pro/

之前老是觉得src文件夹很冗余，看到了上面的这篇文章，发现在一个项目有多个模块时用src文件夹放所有的代码文件也不错，比如这个模块既有正常的代码文件，又有gui页面时。

```
<myproject>
├── src/
   ├── myproject/
   ├── gui/
   └── tests/
├── README.md
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
