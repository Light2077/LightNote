https://www.runoob.com/w3cnote/python-redis-intro.html

## 安装

```
pip install redis
```

测试是否安装成功

```python
import redis
r = redis.Redis(host='localhost', port=6379, password='123456')
r.set('foo', 'bar')
```

redis每次get到的都是二进制字节。可以通过设置`decode_responses=True`来自动decode

## 巧用pickel

[Django-redis如何支持存取整型和布尔值](https://michaelyou.github.io/2016/11/03/Django-redis%E5%A6%82%E4%BD%95%E6%94%AF%E6%8C%81%E5%AD%98%E5%8F%96%E6%95%B4%E5%9E%8B%E5%92%8C%E5%B8%83%E5%B0%94%E5%80%BC/)

使用pickel来让redis可以存取任何类型的python对象。

```python
import pickle
import redis

student = {'name': 'lily', 'age': 20}
data = pickle.dumps(student)

r.set('data', data)

student = pickle.loads(r.get('data'))
```

## redis连接池

connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。

默认，每个Redis实例都会维护一个自己的连接池。可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。

```python
import redis    # 导入redis 模块

pool = redis.ConnectionPool(host='localhost', port=6379, password=123456)
r = redis.Redis(connection_pool=pool)
```

## redis基本命令



### 删除

```python
r.delete('name')
```

### 查看是否存在

```python
r.exists('name')
```

### 模糊匹配key

```python
r.keys("foo*")
```

### 设置超时时间

```python
# 多少秒后超时
r.expire('name', 5)

# 在某个时间点超时
r.expireat('name', datetime.datetime.now() + datetime.timedelta(seconds=10))
```

### 取消超时时间

```python
r.persist('name')
```



### 重命名

对某个key重命名

```python
r.rename('name', 'xingming')
```

### 随机获取一个key

```python
r.randomkey()
```

## 管道

redis默认在执行每次请求都会创建（连接池申请连接）和断开（归还连接池）一次连接操作，如果想要在一次请求中指定多个命令，则可以使用pipline实现一次请求指定多个命令，并且默认情况下一次pipline 是原子性操作。

管道（pipeline）是redis在提供单个请求中缓冲多条服务器命令的基类的子类。它通过减少服务器-客户端之间反复的TCP数据库包，从而大大提高了执行批量命令的功能。

```python
import redis
import time

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
# 默认的情况下，管道里执行的命令可以保证执行的原子性
# 如果设定transaction=False，就取消了这一特性

# pipe = r.pipeline(transaction=False)
# pipe = r.pipeline(transaction=True)
pipe = r.pipeline() # 创建一个管道

pipe.set('name', 'jack')
pipe.set('role', 'sb')
pipe.sadd('faz', 'baz')
pipe.incr('num')    # 如果num不存在则vaule为1，如果存在，则value自增1
pipe.execute()

print(r.get("name"))
print(r.get("role"))
print(r.get("num"))
```



## 常用操作

### set

```python
r.set(name, value, ex = None, px = None, nx = False, xx = False, exat = None)
```

常用参数解释

- name：可以传入二进制或字符串
- value：可以传入二进制、str、int、float
- ex：过期时间（秒），可以传入float、`datetime.timedelta`。
- px：过期时间（毫秒），可以传入float、`datetime.timedelta`。
- nx：如果设置为True，则只有name**不存在**时，当前set操作才执行。
- xx：如果设置为True，则只有name**存在**时，当前set操作才执行
- exat：过期时刻，可以传入int的时间戳或者`datetime.datetime`

set成功返回True，失败返回False

### setnx

不存在才添加

```python
r.setnx('name', 'lily')
# 等价于
r.set('name', 'lily', nx=True)
```

### setex

设置过期时间

```python
r.setex('name', 5, 'lily')
# 等价于
r.set('name', 'lily', ex=5)
```

### mset与mget

批量设置获取值

```python
mset(*args, **kwargs)
mget(keys, *args)
```

示例

```python
r.mget({'k1': 'v1', 'k2': 'v2'})
r.mset(k1="v1", k2="v2") # 这里k1 和k2 不能带引号，一次设置多个键值对
print(r.mget("k1", "k2"))   # 一次取出多个键对应的值
print(r.mget("k1"))
```

### 获取原来的值并设置新的值

```python
print(r.getset("food", "barbecue"))
```

### incr

```python
incr(name, amount=1)
```

自增 name 对应的值，当 name 不存在时，则创建 name＝amount，否则，则自增。

```python
r.set('foo', 123)
a = r.incr('foo')
print(a)
```

```
124
```

> incr 不影响过期时间，当某个key设定了过期时间以后，在对其进行incr操作，到期后仍然会删除该键值对。

### decr

自减，和incr操作相反

## redis实战中使用

https://blog.csdn.net/weixin_45599402/article/details/116615735

```python
class Redis:
    """
    redis数据库操作
    """
    @staticmethod
    def _get_r():
        host = app.config['REDIS_HOST']
        port = app.config['REDIS_PORT']
        db = app.config['REDIS_DB']
        passwd = app.config['REDIS_PWD']
        r = redis.StrictRedis(
            host=host, 
            port=port, 
            db=db, 
            password=passwd
        )
        return r

```

实际上在每次使用前都重新创建了一个redis.StrictRedis()

还有另一个

https://cloud.tencent.com/developer/article/1801254

```python
from redis import ConnectionPool, Redis
#获取redis服务器连接
def getRedis():
    while True:
        try:
            pool = ConnectionPool(host='192.168.8.211', port=6379, db=0, password=None, 
            decode_responses=True, health_check_interval=30)
            redis = Redis(connection_pool=pool)
            redis.ping()
        except Exception as e:
            print('redis连接失败,正在尝试重连')
            continue
        else:
            return redis
```

然后我又找到了这个:https://stackoverflow.com/questions/12967107/managing-connection-to-redis-from-python

它告诉我只需要声明一个pool，然后每次用之前创建一个新的链接就行了。

```python
import redis    # 导入redis 模块

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0, password=123456)

def myget():
    r = redis.Redis(connection_pool=POOL)
    print(r.get('name'))

def myset():
    r = redis.Redis(connection_pool=POOL)
    print(r.set('name', 3))
```

## 连接老是超时

https://github.com/redis/redis-py/issues/1232

这个应该是最合理的解决方案了？

https://blog.csdn.net/dslkfajoaijfdoj/article/details/83692668



经过我的操作，似乎只要降低timeout时间就行了

```
CONFIG SET timeout 5
```

我把这个时间从原来的300秒改成了5秒，发现问题就解决了。

但是5秒显然不科学，于是我最终改成了60秒。依然能够正常运行！
