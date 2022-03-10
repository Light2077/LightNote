连接数据库

```python
conn = psycopg2.connect(
    host='127.0.0.7',
    port=5432,
    dbname="demo",
    user="root",
    password=123456
)
```

查询数据

```python
sql = "SELECT * FROM demo"
with conn.cursor() as cur:
    cur.execute(sql)
    data = cur.fetchall()
```

查看某个表的列名

```python
sql = "SELECT column_name FROM" 
      "information_schema.columns\n" \
      "WHERE table_name='demo'"

with conn.cursor() as cur:
    cur.execute(sql)
    d = cur.fetchall()
# d = datetime.datetime.fromtimestamp(d[0][0])
print(d)
```

```
[('column_name1', ), ('column_name2', ), ...]
```

查看数据库的所有表

```python
sql = "SELECT table_name FROM information_schema.tables" \
      "\nWHERE table_schema = 'public'"

with conn.cursor() as cur:
    cur.execute(sql)
    d = cur.fetchall()
# d = datetime.datetime.fromtimestamp(d[0][0])
print(d)
```

```
[('table_name1',),
 ('table_name2',),
 ...
]
```



例：批量执行

```python
import psycopg2

sql = "INSERT INTO table_name VALUES(%s, %s, %s)"
with conn.cursor() as cursor:
    cursor.executemany(sql, values)
    result = cursor.fetchall()
    print(result)
    conn.commit()
```

