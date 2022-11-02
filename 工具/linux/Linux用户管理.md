# Linux用户管理

列出现有用户

```
cat /etc/passwd | cut -d : -f 1
```

添加用户

```
useradd light -m -s /bin/bash
```

- `-m`: 自动建立用户的登入目录
- `-s`: 定用户登入后所使用的shell

> 如果遇到`useradd: cannot lock /etc/passwd; try again later.`
>
> 使用`sudo`

设置密码

```
passwd light
```

```
$ sudo passwd light
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
```

切换用户

```
su light
```

删除用户

同时会删除家目录

```
userdel -r
```

### 修改sudoers文件夹

只有被添加到`/etc/sudoers`文件的用户才能使用`sudo`命令

```
sudo vim /etc/sudoers
```

或

```
visudo
```



找到下面这行

```
ubuntu  ALL=(ALL:ALL) NOPASSWD: ALL
```

然后新加入一行。（`yy`然后`p`）第一百行

```
light ALL=(ALL:ALL) NOPASSWD: ALL
```

查看用户进程

```
ps -u <username>
top -U <username>
```

