## 修改默认启动路径

windows环境下修改jupyter notebook默认启动路径

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

## jupyter打开其他conda环境

1.先激活你要添加的python环境

```
conda activate tf2
```

2.安装ipykernel

```
pip install ipykernel
```

3.添加环境

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

plt.rcParams['font.family'] = "SimHei"   # 中文字体
plt.rcParams['axes.unicode_minus'] = False  # 保证绘图时负号显示不出错
pd.set_option('display.max_columns', 200)  # pandas 最多显示200行
pd.set_option('display.float_format', '{:,.4f}'.format)  # pandas浮点数格式：保留4位小数
# 以上为固定操作，以下添加额外需要的包
```

