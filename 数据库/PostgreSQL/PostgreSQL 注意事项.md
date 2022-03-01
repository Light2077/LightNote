列名不带引号，会被转成小写，如果带引号则保留大写。

从market表中查询`apple`列

```sql
SELECT AppLe FROM market
```

从market表中查询`AppLe`列

```sql
SELECT `AppLe` FROM market
```

上面这两条语句查找的列是**不一样**的。