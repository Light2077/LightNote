通过pandas读取数据

```python
import pandas as pd
import psycopy2

conn_params = {
    "host": "your_host",
    "port": "your_port",
    "database": "your_database",
    "user": "your_username",
    "password": "your_password"
}

# 建立连接
conn = psycopg2.connect(**conn_params)

# 构建查询语句
query = "SELECT * FROM your_table;"

# 使用pandas的read_sql函数查询数据
df = pd.read_sql(query, conn)

# 关闭连接
conn.close()

# 查看结果
print(df.head())
```

一次性读取数据

```python
df = pd.read_sql(sql, conn)
```



分批次读取数据

```python
df = []
for d in pd.read_sql(sql, conn, chunksize=100):
    df.append(d)
df = pd.concat(df)
```

