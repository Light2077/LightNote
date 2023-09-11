https://blog.csdn.net/horses/article/details/107958046

创建表

```postgresql
CREATE TABLE "public"."sales" (
  "transaction_date" date,
  "product_name" varchar(10) COLLATE "pg_catalog"."default",
  "store_name" varchar(10) COLLATE "pg_catalog"."default",
  "sales_volumn" int4
)
;
```

生成虚拟数据

```postgresql
TRUNCATE "public"."sales";
DO $$ 
DECLARE 
    d DATE;
    store VARCHAR(10);
    product VARCHAR(10);
    sales_volume INT;
    stores TEXT[] := ARRAY['淘宝', '京东', '拼多多', '线下'];
    products TEXT[] := ARRAY['apple', 'banana', 'pear'];
BEGIN 
    FOR d IN SELECT generate_series('2023-01-01', '2023-04-30', interval '1 day') 
    LOOP
        FOREACH store IN ARRAY stores
        LOOP
            FOREACH product IN ARRAY products
            LOOP
                sales_volume := FLOOR(RANDOM() * 100 + 1)::INT;
                INSERT INTO "public"."sales" ("transaction_date", "product_name", "store_name", "sales_volumn") 
                VALUES (d, product, store, sales_volume);
            END LOOP;
        END LOOP;
    END LOOP;
END $$;

```

统计不同月份，各个商家的各个产品的销量总和。

```postgresql
SELECT 
    store_name, 
    product_name,
    SUM(CASE WHEN EXTRACT(MONTH FROM transaction_date) = 1 THEN sales_volumn END) AS january,
    SUM(CASE WHEN EXTRACT(MONTH FROM transaction_date) = 2 THEN sales_volumn END) AS february,
    SUM(CASE WHEN EXTRACT(MONTH FROM transaction_date) = 3 THEN sales_volumn END) AS march,
    SUM(CASE WHEN EXTRACT(MONTH FROM transaction_date) = 4 THEN sales_volumn END) AS april
    -- ... 你也可以按需要添加其他月份
FROM "public"."sales"
GROUP BY store_name, product_name
ORDER BY store_name, product_name;
```

```
 store_name | product_name | january | february | march | april
------------+--------------+--------+---------+-------+------
 京东       | apple        |   1702 |    1454 |  1556 | 1528
 京东       | banana       |   1483 |    1544 |  1423 | 1251
 京东       | pear         |   1527 |    1038 |  1573 | 1801
 拼多多     | apple        |   1608 |    1346 |  1686 | 1677
 拼多多     | banana       |   1825 |    1186 |  1344 | 1354
 拼多多     | pear         |   1235 |    1214 |  1124 | 1724
 淘宝       | apple        |   1616 |    1500 |  1442 | 1586
 淘宝       | banana       |   1424 |    1378 |  1785 | 1437
 淘宝       | pear         |   1581 |    1583 |  1370 | 1960
 线下       | apple        |   1673 |    1135 |  1329 | 1712
 线下       | banana       |   1331 |    1333 |  1416 | 1669
 线下       | pear         |   1715 |    1720 |  1584 | 1429
```



关于月份列的写法

使用CASE WHEN

```postgresql
SUM(CASE WHEN EXTRACT(MONTH FROM transaction_date) = 1 THEN sales_volumn END)
```

使用filter与 to_char

> 该方法是Postgre特有的语法

```postgresql
SUM(sales_volumn) filter(where to_char(transaction_date, 'YYYYMM') = '202301')
```

使用CASE 与 to_char

```postgresql
SUM(CASE to_char(transaction_date, 'YYYYMM') WHEN '202301' then sales_volumn ELSE 0 END)
```

