- docker安装python轻量版
- docker安装flask
- 



首先docker安装python，以python3.8为例

```
docker pull python:3.8.12-slim
```

进入docker的python环境

```
docker run -it python:3.8.12-slim /bin/bash
```

安装flask

```
pip install flask=2.0.2
```

退出该容器

```
exit
```



查看刚刚运行的容器的id

```
docker ps -a
```

```
CONTAINER ID   IMAGE              ...
bc6742b7f8e7   python:3.8.12-slim ...
```

创建一个新的镜像

```
docker commit bc6742b7f8e7 flask-demo
```

查看镜像列表，确认创建成功

```
docker images
```

```
REPOSITORY    TAG           IMAGE ID       CREATED         SIZE
flask-demo    latest        09b12eabd6a0   4 seconds ago   141MB
python        3.8.12-slim   23a6a071a881   2 weeks ago     122MB
```



接下来创建所需要的flask程序和dockerfile

创建并进入一个目录

```
mkdir flask_web
cd flask_web
```

创建一个`app.py`文件，并写入如下内容

```python
# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>hello world!</h1>"
```

在当前文件夹下创建并编写Dockerfile

```dockerfile
FROM flask-demo

ADD app.py /web/app.py

WORKDIR /web
CMD flask run -h 0.0.0.0 -p 5000
```

> 如果用uwsgi做http（以后搞）

 使用build生成镜像

```
docker build -t flask_web .
```

运行镜像

```
docker run -it -p 5000:5000 flask_web
```



我是在虚拟机里创建的docker，因此需要查看虚拟机的ip

```
ifconfig
```

只需要ens33这一项

```
ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.22.129  netmask 255.255.255.0  broadcast 192.168.22.255
        ...
```

发现ip地址为 192.168.22.129

访问http://192.168.22.129:5000 即可查看hello world页面