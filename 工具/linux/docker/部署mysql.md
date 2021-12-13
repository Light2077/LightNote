# 部署MySQL

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



