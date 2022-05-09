https://docs.python.org/3/library/typing.html

https://muzing.top/posts/84a8da1c/

typing是辅助类型提示的库

一个非常关键的优点：写了typing不会让你的代码运行得更慢

常见的类型提示

```python
def greeting(name: str) -> str:
    return "hello " + name
```

在python3.9以后，很多类型提示都不需要再从typing库import了

比如:

```python
# 3.8
from typing import List
def show(students: List[str]):
    for s in students:
        print(s)
```

而在python3.9

```python
def show(students: list[str]):
    for s in students:
        print(s)
```

这样的例子包括：

- tuple
- list
- set
- dict

## Union的用法

Union表示某个参数可以传入什么类型，比如

```python
from typing import Union
def foo(a: Union[int, None]):
    pass
```

表示参数a可以是int也可以是None

python3.10版本之后

```python
def foo(a: int | None):
    pass
```

由于一个参数是int，也可以是None的操作太常见了

一般也可以这么表示

```python
from typing import Optional
def foo(a: Optional[int]):
    pass
```



## Dict的用法

```python
from typing import Dict
def foo(a: Dict[str, int]):
    pass
```

表示参数a是一个字典，它的key是str，value是int

## Sequence

有时候不仅可能会传入list，还可能传入tuple，range(10)等类似的参数，只用List就不够了。

所以使用`Sequence`是更常用的方法

```python
from typing import Sequence

def my_sum(nums: Sequence[int]):
    ans = 0
    for n in nums:
        ans += n
    return ans
```

## mypy

可以在命令行中执行：

```
mypy demo.py
```

进行静态类型检查

也可以在vscode中激活相关插件

搜索`python.linting.mypy`，然后enable一下。

