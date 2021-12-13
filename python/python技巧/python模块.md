# 前言

模块搜索路径

- 内置模块
- 当前模块所在目录
- 环境变量PYTHONPATH默认包含python的安装路径
- python安装路径下的lib文件夹
- lib文件夹下的site-packages文件夹（第三方模块）
- sys.path.append()追加的目录



使用os

`__file__`

`os.path.dirname(__file__)`找到当前文件父路径



包和模块

- 包是一个文件夹
- 模块是py文件



权限控制

在模块内可以通过`__all__ = [...]`的方式控制访问权限

```python
# 导入这个包的时候只能访问a 和 b
# 只对import * 有效
__all__ = ['a', 'b']
a = 100
b = 200
c = 300
```

相对导入

```python
# 从当前路径下导入一个包
from . import mod1
```



# 导入模块

import 多次同一个模块，只会执行一次可执行语句。

```python
import time
from time import *
from math import cos
import datetime as dt
from copy import deepcopy as dp
```

```python
# _x  私有变量，建议只在本模块使用
# __x
# __x__

# 结束以后
del (_x, _y, ...)  # 这样别的用户强行调用时就会蹦
```

# pip模块管理

```shell
pip list  # 显示安装的所有包
pip install flask
pip uninstall flask
pip freeze  # 用来列出当前环境安装的模块名和版本号

pip freeze > requirements.txt  # 把需求包放到一个文件里
pip install -r requirements.txt  # 按照该文件安装库
 
# 阿里云 https://mirrors.aliyun.com/pypi/simple/
# 豆瓣 https://pypi.douban.com/simple/
# 清华 https://pypi.tuna.tsinghua.edu.cn/simple/
pip install flask -i https://pypi.douban.com/simple/


```



**永久修改下载源**

在当前用户目录下创建一个pip文件夹。

比如[C:\Users\Light\pip\pip.ini](C:\Users\Light\pip\pip.ini)

新建pip.ini

```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

# 自定义模块

要求：

- 命名规范：数字字母下划线组成。数字不能做开头



```
from demo import *

# 本质是读取模块里的__all__属性，看这个属性定义了哪些变量和函数

# 如果不写__all__默认除了以`_`开始的所有变量和函数都能用

# 可以用__all__限定某些方法或变量的使用
# __all__ = ['a', 'test']

# import demo 不受上述限制
```



`__name__`的使用

- 运行本py文件时`__name__ == '__main__'`
- 作为导入模块时，`__name__ == <模块名>`

```python
if __name__ == '__main__':
    ...
```

# 模块调用类内的方法

```python
class Person:
    
    def eat(self):
        print('正在吃饭')
    def sleep(self):
        print('正在睡觉')
_p = Person()

eat = _p.eat
sleep = _p.sleep
```

这样别的文件使用时

```python
import demo

demo.eat()
demo.sleep()
```





# 包的概念

本质上是一个文件夹，包含许多模块(py文件)。会有`__init__.py`文件，这个文件一般用来导入其他包。**init文件有什么用？**

```
|--package
    |--__init__.py
    |--module1.py
    |--module2.py
```

# os模块

```python
# 经常使用
os.path.isdir()  # 判断是否是文件夹
os.path.isfile()  # 判断是否是文件
os.path.exists()  # 判断是否存在
os.path.abspath()  # 绝对路径
os.path.normpath(path)  # 规范路径
os.path.splitext('2020.2.21.demo.py')  # 文件名后缀名分割

# 其他
os.getcwd()  # 获取当前路径
os.chdir()
os.rename(old_name, new_name)
os.remove(file_name)
os.rmdir(dir_name)  # 删除空目录
os.removedirs(dir_name)  # 递归删除文件夹
os.mkdir(dir_name)
os.name  # 获取操作系统名字
os.sep  # 路径的分隔符
os.environ  # 获取环境配置
os.environ.get('PATH')  # 获取指定环境配置

for root, dirs, files in os.walk(path, topdown=True):
    # 自顶向下
    print(root, dirs, files) 
```

# sys模块

```python
import sys

sys.exit()  # 退出程序，等于exit()
sys.path  # 表示查找模块的的路径
sys.stdin  # standard input file 接收用户输入，和input相关，可以接收用户输入
sys.stdout # 修改这个可以改变默认输出的位置
sys.stderr  # 可以改变错误输出的默认位置

```

# math模块

我还是比较熟的。

```python
import math
math.factorial(6)  # 阶乘

math.floor()  # 向下取整
math.ceil()  # 向上取整

math.pow(2, 10)  # 2 ** 10

math.sin(math.pi / 6)  # 弧度 π=180°

math.fabs(-10)  # 绝对值
math.modf(14.677)  # (0.6769999999999996, 14.0)
```



# random模块

```python
import random

random.randint(a, b)  # [a, b]中的整数随机数
random.randrange(a, b)  # [a, b)中的随机整数
random.uniform(1, 10)  # [1, 10) 中随机浮点数
random.random()  # [0, 1)的随机浮点数
random.choice('1234')  # 用来再可迭代对象随机抽取一个数据
random.sample('1234', n)  # 随机选取n个元素，不会有重复，返回list
random.choices('1234', k=4)  # 随机选取4个元素，会有重复，返回list

random.shuffle(iter)  # 没有返回值，随机打乱iter对象

```



# datetime模块

```python
import datetime as dt
# 4个类： datetime/date/time/timedelta
d = datetime.date(2020, 8, 2)  # 创建一个日期
t = datetime.time(18, 26, 30)  # 创建一个日期


dt.datetime.combine(d, t)  
now = dt.datetime.now()  # 获取当前时间
now.strftime(format='%Y-%m-%d %H:%M:%S')
now.date()
now.time()

d.year
d.month
d.day

t.hour
t.minute
t.second
t.microsecond

dt.datetime.now() + dt.timedelta(3)  # 3天之后的时间

# 没有year和month
delta = dt.timedelta(days=1, seconds=20,minutes=10,hours=10)s
```

# time模块

https://docs.python.org/3/library/time.html

1970-1-1 到2038年的某一天

```python
time.time()  # 当前时间的时间戳
time.strftime('%Y-%m-%d %H:%M:%S')  # 2020-12-06 19:36:28
time.strftime('%x')  # '01/10/21' 日/月/年
time.strftime('%X')  # '18:42:07'

time.asctime()  # 'Sun Aug  2 19:17:26 2020'
time.ctime()  # 'Sun Aug  2 19:17:41 2020'  输入秒数

time.sleep(2)  # 暂停两秒
```

# calender模块

``` python
import calendar

c = calendar.calendar(2020)  # 显示2020年的日历

calendar.setfirstweekday(calendar.SUNDAY)  # 设置每周的起始星期几
cnt = calendar.leapdays(1996, 2010)  # 计算1996-2010年一共有多少个闰年
calendar.islear(2020)  # 判断是否是闰年

m = calendar.month(2200, 3)  # 显示2200年3月的日历
def isleap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 ==0)
```



# hashlib和hmac模块

https://www.cmd5.com

md5解密

```python
import hashlib
import hmac

# hashlib 主要支持 md5 和 sha 加密
# 加密方式： 单向加密(md5, sha) 对称加密 非对称加密(rsa)
x = hashlib.md5()
# x = hashlib.md5('abc'.encode('utf8'))
x.update('abc'.encode('utf8'))
print(x.hexdigest())  # 不能再算回来
```

文件的md5

sha加密

```python
import hashlib
# 224表示224位2进制数
h1 = hashlib.sha1('123456'.encode())
h2 = hashlib.sha224('123456'.encode())
h3 = hashlib.sha256('123456'.encode())
h4 = hashlib.sha384('123456'.encode())

print(h1.hexdigest())
print(h2.hexdigest())
print(h3.hexdigest())
print(h4.hexdigest())
```

hmac模块

```python
import hmac
# 用秘钥key去加密msg
h = hmac.new(key='a'.encode(), msg='你好'.encode())
res = h.hexdigest()
print(res)
```



# uuid模块

```python
import uuid

# uuid1, 基于mac地址，时间戳，随机数，用来生成一个全局唯一的id。可以保证全球范围内的唯一性
# 32个有效字符。 16 ** 32
print(uuid.uuid1()) 
# python不支持
uuid.uuid2()

# 生成固定id
# 使用传入的字符串根据指定算法计算得出
uuid.uuid3(uuid.NAMESPACE_DNS, 'zhangsan')
uuid.uuid5(uuid.NAMESPACE_DNS, 'zhangsan')

# 常用
uuid.uuid4()  # 基于伪随机数。随机的，使用的最多。

```

场景：用户注册，连同uuid一起发给用户。

