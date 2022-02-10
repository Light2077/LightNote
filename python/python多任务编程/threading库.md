https://docs.python.org/3/library/threading.html

在CPython中，由于[全局解释器锁](https://docs.python.org/3/glossary.html#term-global-interpreter-lock)的存在，一次只有一个线程执行python代码。如果想要更好利用多核计算资源，可以参考[multiprocessing](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing) or [concurrent.futures.ProcessPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor) 。不过threading库对于那种IO密集型任务还是很好的。

>[什么是CPU密集型、IO密集型？](https://blog.csdn.net/youanyyou/article/details/78990156)
>
>IO密集型任务（I/O bound）
>
>
>
>CPU性能相对硬盘、内存要好很多，在处理某些任务的时候，任务有大量I/O操作，而CPU占用率很低。
>
>涉及到网络、磁盘IO的任务都是IO密集型任务，任务的大部分时间都在等待IO操作完成。
>
>python这类脚本语言很适合写IO密集型任务的代码，因为其代码量少，开发效率高。而C、C++更适合写计算密集型任务，用它们写IO密集型任务也提升不了多少效率。

## Thread类

```python
class threading.Thread(
    group=None,
    target=None,
    name=None,
    args=(),
    kwargs={},
    *,
    daemon=None
)
```



`threading.active_count()`

```python
import threading
import time

def dance(name):
    print(f"{name} is dancing...")
    time.sleep(3)
    print(f"{name} is finish dancing...")
    
def sing(name):
    print(f"{name} is singing...")
    time.sleep(1)
    print(f"{name} is finish singing...")

print('before start active count:', threading.active_count())
    
threading.Thread(target=dance, args=('lily',)).start()
threading.Thread(target=sing, args=('tom',)).start()

print('running active count:', threading.active_count())
time.sleep(4)
print('ending active count:', threading.active_count())
```

### 线程本地对象

每个线程的`local_data.name`结果都不一样

> 暂时还不了解应用场景

```python
import threading

local_data = threading.local()
local_data.name = '主线程'
def dance():
    local_data.name = 'dance线程'
    print(local_data.name)
    
def sing():
    local_data.name = 'sing线程'
    print(local_data.name)

print(local_data.name)
threading.Thread(target=dance).start()
threading.Thread(target=sing).start()
```

### 自定义线程类

个人认为用途是减少代码量

主要重构`__init__()`方法和`run()`方法。

`__init__()`方法保存要执行的target函数，以及该函数所需的参数`args`，`kwargs`

当线程对象调用`start()`方法后，就会执行`run()`方法。

`run()`方法再执行之前传入的`target`函数。



```python
class MyThread(Thread):
    def __init__(self, target=None,
                  args=(), kwargs={}):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.target(*self.args, **self.kwargs)
```

### 如何加锁

```python
import threading

lock = threading.Lock()

def f():
    with lock:
        do_something()
threading.Thread(target=f).start()
```

