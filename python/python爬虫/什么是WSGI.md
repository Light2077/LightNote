

[WSGI到底是什么？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/95942024)

https://www.liaoxuefeng.com/wiki/1016959663602400/1017805733037760

# 什么是WSGI

全称Python Web Server Gateway Interface

- WSGI是一套接口标准协议/规范
- 是web服务器和python web应用或框架之间的标准接口
- 制定标准，以保证不同Web服务器可以和不同的Python程序之间相互通信，提高web应用在一系列Web服务器之间的移植性。

## web应用处理请求的具体流程

- 用户使用浏览器发送请求
- 请求转发至对应web服务器
- web服务器将请求转交给web应用层序
- web应用程序处理请求
- web应用程序将请求返回给web服务器
- web服务器返回用户响应结果
- 浏览器收到响应，向用户展示



Web服务器（如Apache, Nginx, Caddy等）和Web应用框架（如Django, Flask, Pyramid等）有很多种。每种Web服务器和Web应用框架都有自己的特点和配置方式



你可以把WSGI理解为一种规定，规定了代码要编写什么，web服务器在将请求转交给web应用程序之前，需要先将http报文转换为WSGI规定的格式。

- Web程序必须有一个可调用对象
- 该可调用对象接收两个参数，返回一个可迭代对象

如下

```python
def hello(environ, start_response):
    status = "200 OK"
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    path = environ['PATH_INFO'][1:] or 'hello'
    return [b'<h1> %s </h1>' % path.encode()]
```



# WSGI怎么起作用

web服务器在将请求转交给web应用程序之前，**需要先将http报文转换成WSGI规定的格式**

## WSGI规范

web程序（我暂时将其理解为django、flask这种后端）必须有一个可调用对象，该对象**接收**两个参数。

- `environ`：字典，包含请求的所有信息。
- `start_response`：在可调用对象中调用的函数，用于发起响应，参数包括状态码，header等。

**返回**一个可迭代对象。

# 一个简单的WSGI服务

编写`hello.py`

```python
# hello.py
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']
```

同目录下编写`server.py`

```python
# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from hello import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
```

访问：http://localhost:8000/

即可看到hello, web!

## WSGI

### 在没有WSGI的情况下

1. 用户请求 -> Web服务器（比如Apache或Nginx）
2. Web服务器 -> 特定于服务器的代码（用于处理请求）
3. 特定于服务器的代码 -> Web应用（比如Django或Flask）

例如，用户请求以后，会发送一些信息给Web服务器。比如类似于下面这样的格式

```python
user_request = {
    'method': 'GET',
    'url': '/hello',
    'headers': {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US'
    }
}

```

然后web服务器接收到这个信息后进行处理

```python
def web_server(request):
    print("Web Server received request:", request)
    return server_specific_code(request)

def server_specific_code(request):
    print("Server-specific code is processing the request...")
    # 在这里，你可以添加路由逻辑、安全检查等
    return web_application(request)

```

最终：特定于服务器的代码 -> Web应用

模拟一个Web应用。这个应用接收处理过的请求，并返回一个响应

```python
def web_application(request):
    print("Web Application is generating a response...")
    if request['url'] == '/hello':
        return {
            'status': 200,
            'content': 'Hello, World!'
        }
    else:
        return {
            'status': 404,
            'content': 'Not Found'
        }

```



### 使用WSGI后

1. 用户请求 -> Web服务器（比如Apache或Nginx）
2. Web服务器 -> WSGI中间层
3. WSGI中间层 -> Web应用（比如Django或Flask）

```python
from wsgiref.simple_server import make_server

# 模拟Web应用
def web_application(environ, start_response):
    print("Web Application is generating a response...")
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    
    path = environ['PATH_INFO']
    if path == '/hello':
        return [b'Hello, World!']
    else:
        return [b'Not Found']

# 主程序
if __name__ == '__main__':
    # 创建一个WSGI服务器并运行
    with make_server('', 8000, web_application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

```

在这个示例中，`web_application`函数是一个符合WSGI标准的Web应用。它接受两个参数：`environ`（一个包含所有环境变量的字典）和`start_response`（一个用于发送HTTP状态和HTTP头的可调用对象）。

在WSGI标准中，`start_response`是一个由WSGI服务器（在这个例子中是`wsgiref.simple_server.make_server`）提供的可调用对象（通常是一个函数）。这个`start_response`函数用于设置HTTP响应的状态码和头信息。

当你的Web应用准备好生成一个HTTP响应时，它会调用`start_response`来设置响应的状态（比如`'200 OK'`）和HTTP头（比如`'Content-type': 'text/plain'`）。这样，WSGI服务器就知道如何构建HTTP响应并发送给客户端。

在上面的代码示例中，`start_response`被调用如下：

```python
status = '200 OK'
headers = [('Content-type', 'text/plain; charset=utf-8')]
start_response(status, headers)
```

这里，`status`是HTTP状态码和描述，`headers`是一个包含HTTP头信息的元组列表。

总体来说，`start_response`的实现是WSGI服务器的责任，而调用`start_response`来设置响应状态和头信息则是Web应用的责任。

```python
# 全局变量用于存储HTTP状态和头信息
http_status = None
http_headers = None

# 模拟 start_response 函数
def start_response(status, headers):
    global http_status, http_headers
    http_status = status
    http_headers = headers
```

