方便快捷地匹配文件

```python
import glob

# 提取当前文件夹下的所有png文件
print(glob.glob('./*.png'))
```

| 模式     | 含意                        |
| -------- | --------------------------- |
| `*`      | 匹配所有                    |
| `?`      | 匹配任何单个字符            |
| `[seq]`  | 匹配 *seq* 中的任何字符     |
| `[!seq]` | 匹配任何不在 *seq* 中的字符 |

递归提取home目录下所有csv文件的路径

```python
import os
data_dir = '/home'
pattern = os.path.join(data_dir, f'**/*.csv')
paths = glob.glob(pattern, recursive=True)
```

