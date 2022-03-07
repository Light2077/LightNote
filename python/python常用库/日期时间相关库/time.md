# time

https://docs.python.org/3/library/time.html

1970-1-1 到2038年的某一天

```python
time.time()  # 当前时间的时间戳
time.strftime('%Y-%m-%d %H:%M:%S')  # 2020-12-06 19:36:28
time.strftime('%x')  # '01/10/21' 日/月/年
time.strftime('%X')  # '18:42:07'

time.asctime()  # 'Sun Aug  2 19:17:26 2020'
time.ctime()  # 'Sun Aug  2 19:17:41 2020'  输入秒数

time.sleep(2)  # 暂停两秒
```

## 使用perf_counter进行程序计时

```python
start = time.perf_counter()
# do something

end = time.perf_counter()
```

