

参考：

- [Python中读取ZIP文件【csdn】](https://blog.csdn.net/zhuoqingjoking97298/article/details/121974670)
- [zipfile官方文档](https://docs.python.org/3/library/zipfile.html?highlight=zipfile#module-zipfile)



### 判断是否是有效的zip文件

```python
import zipfile

file_path = './demo.rar'
print(zipfile.is_zipfile(file_path))
```

### 查看压缩包内文件详细信息

会列出压缩包内的所有文件的信息

```python
with zipfile.ZipFile(file_path) as myzip:
    for info in myzip.infolist():
        print(info)
```

```
<ZipInfo filename='demo/1.csv' compress_type=deflate external_attr=0x20 file_size=43 compress_size=40>
<ZipInfo filename='demo/2.csv' ...>
<ZipInfo filename='demo/note/' external_attr=0x10>
<ZipInfo filename='demo/note/3.csv' ...>
<ZipInfo filename='demo/note/4.csv' ...>
<ZipInfo filename='demo/' external_attr=0x10>
```

可以使用`info.filename`，`info.compress_type`查看上述信息

可以用`info.is_dir()`判断路径是否是文件夹

### 查看压缩包内文件路径

```python
with zipfile.ZipFile(file_path) as myzip:
    for name in myzip.namelist():
        print(name)
```

```
demo/1.csv
demo/2.csv
demo/note/
demo/note/3.csv
demo/note/4.csv
demo/
```

### 读取压缩包内文件

```python
with zipfile.ZipFile(file_path) as myzip:
    with myzip.open('demo/note/4.csv') as f:
        text = f.read()
        print(text)
```

```
b',0,1,2,3\r\n0,6,3,7,4\r\n1,7,7,6,1\r\n2,7,3,7,7\r\n'
```

配合pandas

```python
with zipfile.ZipFile(file_path) as myzip:
    with myzip.open('demo/note/4.csv') as f:
        df = pd.read_csv(f)
        print(df, index=None)
```

```
Unnamed: 0 	0 	1 	2 	3
0 	0 	6 	3 	7 	4
1 	1 	7 	7 	6 	1
2 	2 	7 	3 	7 	7
```

### 解压所有文件到指定目录下

```python
output_dir = './output'
with zipfile.ZipFile(file_path) as z:
    z.extractall(path=output_dir)
```

### 解压部分文件到指定目录下

提取所有csv文件放到指定目录下

经过测试，path只能觉得解压到哪个目录下，并不能直接指定文件解压的路径。

```python
import os

output_dir = './output'
with zipfile.ZipFile(file_path) as z:
    for name in z.namelist():
        z.extract(name)
```

