```python
import tqdm
import time

# 假设为 22.56mb
size = 22.56 * 1024 * 1024
pbar = tqdm.tqdm(total = size, initial=0, desc="download", unit_scale=True, unit="B")

total_time = 5
total_iter = 1000
for i in range(total_iter):
    time.sleep(total_time / total_iter)
    pbar.update(size / total_iter)
```

- total : 总大小
- initial：初始进度
- desc：下载描述，在进度条前面
- unit_scale：自动缩放范围，把单位变成 G M K 等格式
- unit：单位字符串