原作者github

https://github.com/yhilpisch/py4fi2nd

前7章的笔记分散到各个部分了，pandas、matplotlib等

之后出现的数据集也可以从这里面下载

可以直接参考这个项目https://aistudio.baidu.com/aistudio/projectdetail/1893297

# 第8章 金融时间序列

- 金融数据
- 滚动统计
- 相关分析
- 高频数据

## 金融数据

需要用到这个数据`tr_eikon_eod_data.csv`

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = "./data/tr_eikon_eod_data.csv"

data = pd.read_csv()
```

```python
data.info()
```

```
<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 2216 entries, 2010-01-01 to 2018-06-29
Data columns (total 12 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   AAPL.O  2138 non-null   float64
 1   MSFT.O  2138 non-null   float64
 2   INTC.O  2138 non-null   float64
 3   AMZN.O  2138 non-null   float64
 4   GS.N    2138 non-null   float64
 5   SPY     2138 non-null   float64
 6   .SPX    2138 non-null   float64
 7   .VIX    2138 non-null   float64
 8   EUR=    2216 non-null   float64
 9   XAU=    2211 non-null   float64
 10  GDX     2138 non-null   float64
 11  GLD     2138 non-null   float64
dtypes: float64(12)
memory usage: 225.1 KB
```

这里使用的数据来自Thomson Reuters (TR) Eikon Data API。TR 金融工具代码称作路透金融工具代码（RIC）。RIC 表示的金融工具为：

在很多情况下，pandas 在重新采样时默认使用区间的左侧标签（或者索引值）。为了在金融业务中保持一致，请确保使用右标签（索引值）——一般是区间内最后一个可用数据点。否则，金融分析中可能潜藏着预见偏差。

