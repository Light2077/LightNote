https://www.gxlcms.com/redis-350514.html

**方法二：通过命令设置密码**

这种方法相对简单，不需要重启redis服务。连接redis之后，通过命令设置，如下：

```
config set requirepass 123456
```

如此，便将密码设置成了123456

设置之后，可通过以下指令查看密码

```
config get requirepass
```