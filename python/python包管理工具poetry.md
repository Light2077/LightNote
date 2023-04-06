# poetry

官网：https://python-poetry.org/

使用教程：https://medium.com/analytics-vidhya/poetry-finally-an-all-in-one-tool-to-manage-python-packages-3c4d2538e828

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

推荐的安装方式是全局安装

[poetry官方安装教程](https://python-poetry.org/docs/#installing-with-the-official-installer)

windows

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

linux

```
curl -sSL https://install.python-poetry.org | python3 -
```





## 基本用法

https://python-poetry.org/docs/basic-usage/

### 创建一个新的项目

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

### 在已有的项目使用poetry

则在项目主目录下

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

### poetry虚拟环境管理

poetry首先会检查当前项目是否存在虚拟环境，如果存在，保持现有环境，如果没有，会自动创建一个与当前依赖相匹配的环境。

可以设置在当前目录下创建虚拟环境，若不设置会安装到默认目录

```
poetry config virtualenvs.in-project true
```

使用poetry创建并进入虚拟环境

> poetry 是进入虚拟环境

```
poetry shell
```

执行后，会在当前目录创建一个名为`.venv`的文件夹

退出虚拟环境

```
exit
```

参数调整的说明，默认情况下

```
poetry config virtualenvs.create true
```

当参数 `virtualenvs.create` 为 `true` 时，执行 `poetry install` 或 `poetry add` 时会检测当前项目是否有虚拟环境，没有就自动创建，默认为 `true`。

比如如果有conda 的虚拟环境，poetry就会在conda的环境安装包。

假设此时退出conda环境，再执行`poetry install`

```
conda deactivate
poetry install
```

会自动创建一个虚拟环境

```
Creating virtualenv tmp in C:\Users\light\Desktop\tmp\.venv
```

> 也就是说，conda的虚拟环境和poetry自己创建的虚拟环境是可以同时存在的。
>
> 如果你已经激活了conda的虚拟环境，那么poetry在安装包时就会安装到conda的环境。
>
> 如果你没有激活conda的虚拟环境，poetry在安装包时会安装到它自己创建的环境。



当参数 `virtualenvs.in-project` 为 `true` 时，虚拟环境的依赖将会放置于项目的文件夹内，而不是 poetry 默认的 `{cache-dir}/virtualenvs`，默认为 `false`。



### pyproject.toml介绍

这是最关键的文件，记录了包管理的方方面面。

```toml
[tool.poetry]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = ["light <435786117@qq.com>"]
readme = "README.md"
packages = [{include = "poetry_demo"}]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

pyproject.toml文件类似上面这样，共包含四个部分

- 第一部分包含了所有的元数据，包括项目名称、版本等等。
- 第二部分包含了项目所需的所有依赖包。The second section defines all the dependencies needed for the project
- 第三部分包含了所有开发时所需的依赖包，实际项目运行不需要。
- The fourth section defines a build system as indicated in [PEP 517](https://www.python.org/dev/peps/pep-0517/).



### 添加依赖包

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

添加时可以指定为开发过程中的依赖

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

卸载开发版本的依赖包

```
poetry remove -D flask
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
poetry install --remove-untracked  # 即将弃用的方法
```

`--sync`的参数解释为

```
Synchronize the environment with the locked packages and the specified groups.
```



## 其他

查看当前配置

```
poetry config --list
```

```
cache-dir = "C:\\Users\\iao\\AppData\\Local\\pypoetry\\Cache"
experimental.new-installer = true
experimental.system-git-client = false
installer.max-workers = null
installer.no-binary = null
installer.parallel = true
virtualenvs.create = true
virtualenvs.in-project = true
virtualenvs.options.always-copy = false
virtualenvs.options.no-pip = false
virtualenvs.options.no-setuptools = false
virtualenvs.options.system-site-packages = false
virtualenvs.path = "{cache-dir}\\virtualenvs"  # C:\Users\iao\AppData\Local\pypoetry\Cache\virtualenvs    
virtualenvs.prefer-active-python = false
virtualenvs.prompt = "{project_name}-py{python_version}"
```





获取当前项目使用的虚拟环境的地址

```
poetry env info --path
```



用poetry导出 requirements

```
poetry export --without-hashes -f requirements.txt -o requirements.txt
```



理论上应该可以直接把`.envs`文件夹拷贝走。

