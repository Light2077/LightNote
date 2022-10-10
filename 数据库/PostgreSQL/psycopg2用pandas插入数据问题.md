插入的数据有空值None，但是psycopg2中直接插入None会报错，需要转换成NULL

需要要用`cur.mogrify()`函数来转换

参考：https://blog.csdn.net/weixin_44778883/article/details/111237003

```python
import psycopg2

conn = psycopg2.connect(
    database='test', 
    user='postgres',
    password='123456', 
    host='localhost', 
    port='5432'
)

with conn.cursor() as cur:
    sql = "insert into test values(%s, %s, %s)"
    sql = cur.mogrify(sql, (None, 23, 1))
    print(sql)
    cur.execute(sql)
    conn.commit()
```

```
b'insert into test values(NULL, 23, 1)'
```



对比了以下3种写入数据库的方式

https://blog.csdn.net/weixin_44731100/article/details/102677927

- insert
- pandas.DataFrame.to_sql
- copy_from



解决None不显示的问题

https://www.geeksforgeeks.org/python-psycopg2-insert-multiple-rows-with-one-query/

NaN 替换为 None

https://blog.csdn.net/m0_64336020/article/details/123197144