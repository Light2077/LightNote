https://docs.python.org/zh-cn/3/library/index.html

## eval()

```python
x = 10
y = 7
res = eval("x+y")
print(res)  # 17
```



其他参数

```python
x = 10
y = 7
res = eval("x+y", {'x': 1, 'y': 2})
print(res)  # 3
```

前面的字典是全局变量，后面的是局部变量

```python
x = 10
y = 7
res = eval("x+y", {'x': 1, 'y': 2}, {'y': 30, 'z': 4})
print(res)  # 31
```

## exec()

exec 的返回值永远为None

```
exec(object[globals, [locals]])
```

```python
x = 10
expr = """
z = 30
res = x + y + z
print(res)
"""

y = 20
exec(expr)  # 10 + 20 + 30
exec(expr, {'x': 1, 'y': 2})  # 1 + 2 + 30
exec(expr, {'x': 1, 'y': 2}, {'y': 3, 'z': 4})  # 1 + 3 + 4
```



