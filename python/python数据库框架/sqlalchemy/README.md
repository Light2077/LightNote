[SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/14/tutorial/index.html)

学习目标：

- 了解sqlalchemy的基本搭建方式
- 数据库增删改查的使用
- 如何保证事务
- 测试环境搭建

目前，SQLAlchemy由**Core**和**ORM**两部分组成，我理解为这是一种解耦，比如[gino](https://python-gino.org/docs/zh/1.0/)库就只用了SQLAlchemy的Core部分。

**SQLAlchemy Core**是基础结构，负责：

- 管理与连接数据库
- 构造数据库查询语句
- 对查询结果的交互

**SQLAlchemy ORM**基于Core构建，并且提供了对象关系映射的功能，通过python的类映射到数据库的某张表，类代表一张表，实例代表表里的一条数据。

> 目前SQLAlchemy的语法准备更新到2.0风格，感觉主要查询语句上可能会发生一些变化。





## 数据库元数据

database metadata，似乎是想用ORM之前还得创建一个这个对象

一般对于整个应用，创建一个元数据对象就OK了。

```python
from sqlalchemy import MetaData
metadata_obj = MetaData()
```

有了MetaData就可以开始建表了。

```python
from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String)
)
```

建好后使用以下语句，提交到数据库

```python
metadata_obj.create_all(engine)
```

我觉得这个比较像过渡用的，实际中还是用以下方式

## Registry

用orm时，创建一个registry对象，这个对象包含了metadata

```python
from sqlalchemy.orm import registry
mapper_registry = registry()
# mapper_registry.metadata
```

然后创建一个基类

```python
Base = mapper_registry.generate_base()
```

创建数据库映射类

```python
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

使用下面的语句可以查看表对象

```python
User.__table__
```

创建实例

```python
sandy = User(name="sandy", fullname="Sandy Cheeks")
```

创建完成后

```python
mapper_registry.metadata.create_all(engine)
```



## 列类型

https://docs.sqlalchemy.org/en/14/core/type_basics.html

# 外键约束

https://docs.sqlalchemy.org/en/14/orm/relationships.html

https://docs.sqlalchemy.org/en/14/glossary.html#term-one-to-many

## one to many



## one to one

# 其他

## 插入数据如果存在就更新

https://docs.sqlalchemy.org/en/14/dialects/mysql.html#insert-on-duplicate-key-update-upsert
