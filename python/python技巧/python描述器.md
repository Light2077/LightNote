[描述器使用指南 — Python 3.11.5 文档](https://docs.python.org/zh-cn/3/howto/descriptor.html)

官方文档学习笔记

### 简单示例

描述器在调用时，一般会通过运算得到结果。

下面的例子中使用了一个NameLength描述器

当调用`s.name_length`时，会把 s 作为参数传到 `NameLength`的 `__get__`方法内。

```python
import os

class NameLength:
    def __get__(self, obj, objtype=None):
        return len(obj.name)

class Student:
    name_length = NameLength()
    def __init__(self, name):
        self.name = name
s = Student("alice")
s.name_length
```

```
5
```

### 托管属性

在类的属性中设置描述器。

实际数据通过描述器来存储管理存储。

因为特性：调用描述器时，会把实例作为参数传给描述器的方法。

因此访问公开属性就能控制实例数据的读写。

描述器的一种流行用法是托管对实例数据的访问。描述器被分配给类字典中的公开属性，而实际数据作为私有属性存储在实例字典中。当访问公开属性时，会触发描述器的 `__get__()` 和 `__set__()` 方法。

在下面的例子中，*age* 是公开属性，*_age* 是私有属性。当访问公开属性时，描述器会记录下查找或更新的日志：

```python
import logging

logging.basicConfig(level=logging.INFO)

class LoggedAgeAccess:
    def __get__(self, obj, objtype=None):
        value = obj._age
        logging.info('Accessing %r giving %r', 'age', value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', 'age', value)
        obj._age = value

class Person:

    age = LoggedAgeAccess()             # Descriptor instance

    def __init__(self, name, age):
        self.name = name                # Regular instance attribute
        self.age = age                  # Calls __set__()

    def birthday(self):
        self.age += 1                   # Calls both __get__() and __set__()
```

```python
mary = Person('Mary M', 30) 
mary.age
mary.birthday()
```

此示例的一个主要问题是私有名称 *_age* 在类 *LoggedAgeAccess* 中是硬耦合的。这意味着每个实例只能有一个用于记录的属性，并且其名称不可更改。

### 定制名称

当一个类使用描述器时，它可以告知每个描述器使用了什么变量名。

在此示例中， `Person` 类具有两个描述器实例 *name* 和 *age*。当类 `Person` 被定义的时候，他回调了 *LoggedAccess* 中的 `__set_name__()` 来记录字段名称，让每个描述器拥有自己的 *public_name* 和 *private_name*：

```python
import logging

logging.basicConfig(level=logging.INFO)

class LoggedAccess:

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        logging.info('Accessing %r giving %r', self.public_name, value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)

class Person:

    name = LoggedAccess()                # First descriptor instance
    age = LoggedAccess()                 # Second descriptor instance

    def __init__(self, name, age):
        self.name = name                 # Calls the first descriptor
        self.age = age                   # Calls the second descriptor

    def birthday(self):
        self.age += 1
```

`__set_name__` 是一个特殊的方法，用于 Python 3.6+ 的描述器协议。当描述器被作为类属性定义的时候，这个方法会被自动调用。

这个方法在类定义完成，类对象被创建后会立即调用。

当 Python 解释器碰到一个新的类定义，它会解析类体，并逐一设置各个类属性。当一个描述器（一个定义了 `__get__` 或 `__set__` 方法的对象）被作为类属性设置时，`__set_name__` 方法会自动被调用。

- `owner`: 该参数是描述器被设置为属性的那个类。上述例子中，`owner` 就是 `Person` 类。
- `name`: 该参数是描述器在 `owner` 类里的名字。上述例子中，第一个描述器的 `name` 是 "name"，第二个是 "age"。

### 总结

描述器 descriptor 就是任何一个定义了 `__get__()`，`__set__()` 或 `__delete__()` 的对象。

描述器仅在用作类变量时起作用。放入实例时，它们将失效。

描述器的主要目的是提供一个挂钩，允许存储在类变量中的对象控制在属性查找期间发生的情况。