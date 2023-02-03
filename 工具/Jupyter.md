## 修改默认启动路径

windows环境下修改jupyter notebook默认启动路径

首先要生成jupyter的配置文件

```
jupyter notebook --generate-config
```

弹出如下提示

```
Overwrite C:\Users\light\.jupyter\jupyter_notebook_config.py with default config? [y/N]y
```

根据路径找到jupyter目录，编辑jupyter_notebook_config.py 

用ctrl + F 搜索

```
c.NotebookApp.notebook_dir =
```

改成自己需要的目录，比如

```
c.NotebookApp.notebook_dir = "D:/notebooks"
```

找到jupyter notebook快捷方式

修改“目标“这一栏

> 注意这里一共有5个路径，分别是：
>
> - python路径
> - cwp.py 路径
> - anaconda 目录
> - python路径（同第一个）
> - jupyter-notebook-scripy.py 路径

```
D:\software\Anaconda\python.exe D:\software\Anaconda\cwp.py D:\software\Anaconda\ D:\software\Anaconda\python.exe D:\software\Anaconda\Scripts\jupyter-notebook-script.py
```

> 有时候修改可能会失效，这时需要右键jupyter notebook的快捷方式->属性，把路径中的`"%USERPROFILE"`删掉。



## jupyter打开其他conda环境

1.先激活你要添加的python环境

```
conda activate tf2
```

2.安装ipykernel

```
pip install ipykernel
```

3.添加环境（要在新环境下，**不要**在base环境执行）

```
python -m ipykernel install --user --name tf2
```

1. 显示现有的所有的虚拟内核名：`jupyter kernelspec list`
2. 卸载指定虚拟内核：`jupyter kernelspec uninstall [虚拟内核名]`

**问题**

tensorflow2在notebook中无法使用gpu，而在命令行环境中可用。

猜测解决方案：在base环境下安装cuda

## jupyter打开其他conda环境2

https://segmentfault.com/a/1190000023346483

在base环境下

```
conda install nb_conda_kernels
```

切换到新添加的环境

```
conda activate tf2
```

在要添加的环境下

```
pip install ipykernel
```

查看kernel

```
python -m nb_conda_kernels list
```

https://www.markroepke.me/posts/2019/06/05/tips-for-slideshows-in-jupyter.html

## 自动重新加载包

```python
%load_ext autoreload
%autoreload 2

# 环境变量加入项目根目录（可以导入自定义的包）
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
```

## 导包固定操作

```python
%load_ext autoreload
%autoreload 2

import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 中文字体
plt.rcParams['font.family'] = "SimHei"
# 保证绘图时负号显示不出错
plt.rcParams['axes.unicode_minus'] = False
# pandas 最多显示200行
pd.set_option('display.max_columns', 200)
# pandas浮点数格式：保留4位小数
pd.set_option('display.float_format', '{:,.4f}'.format)

# 以上为固定操作，以下添加额外需要的包
```

## jupyter文件格式转换

https://blog.csdn.net/qq_36178962/article/details/115870759

https://nbconvert.readthedocs.io/en/latest/index.html

### 批量将ipynb转换为md

在一个文件夹下按照如下目录创建3个ipynb文件。notebook里的内容不关键

```
|-demo1.ipynb
|-demo2.ipynb
|-demo
  |-demo3.ipynb
```

创建一个mycfg.py文件，填写如下内容

```python
c = get_config()
c.NbConvertApp.notebooks = [
	"demo1.ipynb", 
	"demo2.ipynb", 
	'./demo/demo3.ipynb'
]
```

在该文件夹下的目录启动命令行窗口，输入

```
jupyter nbconvert --config mycfg.py --to markdown
```

如果在notebook里用matplotlib绘制了图片，导出markdown后会自动把图片保存到一个文件夹里。

假设demo1.ipynb生成了一张图片，导出的文件为：

```
|-demo1.md
|-demo1 files
  |- xxx.png
```

注意：demo1.ipynb插入的图片并不会跟着一起被导出。

> 后续操作：
>
> - 移动生成的文件夹里的图片到指定目录，删除该文件夹
> - 移动markdown文件到指定目录
> - 修改所有markdown文件里图片的路径。



## 服务器部署Jupyter Lab

https://blog.csdn.net/weixin_42225122/article/details/113866096

https://jupyter.org/

```
conda install -c conda-forge jupyterlab=3
```

开始准备部署

https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html

首先需要查看是否有`jupyter_server_config.py`文件

> - Windows: `C:\Users\USERNAME\.jupyter\jupyter_server_config.py`
> - OS X: `/Users/USERNAME/.jupyter/jupyter_server_config.py`
> - Linux: `/home/USERNAME/.jupyter/jupyter_server_config.py`

如果没有，输入以下代码生成`jupyter_server_config.py`文件

```
jupyter server --generate-config
```



生成密码

```
jupyter server password
```

在下面弹出的信息中输入密码

```
Enter password: 
Verify password: 
[JupyterPasswordApp] Wrote hashed password to /root/.jupyter/jupyter_server_config.json
```



修改`jupyter_server_config.py`的几个配置项

```
c.ServerApp.ip = '*'  # 使其他网络可以访问
c.ServerApp.open_browser = False
c.ServerApp.port = 9999  # 访问的端口
c.ServerApp.root_dir = "xx/xx"  # 默认启动路径
```

> 注意
>
> 这个配置方案是十分简化的方案，完全没有考虑网络安全性

## Jupyter Lab 字体设置

Settings > Advanced Settings Editor

修改右侧的User Preferences

```python
{
    "codeCellConfig": {
        "fontFamily": "Fira Code",
    }
}
```

## magic方法

使用`%lsmagic`可以查看所有magic方法

```
%lsmagic
```

```
|-root
  |-line
  |-cell
```

## Jupyter Lab显示代码运行时间

```
pip install jupyterlab_execute_time
```

## 复制Jupyter Lab里的图片

https://stackoverflow.com/questions/52062493/copy-matlibplot-plot-image-from-jupyter-lab
