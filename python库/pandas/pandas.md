# pandas

直观理解

pandas的两个数据类型：Series, DataFrame

围绕这两个数据类型，pd提供了一系列关于这两个数据类型的操作

- 基本操作
- 运算操作
- 特征类操作
- 关联类操作

非常强调数据和索引之间的关系

## Series

Series就是一维带“标签”的数组。

函数原型？

```python
import pandas as pd

a = pd.Series([9,8,7,6])
```

会输出自动索引

> 0 1 2 3 

也可以自定义索引

```python
import pandas as pd

a = pd.Series([9,8,7,6], index=['a','b','c','d'])
```

### Series创建方式

| 创建方式 | index长度            |
| -------- | -------------------- |
| 列表     | 长度一致             |
| 标量值   | 长度任意             |
| 字典     | 长度任意，元素可重复 |
| ndarray  | 长度一致             |
| 其他函数 |                      |

标量值创建

```python
import pandas as pd

s = pd.Series(25, index=['a','b','c'])
```

```python
''' 输出
>> s
a	25
b	25
c	25
dtype: int64
'''
```

**根据字典创建1**

```python
import pandas as pd

d = pd.Series({'a': 9, 'b':8, 'c':7})
```

```python
''' 输出
>> d
a	9
b	8
c	7
dtype: int64
'''
```

**根据字典创建2**

字典创建也可以用index参数，它可以指定数据排列方式

index的**长度可以小于**字典长度，也可以**重复**。

换言之：index多长，d多长，它的作用是从字典中选取元素。

```python
import pandas as pd

d = pd.Series({'a': 9, 'b':8, 'c':7}, index=['c','a','b','d'])
```

```python
''' 输出
>> d
c	25
a	25
b	25
d   NaN
dtype: float64
'''
```

**根据ndarray类型创建1**

```python
import pandas as pd
import numpy as np

n = pd.Series(np.arange(5))
```

```python
''' 输出
>> n
0	0
1	1
2	2
3	3
4   4
dtype: int32
'''
```

**根据ndarray类型创建2**

指定数据的索引

此法常用

```python
import pandas as pd
import numpy as np

n = pd.Series(np.arange(5), index=np.arange(9,4,-1))
```

```python
''' 输出
>> n
9	0
8	1
7	2
6	3
5   4
dtype: int32
'''
```

### Series类型的基本操作

**查看值和索引**

值(value)的输出是numpy的ndarray类型

索引(index)的输出是pandas的Index类型

```python
import pandas as pd

b = pd.Series([9,8,7,6],['a','b','c','d'])
```

```python
''' 输出
>> b.values
array([9, 8, 7, 6], dtype=int64)

>> b.index
Index(['a', 'b', 'c', 'd'], dtype='object')
'''
```

**根据index查看值**

自动索引和自定义索引是并存的

并存但是不混用

要么用自定义索引，要么用自动索引

```python
b['b']
'''
8
'''
b[1]
'''
8
'''
b[['c','d', 0]]

'''
# 0在自定义索引中不存在，所以输出NaN
c 7.0
d 6.8
0 NaN
dtype: float64
'''

b[['c','d','a']]
'''
c 7
d 6
a 9
dtype: int64
'''
```

**索引切片**

用自动索引切片时，自定义索引也会跟着一起切

```python
b[:3]
'''
a 9
b 8
c 7
dtype: int64
'''
```

**一些与numpy相似的操作**

in 只会判断自定义索引

```python
'c' in b
# 判断'c' 是不是b中索引的一部分
'''
True
'''

0 in b
'''
False
'''

b.get('f',100) # 若值不存在，返回100
'''
100
'''
```

Series类型对齐

```python
import pandas as pd

a = pd.Series([1,2,3],['c','d','e'])
b = pd.Series([9,8,7,6],['a','b','c','d'])
```

```python
a + b
'''
# 两个Series都得有对应的index
a    NaN  
b    NaN
c    8.0
d    8.0
e    NaN
dtype: float64
'''
```

**name属性**

```python
b.name
# 什么都不输出
b.name = 'Series对象'
# 给这个b赋予了名字
b.index.name = '索引列'
b
'''
索引列
a    9
b    8
c    7
d    6
Name: Series对象, dtype: int64
'''
```

## DataFrame的创建和查看

索引加队列数据构成，有点像excel，基本上都是2维数据

纵向称为index (axis=0) 对于行的索引

横向为column 对于列的索引

创建方式：

- 二维ndarray
- 由一维ndarray、列表、字典、元组、Series <font color='orange'>**构成的字典**</font>
- Series类型
- 其他的DataFrame类型

### 二维ndarray

基本生成方式，会自动生成**二维**索引

```python
import pandas as pd
import numpy as np

d = pd.DataFrame(np.arange(10).reshape(2,5))
''' >> d
   0  1  2  3  4
0  0  1  2  3  4
1  5  6  7  8  9
'''
```

### 通过Series类型的字典创建

字典的key作为列索引

字典中Series的index作为行索引

```python
dt = {'one': pd.Series([1,2,3], index=['a','b','c']),
      'two': pd.Series([9,8,7,6], index=['a','b','c','d'])}
d = pd.DataFrame(dt)
''' >> d
   one  two
a  1.0    9
b  2.0    8
c  3.0    7
d  NaN    6
'''
```

```python
pd.DataFrame(dt, index=['b','c','d'], columns=['two','three'])
'''
   two three
b    8   NaN
c    7   NaN
d    6   NaN
'''
```

在上面dt的基础之上

可见由于没有事先定义好的three，那一列的数据均为NaN

而且这次取的index也不完全，只取了b,c,d

### 通过列表类型的字典创建

跟上面的区别不大感觉

```python
import pandas as pd
dl = {'one': [1,2,3,4], 'two': [9,8,7,6]}
d = pd.DataFrame(dl, index=['a','b','c','d'])
''' >> d
   one  two
a    1    9
b    2    8
c    3    7
d    4    6
'''
```

### 例：各大城市某数据表格

```python
import pandas as pd
dl = {'城市': ['北京','上海','广州','深证', '沈阳'],
      '环比': [101.5, 101.2, 101.3, 102.0, 100.1],
      '同比': [120.7, 127.3, 119.4, 140.9, 101.4],
      '定基': [121.4, 127.8, 120.0, 145.5, 101.6]}
d = pd.DataFrame(dl, index=['c1','c2','c3','c4','c5'])
''' >> d
    城市     环比     同比     定基
c1  北京  101.5  120.7  121.4
c2  上海  101.2  127.3  127.8
c3  广州  101.3  119.4  120.0
c4  深证  102.0  140.9  145.5
c5  沈阳  100.1  101.4  101.6
'''
```

查看行索引

```python
d.index
'''
Index(['c1', 'c2', 'c3', 'c4', 'c5'], dtype='object')
'''
```

查看列索引

```python
d.columns # 注意有个s
'''
Index(['城市', '环比', '同比', '定基'], dtype='object')
'''
```

查看数据

```python
d.values
'''
array([['北京', 101.5, 120.7, 121.4],
       ['上海', 101.2, 127.3, 127.8],
       ['广州', 101.3, 119.4, 120.0],
       ['深证', 102.0, 140.9, 145.5],
       ['沈阳', 100.1, 101.4, 101.6]], dtype=object)
'''
```

查看某一列的数据

```python
d['同比']
'''
c1    120.7
c2    127.3
c3    119.4
c4    140.9
c5    101.4
Name: 同比, dtype: float64
'''
```

查看某一行数据

```python
d.ix['c2']
'''
城市       上海
环比    101.2
同比    127.3
定基    127.8
Name: c2, dtype: object
'''
```

根据2个索引查看某个具体数据

这里索引顺序是不能改变的：**先列后行**

```python
d['同比']['c2']
'''
127.3
'''
```

## 数据类型操作

如何改变Series和DataFrame对象？

增加或重排：reindex()

删除：drop

### 重排索引

在上面已经建立好的df的基础上**重排**

```python
d = d.reindex(columns=['城市','同比','环比','定基'])
d = d.reindex(index=['c5', 'c4', 'c3', 'c2', 'c1'])
'''
    城市     同比     环比     定基
c5  沈阳  101.4  100.1  101.6
c4  深证  140.9  102.0  145.5
c3  广州  119.4  101.3  120.0
c2  上海  127.3  101.2  127.8
c1  北京  120.7  101.5  121.4
'''
```

`.reindex(index=None,columns=None,...)`

| 参数          | 说明                                            |
| ------------- | ----------------------------------------------- |
| index,columns | 新的行列自定义索引                              |
| fill_value    | 重新索引中，填充缺失位置的值                    |
| method        | 填充方法：ffill向前填充，bfill向后填充          |
| limit         | 最大填充量                                      |
| copy          | 默认Ture，生成新的对象，False时，新旧相等不复制 |

### 索引类型的常用方法

索引是不可改变的，“.”的前面是行索引或者列索引

| 方法               | 说明                               |
| ------------------ | ---------------------------------- |
| .append(idx)       | 连接另一个Index对象，产生新的Index |
| .diff(idx)         | 计算差集，产生新的Index            |
| .intersection(idx) | 计算交集                           |
| .union(idx)        | 计算并集                           |
| .delete(loc)       | 删除loc位置处的元素                |
| .insert(loc,e)     | 在loc位置增加一个元素e             |

例：插入行与删除列

```python
ni = d.index.insert(5, 'c0')
nc = d.columns.delete(2)
#nd = d.reindex(index=ni, columns=nc, method='ffill')
# 貌似method='ffill'是错的
nd = d.reindex(index=ni, columns=nc).ffill()
''' >> nd
    城市     环比     定基
c1  北京  101.5  121.4
c2  上海  101.2  127.8
c3  广州  101.3  120.0
c4  深证  102.0  145.5
c5  沈阳  100.1  101.6
c0  沈阳  100.1  101.6
'''
```

### 删除指定索引对象

这一操作**不改变原来的数据**

```python
import pandas as pd

a = pd.Series([9,8,7,6],index=['a','b','c','d'])
''' >> a.drop(['b','c'])
a    9
d    6
dtype: int64
'''
```

换成城市的例子

```python
d.drop('c5') # 删除某一行
'''
    城市     环比     同比     定基
c1  北京  101.5  120.7  121.4
c2  上海  101.2  127.3  127.8
c3  广州  101.3  119.4  120.0
c4  深证  102.0  140.9  145.5
'''

d.drop('同比', axis=1) # 删除某一列
'''
    城市     环比     定基
c1  北京  101.5  121.4
c2  上海  101.2  127.8
c3  广州  101.3  120.0
c4  深证  102.0  145.5
c5  沈阳  100.1  101.6
'''
```

## 数据类型运算

算术运算根据行列索引，补齐后运算，运算默认产生浮点数

### DataFrame之间的运算

```python
import pandas as pd
import numpy as np

a = pd.DataFrame(np.arange(12).reshape(3,4))
b = pd.DataFrame(np.arange(20).reshape(4,5))
a * b
'''
      0     1      2      3   4
0   0.0   1.0    4.0    9.0 NaN
1  20.0  30.0   42.0   56.0 NaN
2  80.0  99.0  120.0  143.0 NaN
3   NaN   NaN    NaN    NaN NaN
'''
```

方法形式的运算

| 方法            |
| --------------- |
| .add(d,**argws) |
| .sub(d,**argws) |
| .mul(d,**argws) |
| .div(d,**argws) |

```python
b.add(a, fill_value = 100)
'''
       0      1      2      3      4
0    0.0    2.0    4.0    6.0  104.0
1    9.0   11.0   13.0   15.0  109.0
2   18.0   20.0   22.0   24.0  114.0
3  115.0  116.0  117.0  118.0  119.0
'''
```

将a跟b之间缺失的元素用100来填充，填充之后再运算



### DataFrame与Series的运算

```python
import pandas as pd
import numpy as np

b = pd.DataFrame(np.arange(20).reshape(4,5))
c = pd.Series(np.arange(4))
b
'''
    0   1   2   3   4
0   0   1   2   3   4
1   5   6   7   8   9
2  10  11  12  13  14
3  15  16  17  18  19
'''
c
'''
0    0
1    1
2    2
3    3
dtype: int32
'''
b-c
'''
      0     1     2     3   4
0   0.0   0.0   0.0   0.0 NaN
1   5.0   5.0   5.0   5.0 NaN
2  10.0  10.0  10.0  10.0 NaN
3  15.0  15.0  15.0  15.0 NaN
'''
相当于
c
'''
    0   1   2   3   
0   0   1   2   3   
1   0   1   2   3   
2   0   1   2   3 
3   0   1   2   3 
'''
```

dataframe与series的运算，会把series拉成行再运算。

如果想列相减

```python
b.sub(c, axis=0)
相当于
c
'''
    0   1   2   3	4   
0   0   0   0   0   0
1   1   1   1   1   1
2   2   2   2   2   2
3   3   3   3   3   3
'''
b-c
'''
    0   1   2   3   4
0   0   1   2   3   4
1   4   5   6   7   8
2   8   9  10  11  12
3  12  13  14  15  16
'''
```

### 比较运算

不会进行补齐，二维与低维之间为广播运算。

默认2维与1维也是把1维拉成一行来比较

```python
import pandas as pd
import numpy as np

a = pd.DataFrame(np.arange(12).reshape(3,4))
b = pd.DataFrame(np.arange(12,0,-1).reshape(3,4))
c = pd.Series(np.arange(4))
a > b
'''
       0      1      2      3
0  False  False  False  False
1  False  False  False   True
2   True   True   True   True
'''
a > c
'''
       0      1      2      3
0  False  False  False  False
1   True   True   True   True
2   True   True   True   True
'''
```

## 数据的排序

对数据的理解 -> 摘要 -> 有损地提取数据特征

- 基本统计（含排序）
- 分布/累计统计
- 数据特征：相关性、周期性

### 按索引排序

`.sort_index(axis=0,ascending=True)`

axis：默认对行索引进行排序

ascending：默认升序

```python
#生成demo
import pandas as pd
import numpy as np

b = pd.DataFrame(np.arange(20).reshape(4,5), index=['c','a','d','b'])

''' >> b
    0   1   2   3   4
c   0   1   2   3   4
a   5   6   7   8   9
d  10  11  12  13  14
b  15  16  17  18  19
'''
```

对**行索引升序**排序（<font color='orange'>**不改变**</font>原来的数据顺序）

```python
b.sort_index(axis=0, ascending=True) # 同b.sort_index() 
'''
    0   1   2   3   4
a   5   6   7   8   9
b  15  16  17  18  19
c   0   1   2   3   4
d  10  11  12  13  14
'''
```

对**列索引降序**排序

```python
b.sort_index(axis=1, ascending=False)
'''
    4   3   2   1   0
c   4   3   2   1   0
a   9   8   7   6   5
d  14  13  12  11  10
b  19  18  17  16  15
'''
```

### 按某行(列)数据值排序

在指定轴上根据数值排序，默认升序

`Series.sort_values(axis=0,ascending=True)`

`DataFrame.sort_values(by,axis=0,ascending=True)`

by——axis轴上的某个索引或索引列表

默认对列数据进行排序，所以by中填的值应该是行索引。

对“2”这一**列**的元素值进行降序排列

```python
b.sort_values(2, ascending=False)
'''
    0   1   2   3   4
b  15  16  17  18  19
d  10  11  12  13  14
a   5   6   7   8   9
c   0   1   2   3   4
'''
```

若想对某行数据进行排序，by中的值是列索引，axis=1。

对“a”这一**行**的元素值进行降序排列

```python
b.sort_values('a',axis=1,ascending=False)
'''
    4   3   2   1   0
c   4   3   2   1   0
a   9   8   7   6   5
d  14  13  12  11  10
b  19  18  17  16  15
'''
```

<font color='00CCCC'>**默认的NaN空值统一放到排序末尾**</font>

## 数据的基本统计分析

| 基本统计分析函数                                    | 说明                            |
| --------------------------------------------------- | ------------------------------- |
| `.sum()`                                            | 计算数据的总和，按0轴计算，下同 |
| `.count()`                                          | 非NaN值的数量                   |
| `.mean()` `.median()`                               | 计算数据的算术均值，算术中位数  |
| `.var()` `.std()`                                   | 计算数据的方差、标准差          |
| `.min()` `.max()`                                   | 计算数据的最小最大值            |
| `.describe()`<font color='orange'>**(常用)**</font> | 对0轴（各列）的统计汇总         |

**仅适用于Series类型**

| 方法                    | 说明                                       |
| ----------------------- | ------------------------------------------ |
| `.argmin()` `.argmax()` | 计算最大值、最小值所在位置的**自动**索引   |
| `.idxmin()` `.idxmax()` | 计算最大值、最小值所在位置的**自定义**索引 |

describe()用法示例

```python
b.describe()
'''
               0          1          2          3          4
count   4.000000   4.000000   4.000000   4.000000   4.000000
mean    7.500000   8.500000   9.500000  10.500000  11.500000
std     6.454972   6.454972   6.454972   6.454972   6.454972
min     0.000000   1.000000   2.000000   3.000000   4.000000
25%     3.750000   4.750000   5.750000   6.750000   7.750000
50%     7.500000   8.500000   9.500000  10.500000  11.500000
75%    11.250000  12.250000  13.250000  14.250000  15.250000
max    15.000000  16.000000  17.000000  18.000000  19.000000
'''
b.describe()[2]
'''
count     4.000000
mean      9.500000
std       6.454972
min       2.000000
25%       5.750000
50%       9.500000
75%      13.250000
max      17.000000
Name: 2, dtype: float64
'''
b.describe()[2]['max']
'''
17.0
'''
#b.describe().ix['max'] # ix过时了，现在用loc
b.describe().loc['max']
'''
0    15.0
1    16.0
2    17.0
3    18.0
4    19.0
Name: max, dtype: float64
'''
```

## 数据的累计统计分析

对数据的前n项进行累计运算，累和之类的

| 方法         | 说明                  |
| ------------ | --------------------- |
| `.cumsum()`  | 依次给出前n项和       |
| `.cumprod()` | 依次给出前n项乘积     |
| `.cummax()`  | 依次给出前n项的最大值 |
| `.cummin()`  | 依次给出前n项的最小值 |



```python
#生成demo
import pandas as pd
import numpy as np

b = pd.DataFrame(np.arange(20).reshape(4,5), index=['c','a','d','b'])

''' >> b
    0   1   2   3   4
c   0   1   2   3   4
a   5   6   7   8   9
d  10  11  12  13  14
b  15  16  17  18  19
'''
```

```python
b.cumsum()
'''
    0   1   2   3   4
c   0   1   2   3   4
a   5   7   9  11  13
d  15  18  21  24  27
b  30  34  38  42  46
'''
```

滚动计算

| 方法                         | 说明                    |
| ---------------------------- | ----------------------- |
| `.rolling(w).sum()`          | 依次计算相邻w个元素之和 |
| `.rolling(w).mean()`         | 算术平均值              |
| `.rolling(w).var()`          | 方差                    |
| `.rolling(w).std()`          | 标准差                  |
| `.rolling(w).min()` `.max()` | 最小值，最大值          |

**前(w-1)行的值会变成NaN**

```python
b.rolling(2).sum()
'''
      0     1     2     3     4
c   NaN   NaN   NaN   NaN   NaN
a   5.0   7.0   9.0  11.0  13.0
d  15.0  17.0  19.0  21.0  23.0
b  25.0  27.0  29.0  31.0  33.0
'''
b.rolling(3).sum()
'''
      0     1     2     3     4
c   NaN   NaN   NaN   NaN   NaN
a   NaN   NaN   NaN   NaN   NaN
d  15.0  18.0  21.0  24.0  27.0
b  30.0  33.0  36.0  39.0  42.0
'''
```

## 数据的相关分析

相关性的简单描述

- x↑y↑，正相关
- x↓y↑，负相关
- x↑y无所谓，不相关

统计学中，用协方差公式来判断两个变量的相关性
$$
cov(X,Y) = \frac{\sum_{i=1}^{n}(X_i-\overline{X})(Y_i-\overline{Y})}{n-1}
$$
$\overline{X}$ 表示均值

若$cov(X,Y)>0$，X和Y正相关

若$cov(X,Y)<0$，X和Y负相关

若$cov(X,Y)=0$，X和Y独立无关

Pearson相关系数
$$
r = \frac{\sum_{i=1}^{n}(x_i-\widetilde{x})(y_i-\widetilde{y})}{\sqrt{\sum_{i=1}^{n}(x_i-\widetilde{x})^2}\sqrt{\sum_{i=1}^{n}(y_i-\widetilde{y})^2}}
$$
$r\in[-1,1]$

- $|r|\in[0.8,1]$极强相关
- $|r|\in[0.6,0.8]$强相关
- $|r|\in[0.4,0.6]$中等相关
- $|r|\in[0.2,0.4]$弱相关
- $|r|\in[0,0.2]$极弱相关或不相关

相关分析函数

| 方法      | 说明                                               |
| --------- | -------------------------------------------------- |
| `.cov()`  | 计算协方差矩阵                                     |
| `.corr()` | 计算相关系数矩阵，Pearson、Spearman、Kendall等系数 |

### 例子：房价与m2系数的相关性分析

```python
import pandas as pd
house_price = pd.Series([3.04, 22.93, 12.75, 22.6, 12.33], index=['2008','2009','2010','2011','2012'])
m2 = pd.Series([8.18, 18.38, 9.13, 7.82, 6.69], index=['2008','2009','2010','2011','2012'])
house_price.corr(m2) # 相关性系数
'''
0.5239439145220387
'''
```

绘图部分

说明pandas的Series类型是可以当做numpy的一维ndarray来用的。而且它会自动把x轴坐标用index的值来显示。

```python
import matplotlib.pyplot as plt
plt.plot(house_price, color='red', marker='o',label='house_price')
plt.plot(m2, color='blue', marker='^',label='m2')
legend = plt.legend(loc='lower right') # 图例
```

![相关性系数](笔记插图/pandas/相关性系数.png)

## 自测

创建

查看

重排

删除

运算

排序

统计

```python

```

# 川流

> 知识的从无到有其实是一个造海的过程。
>
> 先是挖矿，即知道有这么一个知识。
>
> 然后灌水，即掌握知识。
>
> 最后是不断的引流，扩大这片海。

学习了pandas但是还是不太会应用，应该举个例子实战一下。在实际操作中，会给你个CSV格式的表格，然后再用pandas进行处理。

我能想到的操作：

增加，删除某一列/行√

行列的四则运算√

按照行列拆分表格√

按照属性拆分表格比如把表格中所有男生单独拎出来放到另外一个表格。√

### 实际运用pandas处理数据时的疑问

- 怎么显示所有特征，即不要有省略

- 想查看第19个特征列怎么看

  `df[df.columns[19]]`

- [pandas随机获取DataFrame中的数据](https://blog.csdn.net/weixin_41789707/article/details/80930274)

  `df.sample(5)`



## read_csv()参数详解

 [pandas.read_csv参数详解](https://www.cnblogs.com/datablog/p/6127000.html)

`skiprows=1` 跳过文件的第一行

## low_memory = False

[pandas read_csv mixed types问题](https://www.jianshu.com/p/a70554726f26)

> low_memory=False 参数设置后，pandas会一次性读取csv中的所有数据，然后对字段的数据类型进行唯一的一次猜测。这样就不会导致同一字段的Mixed types问题了。
> 但是这种方式真的非常不好，一旦csv文件过大，就会内存溢出；