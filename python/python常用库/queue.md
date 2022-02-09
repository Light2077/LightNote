队列模块`queue`

https://docs.python.org/3/library/queue.html

该模块主要应用于多线程编程



```python
from queue import Queue
q = Queue(maxsize=4)

# 默认参数
q.put('hello', block=True, timeout=None)
q.put('how')
q.put('are')
q.put('you')

# 查看队列里的所有元素
print(q.queue)
```

此时队列已经满了，如果再往里面put一个元素，你的python就会卡住。

```python
q.put('more')
```



可以设置`block=False`，如果队列满了就报错

```python
q.put('more', block=False)
```

```
# 程序会产生一个Full类型的错误
raise Full
```



也可以设置`timeout=2`，如果等待超过一定时间(2s)就报错，报错的信息和`block=False`时一样

```python
q.put('more', timeout=2)
```



不要同时设置`block=False`和`timeout=2`参数，这样是无意义的。因为`block=False`时，就会立马返回`Full`错误。



可以用`put_nowait()` 和`get_nowait()`代替`put(item, block=False)`和`get(item, block=False)`

```python
# 等价于q.put('more', block=False)
q.put_nowait('more')
```

## 队列与线程

下面的例子展示了如何使用队列给线程分配任务

```python
import threading, queue
import time
q = queue.Queue()  # 创建一个队列

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        time.sleep(1)
        print(f'Finished {item}')
        q.task_done()
        
# 开启一个线程
threading.Thread(target=worker, daemon=True).start()

# 发送3个任务
for item in range(3):
    q.put(item)
print('All task requests sent')

# 阻塞直到所有任务执行完毕
q.join()
print('All work completed')
```

然后如果想继续增加任务，只需

```python
q.put(item)
```

