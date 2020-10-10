# 学习目标

- 能说出什么是HTTP协议
- 能够手写代码搭建一个HTTP服务器
- 了解WSGI接口
- 能够看懂自定义WSGI服务器
- 能够使用requests插件发送请求

# 1. HTTP协议

hypertext transfer protocol 超文本传输协议，用于传输超文本 HTML(HyperText Markup Language)

C/S架构 client-server
B/S架构 browser-server



```python
import socket
# http 服务器都是基于 TCP 的 socket 连接
sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('192.168.31.211', 9090))
server_socket.listen(128)

client_socket, client_addr = server_socket.accept()

data = client_socket.recv(1024).decode('utf8')
print(data)
```

然后在浏览器输入`192.168.31.211:9090`，会打印出以下信息。这就是http的请求头。

```
GET / HTTP/1.1
Host: 192.168.31.211:9090
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
```



```
|----------|       request headers        |----------|  
|          | ---------------------------> |          |
| browser  |                              |  server  |
|          | <--------------------------- |          |
|----------|       response headers       |----------|
```



返回内容之前需要设置HTTP相应头

```python
import socket
# http 服务器都是基于 TCP 的 socket 连接
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('0.0.0.0', 9090))
server_socket.listen(128)

# 可以在这里加死循环
client_socket, client_addr = server_socket.accept()
data = client_socket.recv(1024).decode('utf8')

# 发送一个相应头就换一次行
# client_socket.send('HTTP/1.1 200 OK\n'.encode('utf8'))
client_socket.send('HTTP/1.1 200 OK\n'.encode('utf8'))
client_socket.send('Content-Type: text/html;charset=utf-8\n'.encode('utf8'))

# 所有的响应头设置完成以后，再换行
client_socket.send('\n'.encode('utf8'))

msg = 'hello {}'.format(client_addr[0])
client_socket.send(msg.encode('utf8'))

print(msg)

```

把这个文件上传到云服务器

然后`python3 xx.py`就能通过访问服务器的地址来查看网页http://119.45.58.134:9090/

## http请求头

- GET表示请求方式
- `/`表示请求的路径以及请求的参数，比如可能是`/index.html`或`/index.html?name=jack&age=18`
- HTTP/1.1 ：http版本号
- Host: 192.168.31.211:9090 请求的服务器地址
- UserAgent：用户代理，最开始设计的目的是为了能从请求头里辨识浏览器的类型。

```
GET / HTTP/1.1
Host: 192.168.31.211:9090
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
```

## IP地址的绑定

绑定方式：

- `server_socket.bind(('0.0.0.0', 9090))`表示所有可用的地址
- `server_socket.bind(('127.0.0.1', 9090))`只有本机能访问，别人都访问不了
- `server_socket.bind(('192.168.31.211', 9090))`局域网内可以访问

访问方式

- `localhost:9090`
- `127.0.0.1:9090`
- `192.168.31.211:9090`

## 根据不同的请求返回不同的内容

`192.168.31.211:9090/login`

```python
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9090))
server_socket.listen(128)

client_socket, client_addr = server_socket.accept()
data = client_socket.recv(1024).decode('utf8')

# 获取请求头中的 GET /path HTTP/1.1 第二项
path = data.splitlines()[0].split()[1]

# 相应头
response_header = 'HTTP/1.1 200 OK\n' + 'Content-Type: text/html;charset=utf-8\n'
response_header += '\n'


if path == '/login':
    response_body = '欢迎来到登陆页面'
elif path == '/register':
    response_body = '欢迎来到注册页面'
elif path == '/':
    response_body = '欢迎来到首页'
else:
    # 显示页面未找到
    response_header = 'HTTP/1.1 404 Page Not Found\n'
    response_body = '页面不存在'
response = response_header + response_body
client_socket.send(response.encode('utf8'))

print(response_body)

```

## 面向对象的服务器封装

```python
import socket

class MyServer:
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(128)
    def run_forever(self):
        while True:
            client_socket, client_addr = self.socket.accept()
            data = client_socket.recv(1024).decode('utf8')

            # 获取请求头中的 GET /path HTTP/1.1 第二项
            path = data.splitlines()[0].split()[1]

            # 相应头
            response_header = 'HTTP/1.1 200 OK\n' + 'Content-Type: text/html;charset=utf-8\n'
            response_header += '\n'


            if path == '/login':
                response_body = '欢迎来到登陆页面'
            elif path == '/register':
                response_body = '欢迎来到注册页面'
            elif path == '/':
                response_body = '欢迎来到首页'
            else:
                # 显示页面未找到
                response_header = 'HTTP/1.1 404 Page Not Found\n\n'
                response_body = '页面不存在'
            response = response_header + response_body
            client_socket.send(response.encode('utf8'))
        
server = MyServer('0.0.0.0', 9090)
server.run_forever()

```

# 2. WSGI服务器

https://www.liaoxuefeng.com/wiki/1016959663602400/1017805733037760

Python Web Server Gateway Interface，WSGI接口定义非常简单，它只要求web开发者实现一个函数，就可以响应HTTP请求

```python
def demo_app(environ, start_response):
    # 发送HTTP响应
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8')])
    return ['<h1>Hello</h1>'.encode('utf8')]  # 浏览器显示的内容
```

`demo_app()`函数就是符合WSGI标准的一个HTTP处理函数，接收两个参数

- envion：一个包含所有HTTP请求信息的dict对象
- start_response：一个发送HTTP响应的函数

使用`environ['PATH_INFO']`就能拿到用户请求路径

`environ['QUERY_STRING']`可以拿到GET请求字符串

POST 请求数据的方式后面再说。

```python
from wsgiref.simple_server import make_server

def demo_app(environ, start_response):
    # 发送HTTP响应
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ('xxx', 'sss')])
    return ['<h1>Hello</h1>'.encode('utf8')]  # 浏览器显示的内容

# make_server 相当于之前的服务器创建的一堆代码
if __name__ == '__main__':
    # demo_app用于处理用户的请求
    with make_server('', 8000, demo_app) as httpd:
        sa = httpd.socket.getsockname()
        print('Serving HTTP on', sa[0], 'port', sa[1], '...')
        # 作用是打开电脑的浏览器，并在浏览器输入地址
        import webbrowser
        webbrowser.open('http://localhost:8000/xyz?abc')
        httpd.handle_request() # serve one request then exit
        # httpd.serve_forever()  # 永久运行
```



## 根据不同路径返回不同内容

```python
from wsgiref.simple_server import make_server

def demo_app(environ, start_response):
    path = environ['PATH_INFO']
    res_dict = {
        '/': '欢迎来到首页',
        '/test': '欢迎来到test',
        '/demo': '欢迎来到demo',
    }
    if path in res_dict:
        status_code = '200 OK'
        response = res_dict[path]
    else:
        status_code = '404 Not Found'
        response = 'Not Found hhhh!'
        
    # 发送HTTP响应
    start_response(status_code, [('Content-Type', 'text/html;charset=utf8'), ('xxx', 'sss')])
    response = '<h1>%s</h1>' % response
    return [response.encode('utf8')]  # 浏览器显示的内容

# make_server 相当于之前的服务器创建的一堆代码
if __name__ == '__main__':
    # demo_app用于处理用户的请求
    # 第一个参数空表示0.0.0.0
    with make_server('', 8000, demo_app) as httpd:
        sa = httpd.socket.getsockname()
        print('Serving HTTP on', sa[0], 'port', sa[1], '...')
        # 作用是打开电脑的浏览器，并在浏览器输入地址
        import webbrowser
        webbrowser.open('http://localhost:8000/test')
        # httpd.handle_request() # serve one request then exit
        httpd.serve_forever()  # 永久运行

```

状态码

2XX：请求响应成功
3XX：重定向到某个界面
4XX：客户端的错误
5XX：服务器的错误

## 返回不同的类型

还可以打开一个文件，然后读取内容，传输过去。

```python
from wsgiref.simple_server import make_server
import json
def demo_app(environ, start_response):
    path = environ['PATH_INFO']
    query = environ['QUERY_STRING'].split('&')
    res_dict = {
        '/': '欢迎来到首页',
        '/test': json.dumps({'name':query[0], 'age':query[1]}),
        '/demo': '欢迎来到demo',
    }
    if path in res_dict:
        status_code = '200 OK'
        response = res_dict[path]
    else:
        status_code = '404 Not Found'
        response = 'Not Found hhhh!'
        
    # 发送HTTP响应
    start_response(status_code, [('Content-Type', 'text/html;charset=utf8'), ('xxx', 'sss')])
    response = '<h1>%s</h1>' % response
    return [response.encode('utf8')]  # 浏览器显示的内容

# make_server 相当于之前的服务器创建的一堆代码
if __name__ == '__main__':
    # demo_app用于处理用户的请求
    # 第一个参数空表示0.0.0.0
    with make_server('', 8000, demo_app) as httpd:
        sa = httpd.socket.getsockname()
        print('Serving HTTP on', sa[0], 'port', sa[1], '...')
        # 作用是打开电脑的浏览器，并在浏览器输入地址
        import webbrowser
        webbrowser.open('http://localhost:8000/test?lily&18')
        # httpd.handle_request() # serve one request then exit
        httpd.serve_forever()  # 永久运行

```

## 方法的封装

可以使用字典来管理返回的页面，我之前就察觉到了。字典的值可以用一个**函数名**表示。这样只需要维护里边函数的逻辑即可。

调用时`res_dict[path]()`

```python
from wsgiref.simple_server import make_server
import json
def show_index():
    return '欢迎来到首页'

def show_test():
    return json.dumps({'name':'lily', 'age':18})

def show_demo():
    return '欢迎来到demo'

res_dict = {
        '/': show_index,
        '/test': show_test,
        '/demo': show_demo,
    }

def demo_app(environ, start_response):
    path = environ['PATH_INFO']
    
    if path in res_dict:
        status_code = '200 OK'
        response = res_dict[path]()
    else:
        status_code = '404 Not Found'
        response = 'Not Found hhhh!'
        
    # 发送HTTP响应
    start_response(status_code, [('Content-Type', 'text/html;charset=utf8'), ('xxx', 'sss')])
    # response = '<h1>%s</h1>' % response
    return [response.encode('utf8')]  # 浏览器显示的内容

# 新增
def load_html(file_name, **kwargs):
    try:
        with open('pages/' + file_name, 'r', encoding='utf8') as f:
            content = f.read()
            if kwargs:
                content.format(**kwargs)
            return content
    except FileNotFoundError:
        print('文件未找到')
# make_server 相当于之前的服务器创建的一堆代码
if __name__ == '__main__':
    # demo_app用于处理用户的请求
    # 第一个参数空表示0.0.0.0
    with make_server('', 8000, demo_app) as httpd:
        sa = httpd.socket.getsockname()
        print('Serving HTTP on', sa[0], 'port', sa[1], '...')
        # 作用是打开电脑的浏览器，并在浏览器输入地址
        import webbrowser
        webbrowser.open('http://localhost:8000/test')
        # httpd.handle_request() # serve one request then exit
        httpd.serve_forever()  # 永久运行

```

## request模块的介绍

```python
import requests

response = requests.get('http://127.0.0.1:8000/test?alex&22')
print(response)

print(type(response.content), response.content)  # 可以传图片信息

print(type(response.text), response.text)

print(type(response.json()), response.json())  # 如果返回的结果是一个json字符串，可以解析。

```

