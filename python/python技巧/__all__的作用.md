https://blog.csdn.net/weixin_44224529/article/details/122017414

`__all__ `的作用是在模糊导入的情况下，有些模块不必要导入或者只导入部分模块，可以指定`__all__ `的值。

例如一个模块

```python
# fruit
apple = 1
banana = 2
__all__ = ["apple"]
```

在另一个文件中

```python
from fruit import *

print(apple)  # 成功
print(banana)  # 报错
```

