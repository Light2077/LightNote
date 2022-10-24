期望实现的功能

在某个文件路径下用windows命令行中输入`tree`就可以列出这个文件夹的目录树。

我想到的实现方案：

- 用python的os模块变量文件目录，然后print出目录树。

但是要怎么注册成windows命令呢？

而且windows命令已经有一个`tree`命令了，我得重新起一个名称，就叫`mytree`好了。

## 探索过程

### 一个差强人意的解决方案

通过百度，发现可以自己编写一个`.bat`文件，然后通过加入环境变量的方式来执行这个`bat`文件，但是这种形式达不到我的预期。

原因1：执行命令的方式是`xxxx.bat`，我不希望还要输入后缀名

原因2：显示效果不理想，比如

创建一个`demo.bat`文件填入以下内容

```
python --version
```

执行这个`demo.bat`

```
C:\tools>python --version
Python 3.9.7
```

可见它额外显示了一行`python --version`的命令，而我想要的是直接输出结果就行，不要模拟命令行输入语句了。

因此还是需要继续探索。

### linux中的自定义命令

但是我百度了诸如**windows自定义命令**，**windows 自定义 cmd命令**等，没有找到合适的结果。

然后我转换了下思路，搜索**Linux自定义命令**

这次找到一个可行方案：

首先修改`.bashrc`文件，在任意位置加入

```bash
alias pyv='python --version'
```

然后重新加载一下

```
source .bashrc
```

这样直接输入`pyv`就能得到想要的结果

```
>>> pyv
Python 3.9.5
```

### window alias

我发现这个功能主要是通过alias实现的，然后我开始搜索**windows alias**，~~发现操作步骤有点繁琐，遂放弃这一方案。~~

是一些文章写的太复杂了，这篇文章就写的很好：

[windows自定义快捷命令](https://blog.csdn.net/lyfwfm/article/details/114989610)

步骤如下：

**1.关闭所有cmd窗口**

**2.创建别名文件**

创建文件`c:\tools\cmd-alias.bat`，内容如下

```
@echo on
doskey pyv=python --version
doskey hw=echo HelloWorld
```

路径随意，我这里创建了名为`tools`的文件夹。

**3.编辑注册表**

win + r，输入regedit打开注册表编辑器

找到`HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor`

右键新建字符串值，名为AutoRun，值为之前的文件所在路径`c:\tools\cmd-alias.bat`

**4.验证**

命令行输入`pyv`，`hw`试试看能否成功。

**5.其他用法**

可以参考[windows使用alias，高效办公指南！](http://www.360doc.com/content/22/0906/12/77509131_1046756787.shtml)

比如多条命令可以用`$T`连接

```
# 命令1：cd到某个文件夹目录
# 命令2：查看当前目录下所有的文件
# 命令3：在文件管理器中打开
doskey feo=cd C:\Users\xingag\Desktop\fe $T dir $T explorer $* 
```

### mytree

终于开始编写代码了

首先，创建一个这样的文件目录用来测试，文件都是空文件。

```
|- demo
  |- images
    |- 1.png
    |- 2.png
  |- work
    |- week
      |- day
        |- 1.txt
        |- 2.txt
      |- 1.txt
  |- readme.md
```

编写代码

```python
import os
import argparse
parser = argparse.ArgumentParser()
# parser.add_argument("max_deepth", help="enter max_deepth", type=int, default=1)
parser.add_argument("max_deepth", type=int, nargs='?')
args = parser.parse_args()
if args.max_deepth is None:
    args.max_deepth = 1
    
base_path = os.getcwd()
text = ''

paths = [(base_path, 0)]
while paths:
    path, deepth = paths.pop()
    n = os.path.split(path)[-1]
    spaces = ' ' * (deepth+1) * 2
    text += f'{spaces}|- {n}\n'

    dirs = []
    files = []
    if os.path.isdir(path):
        for name in os.listdir(path):
            p = os.path.join(path, name)
            if os.path.isdir(p):
                dirs.append(p)
            else:
                files.append(p)
    dirs.sort(reverse=True)
    files.sort(reverse=True)
    for p in files:
        if deepth >= args.max_deepth:
            continue
        paths.append((p, deepth+1))


    for p in dirs:
        if deepth >= args.max_deepth:
            continue
        paths.append((p, deepth+1))

print(text)
```



在cmd-alias.bat中

```bash
@echo off
doskey mytree=python C:\tools\demo.py $*
```

进入demo文件夹，输入`mytree`默认显示文件目录下的文件。

```
mytree
```

```
  |- demo
    |- images
    |- work
    |- readme.md
```

指定最大深度

```
mytree 3
```

```
  |- demo
    |- images
      |- 1.png
      |- 2.png
    |- work
      |- week
        |- day
        |- 1.txt
    |- readme.md
```

