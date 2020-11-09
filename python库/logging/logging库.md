# 日志基础



https://docs.python.org/3.9/howto/logging.html#logging-basic-tutorial

https://docs.python.org/zh-cn/3.9/howto/logging.html#logging-advanced-tutorial

### 日志的基本使用

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

### 日志的等级

是以数字来指定的，可以print下面的代码查看不同等级对应的数字。

```python
logging.DEBUG  # 10
logging.INFO  # 20 
logging.WARNING  # 30
logging.ERROR  # 40
logging.CRITICAL  # 50
```



### 记录日志到文件

不加`filemode='w'`则每次执行会在保留之前的日志文件的前提下追加新的日志。默认只会记录`WARNING`及以上的信息。

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

### 跨模块记录日志

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



### 日志可以传值

```python
import logging
logging.warning('%s before you %s', 'Look', 'leap!')
```

输出：

```
WARNING:root:Look before you leap!
```

我暂时觉得这个没什么用，直接.format()会更方便吧

### 更改显示消息的格式

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
logging.basicConfig(filename='example.log', 
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p',
                    # level=logging.DEBUG,
                    filemode='w')

logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

`example.log`

```
11/08/2020 19:44:55 PM This message should go to the log file
11/08/2020 19:44:55 PM So should this
11/08/2020 19:44:55 PM And this, too
```



# 日志高级

在Python的logging模块中，主要包含下面四大金刚：

- Loggers： 记录器，暴露了应用程序代码直接使用的接口。
- Handlers：处理器，将日志记录（由记录器创建）发送到适当的目标。
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
logger.warn('warn message')
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

