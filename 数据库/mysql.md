# 1. 数据库概述

CURD创建（Create）、更新（Update）、读取（Retrieve）和删除（Delete）

数据库管理系统（Database Manage System）：管理数据库的软件，用于建立和维护数据库，比如MySQL。

SQL（Structure Query Language）结构化查询语言。SQL是通过数据库软件（DBMS）和数据库（DB）通信的工具。

## 1.1 数据库分类和常见数据库

关系型数据库和非关系型数据库

- 关系型：采用关系模型（二维表）来组织数据结构的数据库
- 非关系型：不采用关系模型组织数据结构的数据库。例如：Redis、MongoDB

开源数据库和非开源数据库

- 开源：MySQL、SQLite、MongoDB
- 非开源：Oracle、SQL Server、DB2

常见关系型数据库

| 数据库软件名称 | 所属公司          | 费用      | 适用场景     |
| -------------- | ----------------- | --------- | ------------ |
| SQLite         | 开源              | 免费      | 嵌入式项目   |
| MySQL          | Oracle（甲骨文）  | 免费/收费 | 中小型项目   |
| SQL Server     | Microsoft（微软） | 版本付费  | 大中型项目   |
| Oracle         | Oracle（甲骨文）  | 授权费/年 | 大型项目     |
| OceanBase      | Alibaba（阿里）   | 方案付费  | 企业级分布式 |

> MySQL 并不是所有版本都是免费的，MySQL 各版本及费用介绍如下:
>
> 1、 MySQL Community Server 社区版本，开源免费，但不提供官方技术支持。
> 2、MySQL Enterprise Edition 企业版本，需付费，可以试用30天。
> 3、 MySQL Cluster 集群版，开源免费。可将几个MySQL Server封装成一个Server。
> 4、 MySQL Cluster CGE 高级集群版，需付费。
> MySQL Community Server 是开源免费的，这也是我们通常用的MySQL的版本。  

> **Oracle商业收费标准简介**
> Oracle软件本身是免费的，所以任何人都可以从Oracle官方网站下载并安装Oracle的数据库软件，收费的是License，即软件授权，如果数据库用于商业用途，就需要购买相应Oracle产品的License。
> 现在Oracle有两种授权方式，按CPU(Process)数和按用户数(Named User Plus)。前一种方式一般
> 用于用户数不确定或者用户数量很大的情况，典型的如互联网环境，而后一种则通常被用于用户数
> 确定或者较少的情况。  

# 2. MySQL入门

https://dev.mysql.com/downloads/windows/installer/8.0.html  

启动与连接

本地连接可省略 -h 选项。

```
mysql -h localhost -u root -p 123456
```



