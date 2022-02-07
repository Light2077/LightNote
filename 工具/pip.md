# Pip常用操作

## 换源

https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

临时使用

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

设为默认

```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```



## 更新包

```
pip install numpy -U
```

## requirements

导出requirements文件

```
pip freeze > requirements.txt
```

依照requirements安装包

```
pip install -r requirements.txt 
```

