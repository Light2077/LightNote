# logging使用案例

## 如何使用





拷贝下面案例中的`log.py`的内容。在主程序`import log`。

其他程序使用日志时只需要

```python
import logging
logger = logging.getLogger(__name__)

logger.info('鸢尾花')
```



## 基础案例

用一个项目来举例

商场里有许多不同类型的商店，比如花店，水果店。花店里有不同的花，水果店里有不同的水果。

需要使用日志模块来介绍这些商品

创建项目目录如下

```
|-market
  |-flower
    |-iris.py
    |-violet.py
  |-fruit
    |-apply.py
    |-orange.py
  |-log.py
  |-main.py
```

编写`log.py`内容，实现既将日志信息输出到终端，又将日志信息输出到日志的功能，且最大日志数量不超过5个。

```python
import logging

# 创建logger记录器
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 文件处理器，保存日志到文件
file_handler = logging.FileHandler('tmp.log', encoding='utf8')
file_handler.setLevel(logging.DEBUG)

# 输出日志到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# 显示格式
formatter = logging.Formatter(
    fmt="[%(asctime)s][%(levelname)s][%(name)s]:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.debug('日志初始化完毕')
```

> 注意
>
> 创建logger对象时，不要传入`__name__`参数，这样会导致无法正确输出日志。
>
> - `logger = logging.getLogger(__name__)` :x:
> - `logger = logging.getLogger()`:heavy_check_mark:





商品py文件的内容为

`./flower/iris.py`

```python
import logging
logger = logging.getLogger(__name__)

def show():
    logger.info('鸢尾花')
```

`./flower/violet.py`

```python
import logging
logger = logging.getLogger(__name__)

def show():
    logger.info('紫罗兰')
```

`./fruit/apple.py`

```python
import logging
logger = logging.getLogger(__name__)

def show():
    logger.info('苹果')
```

`./fruit/orange.py`

```python
import logging
logger = logging.getLogger(__name__)

def show():
    logger.info('橘子')
```

`main.py`

```python
import log

from flower import iris, violet
from fruit import apple, orange

if __name__ == "__main__":
    iris.show()
    violet.show()
    apple.show()
    orange.show()
```

在market目录下打开终端，输入

```
python main.py
```

得到终端输出的结果

```
[2022-01-11 11:14:40][DEBUG][root]:日志初始化完毕
[2022-01-11 11:14:40][INFO][flower.iris]:鸢尾花
[2022-01-11 11:14:40][INFO][flower.violet]:紫罗兰
[2022-01-11 11:14:40][INFO][fruit.apple]:苹果
[2022-01-11 11:14:40][INFO][fruit.orange]:橘子
```

`tmp.log`文件里的结果同上

## 滚动日志

- 将日志保存在日志文件夹内
- 限制单个日志的文件大小，日志文件大小达到一定量级时，重新在一个新的文件中记录
- 日志文件的数量也需要限制，文件数量达到一定量级时，删掉最早的日志

https://docs.python.org/zh-cn/3/howto/logging-cookbook.html#using-file-rotation

将之前的`log.py`文件替换成如下代码

```python
import os
import logging
import logging.handlers

# 创建logger记录器
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 日志模块配置文件
LOG_DIR = os.path.join(BASE_PATH, 'logs')
LOG_FILE_PATH = os.path.join(LOG_DIR, 'output.log')

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
    
# 文件处理器，保存日志到文件
file_handler = logging.handlers.RotatingFileHandler(
    filename=LOG_FILE_PATH, 
    maxBytes=1024 * 1024,  # 日志最大为1Mb
    backupCount=2,  # 最多备份2个日志
    encoding='utf8'
)

file_handler.setLevel(logging.INFO)

# 输出日志到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# 显示格式
formatter = logging.Formatter(
    fmt="[%(asctime)s][%(levelname)s][%(name)s]:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.debug('日志初始化完毕')

```



生成日志形式会是

```
./logs/mylog.log
./logs/mylog.log.1
./logs/mylog.log.2
```

最新的文件始终是`mylog.log`。每次到达大小限制时，都会使用后缀``.1``重命名。每个现有的备份文件都会被重命名并增加其后缀（例如``.1`` 变为``.2``），而``.3``文件会被删除掉。

- `maxBytes`参数设置成了10字节，如果一行超过10字节，也会完整记录一行

























