python中的等号赋值就是内存的赋值

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```



`s1 = Student('Lily', 18)`

创建实例的流程：

- 调用`__new__`方法，申请一段内存空间
- 调用`__init__`方法，并让`self`指向申请好的那段内存空间。
- 变量s1也指向申请好的内存空间



动态属性，意思python是可以给对象新增属性。可以用`__slots__`来限定类能拥有的属性。

```python
class Student:
    # 这个属性直接定义在类内，是一个元组，用来规定对象可以拥有的属性
    __slots__ = ('name', 'age')
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

# 魔术方法

`__del__`

`__str__`

`__repl__`

`__call__`

``` python
class Student:
    # 这个属性直接定义在类内，是一个元组，用来规定对象可以拥有的属性
    __slots__ = ('name', 'age')
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __del__(self):
        # 对象被销毁时自动调用该方法
        print('调用__del__')
    
    def __repl__(self):
        return 'student ' + self.name
    
    def __str__(self):
        # 直接打印对象，打印的是<__name__.类型, 内存地址>
        return 'student name {} age {}'.format(self.name, self.age)
    
    def __call__(self):
        print('hi im %s' % self.name)
        
s = Student('Lily', 16)
# 会调用该对象的 __str__ 或 __repr__ 方法
# 都定义则执行 __str__
print(s)

print(repr(s))  # 就调用 __repr__

# datetime里面就有两个的区别
# x = datetime.datetime.now()
# print(x)
# print(repr(x))
s()

```

`__eq__`

```python
nums1 = [1, 2, 3]
nums2 = [1, 2, 3]

# is 是身份运算符，可以用来判断两个对象是否是同一个对于，根据内存地址
print(nums1 is nums2)  # False
print(nums1 == nums2)  # True调用了list类的__eq__方法


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        # 如果不重写，默认使用内存地址比较。
        return self.name == other.name and self.age == other.age
    
    def __ne__(self, other):
        # != 本质调用 __ne__ 方法，或 __eq__ 方法结果取反
        pass
    
    def __gt__(self, other):
        return self.age > other.age
    
    def __ge__(self, other):
        return self.age >= other.age
    
    def __lt__(self, other):
        return self.age < other.age
    
    def __le__(self, other):
        return self.age <= other.age
    
    def __add__(self, other):
        return self.age + other.age
    
    def __sub__(self, other):
        return self.age - other
    
    def __mul__(self, other):
        return self.age * other

    def __truediv__(self, other):
        return self.age / other
    
    def __mod__(self, other):
        return self.age % other
    
    def __pow__(self, other):
        return self.age ** other
    
    def __int__(self):
        return self.age
    
```

# 内部属性

包括变量和方法，方法也可以看做是个属性

```python
class Student:
    """
    This is a Student class
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def study(self):
        print('%s 正在学习' % self.name)

s = Student('Lily', 18)
print(dir(s))

print(s.__class__)

print(s.__dict__)  # 属性转为字典
  
print(s.__doc__)  # 查看帮助文档
# print(Student.__doc__)

print(s.__module__)  # 查看模块名


```

# 把对象当做字典使用

```python
class Student:
    """
    This is a Student class
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __setitem__(self, key, value):
        # obj[key] = value 会调用对象的 __setitem__ 方法
        self.__dict__[key] = value

    def __getitem__(self, key):
        # obj[key] 会调用对象的 __getitem__ 方法
        return self.__dict__[key]

s = Student('Lily', 18)
print(s.age)
s['age'] = 20
print(s['age'])

```

# 实例属性和对象属性

之前提到的`name`和`age`就是对象属性

类属性在`__init__`函数之外定义，且只单独存在一份。

对象可以查看类属性，但是不能修改

```python
class Student:
    """
    This is a Student class
    """
    school = 'high school'
    def __init__(self, name, age):
        self.name = name
        self.age = age

s = Student('Lily', 14)
print(s.school)
s.school = 'colledge'
print(s.school, print(Student.school))
```

# 私有属性和私有方法

以双下划线开头的就是私有属性和私有方法。

```python
class Student:
    """
    This is a Student class
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__money = 200  # 私有变量
	
    def get_money(self):
        # 接口函数
        return self.__money
    
    def __test(self):
        # 外部无法调用__test
        print('我是私有函数')
s = Student('Lily', 14)

# print(s.__money)  # 报错
# print(s._Student__money)  # 可以强行获取

# print(s.__test())  # 报错
# print(s._Student__test())  # 可以强行调用
```

# 类方法和静态方法

- 如果一个方法里么有用到实例对象的任何属性，可以将这个方法设成**静态方法**。
- 如果这个函数只用到类变量，可以使用**类方法**

```python
class Student:
    """
    This is a Student class
    """
    school = 'shanghai-1'
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    # 这个函数是存在类对象的地址里的
    def study(self):
        print('%s is studying' % self.name)
    
    @staticmethod
    def demo():
        # 如果一个方法里么有用到实例对象的任何属性，可以将这个方法设成静态方法。
        # 静态方法不需要实例对象
        print('hello')
        
    @classmethod
    def transfer(cls, new_school):
        # 如果这个函数只用到类变量
        cls.school = new_school
        
s1 = Student('Lily', 14)
s2 = Student('Alex', 15)
# s1 和 s2 调用 study函数时

# Student.study(p1)  # 用类对象来调用方法
# Student.demo()

s1.transfer('beijing-2')
# Student.transfer('beijing-2')
print(Student.school)
```

# 单例设计模式

![](./img/单例.jpg)



只能创建一个实例，不管怎么创建都是一个实例

```python
class Singleton:
    __instance = None  # 类属性
    __is_first = True
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__is_first = False
        return cls.__instance
    
    def __init__(self, a):
        if self.__is_first:
       	    self.a = a
s1 = Singleton('hello')
s2 = Singleton('hi')
print(s1 is s2)
# 如果不重写 __new__ 方法会调用object的 __new__ 方法
# object的 __new__ 方法会申请内存

```

# 一种奇妙的实例化方法

```python
class Student:
    """
    This is a Student class
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age

s = object.__new__(Student)
s.__init__('lily', 20)

print(s.name, s.age)
```

# 继承

```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def eat(self):
        print(self.name, 'is eating')
        
class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)
    
    def bark(self):
        print(self.name, 'is barking')

class Cat(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)
    
    def catch(self):
        print(self.name, 'is catching')

dog = Dog('wang', 2)
cat = Cat('hello', 3)

dog.eat()
dog.bark()

cat.eat()
cat.catch()
```

## 多继承

了解重名函数的继承顺序

```python
class A:
	def foo():
        print('A 的 foo')

class B:
    pass
        
class C(A):
    pass
        
class D(B):
    def foo():
        print('D 的 foo')

"""
A(foo) -> C -\
             CD
B -> D(foo) -/
"""
class CD(C, D):
    pass

# 可以查看方法的调用顺序
# 深度优先。
print(CD.__mro__)  # C -> A -> D -> B
CD.foo()  # A 的 foo
```

## 私有属性的继承特点

- 父类的私有方法（属性）子类没有

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__money = 100
    def __demo(self):
        print("i m person's demo")
    
class Student(Person):
    pass

s = Student('Lily', 10)

# 报错
# print(s.__money)
# s.__demo()
# print(s._Student__money)

# 强行调用
print(s._Person__money) 
s._Person__demo()

```

## 新式类和经典类

```python
class A(object):
	pass

class A:
    # 默认继承object
	pass

# 新式类：继承自 object 的类
# 经典类：不继承自 object 的类(里面会少很多魔术方法)
# 在 python2 中，如果不手动指定一个类的父类是 object 这个类就是一个经典类。

# python3 不存在这种问题
# 但是为了兼容性还是带上 (object) 比较好
```

## is与isinstance的使用

- is 是身份运算符，本质是id(p1) == id(p2)
-  isinstance 对于父类也会输出True

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    pass

p1 = Person('Lily', 14)
p2 = Person('Lily', 14)
s = Student('Jack', 21)
# is 是身份运算符，本质是id(p1) == id(p2)
print(p1 is p2)

if type(s) == Student:
    print('p1 是Student类创建的实例对象')
    
if type(s) == Person:
    print('s 是Person类创建的实例对象')
    # 这句不会被执行
# isinstance 对于父类也会输出True
if isinstance(s, Student):
    print('p1 是Student类创建的实例对象')
    
if isinstance(s, Person):
    print('s 是Person类创建的实例对象')

if issubclass(Student, Person):
    print('Student 是 Person 的子类')
```

# 多态

## 子类重写父类方法

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def sleep(self):
        print('%s is sleeping' % self.name)
        
class Student(Person):
    def sleep(self):
        print('{} {} is sleeping'.format('student', self.name))
        
p = Person('Lily', 10)
s = Student('Lily', 10)

p.sleep()
s.sleep()
```



## 子类在父类方法上有更多的实现

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
class Student(Person):
#    def __init__(self, name, age, score):
#        self.name = name
#        self.age = age
#        self.score = score

    # 方式1：用父类名手动调用父类的__init__函数
    # def __init__(self, name, age, score):
    #    Person.__init__(self, name, age)
    #    self.score = score
        
    # 方式2(推荐)
    def __init__(self, name, age, score):
        super().__init__(name, age)
        self.score = score
        
p = Person('Lily', 10)
s = Student('Lily', 10, 99)

p.sleep()
s.sleep()
```



多态基于继承，通过子类重写父类方法，达到不同的子类调用相同的父类方法，得到不同的结果，提高代码的灵活度。

## 强制子类必须重写父类方法

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def sleep(self):
        # 子类不重写就会报错
        raise NotImplementedError 
        
class Student(Person):
   	def sleep(self):
        print('student is sleeping')
        
s = Student('Lily', 10)
```

# 可迭代对象

比如：list/tuple/dict/set/str/range/filter/map

只要重写了`__iter__`方法就是可迭代对象

```python
from collections.abc import Iterable

class Demo1:
    pass

class Demo2:
    def __iter__(self):
        pass

d1 = Demo1()
d2 = Demo2()
names = ['hello', 'good']

# 判断是否是可迭代对象
print(isinstance(d1, Iterable))
print(isinstance(d2, Iterable))
print(isinstance(names, Iterable))

```



## 迭代器



```python
class Demo:
    def __init__(self, x):
        self.x = x
        self.count = 0
    
    def __next__(self):
        self.count += 1
        if self.count <= self.x:
            return self.count - 1
        else:
            raise StopIteration  # 让迭代器停止
        
            
    def __iter__(self):
        return self

# for in 循环的本质就是调用可迭代对象的 __iter__ 方法，获取该方法的返回值
# 返回值是一个对象，然后再调用这个对象的 __next__ 方法
# 相当于
# d = Demo(5)
# i = d.__iter__().__next__()  # 不断重复
for i in Demo(5):
    print(i)
# 也可以
i = iter(d)
print(next(i))
print(next(i))
print(next(i))
print(next(i))
print(next(i))
print(next(i))
```

使用场景

```python
class Fibonacci:
    def __init__(self, n):
        self.n = n
        self.cnt = 0
        self.prev = 1
        self.cur = 1
    def __next__(self):
        self.cnt += 1
        if self.cnt <= self.n:
            ans = self.prev
            self.cur, self.prev = self.cur + self.prev, self.cur
            return ans
        else:
            raise StopIteration  # 让迭代器停止
    def __iter__(self):
        return self
    
for i in Fibonacci(10):
    print(i)
```

思考：既然有列表了，为什么还要有生成器呢？

时间换空间

```python
nums = [1, 2, ..., 10000000]
range(1, 1000000)
```



## 生成器

生成器是特殊的迭代器

```python
g = (x ** 2 for i in range(10))
print(type(g))
```

在函数内有yield关键词的函数就是生成器

```python
class Fibonacci:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        prev = cur = 1
        for i in range(self.n):
            ans = prev
            cur, prev = cur + prev, cur
            yield ans
            
print(type(Fibonacci(10).__iter__()))
print(type(type(iter(Fibonacci(10)))))

for i in Fibonacci(10):
    print(i)
```

yield from 的使用

先把gen1和gen2都输出了，在输出gen3的yield

```python
def gen1():
    for i in range(1, 5):
        yield -i
        
def gen2():
    for i in range(1, 5):
        yield i ** 2
        
def gen3():
    yield from gen1()
    print('finish gen1')
    yield from gen2()
    print('finish gen2')
    for i in range(1, 5):
        yield i ** 3
    print('finish gen3')
g = gen3()
while True:
    print(next(g))
```

