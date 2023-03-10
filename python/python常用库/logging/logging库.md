# 日志基础

参考资料：

- [logging官方基础教程](https://docs.python.org/3.9/howto/logging.html#logging-basic-tutorial)
- [logging官方进阶教程](https://docs.python.org/zh-cn/3.9/howto/logging.html#logging-advanced-tutorial)
- [nb-log: 基于logging的国产的日志管理包](https://nb-log-doc.readthedocs.io/zh_CN/latest/articles/c1.html) 里面文档写的很亲民
- [如何跟高手一样用python记录日志](https://guicommits.com/how-to-log-in-python-like-a-pro/)：介绍logging的文章

## 日志的基本使用

```python
import logging
logging.debug("this is a debug log.")
logging.info("this is a info log.")
logging.warning("this is a warning log.")
logging.error("this is a error log.")
logging.critical("this is a critical log.")
```

默认就是这5个级别，默认只会显示WARNING及以上的信息。

```shell
WARNING:root:this is a warning log.
ERROR:root:this is a error log.
CRITICAL:root:this is a critical log.
```

## logger

基础的使用方式跟logging一样，但我发现setLevel居然没用

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug("this is a debug log.")
logger.info("this is a info log.")
logger.warning("this is a warning log.")
logger.error("this is a error log.")
logger.critical("this is a critical log.")
```

还是只显示warning以上的信息

```
WARNING:root:this is a warning log.
ERROR:root:this is a error log.
CRITICAL:root:this is a critical log.
```

要使用这种方式

```python
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

logging.debug('This is a debug message.')

```

这样做的缺点是会输出很多不想看到的DEBUG日志

## 日志的等级

是以数字来指定的，可以print下面的代码查看不同等级对应的数字。

```python
logging.DEBUG  # 10
logging.INFO  # 20 
logging.WARNING  # 30
logging.ERROR  # 40
logging.CRITICAL  # 50
```



## 记录日志到文件

默认`level=logging.WARNING`，只会输出`WARNING`及以上等级的日志

默认`filemode='a'`每次在文件最后追加日志

```python
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

DEBUG级别及以上的日志会被保存。这个是`example.log`文件内的内容

```
DEBUG:root:This message should go to the log file
INFO:root:So should this
WARNING:root:And this, too
```

## 跨模块记录日志

例子如下：

```python
# myapp.py
import logging
import mylib

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    mylib.do_something()
    logging.info('Finished')

if __name__ == '__main__':
    main()
```

```python
# mylib.py
import logging

def do_something():
    logging.info('Doing something')
```

运行myapp.py，输出

```
INFO:root:Started
INFO:root:Doing something
INFO:root:Finished
```

如果想知道日志是从哪个文件发出来的，还需要其他的高级知识[Advanced Logging Tutorial](https://docs.python.org/3.9/howto/logging.html#logging-advanced-tutorial).



## 日志可以传值

```python
import logging
logging.warning('%s before you %s', 'Look', 'leap!')
```

输出：

```
WARNING:root:Look before you leap!
```

我暂时觉得这个没什么用，直接.format()会更方便吧

## 更改显示消息的格式

更完整的信息格式参考 [LogRecord 属性](https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes)

比如函数名，文件名等等。

默认的格式是

```python
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
```



| 格式            | 说明     |
| --------------- | -------- |
| `%(levelname)s` | 警告等级 |
| `%(message)s`   | 警告信息 |
| `%(asctime)s`   | 时间     |

```python
import logging
# 这个是默认格式
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# %m %d %Y 月日年 %H % M %S 时分秒 %p 上午下午
# %H 24小时制 %I 12小时制
logging.basicConfig(
    # filename='example.log', 
    format='[%(asctime)s][%(levelname)s]:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    filemode='a'
)

logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

`example.log`

```
[2022-01-11 10:01:47][DEBUG]:root:This message should go to the log file
[2022-01-11 10:01:47][INFO]:root:So should this
[2022-01-11 10:01:47][WARNING]:root:And this, too
```



常用例子

```python
import logging
logging.basicConfig(
    # filename='example.log', 
    format='[%(asctime)s][%(levelname)s][%(name)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    filemode='a'
)
```



# 日志高级

在Python的logging模块中，主要包含下面四大金刚：

- Loggers： 记录器，暴露了应用程序代码直接使用的接口。
- Handlers：处理器，将日志记录（由记录器创建）发送到适当的目标。例如可以选择将日志像print那样输出到终端，也可以把日志输出到日志文件里。
- Filters： 过滤器，提供了更精细的附加功能，用于确定要输出的日志记录。
- Formatters： 格式化器，指定最终输出中日志记录的样式。

在命名记录器时使用的一个好习惯是在每个使用日志记录的模块中使用模块级记录器，命名如下:

```python
logger = logging.getLogger(__name__)
```



## Logger

三重任务：

- 提供了几种方法，能让应用程序在运行时记录消息
- 根据严重性和过滤器确定要处理的日志消息
- 将相关的日志消息

### 常用的配置logger的方法

[`Logger.setLevel()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.setLevel)

[`Logger.addHandler()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.addHandler)

[`Logger.removeHandler()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.removeHandler)

[`Logger.addFilter()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.addFilter)

[`Logger.removeFilter()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.removeFilter)

### 创建日志消息

配置完成后，通过[`Logger.debug()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.debug) 、 [`Logger.info()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.info) 、 [`Logger.warning()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.warning) 、 [`Logger.error()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.error) 和 [`Logger.critical()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.critical) 都创建日志记录

[`Logger.exception()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.exception) 创建与 [`Logger.error()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.error) 相似的日志信息。 不同之处是， [`Logger.exception()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.exception) 同时还记录当前的堆栈追踪。仅从异常处理程序调用此方法

[`Logger.log()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.log) 将日志级别作为显式参数。对于记录消息而言，这比使用上面列出的日志级别方便方法更加冗长，但这是自定义日志级别的方法

## [`Handler`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Handler)

Handler对象负责将适当的日志消息（基于日志消息的严重性）分派给处理程序的指定目标

标准库包含很多处理程序类型（参见 [有用的处理程序](https://docs.python.org/zh-cn/3/howto/logging.html#useful-handlers) ）；教程主要使用 [`StreamHandler`](https://docs.python.org/zh-cn/3/library/logging.handlers.html#logging.StreamHandler) 和 [`FileHandler`](https://docs.python.org/zh-cn/3/library/logging.handlers.html#logging.FileHandler) 。

- `setLevel()` 方法，就像在记录器对象中一样，指定将被分派到适当目标的最低严重性。为什么有两个 `setLevel()` 方法？记录器中设置的级别确定将传递给其处理程序的消息的严重性。每个处理程序中设置的级别确定处理程序将发送哪些消息。
- [`setFormatter()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Handler.setFormatter) 选择一个该处理程序使用的 Formatter 对象。
- [`addFilter()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Handler.addFilter) 和 [`removeFilter()`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Handler.removeFilter) 分别在处理程序上配置和取消配置过滤器对象。

## 格式化程序

格式化程序对象配置日志消息的最终顺序、结构和内容。 与 [`logging.Handler`](https://docs.python.org/zh-cn/3/library/logging.html#logging.Handler) 类不同，应用程序代码可以实例化格式化程序类，但如果应用程序需要特殊行为，则可能会对格式化程序进行子类化。构造函数有三个可选参数 —— 消息格式字符串、日期格式字符串和样式指示符。

- `logging.Formatter.__init__(fmt=None, datefmt=None, style='%')`

如果`style`是'%',格式化字符串使用`%(<dictionary key>)s`样式进行替换

# 日志操作手册

## 配置日志模块

有三种配置logging的方法：

- 创建loggers、handlers和formatters，然后使用Python的代码调用上面介绍过的配置函数。
- 创建一个logging配置文件，然后使用`fileConfig()`方法读取它。
- 创建一个配置信息字典然后将它传递给`dictConfig()`方法。

```python
#simple_logging_module.py

import logging

# 创建logger记录器
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# 创建一个控制台处理器，并将日志级别设置为debug。
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 创建formatter格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 将formatter添加到ch处理器
ch.setFormatter(formatter)

# 将ch添加到logger
logger.addHandler(ch)

# 然后就可以开始使用了！
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

下面是使用第二种方法，logging配置文件的方式：

```python
# simple_logging_config.py

import logging
import logging.config

logging.config.fileConfig('logging.conf') # 读取config文件

# 创建logger记录器
logger = logging.getLogger('simpleExample')

# 使用日志功能
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```

其中的logging.conf配置文件内容如下：

```
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
```

# 我的logging配置

```
|-logtext
    |-jiangsu
        |-nanjing.py
        |-suzhou.py
    |-taiwan
       |-taibei.py
       |-gaoxiong.py
    |-log
       |-__init__.py
       |-logging.conf
    |-main.py
```

**所有的城市文件类似于下面**

```python
# taiwan/taibei.py
import logging
logger = logging.getLogger(__name__)


def show():
    logger.info('我是台北')
```



**我的配置文件`log/logging.conf`**

```shell
[loggers]
keys=root

[handlers]
keys=consoleHandler, baseFileHandler

[formatters]
keys=baseFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler,baseFileHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=baseFormatter
args=(sys.stdout,)

[handler_baseFileHandler]
class=handlers.RotatingFileHandler
level=DEBUG
propagate=1
formatter=baseFormatter
args=('./log/base.log', 'a', 1024*100, 3, 'utf8')

[formatter_baseFormatter]
format=%(levelname)s %(asctime)s %(name)s: %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

**在log目录下的`log/__init__.py`**

```python
import logging.config

logging.config.fileConfig('log/logging.conf')  # 读取config文件
# 创建logger记录器
logger = logging.getLogger()
```

**主函数main**

注：log一定要放到最顶部

```python
import log
from jiangsu import nanjing, suzhou
from taiwan import gaoxiong, taibei
import logging
logger = logging.getLogger()

if __name__ == '__main__':
    logger.info('开始记录')
    logger.debug('测试debug')
    logger.warning('测试warning')
    logger.error('测试error')
    logger.critical('测试critical')
    nanjing.show()
    suzhou.show()
    taibei.show()
    gaoxiong.show()
```



此时运行`main.py`的话会在log文件夹下生成一个`base.log`文件

```
|-log
    |-__init__.py
    |-base.log  # 新
    |-logging.conf
```

文件内容如下

```
INFO 2020-11-30 17:27:19 root: 开始记录
DEBUG 2020-11-30 17:27:19 root: 测试debug
WARNING 2020-11-30 17:27:19 root: 测试warning
ERROR 2020-11-30 17:27:19 root: 测试error
CRITICAL 2020-11-30 17:27:19 root: 测试critical
INFO 2020-11-30 17:27:19 jiangsu.nanjing: 我是南京
INFO 2020-11-30 17:27:19 jiangsu.suzhou: 我是苏州
INFO 2020-11-30 17:27:19 taiwan.taibei: 我是台北
INFO 2020-11-30 17:27:19 taiwan.gaoxiong: 我是高雄
```



```
# handlers  处理类，可以有多个，用逗号分开
# qualname  logger名称，应用程序通过 logging.getLogger获取。对于不能获取的名称，则记录到root模块。
# propagate 是否继承父类的log信息，0:否 1:是
# [logger_simpleExample]
# level=DEBUG
# handlers=consoleHandler
# qualname=simpleExample
# propagate=0


# 日志格式
#--------------------------------------------------
# %(asctime)s       年-月-日 时-分-秒,毫秒 2013-04-26 20:10:43,745
# %(filename)s      文件名，不含目录
# %(pathname)s      目录名，完整路径
# %(funcName)s      函数名
# %(levelname)s     级别名
# %(lineno)d        行号
# %(module)s        模块名
# %(message)s       消息体
# %(name)s          日志模块名
# %(process)d       进程id
# %(processName)s   进程名
# %(thread)d        线程id
# %(threadName)s    线程名
```

# django log 配置

https://docs.djangoproject.com/en/3.1/topics/logging/

这个配置在添加filter时会报错

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'log/debug.log',
            'formatter': 'base',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'base',
        }
    },
    'formatters': {
        # 基本字体
        'base': {
            'format': '%(levelname)s %(asctime)s %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
        'propagate': True,
    },
}
```

使用`logging.conf`的方式无法配置过滤器！

在settings.py后接

```python
LOGGING_CONFIG = None

import logging.config
logging.config.dictConfig(...)
```

最终，我找到了解决方案，在log文件夹下新建`filter.py`文件

```
|-log
    |-filter.py
```

在里面这么写

通过重写record.name函数达到目的。

精确到了函数级别

```python
import logging


class UserFilter(logging.Filter):
    def filter(self, record):
        if record.name == 'demo.views' and record.funcName in {'login', 'show'}:
            return True
        else:
            return False

```

然后是`settings.py`的配置方法

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'my_filter': {
            '()': 'log.filter.UserFilter',
            # 'foo': 'demo.views.index'
        },

    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'filters': ['my_filter'],
            'class': 'logging.FileHandler',
            'filename': 'log/demo.log',
            'formatter': 'base',
            'encoding': 'utf8',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'base',
            'filters': ['my_filter']
        }
    },
    'formatters': {
        # 基本格式
        'base': {
            'format': '%(levelname)s %(asctime)s %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
        'propagate': True,
        'filters': ['my_filter']
    },
}
```



## RotatingFileHandler

日志大小到一定程度了就换下一个文件

```python
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'filters': ['my_filter'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/demo.log',
            'formatter': 'base',
            'encoding': 'utf8',
            'maxBytes': 1024 * 1024,  # 1mb
            'backupCount': 3  # 最多保留3个文件
        },


# filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False
# args=('./log/base.log', 'a', 1024*100, 3, 'utf8')
```

