# Redis与MongoDB

mysql qps==5k-8k(queries per second)

redis == 11k qps

NoSQL数据库按照其存储类型可以大致分为以下几类：

| 类型       |                                             |                                                              |
| ---------- | ------------------------------------------- | ------------------------------------------------------------ |
| 列族数据库 | **Hbase**<br />Cassandra<br />Hypertable    | 顾名思义是按列存储数据的。最大的特点是方便存储结构化和半结构化数据，方便做数据压缩，针对某一列或几列的查询有非常大的IO优势，适合于批量数据处理和即时查询。 |
| 文档数据库 | **MongoDB**<br />CouchDB<br />ElasticSearch | 文档数据库一般用类json格式存储数据，存储的内容是文档型的。这样也就有机会对某些字段建立索引，实现关系数据库的某些功能，但不提供对参照完整性和分布事务的支持。 |
| KV数据库   | DynamoDB<br />Redis<br />LevelDB            | 可以通过Key快速查到其Value，有基于内存和基于磁盘两种实现方案 |
| 图数据库   | Neo4J<br />FlockDB<br />JanusGraph          | 使用图结构进行语义查询的数据库，它使用节点，边和属性来表示和存储数据。图数据库从设计上，就可以简单快速的检索难以在关系系统中建模的复杂层次结构。 |
| 对象数据库 | db4o<br />Versant                           | 通过类似面向对象语言的语法操作数据库，通过对象的方式存取数据 |

http://nosql-database.org/

## Redis 入门

将数据放在内存里，读写数据惊人。也提供了持久化机制，把内存数据保存到硬盘上。非常善于处理高速缓存和消息队列的服务。百度，新浪，优酷 等等都使用redis

### 1. 简介

remote dictionary server，使用ANSI C编写的高性能key-value存储系统。特点：

- 读写性能极高，并且有丰富的特性（发布/订阅、事务、通知等）
- 支持数据持久化（RDB和AOF两种方式）可以将内存中的数据保存在磁盘中，重启的时候就可以再次进行使用
- 支持多种数据类型，string，hash，list，set，zset，bitmap，hyperloglog等
- 支持主从复制（实现读写分析）以及哨兵模式（监控master是否宕机并自动调整配置）
- 支持分布式集群，可以很容易的通过水平扩展来提升系统整体性能
- 基于TCP提供的可靠传输服务进行通信，很多编程语言都提供了redis客户端支持。

### 2. Redis的应用场景

- 高速缓存：将不常变化但又经常被访问的热点数据放到redis数据库中，可以大大降低关系型数据库的压力，从而提升系统的响应性能。
- 排行榜：很多网站都有排行榜功能，利用redis的列表和有序集合可以非常方便的构造各种排行榜系统
- 商品秒杀/投票点赞 redis提供了对计数操作的支持，网站上常见的秒杀、点赞等功能都可以利用redis的计数器通过+1或-1的操作实现，从而避免了使用关系型数据库的`update`操作
- 分布式锁：利用redis可以跨多台服务器实现分布式锁（类似线程锁，但是能够被多台机器上的多个线程或进程共享）的功能，用于实现一个阻塞式操作。
- **消息队列**：消息队列和高速缓存一样，是一个大型网站不可缺少的基础服务，可以实现业务解耦和非实时业务削峰等特性。

### 3. redis的安装和配置

https://redis.io/



安装报错的解决方案

https://blog.csdn.net/realize_dream/article/details/106483499

cd到解压后的文件夹可以看到已经有makefile文件了

```shell
wget http://download.redis.io/releases/redis-6.0.6.tar.gz

tar -zxvf redis-6.0.6.tar.gz
cd redis-6.0.6/
sudo make && sudo make install
```

### 4. redis启动

但是退出这个页面，redis就关闭了

```
redis-server
```

### 5. redis的配置

在redis源代码目录下有一个名为redis.conf的配置文件，我们可以先查看一下该文件

把这个文件复制到`/usr/local/etc/redis.conf`

然后以后就这样启动：

```
redis-server /usr/local/etc/redis.conf
```

修改配置文件

1. 配置将redis服务绑定到指定的ip地址和端口

   我这里把ip改成了`0.0.0.0`

   ```
   bind 127.0.0.1
   port 6379
   ```

2. 设置后台运行（以守护进程方式运行）

   ```
   daemonize yes
   ```

3. 设置日志级别（debug：调试，verbose：详细，notice：通知，warning：警告）

   ```
   loglevel warning
   ```

4. 配置数据库的数量，默认16个

   ```
   database 16  # redis数据库不需要自己新建
   ```

5. 配置数据写入规则

   有可能会修改数据

   ```
   save 900 1  # 900 秒 (15 分钟) 内修改过 1 个key 写入一次数据库
   save 300 10 # 300秒内修改过10个key 写入一次数据库
   save 60 10000 #get
   ```

6. 配置redis的持久化机制RDB

   默认的方式，直接镜像内存里的数据，把数据保存到dump.rdb文件里。这个文件在下面可以改。

   ```
   rdbcompression yes  # 压缩RDB文件
   rdbchecksum yes # 对 RDB 文件进行校验
   dbfilename dump.rdb  # RDB 数据库文件的文件名
   dir /var/local/redis  # RDB 文件保存的目录
   ```

7. 配置redis的持久化机制-AOF

   append only file模式

   ```
   appendonly no
   appendfilename "appendonly.aof"
   ```

8. 配置redis的主从复制，通过主从复制可以实现读写分离

   ```
    364 ################################# REPLICATION #################################
    365 
    366 # Master-Replica replication. Use replicaof to make a Redis instance a copy of
    367 # another Redis server. A few things to understand ASAP about Redis replication.
    368 #
    369 #   +------------------+      +---------------+
    370 #   |      Master      | ---> |    Replica    |
    371 #   | (receive writes) |      |  (exact copy) |
    372 #   +------------------+      +---------------+
    373 #
    374 # 1) Redis replication is asynchronous, but you can configure a master to
    375 #    stop accepting writes if it appears to be not connected with at least
    376 #    a given number of replicas.
    377 # 2) Redis replicas are able to perform a partial resynchronization with the
    378 #    master if the replication link is lost for a relatively small amount of
    379 #    time. You may want to configure the replication backlog size (see the next
    380 #    sections of this file) with a sensible value depending on your needs.
    381 # 3) Replication is automatic and does not need user intervention. After a
    382 #    network partition replicas automatically try to reconnect to masters
    383 #    and resynchronize with them.
    384 #
    385 # replicaof <masterip> <masterport>
   
   ```

9. 配置慢查询

   ```
   slowlog-log-slower-than 10000 # 一次操作超过10000毫秒被视作一次慢查询
   slowlog-max-len 128 # 最多纪录128次慢查询
   ```

   



```
set name zhangsan # {'name':'zhangsan'}
set age 18 ex 3 # 设置过期时间为3秒

get name
get age
```



### 6. Redis持久化

redis在运行时，所有的数据都保存在内存里，进程结束以后，会将数据写入到硬盘中。启动时，会读取硬盘里的内容，并将内容全部加载到内存中(会占用大量内存)

工作中会两个方式一起使用：读取rdb文件，读取aof文件，删除aof文件。

- RDB

  默认的持久化方式，是对内存中的数据进行镜像，并以二进制的形式保存在dump.rdb文件中。会根据配置文件的时间节点对文件进行持久化。

  优点：速度快，直接镜像内存的数据，文件小

  缺点：在两次保存间隔内的数据有可能丢失。

- AOF

  Append only file，将修改的每一条指令记录进appendonly.aof中，需要修改配置文件来打开aof功能

  ```
  appendfsync always # 每次有新命令追加到aof文件时就执行一次持久化，非常慢但是安全
  appendfsync everysec # 每秒执行一次持久化，和使用rdb持久化差不多，并且在故障时只会丢失1秒钟的数据
  appendsync no # 不执行持久化
  ```

  优点：适合保存增量数据，数据不丢失。

  缺点：文件体积大，恢复时间长

## Redis 操作

启动redis-cli

```
redis-cli
```

最最基础操作

```
> set name lily
OK
> get name
"lily"
```



http://redisdoc.com/

http://doc.redisfans.com/

### string类型

```

set age 10 ex 3  # 3秒后失效
set age 10 px 100  # 100 毫秒后失效

ttl age  # 可以查看过期时间 -1 表示不会过期
```



```
setnx name amy  # 如果name已经存在，该操作无效
```



```
mset p 20 q 30 t 50 m 60  # 一次性设置多个值
```



```
strlen name
```



```
incr age  # 自增1
incrby age 10 # 增加10

decr # 减1
decrby 10 # 减10
```

### 哈希表

类似字典又套了一个字典

```
# hset 
hset person name lily age 18
hset person addr beijing height 170

# hget 
hget person name

# hgetall 拿到所有的kv
hgetall person

# hexists : 有这个属性返回1 无返回0
hexists person name
hexists person school

# hdel 删掉属性
hdel person addr height

# hlen 查看有几个属性
hlen person

# hstrlen 查看某个属性值字符串长度
hstrlen person name 

# hkeys 查看所有的key
hkeys

# hvals 查看所有的value
hvals

# hmset
# hmget
```

### 列表

redis的列表可以实现类似于队列和栈的结构

```
# 这两个结合到一起，输出的循序是反过来的。
# 因为是lpush
# zhangsan
# lisi zhangsan
# wangwu lisi zhangsan
lpush names zhangsan lisi wangwu
lrange names 0 -1

rpush names jack tony jerry
lrange names 0 -1

# lpop names
# rpop names

lset names 2 rose  # 相当于names[2]=rose
llen names

lindex names 3 # 相当于names[3]

```

### 集合

```
sadd g1 a b c d
sadd g2 c d e f

sismember g1 a
sismember g1 e

# 随机取2个
srandmember g1 2

smembers g1

sdiff # 差
sunion # 并
sinter # 交
```

### 有序集合

```
zadd rank 5 a 2 b 3 c 4 d

zrange rank  # 按照排序展示
zrank rank c  # 查看级别

zrevrange rank 0 -1
zrevrange rank 0 -1 withscores

zincrby rank 5 a
```

## python代码

`pip3 install redis`

redis模块的核心是名为redis的类，该类的对象代表一鸽redis客户端，通过该客户端可以向redis服务器发送命令并获取执行的结果。上面我们在redis客户端中使用的命令基本上就是redis对象可以接收的消息，所以如果了解了redis的命令就可以在python中玩转redis

```python
import redis
client = redis.Redis(host='1.2.3.4', port=6379, password='123')
client.set('username', 'admin')

client.hset('student', 'name', 'hao')

client.hset('student', 'age', 38)

client.keys('*')

client.get('username')

client.hgetall('student')
```

