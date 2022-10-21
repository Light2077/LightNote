# 【python】爬虫异步网络请求async+request与async+aiohttp

在学习协程的时候，会有一个疑问，使用协程语法进行异步请求时，比如`async + requests`，会有用吗？

其实细想一下就知道，由于requests库是用同步的方式写的，因此`async + requests`是肯定没用的。

但是本着实践出真知的思想，顺便复习巩固一下多线程、async、aiohttp的写法，还是手动来验证一下。

为了规避网络波动等影响，在本地用Flask搭建一个简易的服务器用于测试。

文章结构如下：

[toc]

先放结论：

- `threading + requests` 能够并发请求
- `async + requests` 不能并发请求
- `async + aiohttp` 能并发请求

因此在进行爬虫的时候，要想加快效率，要么使用`threading + requests` ，要么就使用`async + aiohttp` 

## 初始环境准备

安装测试所需要的库

```
pip install flask
pip install requets
pip install aiohttp
```

在任意路径创建一个文件夹（文件夹名随意），例如`./async_test`

在该文件夹下创建一个空的py文件`app.py`用于后续搭建测试用后端。

再创建3个py文件分别对应3个实验，创建完毕后文件目录结构如下（此时的py文件都是空的）

```
|- async_test
  |- app.py
  |- 1_threading_requests.py
  |- 2_async_requests.py
  |- 3_async_aiohttp.py
```

## 搭建测试用的后端

让每次请求的时候先沉睡2秒，再返回结果，以此来模拟网络延迟。

在`app.py`文件中添加如下代码

```python
## app.py ##
from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def index():
    time.sleep(2)
    return "Hello World!"

if __name__ == '__main__':
    app.run()
```

在`./async_test`目录下运行

```
python app.py
```

```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

访问http://127.0.0.1:5000/ 延迟2秒后会看到Hello World!

完成这一步就搭建好了测试用后端

## 1.threading+requests

在`1_threading_requests.py`文件中添加如下代码

```python
## 1_threading_requests.py ##
import time
import threading

import requests

def get(i):
    print(time.strftime('%X'), 'start', i)
    resp = requests.get('http://127.0.0.1:5000/')
    print(time.strftime('%X'), 'end', i)

start = time.perf_counter()
for i in range(4):
    threading.Thread(target=get, args=(i,)).start()
print(f'total {time.perf_counter() - start:.2f}s ')
```



在`./async_test`目录下运行

```
python 1_threading_requests.py
```

```
09:23:19 start 0
09:23:19 start 1
09:23:19 start 2
09:23:19 start 3
09:23:21 end 2
09:23:21 end 0
09:23:21 end 3
09:23:21 end 1
```

发现使用多线程的写法是能够并发请求的。

## 2.async + requests

在`2_async_requests.py`文件中添加如下代码

```python
## 2_async_requests.py ##
import time
import asyncio

import requests

async def get(i):
    print(time.strftime('%X'), 'start', i)
    resp = requests.get('http://127.0.0.1:5000/')
    print(time.strftime('%X'), 'end', i)
    
async def main():
    for i in range(4):
        asyncio.create_task(get(i))
        
asyncio.run(main())
```

在`./async_test`目录下运行

```
python 2_async_requests.py
```

```
09:27:11 start 0
09:27:13 end 0
09:27:13 start 1
09:27:15 end 1
09:27:15 start 2
09:27:17 end 2
09:27:17 start 3
09:27:19 end 3
```

发现`async+requests`的写法，代码是顺序执行的，异步并没有起到效果

于是将`get(i)`函数用aiohttp重写

## 3.async + aiohttp

在`3_async_aiohttp.py`文件中添加如下代码

```python
## 3_async_aiohttp.py ##
import time
import asyncio
import aiohttp
import requests

async def get(i):
    print(time.strftime('%X'), 'start', i)
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:5000/') as response:
            html = await response.text()
    print(time.strftime('%X'), 'end', i)

async def main():
    tasks = [asyncio.create_task(get(i)) for i in range(4)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

在`./async_test`目录下运行

```
python 3_async_aiohttp.py
```

```
09:37:43 start 0
09:37:43 start 1
09:37:43 start 2
09:37:43 start 3
09:37:45 end 0
09:37:45 end 2
09:37:45 end 3
09:37:45 end 1
```

发现代码成功异步执行了，总耗时只有两秒

说明python的协程语法需要配合异步python库才会生效。

