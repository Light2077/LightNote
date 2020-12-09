# subprocess

https://docs.python.org/zh-cn/3.8/library/subprocess.html?highlight=subprocess#module-subprocess

偶然看见的[`sched`](https://docs.python.org/zh-cn/3.8/library/sched.html#module-sched) --- 事件调度器

直观感受，subprocess可以开启一个子进程来运行cmd命令。那就意味着可以在一个py文件里运行另一个py文件



## 例1：快速使用subprocess

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

## 例2：subprocess.run()的返回值

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

returncode 表示你run的这个py文件过程是否正确，如果正确，返回0，否则返回1

## 例3：全面的返回值介绍

- `args`：被用作启动进程的参数，可能是列表或字符串
- `returncode`：子进程的退出状态码
- `stdout`：从子进程捕获到的标准输出，但是没设置`subprocess.run()`中的`stdout`参数时，这一项是`None`。
- `stderr`：捕获到的子进程标准错误，没设置`subprocess.run()`中的`stderr`参数时，这一项是`None`。
- `check_returncode()`：如果 [`returncode`](https://docs.python.org/zh-cn/3.8/library/subprocess.html?highlight=subprocess#subprocess.CompletedProcess.returncode) 非零, 抛出 [`CalledProcessError`](https://docs.python.org/zh-cn/3.8/library/subprocess.html?highlight=subprocess#subprocess.CalledProcessError).

修改`main.py`

```python
# main.py
import subprocess

res = subprocess.run(['python', 'hello.py'])
print("args:", res.args)
print("returncode", res.returncode)
print("stdout", res.stdout)
print("stderr", res.stderr)
```

结果：

```
hello world!
args: ['python', 'hello.py']
returncode 0
stdout None
stderr None

Process finished with exit code 0
```

可以看到，没有设置`subprocess.run()`中的参数`stdout`和`stderr`时，这两项都是`None`

## 例4：代码有bug的情况

新建`fail.py`，故意制造一个bug

```python
# fail.py
a = 
```

修改`main.py`

```python
# main.py
import subprocess

res = subprocess.run(['python', 'hello.py'])
res2 = subprocess.run(['python', 'fail.py'])
```

再运行main函数，得到返回

```
hello world!
  File "fail.py", line 2
    a =
      ^
SyntaxError: invalid syntax
```

可以看到，先是正确打印了`hello.py`的内容，然后是`fail.py`的错误信息。

## 例5：捕获stdout和stderr

修改`main.py`

```python
# main.py
import subprocess

res = subprocess.run(['python', 'hello.py'], stdout=subprocess.PIPE)
res2 = subprocess.run(['python', 'fail.py'], stderr=subprocess.PIPE)

print('hello.py stdout:', res.stdout)
print('fail.py stderr:', res2.stderr)
```

结果

```
hello.py stdout: b'hello world!\r\n'
fail.py stderr: b'  File "fail.py", line 2\r\n    a =\r\n      ^\r\nSyntaxError: invalid syntax\r\n'
```

可以通过`res.stdout`与`res2.stderr`分别拿到正确print的信息和错误信息。

同时可以发现，子进程print和报错内容就不会在父进程打印输出了。

注意这里的`res.stdout`是一串二进制字符串。如果设置`encoding`参数，拿到的就是字符串。

```python
res = subprocess.run(['python', 'hello.py'], 
                     stdout=subprocess.PIPE,
                     encoding='utf8')
```



## 例6：与子进程进行通信

可以通过`subprocess.run()`的`input`参数给子进程发送消息。如果不设置encoding，就要传入二进制串，比如`b'hello input'`

```python
# main.py
import subprocess
from subprocess import PIPE

res = subprocess.run(['python', 'hello.py'],
                     input='hello input',
                     encoding='utf8')
```

修改`hello.py`接收传进来的字符串。

```python
# hello.py 
import sys
data = sys.stdin.read()
print(data)
```

结果

```
hello input

Process finished with exit code 0
```

