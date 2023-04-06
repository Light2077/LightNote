https://blog.csdn.net/weixin_44799217/article/details/122083636

核心就是

```shell
nohup -u python demo.py > nohup.out &
tail -f nohup.out
```







将python在终端的输出输出到`nohup.out`文件

```shell
nohup python demo.py >> nohup.out &
```

使用`tail`命令实时查看运行的结果

```shell
tail -f nohup.out
```



有时候可以看到输入的是

```shell
nohup python demo.py > nohup.out 2>&1 &
```

2>&1 解释：

将标准错误 2 重定向到标准输出 &1 ，标准输出 &1 再被重定向输入到 nohup.out 文件中。

    0 – stdin (standard input，标准输入)
    1 – stdout (standard output，标准输出)
    2 – stderr (standard error，标准错误输出)
------------------------------------------------
有时候会发现`nohup.out`文件迟迟不显示python print的结果，这时可以在

这是因为python的输出有缓冲，导致nohup.out并不能够马上看到输出。在使用python运行程序前，可以加入`-u`参数取消缓冲

```shell
nohup python -u demo.py > nohup.out &
```





