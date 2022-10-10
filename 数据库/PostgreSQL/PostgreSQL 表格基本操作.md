# 表格基本操作

## 创建表

```sql
CREATE TABLE table_name(
   column1 datatype,
   column2 datatype,
   column3 datatype,
   .....
   columnN datatype,
   PRIMARY KEY( 一个或多个列 )
);
```

表名要唯一，空白表由发出此命令的用户所有。

实例

创建一个名为`COMPANY`的表

```sql
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
```

创建一个名为`DEPARTMENT`的表

```sql
CREATE TABLE DEPARTMENT(
   ID INT PRIMARY KEY      NOT NULL,
   DEPT           CHAR(50) NOT NULL,
   EMP_ID         INT      NOT NULL
);
```

## 查看表

查看数据库现存的表

```
\d
```

```
           List of relations
 Schema |    Name    | Type  |  Owner   
--------+------------+-------+----------
 public | company    | table | postgres
 public | department | table | postgres
(2 rows)
```

查看表的具体信息

```
\d company
```

```
                  Table "public.company"
 Column  |     Type      | Collation | Nullable | Default 
---------+---------------+-----------+----------+---------
 id      | integer       |           | not null | 
 name    | text          |           | not null | 
 age     | integer       |           | not null | 
 address | character(50) |           |          | 
 salary  | real          |           |          | 
Indexes:
    "company_pkey" PRIMARY KEY, btree (id)

```

## 删除表

```sql
DROP TABLE company, department;
```

删除后再使用`\d`命令来查看就找不到表格了

```sql
\d
```

```
Did not find any relations.
```

## 更新数据

```sql
UPDATE student set name='李华' where sid=1;
```

某一列包含1-3，要求映射到1-苹果、2-梨、3-香蕉

```sql
drop table if exists fruit;
create table fruit (
   num text
);

insert into fruit values ('1'), ('2'), ('2'), ('1'), ('3')

select * from fruit
```

```
1
2
2
1
3
```

修改后：

```sql
update fruit set num=(
    case num 
    when '1' then '苹果' 
    when '2' then '香蕉'
    else '其他' end)
select * from fruit
```

```
苹果
香蕉
香蕉
苹果
其他
```

