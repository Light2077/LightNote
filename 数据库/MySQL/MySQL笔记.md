学生与班级

一个学校可以有多个学生，一个学生只能在一个学校

一个学生可以参加多个小组，一个小组可以有多个学生

一个学生只能有一张校园卡，一张校园卡只属于一个学生

### 导出为csv

- `INTO OUTFILE`：导出路径
- `FIELDS TERMINATED BY`: 以逗号为分隔符
- `OPTIONALLY ENCLOSED BY`: 字符串以双引号包括
- `LINES TERMINATED BY`: 已`\r\n`为换行符。

```mysql
SELECT * FROM student
INTO OUTFILE "./student.csv"
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';
```

> \r\n
>
> \r是回车，相当于光标回到行首
>
> \n是换行，相当于光标往下移一格
>
> 只有回车，会回到本行行首
>
> 只有换行，会往下一行，并不会回到行首
>
> 回车+换行=下一行行首