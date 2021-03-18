# 1. MongoDB介绍

- C++编写
- 面向文档的数据库管理系统

https://www.mongodb.com/

https://docs.mongodb.com/guides/server/install/

MongoDB 的设计目标是高性能、可扩展、易部署、易使用，存储数据非常方便

是一个基于分布式文件存储的数据库。
由C++语言编写。旨在为WEB应用提供可扩展的高性能数据存储解决方案。

MongoDB 是一个介于关系数据库和非关系数据库之间的产品，
是非关系数据库当中功能最丰富，最像关系数据库的。

支持json 和复杂的BSON（Binary Serialized Document Format）数据格式

支持的查询语言非常强大，其语法类似于SQL查询语言

支持对数据建立索引

## 使用场景

- 网站数据：Mongo 非常适合实时的插入，更新与查询，并具备网站实时数据存储所需的复制及高度伸缩性
- 缓存：由于性能很高，Mongo 也适合作为信息基础设施的缓存层。在系统重启之后，由Mongo 搭建的持久化缓存层可以避免下层的数据源过载
- 高伸缩性的场景：Mongo 非常适合由数十或数百台服务器组成的数据库，Mongo 的路线图中已经包含对MapReduce 引擎的内置支持。
- 对象及JSON 数据的存储：Mongo 的BSON 数据格式非常适合文档化格式的存储及查询
- 不建议使用mongodb
  - 高度事务性的系统：例如，银行或会计系统
  - 传统的商业智能应用：针对特定问题的BI 数据库会产生高度优化的查询方式
  - 需要SQL 的问题

# 2. MongoDB的安装和配置

[Windows本地部署](https://www.cnblogs.com/manicstt/p/12391015.html)

```shell
sudo yum install mongodb-server -y  # MongoDB 服务端
sudo yum install mongodb -y  # 安装 MongoDB 客户端
sudo mongod -f /etc/mongod.conf  # 加载配置项，启动 MongoDB 服务器

mongo  # 进入客户端
```

> MongoDB默认保存数据的路径是`/data/db`目录，为此要提前创建该目录。此外，在使用mongod启动服务器时，`--bind_ip`参数用来将服务器绑定到指定的ip地址，也可以用`--port`参数来指定端口，默认端口为27017

## docker安装

https://www.cnblogs.com/smiler/p/10112676.html

```
docker pull mongo
```

-p 宿主机端口:容器端口

```
docker run -dit --name mongo1 -p 27017:27017 mongo
```

注意开启云服务器的端口

进入容器内部

```
 docker exec -it mongo1 sh
```

```
show dbs
```

# 3.基本概念

## 文档

文档是 MongoDB 中数据的基本单位，类似于关系数据库中的行（但比行复杂），可以理解为一个json对象

多个键及其关联的值有序地放在一起就构成了文档

如

```
{"name": "jack", "age": 17}
```

支持的数据类型： 字符类型、整型、浮点型、布尔型(string，int，float，timestamp，binary)

注意：文档中的键值对是有序的

比如`{"name":"disen", "id":123}`和`{"id":123，"name":"disen"}`是两个不同的文档

## 集合

集合就是一组文档，类似于关系数据库中的表

集合是无模式的，集合中的文档可以是各式各样的。集合中可以存放任何类型的文档

为了方便查询可以将结构相同的文档放在同一个集合中。如某业务功能，分user集合，权限集合等

MongoDB推荐使用以命名空间方式命名子集合， 如login.user, login.role

- login. 即是命名空间。注意：login.命名空间 跟 login集合没有任何关系 

## 数据库

由多个文档组成集合，多个集合组成数据库，一个MongoDB 实例可以承载多个数据库

每个数据库都是独立的，即都有独立的权限控制

在磁盘上，不同的数据库存放在不同的文件中

MongoDB 中已存在的系统数据库 

**Admin 数据库**：权限数据库，如果创建用户的时候将该用户添加到admin 数据库中，那么该用户就自动继承了所有数据库的权限。
**Local 数据库**：数据库永远不会被同步到其它节点，可以用来存储本地单台服务器的任意集合
**Config 数据库**：当使用分片模式时，config 数据库在内部使用，用于保存分片的信息

# 4.基本操作

[《MongoDB权威指南》](http://www.ituring.com.cn/book/1172)

进入mongodb环境

```
mongo
```

显示所有数据库

```
show dbs
```

显示所有用户

```
show users
```

显示数据库操作命令

```
db.help()
```

删除当前数据库

```
db.dropDatabase()
```



## 集合操作

创建一个数据库，如果已经存在就切换到这个数据库

```
use lightdb
```

显示当前数据库中的集合

```
show collections
```

创建集合（MongoDB 其实在插入数据的时候，也会自动创建对应的集合，无需预定义集合）

options表示可选参数：

- capped：如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。当该值为 true 时，必须指定 size 参数。
- autoIndexId：如为 true，自动在 _id 字段创建索引。默认为 false。
- size：为固定集合指定一个最大值（以字节计）。如果 capped 为 true，也需要指定该字段。
- max：指定固定集合中包含文档的最大数量

```
db.createCollection('my_col'[, options])
```

删除指定的集合

```
db.my_col.drop()
```

## 数据操作

### 插入数据

都会自动创建_id值，如果_id已存在，insert**不做任何操作**，save会更新

```
db.my_col.insert({_id:1, name: 'disen', age: 20})
db.my_col.save({_id:1, name: 'disen', age: 19})
```

### 查找数据

criteria ：查询条件，可选 
filterDisplay：筛选显示部分数据，显示指定列数据

```
db.my_col.find(criteria, filterDisplay) 
```

 查询所有记录

```
db.my_col.find()
```

查询所有记录，并友好地显示出来，pretty() 是以格式化方式显示文档信息

```
db.my_col.find().pretty()
```

显示所有记录的name和age：

- 1：要显示的key
- 0: 不要显示的key

注意： 要么都为1，要么都为0

```
db.my_col.find({},{name:1, age:1})
```



```
db.my_col.find({name: 'disen'})
```



```
db.my_col.find({name:'disen', age:20})
```



```
db.my_col.find({$or: [{age: 22}, {age: 25}]})
```

查询age > 20的记录

`$or`

`$lt` 小于

 `$lte` 小于等于 

`$gt` 大于 

`$gte`大于等于 

`$ne`不等于

`$regex`正则表示

```
db.my_col.find({"age":{$gt: 20}})
```

查找 age 在 (20, 30)之间的纪录

```
db.my_col.find({age : {$lt :30, $gt : 20}})
```

显示_id为1,3和5的文档记录

```
db.my_col.find({_id:{$in: [1,3,5]}})
```

查询 name的key中包含 y字符的所有文档记录

```
db.my_col.find({name: {$regex: "y"}})
```

查找所有，并按age升序排列，1 升序，-1 降序

```
db.my_col.find().sort({age:1})
```

### 修改数据

criteria: update的查询条件

objNew : update的对象和一些更新的操作符（如$set）等

upsert : 如果不存在update的记录，是否插入objNew，true为插入
	默认是false，不插入

multi: mongodb默认是false,只更新找到的第一条记录，如果为true,按条件查出来多条记录全部更新
	默认false，只修改匹配到的第一条数据。 

```
db.my_col.update(criteria, objNew, upsert, multi ) 
```



```
db.my_col.update({name: 'disen'}, {$set: {age: 30}}, false, true) 
```



### 删除数据

```
db.my_col.remove({name: 'cici'})
```

## 执行脚本

```
 load("/home/apple/addbank.js")
```

脚本路径必须是绝对路径

脚本内容示例

```
db.bank.insert({_id:1,name:"abc",address:"ccddddhh"})
db.bank.insert({_id:2,name:"bcd",address:"ffffddd"})
```



## 备份数据

备份是zhaopin库的jobs集合
-o 指定存放的目录

```
mongodump -d zhaopin -c jobs -o jobs
```

将zhaopin库的所有集合，备份到当前目录中，默认存放在dump子目录中

```
mongodump -d zhaopin
```

注： 将集合数据备份*.bson文件 此文件是用于恢复指定集合的数据

## 恢复数据

恢复指定db库的某一集合(collections)

```
mongorestore -d zhaopin -c jobs dump/zhaopin/jobs.bson
```

恢复dump/zhaopin目录下所有*.bson文件的集合

```
mongorestore -d zhaopin dump/zhaopin
```



# 5. python使用mongodb

https://docs.mongodb.com/getting-started/python/client/

安装库

```
pip install pymongo
```

## MongoDB授权

### 进入mongo系统

打开库

```
use admin
```

创建用户

```
db.createUser( {user: "admin",pwd: "admin0987",roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]})
```

删除用户

```
db.dropUser(用户名)
```

认证是否成功

```
db.auth("admin","admin0987")   #认证，返回1表示成功
```

### 以admin用户登录

共有3种方式

```
mongo 127.0.0.1/<数据库名> -uadmin -p
```

```
mongo <数据库名> -uadmin -p
```

```
mongo -u admin -p  --authenticationDatabase 数据库名 
```

### 修改配置文件

如果以上操作没问题，可以不用修改

```
vim /etc/mongodb.conf
```

将auth修改为true

```
auth = true
```

### 重启服务

```
service mongodb  restart
```

## python 操作



```python
from pymongo import MongoClient

# 连接数据库
client = MongoClient(host='localhost', port=27017)


db = client.admin
db.authenticate("userAdmin","admin0987")
s = db.system.users
print("--all user--")
#print(s.find_one())
for row in s.find({"user":"{$regex:/admin/i}"}):
    print(row)
    
# 获取到一个数据库对象
db = client.lightdb
# db.collection_name 获取到一个表可以进行增删改查的操作
db.student.insert({'name':'alex', 'age':18})
# 拿到的结果是一个cursor对象，可迭代
cursor = db.student.find()
for s in cursor:
    print(s)
```

## 集合操作

```python
# 获取集合
_set = db.users
_set.insert({})  # 插入
_set.save({})  # 
_set.insert([{},{}])  # 插入多条

# 查询所有
for row in _set.find()
    print(row)

"""
_set.update(
   <query>,    #查询条件
   <update>,    #update的对象和一些更新的操作符
   {
     upsert: <boolean>,    #如果不存在update的记录，是否插入
     multi: <boolean>,        #可选，mongodb 默认是false,只更新找到的第一条记录
     writeConcern: <document>    #可选，抛出异常的级别。
   }
)
"""
_set.remove({})  # 删除
```

