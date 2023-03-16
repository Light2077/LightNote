为什么用

为什么我会想要用shell脚本来运行程序？

原本最简单的运行程序的方式就是

```shell
python main.py
```

在过去的学习中，我也是这么去做的，直到我了解到了`PYTHONPATH`https://github.com/ydf0509/pythonpathdemo

> 作者全程一副恨铁不成钢的语气，哈哈

也就是说，在运行python脚本前，可以设定一些环境变量，我能理解到的好处有：

- 可以写一个公共的工具包，设置了`PYTHONPATH`后所有项目都可以使用这个工具包的函数，这样就不用把常用的工具函数到处拷贝了。

但是如果每次都要写一次`export xxxx`，而且万一想加入其他的环境变量呢，每次都要输入未免过于麻烦，这时我突然想到以前一直觉得这玩意没啥用的shell脚本。

下面写一个简单shell脚本和python脚本，放在`tmp`文件夹下进行测试。

```python
# python脚本
import os

host = os.getenv("DATABASE_HOST", "null")
print("host:", host)
```

shell脚本

```sh
#!/bin/bash
export DATABASE_HOST=127.0.0.1

python3 main.py
```

运行python脚本

```
python3 main.py
```

运行shell脚本

```
./run.sh
```

> 若遇到无权限运行此脚本

设置权限

```
chmod u+x run.sh
```

验证`run.sh`设置的环境变量不会影响全局，可以在运行完`run.sh`后在终端输入

```
echo $DATABASE_HOST
```

设置环境变量

```
export DATABASE_HOST=127.0.0.1
```

再次查看

```
echo $DATABASE_HOST
```

```
127.0.0.1
```

重启终端后再次查看，临时环境变量就没了。

设置环境变量多个值

```
export PYTHONPATH=/codes/proj1:/codes/proj2
echo $PYTHONPATH
```

附加环境变量

```
export PYTHONPATH=$PYTHONPATH:/codes/newproj
```

