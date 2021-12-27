## namedtuple

https://www.runoob.com/note/25726

**具名元组**：主要是给元组内的数据命名的，不然元组的含义不清楚.

可以应用在函数返回值中（`scipy.stats.linregress()`）如果一个函数返回值比较多，用默认方式返回容易记不清返回值的含义。

**基本用法**

```python
from collections import namedtuple

Student = namedtuple('Student', ['name', 'age', 'score'])
student = Student('ana', 18, 97)
print(student)
# Student(name='ana', age=18, score=97)
```

**用在函数返回值中**

```python
from collections import namedtuple

Student = namedtuple('Student', ['name', 'age', 'score'])

def select_student():
    return Student('ana', 18, 97)

student = select_student()
print(student)
# Student(name='ana', age=18, score=97)

# 也可以直接解包
name, age, score = select_student()
print(name, age, score)
# ana 18 97
```

