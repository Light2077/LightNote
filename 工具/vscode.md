https://www.zhihu.com/question/322530705/answer/860418884

## 常用快捷键

**查看函数参数提示**：`ctrl+shift+space`

**键盘快捷方式修改**：先按`ctrl+k`再按`ctrl+s`

**选中字母切换为大写**：需要修改键盘快捷方式，搜索**转换为大写**，设置为`alt+shift+u`，同理搜索**转换为小写**设置为`alt+u`。

**标签页切换**：`alt+数字`

**上/下方另起一行**：上方`ctrl+shift+enter`，下方`ctrl+enter`



**设置python解释器**：

- 输入快捷键`ctrl + shift + P`，在界面顶端弹出**搜索窗**
- 在搜索窗中输入`>python select interpreter`，回车
- 选择自动搜索到的python解释器路径，或手动输入路径。



已经熟练：

**变量重命名**：`F2`（会自动对其他文件里引用的该变量进行重命名）

**代码跳转后回退**：`alt + ←`

## 自定义代码片段



## 免密登录

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

### error:notebook画图kernel died

https://stackoverflow.com/questions/65734044/kernel-appears-to-have-died-jupyter-notebook-python-matplotlib

```
conda install --yes freetype=2.10.4
```

## python代码调试

在任意空文件夹下创建`main.py`并传入一下内容

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

