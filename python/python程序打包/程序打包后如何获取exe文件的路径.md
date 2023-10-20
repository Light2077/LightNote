```python
if getattr(sys, 'frozen', False):
    # 如果是由 PyInstaller 打包后的程序
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
```

其他方案

```python
path = os.path.realpath(sys.argv[0])
dir_path = os.path.dirname(path)
```

