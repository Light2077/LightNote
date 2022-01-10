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

