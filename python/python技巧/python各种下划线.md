## 单下划线

一般用来标记这个变量不关键

比如下面这个函数只是想打印10个hello，就不需要用一个变量存遍历的次数了。

```python
for _ in range(10):
    print('hello')
```

还有一种是`_`可以自动记录上一次表达式的结果

```python
>>> 5 + 8
13
>>> _ + 2
15
```

对于大数字的表达可以用下划线分隔

```python
9_000_000_000
```

## 前后双下划线

魔法函数，一般是python内置的函数，命名时不要起这种名字

```python
__str__
__init__
```

## 单前下划线

在一个模块里定义单前下划线的变量

一般表示仅用于模块内部的变量

在另一个模块导入前一个模块时，这个变量用不了

```python
_a = 4
a = 5
```

```python
from my import *
print(a) # ok
print(_a) # not ok
```

## 后单下划线

用来与python内置变量名区分开

```python
class_ = 2
type_ = 4
```

## 双前下划线

表示该变量仅用在类内部

```python
import Person:
    def __init__(self):
        self.name = 'dad'
        self.__age = 33
        
dad = Person()
print(boy.name)
print(boy.__age)  # not ok
```

实际上，python会把这个属性变成

```python
boy._Person__age
```

这样，在子类就不会重写了

```python
import Son(Person):
    def __init__(self):
        self.name = 'son'
        self.__age = 7
        
son = Son()
print('_Person__age:', son._Person__age)
print('_Son__age:', son._Son__age)
```

