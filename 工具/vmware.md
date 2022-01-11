# 安装虚拟机系统

## vmware下载安装

http://www.ddooo.com/softdown/177923.htm



## CentOS 8.5

https://blog.csdn.net/qq_41951895/article/details/121984630

https://blog.csdn.net/qq_34146694/article/details/104475916



下载系统镜像，选boot就行

- [CentOS-8.5.2111-x86_64-boot.iso[789Mb]](https://mirrors.tuna.tsinghua.edu.cn/centos/8.5.2111/isos/x86_64/CentOS-8.5.2111-x86_64-boot.iso)
- [CentOS-8.5.2111-x86_64-dvd1.iso[10.1Gb]](https://mirrors.tuna.tsinghua.edu.cn/centos/8.5.2111/isos/x86_64/CentOS-8.5.2111-x86_64-dvd1.iso)



安装过程中，选最小安装。

### 虚拟机换源

删除其他源，使用阿里源作为下载源。

```
cd /etc/yum.repos.d/
rm -rf *
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
yum makecache
```

https://mirrors.tuna.tsinghua.edu.cn/help/centos/
