# subprocess

https://docs.python.org/zh-cn/3.8/library/subprocess.html?highlight=subprocess#module-subprocess

偶然看见的[`sched`](https://docs.python.org/zh-cn/3.8/library/sched.html#module-sched) --- 事件调度器

## 感性认识

新建一个目录，目录下有两个文件

```
|-demo
    |-main.py
    |-hello.py
```

在`hello.py`中

```python
# hello.py
print('hello world!')
```



在`main.py`中

```python
import subprocess

subprocess.run(['python', 'hello.py'])
```



执行`main.py`文件得到如下结果

```
hello world!
```



就是能在python程序中，另起一个进程跑另一个py文件。



## **`subprocess.run()`的返回值**

修改代码如下：

```python
# main.py
import subprocess

res = subprocess.run(['python', 'hello.py'])
print("args:", res.args)
print("returncode", res.returncode)
```

运行后

```
hello world!
args: ['python', 'hello.py']
returncode: 0
```

returncode 表示你run的这个py文件过程是否正确

如果正确，返回0，否则返回1



修改`hello.py`，故意制造一个bug

```python
# hello.py
print('hello world!')
a = 
```

再运行main函数，得到返回

```
  File "hello.py", line 3
    a = 
       ^
SyntaxError: invalid syntax
args: ['python', 'hello.py']
returncode: 1
```

全面的返回值：

- `args`：被用作启动进程的参数，可能是列表或字符串
- `returncode`：子进程的退出状态码
- `stdout`：从子进程捕获到的标准输出
- `stderr`：捕获到的子进程标准错误
- `check_returncode()`：如果 [`returncode`](https://docs.python.org/zh-cn/3.8/library/subprocess.html?highlight=subprocess#subprocess.CompletedProcess.returncode) 非零, 抛出 [`CalledProcessError`](https://docs.python.org/zh-cn/3.8/library/subprocess.html?highlight=subprocess#subprocess.CalledProcessError).

## 疑惑

- 如何得到错误信息

修改`main.py`

```python
# main.py
import subprocess
from subprocess import PIPE

res = subprocess.run(['python', 'hello.py'], stdout=PIPE, stderr=PIPE)
print('stdout': res.stdout)
print('stderr': res.stderr)
```

## 与子进程进行通信

可以通过`subprocess.run()`的`input`参数给子进程发送消息。如果不设置encoding，就要传入二进制串，比如`b'hhhhhhh'`

```python
# main.py
import subprocess
from subprocess import PIPE

res = subprocess.run(['python', 'hello.py'],
                     input='hhhhhhh',
                     encoding='utf8')
print('stdout:', res.stdout)
```

```python
# hello.py 
import sys
data = sys.stdin.read()
print(data)
```

