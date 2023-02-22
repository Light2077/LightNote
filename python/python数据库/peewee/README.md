http://docs.peewee-orm.com/en/latest/

数据库连接

首先是数据库的连接

http://docs.peewee-orm.com/en/latest/peewee/database.html



Sqlite

```python
database = SqliteDatabase("demo.db")
```





定义模型

```python
from peewee import *

database = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = database 
        table_name = 'person'
    
    # 查询00后
    def after_00(self):
        return (Person
                .select()
                .where(Person.birthday >= '2000-01-01')
                .order_by(Person.birthday)
               )
```

由于没有定义主键，框架会自动给表添加一列整数自增的主键`id`

可以直接在模型类下面定义一些函数。



连接数据库并创建这些表一般这么操作

```python
def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])
```





各种字段类型

http://docs.peewee-orm.com/en/latest/peewee/models.html#fields

如果想自动填充创建日期字段，或指定时间

```python
import datetime

class User:
    # ...
    # 默认为创建时间
    create_time = DateTimeField(default=datetime.datetime.now)
    # 默认为指定时间
    last_login_time = DataTimeField(default=datetime.datetime(2020, 1, 1))
    # ...
```



保存数据

保存数据的两种方法

`.save()`

```python
from datetime import date
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save()
```

`.create()`

```python
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
tom = Person.create(name='tom', birthday=date(1999, 5, 5))
```

更新数据

可以直接更新

```python
grandma.name = 'Grandma L.'
grandma.save()

```

删除数据

返回的是删除数据的数量

```python
tom.delete_instance()
# Returns: 1
```

查询数据

查询单条数据

使用`Select.get()`查询一条数据

```python
grandma = Person.select().where(Person.name == 'Grandma L.').get()
```

也可以使用简化版

```python
grandma = Person.get(Person.name == 'Grandma L.')
```

遍历多条记录

```python
query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print(pet.name, pet.owner.name)
```

> 这样做会有一个[N+1](http://docs.peewee-orm.com/en/latest/peewee/relationships.html#nplusone)的问题，大概就是，因为这里的查询语句只涉及了Pet，而print中却包含了Person对象，这会导致每次print`pet.owner.name`的时候都要再查一次数据库，这就降低了数据库查询效率。

避免这种情况可以采用联合查询

```python
query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

for pet in query:
    print(pet.name, pet.owner.name)
```

查询某人的所有宠物

```python
for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    print(pet.name)
```

如果之前创建过对象，也可以这么查询

```python
for pet in Pet.select().where(Pet.owner == uncle_bob):
    print(pet.name)
```

排序

默认是升序排序

```python
for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    print(pet.name)
```

选择降序排序

```python
for person in Person.select().order_by(Person.birthday.desc()):
    print(person.name, person.birthday)
```

条件

条件的合并

```python
d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
query = (Person
         .select()
         .where((Person.birthday < d1940) | (Person.birthday > d1960)))

for person in query:
    print(person.name, person.birthday)

# prints:
# Bob 1960-01-15
# Grandma L. 1935-03-01
```

between

```python
query = (Person
         .select()
         .where(Person.birthday.between(d1940, d1960)))

for person in query:
    print(person.name, person.birthday)
```

## 聚合与Prefetch

查询某人的宠物数量

```python
for person in Person.select():
    print(person.name, person.pets.count(), 'pets')
```

同样，这里也存在N+1问题，每次统计宠物数量`person.pets.count()`时都会额外执行一次查询语句。这时可以用聚合函数解决这一问题

```python
query = (Person
         .select(Person, fn.COUNT(Pet.id).alias('pet_counts'))
         .join(Pet, JOIN.LEFT_OUTER)
         .group_by(Person)
         .order_by(Person.name))

for person in query:
    print(person.name, person.pet_count, 'pets')

```

peewee提供了一个魔法助手`fn()`，它能使用所有的SQL函数。

上面的

```
fn.COUNT(Pet.id).alias('pet_count')
```

相当于

```mysql
COUNT(pet.id) AS pet_count
```



### Prefetch

因为一个人可以有多个宠物，因此用`OUTER`连接时，会出现多个Person对象，比如

```python
query = (Person
         .select(Person, Pet)
         .join(Pet, JOIN.LEFT_OUTER)
         .order_by(Person.name, Pet.name))
for person in query:
    # We need to check if they have a pet instance attached, since not all
    # people have pets.
    if hasattr(person, 'pet'):
        print(person.name, person.pet.name)
    else:
        print(person.name, 'no pets')

# prints:
# Bob Fido
# Bob Kitty
# Grandma L. no pets
# Herb Mittens Jr
```

Bob就出现了多次。讲道理感觉是有点不合理。这时就可以使用Prefetch

```python
query = Person.select().order_by(Person.name).prefetch(Pet)
for person in query:
    print(person.name)
    for pet in person.pets:
        print('  *', pet.name)
```

这样Person只出现一次，然后宠物归类到一起

## SQL Functions

其他用法可以参考 [Querying](http://docs.peewee-orm.com/en/latest/peewee/querying.html#querying) 

```python
expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
    print(person.name)
```

## 数据库

关闭数据库

```python
database.close()
```

连接池[connection pool](http://docs.peewee-orm.com/en/latest/peewee/database.html#connection-pooling) 可以帮助降低启动成本

## 已有的数据库

对于已经建立好的数据，可以用peewee自动生成模型文件，例：

```
python -m pwiz -e postgresql charles_blog > blog_models.py
```



## 模糊查询

https://blog.csdn.net/qq_41445357/article/details/109106081

