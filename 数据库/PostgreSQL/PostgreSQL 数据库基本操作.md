# 数据库操作

## 创建数据库

```sql
CREATE DATABASE demo;
```

## 查看数据库

```sql
\l
```

```
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 demo      | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(4 rows)

```



## 选择数据库

语法格式`\c` + 数据库名

```sql
\c demo
```

```
You are now connected to database "demo" as user "postgres".
demo=# 
```

也可以在命令行使用如下代码直接进入某个数据库

```
psql -h localhost -p 5432 -U postgres demo
```

## 删除数据库

### DROP DATABASE

```SQL
DROP DATABASE [ IF EXISTS ] database_name;
```

首先要切换到其他数据库

```
\c postgres
```

删除数据库

```
DROP DATABASE demo;
```



### dropdb

dropdb 是 DROP DATABASE 的包装器。

dropdb 用于删除 PostgreSQL 数据库。

dropdb 命令只能由超级管理员或数据库拥有者执行。

dropdb 命令语法格式如下：

```
dropdb -h localhost -p 5432 -U postgres demo
```

