https://docs.python.org/3/library/typing.html

typing是辅助类型提示的库

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
def foo(a: Union[int, str]):
    pass
```

表示参数a可以是int也可以是str

## Dict的用法

```python
from typing import Dict
def foo(a: Dict[str, int]):
    pass
```

表示参数a是一个字典，它的key是str，value是int



