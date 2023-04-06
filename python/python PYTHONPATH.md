虽然被作者骂成笨瓜了，但是不得不承认他写的挺好的。

https://github.com/ydf0509/pythonpathdemo

PYTHONPATH的作用演示，创建这样一个项结构的项目

```
|=demo
  |=d1
    |=d2
      |=d3
        |-apple.py
  |=d4
    |=d5
      |=banana.py
```

使用方式

Windows

```
set PYTHONPATH=E:\Github\work\my_project
python demo.py
```

写在一行

```
set PYTHONPATH=E:\work\my_project & python demo.py
```



Linux

```
export PYTHONPATH=/projects/my_project ; python run.py
```





一个环境变量设置多个值，linux是 `:` 隔开，win是` ;` 隔开。

```
# Linux
export PYTHONPATH=/codes/proj1:/codes/proj2

# Windows
set PYTHONPATH=/codes/proj1;/codes/proj2
```



vscode 设置 PYTHONPATH

`ctrl + shift + p` , 搜索open settings ，找到json文件，加入或者修改下面这行。

```json
"terminal.integrated.env.windows": {"PYTHONPATH":"${workspaceFolder};${env:PYTHONPATH}"}
```

