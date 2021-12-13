如何查看linux系统是32位还是64位的

```
getconf LONG_BIT
```



使用yum时出现

```
Failed to set locale, defaulting to C.UTF-8
```

https://blog.csdn.net/zhujing16/article/details/107502403

原因：语言包没有安装

解决：

```
dnf install langpacks-en glibc-all-langpacks -y
```



