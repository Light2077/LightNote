在 Python 的 functools 模块中，partial() 函数可以将函数和部分参数组合成一个新函数，这个新函数可以使用原始函数的部分参数，而不需要每次都指定。

这个函数在函数调用链中特别有用，因为可以减少手动传递参数的次数。

```python
from functools import partial

def foo(a, b, c):
    print(a, b, c)

new_foo = partial(foo, b=2, c=3)
new_foo(1)  # 输出 1 2 3
```

