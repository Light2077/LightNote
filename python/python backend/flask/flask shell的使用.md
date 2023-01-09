

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

```python
with app.test_request_context('/hello'):
    print(request.method)
    
    
request_context = app.test_request_context('/hello?name=Light')
request_context.push()
print(request.method)

request_context.pop()
```

request的常用方法

假设请求URL为：http://127.0.0.1:5000/hello?name=Light

获取到的request属性为

```python
request.path  # '/hello'
request.full_path  # '/hello?name=Light'
request.host  # '127.0.0.1:5000'
request.host_url  # 'http://127.0.0.1:5000/'
request.base_url  # 'http://127.0.0.1:5000/hello'
request.url  # 'http://127.0.0.1:5000/hello?name=Light'
request.url_root  # 'http://127.0.0.1:5000/'

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
request.data  # string, 请求数据
request.endpoint  # string, 当前请求的端点值
request.files  # MultiDict对象，所有上传文件，key为input标签中的name
request.form  # ImmutableMultiDict，解析后的表单数据，key为input标签中的name
request.values  # CombineMultiDict，结合了args和form

# 获取请求中的数据，默认读取为字节字符串(bytestring)
# as_test=True 会返回解码后的unicode字符串
request.get_data(cache=True, as_text=True, parse_from_data=False)

# 返回json数据，若MIME类型不是JSON，则返回None
# silent=True, 解析出错返回None，否则400
request.get_json(self, force=False, silent=False, cache=True)

request.headers  # EnvironHeaders对象，可以以字典形式操作
request.is_json  # bool, 通过MIME类型判断是否为JSON数据
request.json  # 内部调用get_json()
request.method  # 请求的HTTP方法
request.referrer  # 请求发起的源URL，即referer
request.scheme  # 请求的URL模式（http 或 https)
request.user_agent  # 用户代理信息
```

> MultiDict类是字典之类，实现了一个键对应多个值的情况（一个文件上传字段可能会接收多个文件）。
>
> 通过`getlist()`方法获取文件对象列表。
>
> `ImmutableMultiDict`的值不可修改
>
> 参考：http://werkzeug.pocoo.org/docs/latest/datastructures/