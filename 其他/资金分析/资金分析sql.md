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

## 建表语句

### 交易明细表

```sql
-- DROP TABLE IF EXISTS "xx"."交易明细";
CREATE TABLE "xx"."交易明细" (
  "交易卡号" text COLLATE "pg_catalog"."default",
  "交易账号" text COLLATE "pg_catalog"."default",
  "查询反馈结果原因" text COLLATE "pg_catalog"."default",
  "交易户名" text COLLATE "pg_catalog"."default",
  "交易证件号码" text COLLATE "pg_catalog"."default",
  "交易时间" timestamp(6),
  "交易金额" float8,
  "交易余额" float8,
  "收付标志" text COLLATE "pg_catalog"."default",
  "交易对手账卡号" text COLLATE "pg_catalog"."default",
  "现金标志" text COLLATE "pg_catalog"."default",
  "对手户名" text COLLATE "pg_catalog"."default",
  "对手身份证号" text COLLATE "pg_catalog"."default",
  "对手开户银行" text COLLATE "pg_catalog"."default",
  "摘要说明" text COLLATE "pg_catalog"."default",
  "交易币种" text COLLATE "pg_catalog"."default",
  "交易网点名称" text COLLATE "pg_catalog"."default",
  "交易发生地" text COLLATE "pg_catalog"."default",
  "交易是否成功" text COLLATE "pg_catalog"."default",
  "传票号" text COLLATE "pg_catalog"."default",
  "IP地址" text COLLATE "pg_catalog"."default",
  "MAC地址" text COLLATE "pg_catalog"."default",
  "对手交易余额" float8,
  "交易流水号" text COLLATE "pg_catalog"."default",
  "日志号" text COLLATE "pg_catalog"."default",
  "凭证种类" text COLLATE "pg_catalog"."default",
  "凭证号" text COLLATE "pg_catalog"."default",
  "交易柜员号" text COLLATE "pg_catalog"."default",
  "备注" text COLLATE "pg_catalog"."default",
  "商户名称" text COLLATE "pg_catalog"."default",
  "商户代码" text COLLATE "pg_catalog"."default",
  "交易类型" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Indexes structure for table 其他交易明细
-- ----------------------------
CREATE INDEX "idx1" ON "xx"."交易明细" USING btree (
  "交易卡号" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx2" ON "xx"."交易明细" USING btree (
  "交易对手账卡号" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx3" ON "xx"."交易明细" USING btree (
  "交易户名" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
```

### 账户信息表

```sql

-- ----------------------------
-- Table structure for 账户信息
-- ----------------------------
-- DROP TABLE IF EXISTS "xx"."账户信息";
CREATE TABLE "xx"."账户信息" (
  "账户开户名称" text COLLATE "pg_catalog"."default",
  "开户人证件号码" text COLLATE "pg_catalog"."default",
  "交易卡号" text COLLATE "pg_catalog"."default",
  "交易账号" text COLLATE "pg_catalog"."default",
  "账号开户时间" timestamp(6),
  "账户余额" float4,
  "可用余额" float4,
  "币种" text COLLATE "pg_catalog"."default",
  "开户网点代码" text COLLATE "pg_catalog"."default",
  "开户网点" text COLLATE "pg_catalog"."default",
  "账户状态" text COLLATE "pg_catalog"."default",
  "炒汇标志名称" text COLLATE "pg_catalog"."default",
  "销户日期" timestamp(6),
  "账户类型" text COLLATE "pg_catalog"."default",
  "开户联系方式" text COLLATE "pg_catalog"."default",
  "通信地址" text COLLATE "pg_catalog"."default",
  "联系电话" text COLLATE "pg_catalog"."default",
  "代理人" text COLLATE "pg_catalog"."default",
  "代理人电话" text COLLATE "pg_catalog"."default",
  "备注" text COLLATE "pg_catalog"."default",
  "开户省份" text COLLATE "pg_catalog"."default",
  "开户城市" text COLLATE "pg_catalog"."default",
  "账号开户银行" text COLLATE "pg_catalog"."default",
  "客户代码" text COLLATE "pg_catalog"."default",
  "法人代表" text COLLATE "pg_catalog"."default",
  "客户工商执照号码" text COLLATE "pg_catalog"."default",
  "法人代表证件号码" text COLLATE "pg_catalog"."default",
  "住宅地址" text COLLATE "pg_catalog"."default",
  "邮政编码" text COLLATE "pg_catalog"."default",
  "代办人证件号码" text COLLATE "pg_catalog"."default",
  "邮箱地址" text COLLATE "pg_catalog"."default",
  "关联资金账户" text COLLATE "pg_catalog"."default",
  "地税纳税号" text COLLATE "pg_catalog"."default",
  "单位电话" text COLLATE "pg_catalog"."default",
  "代办人证件类型" text COLLATE "pg_catalog"."default",
  "住宅电话" text COLLATE "pg_catalog"."default",
  "法人代表证件类型" text COLLATE "pg_catalog"."default",
  "国税纳税号" text COLLATE "pg_catalog"."default",
  "单位地址" text COLLATE "pg_catalog"."default",
  "工作单位" text COLLATE "pg_catalog"."default",
  "销户网点" text COLLATE "pg_catalog"."default",
  "最后交易时间" timestamp(6),
  "账户销户银行" text COLLATE "pg_catalog"."default",
  -- "卡号类型" text COLLATE "pg_catalog"."default"
  "账卡号标签" text COLLATE "pg_catalog"."default"
);
```

> “卡号类型”改为“账卡号标签”，可以用来自行标记该卡的标签。
