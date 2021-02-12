安装mycli，然后使用`mycli -ulight`可以获得更好的编辑权限。

mycli修改换行，把`~/.myclirc`里的multi_line改成true即可

# 1. 数据库入门

## 基本介绍

层次结构就理解为一个公司，分很多部门，每个部门有许多岗位。

早期数据库

1. 萌芽阶段：数据放在文件里。

2. 层次型数据库：

   优点：结构简单清晰，查询效率高

   缺点：现实世界很多联系是非层次的，这种数据库不适用于具有多对多联系的结点。查询子女结点必须通过双亲节点。结构严密，层次命令趋于程序化

3. 网状型数据库：没有解决导航问题，解决了数据完整性问题

   优点：能够更为直接地描述现实世界，一个结点可以有多个双亲，结点之间可以有多种联系；具有良好的性能，存取效率高

   缺点：结构复杂，随着应用环境的扩大，数据库的结构越来越复杂，不利于最终用户掌握；网状模型的DDL,DML复杂，并且要嵌入某一种高级语言（C，COBOL）用户不容易掌握和使用，由于记录之间的联系是通过存取路径实现的。应用程序在访问数据时必须选择适当的存取路径，因此用户必须了解系统结构的细节，加重了编写应用程序的负担。

4. **关系型数据库**：

   优点：建立在严格的数据概念的基础上，概念单一，无论实体还是实体之间的联系都用关系来表示。对数据的检索和更新结构也是关系（表）；它的存取路径对用户透明，从而有更高的独立性，更好的安全保密性，简化了程序员的工作和数据库开发建立的工作

   缺点：存取路径的隐蔽导致查询效率不如格式化数据模型

### SQL语言

Structured Query Language

### 关系型数据库

RDBMS relational database management system

特点：

- 数据以表格的形式出现
- 每行为各种记录名称
- 每列为记录名称所对应的数据域
- 许多的行和列组成一张表单
- 若干的表单组成database

| 数据库     | SQL类型          | 公司               |
| ---------- | ---------------- | ------------------ |
| Oracle     | PL/SQL           | 甲骨文             |
| MySQL      | My/SQL           | 甲骨文             |
| SQL-Server | T-SQL            | 微软               |
| Access     | SQL              | 微软               |
| SQLite     | 内嵌型小型数据库 | 移动前端用的比较多 |

## 数据库相关术语和概念

- 数据库：一些关联表的集合
- 数据表：表是数据的矩阵。在一个数据库中的表看起来像一个简单的电子表格
- 列：一列（数据元素）包含了相同类型的数据，例如邮政编码的数据
- 行：一行（元祖，或记录）是一组相关的数据，例如一条用户订阅的数据
- 冗余：存储2倍数据，冗余降低了性能，提高了数据安全性
- 主键：唯一的，一个数据表中只有一个主键，可以用它来查询数据
- 外键：用来关联2个表
- 复合键：将多列作为一个索引键，一般用于复合索引
- 索引：使用索引可以快速访问数据库表中的特定信息。索引是对数据库表中一列或多列的值进行排序的一种结构。类似书籍的目录
- 参照完整性：参照的完整性要求关系中不允许引用不存在的实体。与实体完整性是关系模型必须满足的完整性约束条件，目的是保证数据的一致性。

## Linux数据库的开启和连接

Debian平台的Linux系统安装，ubuntu。

`sudo apt install -y mysql-server mysql-client`

centos：

- 从[mysql官网](https://dev.mysql.com/downloads/)上下载
- `wget https://dev.mysql.com/get/mysql80-community-release-el8-1.noarch.rpm`


- `yum install -y mysql80-community-release-el8-1.noarch.rpm`

- 安装完成后可以用`yum repolist|grep mysql`查看

- 默认安装的mysql版本是8.0而我们常用的是5.7，所以需要修改配置文件，默认安装5.7


  - `vim /etc/yum.repos.d/mysql-community.repo`将mysql80的enable值修改为0，mysql57的enable修改为1

    ```
    [mysql157-community]
    name=MySQL 5.7 Community Server
    baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/$basearch/
    enabled=1
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
    
    [mysql80-community]
    name=MySQL 8.0 Community Server
    baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/8/$basearch/
    enabled=0
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
    ```

  - `sudo yum install mysql-community-server`

系统的配置文件和应用程序的配置文件`/etc`（所有用户共享）, `~/`当前用户家目录下的配置项，只对当前用户有效

## 开启数据库服务

- ubuntu : `service mysql start|stop|restart|status`
- deepin : `systemctl start|stop|restart|status mysqld`
- centos7 : `systemctl start|stop|restart|status mysqld`
- centos6 : `service mysqld start|stop|restart|status `

`ps -aux|grep -v grep|grep mysql`

`mysql --version`

需要客户端来访问数据库`sudo mysql -uroot `

## 连接数据库

语法：`mysql -hlocalhost -uroot -p123456 -P3306`

- -h host(ip地址) localhost = 127.0.0.1
- -u 用户名
- -p 用户密码
- -P 端口默认端口3306

其他版本的linux里root用户的默认密码是空，centos7会生成一个临时密码，可以用`cat /var/log/mysqld.log |grep password`【#jdOp1A_0-Fm】

`mysql -hlocalhost -uroot -p#jdOp1A_0-Fm -P3306`

进入mysql后需要先修改密码

`alter user root@localhost identified with mysql_native_password by 'Y47yn32b!';`

## 密码忘记

- 打开配置 `sudo vim /etc/my.cnf`

- 添加：

  ```
  [mysqld]
  skip-grant-tables
  ```

- 修改完成后，保存退出，重启服务`sudo systemctl restart mysqld`

- 使用命令`sudo mysql -uroot`重新连接Mysql服务器。此时可以不使用密码直接登录用户

- 执行`update mysql.user set authentication_string=password('123456') where user="root";`修改root用户密码

- 执行`flush privileges;`刷新策略，使策略立即生效并退出mysql客户端

- 修改`sudo vim /etc/my.cnf`注释掉刚才该的那句

- 重启服务`sudo systemctl restart mysqld`

## 用户创建相关操作

**mysql权限的两个阶段**

第一阶段为连接验证，主要限制用户连接mysql-server时使用的ip及密码

第二阶段为操作检查，主要检查用户执行的指令是否被允许，一般非管理员用户不允许执行drop，delete等危险操作

**权限控制安全准则**

- 只授予能满足需要的最小权限，防止用户执行危险操作
- 限制用户的登陆主机，防止不速之客登陆数据库
- 禁止或删除没有密码的用户
- 禁止用户使用弱密码
- 定期清理无效的用户，回收权限或删除用户

root用户只能本机登陆，不能远程登陆

**常用操作**

### 1.创建账户，权限授予

- 8.0以前

  ```mysql
  GRANT ALL PRIVILEGES on *.* to '用户名'@'主机' IDENTIFIED BY '密码' WITH GRANT OPTION;
  flush privileges; -- 刷新使权限生效
  ```

  - `ALL PRIVILEGES`授予全部权限，也可以指定`selct, insert, update, delete, create, drop, index, alter, grant, references, reload, shutdown, process, file`
  - `*.*`表示允许操作的数据库或表，这里表示所有文件。
  - 表示允许用户从哪个主机登陆，`%`表示允许任意主机登陆
  - with grant option 允许向下传递文件

- 8.0之后

  ```mysql
  CREATE USER '用户名'@'主机' IDENTIFIED BY '密码';  -- 创建账户
  GRANT ALL ON *.* TO '用户名'@'主机' WITH GRANT OPTION; -- 授权
  ```

### 2.修改密码

```mysql
-- 两个方法都行
update user set authentication_string=password('123456') where user="light";

alter user 'light'@'localhost' identified with mysql_native_password by '!Ztn1996';  -- 该方法需要特殊字符 大小写 数字
```

### 3.查看权限

```mysql
show grants;
show grants for 'light'@'localhost';
```

### 4.回收权限

```mysql
revoke all privileges on *.* from 'light'@'localhost'; -- 回收用户的所有权限
revoke grant option on *.* from 'light'@'localhost'; -- 回收权限传递
```

### 5.删除用户

```mysql
use mysql;
select host, user from user;
drop user light@localhost;
```



### 6. 创建一个能远端登陆的账号

`grant all privileges on *.* to 'alice'@'%' identified by '!Alice2077' with grant option;`

- 修改mysql配置文件：
  - ubuntu18.04 `/etc/mysql/mysql.conf.d/mysqld.cnf`
  - centos7.7 `/ect/my.cnf`

在`bind-address=127.0.0.1`注释掉（centos没有，如果有的话注释掉），让计算机允许mysql远程登陆。

- 打开服务器的3306端口
- 使用客户端远程登陆到mysql数据库

`sudo mysql -ualice -h<远端服务器ip> -P 3306 -p`

## 数据库的操作

mysql里有个user表，可以看到column有host user等列名，host表示能登陆的方式。

`authentication_string`是加密后的密码

`drop user jack@'%'`



### 创建数据库

```mysql
create database [if not exists] lightdb charset=utf8;
```

- 多次创建会报错
- 如果不指定字符编码，默认为utf8mb4（一个汉字4字节）
- 给数据库命名一定要习惯性加上反引号，防止和关键字冲突

### 查看数据库

```mysql
show databases;
```

### 选择数据库

```mysql
use lightdb;
```

### 修改数据库

```mysql
-- 只能修改字符集
alter database '数据库名' charset=新字符集;
```

### 删除数据库

```mysql
drop database [if exists] lightdb;
```

## 表的操作

### 1. 表的创建

```mysql
create table [if not exists] student (
    id int not null auto_increment primary key comment '主键',
    name char(255) comment '姓名' default '',
    age int not null,
    tel varchar(32) unique
)charset=utf8mb4;
```

### 2. 查看所有表格

```mysql
show tables;
```

### 3. 显示表格信息

```mysql
describe student;

desc student;  -- 两者一样

show create table student;  -- 查看建表语句
```



### 4. 删表格

```mysql
drop table student;
```

### 5. 修改表

```mysql
-- 修改表名
alter tabel student rename xuesheng

-- 移动表
alter tabel student rename to 数据库名.表名;
```

### 6. 修改字段

```mysql
alter tabel 表名 add 字段名 类型 [属性]; -- 新增一个字段

alter tabel 表名 add 字段名 数据类型 [属性] first; -- 加到表的最前面
alter tabel 表名 add 字段名 数据类型 [属性] after 另一个字段名; -- 加到另一个字段名的下面

alter tabel 表名 modify 字段名 数据类型 [属性];  -- 修改字段属性

alter tabel 表名 change 原字段名 新字段名 数据类型 [属性];  -- 修改字段名
alter tabel 表名 change 原字段名 新字段名 数据类型 after 另一个字段; -- 修改字段位置

alter tabel 表名 drop 字段名  -- 删除字段


```

### 7. 复制表格

```mysql
-- 复制一个表 不建议使用，不会复制自增和主键等属性
create table student2 select * from student

-- 创建新表，把字段和属性复制过去
create table student3 like student
insert into student3 select * from student -- 把数据复制过去
```





# 2. 数据库操作

## 增删改查(CDUR)

### 增加数据

```mysql
insert into student(id, name, age) values(1, 'zhangsan', 18)

insert into student(name, age) values('tom', 19) -- 也可以不写id

insert into student values(3, 'lily', 18) -- 省略了字段的话必须一一匹配

insert into student values(NULL, 'jack', 18) -- 可以填null让数据自己填id
```

### 查询数据

`select <字段名> from <表名>`

可以配合where或having来进行条件判断。

```mysql
select * from student

select id, age from student
select name from student

select name, age from student having name='tom';
```

### 修改数据

一般也要配合where或having来进行条件判断。

```mysql
update student set name='alice' where id=1;

-- select host, user, authentication_string from user;
update user set authentication_string=password('!Light2077') where User='light';
```

### 删除数据

```mysql
delete from student;  -- 会清空数据
delete from student where id=2;
delete from studnet where id in (1, 2, 3, 4);
truncate student -- 清空表名
```

## Mysql找那个的编码和数据类型

### 字符集

保存，传输存续的时候的时候会用到字符集。

| 常见字符集 | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| ASCII      | 基于罗马字母表的一套字符集，用一个字节的低7位表示字符，高位始终为0 |
| LATIN1     | 相对于ASCII做了扩展，仍用一个字节表示字符，但启用了高位，拓展了范围 |
| GB2312     | 简体中文字符，一个汉字最多2字节                              |
| GBK        | 所有的中文字符，一个汉字最多2字节                            |
| UTF8       | 国际通用编码，一个汉字最多3字节                              |
| UTF8MB4    | 国际通用编码，在utf8的基础上加强了对新文字的识别，一个汉字最多4字节。 |

查看字符编码集

```mysql
show variables like '%character%
```

看`character_set_database`这一行确定编码。

```
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | latin1                     |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | latin1                     |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
```



也可以使用：

```mysql
show create database test; 
```



```
+----------+-----------------------------------------------------------------+
| Database | Create Database                                                 |
+----------+-----------------------------------------------------------------+
| test     | CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET latin1 */ |
+----------+-----------------------------------------------------------------+
```

如果数据库没指定编码集是utf8会很麻烦，新建的表的默认编码集也会是latin1。此时插入中文数据会报错。比如新建一个表，这个表不指定编码，默认为latin1。

```mysql
create table t1(
id int primary key auto_increment,
name varchar(32)
);
```

此时执行插入中文的语句会报错

```mysql
insert into t1 values(1, '李华')
```

需要修改表和字段的编码集才能插入中文数据。

```mysql
alter table t1 charset=utf8;  -- 可以通过这行改表的编码集，但是还会报错
alter table t1 modify name varchar(32) charset utf8;  -- 此时把字段类型也改了。
```

### 校对集

实现字符的比较。比较字符的大小。

```mysql
show character set;
```

```
+----------+---------------------------------+---------------------+--------+
| Charset  | Description                     | Default collation   | Maxlen |
+----------+---------------------------------+---------------------+--------+
| ascii    | US ASCII                        | ascii_general_ci    | 1      |
| gbk      | GBK Simplified Chinese          | gbk_chinese_ci      | 2      |
| utf8     | UTF-8 Unicode                   | utf8_general_ci     | 3      |
| utf8mb4  | UTF-8 Unicode                   | utf8mb4_general_ci  | 4      |
```

default collation就表示默认校验集

- `_ci`表示大小写不敏感
- `_cs`大小写敏感
- `_bin`binary collation 二元法，直接比较字符的编码，可以认为是区分大小写的。

可以用下面这句查看所有的校对集

```mysql
show collation;
```



```mysql
create database test2 charset=utfmb4 collate=utf8mb4_general_cs;

create table t1(
    str char(1)
)charset=utf8mb4 collate=utf8mb4_general_cs;

create table t1(
    str char(1)
)charset=utf8mb4 collate=utf8mb4_bin;

```

## MySQL数据类型

### 整型

| 整数类型     | 字节 | 最小值                            | 最大值                                           |
| ------------ | ---- | --------------------------------- | ------------------------------------------------ |
| TINYINT      | 1    | 有符号：-128<br />无符号：0       | 有符号：127<br />无符号：255                     |
| SMALLINT     | 2    | 有符号：-32768<br />无符号：0     | 有符号：32767<br />无符号：65535                 |
| MEDIUMINT    | 3    | 有符号：`-2 ** 23`<br />无符号：0 | 有符号：`2 ** 23-1`<br />无符号：`2 ** 24 - 1`   |
| INT, INTEGER | 4    | 有符号：`-2 ** 31`<br />无符号：0 | 有符号：`2 ** 31 - 1`<br />无符号：`2 ** 32 - 1` |
| BIGINT       | 8    | 有符号：`-2 ** 63`<br />无符号：0 | 有符号：`2 ** 63 - 1`<br />无符号：`2 ** 64 - 1` |

- 一个无符号数一定是非负数

  ```mysql
  create table t3(
      id int primary key auto_increment,
     age tinyint unsigned,
  );
  ```

  

- 显示宽度(zerofill)：整型显示宽度，位数不足时用0填充

  ```mysql
  create table t4(
  id int(10) zerofill primary key auto_increment,
  name char(32)
  );
  insert into t4 values(12345, '5个'); -- 在mycli看不到填充的0，用图形化界面能看到
  insert into t4 values(1234567890, '10个');
  insert into t4 values(123456789012, '12个'); -- 会报错
  select * from t4
  ```

  

### 浮点型

| 浮点数类型                 | 字节 | 最小值                              | 最大值                   |
| -------------------------- | ---- | ----------------------------------- | ------------------------ |
| FLOAT                      | 4    | ±1.175494351E-38                    | ±3.402823466E+38         |
| DOUBLE                     | 8    | ±2.2250738585072014E-308            | ±1.7976931348623157E+308 |
| DEC(M,D)<br />DECIMAL(M,D) | M+2  | 给定DECIMAL的有效取值范围由M和D决定 | 同上                     |
| BIT(M)                     | 1-8  | BIT(1)                              | BIT(64)                  |

定点数位数更长。

使用方式

- float(M,D)
- double(M,D)
- decimal(M,D)

M表示支持多少个长度，D是小数点后面的位数

```mysql
create table t5(
a float(10, 2),
b double(10, 2),
c decimal(10, 2) -- 均表示最长10位，小数点后面2位
)
```

### 字符串型

| 字符串类型   | 字节 | 描述及存储需求                                            |
| ------------ | ---- | --------------------------------------------------------- |
| CHAR(M)      | M    | M为0~255之间的整数                                        |
| VARCHAR(M)   |      | M为0~65535之间的整数，值的长度+1个字节                    |
| TINYBLOB     |      | 允许长度0~2^8^-1个字节的定长字节字符串，值的长度+1个字节  |
| BLOB         |      | 允许长度0~2^16^-1个字节的定长字节字符串，值的长度+2个字节 |
| MEDIUMBLOB   |      | 允许长度0~2^24^-1个字节的定长字节字符串，值的长度+3个字节 |
| LONGBLOB     |      | 允许长度0~2^32-1^个字节的定长字节字符串，值的长度+4个字节 |
| TINYTEXT     |      | 允许长度0~2^8^-1个字节的定长字节字符串，值的长度+2个字节  |
| TEXT         |      | 允许长度0~2^16^-1个字节的定长字节字符串，值的长度+2个字节 |
| MEDIUMTEXT   |      | 允许长度0~2^24^-1个字节的定长字节字符串，值的长度+3个字节 |
| LONGTEXT     |      | 允许长度0~2^32^-1个字节的定长字节字符串，值的长度+4个字节 |
| VARBINARY(M) |      | 允许长度0~M个字节的定长字节字符串，值的长度+1个字节       |
| BINARY(M)    | M    | 允许长度0~M个字节的定长字节字符串                         |

```mysql
alter table s1 add address char(3); -- 3表示字符串的长度

insert into s1(name, age, address) values('tony', 20, 'city'); -- 报错，长度不能超过3
insert into s1(name, age, address) values('tony', 20, '乌鲁木齐'); -- 报错
```



`CHAR`与`VARCHAR`区别：

| Type       | Input     | Saved in DB | 字节数 | Desc                              |
| ---------- | --------- | ----------- | ------ | --------------------------------- |
| CHAR(5)    | `"a"`     | `"a     "`  | 5      | 固定占5个字节，不足的用空格补齐   |
| VARCHAR(5) | `"a"`     | `"a"`       | 2      | 固定1字节，额外用1字节记录位长    |
| CHAR(5)    | `"abc  "` | `"abc  "`   | 5      | 保留结尾空格，依然占5字节         |
| VARCHAR(5) | `"abc  "` | `"abc"`     | 4      | 删除结尾空格，额外用1字节记录位长 |
| CHAR(5)    | `"abcdefg"`   | `"abcde"` | 5 | 抛错                              |
| VARCHAR(5) | `"abcdefg"` | `"abcde"` | 6 | 抛错 |

blob存非文字信息，text存博客之类的文字信息

### 枚举型

多选一时使用的数据类型，在前端使用单选框的时候，枚举类型可以发挥作用。

优点：

- 限制了可选值
- 节省空间
- 运行效率高

```mysql
create table t6(
name varchar(32),
sex enum('男', '女', '保密') default '保密'
);
insert into t6 set name='Tony', sex=1;
insert into t6(name) values('Alex');
```

### 集合

set最多可以有64个不同的成员，类似于复选框，有多少可以选多少。在现代网站开发中，多选框的值有上千个，值存储的空没有索引用的多，y8iban将复选框的值单独设计成一张表

```mysql
create table t7(
name varchar(32),
hobby set('吃', '喝', '玩', '睡')
);
insert into t7 values('张三', '睡,喝,吃');
insert into t7 values('李四', '玩,吃');
```

### 时间类型

| 日期和时间类型 | 字节 | 最小值              | 最大值              |
| -------------- | ---- | ------------------- | ------------------- |
| DATE           | 4    | 1000-01-01          | 9999-12-31          |
| DATATIME       | 8    | 1000-01-01 00:00:00 | 9999-12-31 23:59:59 |
| TIMESTAMP      | 4    | 19700101080001      | 2038年的某个时刻    |
| TIME           | 3    | -838:59:59          | 838:59:59           |
| YEAR           | 1    | 1901                | 2155                |

- datetime

  ```mysql
  create table t8(
  create_at datetime
  );
  
  insert into t8 values('2020-11-19 08:00:00');
  insert into t8 values('2020/11/20 09:00:00');
  insert into t8 values(now());
  
  insert into t8 values('12020/11/20 09:00:00'); -- 报错
  
  ```

- time

  ```mysql
  create table t9(
  create_at time
  );
  
  insert into t9 values('12:12:12'); -- 12:12:12 
  insert into t9 values('100:12:12'); -- 4 days, 4:12:12
  insert into t9 values('-100:12:12'); --  -5 days, 19:47:48 
  insert into t9 values('10 10:12:12'); -- 10 days, 10:12:12
  -- 时间的范围是[-839:59:59 - 838:59:59]
  insert into t9 values('839:12:12'); -- 报错
  ```

- timestamp时间戳类型

  - 时间戳类型在显示方面和datetime一样，咋存储不一样
  - 范围从1970-1-1 0:0:0 到2038-1-19 11:14:07
  - 时间戳用4个字节表示
  - 该值大小与存储的长度有关：`2 ** (4 * 8 - 1)`

  ```mysql
  create table t10(
  create_time timestamp
  );
  insert into t10 values(now());
  insert into t10 values('2038-1-19 11:14:07');
  select * from t10;
  
  insert into t10 values('2038-1-19 11:14:08'); -- 报错
  ```

- year，同理，用字符串传年份。

### 布尔型

mysql中的bool类型也是0和1

```mysql
create table t11(
cond boolean
);
# 范围在-128 - 127 直接
insert into t11 set cond=True; -- 1
insert into t11 set cond=1; -- 1
insert into t11 set cond=10; -- 10
insert into t11 set cond=-1; -- -1

insert into t11 set cond=-0.1; -- 0
insert into t11 set cond=0.1; -- 0
insert into t11 set cond=0; -- 0
insert into t11 set cond=False; -- 0
select * from t11;
insert into t11 set cond='True'; -- 报错
```



### 列的属性

- null

  - `null`:是可以为空，默认不写
  - `not null`: 不可以为空

- default，默认值一般与null搭配

  - `name varchar(32) default 'admin' not null`

- auto_increment

  - 常配合主键使用，自动增长的列，从1开始。

- primary key

  - 主键一般是唯一的标识
  - 特性：不能为空，不能重复，一张表中只有一个主键

  ```mysql
  -- 联合主键，使用较少
  create table double_primary_key_test(
  id int;
  sid int,
  primary key(id, sid)
  );
  
  insert into double_primary_key_test values(1, 1);
  insert into double_primary_key_test values(1, 2);
  insert into double_primary_key_test values(2, 1);
  
  insert into double_primary_key_test values(1, 1); -- 报错
  ```

- unique

  - 唯一键，一列中的数据不能重复
  - 

## 运算符

### 算术运算符

```mysql
select 123 + 543, 12 * 5, -123 / 2, 10 % 3, 2 / 0, 3 % 0;
/*
+-----------+--------+----------+--------+--------+--------+
| 123 + 543 | 12 * 5 | -123 / 2 | 10 % 3 | 2 / 0  | 3 % 0  |
+-----------+--------+----------+--------+--------+--------+
| 666       | 60     | -61.5000 | 1      | <null> | <null> |
+-----------+--------+----------+--------+--------+--------+
*/
```

### 比较运算符

| 运算符   | 作用           |
| -------- | -------------- |
| `=`      |                |
| `<>`或`!=` | 不等于         |
| `<=> `     | NULL安全的等于 |
| `< `       |                |
| `<=`       |                |
| `> `       |                |
| `>=`     |                |
| BETWEEN | 存在指定范围 |
| IN | 存在指定集合 |
| IS NULL | 为NULL |
| IS NOT NULL |                |
| LIKE | 通配符匹配 |
| REGEXP或 RLIKE | 正则表达式匹配 |

- 范围比较

  ```mysql
  select 123 between 100 and 200, 'b' in ('a', 'b', 'c');
  
  /*
  +-------------------------+------------------------+
  | 123 between 100 and 200 | 'b' in ('a', 'b', 'c') |
  +-------------------------+------------------------+
  | 1                       | 1                      |
  +-------------------------+------------------------+
  */
  ```

- null比较，`<=>`相当于is

  ```mysql
  select 3 = null, 3 is null, 3 <=> null;
  /*
  +----------+-----------+------------+
  | 3 = null | 3 is null | 3 <=> null |
  +----------+-----------+------------+
  | <null>   | 0         | 0          |
  +----------+-----------+------------+
  */
  ```

- 模糊比较

  ```mysql
  select 'helloworld' like 'hello%'; -- % 理解为通配符
  select * from student where name like "___"; -- 模糊查询_ 表示单个符号 % 表示任意个符号
  select * from student where eyear rlike "^2017"
  /*
  +----------------------------+
  | 'helloworld' like 'hello%' |
  +----------------------------+
  | 1                          |
  +----------------------------+
  */
  ```

### 逻辑运算符

| 运算符   |
| -------- |
| NOT或!   |
| AND或&&  |
| OR或\|\| |
| XOR异或  |

```mysql
select * from t1 where name like '%s%';

select * from t1 where name like '%s%' and age < 18;
```

# 3. 数据库的查询

## 构造数据

为操作方便先构造以下数据

**学生表**

```mysql
create table student(
id int unsigned primary key auto_increment,
name char(32) not null unique,
sex enum('男', '女') not null,
city char(32) not null,
description text,
birthday date not null default '1995-1-1',
money float(7, 2) default 0,
only_child boolean
)charset=utf8;

insert into student
(name, sex, city, description, birthday, money, only_child)
values
('郭德纲', '男', '北京', '班长', '1997/10/1', rand() * 100, True),
('陈乔恩', '女', '上海', NULL, '1995/3/2', rand() * 100, True),
('赵丽颖', '女', '北京', '班花,不骄傲', '1998/4/3', rand() * 100, False),
('王宝强', '男', '重庆', '超爱吃火锅', '1994/3/16', rand() * 100, False),
('赵雅芝', '女', '重庆', '全宇宙三好学生', '1992/6/6', rand() * 100, False),
('张学友', '男', '上海', '奥林匹克总冠军', '1991/5/30', rand() * 100, True),
('陈意涵', '女', '上海', NULL, '1994/4/17', rand() * 100, True),
('赵本山', '女', '南京', '副班长', '1993/2/12', rand() * 100, False),
('张柏芝', '女', '上海', NULL, '1992/11/24', rand() * 100, True),
('吴亦凡', '男', '南京', '大碗宽面要不要', '1995/6/12', rand() * 100, True),
('鹿晗', '男', '北京', NULL, '1996/7/8', rand() * 100, True),
('关晓彤', '女', '北京', NULL, '1997/12/23', rand() * 100, False),
('周杰伦', '男', '台北', '小伙子人才啊', '1998/3/16', rand() * 100, True),
('马云', '男', '南京', '首富', '1990/4/1', rand() * 100, True),
('马化腾', '男', '深圳', '马云死对头', '1990/11/28', rand() * 100, False);
```

**成绩表**

```mysql
create table score(
id int unsigned primary key auto_increment,
math float not null default 0,
english float not null default 0
)charset=utf8;

insert into score(math, english)
values
(49, 72), (62, 66.7), (44, 86), (77.5, 74), (41, 75),
(82, 59.5), (64.5, 85), (62, 98), (87, 94), (67, 53),
(81, 90), (78, 70), (83, 66), (23, 99), (97, 98);
```

**加个反引号避免表名或者属性与关键字重名**。

## 常用的查询语句

### 1. SELECT: 字段表达式

- select 既可以查询，也可做输出

  ```mysql
  select rand();
  select unix_timestamp(); -- 显示unix时间戳
  select id, name from student;
  
  select id, name from student where sex='女';
  ```

### 2. FROM子句

from后接数据源，数据源可以写多个。比如

```mysql
select student.id, student.name, score.math from student, score; -- 结果很奇怪
```

### 3. WHERE语句

- where是条件查询，只返回结果为True的数据

  ```mysql
  select name from student where city="上海";
  ```

- 空值判断

  ```mysql
  select name from student where description is null;
  select name from student where description is not null;
  ```

- 范围判断

  ```mysql
  select id, math from score where math between 60 and 70;
  select id, math from score where math not between 60 and 70;
  
  select * from score where math>=80 and english <= 60;
  ```

#### 4 HAVING语句

```mysql
select name, birthday from student where birthday > '1995-1-1';
select name, birthday from student having birthday > '1995-1-1';

select * from student where id>=3 and city='北京';
select * from student having id>=3 and city='北京';

select * from student where id>=3 having city='北京';
```

where和having的区别

```mysql
-- 只能使用where
select id, name, sex, city from student where money>=20;

select id, name, sex, city from student having money>=20; -- 报错，因为money没出现在from之前
```



```mysql
select id as i, name as n, sex as s, city as c from student where name='周杰伦';
-- 报错 where不能使用别名
select id as i, name as n, sex as s, city as c from student where n='周杰伦';

-- having 可以使用别名，where不可以
select id as i, name as n, sex as s, city as c from student having n='周杰伦';

-- having 可以使用聚合函数，where不可以

select city, group_concat(birthday) from student group by city having min(birthday) > '1995-1-1';

select city, group_concat(sex) from student group by city;
```

### 5GROUP BY:分组查询

- 按照某一字段进行分组，会把该字段中值相同的归为一组，将查询的结果分类显示，方便统计。
- 如果有where要放在where后面
- 语法：`select 字段 from 表名 group by 分组字段;`

```mysql
-- 直接分组
select city, group_concat(birthday) from student group by city;

-- 选出生日晚于1995-1-1的同学，再进行分组
select city, group_concat(birthday) from student where birthday > '1995-1-1' group by city;
```



### 6 ORDER BY:按字段排序

- ORDER BY 主要用于排序
- 写在GROUP BY 后面，如果有HAVING 写在 HAVING 后面
- 语法：`select 字段 from 表名 order by 排序字段 asc|desc;`
- asc 升序， desc降序，默认asc

```mysql
select name, birthday from student order by birthday asc;

select name, birthday, sex from student having sex='女' order by birthday asc;

-- 先选出每个城市最大的同学，在按降序排序
select city, min(birthday)  from student group by city order by min(birthday) desc;
```

### 7.LIMIT 限制取出数量

```mysql
-- 应用场景：
-- per_page = 5 每页显示5个
-- cur_page = 2 当前页码
-- 偏移量 offset = (cur_page - 1) * per_page
select * from student limit 5;

-- 一下两句等价
select * from student limit 5 offset 3; -- 从第四个开始
select * from student limit 3, 5;
```

### 8. DISTINCT:去重

```mysql
select distinct city from student;
```

### 9. dual表

dual是一个虚拟的表，仅仅为了保证select from语句的完整性

```mysql
select now();

select now() from dual;
```



## 函数

### 聚合函数

| Name            | desc                         |
| --------------- | ---------------------------- |
| AVG()           |                              |
| BIT_AND()       |                              |
| BIT_OR()        |                              |
| BIT_XOR()       |                              |
| COUNT()         |                              |
| COUNT(DISTINCT) | 返回许多不同值的计数         |
| GROUP_CONCAT()  | 返回连接的字符串             |
| JSON_ARRAY()    | 将结果集作为单个JSON数组返回 |
| JSON_OBJECT()   | 将结果集作为单个JSON对象返回 |
| MAX()           |                              |
| MIN()           |                              |
| STD()           | 返回样本标准差               |
| STDDEV()        | 返回样本标准差               |
| STDDEV_POP()    | 返回样本标准差               |
| STDDEV_SAMP()   | 返回样本标准差               |
| SUM()           |                              |
| VAR_POP()       | 返回样本方差                 |
| VAR_SAMP()      | 返回样本方差                 |
| VARIANCE()      | 返回样本方差                 |



```mysql
select city, group_concat(money), group_concat(name) from student group by city;

select city, 
count(name) as 人数,
sum(money) as 总金钱数,
avg(money) as 平均金钱sel
from student group by city;

-- 取出每个城市中满足最小出生年份大于1995的同学
-- (只要一个城市有人小于95年的，这个城市就没了)

select city, group_concat(birthday) from student group by city having min(birthday) > '1995-1-1';

-- 过滤掉小于95年的同学
select city, group_concat(birthday) from student where birthday > '1995-1-1' group by city;
```



### 数值计算类

```mysql
select abs(-2), ceil(1.1), floor(1.1);
select mod(5,3), round(2.13579, 3), truncate(2.13579, 3);
select rand();
```

### 日期类

```mysql
select curdate() as 当前日期, curtime() as 当前时间, now() as 当前日期时间;

select unix_timestamp(now());
select unix_timestamp('2020-08-10 20:15:30');

select datediff('2077-11-1', '2020-11-19');

select now(),
year(now()), 
month(now()) as 一年的第几月, 
week(now()) as 一年的第几周,
day(now()) as 一年的第几天;

select monthname(now());

select hour(now()), minute(now());

select date_format(now(), '%y-%m-%d %h:%i:%s');
```

### 字符串相关

| 函数                    | 功能                                                   |
| ----------------------- | ------------------------------------------------------ |
| CONCAT(S1, S2, ..., Sn) | 拼接字符串                                             |
| INSERT(str,x,y,instr)   | 将字符串str从第x位置开始，把y个字符长的子串替换为instr |
| LOWER(str)              |                                                        |
| UPPER(str)              |                                                        |
| LEFT(str, x)            | 返回最左边x个字符                                      |
| RIGHT(str, x)           |                                                        |
| LPAD(str, n, pad)       | 用字符串pad对str左边填充，直到长度为n                  |
| RPAD(str, n, pad)       |                                                        |
| LTRIM(str)              | 去掉字符串str左边的空格                                |
| RTRIM(str)              |                                                        |
| REPEAT(str, x)          |                                                        |
| REPLACE(str, a, b)      | 字符串b替换字符串str中出现的所有字符串a                |
| TRIM(str)               |                                                        |
| SUBSTRING(str,x,y)      | 返回从字符串str x位置起y个字符长度的子串。             |

### 其他函数

| 函数           | 功能                 |
| -------------- | -------------------- |
| DATABASE()     | 返回当前数据库名     |
| VERSION()      |                      |
| USER()         |                      |
| INET_ATON(IP)  |                      |
| INET_NTOA(num) |                      |
| PASSWORD(str)  | 返回字符串的加密版本 |
| MD5(str)       |                      |

## 多表查询

### 1. UNION 联合查询

![image-20200810115516052](img/union.png)

union操作符用于合并两个或多个select语句的结果集。

要求：

- select 语句的字段数（**列数**）必须一样
- 数据类型可以不一样
- 字段名默认按照左边的表来设置

```mysql
select * from student union select * from score;
-- The used SELECT statements have a different number of columns

create table s2 like student;

insert into s2 values
(20, '谢霆锋', '男', '上海', '帅哥一枚', '1995/2/16', rand() * 100, True),
(21, '王菲', '女', '上海', NULL, '1993/1/7', rand() * 100, True),
(22, '刘亦菲', '女', '深圳', '神仙姐姐', '1996/10/15', rand() * 100, True);

-- 可以拼接了，但是id重复了
select * from student union select * from s2;

-- union 是上下合并的
select student.id, student.name, student.city from student union select * from score;
```

### 2. INNER JOIN查询

- 只有两边id相等的数据会被合并

![image-20200810120948488](img/inner join.png)

```mysql
select student.id, student.name, student.city, score.math, score.english from student inner join score;
-- 结果会是一个笛卡尔积，横着拼，但是一共有15 * 15 = 225 行

-- 基于某一列来合并
select student.id, student.name, student.city, score.math, score.english from student inner join score on student.id = score.id;

-- 合并两张表
select * from student inner join score on student.id = score.id;

select student.*, score.math from student inner join score on student.id = score.id;
```

### 3. LEFT JOIN : 左连接

- left join 关键字从左表返回所有的行，如果右表没有匹配，结果为NULL。
- 左表的数据全有，右表数据不一定有。

```mysql
-- 先创个新表
 create table s3 like s2;
 
-- 把之前创的2个表合并
insert into s3 select * from student union select * from s2;

-- 左连接
select * from s3 left join score on s3.id=score.id;
```

### 4. RIGHT JOIN : 右连接

- 右表的数据全有，左表数据不一定有。

```mysql
select * from s3 right join score on s3.id=score.id;
```

##### 5. FULL JOIN : 全连接

- full join 的连接方式是只要左表和右表其中一个表存在匹配，就返回行。相当于结合了left join和right join的结果
- mysql不支持full join

```mysql
select * from t1 full outer join t2 on t1.id = t2.id
```

### 子查询

```mysql
select name, math from student inner join score on student.id = score.id where score.id in (select score.id from score where math > 80);

-- 简化
select name from student where id in (select id from score where math > 80);
```

## 视图表

- 视图是数据特定子集，是从其他表里提取出数据形成的虚拟表，或者说临时表。
- 创建视图表依赖一个查询
- 视图是永远不会自己消失的除非手动删除。
- 视图有时对提高效率有帮助，临时表不会对性能有帮助，是资源消耗者。
- 视图一般随该数据库存放在一起，临时表永远在tempdb里。
- 视图适合于多表连接浏览时会用；不适合增删改，这样可以提高执行效率。
- 一般视图表名称以`v_`为前缀，用来与正常表进行区分。
- 对原表的修改会影响到视图中的数据（影响是双向的）。
- 最好不要改视图表（以前的版本不允许修改）

建立视图表时有个ALGORITHM参数：

- UNDFINED MERGE效果一样，可以修改
- TMPTABLE 不能修改

```mysql
create view v_score as select a.id, a.name, b.math, b.english
from student a inner join score b on a.id = b.id;

-- 不能修改的视图表
create algorithm=temptable view v_score as select a.id, a.name, b.math, b.english
from student a inner join score b on a.id = b.id;

-- 查询
select * from v_score;

-- 删除
drop view v_score;
```



## 练习：

### 查找每个城市，数学最高的学生

```mysql
-- 先简化一下问题，找到每个城市年龄最小的学生
-- 这里有个问题，不能显示对应姓名
select city, max(birthday) from student group by city;

-- 这里需要子查询
select name, city, birthday from student where birthday in (select max(birthday) from student group by city);

-- 合并两表
select city, math from student inner join score on student.id = score.id;

-- 合并两个操作
select city, max(math) from student inner join score on student.id = score.id group by city;

-- 查看名字 但是可能会出bug
select student.name, student.city, score.math from student
inner join score on student.id = score.id
where score.math in (
select max(math) from student inner join score on student.id = score.id group by city
);

-- 只拿最大数学成绩的id
create view v_math as select city, max(math) from student join score on student.id = score.id group by city;

select student.id, name, sex, city, math from student join score on student.id = score.id where math in (select `max(math)` from v_math);

-- 合并两个表
create view v_exam as select student.*, math, english from student inner join score on student.id = score.id;

-- 特点是合并的同时把城市信息带上。
select v_exam.id, v_exam.name from v_exam inner join (select city, max(math) as max_math from v_exam group by city) as m on v_exam.city = m.city and v_exam.math=m.max_math;
```



### 查找每个城市，英语最低的学生。

### 计算最大学生和最小学生相差多少天

```mysql
select datediff(max(birthday), min(birthday)) from student;
```

### 计算男生和女生的数学和英语平均分

```mysql
select sex, avg(english), avg(math) from student inner join score on student.id = score.id group by sex;


-- 1.先联合两表
select sex, score.math,score.english from student inner join score on student.id = score.id;

-- 2.组合两表
select sex, group_concat(score.math), group_concat(score.english) from student inner join score on student.id = score.id group by sex;

-- 3.求均值
select sex, avg(score.math), avg(score.english) from student inner join score on student.id = score.id group by sex;
```

# 4. 数据库高级特性

## 4.1 存储引擎

存储引擎就是如何存储数据，如何为数据建立索引和如何更新，查询数据等技术的实现方法。MySQL默认支持多种存储引擎，以适用不同领域的数据库应用需要，用户可以通过选择使用不同的存储引擎提高应用效率，提供灵活的存储。

查看当前的存储引擎

```mysql
show variables like '%engine%';

show engines;
```



### MySQL常用存储引擎

| 功能         | MYISAM | Memory | InnoDB | Archive |
| ------------ | ------ | ------ | ------ | ------- |
| 存储限制     | 256TB  | RAM    | 64TB   | None    |
| 支持事物     | no     | no     | yes    | no      |
| 支持全文索引 | yes    | no     | no     | no      |
| 支持数索引   | yes    | yes    | yes    | no      |
| 支持哈希索引 | no     | yes    | no     | no      |
| 支持数据缓存 | no     | n/a    | yes    | no      |
| 支持外键     | no     | no     | yes    | no      |

**InnoDB**

事务性数据库的首选引擎，支持事物安全部(ACID)，支持行锁定和外键，是默认的MySQL引擎。

特性：

- **给mysql提供了具有提交、回滚、崩溃恢复能力的事务安全存储引擎。**
- 是为处理巨大数据量的最大性能设计。它的CPU效率比其他基于磁盘的关系型数据库引擎高。
- 存储引擎自带缓冲池，可以将数据和索引缓存到内存中。
- **支持外键的完整性约束**
- 被用在众多需要高性能的大型数据库站点上
- **支持行级锁**

**MyISAM**

基于ISAM存储引擎，并对其进行扩展，它是在web，数据仓储和其他应用环境下最常使用的存储引擎之一，MyISAM拥有较高的插入、查询速度，但不支持事务。

特性：

- 大文件支持更好
- 当删除，更新，插入混用时，产生更少碎片
- 每个MyISAM表最大索引数是64，这可以通过重新编译来改变，每个索引的最大列数是16
- 最大的键长度是1000字节。
- BLOB和TEXT列可以被索引（博客被索引）
- NULL被允许在索引的列中，这个值占每个键的0-1个字节
- 所有数字键值以高字节优先被存储以允许一个更高的索引压缩
- MyISAM类型表的AUTO_INCREMENT列更新比InnoDB类型的AUTO_INCREMENT更快
- 可以把数据文件和索引文件放在不同目录
- 每个字符列可以有不同的字符集
- 有varchar的表可以固定会动态记录长度
- varchar和char列可以多达64kb
- **只支持表锁**

**MEMORY**

memory存储引擎将表中的数据存储到内存中，为查询和引用其他表数据提供快速访问。

### 存储引擎的选择

一般来说，对插入和并发性能要求较高的，或者需要外键，或者需要事务支持的情况下，选择Innodb。插入较少，查询较多的场景优先考虑MyISAM。淘宝订单用InnoDB，维基百科用MyISAM。

### 使用引擎

一般在建表时添加

```mysql
create table abc（
name char(10)
)engine=MyISAM charset=utf8; -- engine=InnoDB
```

### InnoDB 和 MyISAM 在文件方面的区别

可以在`var/lib/mysql`内查看

InnoDB 将一张表存储为2个文件

- demo.frm 存储表的结构和索引
- demo.ibd 存储数据，idb存储是有限的，存储不足自动创建ibd1，ibd2
- InnoDB的文件创建在对应的数据库中，不能任意移动

MyISAM 将一张表存储为3个文件

- demo.frm 存储表的结构
- demo.myd 存储数据
- demo.myi 存储表的索引
- MyISAM 的文件可以任意的移动

索引的解释：为了快速找到一条数据，给索引建了一个表。只查索引列，使用B+树内置的查找算法查找数据。适用于数据量非常大的情况，或者查找非常频繁的情况。

## 4.2 关系与外键

### 关系

- 一对一
  - 在A表中有一条记录，在B表中同样有唯一一条记录相匹配
  - 如学生表和成绩表
- 一对多/多对一
  - 在A表中有一条记录，在B表中有多条记录对应
  - 如博客中的用户表和文章表
- 多对多
  - A表中一条记录有多条B表数据对应，同样B表中一条数据在A表中也有多条与之对应
  - 如博客中的收藏表。一个用户可以收藏多篇文章，一篇文章可以被多个用户收藏

## 外键

外键是一种约束，它只保证数据的一致性，并不能给系统性能带来任何好处。

建立外键时，都会在外键列上建立对应的索引。外键的存在会在每一次数据插入、修改时进行约束检查，如果不满足外键约束，则禁止数据的插入和修改，这必然带来一个问题，就是在数据量特别大的情况下，每一次约束检查必然导致性能的下降。

出于性能的考虑，如果我们的系统对性能要求较高，那么可以考虑在生产环境中不使用外键。

### **构造数据**

```mysql
create table `user` (
id int unsigned primary key auto_increment,
gid int unsigned,
name char(32) not null
)charset=utf8;

create table product(
id int unsigned primary key auto_increment,
name char(32) not null unique,
price float
)charset=utf8;

-- 用户信息表 1对1
create table userinfo(
id int unsigned primary key auto_increment,
phone int unsigned unique,
age int unsigned,
location varchar(128)
)charset=utf8;

-- 用户组表 1对多
create table `group`(
id int unsigned primary key auto_increment,
gname char(32) not null unique
)charset=utf8;

-- 订单表 多对多
create table `order` (
id int unsigned primary key auto_increment,
uid int unsigned,
pid int unsigned
)charset=utf8;
```

### 添加外键

需要建立外键约束，保证两个表是一一对应的。

```mysql
-- user(主表) 与 userinfo(副表) 【userinfo 中id的值必须与 user的id一一对应】
-- 添加数据的顺序：user -> userinfo
-- 删除数据的顺序：userinfo -> user
alter table userinfo add constraint fk_user_id foreign key(id) references user(id);

-- 1 对 多
alter table `user` add constraint fk_gid foreign key(gid) references usergroup(id);

insert into `group` values(1, '普通用户'), (2, 'vip用户');
insert into `user` values(1, 1, 'lily'), (2, 1, 'tom'), (3, 2, 'alex'), (4, 2, 'any');
-- 添加外键失败。

-- 多对多
insert into product values(1, '苹果', 5), (2, '雪梨', 15), (3, '香蕉', 10), (4, '芒果', 20);

-- 需要再用一张表来表示
-- lily : 雪梨, 香蕉, 芒果
-- tom : 芒果
-- alex : 苹果, 雪梨
-- any : 香蕉, 雪梨
insert into `order` values
(1, 1, 2), (2, 1, 3), (3, 1, 4),
(4, 2, 4),
(5, 3, 1), (6, 3, 2),
(7, 4, 3), (8, 4, 2);

-- 建立外键约束
-- 修改order时要满足user和product的id出现过。
alter table `order` add constraint fk_uid foreign key(uid) references user(id);
alter table `order` add constraint fk_pid foreign key(pid) references product(id);

-- 删除外键
alter table `order` drop foreign key fk_pid;
```

# 5. 数据库事务及其他

## 5.1 事务

### 简介

事务主要用于处理操作量大、复杂度高、且**关联性强**的数据。

比如：在人员管理系统中，你删除一个人员，既需要删除人员的基本资料，也要删除和该人员相关的信息，如信箱，文章等等，这样这些数据库操作语句就构成一个事务。

在mysql中只有innodb存储引擎支持事务。

事务处理可以用来维护数据库的完整性，保证成批的sql语句要么全部执行，要不全部不执行。主要针对insert，update，delete语句而设置。

### 事务四大特性

在写入或更新资料的过程中，为保证事务(transaction)是正确可靠的，所必须具备的4个特性（ACID）：

- 原子性(Atomicity):

  - 事务中的所有操作，要么全部完成要么全部不完成，不会结束在中间某个环节。
  - 事务在执行过程中发生错误，会被回滚(Rollback)到事务开始前的状态。

- 一致性(Consistency):

  - 在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设规则，这包含资料的精确度，串联性以及后续数据库可以自发性地完成预定的工作。

- 隔离性(Isolation):

  并发事务之间互相影响的程度，比如一个事务会不会读取到另一个未提交的事务修改的数据。在事务并发操作时，可能出现的问题有：

  - **脏读**：事务A修改了一个数据，但未提交，事务B读到了事务A未提交的更新结果，如果事务A提交失败，事务B读到的就是脏数据
  - **不可重复读**：在同一个事务中，对于同一份数据读取到的结果不一致。比如，事务B在事务A提交前读到的结果，和提交后读到的结果可能不同。不可重复读出现的原因就是事务并发修改记录，要避免这种情况，最简单的方法就是对要修改的记录加锁，这会导致锁竞争加剧，影响性能。另一种方法是通过MVCC可以在无锁的情况下避免不可重复读。
  - **幻读**：在同一个事务中，同一个查询多次返回的结果不一致。事务A新增了一条记录，事务B在事务A提交前后各执行了一次查询操作，发现后一次比前一次多了一条记录。幻读是由于并发事务增加记录导致的，这个不能像不可重复读通过记录加锁解决，因为对于新增的记录根本无法加锁。需要将事务串行化，才能避免幻读。

  事务的隔离级别从低到高有：

  1. 读取未提交(Read uncommitted)
     - 所有事务都可以看到其他未提交事务的执行结果
     - 本隔离级别很少用于实际应用，因为它的性能也不必其他级别好多少。、
     - 会出现脏读(dirty read)：读取到未提交的数据
  2. 读提交(read committed)
     - 这是大多数数据库系统的默认隔离级别（但不是MySQL默认的）
     - 它满足了隔离的简单定义：一个事务只能看见已经提交事务做的改变
     - 会出现不可重复读(nonrepeatable read)：在同一个事务中执行完全相同的select语句可能看到不一样的结果。导致这种情况的原因：
       - 有一个交叉的事务有新的commit，导致数据改变
       - 一个数据库被多个实例操作时，同一事物的其他实例在该实例处理其间可能会有新的commit
  3. 可重复读(repeatable read)
     - 这是mysql默认事务隔离级别
     - 它确保同一事务的多个实例在并发读取数据时，会看到同样的数据行
     - 此级别可能会出现幻读(phantom read): 当用户读取某一范围的数据行时，另一个事务又在该范围内插入了新行，用户再读取该范围数据行时，会发现有新的幻影行。
     - innodb通过多版本并发控制(mvcc, multiversion concurrency control)机制解决幻读问题
     - innodb还通过间隙锁解决幻读问题
  4. 串行化(serializable)
     - 这是最高的隔离级别
     - 它通过强制事务排序，使之不可能相互冲突，从而解决幻读问题。简言之，它是在每个读的数据行上加上共享锁。
     - 在这个级别，可能导致大量的超时现象和锁竞争

- 持久性(durability):

  事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。



### 语法与使用

- 开启事务：`begin` 或 `start transaction`

- 提交事务：`commit`

- 回滚：`rollback`撤销正在进行的所有未提交的修改

- 创建保存点：`savepoint identifier`

- 删除保存点：`release savepoint identifier`

- 把事务回滚到保存点：`rollback to identifier`

- 查询事务的隔离级别：`show variables like '%isolation%';`

- 设置事务的隔离级别：

  ```mysql
  set [session | global] transaction isolation level { read uncommitted | read committed | repeatable read | serializable}
  ```

  InnoDB提供的隔离级别有：

  - `READ`
  - `UNCOMMITTED`
  - `READ COMMITTED`
  - `REPEATABLE READ`
  - `SERIALIZABLE`



### 示例

```mysql
create table person( 
id int unsigned primary key auto_increment, 
name varchar(10) not null, 
age tinyint,
money float) 
charset=utf8; 

begin;
insert into person values(1, 'lily', 16, 2000);
insert into person values(2, 'tony', 15, 0);
commit;

begin;
update person set money=500 where name='tony';
update person set money=1500 where name='lily';
rollback;
commit;
```



## 5.2 存储过程

不常用

存储过程(stored procedure) 是一种在数据库中存储复杂程序，一遍外部程序调用的一种数据库对象。

存储过程是为了完成特定功能的sql语句集，经编译创建并保存在数据库中，用户可通过指定存储过程的名字并给定参数（需要时）来调用执行。

存储过程思想上很简单，就是数据库sql语言层面的代码封装与重用。

- 优点：
  - 存储过程可封装，并隐藏复杂的商业逻辑
  - 存储过程可以返回值，可以接收参数
  - 存储过程无法使用select指令来运行，因为它是子程序，与查看表，数据表或用户定义函数不同。
  - 存储过程可用在数据检验，强制实行商业逻辑等。
- 缺点
  - 存储过程往往定制化于特定的数据库上；因为支持的编程语言不同，当切换到其他厂商的数据库系统时小重写原有的存储过程。
  - 存储过程的性能调校与撰写受限于各种数据库系统。

### 语法

1. 声明语句结束符，可以自定义：

   存储过程中有很多sql语句，sql语句的后面为了保证语法结构必须要有分好`;`,但是默认情况下分号表示客户端代码发送到服务器执行。必须更改结束符。(mycli 不支持)

   ```mysql
   delimiter //; -- 结束符改成 //
   -- 或
   delimiter $$; -- 结束符改成 $$
   ```

2. 声明存储过程：

   ```mysql
   create procedure demo_in_parameter(in p_in int)
   ```

3. 存储开始和结束符号：

   ```mysql
   begin ... end
   ```

4. 变量赋值：

   ```mysql
   set @p_in=1
   ```

5. 变量定义：

   ```mysql
   declare l_int int unsigned default 400000;
   ```

   

6. 创建mysql存储过程，存储函数

   ```mysql
   create procedure 存储过程名(参数)
   ```

7. 存储过程体：

   ```mysql
   create function 存储函数名(参数)
   ```

   

### 使用

- 简单用法

  ```mysql
  -- 定义
  -- 如果存储过程中就一条sql语句，begin...end两个关键字可以省略
  create procedure get_info()
  select * from student;
  
  -- 调用
  call get_info();
  ```

- 复杂一点的(只能在mysql中使用，mycli无法识别)

  ```mysql
  delimiter //
  create procedure foo(in uid int, in hello_str varchar(32))
  begin
  select hello_str;
  select * from person limit uid;
  select * from score limit uid;
  end//
  delimiter ;//
  
  -- 查询
  show procedure status like '%foo%';
  
  -- 删除(这个程序会一直存在)
  drop procedure foo;
  ```

  

## 5.3 python操作

安装`pip3 install pymysql`

这个用的也不多

```python
import pymysql

# 打开一个数据库的连接
# db = pymysql.connect() # 结果是一个connection类型的对象
#  db.cursor() 获取到一个cursor对象，用它来操作数据库

# with pymysql.connect() as cursor # x 的结果就是一个cursor对象
db = pymysql.connect(host='localhost', # 119.45.58.134
                     user='light',  
                     password='!Light2077', 
                     database='lightdb', 
                     port=3306, 
                     charset='utf8')

cursor = db.cursor()
cursor.execute('select * from student')
db.commit()
cursor.close()
print(cursor.fetchone())
print(cursor.fetchall())  # 拿到的是一个元组
# 关闭连接
db.close()
```



## sql注入

通过一些手段影响sql语句的输入，就是sql注入。

```python
import pymysql, hashlib

# 打开一个数据库的连接
# db = pymysql.connect() # 结果是一个connection类型的对象
#  db.cursor() 获取到一个cursor对象，用它来操作数据库

# with pymysql.connect() as cursor # x 的结果就是一个cursor对象
username = input('请输入用户名')
password = input('请输入密码')
h = hashlib.md5()
h.update(password.encode('utf8'))
password = h.hexdigest()

db = pymysql.connect(host='localhost', # 119.45.58.134
                     user='light',  
                     password='!Light2077', 
                     database='lightdb', 
                     port=3306, 
                     charset='utf8')

cursor = db.cursor()
sql = "select * from account where username='%s' and password='%s'" % (username, password)

cursor.execute(sql)

# 更安全的做法
# sql = "select * from account where username='%s' and password='%s'"
# cursor.execute(sql, (username, password))

db.commit()
cursor.close()
# print(cursor.fetchone())
# print(cursor.fetchall())  # 拿到的是一个元组
# 关闭连接
db.close()

result = cursor.fetchone()
# 有个bug，输入lilyy'# sql语句相当于变成
# select * from account where username='lilyy'# and password='%s'
# 井号后面都是注释
if not result:
    print('用户名或密码错误')
else:
    print(cursor.fetchone())
    print('欢迎回来%s' % username)
```

## 5.5 数据备份与恢复

```mysql
-- 备份 : 在当前目录下备份
mysqldump -h localhost -u root -p dbname > dbname.sql

-- 恢复
mysql -h localhost -u root -p123456 dbname < ./dbname.sql
```

主从复制，有一个主表，几个从表。读写分离，读取从表的数据，操作主表的数据。



# 练习

```mysql
-- 部门表 [部门编号deptno 部门名称dname 部门地址loc]
create table dept(
deptno int primary key,
dname varchar(14),
loc varchar(13)
)charset=utf8;

-- 添加数据
insert into dept values(10, 'accounting', 'NEW YORK');
insert into dept values(20, 'research', 'DALLAS');
insert into dept values(30, 'sales', 'CHICAGO');
insert into dept values(40, 'operations', 'BOSTON');
```



```mysql
-- 员工表emp [员工编号empno 员工姓名ename 员工工作job 员工直属领导编号mgr]
-- [入职时间hiredate 工资sal 奖金comm 部门编号deptno]
create table emp(
empno int primary key,
ename varchar(10),
job varchar(9),
mgr int,
hiredate date,
sal double,
comm double,
deptno int
)charset=utf8;

insert into emp values(7369,'smith', 'clerk', 7902,'1980-12-17',800,NULL,20);
insert into emp values(7499,'allen', 'salesman', 7698,'1981-2-20',1600,300,30);
insert into emp values(7521,'ward', 'salesman', 7698,'1981-2-22',1250,500,30);
insert into emp values(7566,'jones', 'manager', 7839,'1981-4-2',2975,NULL,20);
insert into emp values(7654,'martin', 'salesman', 7698,'1981-9-28',1250,1400,30);
insert into emp values(7698,'blake', 'manager', 7839,'1981-5-1',2850,NULL,30);
insert into emp values(7782,'clark', 'manager', 7839,'1981-6-9',2450,NULL,10);
insert into emp values(7788,'scott', 'analyst', 7566,'1987-7-3',3000,NULL,20);
insert into emp values(7839,'king', 'president', NULL,'1981-11-17',5000,NULL,10);
insert into emp values(7844,'turner', 'manager', 7698,'1981-9-8',1500,0,30);
insert into emp values(7876,'adams', 'clerk', 7788,'1987-7-13',1100,NULL,20);
insert into emp values(7900,'james', 'clerk', 7698,'1981-12-3',950,NULL,30);
insert into emp values(7902,'ford', 'analyst', 7566,'1981-12-3',3000,NULL,20);
insert into emp values(7934,'miller', 'clerk', 7782,'1981-1-23',1300,NULL,10);
```



```mysql
-- 工资等级表salgrade [等级grade 最低工资lowasl 最高工资hisal]
create table salgrade(
grade int,
lowsal double,
hisal double
);

insert into salgrade values (1, 700, 1200);
insert into salgrade values (2, 1201, 1400);
insert into salgrade values (3, 1401, 2000);
insert into salgrade values (4, 2001, 3000);
insert into salgrade values (5, 3001, 9999);
```



1.找出姓名以a,b,s开始的员工信息

```mysql
-- 正则表达式 regexp
select * from emp where ename rlike "^[abs]";
-- left(字段, 个数) 获取指定字段中左边的的指定个数的子串
select * from emp where left(ename, 1) in ('a', 'b', 's');
```

2.返回员工的详细信息并按姓名排序

```mysql
select * from emp order by ename asc;

select * from emp order by ename desc;
```

3.返回员工的信息并按工作降序 工资升序排序

```mysql
select * from emp order by job desc, sal asc;
```

4.返回拥有员工的部门名，部门号

```mysql
-- select dname, dept.deptno from dept inner join emp on dept.deptno=emp.deptno
-- 直接这么写，编号和部门名重复
select dname, dept.deptno from dept inner join emp on dept.deptno=emp.deptno group by dept.deptno;

select distinct(dname), dept.deptno from dept inner join emp on dept.deptno=emp.deptno

-- 
```

5.工资高于turner的员信息

```mysql
select * from emp where sal >= (select sal from emp where ename='turner');
```

6.返回员工和所属的经理姓名(难-自连接)

```mysql
select empno, ename, mgr from emp;

select e.ename, m.ename from emp as e inner join emp as m on e.mgr = m.empno;
```

7.返回雇员的雇佣日期早于其经理雇佣日期的员工及其经理姓名

```mysql
select e.ename, e.hiredate, m.ename, m.hiredate from emp as e inner join emp as m on e.mgr = m.empno where e.hiredate < m.hiredate;
```

8.返回员工姓名及其所在部门名称

```mysql
select ename, dname from emp inner join dept on emp.deptno=dept.deptno;
```

9.返回从事clerk工作的员工姓名和所在部门名称

```mysql
select ename, dname from emp inner join dept on emp.deptno=dept.deptno where job='clerk';
```

10.返回部门号及其本部门的最低工资

```mysql
select dept.deptno, min(sal) from dept inner join emp on dept.deptno=emp.deptno group by dept.deptno;
```

11.返回销售部(sales)所有员工的姓名

```mysql
select ename from emp inner join dept on dept.deptno=emp.deptno where dept.dname='sales';
```

12.返回与scott从事相同工作的员工

```mysql
select ename from emp where job=(select job from emp where ename='scott');
```

13.返回员工的详细信息（包括部门名称及部门地址）

```mysql
select emp.*, dept.dname, dept.loc from emp left join dept on dept.deptno=emp.deptno;
```

14.返回员工工作及其从事此工作的最低工资

```mysql
select job, min(sal) from emp group by job; 
```

15.返回工资处于第四级别的员工的姓名

```mysql
select * from emp where sal between (select lowsal from salgrade where grade=4)
and (select hisal from salgrade where grade=4);

select * from emp, salgrade where emp.sal between salgrade.lowsal and salgrade.hisal and salgrade.grade=4;

select * from emp inner join salgrade on sal between salgrade.lowsal and salgrade.hisal and salgrade.grade=4;
```

16.返回工资为2等级的职员姓名，部门所在地，和2等级的最低最高工资

```mysql
select ename, loc, lowsal, hisal from emp, dept, salgrade where salgrade.grade=2 and emp.deptno=dept.deptno and emp.sal between salgrade.lowsal and salgrade.hisal;
```

17.工资等级高于turner的员工信息

```mysql
-- 分解1：找到turner员工的工资等级
select grade from salgrade inner join emp on sal between lowsal and hisal where ename='turner';

-- 分解2：找到高于等级3的员工信息
select * from emp inner join salgrade on sal between lowsal and hisal where grade > 3;

select * from emp inner join salgrade on sal between lowsal and hisal and grade > (select grade from salgrade inner join emp on sal between salgrade.lowsal and salgrade.hisal where emp.ename='turner');
```



















