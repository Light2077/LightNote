创建连接

```python
import sqlite3

conn = sqlite3.connect(database='test.db')
conn.close()
```

如果存在`test.db`则直接连接，若不存在则创建后连接。

建表语句

```python
sql = """
CREATE TABLE student(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
age INT NOT NULL,
gender CHAR(10) NOT NULL
);
"""
cursor.execute(sql)
```

插入数据

```python
sql = """
INSERT INTO student(name, age, gender) 
values 
("tom", 18, "male"),
("lily", 19, "female"),
("jack", 20, "male");
"""
cursor.execute(sql)
conn.commit()
```

查看数据

```python
sql = "select * from student"
res = cursor.execute(sql)
res.fetchall()
```

```
[(1, 'tom', 18, 'male'),
 (2, 'lily', 19, 'female'),
 (3, 'jack', 20, 'male')]
```



