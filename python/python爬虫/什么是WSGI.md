https://zhuanlan.zhihu.com/p/95942024



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