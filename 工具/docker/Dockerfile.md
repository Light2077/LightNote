想改变工作路径时

```dockerfile
WORKDIR /project/web
CMD flask run
```

忽略某些文件时，创建`.dockerignore`

语法类似`.gitignore`

```
__pycache__/
.vscode/
notebooks/
```



```
# Base Images
## 从天池基础镜像构建
FROM registry.cn-shanghai.aliyuncs.com/tcc-public/python:3

## 把当前文件夹里的文件构建到镜像的根目录下
ADD . /

## 指定默认工作目录为根目录（需要把run.sh和生成的结果文件都放在该文件夹下，提交后才能运行）
WORKDIR /

## 镜像启动后统一执行 sh run.sh
CMD ["sh", "run.sh"]
```

