官网

https://www.djangoproject.com/

手动创建一个项目

```shell
django-admin startproject day01
```

命令行创建项目

```
django-admin startproject mysite
```

https://docs.djangoproject.com/zh-hans/3.1/intro/tutorial01/

```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```



直接运行

```shell
python manager.py runserver

# 加参数可以指定端口
python manage.py runserver 8080
```



建立应用

```
python manage.py startapp App
```

