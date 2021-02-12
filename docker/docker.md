## docker

https://docs.docker.com/

## docker 安装

docker 安装

```shell
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

安装完毕后启动docker服务

```shell
systemctl start docker
```

运行docker的hello world示例

```shell
docker run hello-world
```

或者参考腾讯的官方文档

https://cloud.tencent.com/document/product/213/46000

## 配置镜像加速

创建`daemon.json`文件

```
vim /etc/docker/daemon.json
```

把下面的代码拷贝进文件中

```json
{
    "registry-mirrors": ["https://y4tay211.mirror.aliyuncs.com"]
}
```

重启

```
systemctl daemon-reload
systemctl restart docker
```

## 配置docker 私有仓库的安全地址

修改`/etc/docker/daemon.json`

```
{
    "registry-mirrors": ["https://y4tay211.mirror.aliyuncs.com"],
    "insecure-registries": ["10.35.166.143:5000"]
}
```



## Image镜像的概念

- 镜像是一个只读层，就是不会变化。
- 镜像可以叠加
- 最底层的镜像就是**父镜像**
- 镜像ID是一个64位的十六进制字符串(256bit)

![](https://doc.yonyoucloud.com/doc/chinese_docker/terms/images/docker-filesystems-multilayer.png)



### 获取镜像

这样会不会比较慢，需要国内源。

```shell
sudo docker pull ubuntu:12.04
# 相当于
sudo docker pull registry.hub.docker.com/ubuntu:12.04
```

Docker中国区官方镜像
https://registry.docker-cn.com

网易
http://hub-mirror.c.163.com

ustc 
https://docker.mirrors.ustc.edu.cn

中国科技大学
https://docker.mirrors.ustc.edu.cn

阿里云容器 服务
https://cr.console.aliyun.com/



```shell
docker run -t -i ubuntu:15.10 /bin/bash 
```

- -i 交互式操作
- -t 终端

### 列出本地镜像

```shell
docker images
```

## Container(容器)

容器和镜像比较类似，区别在于容器是可以写的。

查看有哪些容器在运行，-a表示查看包括未运行的容器

```shell
docker ps -a
```

启动重启停止容器

```shell
docker start container_name/container_id
docker restart container_name/container_id
docker stop container_name/container_id
```

进入容器

```shell
docker attach container_name/container_id
```

运行容器中的镜像

```shell
docker run -t -i container_name/container_id /bin/bash
```



删除容器和镜像

想要停止容器

```shell
docker ps
docker stop container_name/container_id
```

删除容器

```shell
docker rm container_name/container_id
```

删除镜像

```shell
docker rmi image_name
```

[docker使用腾讯云镜像](https://www.jianshu.com/p/3abaed03a63b)

## Repository(仓库)

仓库是集中存放镜像文件的场所。

## Dockerfile

可以轻松定义镜像内容。

我们从上图中可以看到，Dockerfile 可以自定义镜像，通过 Docker 命令去运行镜像，从而达到启动容器的目的。Dockerfile 是由一行行命令语句组成，并且支持已 # 开头的注释行。

一般来说，我们可以将 Dockerfile 分为四个部分：

- 基础镜像（父镜像）信息指令 FROM。
- 维护者信息指令 MAINTAINER。
- 镜像操作指令 RUN 、EVN 、ADD 和 WORKDIR 等。
- 容器启动指令 CMD 、ENTRYPOINT 和 USER 等。


下面是一段简单的 Dockerfile 的例子：

```dockerfile
FROM python:2.7
MAINTAINER Angel_Kitty <angelkitty6698@gmail.com>COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000ENTRYPOINT ["python"]CMD ["app.py"]
```

我们可以分析一下上面这个过程：

- 从 Docker Hub 上 Pull 下 Python 2.7 的基础镜像。
- 显示维护者的信息。
- Copy 当前目录到容器中的 /App 目录下 复制本地主机的 <src> ( Dockerfile 所在目录的相对路径)到容器里 <dest>。
- 指定工作路径为 /App。
- 安装依赖包。
- 暴露 5000 端口。
- 启动 App。


这个例子是启动一个 Python Flask App 的 Dockerfile（Flask 是 Python 的一个轻量的 Web 框架），相信大家从这个例子中能够稍微理解了 Dockfile 的组成以及指令的编写过程。

### Dockerfile 常用的指令

根据上面的例子，我们已经差不多知道了 Dockerfile 的组成以及指令的编写过程，我们再来理解一下这些常用命令就会得心应手了。

由于 Dockerfile 中所有的命令都是以下格式：INSTRUCTION argument ，指令（INSTRUCTION）不分大小写，但是推荐大写和 SQL 语句是不是很相似呢？下面我们正式来讲解一下这些指令集吧。

#### FROM

FROM 是用于指定基础的 images ，一般格式为 FROM <image> or FORM <image>:<tag>。

所有的 Dockerfile 都应该以 FROM 开头，FROM 命令指明 Dockerfile 所创建的镜像文件以什么镜像为基础，FROM 以后的所有指令都会在 FROM 的基础上进行创建镜像。

可以在同一个 Dockerfile 中多次使用 FROM 命令用于创建多个镜像。比如我们要指定 Python 2.7 的基础镜像，我们可以像如下写法一样：

```
FROM python:2.7
```



#### MAINTAINER

MAINTAINER 是用于指定镜像创建者和联系方式，一般格式为 MAINTAINER <name>。

这里我设置成我的 ID 和邮箱：

```
MAINTAINER Angel_Kitty <angelkitty6698@gmail.com>
```



#### COPY

COPY 是用于复制本地主机的 <src> (为 Dockerfile 所在目录的相对路径)到容器中的 <dest>。

当使用本地目录为源目录时，推荐使用 COPY 。一般格式为 COPY <src><dest> 。

例如我们要拷贝当前目录到容器中的 /app 目录下，我们可以这样操作：

```
COPY . /app
```



#### WORKDIR

WORKDIR 用于配合 RUN，CMD，ENTRYPOINT 命令设置当前工作路径。

可以设置多次，如果是相对路径，则相对前一个 WORKDIR 命令。默认路径为/。一般格式为 WORKDIR /path/to/work/dir。

例如我们设置 /app 路径，我们可以进行如下操作：

```
WORKDIR /app
```



#### RUN

RUN 用于容器内部执行命令。每个 RUN 命令相当于在原有的镜像基础上添加了一个改动层，原有的镜像不会有变化。一般格式为 RUN <command>。

例如我们要安装 Python 依赖包，我们做法如下：

```
RUN pip install -r requirements.txt
```



#### EXPOSE

EXPOSE 命令用来指定对外开放的端口。一般格式为 EXPOSE <port> [<port>...]。

例如上面那个例子，开放5000端口：

```
EXPOSE 5000
```



#### ENTRYPOINT

ENTRYPOINT 可以让你的容器表现得像一个可执行程序一样。一个 Dockerfile 中只能有一个 ENTRYPOINT，如果有多个，则最后一个生效。

ENTRYPOINT 命令也有两种格式：

- ENTRYPOINT ["executable", "param1", "param2"] ：推荐使用的 Exec 形式。
- ENTRYPOINT command param1 param2 ：Shell 形式。


例如下面这个，我们要将 Python 镜像变成可执行的程序，我们可以这样去做：

```
ENTRYPOINT ["python"]
```



#### CMD

CMD 命令用于启动容器时默认执行的命令，CMD 命令可以包含可执行文件，也可以不包含可执行文件。

不包含可执行文件的情况下就要用 ENTRYPOINT 指定一个，然后 CMD 命令的参数就会作为 ENTRYPOINT 的参数。

CMD 命令有三种格式：

- CMD ["executable","param1","param2"]：推荐使用的 exec 形式。
- CMD ["param1","param2"]：无可执行程序形式。
- CMD command param1 param2：Shell 形式。


一个 Dockerfile 中只能有一个 CMD，如果有多个，则最后一个生效。而 CMD 的 Shell 形式默认调用 /bin/sh -c 执行命令。

CMD 命令会被 Docker 命令行传入的参数覆盖：docker run busybox /bin/echo Hello Docker 会把 CMD 里的命令覆盖。

例如我们要启动 /app ，我们可以用如下命令实现：

```
CMD ["app.py"]
```


 当然还有一些其他的命令，我们在用到的时候再去一一讲解一下。

### 构建 Dockerfile

我们大体已经把 Dockerfile 的写法讲述完毕，我们可以自己动手写一个例子：

```
mkdir static_web
cd static_web
touch Dockerfile
```


 然后 vi Dockerfile  开始编辑该文件，输入 i 开始编辑。以下是我们构建的 Dockerfile 内容：

```
FROM nginx
MAINTAINER Angel_Kitty <angelkitty6698@gmail.com>
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```


 编辑完后按 esc 退出编辑，然后  ：wq写入，退出。

我们在 Dockerfile 文件所在目录执行：

```
docker build -t angelkitty/nginx_web:v1 .
```


 我们解释一下：

- -t 是为新镜像设置仓库和名称
- angelkitty 为仓库名
- nginx_web 为镜像名
- ：v1 为标签（不添加为默认 latest ）


我们构建完成之后，使用 Docker Images 命令查看所有镜像，如果存在 REPOSITORY 为 Nginx 和 TAG 是 v1 的信息，就表示构建成功。


 接下来使用 docker run 命令来启动容器：

```
docker run --name nginx_web -d -p 8080:80   angelkitty/nginx_web:v1
```


 这条命令会用 Nginx 镜像启动一个容器，命名为 nginx_web ，并且映射了 8080 端口。

这样我们可以用浏览器去访问这个 Nginx 服务器：http://localhost:8080/ 或者 http://本机的 IP 地址：8080/，页面返回信息：

http://119.45.58.134:8080/