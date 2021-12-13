https://www.liaoxuefeng.com/wiki/1016959663602400/1019223241745024

# [`urllib`](https://docs.python.org/zh-cn/3/library/urllib.html?highlight=urllib#module-urllib) --- URL 处理模块

**源代码:** [Lib/urllib/](https://github.com/python/cpython/tree/3.9/Lib/urllib/)

------

`urllib` 是一个收集了多个涉及 URL 的模块的包：

- [`urllib.request`](https://docs.python.org/zh-cn/3/library/urllib.request.html#module-urllib.request) 打开和读取 URL
- [`urllib.error`](https://docs.python.org/zh-cn/3/library/urllib.error.html#module-urllib.error) 包含 [`urllib.request`](https://docs.python.org/zh-cn/3/library/urllib.request.html#module-urllib.request) 抛出的异常
- [`urllib.parse`](https://docs.python.org/zh-cn/3/library/urllib.parse.html#module-urllib.parse) 用于解析 URL
- [`urllib.robotparser`](https://docs.python.org/zh-cn/3/library/urllib.robotparser.html#module-urllib.robotparser) 用于解析 `robots.txt` 文件

# [`urllib.request`](https://docs.python.org/zh-cn/3/library/urllib.request.html#module-urllib.request)

```python
urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
```

## 读取网页信息

```python
from urllib import request
url = 'https://www.baidu.com'
with request.urlopen(url) as f:
    data = f.read()
    print('Data:', data.decode('utf-8'))
```

## 添加头信息

```python
from urllib import request
url = 'https://www.baidu.com'

req = request.Request(url)
req.add_header('User-Agent', 
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
               'AppleWebKit/537.36 (KHTML, like Gecko)'
               'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134')

with request.urlopen(req) as f:
    data = f.read()
    print('Data:', data.decode('utf-8'))
```

添加了头信息之后，得到的数据就变多了。

## 使用代理服务器

```python
from urllib import request
url = 'https://www.baidu.com'

req = request.Request(url)
req.add_header('User-Agent', 
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
               'AppleWebKit/537.36 (KHTML, like Gecko)'
               'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134')
# 设置代理服务器信息
ip=request.ProxyHandler({'http':'116.214.32.51:8080'})
opener=request.build_opener(ip,request.HTTPHandler)
with opener.open(req) as f:
    data = f.read()
    print('Data:', data.decode('utf-8'))

```

