https://hub.docker.com/_/python

有许多安装版本

比如

```
docker pull python:3.8.12-slim
```

目前还不清楚slim, slim-bullseys, slim-buster, buster的区别

进入python

```
docker run -it python:3.8.12-slim /bin/bash
```

