

普通的创建对象的方法：

```python
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print('I am __init__')

u = User('zs', '123456')
print(u)
"""
I am __init__
<__main__.User object at 0x00000270696B8970>
"""
```

new方法的使用

由于没有给`__new__`设置返回值，对象并没有被调用

```python
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print('I am __init__')

    # 该方法必须返回当前类的对象
    def __new__(cls, *args, **kwargs):
        print('I am __new__')


u = User('zs', '123456')
print(u)
"""
I am __new__
None
"""
```

正确使用



```python
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print('I am __init__')

    # 该方法必须返回当前类的对象
    def __new__(cls, *args, **kwargs):
        print('I am __new__')
        return object.__new__(cls)
	

u = User('zs', '123456')
print(u)
"""
I am __new__
I am __init__
<__main__.User object at 0x0000015214258B80>
"""
```

总结：

- 先调用`__init__`再调用`__new__`。
- `__new__`至少要有一个参数cls，代表要实例化的类。
- **new方法必须要有返回值**，可以返回父类的`__new__`，也可以返回`object.__new__(cls)`
- 类是制造商，`__new__`方法是原材料购买环节，`__init__`就是在原材料的基础上，加工，初始化商品环节。

