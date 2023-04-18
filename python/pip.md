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

设置为腾讯源

查看pip config 配置位置，一般在`~/.pip/pip.conf`

```
pip config set global.index-url http://mirrors.tencentyun.com/pypi/simple
pip config set global.trusted-host mirrors.tencentyun.com
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



## chatgpt教你迁移环境

在这种情况下，尝试使用`pip`的`wheel`功能在源服务器上创建二进制分发包，然后将这些包复制到目标服务器上。请按照以下步骤操作：

在源服务器上，确保已安装`wheel`库：

```
pip install wheel
```

激活源服务器上的虚拟环境并导出`requirements.txt`文件：

```bash
source demo_env/bin/activate
pip freeze > requirements.txt
```

在源服务器上，为`requirements.txt`中列出的所有包创建`wheel`文件：

```bash
pip wheel --wheel-dir wheelhouse -r requirements.txt
```

这将在`wheelhouse`目录中为每个包创建一个`.whl`文件。

将`wheelhouse`目录和`requirements.txt`文件复制到目标服务器。

在目标服务器上，创建一个新的虚拟环境并激活它：

```bash
python3.9 -m venv demo_env
source demo_env/bin/activate
```

使用`requirements.txt`文件和`wheelhouse`目录在目标服务器上的新虚拟环境中离线安装包：

```bash
pip install --no-index --find-links=wheelhouse -r requirements.txt
```

这将从`wheelhouse`目录中的`.whl`文件安装所需的包，而不会尝试从互联网上下载任何内容。这样，您可以在无法访问互联网的目标服务器上设置虚拟环境。



> ​	按照上面的方法迁移时报了错

```
ERROR: cryptography-39.0.2-cp36-abi3-manylinux_2_24_x86_64.whl is not a supported wheel on this platform.
```

在源服务器上创建的`.whl`文件不兼容目标服务器的平台。这可能是因为源服务器和目标服务器之间的Python版本、操作系统或体系结构不同。

在这种情况下，我建议您在目标服务器上尝试从源代码构建包。为此，您可以遵循以下步骤：

在源服务器上，获取`requirements.txt`中列出的所有包的源代码。您可以使用`pip download`命令将源代码包下载到一个目录中：

```bash
pip download --no-binary=:all: --dest packages -r requirements.txt
```

这将下载源代码包（通常是`.tar.gz`格式）到名为`packages`的目录。

将`packages`目录和`requirements.txt`文件复制到目标服务器。

在目标服务器上，创建一个新的虚拟环境并激活它（如果尚未创建）：

```bash
python3.9 -m venv demo_env
source demo_env/bin/activate
```

在目标服务器上的新虚拟环境中离线安装包：

```bash
pip install --no-index --find-links=packages -r requirements.txt
```

这将从`packages`目录中的源代码包安装所需的包，而不会尝试从互联网上下载任何内容。如果目标服务器上有必要的编译工具和库，这应该可以解决兼容性问题。

## 用docker帮助环境迁移

原因：

- 内网无法用pip联网安装包，需要下载好whl文件
- 在ubuntu系统下载的whl文件，可能无法在centos中顺利安装。

这时候需要找一台联网的服务器，安装docker，配一个centos的环境

首先查看目标服务器的具体版本

centos服务器

```
cat /etc/centos-release
```

```
CentOS Linux release 7.9.2009 (Core)
```

ubuntu服务器

```
lsb_release -a
```

```
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.4 LTS
Release:        18.04
Codename:       bionic
```



安装docker

```
sudo apt-get update
sudo apt-get install docker.io
```

下载并启动 CentOS Docker 镜像

```
sudo docker run -it centos:7 /bin/bash
# 具体设定版本
sudo docker run -it centos:7.9.2009 /bin/bash
```

启动并进入镜像

```
sudo docker run -it centos:7.9.2009 /bin/bash
```

更新系统软件包

```shell
yum update -y
```

安装编译工具

```
yum install -y make
```

安装sqlite

```
yum install sqlite-devel
```



安装 Python 3.9

在容器中运行以下命令

> https://registry.npmmirror.com/-/binary/python/3.9.6/Python-3.9.6.tgz

```shell
yum install -y gcc openssl-devel bzip2-devel libffi-devel
yum install -y wget
# wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz
wget https://registry.npmmirror.com/-/binary/python/3.9.6/Python-3.9.6.tgz
tar xzf Python-3.9.6.tgz
cd Python-3.9.6
./configure --enable-optimizations
make altinstall

```

验证是否安装成功

```
python3.9
pip3.9
```

映射到python3和pip3

```
ln -s /usr/local/bin/python3.9 /usr/local/bin/python3
ln -s /usr/local/bin/pip3.9 /usr/local/bin/pip3
```

有时候，需要重新编译安装python，比如sqlite版本不够，不能运行某些项目，需要升级，升级sqlite后就得重新编译安装python

```
cd /home/projects/python/Python-3.9.6
make clean
./configure --enable-optimizations --with-openssl=/usr/local/openssl --with-system-ffi --enable-loadable-sqlite-extensions
make
make altinstall
```



将容器打包为一个镜像

```
docker ps
```

```
CONTAINER ID   IMAGE             COMMAND       CREATED       STATUS       PORTS     NAMES
77ed7cc020f7   centos:7.9.2009   "/bin/bash"   2 hours ago   Up 2 hours             wonderful_liskov
```

打包

```
docker commit wonderful_liskov centos7.9_python3.9
```

然后启动这个打包好的镜像

如果要配置端口映射

```
docker run -d -p 8080:8080 --name mycentos centos7.9_python3.9 /bin/bash
docker exec -it [容器名或id] /bin/bash
```

不配置

```
docker run -it --name mycentos centos7.9_python3.9 /bin/bash
```

创建并进入文件夹

```
mkdir -p /home/projects/example
cd /home/projects/example
```

创建并启动虚拟环境

```
python3 -m venv venv
source venv/bin/activate
```

配置好需要的虚拟环境后



在源服务器上，确保已安装`wheel`库：

```
pip install wheel
```

激活源服务器上的虚拟环境并导出`requirements.txt`文件：

```
source demo_env/bin/activate
pip freeze > requirements.txt
```

在源服务器上，为`requirements.txt`中列出的所有包创建`wheel`文件：

```
pip wheel --wheel-dir wheelhouse -r requirements.txt
```

这将在`wheelhouse`目录中为每个包创建一个`.whl`文件。

打包

```
tar czvf package.tar.gz wheelhouse/ requirements.txt
```

将文件拷贝出来解压到目标服务器。

> 如果用的是docker

```
docker cp <容器名或容器 ID>:/home/package.tar.gz /home/local/

```



将`wheelhouse`目录和`requirements.txt`文件复制到





在目标服务器上，创建一个新的虚拟环境并激活它：

```
python3.9 -m venv demo_env
source demo_env/bin/activate
```

使用`requirements.txt`文件和`wheelhouse`目录在目标服务器上的新虚拟环境中离线安装包：

```
pip install --no-index --find-links=wheelhouse -r requirements.txt
```

这将从`wheelhouse`目录中的`.whl`文件安装所需的包，而不会尝试从互联网上下载任何内容。这样，您可以在无法访问互联网的目标服务器上设置虚拟环境。

