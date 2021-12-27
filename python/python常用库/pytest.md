https://docs.pytest.org/en/stable/

### 最简单用法

```python
# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5
```

`pytest`会运行所有当前目录下的`test_*.py`和`*_test.py`文件



### 把测试函数组织成一个类

```python
# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")
```

通过文件名运行pytest

```
pytest -q test_class.py
```

### 编写触发期望异常的断言

你可以使用`pytest.raises()`作为上下文管理器，来编写一个触发期望异常的断言：

```python
import pytest


def myfunc():
    raise ValueError("Exception 123 raised")


def test_match():
    with pytest.raises(ValueError):
        myfunc()
```

如果触发了异常，则测试通过