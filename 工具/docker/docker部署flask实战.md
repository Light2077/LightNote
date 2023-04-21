### 在本机创建项目

1.创建虚拟环境并进入

```
python -m venv venv
source venv/bin/activate
```

2.安装Flask

```
pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3.编写`app.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello</h1>"
```

4.测试该项目能否运行

```
flask run --host 0.0.0.0 --port 8000
```

5.导出requirements.txt

```
pip freeze > requirements.txt
```



### 编写Dockerfile

创建`Dockerfile`

```
FROM python:3.9-slim-buster

# 将工作目录设置为 /app
WORKDIR /app

# 复制当前目录下的所有文件到容器中的 /app 目录
COPY . /app

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 将容器的默认端口设置为 8000
EXPOSE 8000

# 设置环境变量
ENV FLASK_APP=app.py

# 在容器启动时运行命令
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

```

> `--no-cache-dir`的作用：
>
> 默认情况下，`pip install` 会使用缓存中的软件包来加速安装过程，如果缓存中的软件包与我们需要的软件包版本不匹配，可能会导致安装出现问题。
>
> `--no-cache-dir` 表示禁用缓存，强制从 PyPI 下载最新的软件包。

（可选）创建`.dockerignore`，在构建docker镜像拷贝文件时忽略指定的文件

```
venv/
__pycache__
```

构建docker镜像

`.`表示使用当前目录下的Dockerfile构建镜像

```
docker build -t myflaskapp:latest .
```

运行容器

```
docker run -p 8000:8000 myflaskapp:latest
```

如果希望后台运行

```
docker run -d -p 8000:8000 myflaskapp:latest
```

后台运行时查看日志

```
docker logs <container_id>
```



然后就可以访问对应端口的页面查看效果了

