https://www.runoob.com/docker/docker-install-redis.html

docker拉取redis镜像

```
docker pull redis:latest
```

运行redis容器

```
docker run -itd --name redis-test -p 6379:6379 redis
```

测试redis-cli服务

```
docker exec -it redis-test /bin/bash
```

