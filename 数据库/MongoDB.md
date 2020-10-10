# 1. MongoDB介绍

- C++编写
- 面向文档的数据库管理系统

https://www.mongodb.com/

https://docs.mongodb.com/guides/server/install/

# 2. MongoDB的安装和配置

```shell
sudo yum install mongodb-server -y  # MongoDB 服务端
sudo yum install mongodb -y  # 安装 MongoDB 客户端
sudo mongod -f /etc/mongod.conf  # 加载配置项，启动 MongoDB 服务器

mongo  # 进入客户端
```

> MongoDB默认保存数据的路径是`/data/db`目录，为此要提前创建该目录。此外，在使用mongod启动服务器时，`--bind_ip`参数用来将服务器绑定到指定的ip地址，也可以用`--port`参数来指定端口，默认端口为27017

# 3.基本操作

[《MongoDB权威指南》](http://www.ituring.com.cn/book/1172)

```
# 终端的方式操作MongoDB基本不会涉及
show databases; 显示所有数据库

use lightdb  # 直接创建一个表
switched to db lightdb  # 换数据库

db.createCollection('student')  # 创建一个表
db.createCollection('teacher')

show collections  # 查看表
# 增
db.student.insert({'name':'zhangsan', 'age':18});
db.student.insert({'name':'lisi', 'age':16})

# 查
db.student.find()  # 查找所有数据
db.student.find().pretty()

# 改
db.student.update({'name':'zhangsan'}, {'name':'jerry', 'age':22})

# 删
db.student.delete
db.teacher.drop() # 删除teacher这个表
db.dropDatabase()  # 删除当前数据库
```

# 4. python使用mongodb

`pip install pymongo`

```python
from pymongo import MongoClient

client = MongoClient()

client = MongoClient(host='localhost', port=27017)

# 获取到一个数据库对象
db = client.lightdb

# db.collection_name 获取到一个表可以进行增删改查的操作
db.student.insert({'name':'alex', 'age':18})
# 拿到的结果是一个cursor对象，可迭代
cursor = db.student.find()
for s in cursor:
    print(s)
```

