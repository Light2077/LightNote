https://www.cnblogs.com/whtjyt/p/16360069.html

主要通过request对象来获取：

- GET请求的数据获取：`request.args.get("username")`
- POST请求的数据获取：`request.form.get("username")`

### Get方式

前端代码

```html
<form action="/test" method="GET">
    <div>username<input name="username" type="text"/></div>
    <div>password<input name="password" type="password"></div>
    <input type="submit" value="提交">
</form>
```

Python代码

```python
from flask import Flask, request

app = Flask(__name__)
@app.route("/test")
def test():
    a = request.args
    print(a.get("username"))
    print(a.get("password"))
    return "success"
```

### Post方式

前端代码

```html
<form action="/test" method="POST">
    <div>username<input name="username" type="text"/></div>
    <div>password<input name="password" type="password"></div>
    <input type="submit" value="提交">
</form>
```

Python代码

```python
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/test", methods=["POST"])
def test():
    a = request.form
    print(a.get("username"))
    print(a.get("password"))
	#当前端传递的数据为复选框，可以使用getlist,返回的为list类型数据
    return "success"
```

