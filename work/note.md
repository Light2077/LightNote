# 虚拟机配置

**如果虚拟机网络是通的可以无视这部分**

拷贝50多个G的虚拟机文件，下载并打开vmware，点击**打开虚拟机**。找到下载的虚拟机镜像打开。

然后因为是拷贝的虚拟机，原来的网络配置和新机器可能对不上号，会出现虚拟机连不上网的情况。先要配置虚拟机的网络。

- 查看主机网络连接。win+s 搜索：“查看网络连接”

- 双击**VMware Virtual Ethernet Adapter for VMnet8**，点击**属性**，找到并双击**Internet协议版本4（TCP/IPv4）**

- 查看ip地址，如果没有默认网关的话可以把默认网关设置一下，我这里的配置是

  ```
  ip地址: 192.168.142.10
  子网掩码: 255.255.255.0
  默认网关：192.168.142.1
  
  首选DNS服务器：114.114.114.114
  ```

- ~~回到VMware，点击【编辑】→【虚拟网络编辑器】确定一下VMnet8的设置要和上面一致，比如这里的子网IP应该是`192.168.142.0`~~

- ~~点击【虚拟机】→【设置】，点击左边的网络适配器，网络连接选项选择自定义，然后下拉列表选VMnet8（NAT模式）~~（ps: 上面这两步好像不需要也行）

- 打开虚拟机的终端，修改这个文件`vi /etc/sysconfig/network-scripts/ifcfg-ens33`

  主要修改的是最下面几行，确保IP和网关和上面设置的一致

  ```
  # ... 上面的省略了
  DEVICE=ens33
  ONBOOT=yes
  ZONE=public
  IPADDR=192.168.142.18
  PREFIX=24
  GATEWAY=192.168.142.1
  DNS1=114.114.114.114
  ```

- 然后`ping www.baidu.com`应该就能ping通了。



启动

```shell
激活conda环境：source /home/workflow/conda/bin/activate octopus
不使用Pycharm启动：python manage.py runserver 0.0.0.0:8888
```

hive是基于Hadoop的一个数据仓库工具

desktop是BDAP平台的核心执行代码。

# nginx端口映射

参考文章

[windows下nginx的安装和使用](https://www.cnblogs.com/jiangwangxiang/p/8481661.html)

[window端口转发端口映射nginx实现端口转发](https://www.jianshu.com/p/9dc35c87e4bf)



为了让同一个局域网的其他主机也能连上你这台电脑的虚拟机。

- 下载并解压nginx：http://nginx.org/en/download.html。（**路径不能出现中文**）

- 修改nginx目录下`conf/nginx.conf`文件，在文件最后添加：

  ```nginx
  stream {
      upstream mstsc {
          server 192.168.142.18:8090;
      }
  
      server {
          listen 8090;
          proxy_pass mstsc;
      }
  }
  ```

  假如你的电脑IP地址是`172.16.1.166`，你的电脑上配置了一台虚拟机，它的ip是`192.168.142.18`，但是同一局域网的其他主机无法访问这台虚拟机。

  那通过上面的配置后，别人访问你主机的`172.16.1.166:8090`时就等于访问了你这台主机上的虚拟机的ip：`192.168.142.18:8090`。



gitlab登陆

http://172.16.2.114:9999/users/sign_in

# 项目启动

## 后端

这部分要运行在虚拟机中

```
git clone http://172.16.2.114:9999/ghb/wlxybdap.git

cd wlxybdap
python manage.py runserver 0.0.0.0:8090
# nohup python manage.py runserver 0.0.0.0:8090
```



## 前端

这部分运行在主机内

### linux安装nodejs

```
wget https://npm.taobao.org/mirrors/node/v14.15.0/node-v14.15.0-linux-x64.tar.xz
```

解压

```
tar -xvf node-v14.15.0-linux-x64.tar.xz
```

重命名

```
mv node-v14.15.0-linux-x64.tar.xz nodejs
```

创建软连接

```
ln -s <你的安装位置>/nodejs/bin/npm /usr/local/bin
ln -s <你的安装位置>/nodejs/bin/node /usr/local/bin
```

### windows安装

上官网下载安装包安装即可。http://nodejs.cn/download/

拷贝项目

```
git clone http://172.16.2.114:9999/lyf/frontend.git
```

进入项目，并安装依赖

```
cd frontend
npm install
```



修改项目文件`vue.config.js`

把下面这部分的target改成端口映射后的target

```vue
'/oldPasa': {

    target: 'http://172.16.1.166:8090', // 主要改这行！
    changeOrigin: true, // 当target指向是域名不是ip，需要设置为true，不然node转发会失败
    secure: false, // 如果是https接口，需要配置这个参数
    pathRewrite: {
        '^/oldPasa': ''
    }
},
```

运行项目

```
npm run dev
```

