

```
flask shell
```

配置shell上下文

```python
# app.py
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note)
```

这样，打开flask shell就能直接使用db和Note了。



手动激活上下文

```python
from app import app
from flask import current_app

with app.app_context() as current_app:
    print(app.name)
    
# 效果相同
app_context = app.app_context()
app_context.push()  # 激活上下文
print(app.name)

app_context.pop()  # 退出上下文
```

创建请求上下文

具体参数查看：https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.test_request_context

```python
with app.test_request_context('/hello'):
    print(request.method)
    
    
request_context = app.test_request_context('/hello')
request_context.push()
print(request.method)

request_context.pop()
```

request的常用方法

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
request.view_args  # 以字典形式返回端点参数值
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