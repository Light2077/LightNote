# pip手册

https://pip.pypa.io/en/stable/cli/pip_download/



## 换源

比如需要在一台新虚拟机部署环境，若该虚拟机可以联网，则更换默认的pip源，加快下载包的速度。

https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

### 临时使用

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

### 设为默认

```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 配置多个镜像源

如果您想配置多个镜像源平衡负载，可在已经替换 `index-url` 的情况下通过以下方式继续增加源站：

```
pip config set global.extra-index-url "<url1> <url2>..."
```

请自行替换引号内的内容，源地址之间需要有空格

可用的 `pypi` 源列表（校园网联合镜像站）：https://mirrors.cernet.edu.cn/list/pypi

### 文件位置

` C:\Users\<username>\AppData\Roaming\pip\pip.ini `



## 更新pip

```
python -m pip install --upgrade pip
# 如果速度较慢，使用
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
```



## 更新包

```
pip install numpy -U
```

## 离线下载安装包

### 离线下载

下载单个包。

```
pip download -d <offline_pkg> <pkg_name>
```

例：将tqdm包下载到当前目录下的pkgs文件夹，会自动下载tqdm的依赖库

```
pip download -d ./pkgs tqdm
```



下载多个包

```
pip download -d <pkgs_dir> -r requirements.txt
```

例：将`requirements.txt`内包含的包都下载到当前目录下的pkgs文件夹内

`requirements.txt`文件内容

```
colorama==0.4.4
tqdm==4.63.0
numpy==1.22.3
```

命令行语句

```
pip download -d ./pkgs -r requirements.txt
```



### 离线安装

批量离线安装包：https://www.cnblogs.com/JonaLin/p/12161557.html

安装单个离线包

```
pip install --no-index --find-links=<pkgs_dir>/<pkg_name>
```

安装多个离线包

```
pip install --no-index --find-links=<pkgs_dir>/ -r requirements.txt
```

### 下载特定python版本的包

使用参数`--python-version`

```
pip download -d ./pkgs psycopg2-binary --python-version 3.6 --no-deps
```

必须要加`--no-deps`否则会报错

```
ERROR: When restricting platform and interpreter constraints using --python-version, --platform, --abi, or --implementation, either --no-deps must be set, or --only-binary=:all: must be set and --no-binary must not be set (or must be set to :none:).
```





## 下载特定平台的包

场景：

linux服务器没有互联网，需要从本地下载对应平台的python包再传到服务器上安装

例

```
pip download --only-binary=:all: --platform linux_x86_64 numpy
```

下载到指定路径

```
pip download -d "./pkgs" <some_package>
```

结合

```
pip download -d "./pkgs" --no-deps --platform linux_x86_64 numpy
```

如果`--platform`不行

尝试不用这个参数，或者换成

```
manylinux2014_x86_64
```



### 完整案例

下载linux环境下的`numpy`包到当前目录下的`pkgs`文件内。

```
pip download --only-binary=:all: --platform linux_x86_64 -d ./pkgs numpy
```

这里遇到2个问题

首先是会报错

```
ERROR: Could not find a version that satisfies the requirement numpy (from versions: none)
ERROR: No matching distribution found for numpy
```

说是找不到满足条件的包，查看numpy的[release](https://github.com/numpy/numpy/releases)

```
...
numpy-1.22.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
...
```

得知，`--platform`参数需要修改为`manylinux2014_x86_64`

修改后输入下面的语句

```
pip download --only-binary=:all: --platform manylinux2014_x86_64 -d ./pkgs numpy
```

下载成功！得到了下面这个包，经过测试，这个包和我在linux服务器上直接pip下载得到的包完全一致。

```
numpy-1.22.3-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

下载其他包也同理



参考下面这篇文章后

https://imshuai.com/python-pip-install-package-offline-tensorflow

得知，最好的解决方法还是pyenv + docker来下载包，然后拷贝到离线环境中去。



## requirements的导出和使用

导出requirements文件

```
pip freeze > requirements.txt
```

依照requirements安装包

```
pip install -r requirements.txt 
```



## pip查看某个包的依赖包

