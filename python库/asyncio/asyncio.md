https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutines

# 协程的最简单应用

下面这个代码就是最简单的协程应用，先打印`hello`，等待1秒后打印`world`

```python
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')

asyncio.run(main())
```

```
hello
world
```

注：使用Jupyter Notebook时会报错，建议使用命令行来运行python脚本。



直接调用`main()`不会执行

```
>>> main()
<coroutine object main at 0x00000199748C5540>
```

# 运行协程的三种方式

- 方式一：`asyncio.run(<func>)`就是第一个例子的方式
- 方式二：`await <func>`等待一个协程运行完后，运行下一个协程
- 方式三：使用`asyncil.create_task()`来并发运行asyncio任务。

## 方式二：等待一个协程

下面的例子会在1秒后打印`hello`，**再**等2秒后打印`world`。一共执行了3秒。

![](img/运行方式2.png)

```python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```

预期输出

```
started at 17:52:20
hello
world
finished at 17:52:23
```

## 方式三 并发运行多个协程

下面的例子会先打印`hello`，过1秒后打印`world`。总共执行2秒。

![](img/运行方式3.png)

```python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    
async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")
    
asyncio.run(main())
```

结果会比方式二快1秒。

```
started at 17:57:34
hello
world
finished at 17:57:36
```

# 可等待对象

如果一个对象`<obj>`可以用`await <obj>`，那这个对象就是**可等待对象(awaitable)**。主要有三种可等待对象：协程、任务、和Future

## 协程

- 协程函数：以`async def`定义的函数
- 协程对象：协程函数返回的对象

像之前的代码，等待的就是**协程**，会等上面执行完了才执行下面的：

```python
await say_after(1, 'hello')
await say_after(2, 'world')
```

## 任务

使用`asyncio.create_task()`可以把一个协程函数打包成一个任务。

使用`await task`时，会立即运行该任务。

比如方式三的这段代码，等待的就是**任务**，会一起执行这两个函数。

```python
task1 = asyncio.create_task(
        say_after(1, 'hello'))

task2 = asyncio.create_task(
        say_after(2, 'world'))

await task1
await task2
```

## future对象

这个东西，一般不会用到。略

# asyncio.run

这个东西一般只调用一次

```python
asyncio.run(main())
```

负责管理asyncio事件循环、终结异步生成器、关闭线程池。:question:

# 并发运行任务

```python
asyncio.gather(*aws, loop=None, return_exceptions=False)
```

并发运行`aws`序列中的可等待对象

如果`aws`中有协程，会自动把这个协程打包成任务加入日程

如果所有可等待对象都成功完成，结果将是一个由所有返回值聚合而成的列表。结果值的顺序与 *aws* 中可等待对象的顺序一致。

# 屏蔽取消

保护一个可等待对象，防止其被取消

```python
# awaitable
asyncio.shield(aw, *, loop=None)
```

如果 *aw* 是一个协程，它将自动作为任务加入日程。

```python
res = await asyncio.shield(something())
# 相当于
res = await something()
```

前者如果包含它的协程被取消，`something()`中的任务会继续运行。

# 超时

```python
# coroutine
asyncio.wait_for(aw, timeout, *, loop=None)
```



如果发生超时，任务将取消并引发 [`asyncio.TimeoutError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.TimeoutError).

要避免任务 [`取消`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.cancel)，可以加上 [`shield()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.shield)。

如果 *aw* 是一个协程，它将自动作为任务加入日程。