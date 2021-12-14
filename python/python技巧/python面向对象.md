`__new__`详解

```python
class Student:
    def __new__(cls, *args, **kwargs):
        print(f'args: {args}, kwargs:{kwargs}')
        return object.__new__(cls)
    
    def __init__(self, name, age):
        print(name, age)
s = Student('tom', 19)

```



python中的等号赋值就是内存的赋值

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

`s1.__dict__`可以查看类或者对象的属性值。

`s1 = Student('Lily', 18)`

创建实例的流程：

- 调用`__new__`方法，申请一段内存空间

  ```python
  class Student:
      def __new__(cls):
          print('分配内存空间...')
          obj = object.__new__(cls)
          print(obj)
          return obj  # 如果不返回，就不会调用__init__
  ```

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

student1 = Student(name='tom', age='18')
# 报错
# student1.sex = 'male'

```

# 魔术方法

`__del__`

只有当指向对象的所有变量都被删除时，对象的空间才会被释放

```python
s1 = Student('tom', 18)
s2 = s1

del s1 
# 对象并不会被删除

del s2
# 对象被删除了。
# 现在才会执行 __del__ 方法
```



`__str__`

`__repl__`

都定义的时候，print(s)默认是`__str__`

和`__str__`的区别在于，在对象被放到列表内时，优先打印`__repl__`返回的内容。

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

## `@property` 与 `@<attr>.setter`

```python
class Student:
    """
    This is a Student class
    """
    school = 'high school'
    def __init__(self, name, age):
        self.name = name
        self.__age = age
     
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, age):
        if age < 18:
            print('未满18')
        else:
            print(f'年龄修改为{age}')
            self.__age = age
            
s = Student('lily', 19)
print(s.age)
s.age = 17  # 未满18
print(s.age)
s.age = 22  # 年龄修改为22
print(s.age)
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

![](images/单例.jpg)



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

深度优先

```
GrandFather  GrandMother
    |             |
  Father       Mother
       \       /
         Child 
```

调用顺序：Father->GrandFather->Mother->GrandMother

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

`obj.__bases`__可以查看继承自谁

## 菱形继承

广度优先，创建对象的过程

```
    Human
    /   \
Father Mother
    \   /
    Child
```

```python
class Human:
    def __init__(self):
        print('人类...')


class Father(Human):
    def __init__(self):
        print('父亲初始化...')
        super().__init__()
        print('父亲初始化结束...')
class Mother(Human):
    def __init__(self):
        print('母亲初始化...')
        super().__init__()
        print('母亲初始化结束...')

class Child(Father, Mother):
    def __init__(self):
        print('孩子初始化...')
        super().__init__()
        print('孩子初始化结束...')

print(Child.__mro__)
c = Child()

"""
孩子初始化...
父亲初始化...
母亲初始化...
人类...
母亲初始化结束...
父亲初始化结束...
孩子初始化结束...
"""
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

不一定发生继承，只要调用方法名一致，只不过方法实现的效果不同。

要想限制在某个类及其子类才能调用的话，可以使用`isinstance(obj, class)`来判断

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



## 子类在父类方法上有更多的实现super

super().func() 可以调用父类的方法，避免重写，super()可以调用任意父类的对象。

应用场景：

- 父类的方法执行了一堆操作
- 子类不想重写这些操作，只是想增加一点其他操作时

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



多继承怎么搞。

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

#  类方法和静态方法

类是有类属性的，类属性可以用self调用，也可以用类方法调用。

```python
class Dog:
    legs = 4
    def print_info(self):
        print(f'狗有{self.legs}条腿')
    
    @classmethod
    def print_class_info(cls):
        print(f'(类方法)狗有{cls.legs}条腿')
d = Dog()
d.print_info()
Dog.print_class_info()
```

通过类对象修改类属性无效，只对该对象有效。

```python
d.legs = 2
d.print_info()
Dog.print_class_info()
```



静态方法

类和对象都可以调用该方法。

```python
class Dog:
    @staticmethod
    def hello():
        print('hello')
```






