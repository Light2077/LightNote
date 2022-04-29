方便快捷地匹配文件

```python
import glob

# 提取当前文件夹下的所有png文件
print(glob.glob('./*.png'))
```



- `*`匹配多个字符
- `?`匹配单个字符