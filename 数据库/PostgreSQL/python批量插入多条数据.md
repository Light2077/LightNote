



```python
import pandas as pd
import psycopg2
conn = psycopg2.connect(
            dbname='test',
            user='root',
            password=123456,
            host='localhost',
            port=5432,
            connect_timeout=5,
        )

df = pd.DataFrame({
    'sname': ['a', 'b', 'c', 'd', 'a', 'b'],
    'idx': [1, 2, 3, 4, 1, 2]
})

sql = (
    'INSERT INTO test_student VALUES (%s, %s) '
    'ON CONFLICT("sname", "idx") '
    'DO NOTHING'
)

with conn.cursor() as cur:
    cur.executemany(sql, df.values)
    conn.commit()
```

这样会自动忽略重复数据

如果要更新

```python
df = pd.DataFrame({
    'sname': ['a', 'b', 'c', 'd'],
    'idx': [6, 7, 3, 4]
})

sql = (
    'INSERT INTO test_student VALUES (%s, %s) '
    'ON CONFLICT("sname", "idx") '
    'DO UPDATE SET '
    'idx=excluded.idx'
)


with conn.cursor() as cur:
    cur.executemany(sql, df.values)
    conn.commit()
```

