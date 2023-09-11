# PostgreSQL技巧汇总

## 常用函数

### 数学函数

```sql
abs() 返回绝对值
pi() 返回圆周率值
sqrt() 返回非负数的二次方根
mod(x,y) 返回x被y除（x/y）后的余数,x也可以为小数

ceil(x) 或 ceiling(x) 返回不小于x最小整数值
floor(x) 返回不大于x的最大整数值

round(x) 返回最接近于x的整数
round(x,y) 返回最接近于x的数，其值保留小数点后y位，若y为负值，则保留小数点左边y位

sign(x) x为负，零，正时返回结果依次为：-1,0,1

pow(x,y) 或 power(x,y) 返回x的y次乘方的结果值
exp(x) 返回e的x乘方后的值
log(x)	返回x的自然对数

radians(90) 将角度值90转变为弧度值1.5707...
degrees(pi()) 将弧度值转变为角度值180

sin()
asin()
cos()
acos()
tan()
atan()
cot()
```

### 字符串函数

```sql
char_length(str) 返回str包含字符的个数
length(str) 返回字符串的字节长度，使用utf8编码时，一个汉字占三个字节，一个数字或字母占一个字节。

concat(s1,s2,...,sn) 把这些字符串连接起来。当有null时忽略，当有任一二进制字符串，结果为一个二进制字符串。
concat_ws(x,s1,s2,...,sn) 第一个参数x是其他参数的分隔符。

left(s,n) 返回字符串s最左边n个字符
right(s,n) 返回字符串s最右边n个字符

lpad(s1,len,s2):返回长度len的s1字符串，若s1长于len，则截取前len个；否则，在左边填充s2至长度为len.
rpad(s1,len,s2):返回长度len的s1字符串，若s1长于len，则截取前len个；否则，在右边填充s2至长度为len.

ltrim(s): 字符串左边空格被删除
rtrim(s):字符串右边空格被删除
trim(s):字符串左右两边边空格被删除
trim(s1 from s) : 删除字符串s两端所有的子字符串s1

repeat(s,n): 返回重复n次s组成的字符串。
replace(s,s1,s2) : 使用s2替换s中的s1

substring(s,n,len):返回起始于n位置的len个字符组成的字符串
position(str1 in str): 返回子字符串str1在str中的开始位置

reverse(s): 将字符串s反转
```

### 日期时间

```sql
current_date
current_time 带时区
localtime 不带时区
current_timestamp 或 now()
localtimestamp

extract(类型 from 日期) ： 从日期中提取某类型的时间值。类型有（day,month,year,doy[一年中的第几天]，dow[一周中的星期几],quarter[几季度]）

日期和时间的运算操作：
    date'2019-09-28' + integer'10'  : '2019-10-08'
    date'2019-09-28' + interval '3 hour'  : '2019-09-28 03:00:00'
    date'2019-09-28' + time '06:00'  : '2019-09-28 06:00:00'
    date '2019-11-01' - date '2019-09-10' : 52
    50 * interval '2 second' : 00:01:40
    interval '1 hour' / integer '2' : 00:30:00 

```



## 降序排序时空值放到最后

知识点：

- PG中的空值在排序时被视为一个很大的数
- 因此默认降序排序时空值会被放到最前面
- 使用`NULLS FIRST`将空值放到最前
- 使用`NULLS LAST`将空值放到最后

```sql
SELECT name, age FROM student
ORDER BY age DESC NULLS LAST
```

案例演示

```sql
-- 创建用于演示的student表并插入数据
DROP TABLE IF EXISTS student;
CREATE TABLE student (
    name VARCHAR(10),
    age int2
);

INSERT INTO student
VALUES
	( 'Alice', 10 ),
	( 'Bob', NULL ),
	( 'Carl', 100 )
```

默认升序查询

```sql
SELECT name, age FROM student 
ORDER BY age
```

```
name	age
Alice	10
Carl	100
Bob		NULL
```

降序查询

```sql
SELECT name, age FROM student 
ORDER BY age DESC
```

```
name	age
Bob		NULL
Carl	100
Alice	10
```

可以看出，**PG中的空值在排序时被视为一个很大的数**

要想在降序排序时把空值放到最后，可以使用`NULLS LAST`

```sql
SELECT name, age FROM student
ORDER BY age DESC NULLS LAST
```

在升序排序时把空值放到最前面，可以使用`NULLS FIRST`

```sql
SELECT name, age FROM student
ORDER BY age NULLS FIRST
```

## ROW_NUMBER()

按照特定的顺序编号，实际效果等同于新增了一列编号列。

语法：

```SQL
ROW_NUMBER() OVER( [ PARTITION BY col1] ORDER BY col2[ DESC ] ) 
```

- `PARTITION`：按照某一列分组
- `ORDER BY`：按照某一列排序

最简单的案例介绍：

按照score(分数)排序编号。

```sql
SELECT
  row_number() over(ORDER BY score DESC) rn
FROM student_score
```

按照course(学科)分组，score分数排序编号。

```sql
SELECT
  row_number() over(PARTITION course ORDER BY score DESC) rn
FROM student_score
```



案例：学生表成绩排序

```sql
DROP TABLE IF EXISTS student_score;
CREATE TABLE student_score(
    id int,
    name text, 
    course text, 
    score numeric
);
INSERT INTO student_score VALUES
(1,'周润发','数学',91.5),  
(2,'周润发','语文',89.5),  
(3,'周润发','英语',79.5),  
(4,'周润发','物理',84.5),  
(5,'周润发','化学',98.5),  
(6,'刘德华','数学',89.5),  
(7,'刘德华','语文',99.5),  
(8,'刘德华','英语',79.5),  
(9,'刘德华','物理',89.5),  
(10,'刘德华','化学',69.5),  
(11,'张学友','数学',89.5),  
(12,'张学友','语文',91.5),  
(13,'张学友','英语',92.5),  
(14,'张学友','物理',93.5),  
(15,'张学友','化学',94.5);  
```

### 1.按分数排名

```sql
SELECT
  *,
  row_number() over(ORDER BY score DESC) rn
FROM student_score
```

```
 id | name  | course | score | rn
----+--------+--------+-------+----
  7 | 刘德华 | 语文   |  99.5 |  1
  5 | 周润发 | 化学   |  98.5 |  2
 15 | 张学友 | 化学   |  94.5 |  3
 14 | 张学友 | 物理   |  93.5 |  4
 13 | 张学友 | 英语   |  92.5 |  5
  1 | 周润发 | 数学   |  91.5 |  6
 12 | 张学友 | 语文   |  91.5 |  7
  6 | 刘德华 | 数学   |  89.5 |  8
  9 | 刘德华 | 物理   |  89.5 |  9
 11 | 张学友 | 数学   |  89.5 | 10
  2 | 周润发 | 语文   |  89.5 | 11
  4 | 周润发 | 物理   |  84.5 | 12
  8 | 刘德华 | 英语   |  79.5 | 13
  3 | 周润发 | 英语   |  79.5 | 14
 10 | 刘德华 | 化学   |  69.5 | 15
```

### 2.按学科分组排名

```sql
SELECT
  *,
  row_number() over(PARTITION course ORDER BY score DESC) rn
FROM student_score
```

```
 id | name  | course | score | rn
----+--------+--------+-------+----
  5 | 周润发 | 化学   |  98.5 |  1
 15 | 张学友 | 化学   |  94.5 |  2
 10 | 刘德华 | 化学   |  69.5 |  3
  1 | 周润发 | 数学   |  91.5 |  1
 11 | 张学友 | 数学   |  89.5 |  2
  6 | 刘德华 | 数学   |  89.5 |  3
 14 | 张学友 | 物理   |  93.5 |  1
  9 | 刘德华 | 物理   |  89.5 |  2
  4 | 周润发 | 物理   |  84.5 |  3
 13 | 张学友 | 英语   |  92.5 |  1
  3 | 周润发 | 英语   |  79.5 |  2
  8 | 刘德华 | 英语   |  79.5 |  3
  7 | 刘德华 | 语文   |  99.5 |  1
 12 | 张学友 | 语文   |  91.5 |  2
  2 | 周润发 | 语文   |  89.5 |  3
```

### 3.获取每个学科的最高分

```sql
SELECT * FROM (
  SELECT 
    *,
    row_number() over(PARTITION BY course ORDER BY score desc) rn 
  FROM student_score
) t where rn=1;
```

```
 id | name  | course | score | rn
----+--------+--------+-------+----
  5 | 周润发 | 化学   |  98.5 |  1
  1 | 周润发 | 数学   |  91.5 |  1
 14 | 张学友 | 物理   |  93.5 |  1
 13 | 张学友 | 英语   |  92.5 |  1
  7 | 刘德华 | 语文   |  99.5 |  1
```

## RANK

rank类似row_number，只不过成绩相同会视为相同的排名，比如

```
100 1
100 1
98  3
95  4 
92  5
92  5
85  7
```

## DENSE_RANK

成绩相同会视为排名相同，但是排序不会间隔。

```
100 1
100 1
98  2
95  3 
92  4
92  4
85  5
```

## 字符串切片

从1开始算

```sql
select substr('apple', 1, 3)
```

```
app
```









## 字符串替换



默认只替换第一个出现的匹配项，g表示替换所有匹配项

```sql
select regexp_replace(stu_name, '[:-]', '', -'g')
from student 
```

也可以用`replace()`替换，默认直接就替换所有的。



## 字符串大小写转换





```sql
SELECT lower(stu_name) FROM student
SELECT upper(stu_name) FROM student
```



## 创建临时表

```sql
CREATE TEMP TABLE temp_table_test as (
  SELECT * FROM student
)
```

## 求众数

```sql
SELECT
  mode() within group (order by goods) as most_goods 
FROM order_list
```



从订单表中找出出现次数最多的商品

语法比较固定

```sql
mode() within group (order by <fields>)
```

一般情况下，这种写法是为了服务需要排序的聚合函数，比如还有

```postgresql
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY column_name) FROM table;
SELECT percentile_disc(0.5) WITHIN GROUP (ORDER BY column_name) FROM table;
```



## 时间戳字段自动填充

https://juejin.cn/post/7033762606175223839

实现在创建数据时自动用系统当前时间填充时间戳

```sql
CREATE TABLE users (
  ...
  create_at timestamp(6) default current_timestamp,
  -- 效果相同
  -- create_at timestamp(6) default now()
)
```

## 更新数据时自动更新时间

示例表

```sql
create table test_update (
  name varchar(20),
  update_time timestamp(6) default now()
)
```

创建触发器

为了能够使用这个触发器，创建表的字段和触发器更新的字段要一样。

```sql
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = now();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

使用触发器

```sql
CREATE TRIGGER test_trigger -- 触发器名称
BEFORE UPDATE ON test_update  -- 用于哪个表
FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
```

> 似乎是有问题的

## 插入数据时冲突处理

如果不处理的话，默认是报错的，可以用`ON CONFLICT`处理

基本语法：

```sql
INSERT INTO <table_name>(<column_list>) VALUES(<value_list>)
ON CONFLICT <target> <action>;
```

target

- 字段名
- 约束名
- 带谓语的 WHERE 子句（？）

action：

- DO NOTHING：已经重复就忽略不插入
- DO UPDATE SET column_1 = value_1, ...

参考：

- https://blog.csdn.net/lixinkuan328/article/details/107231321
- https://blog.csdn.net/CoderTnT/article/details/86532321

案例

```sql
insert into tbl   
  select id,id,1,random(),now() from generate_series(1,1000000) t(id)   
  on conflict(c1,c2)   
  do update   
  set   
  c3=excluded.c3,c4=excluded.c4,c5=excluded.c5  
  where  
  tbl.c3 is distinct from excluded.c3 or  
  tbl.c4 is distinct from excluded.c4;  
```

如果联合唯一索引，包括null

https://qastack.cn/dba/151431/postgresql-upsert-issue-with-null-values

https://dba.stackexchange.com/questions/151431/postgresql-upsert-issue-with-null-values



## 数据更新

