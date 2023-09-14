**PostgreSQL**多了一些窗口函数

每个部门工资最高的员工

```postgresql
SELECT department, name, salary,
       rank() OVER (PARTITION BY department ORDER BY salary DESC)
FROM employees;
```

PG多了一些数据类型，比如JSON、XML、ARRAY等

PG的索引比较多，除了MYSQL也有的B-Tree之外，还有Hash索引。



大小写差异，pg会默认把大写变成小写。除非用双引号：`"Age"`

单引号都是表示字符串，PG用双引号表示是字段，MySQL用反引号。