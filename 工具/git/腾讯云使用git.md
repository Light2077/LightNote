## 腾讯云链接github

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



## 腾讯云连接gitlab

登录gitlab：http://172.16.2.114:9999/

可以查看这个教程生产一个ssh key: http://172.16.2.114:9999/help/ssh/README#generating-a-new-ssh-key-pair



```shell
ssh-keygen -t ed25519 -C "435786117@qq.com"
```

把下面这个的内容加入到gitlab的ssh keys里

```shell
cat .ssh/id_ed25519.pub
```



