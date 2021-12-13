[pymysql官方文档](https://pymysql.readthedocs.io/en/latest/)

https://github.com/PyMySQL/PyMySQL

- DB-API 2.0：http://www.python.org/dev/peps/pep-0249
- MySQL参考手册：http://dev.mysql.com/doc/
- MySQL客户端/服务器协议：http://dev.mysql.com/doc/internals/en/client-server-protocol.html

## 连接

### 连接时不指定数据库

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456')
```

获取一个游标对象

```python
cursor = db.cursor()
cursor.execute('SHOW DATABASES')
```

```
8
```

返回结果为8，或任意数字，表示有8条返回结果。

```python
# 获取单条结果
cursor.fetchone()
```

```
('demo',)
```

获取到了其中一条数据，表示其中一个数据库

```python
# 一次性获取全部结果
cursor.fetchall()
```

```
(('information_schema',),
 ('mysql',),
 ('oracle',),
 ('performance_schema',),
 ('sakila',),
 ('sys',),
 ('world',))
```

### 连接时指定数据库

```python
import pymysql # 导入pymysql
# 创建连接对象
connection = pymysql.connect(host="localhost",
                             user="root",
                             password="123456",
                             database="demo",
                             port=3306,
                             charset="utf8mb4")

connection.close()
```

### 使用字典类游标

```python
connection = pymysql.connect(host="localhost",
                             user="root",
                             password="123456",
                             database="demo",
                             port=3306,
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)
```

### 使用with语句

```python
with connection:
    with connection.cursor() as cursor:
        sql = 'SHOW TABLES'
        cursor.execute(sql)
    connection.commit()
    
    result = cursor.fetchone()
    print(result)
```

```
{'Tables_in_demo': 'address'}
```

注：使用with语句时，结束后会自动关闭连接，也可以单独使用cursor

```python
with connection.cursor() as cursor:
    ...
connection.commit()
connection.close()
```



### 关闭连接

```python
cursor.close()  # 关闭游标
connection.close()  # 关闭数据库连接

# 通过游标获取的结果集保存到变量result中，即使关闭数据库连接，仍然可以访问
```



## 创建数据库

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456')

with connection:
    with connection.cursor() as cursor:
        database = 'demo'  # 新数据库名称

        # 如果存在这个数据库就先删除
        cursor.execute('DROP DATABASE IF EXISTS `%s`' % database)
        # 创建新的数据库
        cursor.execute('CREATE DATABASE `%s` charset=utf8' % database)
```



## 创建数据库表

### 学生表

| 字段名 | 说明 | 类型     |
| ------ | ---- | -------- |
| id     | 主键 | INT      |
| name   | 名字 | CHAR(20) |
| age    | 年龄 | INT      |



```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')

with connection:
    with connection.cursor() as cursor:
        table = 'student'  # 新表名称

        # 如果存在这个数据库就先删除
        cursor.execute('DROP TABLE IF EXISTS `%s`' % table)

        sql = """CREATE TABLE `%s` (
                 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                 name CHAR(20) NOT NULL,
                 age INT NOT NULL)
                 CHARSET=utf8
              """ % table

        cursor.execute(sql)
        # cursor.fetchall() 返回为空
        # 查看是否成功建表
        cursor.execute('show tables;')
        print(cursor.fetchall())
        
        # (('student',),)
```

## CRUD操作

### 插入1条数据

给定一个字典，插入1条数据

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')


table = 'student'
item = ('lily', 19)
# data = [('lily', 18), ('tom', 17), ('jack', 19), ('amy', 16)]

with connection:
    with connection.cursor() as cursor:
        # 清空表
        cursor.execute('truncate table student;')
        
        # 插入一条数据
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')


table = 'student'
item = ('lily', 19)
# data = [('lily', 18), ('tom', 17), ('jack', 19), ('amy', 16)]

with connection:
    with connection.cursor() as cursor:
        # 清空表
        cursor.execute('truncate table student;')
        
        # 插入一条数据
        sql = f"insert into `{table}` (name, age) values('{item[0]}', {item[1]})"
        cursor.execute(sql)
        
        # 查看表内所有数据
        cursor.execute('select * from student')
        print(cursor.fetchall())
        cursor.execute(sql)
        
        # 查看表内所有数据
        cursor.execute('select * from student')
        print(cursor.fetchall())
```



```python
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)
```

### 插入多条数据

```python
cursor.executemany(sql, values)
```

values是一个列表，列表里每个元素是元组，存着需要插入的数据。



```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')
table = 'student'
# 待插入的数据
students = [('lily', 18),
            ('alex', 21),
            ('tom', 17),
            ('jack', 19),
            ('joy', 12),]


with connection:
    with connection.cursor() as cursor:
        # 清空表
        cursor.execute('truncate table student;')

        # 插入一条数据
        # 注意：这里不能加引号
        sql = "INSERT INTO {}(name, age) VALUES(%s, %s)".format(table)

        # 核心是这一句
        cursor.executemany(sql, students)

        # 查看表内所有数据
        cursor.execute('select * from student')
        print(cursor.fetchall())
    # 不加commit的话，前面的操作相当于没有实施
    connection.commit()

```



### 查询

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')
table = 'student'

age_limit = 18

# 选出年龄大于18的学生
with connection:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM %s WHERE age > %s" % (table, age_limit)
        cursor.execute(sql)
        print(cursor.fetchall())

```



### 更新

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')
table = 'student'

# 过了一年，年龄加一岁
with connection:
    with connection.cursor() as cursor:
        sql = "UPDATE %s SET age = age + 1" % table
        cursor.execute(sql)
        
        # 查看表内所有数据
        cursor.execute('select * from student')
        print(cursor.fetchall())
        
    # 不commit，上述语句无效
    connection.commit()

```



### 删除

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')
table = 'student'

# 删除年龄小于18的学生
with connection:
    with connection.cursor() as cursor:
        sql = "DELETE FROM %s WHERE age < %s" % (table, 18)
        cursor.execute(sql)
        
        # 查看表内所有数据
        cursor.execute('select * from student')
        print(cursor.fetchall())
        
    # 不commit，上述语句无效
    connection.commit()
```

## 回滚

核心：`connection.rollback()`

以后写的时候尽量用try except + 回滚来写

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')

with connection:
    with connection.cursor() as cursor:
        try:
            # 插入一条正常数据
            cursor.execute("INSERT INTO student Values(6, 'luna', 14)")
            
            # 插入了一条相同主键的数据，会报错
            cursor.execute("INSERT INTO student Values(6, 'lina', 24)")
            connection.commit()
        except Exception as e:
            print(e)
            print("发生了异常，自动回滚")
            connection.rollback()
            
        # 查询student表所有数据，可以发现上面相当于全部没被执行
        cursor.execute('SELECT * FROM student')
        print(cursor.fetchall())
```

如果正确执行

```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='demo',
                             charset='utf8')

with connection:
    with connection.cursor() as cursor:
        try:
            # 插入一条正常数据
            cursor.execute("INSERT INTO student Values(6, 'luna', 14)")
            # 插入一条正常数据
            cursor.execute("INSERT INTO student Values(7, 'lina', 24)")
            connection.commit()
        except Exception as e:
            print(e)
            print("发生了异常，自动回滚")
            connection.rollback()
            
            # 查询student表所有数据，可以发现上面相当于全部没被执行
            cursor.execute('SELECT * FROM student')
            print(cursor.fetchall())
```

