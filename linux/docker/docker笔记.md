进入某个容器：

```
docker run -it registry.cn-shenzhen.aliyuncs.com/light2077/covid19sim:0.3 /bin/bash
```



查看运行中的容器：

```
docker ps
```



查看所有容器

```
docker ps -a
```



停用全部运行中的容器

```
docker stop $(docker ps -q)
```

删除全部容器

```
docker rm $(docker ps -aq)
```

容器更新为镜像

`docker commit -a 'light' -m 'container to image' ec6fea995006 registry.xxxx `



开始容器：

`docker start 5f578ea1a027 `

进入容器：

`docker attach 5f578ea1a027 `



推送镜像，以[阿里云](https://cr.console.aliyun.com/)为例:

先登录

`docker login --username=light2077 registry.cn-shenzhen.aliyuncs.com`

`docker push registry.cn-shenzhen.aliyuncs.com/light2077/covid19sim:xx` xx填版本号

容器拷贝东西：

把当前目录下的run.sh拷贝到容器的根目录下：`docker cp run.sh 5f578ea1a027:/`





利用docker构建image

## docker run的参数

-v 挂载位置 `<宿主机目录>:<容器目录>`