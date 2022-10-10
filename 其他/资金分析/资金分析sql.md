### 主账户统计

> `::DECIMAL(18,2)`保留了2位小数

```sql

DROP TABLE IF EXISTS "0922主账户统计";
CREATE TABLE "0922主账户统计" AS (
WITH t1 as (
SELECT 
	"交易卡号",
	string_agg(distinct "交易户名", ';') 交易户名,
	string_agg(distinct "交易证件号码", ';') 交易证件号码,
	
	sum(COALESCE(交易金额, 0)) 交易总额,
	sum(case 收付标志 when '进' then 交易金额 else 0 end) 入金总额,
	sum(case 收付标志 when '出' then 交易金额 else 0 end) 出金总额,
	
	avg(case 收付标志 when '进' then 交易金额 else 0 end) 平均入金,
	avg(case 收付标志 when '出' then 交易金额 else 0 end) 平均出金,
	
	sum(case 收付标志 when '进' then 1 else 0 end) 入金次数,
	sum(case 收付标志 when '出' then 1 else 0 end) 出金次数,
	
	count ( distinct 交易对手账卡号 ) 对手数,
	min( "交易时间" ) 最早交易时间,
	max( "交易时间" ) 最晚交易时间
FROM "收款卡交易明细"
GROUP BY 交易卡号
)
SELECT 
  t1.交易卡号,
	t1.交易户名,
	t1.交易证件号码,
	t1.交易总额::DECIMAL(18,2),
	(COALESCE(t1.入金总额, 0) - COALESCE(t1.出金总额, 0))::DECIMAL(18,2) 净值,
	t1.入金总额::DECIMAL(18,2),
	t1.出金总额::DECIMAL(18,2),
	(t1.入金总额 / (CASE t1.交易总额 WHEN 0 THEN NULL ELSE 交易总额 END))::DECIMAL(18,4) 入金比率,
	(t1.出金总额 / (CASE t1.交易总额 WHEN 0 THEN NULL ELSE 交易总额 END))::DECIMAL(18,4) 出金比率,
	(t1.平均入金)::DECIMAL(18,2),
	(t1.平均出金)::DECIMAL(18,2),
	t1.入金次数,
	t1.出金次数,
	t1.对手数,
	t1.最早交易时间,
	t1.最晚交易时间
FROM t1
ORDER BY 交易总额 DESC
)
```



### 交易明细分组统计

适用于查控平台的交易明细格式（32个字段）

```sql
-- 统计共同交易对手
DROP TABLE IF EXISTS "0922收款卡交易明细分组统计";
CREATE TABLE "0922收款卡交易明细分组统计" AS (

SELECT 
	"交易卡号",
	string_agg(distinct "交易户名", ';') 交易户名,
	string_agg(distinct "交易证件号码", ';') 交易证件号码,
	"收付标志",
	"交易对手账卡号",
	mode() within group (order by 对手户名) 对手户名, -- 取出现次数最多的作为对手户名
	-- string_agg(distinct "对手户名", ';') 对手户名拼接,
	SUM ( "交易金额" ) AS "交易金额",
	AVG ( "交易金额" ) AS "平均交易额",
	COUNT ( * ) AS "交易次数",
	COUNT (DISTINCT "交易对手账卡号") "对手数",
	MIN ( "交易时间" ) 最早交易时间,
	MAX ( "交易时间" ) 最晚交易时间

FROM "收款卡交易明细"
GROUP BY
		"交易卡号",
		"收付标志",
		"交易对手账卡号"
)
ORDER BY 交易金额 DESC

```

### 共同交易对手统计

```sql
DROP TABLE IF EXISTS "收款卡共同交易对手_2020后_基于平台筛选";
CREATE TABLE 收款卡共同交易对手_2020后_基于平台筛选 AS (
	SELECT COUNT
			( DISTINCT 交易卡号 ) AS "交易卡号数量",
			"收付标志",
			"交易对手账卡号",
			"对手户名",
			SUM ( "交易金额" ) AS "交易总额",
			COUNT ( * ) AS "交易次数",
			AVG ( 交易金额 ) AS 交易金额平均值,
			MODE ( ) WITHIN GROUP ( ORDER BY 交易金额 ) AS 交易金额众数,
			PERCENTILE_DISC ( 0.5 ) WITHIN GROUP ( ORDER BY 交易金额 ) AS 交易金额中位数,
			MIN ( 交易金额 ) AS 最小交易金额,
			MAX ( 交易金额 ) AS 最大交易金额,
			SUM ( CASE WHEN 交易金额> 1000 THEN 1 ELSE 0 END) AS "交易金额大于1千次数",
			SUM ( CASE WHEN 交易金额> 5000 THEN 1 ELSE 0 END) AS "交易金额大于5千次数",
			SUM ( CASE WHEN 交易金额> 10000 THEN 1 ELSE 0 END) AS "交易金额大于1万次数",
			SUM ( CASE WHEN 交易金额> 50000 THEN 1 ELSE 0 END) AS "交易金额大于5万次数",
			SUM ( CASE WHEN 交易金额> 100000 THEN 1 ELSE 0 END) AS "交易金额大于10万次数",
			MIN ( "交易时间" ) AS "最早交易时间",
			MAX ( "交易时间" ) AS "最晚交易时间" 
		FROM
			public."收款卡交易明细_基于订单记录筛选" 
		WHERE
			"交易时间" >= '2020-01-01' 
			-- AND 交易时间 < '2022-03-01' 
		GROUP BY
			"交易对手账卡号",
			"对手户名",
			"收付标志" 
		ORDER BY
		交易总额 DESC
)
```



### MAC地址数据清洗

```sql
SELECT LOWER(regexp_replace("MAC地址", '[:-]', '', 'g'))
FROM "其他交易明细" 
WHERE "MAC地址" IS NOT NULL
```

### 收付标志清洗

```sql
-- update  收款卡交易明细 set 收付标志='进' WHERE 收付标志 in ('C', '入', '贷')
-- update  收款卡交易明细 set 收付标志='出' WHERE 收付标志 in ('D', '借')
update 收款卡交易明细 set 收付标志=(
  CASE 收付标志
    WHEN 'C' THEN '进'
    WHEN 'D' THEN '出'
    
    WHEN '入' THEN '进'
    WHEN '贷' THEN '进'
    WHEN '借' THEN '出'
    ELSE 收付标志
 END
)
```

