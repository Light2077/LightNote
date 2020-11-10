创建环境
```shell
conda create -n BlueWhale python==3.6.12
```

激活环境

```shell
conda activate BlueWhale
```

安装django 3.1.2

```shell
pip install django==3.1.2
```



创建项目

```shell
django-admin startproject BlueWhale
```

进入项目文件夹，测试项目是否创建成功

```
cd BlueWhale
python manage.py runserver
```



创建新的应用

```shell
python manage.py startapp demo
```

注册APP，修改根目录`settings.py`文件

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo',  # new app
]
```



在`demo/models.py`下添加

```python
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

安装mysqlclient（django官方推荐使用mysqlclient替代pymysql）

```shell
pip install mysqlclient
```



通过finalshell连接并进入数据库

```
mysql -u root -p
```

创建一个名为BlueWhale的数据库

```mysql
create database BlueWhale charset=utf8;
```

修改`settings.py`文件关于数据库的配置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # 数据库引擎
        'NAME': 'BlueWhale',  # 数据库名，先前创建的
        'USER': 'root',     # 用户名，可以自己创建用户
        'PASSWORD': 'AutoML@1',  # 密码
        'HOST': '172.16.2.114',  # mysql服务所在的主机ip
        'PORT': '3306',         # mysql服务端口
    }
}
```

迁移数据库

```shell
python manage.py makemigrations demo
python manage.py migrate
```

