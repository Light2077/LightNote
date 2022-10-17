https://blog.csdn.net/weixin_42845682/article/details/107111996

[序列创建](https://www.postgresql.org/docs/9.6/sql-createsequence.html)

[序列操作](https://www.postgresql.org/docs/9.6/functions-sequence.html)

[一文全面了解PostgreSQL的序列（sequence）](https://www.modb.pro/db/407756)



### 单独创建序列

最简单的方式

```sql
CREATE SEQUENCE test_id_seq;
```



参数调整

```sql
CREATE SEQUENCE 
test_id_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START WITH 1
CACHE 1; 
```

### 创建表时主键设置为序列

会自动创建一个序列

```sql
create table test(
	id serial primary key,
	age int
)
```

### 创建表时指定使用序列

需要提前创建一个名为`test_id_seq`的序列

```sql
create table test(
	id int default nextval('test_id_seq') primary key,
	age int
)
```

### 查看所有序列

如何查看所有的SEQUENCE

```sql
SELECT c.relname FROM pg_class c WHERE c.relkind = 'S';
```

### 删除序列

```sql
drop sequence test_id_seq;
```

### 查看序列下一个值

```sql
select nextval('test_id_seq')
```

### 查看序列当前值

ps: 需要先执行一次`nextval`才能查看

```sql
select currval('test_id_seq')
```



### 重设序列当前值

```sql
select setval('test_id_seq', 1);
```

