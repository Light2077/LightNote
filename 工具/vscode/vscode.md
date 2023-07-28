https://www.zhihu.com/question/322530705/answer/860418884

## 常用快捷键

**查看函数参数提示**：`ctrl+shift+space`

**键盘快捷方式修改**：先按`ctrl+k`再按`ctrl+s`

**选中字母切换为大写**：需要修改键盘快捷方式，搜索**转换为大写**，设置为`alt+shift+u`，同理搜索**转换为小写**设置为`alt+u`。

**标签页切换**：`alt+数字`

**上/下方另起一行**：上方`ctrl+shift+enter`，下方`ctrl+enter`



折叠/展开光标所在位置的代码块

- 折叠：`Ctrl + Shift + [`
- 展开：`Ctrl + Shift + ]`

折叠展开文件中所有代码块：

- 折叠：`Ctrl + K` + `Ctrl + 0`
- 展开：`Ctrl + K` + `Ctrl + J`

单行缩进：

- 增加缩进：`Ctrl + ]`
- 减少缩进：`Ctrl + [`



**设置python解释器**：

- 输入快捷键`ctrl + shift + P`，在界面顶端弹出**搜索窗**
- 在搜索窗中输入`>python select interpreter`，回车
- 选择自动搜索到的python解释器路径，或手动输入路径。



已经熟练：

**变量重命名**：`F2`（会自动对其他文件里引用的该变量进行重命名）

**代码跳转后回退**：`alt + ←`

打开setting的json，快捷键`ctrl + shift + P`，搜索 Open User Settings (JSON)。（直接搜 open setting，就能看到选项）

## 自定义代码片段

进入方式，在`ctrl + shift + P`中搜索Snippets: Configure User Snippets

选择python.json

下面是其中一个例子

```cs
{
    "HEADER": {
		"prefix": "header",
		"body": [
			"#!/usr/bin/env python",
			"# -*- encoding: utf-8 -*-",
			"\"\"\"",
			"@File    :   $TM_FILENAME",
			"@Time    :   $CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE:$CURRENT_SECOND",
			"@Author  :",
			"@Version :   1.0",
			"@Desc    :",
			"\"\"\"",
			"",
			"",
			"$0"
		],
	},
}
```



## 免密远程登录

本机为windows，远端为linux。希望vscode每次连接到远端时无需重新输入密码

将本机的`id_rsa.pub`文件拷贝到远端`~`目录下

写入authorized_keys

```
cat ~/id_rsa.pub >> ~/.ssh/authorized_keys
```

或者复制`id_rsa.pub`的内容，然后手动粘贴到远端的`authorized_keys`



### 编辑ssh config

在vscode界面中按快捷键：ctlr+shift+P 

然后输入

```
Remote-SSH Open SSH Configuration File...
```

不用完全输入，输一点就可以看到自动补全的结果了，然后回车进去编辑config文件

一般路径是

```
c:\users\<用户名>\.ssh\config
```

格式为

```
Host your_host_name1
    HostName 12.33.44.55
    User root

Host your_host_name2
    HostName 12.33.44.56
    User root
```

每个host就是要连接的远程服务器。

### python配置虚拟环境

ctlr+shift+P 然后输入Python: Select Interpreter，选择虚拟环境的python解释器即可

### error:试图写入的管道不存在

直接设置remote ssh 的config绝对路径即可。

ctrl+shift+P  然后输入 remote ssh config file

看起来你在使用 VSCode 的 Remote-SSH 插件连接到远程服务器时遇到了一个常见的问题。在你试图连接到的远程服务器的 SSH 密钥已经改变，这可能是由于以下几个原因：

1. 服务器的 SSH 密钥确实已经被更改了，例如重新安装了系统或者更改了 SSH 配置。
2. 你正在尝试连接到一个新的服务器，但是这个服务器使用了你之前连接过的一个服务器的 IP。
3. 确实存在中间人攻击，这是最危险的可能性，也就是有人在你的电脑和服务器之间插手，试图窃取你的信息。

在排除了第三种可能性之后，你可以按照以下步骤来解决这个问题：

1. 打开一个终端。
2. 运行命令 `ssh-keygen -R 你的服务器IP`。例如，如果你的服务器 IP 是 `81.19.62.79`，那么你就运行 `ssh-keygen -R 81.19.62.79`。
3. 这个命令会从你的 `known_hosts` 文件中移除旧的密钥。这个文件位于 `~/.ssh/known_hosts`，在 Windows 中通常在 `C:\\Users\\你的用户名\\.ssh\\known_hosts`。
4. 之后再次尝试用 VSCode 连接服务器，它会提示你添加新的密钥，你可以选择接受。

但请注意，如果你不确定是否存在中间人攻击，那么最好先联系你的系统管理员确认一下情况。如果你自己就是系统管理员，你应该确认一下服务器的 SSH 密钥是否确实已经被更改。如果没有更改，那么可能就存在安全问题。



### error:notebook画图kernel died

https://stackoverflow.com/questions/65734044/kernel-appears-to-have-died-jupyter-notebook-python-matplotlib

```
conda install --yes freetype=2.10.4
```

## python代码调试

在任意空文件夹下创建`main.py`并传以下内容

```python
def foo(a, b):
    b -= 100
    c = a + b  # break1 
    print(c)


a = 1
b = 2
for i in range(10):
    a += 1
    b *= a  # break2
    foo(a, b)
```

右键文件夹选择使用vscode打开。

- ==F5== Continue 跳转到下一个断点
- ==F10== Step Over 单步运行，如果遇到子函数
  - 子函数内无断点，将子函数当做一行，继续运行
  - 子函数内有断点，跳转到断点再单步运行。
- ==F11== Step Into 单步运行，遇到子函数，进入并从子函数第一行开始单步运行
- ==Shift + F11== Step Out 单步跳出，如果子函数内无断点，跳出子函数，若子函数有断点，执行完断点后再跳出子函数。

## 初始界面

在设置（ctrl + numpad9）中搜索 startup

将workbench: startup editor这一项设置为：`welcomPageInEmptyWorkbench`

## 代码自动格式化



[python代码格式化工具只懂autopep8？这里有更好的 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/203307235)

[psf/black: The uncompromising Python code formatter (github.com)](https://github.com/psf/black)

在setting中设置的关键词：Format
