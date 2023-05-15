

# Anaconda

- 更新Anaconda：`conda update conda`

- 更新所有包：`codna update --all`

- 创建新环境：`conda create -n tf2 python=3.7`

- 加速包的下载安装：[清华镜像站使用](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)



列出环境

```
conda env list
```

创建环境

```
conda create --name tf2.1 python==3.7
```

删除环境

 ```
conda env remove -n [env-name]
 ```



https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

pip临时换源

```
pip install -i https://pypi.douban.com/simple
```



pip永久换源

```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```



## TensorFlow 2.4

https://tf.wiki/

## 使用代理时报错

在创建新的环境时，如果开着代理，会报错。

```
conda create -n streamlit python=3.9
```

```
Collecting package metadata (current_repodata.json): failed

ProxyError: Conda cannot proceed due to an error in your proxy configuration.
Check for typos and other configuration errors in any '.netrc' file in your home directory,
any environment variables ending in '_PROXY', and any other system-wide proxy
configuration settings.
```

可以修改`.condarc`来设置不使用任何代理。

```
proxy_servers:
  http:
  https:
```

一般在`C:\Users\<username>\.condarc`