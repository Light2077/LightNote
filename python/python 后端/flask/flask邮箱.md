https://waynerv.github.io/flask-mailman/

# 电子邮件

## Flask-Mail

https://github.com/mattupstate/flask-mail

https://pythonhosted.org/Flask-Mail/

```
pip install flask-mail
```

初始化

```python
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)
```

更加常用的初始化方式是

```python
mail = Mail()

app = Flask(__name__)
mail.init_app(app)
```

在这种情况下，将使用Flask的Current_App上下文全局的配置值发送电子邮件。如果您在同一过程中运行多个应用程序，但是具有不同的配置选项，这将很有用。

### 配置Flask-Mail

```python
# 用于发送右键的SMTP服务器
MAIL_SERVER = 'localhost'

MAIL_PORT = 25

# 是否使用STARTTLS
# MAIL_PORT = 587
MAIL_USE_TLS = False

# 是否使用SSL/TLS
# MAIL_PORT = 465
MAIL_USE_SSL = False

# 发信服务器的用户名
MAIL_USERNAME = "123456@qq.com"

# 发信服务器的密码
MAIL_PASSWORD = None

# 默认发信人
MAIL_DEFAULT_SENDER = None
```

常用电邮服务提供商的SMTP配置

- `smtp.gmail.com`
- `smtp.qq.com`
- `smtp.sina.com`
- `smtp.163.com`
- `smtp.office365.com`

```python
# Gmail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PASSWORD = '<邮箱密码>'

# qq
MAIL_SERVER = 'smtp.qq.com'
MAIL_PASSWORD = '<授权码>'

# 新浪
MAIL_SERVER = 'smtp.sina.com'
MAIL_PASSWORD = '<邮箱密码>'

# 163
MAIL_SERVER = 'smtp.163.com'
MAIL_PASSWORD = '<授权码>'

# outlook
MAIL_SERVER = 'smtp.office365.com'
MAIL_PASSWORD = '<邮箱密码>'
```

### 发送邮件

```python
from flask_mail import Message

@app.route("/")
def index():

    msg = Message("Hello",
                  sender="from@example.com",
                  recipients=["to@example.com"])
```



### 构建邮件数据

```python
from flask_mail import Message
from app import mail

message = Message(
    subject='Hello, world!',
    recipients=['Zorn <zorn@example.com>'],
    body='hello world'
)
```

### 发送邮件

```python
mail.send(message)
```

## 使用事务邮件服务SendGird

- Mailgun：https://www.mailgun.com/
- SendGrid：https://sendgrid.com/

## 案例

实现效果

访问：http://127.0.0.1:5000/send_email

会向指定的邮箱发送一封邮件。

创建以下结构的文件

```
|-test_email
  |-app.py
```

在`app.py`中

```python
from flask import Flask
from flask_mail import Mail, Message
mail = Mail()
app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_USERNAME"] = "223@qq.com"
app.config["MAIL_PASSWORD"] = "xxx"
mail.init_app(app)
@app.route("/")
def index():
    msg = Message("Hello",
                  sender="223@qq.com",
                  recipients=["123@qq.com"])
    mail.send(msg)
    return "success!"
```

QQ邮箱的授权码（`MAIL_PASSWORD`）如何获取：https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256