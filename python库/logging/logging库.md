# 日志logging

## 记录日志到文件

不加`filemode='w'`则每次执行会在保留之前的日志文件的前提下追加新的日志。

```python
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

## 更改显示消息的格式

更完整的信息格式参考 [LogRecord 属性](https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes)

比如函数名，文件名等等。

| 格式            | 说明     |
| --------------- | -------- |
| `%(levelname)s` | 警告等级 |
| `%(message)s`   | 警告信息 |
| `%(asctime)s`   | 时间     |

```python
# logging.basicConfig(filename='example.log', level=logging.INFO)
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p')
# %m %d %Y 月日年 %H % M %S 时分秒 %p 上午下午
# %H 24小时制 %I 12小时制
```

