https://zhuanlan.zhihu.com/p/367875150

1、通过操作系统层的shell命令查看

```text
ps -ef |grep postgres |wc -l
```

该命令只是一个大概进程数查询，这其中包含了很多数据库自身进程（例如archive进程等），如果想要精确连接数请考虑下面两种方式。

2、通过登录数据库后查看后台连接进程

```sql
SELECT count(*) FROM pg_stat_activity;
```

3、与2同理，但是此条SQL不包含当前查询进程

```sql
SELECT count(*) FROM pg_stat_activity WHERE NOT pid=pg_backend_pid();
```

4.重置pg表的序列号

```sql
select setval('表名_id_seq',(select max(id) from 表名));
```



