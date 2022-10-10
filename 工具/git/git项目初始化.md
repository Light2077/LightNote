## 腾讯云连github

```
yum install git
```

配置用户名和邮件

```shell
git config --global user.name "light"
git config --global user.email "435786117@qq.com"
```

配置Git的私钥和公钥

```shell
ssh-keygen -t rsa -C "435786117@qq.com"
```

查看生成的公钥和私钥，然后把内容复制到github上

https://github.com/settings/keys

```shell
cat ~/.ssh/id_rsa.pub
```

验证是否配置成功了

```shell
ssh git@github.com
```

看到successfully就表示成功了



## 本地连服务器项目

创建一个git用户

```
sudo useradd -m git                                      （创建
sudo passwd git  
```





```shell
git clone git@192.168.1.101:/home/project/xxproject
```

```

```



## Command line instructions

You can also upload existing files from your computer using the instructions below.

**Git global setup**

```
git config --global user.name "iao"
git config --global user.email "iao"
```

**Create a new repository**

```
git clone git@172.16.2.114:ztn/opserver.git
cd opserver
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

### Push an existing folder

```
cd existing_folder
git init
git remote add origin git@172.16.2.114:ztn/opserver.git
git add .
git commit -m "Initial commit"
git push -u origin master
```

### Push an existing Git repository

```
cd existing_repo
git remote rename origin old-origin
git remote add origin git@172.16.2.114:ztn/opserver.git
git push -u origin --all
git push -u origin --tags
```



```
git remote add origin git@github.com:15th-airborne/lightbot.git
git branch -M main
```

