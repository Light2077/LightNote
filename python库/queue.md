队列模块`queue`



# 先进先出队列`Queue`

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



不需要同时设置`block=False`和`timeout=2`参数，这样是无意义的。因为`block=False`时，就会立马返回`Full`错误。



可以用`put_nowait()` 和`get_nowait()`代替`put(item, block=False)`和`get(item, block=False)`

```python
# 等价于q.put('more', block=False)
q.put_nowait('more')
```

