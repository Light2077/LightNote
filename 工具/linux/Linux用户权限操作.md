查看文件权限

```
drwxrwxr-x  2 root   light  4096 Apr 14 11:57 projects/
```



## 用户组的概念



创建一个用户时，会自动创建一个和用户同名的分组。组存在的意义是为了更方便地管理权限。

- `groups`查看当前用户所在的分组
- `groups alice`查看某个用户所在分组
- `gpasswd -a alice light`把用户alice加到组light内
- `gpasswd -d alice light`把用户alice从组light内移除

![](images/用户组.png)



在ubuntu中可以用`gpasswd -a light sudo`使得light用户也能使用`sudo`命令。

而在centos中则是`gpasswd -a light wheel`

因为在centos的sudoers文件中有一个地方是：

```
## Allows people in group wheel to run all commands
%wheel  ALL=(ALL)       ALL
```

## 3.5 用户管理相关指令

查看所有用户和用户组文件

```sh
vim /etc/passwd
```

```sh
用户名:密码:用户id:组id::家目录:用户登录脚本
light:x:1000:1000::/home/light:/bin/bash
alice:x:1001:1001::/home/alice:/bin/bash
```

| 用户名 | 密码 | 用户id | 组id | 家目录      | 用户登录脚本 |
| ------ | ---- | ------ | ---- | ----------- | ------------ |
| light  | x    | 1000   | 1000 | /home/light | /bin/bash    |
| alice  | x    | 1001   | 1001 | /home/alice | /bin/bash    |

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

r读、w写、x执行

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

把`demo.txt`文件的**所属组**改成用户组light

```sh
sudo chgrp light demo.txt
```

把`demo.txt`文件的**所有者**改成用户light。

```sh
sudo chown light demo.txt
```

把`demo.txt`文件的**所有者和所属组**都改成用户light和用户组light。

```sh
sudo chown light:light demo.txt
```

