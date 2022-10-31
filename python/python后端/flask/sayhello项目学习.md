项目下载

```
git clone git@github.com:greyli/sayhello.git
```

切换到项目内创建虚拟环境

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

安装依赖包

```
pip install -r requirements.txt
```



启动项目

```
flask forge
flask run
```

访问：http://127.0.0.1:5000/即可看到示例程序

SayHello程序结构



```
  |- sayhello
    |- static
    |- templates
    |- __init__.py
    |- commands.py  # 自定义Flask命令
    |- errors.py  # 错误处理
    |- forms.py  # 表单
    |- models.py  # 数据库模型
    |- settings.py  # 配置文件
    |- views.py  # 视图函数
```

原先的各种初始化工作转移到`__init__.py`内了

```python
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask('sayhello')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from sayhello import views, errors, commands

```

而环境变量文件`.flaskenv`，`.env`也转移到文件目录的上一层

```
  |- sayhello
    |- sayhello
    |- venv
    |- .flaskenv
    |- data.db
    ...
```





## 配置文件

这里采用配置文件写入`settings.py`的方式

在`__init__.py`中

```python
app.config.from_pyfile('settings.py')
```

`settings.py`中

```python
# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import sys

from sayhello import app

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)

```

## Web程序开发流程

- 分析需求，列出功能清单或写需求说明书。
- 设计程序功能，写功能规格书和技术规格书。
- 进入开发与测试的迭代。
- 调试和性能等专项测试。
- 部署上线（ deployment ） 。
- 运行维护与营销等。

前端开发的主要流程如下：

- 根据功能规格书画页面草图（ sketching ） 。
- 根据草图做交互式原型图（ prototyping ） 。
- 根据原型图开发前端页面（ HTML 、css 、JavaScript ） 。


后端开发的主要流程如下：

- 数据库建模。
- 编写表单类。
- 编写视图函数和相关的处理函数。
- 在页面中使用Jinja2 替换虚拟数据。



原型设计工具Axure RP、MockPlus。



数据库建模

```python
from datetime import datetime

from sayhello import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
```

表单类创建

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()
```

视图函数

```python
from flask import flash, redirect, url_for, render_template

from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', form=form, messages=messages)
```



