## 部署MySQL

查看mysql可用版本

```
docker search mysql
```

拉取mysql5.7的镜像

```
docker pull mysql:5.7
```

查看是否成功mysql5.7的镜像

```
docker images
```

```
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
mysql         5.7       738e7101490b   4 days ago     448MB
```

创建配置文件

```
cd /opt
mkdir -p docker_v/mysql/conf
cd docker_v/mysql/conf/
touch my.cnf
```

运行容器

```
docker run -p 3306:3306 --name mysql -v /opt/docker_v/mysql/conf:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
```

命令说明：

- **-p 3306:3306：**将容器的3306端口映射到主机的3306端口
- **-v /opt/docker_v/mysql/conf:/etc/mysql/conf.d：**将主机/opt/docker_v/mysql/conf目录挂载到容器的/etc/mysql/conf.d
- **-e MYSQL_ROOT_PASSWORD=123456：**初始化root用户的密码
- **-d:** 后台运行容器，并返回容器ID

查看运行中的容器

```
docker ps
```

查看到容器id为

```
CONTAINER ID
f09484174bc3
```

登录到docker容器

```
docker exec -it f09484174bc3 /bin/bash
```

进入mysql

```
mysql -h localhost -u root -p
```



关闭容器

```
docker stop f09484174bc3
```

删除容器

```
docker rm f09484174bc3
```

删除镜像

```
docker rmi 738e7101490b
```

## 部署redis

https://www.runoob.com/docker/docker-install-redis.html

docker拉取redis镜像

```
docker pull redis:latest
```

运行redis容器

```
docker run -itd --name redis-test -p 6379:6379 redis
```

- `-i` 选项：表示要以交互式模式运行容器，即启动容器的标准输入（stdin）通道。通常需要和 `-t` 选项一起使用才能起到实际效果。
- `-t` 选项：表示为容器分配一个虚拟终端（TTY），即启动容器的标准输出（stdout）通道。通常需要和 `-i` 选项一起使用才能起到实际效果，以便用户可以在容器中交互式地执行命令。
- `-d` 选项：表示要以守护进程（后台）模式运行容器，即容器将在后台运行而不是前台。通常在需要后台运行容器的场景下使用，例如运行 Web 服务器等服务。



测试redis-cli服务

```
docker exec -it redis-test /bin/bash
```

## 安装python

python有许多安装版本

https://hub.docker.com/_/python

```
# 指定安装版本
docker pull python:3.10.11-slim

# 不用指定版本，会自动选择最新的，比如3.10.11
docker pull python:3.10-slim
```

在 Docker 中，slim、bullseye 和 buster 是三个不同的 Debian Linux 版本，它们的差异在于它们所基于的 Debian 版本不同。

- slim：是一个精简的 Debian 版本，基于 Debian Buster 的最小化安装，只包含必需的软件包，因此镜像非常小巧。但是，由于其只包含了必需的软件包，可能会导致某些应用程序无法正常运行。
- bullseye：是基于 Debian Bullseye 的完整版，包含了较为完整的软件包，因此相对于 slim 版本，镜像会更大。bullseye 是 Debian 的下一个稳定版本（当前是测试版本）。
- buster：是 Debian 的上一个稳定版本，因此它比较成熟和稳定。与 bullseye 版本相比，镜像大小可能会稍微大一些，但是比 slim 版本更全面。

安装完毕后

```
docker images
```

```
REPOSITORY            TAG         IMAGE ID       CREATED         SIZE
python                3.10-slim   5c359f2246d1   8 days ago      125MB
```

进入python

```
docker run -it python:3.10-slim /bin/bash
```

查看python版本

```
python --version
```

```
Python 3.10.11
```



python的Dockfile示例

```dockerfile
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]
```



