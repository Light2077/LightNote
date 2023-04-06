# PostgreSQL 模式

https://www.postgresqltutorial.com/postgresql-schema/

## 创建schema

schema

模式有点类似于python中模块的概念。

一个数据库的表名只能有一个，但是有的表比较接近怎么办？

比如**市场**数据库里有许多商品，每个商品都有价格，就形成了**价格**表。但是水果店和花店都要用价格表怎么办？这时候就可以用**模式**

只要有权限，一个用户可以访问他所连接的数据库中的任意模式中的对象。

优点：

- 允许多个用户使用一个数据库而不会干扰其它用户。
- 把数据库对象组织成逻辑组，让它们更便于管理。
- 第三方的应用可以放在不同的模式中，这样它们就不会和其它对象的名字冲突。

```sql
CREATE SCHEMA fruit_shop;
CREATE SCHEMA flower_shop;
```

输出`CREATE SCHEMA`即表示成功创建模式

```
CREATE SCHEMA
```



这时候就可以创建表名相同的两个表

```sql
CREATE TABLE fruit_shop.price(
    ID INT                 NOT NULL,
    NAME VARCHAR(20)       NOT NULL,
    PRICE DECIMAL(18, 2),
    PRIMARY KEY (ID)
);

CREATE TABLE flower_shop.price(
    ID INT                 NOT NULL,
    NAME VARCHAR(20)       NOT NULL,
    PRICE DECIMAL(18, 2),
    PRIMARY KEY (ID)
);
```

但是输入`\d`没有东西显示

```
\d
```

```
Did not find any relations.
```

查看是否创建成功

```sql
SELECT * FROM fruit_shop.price;
```

```
 id | name | price 
----+------+-------
(0 rows)
```

## 查看所有的schema

```sql
SELECT nspname FROM pg_namespace; 
```

```
      nspname       
--------------------
 pg_toast
 pg_catalog
 public
 information_schema
 fruit_shop
 flower_shop
(6 rows)
```

或

```
\dnS
```

```
        List of schemas
        Name        |  Owner   
--------------------+----------
 flower_shop        | postgres
 fruit_shop         | postgres
 information_schema | postgres
 pg_catalog         | postgres
 pg_toast           | postgres
 public             | postgres
```

## 删除模式

```sql
DROP SCHEMA fruit_shop;
```

```
ERROR:  cannot drop schema fruit_shop because other objects depend on it
DETAIL:  table fruit_shop.price depends on schema fruit_shop
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

因为模式不为空，里面有表格

根据上面的提示，删除schema及其下属的所有表。

```sql
DROP SCHEMA fruit_shop CASCADE;
DROP SCHEMA flower_shop CASCADE;
```



