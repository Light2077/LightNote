# Datetime

https://docs.python.org/3/library/datetime.html

主要掌握这几个函数

- datetime.date()
- datetime.datetime()
- datetime.timedelta()

四个类：

- datetime
- date
- time
- timedelta

# 常用操作

时间戳转datetime格式

```python
import datetime
dt_stamp = 1633864562
dt = datetime.datetime.fromtimestamp(dt_stamp)
print(dt)
```

```
2021-10-10 19:16:02
```

字符串转时间戳

```python
import datetime
dt_str = '2021-10-10 19:16:02'
dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
print(dt.timestamp())
# 1633864562.0
```

获取当天日期

```python
import datetime

datetime.date.today()
# datetime.date(2021, 8, 22)
```

获取当前日期和时间

```python
datetime.datetime.now()
# datetime.datetime(2021, 8, 22, 21, 48, 9, 297904)
```

创建一个日期

```python
datetime.date(2021, 8, 22)
# datetime.date(2021, 8, 22)
```

创建一个日期和时间

```python
datetime.datetime(2021, 8, 22, 12, 5, 30)
# datetime.datetime(2021, 8, 22, 12, 5, 30)
```

使用字符串创建日期和时间

```python
datetime.datetime.strptime('2021-08-22 12:05:30', '%Y-%m-%d %H:%M:%S')
# datetime.datetime(2021, 8, 22, 12, 5, 30)
```

日期时间对象转换为字符串

```python
now = datetime.datetime.now()
datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
# '2021-08-22 21:52:30'

str(now)
# '2021-08-22 23:25:32.100138'
```



`datetime.datetime`的常用属性

```python
now = datetime.datetime.now()
now.year
now.month
now.day

now.hour
now.minute
now.second
now.microsecond
```



日期时间的运算(`datetime.timedelta()`)

```python
# 创建时间戳
now = datetime.datetime.now()
d = datetime.timedelta(days=1, 
                       seconds=10, 
                       microseconds=239, 
                       milliseconds=233, 
                       minutes=10,
                       hours=19, 
                       weeks=1)
# 时间戳运算
print(now + d)
# 2021-08-31 17:57:22.920383
```



时间戳

```python
# 北京时间1970年01月01日08时00分00秒 到现在经过的秒数
datetime.datetime.timestamp(now)
```

## 相减操作

```python
import datetime

t1 = datetime.datetime(2021, 6, 1)
t2 = datetime.datetime(2020, 1, 12, 10, 30, 5)
t2 - t1
```







