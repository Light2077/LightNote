真的反反复复学习了好多次了。

本来想等《Flask Web 开发实战》第二版，但是这会包含很多不确定性，还是算了。

第一版下载：[【百度云】](https://pan.baidu.com/s/1PkV54TnQmhaTlOTA5QpjTA?pwd=aj5u) [【勘误表】](https://docs.helloflask.com/book/1/errata/1-1/)




感觉学习需要一个框架，不然每次过了很久再回来重新学，都要重新看教材，太麻烦了啊。关键这个我自己也总结不好，挺头疼的。

总之，这个文档的内容重在使用，类似于工具文档，是上面这本书知识点的精简版。

该解释的解释一下下就好。

# 初识Flask

### 环境准备

在任意路径创建一个名为`flask_study`的文件夹。

在该目录下运行以下命令

创建虚拟环境

```
python -m venv venv
```

linux激活虚拟环境

```
source ./venv/bin/activate	
```

windows激活虚拟环境

```
.\venv\Scripts\activate
```

安装包管理工具`pip-tools`

```
pip install pip-tools
```

在`flask_study`目录下创建`requirements.in`文件并填入以下内容

```
flask==2.0.2
```

> 也可以不指定flask版本

编译依赖包

```
pip-compile ./requirements.in
```

安装依赖包

```
pip-sync
```



至此就完成了flask的基础环境配置，当前目录文件如下

```
  |- flask_study
    |- venv
    |- requirements.in
    |- requirements.txt
```

> 如果环境中安装了Flask，只想快速测试Flask的功能，也可以不进行上述步骤

### 第一个Flask程序

创建`app.py`文件，内容：

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>hello world!</h1>"
```

运行该服务器

```
flask run
```

```
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

访问：http://127.0.0.1:5000/ 即可看到hello world!



其中`index()`函数被称为视图函数view。

这个名词来源于 MVC架构 (Model-View-Controller，模型－视图－控制器）



### 路由基本使用

每个函数的路由用`@app.route('/xxx')`装饰器来定义。

被定义的函数叫**视图**，比如`index()`函数就是一个视图

路由的常见用法如下：

- 一个视图可以绑定多个URL
- 动态URL：URL可以传参数

代码案例

```python
from flask import Flask

app = Flask(__name__)

# 一个视图绑定多个URL
@app.route("/buy", defaults={"goods": "coffee"})
@app.route("/buy/<goods>")
def buy(goods):
    return "you bought %s" % goods

# 动态URL
@app.route("/hello/<name>")
def hello(name):
    return "hello %s!" % name

if __name__ == '__main__':
    app.run()
```

测试

- http://127.0.0.1:5000/hello: 404
- http://127.0.0.1:5000/hello/lily: 显示hello lily
- http://127.0.0.1:5000/buy：显示you bought coffee
- http://127.0.0.1:5000/buy/flower: 显示you bought flower

### 获取query字符串

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name', '...')
    return "hello, %s!" % name
```

测试

- http://127.0.0.1:5000/hello
- http://127.0.0.1:5000/hello?name=world

模拟发送请求

```python
import requests
url = 'http://127.0.0.1:5000/hello'
# 不传参数
resp = requests.get(url)
print(resp.text)
# 传入参数
# 同 http://127.0.0.1:5000/hello?name=world
resp = requests.get(url, params={'name': 'world'})
print(resp.text)
```

```
hello, ...!
hello, world!
```



### flask run

`flask run`默认监听http://127.0.0.1:5000/，并开启**多线程支持**，会自动寻找`app.py`文件来运行。

可以通过修改环境变量来修改程序主模块，比如想运行`hello.py`，就可以修改环境变量`FLASK_APP`

linux

```
export FLASK_APP=hello
```

windows

```
set FLASK_APP=hello
```

**使服务器外部可见**

```
flask run --host=0.0.0.0
```

**改变端口**

```
flask run --port=8000
```

**查看其他命令**

```
flask --help
```

> 以前是通过`app.run()`来启动服务器，现在不推荐了。
>
> 建议统一使用`flask run`+环境变量配置的方式来启动服务器。

### 环境变量管理

默认情况下flask会加载系统的环境变量，可以安装`python-dotenv`来管理Flask的环境变量。

```
pip install python-dotenv
```



创建`.env`，`.flaskenv`两个文件来配置环境变量。



优先级为：

- 手动设置
- `.env`：存储密码等敏感设置环境变量
- `.flaskenv`：存储公开环境变量

通用格式

```
FLASK_<命令>_<选项>
```

可以用`flask --help`来查看所有可用命令



常用环境变量

```
FLASK_APP=app
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
FLASK_ENV=development
```

解释：

- `FLASK_ENV`，默认为生产环境（production），开发过程中可以设置为development。

### 调试和重载

**调试**

在开发环境下会自动开启调试模式（Debug Mode）

```
flask run
```

```
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 636-634-369
```

点击错误信息右侧的命令行图标， 会弹出窗口要求输入PIN 码。

也就是在启动服务器时命令行窗口打印出`Debugger PIN` 。

输入PIN 码后，我们可以点击错误堆栈的某个节点右侧的命令行界面图标，这会打开一
个包含代码执行上下文信息的Python Shell ，我们可以利用它来进行调试。

**重载**

重载的作用是当修改代码保存后，服务器会自动重启。

比如随意修改`app.py`并`ctrl+s`保存后终端会显示

```
 * Detected change in 'E:\flask_study\app.py', reloading
 * Restarting with stat
```

默认会使用Werkzeug 内置的stat 重载器，推荐使用`watchdog`库，据说效果更好

```
pip install watchdog
```

### flask shell

主要是为了调试，用flask shell会获得跟app一样的环境。

```
flask shell
```

```
Python 3.9.7 (default, Sep 16 2021, 16:59:28) [MSC v.1916 64 bit (AMD64)] on win32
App: app [development]
Instance: E:\flask_study\instance
```

后面的带有`>>>`的代码片段就表示是在shell中的输入，在这个终端中输入

```
>>> app
<Flask 'app'>
>>> app.name
'app'
```

> 后续会有更详细的介绍

### Flask扩展

通用的flask扩展加载方式如下

```python
from flask import Flask
from flask_foo import Foo

app = Flask(__name__)
foo = Foo(app)
```

通常扩展是作为Flask和其他库之间的一层胶水。

### 项目配置

设置配置

键值对配置

```python
app.config['ADMIN_NAME'] = 'Lily'
```

update方法

```python
app.config.update(
    TESTING=True,
    SECRET_KEY='xxxxx'
)
```

还可以将配置变量存储在单独python脚本、JSON文件、python类等



读取配置

```python
admin_name = app.config('ADMIN_NAME')
```

### URL与端点

推荐使用`url_for()`函数来获取URL，该函数的第一个参数就是**端点值(endpoint)**

比如下面这个例子中：

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/hello/<name>')
def hello(name):
    return "hello, %s!" % name
```

调用`url_for('index')`就可以得到`/`

而调用`url_for('hello', name='jack')`就会得到`/hello/jack`

`url_for('hello', _external=True, name='jack')`

得到`http://localhost:5000/hello/jack`





### Flask命令

可以自定义Flask命令

```python
# app.py
from flask import Flask
import click
app = Flask(__name__)

@app.cli.command()
def greeting():
    click.echo('hello!')
```

在命令行

```
flask greeting
```

```
hello
```

> 更多自定义命令可以参考http://click.pocoo.org/6/

常用命令介绍

**查看程序中定义的所有路由**

```
flask routes
```





### 模板与静态文件

通常模板文件放在`templates`文件夹

静态文件放在`static`文件夹

```
|- flask_study
  |- templates/
  |- static/
  |- app.py
```

开发环境下建议用本地资源

# Flask与HTTP

## HTTP请求

### Request对象

假设请求URL为：http://localhost:5000/hello?name=Light

获取到的request属性为

```python
request.path  # u'/hello'
request.full_path
request.host
request.host_url
request.base_url
request.url
request.url_root
```

例如：获取查询字符串

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')
    return f'hello {name}'
```

其他常用属性和方法

```python
request.args
request.blueprint  # 当前蓝图名称
request.cookies  # 随请求提交的cookies字典
data  # string, 请求数据
endpoint  # string, 当前请求的端点值
files  # MultiDict对象，所有上传文件，key为input标签中的name
form  # ImmutableMultiDict，解析后的表单数据，key为input标签中的name
values  # CombineMultiDict，结合了args和form

# 获取请求中的数据，默认读取为字节字符串(bytestring)
# as_test=True 会返回解码后的unicode字符串
get_data(cache=True, as_text=True, parse_from_data=False)

# 返回json数据，若MIME类型不是JSON，则返回None
# silent=True, 解析出错返回None，否则400
get_json(self, force=False, silent=False, cache=True)

headers  # EnvironHeaders对象，可以以字典形式操作
is_json  # bool, 通过MIME类型判断是否为JSON数据
json  # 内部调用get_json()
method  # 请求的HTTP方法
referrer  # 请求发起的源URL，即referer
scheme  # 请求的URL模式（http 或 https)
user_agent  # 用户代理信息
```

> MultiDict类是字典之类，实现了一个键对应多个值的情况（一个文件上传字段可能会接收多个文件）。
>
> 通过`getlist()`方法获取文件对象列表。
>
> `ImmutableMultiDict`的值不可修改
>
> 参考：http://werkzeug.pocoo.org/docs/latest/datastructures/

### 设置http方法

默认是GET方法，可以通过给`methods`参数传入一个列表来选择方法

测试案例

```python
@app.route('/test_post', methods=['POST'])
def test_post():
    data = json.loads(request.get_data())
    data['score'] = 100
    return jsonify(data)
```

获取响应数据

```python
data = {
    'name': 'lily',
    'age': 19
}
resp = requests.post("http://127.0.0.1:5000/test_post", json=data)
print(resp.json())
```



### URL参数转换器

路由可以指定参数的数据类型，默认都是string，可以指定不同的转换器

```python
@app.route('hello/<int:year>')
@app.route('hello/<float:month>')
# 包含斜线的字符串，static路由的URL规则中的filename变量就用这个转换器
@app.route('hello/<path:file_save_path>')

# 匹配配一系列给定值中的一个元素
@app.route('hello/<any(blue, white, red):color>')

@app.route('hello/<uuid:merchant_id>')
```

### 请求钩子

作用：用于在进行请求处理前、后执行一些代码。

比如以下5个请求钩子

```python
# 处理第一个请求前运行
@app.before_first_request

# 处理每个请求前运行
@app.before_request

# 每个请求结束后运行，如果没有未处理的异常抛出
@app.after_request

# 每个请求结束后运行
# 如果发生异常，会传入异常对象作为参数到注册的函数中
@app.teardown_request

# 在视图函数内注册一个函数， 会在这个请求结束后运行
@app.after_this_request
```

请求处理函数调用示意图如下

![请求处理函数调用示意图.drawio](images/请求处理函数调用示意图.drawio.svg)

**应用场景**

- before_first_request：运行程序前执行的初始化操作，创建数据库表、添加管理员用户等
- before_request：记录用户的最后在线时间。
- after_request：视图函数中进行了数据库的操作，进行完毕后提交修改

> after_request 钩子和after_this request 钩子必须接收一个响应类对象作为参数，并且返回同一个或更新后的响应对象。
>
> ? 没看懂

## HTTP响应

### 响应报文

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 17
Server: Werkzeug/2.0.2 Python/3.8.12
Date: Sat, 08 Jan 2022 06:45:34 GMT
```

对应

```
协议 状态码 原因短语  # 状态行       ─┐
key1: value1       # ─┐           |
...                #  ├ 首部字段   |- 报文首部
keyn: valuen       # ─┘          ─┘
                   # 空行：用于隔开报文首部和报文主体
<h1>hello</h1>     # ─┐
...                #  ├ 报文主体
...                # ─┘
```

### 常见HTTP状态码

| 状态码 | 原因短语              | 说明                                                         |
| ------ | --------------------- | ------------------------------------------------------------ |
| 200    | OK                    | 请求被正常处理                                               |
| 201    | Created               | 请求被处理，并创建了一个新资源                               |
| 204    | No Content            | 请求处理成功，但无内容返回                                   |
| 301    | Moved Permanently     | 永久重定向                                                   |
| 302    | Found                 | 临时性重定向                                                 |
| 304    | Not Modified          | 请求的资源未被修改，重定向到缓存的资源                       |
| 400    | Bad Prequest          | 表示请求无效，即请求报文中存在错误                           |
| 401    | Unauthorized          | 类似403，表示请求的资源需要获取授权信息，在浏览器中会弹出认证弹窗 |
| 403    | Forbidden             | 表示请求的资源被服务器拒绝访问                               |
| 404    | Not Found             | 表示服务器上无法找到请求的或URL无效                          |
| 500    | Internal Server Error | 服务器内部发生错误                                           |

响应状态码详细列表：https://tools.ietf.org/html/rfc7231

### Flask响应方式

就是视图函数的响应方式，举例如下

```python
# 方式1：只返回响应主体
@app.route('/hello')
def hello():
    return 'hello'

# 方式2：返回响应主体、状态码
@app.route('/hello')
def hello():
    return 'hello', 201

# 方式3：返回响应主体、状态码、首部字段
@app.route('/hello')
def hello():
    return 'hello', 302, {'Location':'http://www.example.com'}
```

> 视图函数可以返回最多由三个元素组成的元组：响应主体、状态码、首部字段

### 重定向

就是网页跳转

这个视图函数就是一个重定向的例子

```python
@app.route('/hello')
def hello():
    return 'hello', 302, {'Location':'http://www.baidu.com'}
```

在flask中可以简化为

```python
from flask import Flask, redirect
@app.route('/hello')
def hello():
    return redirect('http://www.baidu.com')
```

重定向到其他视图

```python
from flask import Flask, redirect , url_for
@app.route('/')
def index():
    return 'hello'

@app.route('/hello')
def hello():
    return redirect(url_for('index'))
```

### 响应错误

一般用`abort()`返回指定的错误响应代码

```python
from flask import Flask, abort
@app.route('/404')
def not_found():
    abort(404)
```

> 无需调用return语句，会自动中断，abort后面的代码都不会执行

### 响应格式

大多数情况下，格式都是HTML。

通过改变Content-Type可以改变数据格式

```
Content-Type: text/html; charset=utf-8
```

> MIME类型(又称为media type或content type)
>
> 是一种用来标识文件类型的机制。与文件扩展名相对应。
>
> 格式为：类型名/子类型名。
>
> - text/html: 就是HTML的MIME类型
> - image/png: 就是png图片的MIME类型
>
> 可以参考：https://www.iana.org/assignments/media-types/media-types.xhtml

可以使用`make_response()`方法生成响应对象，传入响应的主体，然后设置该对象的mimetype属性

```python
from flask import make_reponse

@app.route('/foo')
def foo():
    response = make_reponse('Hello')
    response.mimetype = 'text/plain'
    # 效果相同
    # response.headers['Content-Type']='text/plain; charset=utf-8'
    return response
```

**MIME数据类型**

- text/html：默认的数据格式
- text/plain：纯文本，HTML标签会原封不动地展示出来
- application/xml：XML一般作为AJAX请求的响应格式，或是Web API的响应格式。
- application/json：flask提供了`jsonify()`函数可以方便地返回JSON响应

json用法

```python
# 参数方式
@app.route('/foo')
def foo():
    return jsonify(name='lily', age=18)

# 字典方式
@app.route('/foo')
def foo():
    jsonify({'name': 'lily', 'age', 18})

# 默认生成200响应，可以增加返回值以更改响应类型
@app.route('/foo')
def foo():
    jsonify(message='error'), 500
```

### Cookie

**为什么要用cookie**：HTTP是无状态协议(stateless)，在响应结束后，服务器不会留下任何关于对方状态的信息。

**如何理解cookie**：可以把cookie理解为保存在浏览器的小型文本数据。

**cookie运作方式**：浏览器接收到服务器发来的cookie之后，下次向同样服务器发请求时会携带cookie数据，存储在字段`Cookie`内。

**cookie使用场景**：

- 用户的登录状态
- 视频上次播放位置
- 语言偏好等

如何在flask中使用cookie

```python
from flask import make_response

@app.route('/set/<name>'):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response
```

这会在报文首部创建一个Set-Cookie字段

```
Set-Cookie: name=Lily;Path=/+
```

浏览器保存了cookie后，下次浏览器再向服务器发送请求时就会自动带上这个cookie

#### Response类的常用属性和方法

| 方法/属性    | 说明                                                    |
| ------------ | ------------------------------------------------------- |
| headers      | Werkzeug的Headers对象，表示响应首部，可以像字典一样操作 |
| status       | str，状态码                                             |
| status_code  | 状态码，整形                                            |
| mimetype     | MIME类型（仅包括内容类型部分）                          |
| set_cookie() | 用来设置一个cookie                                      |

> 此外也有`get_json()`、`is_json()`方法以及json属性

#### set_cookie()常用参数

| 参数     | 说明                                           |
| -------- | ---------------------------------------------- |
| key      | 键                                             |
| value    | 值                                             |
| max_age  | int, cookie被保存的时间                        |
| expires  | datetime对象或UNIX时间戳，具体过期时间         |
| path     | 限制cookie只在给定的路径可用，默认整个域名     |
| domain   | 设置cookie可用的域名                           |
| secure   | bool，若为True，只有通过HTTPS才可以使用        |
| httponly | bool，若为True，禁止客户端JavaScript获取cookie |

### Session

session可以理解为加密的Cookie。

有些敏感的数据，比如账号密码如果存在cookie里，那别人是可以伪装的。

> 注意这里的session是有差异的。
>
> Flask的session指加密的Cookie，存储在浏览器上的一个名为session的cookie里。
>
> 而编程中的session指**用户会话(user session)**，即服务器和客户端之前的交互活动。

#### 1.设置程序秘钥

作用：用于加密、解密数据

```python
app.secret_key = 'ABCD'
```

更安全的做法是写入环境变量，比如`.env`文件

```
SECRET_KEY = ABCD
```

然后在代码中获取

```python
import os
app.secret_key = os.getenv('SECRET_KEY', '默认秘钥')
```

#### 2. 模拟用户认证

```python
from flask import session
...
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))
```

当用户访问http://127.0.0.1:5000/login时

就会添加一个名为session的cookie，里边存着`logged_in`

除非知道秘钥，否则加密的session用户是无法修改的。

#### 如何使用session？

重定向到hello视图后，来修改

```python
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = f'hello, {name}!'
        if 'logged_in' in session:
            response += '[Authticated]'
        else:
            response += '[Not Authenticatetd]'
        return response
        
```

可以用`session['logged_in']`或`session.get('logged_in')`获取值。

案例二：通过判断是否登录决定用户能否访问到管理界面



```python
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page!'
```

#### 删除session项目

用户登出

```python
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))
```

#### 其他

默认情况下session 会在用户关闭浏览器时删除

通过设置

```python
session.permanent = True
```

将session有效期延长至默认31天

通过环境变量`PERMANENT_SESSION_LIFETIME`来修改这个时间，这是一个`datetime.timedelta`对象

> session还是不能存储密码等敏感信息，因为即使不知道密钥还是可以被某些工具破解session内容。

## Flask上下文

Flask的两种上下文：

- **程序上下文**（application context）：存储程序运行所必须的信息
- **请求上下文**（request context）：存储请求的各种信息，如请求的URL，HTTP方法等。

### 上下文全局变量

Flask将请求报文封装在**request**对象里，使用的时候并不需要传递这个参数。

> 正常情况下，视图函数使用request前必须要给函数传入这个对象，这样会造成大量没有必要的重复。

大概原理：

> Flask 会在每个请求产生后自动激活当前请求的上下文，激活请求上下文后， request 被临时设为全局可访问 而当每个请求结束后， Flask 就销毁对应的请求上下文。

多线程的情况下，Flask通过本地线程（thread local）技术将请求对象在特定的线程和请求中全局可访问。

> 像`response`对象这样好用的上下文全局变量，Flask一共提供了四个

| 变量名      | 类型       | 说明                                                         |
| ----------- | ---------- | ------------------------------------------------------------ |
| current_app | 程序上下文 | 指向处理请求的当前程序实例                                   |
| g           | 程序上下文 | 替代python的全局变量用法，确保仅在当前请求中可用。用于存储全局数据，每次其你去都会重设 |
| request     | 请求上下文 | 封装客户端发出的请求报文数据                                 |
| session     | 请求上下文 | 用于存储请求之间的数据，通过Cookie实现。                     |

### 激活上下文

以下情况Flask会自动激活**程序上下文**

- `flask run`启动程序时
- `app.run()` 启动程序时
- 执行使用 `@app.cli.command()` 装饰器注册的flask命令时
- 使用 `flask shell` 启动 python shell时

当请求进入时， Flask 会自动激活**请求上下文**，这时我们可以使用 request session 变量。

请求上下文被激活时，程序上下文也被自动激活 当请求处理完毕后，请求上下文和程序上下文也会自动销毁。

> `url_for()`和`jsonify()`等函数也只能在视图函数中使用。

手动激活上下文，比如可以在一个普通的shell中

```python
from app import app
from flask import current_app

with app.app_context():
    print(current_app.name)
    
# 效果相同
app_context = app.app_context()
app_context.push()  # 激活上下文
print(current_app.name)

app_context.pop()  # 退出上下文
```

```
app
```

创建请求上下文

```python
with app.text_request_context('/hello'):
    print(request.method)
```

### 上下文钩子
