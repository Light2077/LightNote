https://stackoverflow.com/questions/68358218/pandas-merging-start-end-time-ranges-with-short-gaps

```python
import numpy as np
import pandas as pd

np.random.seed(1)
df = pd.DataFrame(np.random.randint(1,5,30)
                  .cumsum()
                  .reshape(-1, 2), columns = ["start", "end"])

# 合并短间隔区间
def merge_short_interval(df, n=1):
    """ 间隔小于n的相邻区间会被合并 """
    g = df['start'].sub(df['end'].shift())
    df = df.groupby(g.gt(intervel).cumsum()).agg({'start':'min', 'end':'max'})
    return df

merge_short_interval(df)
```

思路

- 计算当前开始时刻减上一结束时刻，得到两个时间范围的间隔。
- 然后根据时间间隔分组，间隔小于阈值的被分为同一组。
- 对于每组，求出时间范围的最小、最大值，作为合并后的新范围。



这个方法还能够合并重叠的区间，前提是要有序排列。