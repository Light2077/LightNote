### 查看可用版本

```
docker search python
```

### 基于镜像启动容器

```
docker run -it --name my-container centos:7 /bin/bash
```

这个命令表示在一个新的 Docker 容器中启动一个交互式的 Bash shell。

具体来说，它的含义如下：

- `docker run` 命令用于启动一个新的容器。
- `-it` 选项表示创建一个交互式的终端，并将其绑定到容器的标准输入（stdin）和标准输出（stdout）上。这样，你就可以在容器内部运行命令，并查看命令的输出结果。
- `--name`，给容器命名
- `centos:7` 表示使用 CentOS 7 镜像创建容器。如果在本地不存在该镜像，则 Docker 会自动从 Docker Hub 上下载该镜像。
- `/bin/bash` 表示在容器内部运行的命令。在本例中，我们使用 Bash shell。因此，当你运行该命令后，Docker 将会在一个新的 CentOS 7 容器中启动一个交互式的 Bash shell，并将其绑定到当前的终端上。

#### 设置IP映射

如果要映射IP就不能使用`-it`选项了

格式：`<宿主机IP>:<容器IP>`

```
docker run -p 8080:80 <image_name>
```

映射多个IP

```
docker run -p 192.168.1.100:8080:80 -p 192.168.1.101:8080:80 <image_name>
```

#### 设置路径挂载

```
docker run -v /host/dir:/container/dir <image_name>
```



### 查看运行中的容器

```
docker ps
```

### 查看所有容器

```
docker ps -a
```

### 进入某个运行中的容器

```
docker exec -it my_container /bin/bash
```



### 停用全部运行中的容器

```
docker stop $(docker ps -aq)

```

### 删除全部容器

```
docker rm $(docker ps -aq)
```

### 容器打包为镜像

`docker commit` 命令用于将一个正在运行的 Docker 容器打包成一个新的镜像。它的基本语法如下：

```
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
```

案例

```
docker commit -a "Lyra" -m "注释信息" ec6fea995006 registry.xxxx
```

- `-a` 或 `--author`：用于指定镜像的作者信息。
- `-m` 或 `--message`：用于添加一条注释信息。
- `CONTAINER` 表示容器的 ID 或名称，它用于指定要打包成镜像的容器。案例中的`CONTAINER` 是 `ec6fea995006`
- `REPOSITORY` 和 `TAG` 表示新镜像的名称和标签。例如 `my-repo/my-image:1.0` 表示该镜像的名称为 `my-repo/my-image`，标签为 `1.0`。如果不指定标签，则默认为 `latest`。

简化版

```
docker commit my_container my_image
```

### 启动容器

`docker start 5f578ea1a027 `

### 进入容器

`docker attach 5f578ea1a027 `



### 推送镜像

以[阿里云](https://cr.console.aliyun.com/)为例:

先登录

`docker login --username=light2077 registry.cn-shenzhen.aliyuncs.com`

`docker push registry.cn-shenzhen.aliyuncs.com/light2077/covid19sim:xx` xx填版本号

从本机传输文件到容器：

把当前目录下的run.sh拷贝到容器的根目录下：`docker cp run.sh 5f578ea1a027:/`

利用docker构建image

## docker run的参数

-v 挂载位置 `<宿主机目录>:<容器目录>`