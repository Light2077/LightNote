```python
import datetime

datetime.date.today()
# datetime.date(2023, 2, 22)
```

只能获得当天的日期

想获得今天的日期的时间戳

```python
today = datetime.date.today()
today_timestamp = datetime.datetime.strptime(str(today), '%Y-%m-%d').timestamp()
print(today_timestamp)
# 1676995200.0
```

