https://docs.python.org/zh-cn/3/library/unittest.html

命令行运行

```
python -m unittest tests/test_something.py
```



异步测试

https://docs.aiohttp.org/en/stable/testing.html

```python
from unittest import IsolatedAsyncioTestCase
events = []
class Test(IsolatedAsyncioTestCase):
    def setUp(self):
        events.append("setUp")

    async def asyncSetUp(self):
        self._async_connection = await AsyncConnection()
        events.append("asyncSetUp")

    async def test_response(self):
        events.append("test_response")
        response = await self._async_connection.get("https://example.com")
        self.assertEqual(response.status_code, 200)
        self.addAsyncCleanup(self.on_cleanup)

    def tearDown(self):
        events.append("tearDown")

    async def asyncTearDown(self):
        await self._async_connection.close()
        events.append("asyncTearDown")

    async def on_cleanup(self):
        events.append("cleanup")
```

## 单元测试使用示例

参考视频：https://www.bilibili.com/video/BV1sZ4y1i7nQ

### 初始化

首先创建一个项目结构

```
├── example
  ├── vector
  │ ├── __init__.py
  │ └── vector.py
  └── test
    ├── __init__.py
    └── test_vector.py
```

在`vector/__init__.py`中

```python
from .vector import Vector
```

在`vector.py`中

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y)
    def mul(self, factor):
        return Vector(self.x * other.x,
                      self.y * other.y)
    def dot(self, factor):
        return self.x * other.x + self.y * other.y
    
    def norm(self):
        return (self.x * self.x + self.y * self.y) ** 0.5
```

`test_vector.py`中

```python
import unittest
from vector import Vector

class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector(1, 2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
```

直接在`example`目录下执行

```
python -m unittest
```

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

### 什么是测试

上面的案例就是一个测试，测试的目的是看看你写的代码输出的结果跟你预想的是否一致。

unittest的代码编写规范：

- 文件名需要以`test_`开头。（也有其他格式，为了减轻理解负担，建议统一只用一种格式）
- 测试类需要继承`unittest.TestCase`
- 测试类的方法需要以`test_`开头

### assert函数

unittest通过一系列内置的assert函数帮助判断测试结果。

常用的assert函数：

| 方法                                                         | 检查对象               |
| ------------------------------------------------------------ | ---------------------- |
| [`assertEqual(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertEqual) | `a == b`               |
| [`assertNotEqual(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertNotEqual) | `a != b`               |
| [`assertTrue(x)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertTrue) | `bool(x) is True`      |
| [`assertFalse(x)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertFalse) | `bool(x) is False`     |
| [`assertIs(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertIs) | `a is b`               |
| [`assertIsNot(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertIsNot) | `a is not b`           |
| [`assertIsNone(x)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertIsNone) | `x is None`            |
| [`assertIsNotNone(x)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertIsNotNone) | `x is not None`        |
| [`assertIn(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertIn) | `a in b`               |
| [`assertNotIn(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertNotIn) | `a not in b `          |
| [`assertIsInstance(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertIsInstance) | `isinstance(a, b)`     |
| [`assertNotIsInstance(a, b)`](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertNotIsInstance) | `not isinstance(a, b)` |

>  assertEqual与assertTrue的区别

将`test_vector.py`内容改为

```python
class TestVector(unittest.TestCase):
    def test_assert_equal(self):
        v = Vector(1, 2)
        self.assertEqual(v.x, 0)
    def test_assert_true(self):
        v = Vector(1, 2)
        self.assertTrue(v.x == 0)
```

再次运行

```
python -m unittest
```

```
# test_assert_equal
AssertionError: 1 != 0

# test_assert_true
AssertionError: False is not true
```

两个测试都报错了，但使用`assertEqual`时，能得知`v.x`是1，不等于0。而使用`assertTrue`只能知道表达式不为`True`，缺少了`v.x`的值的信息。

### 测试不成功的情况

修改`vector.py`

```python
class Vector:
    def __init__(self, x, y):
        if isinstance(x, (int, float)) and \
           isinstance(y, (int, float)):
            self.x = x
            self.y = y
        else:
            raise ValueError("not a number")
    # ...
```

如果初始化Vector时，传入的x或y不是数字，就应该报错。

修改`test_vector.py`

```python
class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector(1, 2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        
        with self.assertRaises(ValueError):
            v = Vector("1", "2")
```

### setUp和tearDown

在运行**每个method**之前或之后做一些事

```python
class TestVector(unittest.TestCase):
    def setUp(self):
        print("start")
    def tearDown(self):
        print("end")
    # ...
```

### setUpClass和tearDownClass

在测试前、测试后做一些事情

```python
class TestVector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("start")
    @classmethod
    def tearDownClass(cls):
        print("end")
```

### skipIf

测试在某些情况下不运行，比如某些特定的python版本不运行，系统是windows时不运行。

```python
class TestVector(unittest.TestCase):
    # ...
    
    @unittest.skipIf(sys.platform == "win32", 
                     "Do not support Windows")
    def test_add(self):
        v1 = Vector(1, 2)
        v2 = Vector(2, 3)
        v3 = v1.add(v2)
        self.assertEqual(v3.x, 3)
```

限制python版本的情况

```python
@unittest.skipIf(sys.version_info < (3, 7),
                 "only supprt 3.7+")
```

### 测试方案

可以通过传入不同参数，控制测试的范围

```python
python -m unittest tests.test_vector.TestVector.test_add
```

上面演示了一个执行到最底层的测试。

可以放宽测试范围再看看测试结果。
