https://blog.csdn.net/farxix/article/details/102913082

日期时间操作相关：https://www.postgresql.org/docs/current/functions-datetime.html

交易时间转为整点

```sql
SELECT
  交易时间,
	( SELECT to_char( 交易时间, 'yyyy-MM-dd hh24:00' ) ) 交易时间 
FROM
	test_trade
```

时间会向下取整

```
交易时间			 整点
2021-04-15 08:28:14	2021-04-15 08:00
2021-04-16 21:58:43	2021-04-16 21:00
```

如何向上取整？

时间取整：`DATE_TRUNC`

```sql
SELECT DATE_TRUNC('hour', TIMESTAMP '2020-03-17 02:09:30');
-- 返回：'2020-03-17 02:00:00'
```

时间加减

```sql
--取现在的时间并加1小时
SELECT NOW() + INTERVAL '1 HOUR';

--取现在的时间减去1小时
SELECT NOW() - INTERVAL '1 HOUR';

--在表格hosp_time里取admittime, 并往后推staylength个小时
SELECT admittime::timestamp + INTERVAL '1 HOUR' * staylength
FROM hosp_time;

```

查看当前时间

```sql
SELECT CURRENT_TIME;
Result: 14:39:53.662522-05

SELECT CURRENT_DATE;
Result: 2019-12-23

SELECT CURRENT_TIMESTAMP;
Result: 2019-12-23 14:39:53.662522-05

SELECT CURRENT_TIMESTAMP(2);
Result: 2019-12-23 14:39:53.66-05

SELECT LOCALTIMESTAMP;
Result: 2019-12-23 14:39:53.662522
```

