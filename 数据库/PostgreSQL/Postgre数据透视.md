https://blog.csdn.net/horses/article/details/107958046

```sql
select coalesce(product, '【全部产品】') "产品", coalesce(channel, '【所有渠道】') "渠道", 
       sum(amount) filter(where to_char(saledate, 'YYYYMM') = '201901') "一月",
       sum(amount) filter(where to_char(saledate, 'YYYYMM') = '201901') "二月",
       sum(amount) filter(where to_char(saledate, 'YYYYMM') = '201901') "三月",
       sum(amount) filter(where to_char(saledate, 'YYYYMM') = '201901') "四月",
       sum(amount) filter(where to_char(saledate, 'YYYYMM') = '201901') "五月",
       sum(amount) filter(where to_char(saledate, 'YYYYMM') = '201901') "六月",
       sum(amount) "总计"
from sales_data
group by rollup (product, channel);

```

