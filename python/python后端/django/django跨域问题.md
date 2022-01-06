# 什么是跨域问题

pass

# 怎么解决跨域问题

1.安装`django-cors-headers`

```
pip install django-cors-headers
```

2.修改配置文件`settings.py`

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://*.*.*.*',
    # "http://localhost",
    # "http://10.0.108.*",
)
CORS_ALLOW_METHODS = ('DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'VIEW',)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
```

重点是配置白名单，注意要加`http://`前缀。

