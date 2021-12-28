```shell
systemctl start xxx  # 启动某个服务
systemctl stop xxx  # 
systemctl enable xxx  # 开机自启动
systemctl disable xxx  # 关闭开机自启动
systemctl status xxx  # 查看某个服务状态
```



## 拷贝

将某目录下的一个文件拷贝到另一个目录下

```
cp shop/apple.csv warehouse
```

将某文件夹内的所有文件全部拷贝到另一个目录下

```
cp -r shop/. warehouse
```

将某文件及其所有文件拷贝到另一个目录下

```
cp -r shop warehouse
```

## 远程拷贝

将本地电脑上的某个文件拷贝到另一台电脑上

```
scp shop/apple.csv root@192.168.1.123:/home/shop
```

## 移动

