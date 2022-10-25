真的反反复复学习了好多次了。

本来想等《Flask Web 开发实战》第二版，但是这会包含很多不确定性，还是算了。

第一版下载：[百度云](https://pan.baidu.com/s/1PkV54TnQmhaTlOTA5QpjTA?pwd=aj5u)


感觉学习需要一个框架，不然每次过了很久再回来重新学，都要重新看教材，太麻烦了啊。关键这个我自己也总结不好，挺头疼的。

总之，这个文档的内容重在使用，类似于工具文档，是上面这本书知识点的精简版。

该解释的解释一下下就好。

## 初识Flask

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

可以通过修改环境变量来修改程序主模块

linux

```
export FLASK_APP=hello
```

windows

```
set FLASK_APP=hello
```

