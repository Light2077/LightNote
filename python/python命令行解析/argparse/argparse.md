# argparse

https://docs.python.org/3/library/argparse.html

## 复习

现在有这样一个程序，要求使用`argparse`库完善下面的代码，实现从命令行传入参数给say_hello()函数并正确运行

```python
# 导入命令行解析库

def say_hello(name, age):
    print(f"hello {name}, you are {age} years old.")
    
if __name__ == "__main__":
    # 创建解析对象
    # 添加name和age参数
    # 解析命令行参数
    # 调用say_hello函数，并传递解析后的参数

```

完整版

```python
# 导入命令行解析库
import argparse

def say_hello(name, age):
    print(f"hello {name}, you are {age} years old.")

if __name__ == "__main__":
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description="a program to say hello")
    # 添加name和age参数
    parser.add_argument("--name", help="your name", type=str)
    parser.add_argument("--age", help="your age", type=int)
    # 解析命令行参数
    args = parser.parse_args()
    # 调用say_hello函数，并传递解析后的参数
    say_hello(args.name, args.age)

```



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

- positional arguments 位置参数：是必须要输入的参数
- optional arguments 可选参数：可以输入也可以不输入，在输入时需要指定参数名称，比如`python demo.py -n jack`

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

## 例4：短选项

就是True和False的选项

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", 
    help="increase output verbosity",
    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
```

```
python3 prog.py -v
```

```
verbosity turned on
```

## 例5：矛盾的选项



```python
import argparse

parser = argparse.ArgumentParser(description="calculate X to the power of Y")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print(f"{args.x} to the power {args.y} equals {answer}")
else:
    print(f"{args.x}^{args.y} == {answer}")
```

```shell
$ python3 prog.py --help
usage: prog.py [-h] [-v | -q] x y

calculate X to the power of Y

positional arguments:
  x              the base
  y              the exponent

options:
  -h, --help     show this help message and exit
  -v, --verbose
  -q, --quiet
```

注意 `[-v | -q]`，它的意思是说我们可以使用 `-v` 或 `-q`，但不能同时使用两者

## 例6：传入list

```python
# demo.py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mylist', nargs='+', help='list of integers')
args = parser.parse_args()

mylist = args.mylist
print(mylist)
```

在命令行中

```
python demo.py --mylist 1 2 3 4 5
```

## 手动传参进行测试

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("-l", "--level", help="等级")
parser.add_argument("--items", nargs="+", help="物品")
parser.add_argument("--hero", action="store_true", help="是否是英雄单位")

# 相当于 python demo.py tom - 60 --items weapon armor -h
args = parser.parse_args(["tom", "-l", "60", "--items", "weapon", "armor", "--hero"])

print(args)
# Namespace(hero=True, items=['weapon', 'armor'], level='60', name='tom')
```

查看帮助文档

```python
parser.print_help()
```

```
usage: ipykernel_launcher.py [-h] [-l LEVEL] [--items ITEMS [ITEMS ...]] [--hero] name

positional arguments:
  name

optional arguments:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
                        等级
  --items ITEMS [ITEMS ...]
                        物品
  --hero                是否是英雄单位
```

因为我是在jupyter中测试的，所以usage中显示的是`ipykernel_launcher.py`

## ArumentParser的参数

```python
parser = argparse.ArumentParser(
    prog="program name",  # default: sys.argv[0]
    usage="usage message",
    description="A description of what the program does",
    epilog="Text following the argument descriptions",
)
```



