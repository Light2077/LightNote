# poetry

官网：https://python-poetry.org/

## 安装

可以在conda的base环境下直接

```
pip install poetry
```

查看是否安装成功

```
>>> poetry --version
Poetry (version 1.3.1)
```

更新

```
poetry self update
```

## 基本用法

https://python-poetry.org/docs/basic-usage/

创建新项目

```
poetry new poetry-demo
```

文件结构为

```
poetry-demo
├── pyproject.toml
├── README.md
├── poetry_demo
│   └── __init__.py
└── tests
    └── __init__.py
```

如果想在已有的项目使用poetry，则在项目主目录下

```
poetry init
```

~~注意：在add依赖包之前，最好还是创建一个虚拟环境~~

```
python -m venv venv
# Windows激活虚拟环境
.\venv\Scripts\activate.bat
# Linux激活虚拟环境
source ./venv/Scripts/activate
```

> 不要用上面的方法了

设置在当前目录下创建虚拟环境

```
poetry config virtualenvs.in-project true
```

使用poetry创建虚拟环境

```
poetry shell
```

执行后，会在当前目录创建一个名为`.venv`的文件夹

退出虚拟环境

```
exit
```





增加一个依赖包，以flask为例

```
poetry add flask
```

```
Using version ^2.2.2 for flask

Updating dependencies
Resolving dependencies... Downloading 
...
...

Writing lock file

Package operations: 9 installs, 0 updates, 0 removals

  • Installing colorama (0.4.6)
  • Installing markupsafe (2.1.1)
  • Installing zipp (3.11.0)
  • Installing click (8.1.3)
  • Installing importlib-metadata (5.2.0)
  • Installing itsdangerous (2.1.2)
  • Installing jinja2 (3.1.2)
  • Installing werkzeug (2.2.2)
  • Installing flask (2.2.2)
```

会自动增加相应的依赖包

可以指定为开发过程中的依赖

```
poetry add pytest --dev
```

安装`pyproject.toml`文件中的全部依赖

```
poetry install
```

只安装非development依赖

```
poetry install --no-dev
```

更新所有锁定版本的依赖包

```
poetry update
```

更新指定依赖包

```
poetry update flask
```

卸载依赖包

```
poetry remove flask
```

查看可以更新的依赖包

```
poetry show --outdated
```

查看项目安装的依赖，`-t`表示以树形结构查看

```
poetry show
poetry show -t
```

### 如果不小心用pip安装了一个其他包怎么办

如果你反应得够快

那就先用poetry add 然后再remove

```
poetry add requests
poetry remove requests
```

这个方法当然不够好

最优解是

```
poetry install --sync
# 或
poetry install --remove-untracked  # 即将弃用
```

`--sync`的参数解释为

```
Synchronize the environment with the locked packages and the specified groups.
```

