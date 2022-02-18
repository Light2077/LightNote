https://www.zhihu.com/question/322530705/answer/860418884

## 常用快捷键

变量重命名：`F2`（会自动对其他文件里引用的该变量进行重命名）

设置代码运行使用的python解释器：

- 输入快捷键`ctrl + shift + P`，在界面顶端弹出**搜索窗**
- 在搜索窗中输入`>python select interpreter`，回车
- 选择自动搜索到的python解释器路径，或手动输入路径。

代码跳转后回退：`alt + ←`



## 免密登录

本机为windows，远端为linux。希望vscode每次连接到远端时无需重新输入密码

将本机的`id_rsa.pub`文件拷贝到远端`~`目录下

写入authorized_keys

```
cat ~/id_rsa.pub >> ~/.ssh/authorized_keys
```

或者复制`id_rsa.pub`的内容，然后手动粘贴到`authorized_keys`



### 编辑ssh config

ctlr+shift+P 然后输入

```
Remote-SSH Open SSH Configuration File...
```

不用完全输入，输一点就可以看到自动补全的结果了，然后回车进去选择要编辑config文件

一般路径是

```
c:\users\<用户名>\.ssh\config
```

格式为

```
Host your_host_name1
    HostName 192.168.12.321
    User root

Host your_host_name2
    HostName 119.3.145.185
    User root
```

每个host就是要连接的远程服务器。

### python配置虚拟环境

ctlr+shift+P 然后输入Python: Select Interpreter，选择虚拟环境的python解释器即可

### 试图写入的管道不存在

直接设置remote ssh 的config绝对路径即可。

ctrl+shift+P  然后输入 remote ssh config file
