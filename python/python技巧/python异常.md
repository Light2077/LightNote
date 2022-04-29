https://docs.python.org/3/library/sys.html?highlight=sys%20exc_info#sys.exc_info



sys库中关于异常的部分

```python
sys.excepthook(type, value, traceback)
```

在学习logging库捕获异常的方式时，了解到可以通过修改上面这个函数的方式自动将错误记录到日志内。