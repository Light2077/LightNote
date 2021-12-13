删除markdown里没用到的图片

检索当前文件夹下所有图片的路径

检索md文件用到的所有图片的路径







创建一个示例用文件夹

```python
import os
import argparse
parser = argparse.ArgumentParser()
# 文件路径参数，默认是当前文件夹下
parser.add_argument("-p", "--path", type=str, default="./")  # 增加一个位置参数
args = parser.parse_args()

```

