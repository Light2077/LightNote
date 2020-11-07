



```python
import datetime

# 获取当前日期和时间
now = datetime.datetime.now()

# 自己创建一个日期时间
dt1 = datetime.datetime.strptime('2010-10-10 18:23:45', '%Y-%m-%d %H:%M:%S')
dt2 = datetime.datetime(2020, 10, 10, 12, 25, 30)

# 日期时间对象转换为字符串
now = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')

# 了解日期时间对象
# type(now)  # datetime.datetime
```



`datetime.datetime`的常用属性

```python

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

d = datetime.timedelta(days=1, 
                       seconds=10, 
                       microseconds=239, 
                       milliseconds=233, 
                       minutes=10,
                       hours=19, 
                       weeks=1)
# 时间戳运算
print(now + d)
```



时间戳

```python
# 北京时间1970年01月01日08时00分00秒 到现在经过的秒数
datetime.datetime.timestamp(now)
```





