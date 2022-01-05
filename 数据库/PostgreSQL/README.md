https://www.runoob.com/postgresql/postgresql-tutorial.html

[PostgreSQL 部署](PostgreSQL 部署.md)

[PostgreSQL 数据库基本操作](PostgreSQL 数据库基本操作.md)

[PostgreSQL 表格基本操作](PostgreSQL 表格基本操作.md)

[PostgreSQL 模式](PostgreSQL 模式.md)

# 其他

[postgreSQL 日期函数 Extract](https://blog.csdn.net/u014071328/article/details/78789381/)

### EXTRACT函数

要从日期或时间型字段中提取

```sql
SELECT EXTRACT(YEAR FROM enter_time) FROM student
```

演示

```sql
SELECT now();
```

```
2021-12-29 08:24:16.083942 +00:00
```

提取现在的月份

```sql
select extract(month from now())
```

```
12
```

### 时间戳转日期

假设`enter_time`字段是时间戳

```sql
select to_timestamp(enter_time) from student limit 10;
```

默认时区是+0，需要+8个小时

### 时间戳直接提取

需要结合`EXTRACT`和`TO_TIMESTAMP`函数

```sql
select extract(second from to_timestamp(collect_time)) from d7_2021_12 limit 10;

```

日期时间运算

例如

> 注意
>
> `'4 hour'`’不能使用双引号，会报错

```sql
select now()+ interval '4 hour';
```



实现类似python的resample操作

按分钟进行聚合

```sql
select extract(days from to_timestamp(collect_time))   as d,
       extract(hour from to_timestamp(collect_time))   as h,
       extract(minute from to_timestamp(collect_time)) as m,
       avg(drawing_speed)
from d7_2021_12
group by d, h, m
limit 100;
```

每3分钟进行聚合

```sql
select extract(days from to_timestamp(collect_time))   as day,
       extract(hour from to_timestamp(collect_time))   as hour,
       floor(extract(minute from to_timestamp(collect_time)) / 3) * 3 as minute,
       AVG(drawing_speed) as drawing_speed
from d7_2021_12
group by day, hour, minute
limit 10;
```



### 间隔x个数据聚合

每隔10个数据求均值

```sql
select floor(id / 10) as i , avg(price) 
from selling 
group by i
```

