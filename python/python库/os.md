删除文件夹

```python
os.removedirs(path)
```

文件树遍历

其中root是文件的绝对路径

```python
for root, dirs, files in os.walk(args.path):
    print(root)
```



文件路径归一化

```python
os.path.normpath(path)
```

