分布式，开放源码的分布式应用程序协调服务。是Hadoop和Hbase的重要组件。

分布式的协调服务框架啊，用于分布式环境的管理，统一命名服务，分布式环境元数据的存储，包括分布式锁服务等。

五大作用

- 集群管理：监控集群中服务节点的运行状态是正常工作还是宕机
- 集群配置信息的统一管理：可以确保集群中每台配置信息的同步和一致
- 集群监控和主备切换：能监听到主master挂了，唤醒备用master
- 集群中统一的命名服务：确保每台服务器命名的唯一性
- 集群分布式锁服务



常用指令

进入bin目录

```shell
sh zkServer.sh start
```



确认是否开启成功

```shell
jps
sh zkServer.sh status
```



启动客户端

```
sh zkCli.sh
```



创建节点

```
create /park01 hello1811
```



查看节点信息

```
get /park01 hello 1811
```

修改数据

```
set /park01 hellozk
```

删除节点

```
delete /park01/node01   # 有子节点时无法删除
rmr /park01  # 可以直接删除
```

退出

```
quit
```

### zookeeper服务端指令

```shell
sh zkServer.sh start
sh zkServer.sh status
sh zkServer.sh restart
sh zkCli.sh  # 操作客户端
sh zkServer.sh stop
```

### zookeeper四种节点

- 普通持久节点 持久指的是当前创建结点的客户端挂掉之后节点依然存在

  ```
  create /park01 123
  ```

- 普通临时节点 临时指的是当创建此节点的客户端线程挂掉之后，节点被删除

  ```
  create -e /park01 123 
  ```

- 顺序持久节点：顺序指的是在指定路径后拼上一个递增的顺序号

  ```
  create -s /park01 123
  ```

- 顺序临时节点

  ```
  create -e -s /park01 123
  ```

### zookeeper结构

- 有一个根节点

- 每个节点都可以有子节点

- 节点被称为znode节点

- 每个znode节点都可以存储数据

- 无论是查看节点还是创建节点，都要基于根节点操作

- 操作节点通过路径，比如查看`ls /park01`

- 在创建节点时， 需要为节点指定初始数据，否则不会创建节点

- 多个znode节点形成了znode树，存储了节点之间的父子关系，以及节点的信息数据和cmd下输入tree查看文档树类似

- znode树维系在内存里目的是供客户端快速查询以及快速响应

- Zookeeper不适合存储海量数据，①Zookeeper是把数据维系在

     内存中，如果是海量数据，会超过内存上限；②Zookeeper应用场

     景也不是为存储海量数据而设计，因为其是一种分布式协调服务框架

     存储的是管理数据和配置信息。

- Zookeeper的路径是具有唯一性的，我们可以利用此特性实现集群统一命名服务



