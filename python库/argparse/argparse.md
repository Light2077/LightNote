# argparse

https://docs.python.org/zh-cn/3/howto/argparse.html#id1

就是在命令行用python运行脚本文件时，可以附带参数命令。

比如在linux系统下：

```
ls -a
```

## 例1：快速使用

创建一个`demo.py`文件。

```python
# demo.py
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")  # 增加一个位置参数
args = parser.parse_args()
print("hello %s!" % args.name)
```

在这个文件所在的目录下打开终端，并输入

```
python demo.py jack
```

结果：

```
hello jack!
```

使用`-h`或`--help`查看帮助：

```
>>> python demo.py -h
usage: demo.py [-h] name

positional arguments:
  name

optional arguments:
  -h, --help  show this help message and exit
```

- positional arguments 是必须要输入的参数
- optional arguments 可以输入也可以不输入

## 例2：add_argument的常用参数

- `type`: 指定这个参数的数据类型，默认是字符串
- `help`: 提示说明，建议每个参数都写

```python
# demo.py
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name", help="enter you name", type=str)
parser.add_argument("age", help="enter you age", type=int)
args = parser.parse_args()
print(f"hello {args.name}, you are {args.age} years old.")
```

如果还是只输入jack，会报错，因为增加了`age`这个位置参数

```
python demo.py jack
```

```
usage: demo.py [-h] name age
demo.py: error: the following arguments are required: age
```

输入姓名和年龄

```
python demo.py jack 13
```

```
hello jack, you are 13 years old.
```

如果年龄输成字符串，会报错

```
python demo.py jack apple
```

```
usage: demo.py [-h] name age
demo.py: error: argument age: invalid int value: 'apple'
```

查看帮助

```
python demo.py --help
```

```
usage: demo.py [-h] name age

positional arguments:
  name        enter you name
  age         enter you age

optional arguments:
  -h, --help  show this help message and exit
```

## 例3：缩写与可选参数

这个例子把name和age变成可选参数，并且使用缩写

```python
# demo.py
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="enter you name", type=str)
parser.add_argument("-a", "--age", help="enter you age", type=int)
args = parser.parse_args()
if not args.name or not args.age:
    print('do not know who you are')
else:
    print(f"hello {args.name}, you are {args.age} years old.")
```

这次什么都不输入就不会报错了

```
python demo.py
```

```
do not know who you are
```

用缩写和全称输入name和age

```
python demo.py -n jack --age 13
```

```
hello jack, you are 13 years old.
```

直接输入name和age，会报错

```
python demo.py jack 13
```

```
usage: demo.py [-h] [-n NAME] [-a AGE]
demo.py: error: unrecognized arguments: jack 13
```

查看帮助：可以看到name和age变成了可选参数

```
python demo.py -h
```

```
usage: demo.py [-h] [-n NAME] [-a AGE]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  enter you name
  -a AGE, --age AGE     enter you age
```



