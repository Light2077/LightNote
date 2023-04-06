文章[Logging in Python like a PRO ](https://guicommits.com/how-to-log-in-python-like-a-pro/)提到

- 调用logging的`setLevel`,`addHander`,`addFilter`的方式难以理解和维护
- 使用文件配置(`fileConfig`)的方式不够灵活，不方便动态设定一些值
- 而使用python字典配置(`dictConfig`)的方式容易学习也容易设置。

本着一招鲜吃片天的思想，先学习最实用的logging配置方式。

下面从简单的案例开始，逐步增加复杂度并使用`dictConfig`的方式实现logging的配置。

## dictConfig模板

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": { },
    "filters": { },
    "handlers": { },
    "loggers": { },
    "root": { },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

参数解释：

- `version`，version表示目前python的架构版本，以后如果发布了另一种架构版本的python，这个值可能会变，当然现在的python只有一个架构版本。

- `disable_existing_loggers` ：建议就设为False，字面上理解就是是否禁用其他现存的logger。

- `formatters`：[`Formatter`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Formatter) 格式器对象，用于控制日志输出格式。

- `filters`：是一个字典，其中键是过滤器 ID ，值是一个描述如何配置相应 Filter 实例的字典。

  将在配置字典中搜索键 `name` (默认值为空字符串) 并且该键会被用于构造 [`logging.Filter`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Filter) 实例。

- `handlers`：处理器对象，用于控制日志往哪里输出

- `loggers`：记录器对象，键是记录器名称，值是一个描述如何配置相应 Logger 实例的字典。

- `root`：类似于`loggers`中的每个logger，`propagate` 设置不可用。

下面介绍config的每一项应该怎么填写。

### formatters

格式器的配置

```python
"formatters": {
    "simple": {  
        "format": "%(message)s",
    },
    "default": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S", 
    }
}
```

上面展示了formatters包含两个Formatter的例子。其中：

`default`和`simple`分别是这两个Formatter的名字，他们都通过`format`来格式化日志输出的结果，其中`default`格式器还多了一个`datefmt`的配置，用于格式化日期时间的输出。

`format`控制日志具体显示什么内容，对于上面的例子，simple格式器显示的日志类似于：

```
```

default格式器显示日志类似于：

```
```

更完整的信息格式参考 [LogRecord 属性](https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes)

```
%(levelname)-8s - %(message)s
```

`-8s`表示用空格填充，以保证对齐，效果类似于

```
DEBUG    - A DEBUG message
INFO     - An INFO message
WARNING  - A WARNING message
ERROR    - An ERROR message
CRITICAL - A CRITICAL message
```



### handles

```python
"handlers": {
    "logfile": {
        "formatter": "default",
        "level": "ERROR",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": ERROR_LOG_FILENAME,
        "backupCount": 2,
    },
    "verbose_output": {
        "formatter": "simple",
        "level": "DEBUG",
        "class": "logging.StreamHandler", 
        "stream": "ext://sys.stdout",
    }
}
```

- `formatter`：选用的格式器。
- `level`：日志输出的等级。
- `class`：对应的logging.handles类。
- `filename`：日志要输出到的文件名。
- `backupCount`：最多存在多少个日志文件。

其他的handles：https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers

可以参考官方文档，实例化这些处理器需要什么参数都可以在上面的字典中配置



`"ext://sys.stdout"`是什么意思？

有时一个配置需要引用配置以外的对象，例如 `sys.stdout`。 如果配置字典是使用 Python 代码构造的，直接使用`sys.stdout`即可。

```python
"stream": sys.stdout
```

但是如果配置文件是写在json内时，就得把字符串`"std.stdout"`与python对象`std.stdout`区分开来。

通过增加前缀的方式来标记出python对象，所以就引入了`ext://`。

```python
"stream": "ext://sys.stdout"
```

### loggers与root

只需要配置`level`和`handlers`。

```python
"loggers": {
    "tryceratops": {
        "level": "INFO",
        "handlers": [
            "verbose_output",
        ],
    },
},
"root": {
    "level": "INFO",
    "handlers": [
        "logfile",
    ]
}
```

loggers不一定要配置，需要配置root。

## 案例

### 最简单的logging配置

在任意文件目录下，创建`demo1.py`

```
|-example
  |-demo1.py
```

添加如下代码

```python
import logging

config = {
    "version": 1,
    "disable_existing_loggers": False, 
}

logging.config.dictConfig(config)
```



任务：使用python字典的方式配置一个最简单的logging



这里学习的是项目 [`Tryceratops 🦖✨ config`](https://github.com/guilatrova/tryceratops/blob/main/src/tryceratops/settings.py).

使用方式：创建一个`settings.py`文件，内容是日志的配置文件。

```python
ERROR_LOG_FILENAME = ".tryceratops-errors.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "tryceratops": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": "INFO", "handlers": ["logfile"]},
}
```



## 快速配置使用

在项目代码目录下创建`log.py`并填入如下内容

```python
import os
import logging
import logging.config

# PARENT_DIR -- log.py所在文件夹的父文件夹
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PARENT_DIR, "logs")

NORMAL_LOG_FILENAME = os.path.join(LOG_DIR, "output.log")
ERROR_LOG_FILENAME = os.path.join(LOG_DIR, "error.log")
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(message)s",
        },
        "default": {
            "format": "[%(asctime)s][%(levelname)s][%(name)s][%(lineno)d]:%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "normal": {
            "formatter": "default",
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": NORMAL_LOG_FILENAME,
            "backupCount": 2,  # 最多备份2个日志
            "maxBytes": 1024 * 1024,  # 日志最大为1Mb
            "encoding": "utf-8",
        },
        "error": {
            "formatter": "default",
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOG_FILENAME,
            "backupCount": 2,  # 最多备份2个日志
            "maxBytes": 1024 * 1024,  # 日志最大为1Mb
            "encoding": "utf-8",
        },
        "stream": {
            "formatter": "simple",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {},
    "root": {"level": "INFO", "handlers": ["normal", "error", "stream"]},
}


logging.config.dictConfig(LOGGING_CONFIG)

```

在程序的入口文件比如`__init__.py`导入`log`模块

```python
# import 其他包
...
# 开始import自己的包之前
from . import log
```

