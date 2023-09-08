[python教程：mixin详解 (taodudu.cc)](http://www.taodudu.cc/news/show-563191.html)

Mixin类似Unity中的接口

直接上例子

```python
import json

class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        return cls(**json.loads(json_str))

# 使用 Mixin 的类
class Person(JsonMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 使用示例
p = Person("Alice", 30)
json_str = p.to_json()
print(json_str)  # 输出：{"name": "Alice", "age": 30}

new_p = Person.from_json(json_str)
print(new_p.name, new_p.age)  # 输出：Alice 30

```

特点

**单一职责**：一个 Mixin 通常会实现一组相关的功能，但不定义类的核心功能。

**可复用性**：Mixin 的方法可以在多个类中复用。

**不依赖子类实现**：Mixin 本身不依赖于子类的实现，同样，子类的核心功能通常也不依赖于 Mixin。

> **Mix-in类（混入类）**：只定义一些**方法**给子类使用，不定义自己的实例属性，也不要求调用它的`__init__`方法。Mix-in类并不是新的语法，只是一种特殊的类，只用来提供方法。
>
> 通俗的说：Mixin是给类增加了功能。你去掉JsonMixin，Person类内的方法还是可以正常工作的。