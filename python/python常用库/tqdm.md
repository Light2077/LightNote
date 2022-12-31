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
    pbar.set_description("Processing %s" % i)
```

- total : 总大小
- initial：初始进度
- desc：下载描述，在进度条前面
  - unit_scale：自动缩放范围，把单位变成 G M K 等格式

- unit：单位字符串

```
Processing 276:  28%|██▊       | 6.55M/23.7M [00:01<00:04, 4.24MB/s]
```



随时间显示

```python
import datetime
import time
from tqdm.auto import tqdm
td = datetime.datetime(2022, 10, 13, 17, 30) - datetime.datetime.now()
pbar = tqdm(total=td.seconds, bar_format='{desc}|{bar}|{n:.2f}/{total}[{rate_fmt}{postfix}]')


start = time.perf_counter()

cum = 0
while cum < td.seconds:
    time.sleep(0.01)
    now = time.perf_counter()
    cur = now - start
    
    d = cur - cum
    pbar.update(d)
    cum += d 
    pbar.set_description('%.2f' % cum)
```



bar_format可以高度定制进度条的显示样式

```
{desc}|{bar}|{n:.2f}/{total}[{rate_fmt}{postfix}]
```

对应

```
3.89: |█████████                       |3.89/10[ 1.00it/s]
```



默认是

```
{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]
```

```
  46%|██████████████               | 4.623/10 [00:04<00:05,  1.00s/it]
```

如果不设置desc的话前面就是空白的





案例：显示文字版的时钟

```python
import datetime
import time
from tqdm.auto import tqdm
td = datetime.datetime(2022, 10, 13, 17, 30) - datetime.datetime.now()

pbar = tqdm(total=td.seconds, bar_format='{desc}|{bar}|{n:.2f}/{total}')
start = time.perf_counter()

cum = 0
while cum < td.seconds:
    time.sleep(0.01)
    now = time.perf_counter()
    cur = now - start

    d = cur - cum
    pbar.update(d)
    cum += d
    
    pbar.set_description(datetime.datetime.now().strftime('%X'))
```



不显示进度条

```python
for path in tqdm(paths, disable=not verbose)
    ...
```

