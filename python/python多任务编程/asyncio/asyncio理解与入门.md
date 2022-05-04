# asyncio

https://www.bilibili.com/video/BV1oa411b7c9

```python
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')
    
asyncio.run(main())
```

asyncio的核心就是事件循环（event loop）

asyncio不能提升运算速度，它适合的场景是需要进行IO等待的场景，最常见的场景就是爬虫了。

事件循环里包含很多任务，每个任务要**主动**告诉循环，我的任务完成了，可以让别的任务开始了。

优点在于任务是什么时候停止是你自己可以决定的。

## coroutine

coroutine一般指：

- coroutine function：比如上面示例的main函数
- coroutine object：coroutine函数调用的返回值`main()`就是coroutine 对象。一般都是指coroutine对象。

如何运行coroutine函数：

- 启动事件循环：`asyncio.run()`
- 将coroutine 对象变成task

## await

```python
import asyncio
import time

async def say_after(wait, text):
    await asyncio.sleep(wait)
    print(text)
    
async def main():
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")
    
asyncio.run(main())
```

```
started at 18:27:39
hello
world
finished at 18:27:42
```

下面通过事件循环内包含的任务的情况来说明流程。

```python
asyncio.run(main())
```

事件循环：只有一个task main

```python
await say_after()
```

执行了say_after后，事件循环多了一个task，同时事件循环开始执行这个task，但是立刻遇到了

```python
await asyncio.sleep(1)
```

事件循环发现`asyncio.sleep(1)`要等待，于是看看有没有其他任务要执行，发现没有，回来继续执行这个函数。

运行完毕后，事件循环只剩两个task：`main`、`say_after`

事件循环继续运行`say_after`，运行完毕后继续运行`main`



总结，控制权交还给事件循环的时机有两个：

- await发生时
- await的函数(task)运行完毕时

## creat_task()

问题：上面有两个`say_after`但是一次只等一个函数，没有做到同时等待

原因：await做的事情太多了：

- 首先它将一个函数包装成task。
- 然后把这个task加入事件循环。
- 最后等待这个task运行完毕。

实际上，我们只想做前两步。这里就引入了`creat_task`函数。

```python
import asyncio
import time

async def say_after(wait, text):
    await asyncio.sleep(wait)
    print(text)
    
async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))
    
    task2 = asyncio.create_task(
        say_after(2, 'world'))
    
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")
    
asyncio.run(main())
```

```
started at 18:27:03
hello
world
finished at 18:27:05
```



`create_task`只做了两件事

- 将函数包装成task。
- 把这个task加入事件循环。

这时事件循环就已经包含了总共3个task了，但是现在事件循环也不会执行这两个新加入的task，因为控制权还没交还给事件循环。

因此仍需要`await`切换控制权

```python
await task1
await task2
```

当事件循环执行task1时，task1执行到`await asyncio.sleep(1)`时，控制权交还给事件循环，此时事件循环就又可以执行`task2`了。

## asyncio.gather()

如果task很多的话，可以用`asyncio.gather()`函数批量加入事件循环。

```python
ret = await asyncio.gather(task1, task2)
```

返回值被存储在ret里，结果是一个list，与task的顺序一一对应。

上面这条语句相当于告诉事件循环，我要等待所有的task执行完毕。

直接给coroutine对象也是可以的

```python
ret = await asyncio.gather(
    say_after('hello'),
    say_after('world')
)
```

如果事先保存了一个列表，就需要使用`*`解包

```python
tasks = [task1, task2]
ret = await asyncio.gather(*tasks)
```

## await机制详解

https://www.bilibili.com/video/BV1ST4y1m7No