首先我知道一个类代表一张表，然后用这个类实例化生成的实例就代表一条数据。

要做的事：创建类，建表。

然后增删改查数据。



在开始应用SQLAlchemy之前，首先要创建一个[Engine](https://docs.sqlalchemy.org/en/14/core/future.html#sqlalchemy.future.Engine)对象。

> 暂时把这个东西理解为类似于pymysql中的 conn

在内存中建立一个数据库并连接

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
```

与MySQL数据连接

https://docs.sqlalchemy.org/en/14/core/engines.html#mysql

```python
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/mydb')
```

需要安装

```
pip install pymysql
```



每次想要执行操作时

```python
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.commit()  # 提交操作
```

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
