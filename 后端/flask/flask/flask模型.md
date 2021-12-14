# flask模型

MTV框架中的M

主要和数据库进行交互，进行数据持久化保存。传输使用pymysql构建**数据库**与**flask app**的桥梁。

ORM(objext relation model) 映射，需要准备一个类，对应的是一张数据库中的表。对象则对应一条数据。比如学生表：存的字段有ID，name，age，score。那这个类的属性也有id，name，age，score。



设定配置文件

# flask-script

flask-script,是一个让你的命令行支持自定义命令的工具，它为flask程序添加了一个命令行解释器，可以让我们的程序从命令行直接执行相应的程序。



怎么使用



怎么启动



需要用manager的命令来启动



runserver的可选参数





使用manager的自定义命令





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

filter是布尔查找，记得结尾要加上或



以下是User.query.filter()括号内的内容



## 排序(order_by)



## 限制(limit)

limit 常常和 offset一起使用。应用场景就是分页操作等，不过flask封装好了一个分页的操作



## 删除

逻辑删除和物理删除，一般在开发过程中都使用物理删除。



## 更新





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

  

- 配置数据库的连接路径里

  

- 创建一个包ext与数据库映射建立关系

  - 在中添加

    

  - 在apps/__init__.pypython
    from flask import Flask
    import settings
    from ext import db
    
    def create_app():
        ...
        app.config.from_object(settings.DevConfig)
    	db.init_app(app)
        ...
        return app
    python
  app = create_app()
  manager = Manager(app=app)
  # 建立数据库映射
  migrate = Migrate(app=app, db=db)
  # 把migrate的命令交给manager处理
  manager.add_command('db', MigrateCommand)
  python
  class User(db.Model):
      # db.Column 映射表中一列
      id = db.Column(db.Integer, primary_key=True, autoincrement=True)
      username = db.Column(db.String(15), nullable=False)
      password = db.Column(db.String(12), nullable=False)
      phone = db.Column(db.String(11), unique=True)
      rdatetime = db.Column(db.DateTime, default=datetime.now)
  
      def __repr__(self):
          return self.username
  python
    from apps.user.models import User
    
    python app.py db init
    
    python app.py db migrate
    
    # 如果你原来的数据库里有其他的表，会被删掉。
    python app.py db upgrade
    
    # 这个命令可以降级，但是之前删除的表中的数据无法恢复
    python app.py db downgrade
    python
# 1对多的使用。user是1 article是多
user.articles  # 可以获取该用户的所有文章
article.user  # 可以获取该文章的用户

pip install flask-bootstrap
exts/__init__.pypython
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()
apps/__init.pypython
from exts import bootstrap
def create_app():
    ...
    bootstrap.init_app(app)
    ...
    return app
template/base.htmljinja2
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
python
# 密码加密 sha256$salt$qweq
user.password = generate_password_hash(password)

# 验证密码是否正确
if user and check_password_hash(user.password, password):
    pass
python
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
js
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
python
response = redirect(url_for('user.index'))
response.set_cookie('uid', user.id, max_age=1800)
python
uid = request.cookies.get('uid', None)
python
response = redirect(url_for('user.index'))
response.delete_cookie('uid')
python
# settings.py
SECRET_KEY = 'asdfasdfasfdasdf'  # 随便赋值
python
from flask import session
session['uid'] = user.id
python
uid = session.get('uid', None)
python
del session['uid']  # 删除一个键值对

session.clear()  # 把整个空间都删除
python
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
flask.gflask.gpython
@user_bp.before_app_request
def before_request():
    if request.path in required_login_set:
        uid = session.get('uid', None)
        if uid:
            user = User.query.get(uid)
            g.user = user  # g -- global 是一个对象，是本次请求的对象
        else:
            return redirect(url_for('user.login'))
flask.gpython
# 处理完视图函数后会经过这个函数，拿到response的时候往回走
# 相当于每次给响应的时候都会给路由加个cookie
@user_bp.after_app_request
def after_request_demo(response):
    response.set_cookie('name', 'zhangsan', max_age=300)
    return response
html
<form enctype="multipart/form-data">
    
</form>
python
request.files.get('icon')
`

