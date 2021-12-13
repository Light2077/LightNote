https://www.bilibili.com/video/bv1Az411q7BE

# 1. Linux操作系统入门

## 1.1 操作系统介绍

操作系统分类

- 桌面操作系统：windows系列，Mac系列，linux系列
- **服务器操作系统**：windows服务器系列(server 2000)，linux服务器系列(CentOS等)，Mac server
- 嵌入式操作系统：路由器
- 移动设备操作系统：塞班，安卓，ios



服务器的要求：

- 性能要强大：内存,CPU,硬盘，可以没有显示器，显卡看情况
- 要有专门的操作系统（与桌面版区别）

## 1.2 Linux入门

**下载安装**

[阿里云centos镜像](https://mirrors.aliyun.com/centos/)

`/centos/7.8.2003/isos/x86_64/`

选DVD或者LIVEGNOME(图形化界面)。注：电脑8G内存以下最好别用虚拟机。



## 1.3 SSH远程连接Linux操作系统

### 虚拟机连接

- 创建一个用户
- 虚拟机需要安装和启动SSH服务端
  - `sudo yum install ssh` 安装ssh
  - `sudo systemctl start sshd`启动ssh

云服务器不需要启动ssh，默认开启了。

windows要用ssh需要安装git这个软件。

`ssh <username>@<ip地址>`然后输入密码就可以连入本地虚拟机。

### 云服务器的连接

[我买的腾讯云服务器](https://console.cloud.tencent.com/cvm/instance)

在cmd输入这个`ssh root@119.45.58.134`，

然后输入密码:`!light2077`

如果仅在cmd下操作Linux系统，可能会不太方便，建议使用一些操作工具。

操作工具：xshell / putty / [**finalshell**](http://www.hostbuf.com)

### Linux启动流程(了解)

- 加载BIOS(basic input output system)：BIOS是系统启动时加载的第一个软件

  - 启动上电自检POST(Power-On-Self-Test)负责完成对CPU、主板、内存、软硬盘子系统、显示子系统（包括显示缓存）、串并行接口、键盘、CD-ROM光驱等的检测，主要检查硬件的好坏。
  - 对外部设备进行初始化，读取BIOS参数，并和实际的硬件进行比较，如果不符合会影响系统启动
  - 查找MBR(master boot record, 主引导分区)如果未找到，会提示找不到硬盘

- 读取主引导分区（MBR）：拷贝启动引导代码BootLoader

- 启动引导代码（bootloader）：当硬盘有多个操作系统时，可以选择进入哪个操作系统

- 加载内核，进入操作系统：运行第一个程序：`/sbin/init`

  - `/sbin/init`会读取相关的配置文件，来确定系统的运行级别

    - 0：关机
    - 1：单用户模式
    - 2：无网络支持的多用户模式
    - 3：有网络支持的多用户模式
    - 4：保留，未使用
    - 5：有网络支持，且有图形化界面的多用户模式
    - 6：重启
    - 切换运行级别：init级别

    输入`runlevel`可以查看

    输入`init 0`可以关机

  - 根据运行的级别，查找对应的脚本文件。

  - 解析用户自定义的启动脚本：`etc/rc.local`

  - 进入用户界面



## 1.4 安装软件的方式

### 软件管理相关的命令：

- debian平台(ubuntu): 
  - 安装包后缀：.deb
  - dpkg：用于安装离线安装包，不会自动安装依赖
  - apt：使用的更多，在线安装软件，而且会自动安装依赖。
- fedora平台(centos): 
  - 安装包后缀：.rpm
  - rpm：用于安装离线安装包，不会自动安装依赖
  - yum：使用的更多，在线安装软件，而且会自动安装依赖。
- windows
  - 安装包后缀：exe .msi

安装软件的方式：

- 下载离线安装包：dpkg/rpm
- 直接在线安装：apt/yum
- 把代码的源代码下载下来，然后编译安装。比如下载.tgz源代码文件。



### centos软件安装相关命令

`rpm -ivh <包名>.rpm`

`rpm -qa` 查看系统安装的所有软件

`rpm -e <包名>` 删除软件一般会失败



yum yellow dog updater 是一个在Fedora和RedHat以及Centos中的shell前段软件包管理器，基于RPM包管理器，能够从指定的服务器自动下载RPM包并且安装， 可以自动处理依赖性关系，并且一次安装所有依赖的软件包，无须繁琐地一次次下载安装。

`yum install <包名>.rpm`

`yum install python` 直接从网上自己下载，并把依赖也下载了

`yum list installed`查看安装的软件

`yum remove <包名>`会自动把依赖这个包的其他包也给删掉

`yum check-update`显示更新

`yum update <包名>`更新指定的软件

`yum info <packagename>`列出指定软件包详情

`yum search <packagename>`搜索软件包

`sudo yum ...` 表示使用管理员权限安装东西。

# 2. Linux文件管理和用户管理

## 2.1 文件系统介绍

常见文件系统：

- FAT16：MS-DOS6.X及以下版本使用，每个磁盘分区最多2G，已经被淘汰了。
- FAT32：Windows95以后的系统都支持，可以减少磁盘浪费，每个簇固定位4kb。单个文件最大不能超过4G。后缀名最多3个字符。
- NTFS：磁盘利用率更高，簇更小，可以共享资源。
- RAW：文件有问题的时候产生的文件系统
  - 没有格式化
  - 格式化中途取消
  - 硬盘坏道
  - 硬盘出现不可预知的错误
- EXT：扩展文件系统
- HFS：苹果的文件系统

## 2.2 Linux里的文件系统

linux只有一个盘符，以`/`开始，相当于树形结构的根，加粗的需要重点记忆

| 目录        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| /           | 系统根目录                                                   |
| **/bin**    | 包含了一些二进制文件，即可执行文件。我们在命令行里执行的指令等，其实都是执行这个目录里的二进制文件。 |
| /boot       | 系统启动相关时所需的文件（勿动）                             |
| /dev        | 设备文件，其中许多都是在启动时或运行时生成的。例如，如果你讲新的网络摄像头连接到机器中，会自动弹出一个新的设备条目 |
| **/etc**    | 用来存放所有的系统管理所需要的配置文件和子目录（以后会经常修改） |
| **/home**   | 用户的主目录，每一个用户都有自己的目录，所有的用户都存放在home目录下。 |
| /lib(64)    | 用来存放系统最基本的动态链接共享库，几乎所有的应用程序都需要用到这些共享库 |
| /lost+found | 这个目录一般情况下是空的，当系统非法关机后，这里会存放一些没来得及保存的文件 |
| /media      | Linux系统自动识别的一些设备，比如U盘光驱等，当识别后Linux会把识别的设备 |
| /opt        | 第三方软件可以安装到这个文件夹里                             |
| **/root**   | root用户的家目录，权限非常高的用户                           |
| /sbin       | 高级的命令，可能需要高级用户权限来执行                       |
| /usr        | 非常重要的目录，用来存放用户安装的应用程序和用户文件         |
| /mnt        | 系统提供该目录是为了让用户临时挂载别的文件系统的，我们可以将光盘挂载在/mnt/上，然后进入该目录酒而已查看光驱内容了 |
| /proc       | 虚拟目录，是系统内存的映射，可以通过直接访问这个目录来获取系统信息 |
| /run        | 是一个临时文件，存储系统启动以来的信息，系统重启时文件被删除 |
| /srv        | 存放一些服务启动之后需要提取的数据                           |
| /tmp        | 存放临时文件                                                 |
| /var        | 经常修改的数据，比如程序运行的日志文件。                     |
|             |                                                              |

- 以`.`开头的文件是隐藏文件

## 2.3 cd命令的使用



| 命令       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| `cd <dir>` | 进入某个目录                                                 |
| `cd ~`     | 进入当前用户的家目录。<br>root用户：`/root`。<br>普通用户：`/home/username` |
| `cd /`     | 进入根目录                                                   |
| `cd -`     | 跳到上一次所在的位置                                         |
| `cd ..`    | 跳到上一级                                                   |

这里创建一个新的用户，老是用root用户权限太高，可能一个失误操作系统没了。

添加新的用户`sudo useradd light -m -s /bin/bash`
设置密码：`sudo passwd light`(Q号)
设置权限？：`sudo gpasswd -a light root`

## 2.4 目录操作常见命令

`pwd`print work directory：显示当前工作路径

`cd`change directory：改变工作路径

| 符号 | 说明             |
| ---- | ---------------- |
| `.`  | 当前目录         |
| `..` | 上一级目录       |
| `~`  | 当前用户家目录   |
| `-`  | 上次切换前的目录 |
| `/`  | 根目录           |

注意事项：

- 使用cd时，后面为空，默认进入家目录。等价于`cd ~`
- 所有以`/`开头的路径都是绝对路径。
- 以`.`或`..`开头的目录都是相对目录

## 2.5 相对路径和绝对路径

相对路径：相对于当前文件夹路径

- `cd <dirname>`进入到当前文件夹的`<dirname>`文件夹
- `cd ./<dirname>`等价于`cd <dirname>`
- `cd ../<dirname>`进入到上一级文件夹里的`<dirname>`文件夹

绝对路径：

- `cd /home/<dirname>`



## 2.6 ls命令的基本使用

以`.`开头的文件就是隐藏文件

`ls <path>`列出文件和文件夹（不包含隐藏的文件和文件夹，如`.demo`）

`ls`:命令`-a`:选项，可选的 `/home/light`:参数
`ls -a`就可以显示隐藏文件。
`ls -l`:显示详细信息
`ls -lh`: 在显示详细信息的时候，文件的大小用k，m，g等格式显示。



### **使用`ls -l`的详细解释**

```
[light@VM-0-12-centos ~]$ ls -l
总用量 4
drwxrwxr-x 2 light light 4096 7月  29 23:58 testdir
-rw-rw-r-- 1 light light    0 7月  29 23:58 test.txt
```

- 第一个字母（常见的3种）

  - `d` —— 表示是个文件夹
  - `-` —— 表示是一个普通文件
  - `l` —— 表示是个链接（快捷方式）

- 剩下的9个字母：**每三个字母分为一组**

  比如`rwxrwxr-x`分为`（rwx) (rwx) (r-x)`

  分别对应：**所有者**，**所属组**，**其他权限**

  - `r` —— 拥有读权限
  - `w` —— 拥有写权限
  - `x` —— 拥有可执行权限
  - `-` —— 无权限

- 数字`2`

  - 如果是文件夹，表示这个文件夹下有几个文件。文件夹的数字至少为2。因为默认包含了`.`和`..`这两个文件夹。
  - 如果是文件，表示文件硬连接个数

- `light light`分别对应**所有者**和**所属组**

- `4096 7月  29 23:58` 表示**最后一次**修改的时间

- `testdir` 表示文件或文件名

## 2.7 别名

### 查看别名

单单输入`alias`可以查看系统默认的别名

```
[light@VM-0-12-centos testdir]$ alias
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias l.='ls -d .* --color=auto'
alias ll='ls -l --color=auto'
alias ls='ls --color=auto'
alias vi='vim'
```

比如这里预定义了`ll`

### **新建别名**

`alias lh='ls -lh'`

当输入`lh`时，效果等同于输入`ls -lh`
但在目前，重启系统以后，这个临时的别名就没了。持久化的方案之后会介绍。

## 2.8 文件的创建删除

### 创建

`mkdir <dirname>`创建单个文件夹

`mkdir -p school/class/student`递归创建多个文件夹

`touch <filename>` 创建单个文件

### 删除

`rmdir` 删除空文件夹，一般不用这个

`rm -rf <name>`递归删除文件或文件夹

`rm -rf *.txt`可以识别通配符

### 复制

`cp test.txt test2.txt`复制并改名、

### 移动

`mv test2.txt <dst>`把文件移到指定目录`<dst>`

## 2.9 文件查看

| 命令            | 说明                        |
| --------------- | --------------------------- |
| `cat test.txt`  | 从上到下查看文本信息        |
| `tac test.txt`  | 从下到上查看文本信息        |
| `head test.txt` | 查看文件前n行信息，默认10行 |
| `tail test.txt` | 查看文件后n行信息，默认10行 |
| `nl`            | 类似`cat`，但是带行号       |
| `wc`            | 统计（不常用）              |
| `more`          | 默认显示一个屏幕的文件      |
| `less`          |                             |

**more和less说明**

- `q`退出
- 回车：下一行
- 空格：下一页
- more会在查看完文件后自动退出，less不会
- less可以用上下键查看，more不能
- 经常结合管道（？）使用

## 2.10 vim的使用

### 命令模式

默认进入vim后就是这个模式

| 命令            | 说明                   |
| --------------- | ---------------------- |
| `shift + z + z` | 保存并退出             |
| `dd`            | 删除一行               |
| `ndd`           | 删除n行                |
| `u`             | 撤销                   |
| `yy`            | 复制一行               |
| `nyy`           | 复制n行                |
| `p`             | 粘贴                   |
| `G`             | 定位到最后一行         |
| `gg`            | 定位到第一行           |
| `ngg`           | 定位到第n行            |
| `x`             | 删除光标右边第一个字符 |
| `nx`            | 删除光标右边第n个字符  |
| `X`             | 删除光标左边第一个字符 |
| `nX`            | 删除光标右边第n个字符  |
| `$`             | 定位到行尾             |
| `0`或`^`        | 定位到行首             |
| `ctrl + f`      | 往下翻页               |
| `ctrl + b`      | 往上翻页               |
| `ctrl + d`      | 往下翻半页             |
| `ctrl + u`      | 往上翻半页             |
| `ctrl + r`      | 反撤销                 |

### 插入模式

在命令模式的情况下，按某个键进入插入模式

| 命令 | 说明                   |
| ---- | ---------------------- |
| `i`  | 在当前光标进入         |
| `I`  | 在第一个非空字符进入   |
| `o`  | 在下一行插入           |
| `O`  | 在上一行               |
| `s`  | 删除光标所在文件，插入 |
| `S`  | 删除整行，插入         |
| `a`  | 在光标下一个字符前插入 |
| `A`  | 在行尾插入             |

### 编辑模式

按esc返回命令模式

| 命令                   | 说明                           |
| ---------------------- | ------------------------------ |
| `:wq`                  | 保存退出                       |
| `:q!`                  | 不保存退出                     |
| `:e!`                  | 放弃之前的修改                 |
| `:set nu`              | 显示行号                       |
| `:set nonu`            | 不显示行号                     |
| `:120`                 | 跳转到第120行                  |
| `:/student`            | 搜索，按`n`搜索下一个          |
| `:w <new file name>`   | 另存为                         |
| `:set tabstop=4`       | 设置tab键缩进                  |
| `:set mouse=a`         | 打开鼠标模式                   |
| `:%s/student/学生`     | 默认一行只替换第一个匹配的内容 |
| `:%s/student/学生/g`   | 全部替换                       |
| `:m.ns/student/学生/g` | 替换第m-n行的字符串            |



`vim test.txt +20` 光标在第20行，打开
`vim test2.txt` 如果`test2.txt`不存在，则会新建

正在编辑文件时，另一个终端打开该文件。会出现交换文件比如:

`.test.py.swp`。关闭vim时，该文件自动删除



# 3. Linux文字处理和文件编辑

## 3.1 配置文件以及vim配置

### 配置文件

- `/etc/bashrc`

- `~/.bashrc`

  每次打开终端都会自动执行配置文件的代码。

可以把命令写入`/etc/bashrc`比如把`alias md='mkdir'`写入这个文件的最后一行。下次重新打开终端时，就可以用`md`来创建文件夹了。

`~/.bashrc`同理，但只对当前用户有效。

`vim ~/.bashrc`可以发现，腾讯云的配置如下：

```
# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

```

### vim配置文件

`/etc/vimrc`

`~/.vimrc`只对当前用户生效的文件，一般改这个。

最后一行加入`set nu`

## 3.2 用户管理相关命令

| 命令    | 说明                                                         |
| ------- | ------------------------------------------------------------ |
| whoami  | 查看当前用户名                                               |
| useradd | 创建用户<br />-d指定家目录（最好不用）<br />-m创建家目录,会在`/home`文件夹下创建一个和用户名相同的文件夹<br />-s指定用户登录时的shell解析脚本，一般指定`/bin/bash` |
| userdel | 删除用户，-r会删除用户家目录                                 |
| passwd  | 设定用户密码，未指定用户则修改当前用户的密码                 |
| su -    | 切换用户，一定要加上`-`否则只会切换 家目录，但是环境没有变。不指定用户时默认切换到root用户 |
| sudo    | 以root的身份执行命令                                         |
| visudo  | 专门用于编辑`/etc/sudoers`文件的命令，需要将指定用户添加进去才可以使用sudo命令，如<br />`test ALL=(ALL:ALL)ALL`<br />使用`sudo update-alternatives --config editor`可以修改系统的默认编辑器(nano) |
| groups  | 查看指定用户的组信息                                         |
| chsh    | 修改指定用户的shell解析器                                    |
| chown   | 修改文件所属用户[及用户组]                                   |
| chgrp   | 修改文件所属用户组                                           |
|         |                                                              |
|         |                                                              |

### 添加用户

`useradd alice -m -s /bin/bash`

### 切换用户

切换到指定切换，可能需要密码

`su alice`

`su -`切换到根目录

### 设置密码

`passwd alice`

### 删除用户

`userdel -r`删除用户的同时删除家目录

## 3.3 修改sudoers文件夹

只有被添加到`/etc/sudoers`文件的用户才能使用`sudo`命令

使用`visudo`修改该文件，找到下面这行，然后新加入一行。（`yy`然后`p`）第一百行

```
root ALL=(ALL:ALL)   ALL
light ALL=(ALL:ALL)   ALL
```

直接`vim /etc/visudo`似乎只拥有读的权限。

## 3.4 用户组的概念



创建一个用户时，会自动创建一个和用户同名的分组。组存在的意义是为了更方便地管理权限。

- `groups`查看当前用户所在的分组
- `groups alice`查看某个用户所在分组
- `gpasswd -a alice light`把用户alice加到组light内
- `gpasswd -d alice light`把用户alice从组light内移除

![](img/用户组.png)

在ubuntu中可以用`gpasswd -a light sudo`使得light用户也能使用`sudo`命令。

而在centos中则是`gpasswd -a light wheel`

因为在centos的sudoers文件中有一个地方是：

```
## Allows people in group wheel to run all commands
%wheel  ALL=(ALL)       ALL
```

## 3.5 用户管理相关指令

`vim /etc/passwd`查看所有用户和用户组文件

```
light:x:1000:1000::/home/light:/bin/bash
alice:x:1001:1001::/home/alice:/bin/bash
```

用户名:密码:用户ID:组id::家目录地址:用户登录的脚本（命令解释程序）

`vim /etc/shadow`可以查看密码

```
light:$1$zfi2c4fW$.cXkie1OxPUEf8KEsXSS40:18467:0:99999:7:::
alice:$1$gV2foEtM$OOTFy/2a10Ymg9DKszcqS1:18473:0:99999:7:::

```

密码：

- `*`表示账号被锁定
- `!`表示未设置密码
- `!!`表示密码已过期
- `$1$`表示用MD5加密
- `$2$`blowfish加密
- `$5$`SHA-256加密
- `$6$`SHA-512加密

18467表示距离1970年1月1日的天数

0密码不可修改的天数，如果这个数是5，就表示5天内不能修改密码

99999密码需要修改的期限，这里表示不需要修改

7表示过期了7天只能修改密码就还能再使用。



`vim /etc/group `可以查看用户和用户所属的组



## 3.6 修改文件权限

在light中执行：`sudo cp -a /home/alice/demo.txt .`

把alice用户的demo拷贝过来了，但是demo的所有者和所属组都是alice。（如果不加-a，就都是root）

所以在拷贝别人的文件后，需要修改文件的权限。

### 修改权限：chmod

- o表示其他用户：`sudo chmod o+w demo.txt`就表示给该文件的**其他用户添加写入权限**
- u表示所有者：`sudo chmod u+x demo.txt`就表示给该文件的**所有者添加可执行权限权限**
- g表示所属组：`sudo chmod g-w demo.txt`就表示给该文件的**所属组去除写入权限**
- a表示全部

### chmod的其他写法：

`sudo chmod o=rwx demo.txt`

也可以用数字来表示权限，比如：r = 4 w = 2 x = 1

`sudo chmod 777 demo.txt`权限全开放。每个数字代表一个组的权限。

文件的权限默认是664。`rw-rw-r--`

文件夹默认是775`rwxrwxr-x`

### 默认权限的查看和修改

`umask`可以查看文件（夹）的默认权限。

```
>>> umask
0002
```

对它后三位进行一个取反的操作

`000 000 010`→`111 111 101`翻译过来就是`775`

比如可以修改成`umask 0022`

`000 010 010`→`111 101 101`翻译过来就是`755`

### 修改文件所有者和所属组

`sudo chgrp light demo.txt`把这个文件的所属组改成light组。

`sudo chown light demo.txt`把这个文件的所有者改成用户light的。

`sudo chown light:light demo.txt`把这个文件的所有者和所属组都改成用户light的。

## 3.7 压缩和解压

### zip压缩

`zip text.zip *.txt`把所有的txt文件都压缩进来

`zip text.zip demo `把demo文件夹的文件压缩进text.zip

`unzip text.zip`

```
-d 解压到指定目录
-q 执行时不显示消息
```



### gzip压缩

`gzip test.txt`会把原来的文件替换成`test.txt.gz`

`gunzip test.txt.gz`

`gzip -k test.txt`可以保留源文件。

`gzip -r demo`会把文件夹里的每个文件压缩成gz

`gunzip -r demo`把文件夹的gz文件全部解压

### bzip2压缩

用法和gzip基本一致

不能压缩文件夹

### tar命令

gzip太不方便了，不好打包。就用tar用于打包，不会进行压缩，反而会让文件变大。

`tar -cf test.tar test`

- cxt只能出现其中一个参数
- f要配合cxt使用`tar -tf test.tar`
- 常用压缩方式：`tar -zcvf test.tgz test`
- 常用解压方式：`tar -zxvf test.tgz`
- 解压到指定目录：`tar -zxvf test.tgz -C dd`

| 命令 | 解释                   |
| :--- | ---------------------- |
| -c   | 打包(create)           |
| -x   | 拆包()                 |
| -t   | 不拆包，查看内容       |
| -f   | 指定文件               |
| -v   | 查看打包或拆包的过程   |
| -z   | 使用gzip的方式压缩.tgz |
| -j   | 用bzip2的方式压缩.tbz  |
| -C   | 解压到指定目录         |



# 4. Linux软件安装和系统管理

## 4.1 nginx服务器的使用介绍

### nginx的yum安装

`sudo yum install nginx`

`sudo systemctl start nginx.service`启动nginx服务

`sudo systemctl stop nginx.service`停止nginx服务

执行完这两句以后：打开网址就能看到效果http://119.45.58.134/

`whereis nginx`



查看nginx进程

`ps -aux|grep nginx`

### nginx的启动流程

- 启动`systemctl start nginx.service`

- 读取`/etc/nginx/nginx.conf`配置文件（关键）

  - `listen 80 default_server` 监听端口

  - `root /usr/share/nginx/html`静态页面的存放路径

  - 可以看到访问的文件在：`/usr/share/nginx`

    通过修改里面的html文件可以改变显示的情况。

## 4.2 使用源代码的方式安装

- 从网页下载一个文件：

  `wget http://nginx.org/download/nginx-1.18.0.tar.gz`

- 解压

  `tar -zxvf nginx-1.18.0.tar.gz `

- 编译前执行配置文件：`./configure --prefix=/usr/local/nginx`

  - `--prefix`用来配置Nginx服务器的安装目录
  - 配置出错多是因为缺少依赖库或编译器
  - 需要安装的依赖：`sudo yum install gcc-c++ pcre pcre-devel zlib zlib-devel openssl opensll-devel`
  - configure命令执行成功以后，会生成一个新的Makefile文件
  - `sudo make && sudo make install`
  - 启动nginx：`cd /usr/local/nginx/sbin`，执行`sudo nginx`

## 4.3 开放端口

阿里云的需要开放端口80，腾讯云已经默认开放了。

## 4.4 安装python3



`sudo yum install python3 -y`

但是标准的centos不能直接安装

### 使用EPEL安装

extra packages for enterprise linux

- `sudo yum install epel-release`相当于扩展了软件库
- `sudo yum install python3`

### 使用源码安装

- `wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tgz`
- `tar -zxvf Python3.7.5.tgz`
- 进入解压的文件夹，运行`./configure`
- 运行`yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xzdevel libffi-devel`安装依赖
- `sudo make && sudo make install`安装python
- 运行`ln -s /usr/local/bin/python3.7 /usr/bin/python3`命令，在`/usr/bin`目录下建立python3.7的软连接
- 运行`python3`命令可以打开python3.7

## 4.5 虚拟环境介绍

![](img/虚拟环境.png)

系统的主环境有个site_packages

可以`import sys`然后`sys.path`查看路径

使用虚拟环境的目的是为了简化包，使得把开发好的项目打包的时候不那么臃肿。

## 4.6 虚拟环境管理

pycharm新建项目的时候可以选择同时新建环境。

这样在项目底下就会默认有一个venv文件夹，此时用pip安装包时，包会被装到venv文件夹里。这样的缺点是打包项目时会把依赖包一起打包了。（最直观的影响是上传到github的时候要传很多东西）项目里有代码就够了。

可以把venv文件夹统一放在别的地方。在把项目给别人的时候生成一个文件：

`pip freeze > requirements.txt`

别人就可以一键安装：`pip3 install -r requirements.txt`

##  4.7 linux里的虚拟环境

linux中pip下载包的地方：`whereis python3`

`/usr/local/lib/python3.6/site-packages`

## 4.8 管理虚拟环境

同理，可以在当前用户的家目录`/home/light/.envs`里创建一个总的环境管理文件。然后把各个项目的依赖库放里面。

- `sudo pip3 install virtualenv`

- `sudo pip3 install virtualenvwrapper`

  - `cd /usr/local/bin/`可以看到`virtualenvwrapper.sh`。这个是执行包管理程序的shell脚本。

  - `vim ~/.bashrc`加入3行代码

    ```
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6  # 指定新虚拟环境默认的python版本
    export WORKON_HOME=~/.envs  # 指定虚拟环境创建的位置
    source /usr/local/bin/virtualenvwrapper.sh  # 执行virtualenvwrapper.sh脚本
    ```

  - `source ~/.bashrc` 重新启动bashrc脚本（退出终端再进同理）

  - `mkvirtualenv pa`创建虚拟环境

这样，安装的包就放在：`/home/light/.envs/pa/lib/python3.6/site-packages`

**启动(切换)环境**`workon pb`

**退出环境** `deactivate`

**删除环境** `rmvirtualenv pa`

## 4.9 linux里的环境

`cd /bin/	`

`ll python*`

**新建连接**

`sudo ln -s python3.6 python`新建了一个连接指向python3.6（不建议）

`sudo ln -s pip3 pip`用pip指向pip3



顺便补充：在执行linux命令时，系统在哪里找命令呢。可以用`echo $PATH`查看

# 5. Shell快速入门和版本控制

## 5.1 服务监听的常见命令

相当于windows的任务管理器。

| 列名    | 说明                                                         |
| ------- | ------------------------------------------------------------ |
| USER    | 是哪个用户开启的                                             |
| PID     | 进程ID                                                       |
| %CPU    | 该process 使用的CPU资源百分比                                |
| %MEM    | 占用的物理内存百分比                                         |
| VSZ     | 使用的虚拟内存量(kb)                                         |
| RSS     | 占用的固定内存量(kb)                                         |
| TTY     | 在哪个终端机上运行，若与终端机无关，显示`?`<br />另外， tty1-tty6 是本机上面的登入者程序，若为 pts/0 等等的，则表示为由网络连接进主机的程序。 |
| STAT    | 该程序目前的状态，主要的状态有：<br />R ：该程序目前正在运作，或者是可被运作<br />S ：该程序目前正在睡眠当中 (可说是 idle 状态)，但可被某些讯号 (signal) 唤醒。<br />T ：该程序目前正在侦测或者是停止了<br />Z ：该程序应该已经终止，但是其父程序却无法正常的终止他，造成 zombie (疆尸) 程序的状态 |
| START   | 该 process 被触发启动的时间                                  |
| TIME    | 该 process 实际使用 CPU 运作的时间                           |
| COMMAND | 该程序的实际指令                                             |

`ps -aux`

`ps -aux|grep nginx`查询`nginx`只查到一个进程，这个进程就是自己

`ps -aux|grep -v grep|grep nginx`

`ps -ef`

`ps -u light`



`top`可以动态查看进程信息



`kill <PID>`关闭某个进程

`kill -9 <PID>`强制关闭



`pstree`查看树形结构

`pstree -p`显示PID

`netstat -anop`查看网络的连接状态

`sudo netstat -anop|grep :8080`查看某个端口的情况

```
-a 显示所有socket，包括正在监听的
-n 以网络IP地址代替名称，显示出网络连接情形
-o 显示与网络计时器相关的信息
-t 显示TCP协议的连接情况
-u 显示UDP协议的连接情况
-p 显示建立相关连接的程序名和PID
```

## 5.2 管道和重定向

### 管道

以前一个命令的标准输出作为下一个命令的标准输入。

`ps -aux|grep nginx`中的`|`就是一个管道。

`yum list installed|less`

`find -name demo.txt`从当前目录下查找文件

`find -name demo.py|xargs rm -rf`找到`demo.py`并删除。

### 重定向

符号：`>`与`>>`

`ps -aux > ps.txt`把信息输出到一个txt文件里。文件已经存在，会覆盖原文件。

`ps -aux >> ps.txt`把执行结果追加到文件

分类

- 标准输出：`lx 1> p.txt`若命令执行错误，会创建文件，但是没有任何内容。
- 错误输出：`lx 2> p.txt`把错误信息写入文件，但是如果命令写对了，就会直接输出命令结果，也会创建文件，但是没有任何内容。
- 全部输出：`lx &> p.txt`

## 5.3 多个命令的连接

`ls;mkdir demo`多个命令，前面的错了，后面的也会执行。

`ls || mkdir demo`如果前面的命令执行**成功**，后面的命令不会执行。

`ls && mkdir demo`如果前面的命令执行**失败**，后面的命令不会执行。

## 5.4 shell编程的概念

`.sh`结尾的脚本，自动输入命令，方便维护服务器。

```shell
#!/bin/bash
mkdir student1
mkdir student2
mkdir student3

```

运行：

- `bash test.sh`
- `source test.sh`
- `./test.sh`如果要以此方式执行一个脚本，需要给它添加可执行权限`chmod a+x test.sh`

### 脚本首行

```
#!/bin/sh
#!/bin/bash
#!/usr/bin/env bash
```

python脚本首行

```
#!/usr/bin/env python
```

软连接

`ln -s pip3 pip`



## 5.5 shell编程初体验

```shell
#!/bin/bash

# 字符串可以不加引号
echo hello
echo "I am `whoami`" # 反引号内容会被解释为Linux命令
echo "I love linux"
echo "The CPU is my PC has `cat /proc/cpuinfo |grep -c processor` cores"
exit 0
```



## 5.6 变量和$符的使用

等号两端不能有空格

`$`符号的使用

- `${变量名}`
- `$(cmd)`
- `$((表达式))`

```shell
#!/bin/bash

# 字符串可以不加引号
age=10 # shell里的变量，**等号两端不能有空格！**
echo "I am `whoami`" # 反引号内容会被解释为Linux命令
echo $age
echo ${age}  # {} 大多数情况可以省略
echo $(whoami)  # 相当于 `whoami`
echo $((1+1))
# 特殊取值
echo '$0的值为: '$0  # 显示sh脚本名
echo '$1的值为: '$1  # 显示第一个参数名
echo '$2的值为: '$2  # 显示第二个参数名

echo '$*的值为: '$*  # 显示所有参数
echo '$@的值为: '$@  # 显示所有参数
echo '$#的值为: '$#  # 显示参数个数

echo '$?的值为: '$?  # 显示脚本的执行结果。0表示执行完成正常退出

echo "I am $age years old"
echo 'I am $a years old'  #  单引号不会使用变量
exit 0
```

## 5.7 环境变量的使用

```shell
#!/bin/bash

# shell里还能定义环境变量
export x=yes
```

然后执行以下两句就能看到环境变量x的结果
```
source test.sh
echo x
```

## 5.8 修改环境变量

`echo $PATH`查看环境变量

`export PATH=$PATH:/home/light/mybin`修改，但这个是临时的，重开终端后失效。



`vim ~/.bashrc`

把刚刚那句加到最后一行。

`source ~/.bashrc`

## 5.9 if语句的基本使用

```shell
export PATH=$PATH
read -p `请输入年龄` age
echo $age
```

条件判断语句

```shell
if ls /;then  # if 后接一个命令，如果命令成功执行then，否则执行else
	echo "命令执行成功"
else
	echo "命令执行失败"
fi
```

## 5.10 if条件测试语句

```shell
# 这个语法会报错
if 3 > 2;then
	echo "命令执行成功"
else
	echo "命令执行失败"
fi

# 正确写法
if [ 3 -gt 2 ]; then
	echo "命令执行成功"
else
	echo "命令执行失败"
fi
```

**中括号内左右两边加空格**

### 数值比较

这种比较只能支持数字

| 命令    | 说明         |
| ------- | ------------ |
| a -eq b | a 等于 b     |
| a -ge b | a 大于等于 b |
| a -gt b | a 大于 b     |
| a -le b | a 小于等于 b |
| a -lt b | a 小于 b     |
| a -ne b | a 不等于 b   |

### 字符串比较

```shell
read -p '输入x' x
read -p '输入y' y

if [ $x = $y ];then
	echo "x == y"
else
	echo "x != y"
	
if [ $x != $y ];then
	echo "x == y"
else
	echo "x != y"
	
if [[ $x > $y ]];then
	echo "x == y"
else
	echo "x != y"
```
比较运算符两边可以带空格可以不带
| 命令         | 用法                                        |
| ------------ | ------------------------------------------- |
| `str1 == str2` | 判断两字符串是否相等，等号两边要加空格      |
| `str1 != str2` | 不相等                                      |
| `str1<str2`    | 需要使用`[[]]`                              |
| `str1>str2`    |                                             |
| `-n str1`      | 检查str1的长度是否非0（变量需要添加双引号） |
| `-z str1`      | 检查str1的长度是否为0                       |

### 文件比较

```shell
read -p '请输入一个路径' path

if [ -d $path ];then
	echo "输入的是目录"
else
	echo "输入的不是目录"
```

| 命令            | 说明                           |
| --------------- | ------------------------------ |
| -d file         | 是否存在且是目录               |
| -e file         | 是否存在                       |
| - f file        | 是否存在且是文件               |
| -r file         | 是否存在且可读                 |
| -w file         | 是否存在且可写                 |
| -x file         | 是否存在且可执行               |
| -s file         | 是否存在且非空                 |
| -O file         | 是否存在且属于当前用户         |
| -G file         | 是否存在且所属组与当前用户相同 |
| file1 -nt file2 | 检查file1是否比file2新         |
| file1 -ot file2 | 检查file1是否比file2老         |

## 5.11 case语句

```shell
read -p '请输入您要执行的操作' op

case $op in
	1)
		echo 添加用户
		;;
	2) 
		echo 删除用户
		;;
	3)
		echo 查询用户
		;;
	*)
		echo 操作有误
		;;
esac
```



## 5.12 循环语句



```shell
# 第一种格式
for i in `seq 1 10`
do
	echo $i
done

# 第二种格式:C语言风格
for((j=0;j<=10;j++))
do
	echo $j
done
```



## 5.13 函数

```shell
#!/bin/bash
# function可以省略
function foo() {
	echo 'hello'
	echo "my name is $1 im $2 years old!"
	echo "参数的个数为 $#"
}

# 函数调用，没传参数，默认空格。
echo 函数调用，没传参数，默认空格。
foo

# 传参数，会正确显示
echo 传参数，会正确显示
foo lily 10

```



## 5.14 数组

只支持一位数组。

```shell
# array_name=(value1, value2, ...)
arr=(hello lily "yes" 10)
echo $arr  # 默认获取列表的第0个数据
echo $arr[3]  # 结果是hello[3]

echo ${arr[3]}  # 需要加大括号

# 获取所有数据
echo ${arr[*]}
echo ${arr[@]}

# 获取长度
echo ${arr[#]}

# 遍历数组
for n in ${arr[*]}
do
	echo $n
done

# 遍历数组
for((x=0;x<${#names[*]});x++)
do
	echo ${names[x]}
done

```

