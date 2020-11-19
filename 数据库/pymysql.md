# 连接

**不连数据库**

```python
localhost = '172.16.1.127'
username = 'root'
password = 'root'
db = pymysql.connect(localhost, username, password, charset="utf8")
```

获取一个游标

```python
cursor = db.cursor()
cursor.execute('SHOW DATABASES')  # return 4 表示有4个数据库

# db.close()  # 数据库关闭了也能用 cursor.fetchall()
one_database = cursor.fetchone()

# ('table1', )
databases = cursor.fetchall()

"""
(('table2',),
 ('table3',)
 ('table4',),)
"""
```



**连数据库**

```python

```

# 创建数据库



```python
localhost = '172.16.1.127'
username = 'root'
password = 'root'
db = pymysql.connect(localhost, username, password, charset="utf8")
cursor = db.cursor()
new_database_name = 'ztn'  # 新数据库名称

# 如果存在这个数据库就先删除
cursor.execute('DROP DATABASE IF EXISTS `%s`' % new_database_name)
# 创建新的数据库
cursor.execute('CREATE DATABASE `%s` charset=utf8' % new_database_name)


```

# 创建数据库表

```python
localhost = '172.16.1.127'
username = 'root'
password = 'root'
database = 'ztn'
db = pymysql.connect(localhost, username, password, database, charset="utf8")
cursor = db.cursor()

table = 'student'
# 如果存在这个表就先删除
cursor.execute('DROP TABLE IF EXISTS `{}`'.format(table))

sql = """CREATE TABLE `{}` (
         id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
         name CHAR(20) NOT NULL,
         age INT NOT NULL)
         CHARSET=utf8
      """.format(table)
cursor.execute(sql)

db.close()
```



# 插入数据

给定一个字典，插入数据

```python
localhost = '172.16.1.127'
username = 'root'
password = 'root'
database = 'ztn'
db = pymysql.connect(localhost, username, password, database, charset="utf8")
cursor = db.cursor()
table = 'student'

name = 'lily'
age = 16

# 注意：有字符串时，一定要加引号''
sql = """INSERT INTO {}(name, age)
         VALUES('{}', {})
      """.format(table, name, age)

try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)
```



**插入多个数据**

使用`cursor.executemany(sql, values)`

values是一个列表，列表里每个元素是元组，存着需要插入的数据。



```python
localhost = '172.16.1.127'
username = 'root'
password = 'root'
database = 'ztn'
db = pymysql.connect(localhost, username, password, database, charset="utf8")
cursor = db.cursor()
table = 'student'

# 待插入的数据
students = [('tom', 18), 
            ('alex', 21), 
            ('alice', 14), 
            ('jack', 19), 
            ('joy', 12), ]

# 注意：这里不能加引号
sql = """INSERT INTO {}(name, age) 
         VALUES(%s, %s)
      """.format(table)

try:
    # 核心在这句话
    cursor.executemany("INSERT INTO student(name, age) VALUES(%s, %s)", students)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)
```



# 数据库查询

```python
import pymysql
localhost = '172.16.1.127'
username = 'root'
password = 'root'
database = 'ztn'
table = 'student'

db = pymysql.connect(localhost, username, password, database, charset="utf8")
cursor = db.cursor()


age_limit = 18
# 选出年龄大于18的学生
sql = """SELECT * FROM {} 
         WHERE age > {}
      """.format(table, age_limit)

try:
    cursor.execute(sql)
    res = cursor.fetchall()
    # 打印结果
    for row in res:
        print(f'id:{row[0]} name:{row[1]} age:{row[2]}')
    db.commit()
except Exception as e:
    db.rollback()
    print(e)
    
db.close()
```



# 数据库更新

```python
import pymysql
localhost = '172.16.1.127'
username = 'root'
password = 'root'
database = 'ztn'
table = 'student'

db = pymysql.connect(localhost, username, password, database, charset="utf8")
cursor = db.cursor()

# SQL 更新语句
sql = "UPDATE student SET age = age + 1"

try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
    
except Exception as e:
    db.rollback()
    print(e)
# 关闭数据库连接
db.close()
```



# 删除

```python
import pymysql
localhost = '172.16.1.127'
username = 'root'
password = 'root'
database = 'ztn'
table = 'student'

db = pymysql.connect(localhost, username, password, database, charset="utf8")
cursor = db.cursor()

# SQL 删除语句
sql = "DELETE FROM student WHERE age > %s" % (20)
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交修改
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()

# 关闭连接
db.close()
```

