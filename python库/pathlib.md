# pathlib

https://docs.python.org/zh-cn/3/library/pathlib.html

```python
from pathlib import Path
p = Path('.')
```

查看所有子目录

```python
[x for x in p.iterdir() if x.is_dir()]
```

列出当前目录树下所有python源代码文件

```python
list(p.glob('**/*.py'))
```

在目录树中移动

```python
p = Path('/etc')
q = p / 'init.d' / 'reboot'
q
```

```
WindowsPath('/etc/init.d/reboot')
```

```python
q.resolve()
```

```
WindowsPath('E:/etc/init.d/reboot')
```

查看文件名

```python
p = Path('./demo/fruits/apple.csv')
p.name
```

```
'apple.csv'
```

查看后缀名，如果没有后缀名，则为None

```python
p.sufiix
```

```
'.csv'
```

路径的文件扩展名列表

```python
Path('my/library.tar.gz').suffixes
```

```
['.tar', '.gz']
```

最后一个路径组件，除去后缀

```python
Path('my/library.tar.gz').stem
```

```
'library.tar'
```



```python
Path('my/library.tar').stem
```

```
'library'
```



返回为字符串



```python
p = Path('/etc/passwd')
str(p)
```

```
'\\etc\\passwd'
```



```python
p.as_uri()
```

```
'file:///etc/passwd'
```

以正斜杠`/`的路径字符串

```python
p.as_posix()
'/etc/passwd'
```



计算相对路径

```python
p = Path('/etc/passwd')
p.relative_to('/etc')
```

```
WindowsPath('passwd')
```

只能计算子路径的索引

```python
p.relative_to('/etc/passwd/apple/1.csv')
# 报错
```

