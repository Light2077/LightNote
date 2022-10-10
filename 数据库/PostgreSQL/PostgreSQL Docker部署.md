## Docker安装postgres

```
docker pull postgres
```

启动镜像

```
docker run --name postgres -e POSTGRES_PASSWORD=123456 -p 5432:5432 -d postgres
```



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

切换到用户postgres

> postgres镜像默认的用户名为postgres。不切换的话无法打开postgresql

```
su postgres
```

进入postgre

```
psql
```

也可以这样进入

```
psql -U postgres
```



退出postgre

```
\q
```



