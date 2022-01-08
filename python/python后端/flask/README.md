[Flask入门教程](https://read.helloflask.com/c0-preface)

[Flask + pyecharts](https://mp.weixin.qq.com/s?__biz=Mzg2MTY3ODk2Mg==&mid=2247491490&idx=1&sn=89422a51ae1b1c15640ae27e9ce32102&source=41#wechat_redirect)

[Jinjia](https://jinja.palletsprojects.com/)

[李辉博客](https://greyli.com/)



安装Flask会自动安装以下依赖

| 名称         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| Jinja2       | 模板渲染引擎                                                 |
| MarkupSafe   | HTML字符转义(escape)工具                                     |
| Werkzeug     | WSGI工具集，处理请求与响应，内置WSGI开发服务器、调试器和重载器 |
| click        | 命令行工具                                                   |
| itsdangerous | 提供各种加密签名功能                                         |

客户端与服务端的交互：

- 用户在浏览器输入URL访问某个资源
- 服务端接收用户请求并分析请求URL
- 为这个URL执行特定的处理函数
- 生成响应并返回给浏览器
- 浏览器接受并解析响应，将信息显示在页面中



视图函数的基本使用：

- 单一路由：访问单个页面使用
- 带参数的路由
- 带参数，带默认值的路由

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"


@app.route("/hello/<name>")
def hello(name):
    return "hello %s!" % name


@app.route("/buy", defaults={"goods": "coffee"})
@app.route("/buy/<goods>")
def buy(goods):
    return "you bought %s" % goods

if __name__ == '__main__':
    app.run()
```

测试结果

- http://127.0.0.1:5000/: 显示hello world
- http://127.0.0.1:5000/hello: 报错
- http://127.0.0.1:5000/hello/lily: 显示hello lily
- http://127.0.0.1:5000/buy：显示you bought coffee
- http://127.0.0.1:5000/buy/flower: 显示you bought flower



补充：获取请求URL中的查询字符串

```python
from flask import request
...

@app.route('/hello')
def hello():
    name = request.args.get('name', 'world')
    reteurn "hello, %s!" % name
```



### flask run

基本使用：

```
flask run
```

自动发现程序实例规则：

- 寻找当前目录下的`app.py`和`wsgi.py`，并从中寻找名为`app`或`application`的程序实例
- 从环境变量`FLASK_APP`对应的值寻找名为`app`或`application`的程序实例
- 如果安装了`python-dotenv`，会自动从`.flaskenv`和`.env`文件中加载环境变量。`.env`优先级更高。

> 教程采用了第三种方式，安装`python-dotenv`并且创建`.flaskenv`和`.env`文件。
>
> 其中`.env`用于存储敏感信息，比如Email服务器的账号密码。

使服务器外部可见

```
flask run --host=0.0.0.0
```

更改端口

```
flask run -port=8000
```

使用环境变量配置

```ini
FLASK_RUN_HOST = 0.0.0.0
FLASK_RUN_PORT = 8000
```

> FLASK内置的命令都可以使用这种模式定义默认选项值，环境变量名格式为：
>
> `FLASK_<COMMAND>_<OPTION>`：FLASK + 命令名 + 可选参数名

### 运行环境设置

开发环境（development enviroment）：本地编写和测试程序时的计算机环境。

生产环境（production enviroment）：网站部署上线供用户访问时的服务器环境

将环境变量FLASK_ENV 的值设置为 development。

```ini
FLASK_ENV = development
```

会开启调试模式，自动激活Werkzeug内置的**调试器(debugger)**和**重载器(reloader)**

调试器允许你在错误页面上执行python代码。

重载器：检测文件变动，代码修改后立即重启开发服务器。

默认使用Werkzeug内置的stat重载器，为了更优秀的体验，可以使用另一个python库watchdog



### python shell

flask有很多操作需要在shell里测试。

需要使用

```
flask shell
```

来打开python shell

### url_for()

如果程序中的URL都是以硬编码的方式写出，那如果需要更改的时候，复杂度会大大提升。

**端点**：在Flask中，**端点**用来标记一个视图函数以及对应的URL规则。端点的默认值为视图函数的名称。例如：

```python
@app.route('/')
def inedx():
    return "Hello World!"
```

这个路由的端点就是`index`。调用`url_for("index")`即可获取对应的URL`/`

如果是动态URL可以传入相应的参数，比如

```python
@app.route("/hello/<name>")
def hello(name):
    return "hello %s!" % name
```

使用

```python
url_for('say_hello', name='lily')
```

得到`/hello/lily`

> 使用`url_for()`函数时，将`_external`参数设为`True`，就会生成完成的URL，比如http://localhost:5000/hello/

### Flask命令

通过`app.cli.command()`装饰器可以注册一个flask命令。

例如：

```python
@app.cli.command()
def hello():
    click.echo('hello world!')
```

使用`flask hello`即可触发该函数。

`click`模块的`.echo()`方法可以你在命令行界面输出字符。

### 模板与静态文件

**MVC架构**：数据处理(Model)、用户界面(View)、交互逻辑(Controller)。最初MVC架构师用来设计桌面程序的。