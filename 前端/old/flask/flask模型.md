# flask模型

MTV框架中的M

主要和数据库进行交互，进行数据持久化保存。传输使用pymysql构建**数据库**与**flask app**的桥梁。

ORM(objext relation model) 映射，需要准备一个类，对应的是一张数据库中的表。对象则对应一条数据。比如学生表：存的字段有ID，name，age，score。那这个类的属性也有id，name，age，score。

```
        对应关系
类                表
属性     < - >    字段
对象              一条数据
```

设定配置文件

# flask-script

flask-script,是一个让你的命令行支持自定义命令的工具，它为flask程序添加了一个命令行解释器，可以让我们的程序从命令行直接执行相应的程序。

```shell
pip install flask-script
```

怎么使用

```python
from flask_script import Manager

manager = Manager(app=app)

if __name__ == '__main__':
    manager.run()
```

怎么启动

```shell
python app.py  # 现在就无效了
```

需要用manager的命令来启动

```
python app.py runserver
```

runserver的可选参数

```
optional arguments:
  -?, --help            show this help message and exit
  -h HOST, --host HOST
  -p PORT, --port PORT
  --threaded
  --processes PROCESSES
  --passthrough-errors
  -d, --debug           enable the Werkzeug debugger (DO NOT use in production
                        code)
  -D, --no-debug        disable the Werkzeug debugger
  -r, --reload          monitor Python files for changes (not 100% safe for
                        production use)
  -R, --no-reload       do not monitor Python files for changes
  --ssl-crt SSL_CRT     Path to ssl certificate
  --ssl-key SSL_KEY     Path to ssl key
```



使用manager的自定义命令

```python
@manager.command
def init():
    print('初始化')
```



# flask-sqlalchemy

http://www.pythondoc.com/flask-sqlalchemy/index.html

[Flask-SQLAlchemy详解](https://www.jianshu.com/p/f7ba338016b8)

flask中一般使用flask-sqlalchemy来操作数据库，使用起来比较简单，易于操作。

安装flask-sqlalchemy的同时还安装了SQLAlchemy

[python orm框架sqlalchemy介绍](https://www.jianshu.com/p/589212e62e6d)

flask-sqlalchemy 对 SQLAlchemy进行了封装，使我们在用数据库映射关系的过程中更加方便。



定义一个类，做flask到数据库的映射

## 查询

filter_by是赋值<字段名>=<值>

filter是布尔查找，记得结尾要加上`.first()`或`.all()`

```python
# 返回所有的user
users = User.query.all()

# 得到的结果是可迭代对象
users = User.query.filter_by(username=username)

# 根据主键查询用户，返回的是一个用户对象
user = User.query.get(2)
# 拿到的是一堆奇奇怪怪的语句
user = User.query.filter(User.username == 'lily')
users = User.query.filter(User.username == 'lily').all()
user = User.query.filter(User.username == 'lily').first()
user = User.query.filter(User.username == 'lily', User.age>18)
# select * from user where rdatetime > xxx
```

以下是User.query.filter()括号内的内容

```python
from sqlalchemy import or_, and_, not_
User.username.startwith('zh')
User.username.contains('zh')
User.username.like('zh%')
User.username.ilike('zh%')  # 忽略大小写

# or_ and_ not_ 的使用
# select * from user where username like '%z%' or username like '%i%'
or_(User.username.contains('z'), User.username.contains('y'))
# select * from user where username like '%z%' and rdatetime < '2020-08-20 15:30:00'
and_(User.username.contains('z'), User.rdatetime < '2020-08-20 15:30:00')

not_(User.username.contains('z'))

# select * from user where age in [17, 18, 22]
User.age.in_([17, 18, 22])
# select * from user where age between 18 and 22
User.age.between(18, 22)
"""
对于整型 / 浮点型 / 日期时间类型 可以使用
__lt__
__le__
__gt__
__ge__
__eq__
__ne__
"""
```

## 排序(order_by)

```python
User.query.order_by()

# 也可以
User.query.order_by(User.age).all()
User.query.order_by(-User.age).all()  # 降序排列

User.query.order_by('age').all()
User.query.order_by('-age').all()  # 报错
```

## 限制(limit)

limit 常常和 offset一起使用。应用场景就是分页操作等，不过flask封装好了一个分页的操作

```python
User.query.order_by('id').limit(2).offset(2).all()
```

## 删除

逻辑删除和物理删除，一般在开发过程中都使用物理删除。

```python
# 逻辑删除
user.isdelete = True
db.session.commit()

# 物理删除
db.session.delete(user)
db.session.commit()
```

## 更新

```python
# 修改属性
user.password = hashlib.sha256(password.encode('utf8')).hexdigest()
user.phone = phone
# 提交更改
db.session.commit()
```



# flask-migrate

[flask-migrate动态迁移数据库](https://www.jianshu.com/p/e4fc86fa21e8)

了解flask_migrate需要先了解flask-script，那么flask-script的作用是什么呢？flask-script的作用是可以通过命令行的形式来操作Flask。例如通过命令跑一个开发版本的服务器、设置数据库，定时任务等。

上面使用flask-script的使用以及对数据库的演示，实际开发中我们使用flask-migrate来动态的迁移数据库，使用flask-migrate必须借助flask-script。

等于说把flask-migrate的命令交给manager去管理。

# 关系总结

flask：超市

mysql：仓库

pymysql：连接超市到仓库的公路

flask-sqlalchemy：实现ORM映射，货车

flask-migrate：发布命令工具，司机，指挥货车什么时候发车

# 使用方法

- 安装：pymysql / flask-sqlalchemy / flask-migrate

  ```
  pip install flask-scripy, flask-sqlalchemy, flask-migrate
  ```

- 配置数据库的连接路径`settings.py`里

  ```python
  class Config:
      SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://alice:!Alice2077@119.45.58.134:3306/lightdb?charset=utf8'
      SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不自动追踪对象的修改
  
  class DevConfig(Config):
      ENV = 'development'
      DEBUG = True
  ```

- 创建一个包ext与数据库映射建立关系

  - 在`exts/__init__.py`中添加

    ```python
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
    ```

  - 在``apps/__init__.py`中

    ```python
    from flask import Flask
    import settings
    from ext import db
    
    def create_app():
        ...
        app.config.from_object(settings.DevConfig)
    	db.init_app(app)
        ...
        return app
    ```

- migrate在app.py中

  ```python
  app = create_app()
  manager = Manager(app=app)
  # 建立数据库映射
  migrate = Migrate(app=app, db=db)
  # 把migrate的命令交给manager处理
  manager.add_command('db', MigrateCommand)
  ```

- 创建模型

  user/models.py

  ```python
  class User(db.Model):
      # db.Column 映射表中一列
      id = db.Column(db.Integer, primary_key=True, autoincrement=True)
      username = db.Column(db.String(15), nullable=False)
      password = db.Column(db.String(12), nullable=False)
      phone = db.Column(db.String(11), unique=True)
      rdatetime = db.Column(db.DateTime, default=datetime.now)
  
      def __repr__(self):
          return self.username
  ```

- 使用命令：

  - :warning: 在app.py 中导入模型，否则执行下面的命令时无效的

    ```python
    from apps.user.models import User
    ```

  - 在终端使用db命令，会创建一个migrations文件夹，为了实现。**这条命令只需要执行一次**，之后执行剩下的两条命令即可。
  
    ```
    python app.py db init
    ```
  
  - 下面这条命令在migrations/versions下生成了个py文件，自动产生了一个版本文件。**为了保证版本的一致性，这个py文件可以手动删除**
  
    ```
    python app.py db migrate
    ```
  
  - 执行下面这条命令，相当于执行了刚刚创建的py文件中的upgrade函数。
  
    ```
    # 如果你原来的数据库里有其他的表，会被删掉。
    python app.py db upgrade
    
    # 这个命令可以降级，但是之前删除的表中的数据无法恢复
    python app.py db downgrade
    ```
  
    
  

# 博客案例分析

用户表

文章表

文章分类表

评论表

关系分析：

一对多解释：比如学生表和成绩表，一个学生可以有多个科目的成绩。学生表和成绩表建立一对多关系，那么在往成绩表里加数据时，成绩表就要依赖学生表里的姓名字段。因为如果“张三”这个人不在学生表内，成绩表就不能有一条数据是(张三，数学，100分)。

一对多http://www.pythondoc.com/flask-sqlalchemy/models.html#one-to-many

外键可以理解为B表的某一列和A表中的某一列关联起来了，A表中的这一列没有的值不能出现在B表。

- 用户 - 文章
- 文章 - 文章分类

方便的使用一对多的对象

```python
# 1对多的使用。user是1 article是多
user.articles  # 可以获取该用户的所有文章
article.user  # 可以获取该文章的用户
```

## 多对多：用户与商品

![](商品用户关系图.png)

多对多：用户对文章评论

一个用户可以评论多篇文章，一篇文章可以被多个用户评论。

思考多对多需要几张表：3张

用户表，文章表，用户文章表，关联关系是用户文章表有两个id，user_id, article_id 与用户和文章的关系相关联。

![](用户文章评论关系图.png)

## 使用flask-bootstrap

https://flask-bootstrap-zh.readthedocs.io/zh/latest/index.html

```
pip install flask-bootstrap
```

在`exts/__init__.py`

```python
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()
```

在`apps/__init.py`

```python
from exts import bootstrap
def create_app():
    ...
    bootstrap.init_app(app)
    ...
    return app
```

创建`template/base.html`

```jinja2
{% extends "bootstrap/base.html" %}
{% block title %}This is an example page{% endblock %}

{% block navbar %}
<div class="navbar navbar-fixed-top">
  <!-- ... -->
</div>
{% endblock %}

{% block content %}
  <h1>Hello, Bootstrap</h1>
{% endblock %}
```

## 密码加密解密

```python
# 密码加密 sha256$salt$qweq
user.password = generate_password_hash(password)

# 验证密码是否正确
if user and check_password_hash(user.password, password):
    pass
```

## ajax验证手机号唯一

```python
@user_bp.route('/check_phone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()

    # 返回必须是json格式, 这个code是我们人为约定的
    # code: 400 不能使用该手机号
    #       200 可以使用该手机号
    if user:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可用')
```

```js
<script>
    $('#inputPhone').blur(function () {
    let phone = $(this).val();
    let span_ele = $(this).next('span');
    if (phone.length == 11) {
        span_ele.text('');
        $.get('{{ url_for('user.check_phone') }}', {phone: phone}, function (data) {
            if (data.code == 400) {
                span_ele.css({'color': 'red'});
                span_ele.text(data.msg)
            }
        })
} else {
           span_ele.css({'color': 'red'});
           span_ele.text('手机格式错误')
}
})

</script>
```



## 会话机制：cookie

- 如何创建cookie
- 如何获取cookie
- 如何删除cookie

### 登陆状态记录

登陆成功后如何记录用户的登陆状态（页面与未登录状态不同）

http协议：无状态协议，页面不知道你是否登陆了。

用cookie和session记录状态。

cookie以key-value的形式保存数据。

服务器给浏览器留了点东西，以后每次浏览器给服务器发请求都会带上cookie。

cookie存在于响应头

session

### 创建cookie

```python
response = redirect(url_for('user.index'))
response.set_cookie('uid', user.id, max_age=1800)
```

### 获取cookie

```python
uid = request.cookies.get('uid', None)
```

### 删除cookie

```python
response = redirect(url_for('user.index'))
response.delete_cookie('uid')
```

## 会话机制：session

把cookie存在服务器，不同的浏览器存的位置还不一样。要用session必须先在配置文件加上SECRET_KEY

```python
# settings.py
SECRET_KEY = 'asdfasdfasfdasdf'  # 随便赋值
```

### 创建session

```python
from flask import session
session['uid'] = user.id
```

### 获取session

```python
uid = session.get('uid', None)
```

### 删除session

```python
del session['uid']  # 删除一个键值对

session.clear()  # 把整个空间都删除
```

## 手机验证码

网易易盾，它有个api可以通过那个api发送手机验证码。

搞清楚用户浏览器 用户手机 服务端 网易易盾这4者之间的关系。

## 权限控制

根据用户登录与否，判断是否给用户看到某页面

[flask常用钩子函数](https://www.jianshu.com/p/f619af63f6cc)

```python
# 直接应用在app上
before_first_request()
before_request()
after_request()
teardown_request()

# 应用到蓝图
before_app_first_request()
before_app_request()
after_app_request()
teardown_app_request()
```



这个函数相当于滤网，在请求某些函数时，要先走这个函数，如果不满足某些要求（登录状态）就跳转到登陆页面。

- `flask.g`是本次请求的对象。存活周期只在这次请求过程中，视图函数执行完后这个对象就没了。
- `flask.g`可以传入html模板

```python
@user_bp.before_app_request
def before_request():
    if request.path in required_login_set:
        uid = session.get('uid', None)
        if uid:
            user = User.query.get(uid)
            g.user = user  # g -- global 是一个对象，是本次请求的对象
        else:
            return redirect(url_for('user.login'))
```

### after_request

视图函数执行完毕后

- 这个函数是否还能使用`flask.g`？

```python
# 处理完视图函数后会经过这个函数，拿到response的时候往回走
# 相当于每次给响应的时候都会给路由加个cookie
@user_bp.after_app_request
def after_request_demo(response):
    response.set_cookie('name', 'zhangsan', max_age=300)
    return response
```

### teardown_app_request

最后调用

## 带图片的表单

编码方式一定要加

```html
<form enctype="multipart/form-data">
    
</form>
```

获取方式也不一样

```python
request.files.get('icon')
```

