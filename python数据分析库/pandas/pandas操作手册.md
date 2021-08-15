这是个按照pandas使用流程来写的操作手册。

pandas是用来处理数据的python工具包，我的理解中，pandas是底层版的excel，它可以实现的功能更多，但是也比excel更麻烦。excel可能动动鼠标就完成一个工作了，但是pandas需要编写相应的代码。

这里的函数相关介绍都只是部分的，是个人感觉经常会用到的，具体的介绍点击链接查看官方文档。

[官方文档](https://pandas.pydata.org/pandas-docs/stable/index.html)

# 1 创建pandas数据类型

也不一定是什么情况都是要读取数据的，有时候我们可能自己要创建一个数据。

pandas有两个数据类型：`Series`和`DataFrame`。分别是带标签的一维和二维数组。

## 1.1 创建Series

[`pd.Series()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html?highlight=series)

创建后会自动生成[0-N]的索引，每一行对应一个数据。

<font color=f05b72>**data **</font>:数组，字典，标量

<font color=f05b72>**index**</font>: array-like or Index (1d)

长度一般要和data一致，最后数据的长度和index挂钩。index 长于 data，多出来的索引对应数据为空值。index 短于 data，数据会变少。

```python
import pandas as pd
s = pd.Series([1,2,3,4],index=['a','b','c','d'])
```

## 1.2 创建DataFrame

[`pd.DataFrame()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html?highlight=dataframe)

<font color=f05b72>**data**</font>: 2维数组或字典

可以用2维数组来生成DataFrame，也可以用字典（<font color='224b8f'>**键对应列名，值是一个Series或list**</font>）。

<font color=f05b72>**index**</font> : Index or array-like

行索引的名字，长度等同于行数。

<font color=f05b72>**columns**</font>: Index or array-like

选择使用data哪几列，没选中的列就忽略了。如果还没有列名，可以用数字，比如：[0,2,4]。

**使用方法举例**

```python
import pandas as pd

data = {'name': ['Lily','Amy','Peter','Jack', 'Alex'],
        'sex': ['female','female','male','male','male'],
        'height': [168.7, 172.3, 175.4, 180.9, 169.4],
        'weight': [51.5, 49.8, 63.2, 77.8, 61.6],
        'health': [True, False, True, True, True]}

index=['c1','c2','c3','c4','c5'] # 行索引
df1 = pd.DataFrame(data,index)

	name	sex		height	weight	health
c1	Lily	female	168.7	51.5	True
c2	Amy		female	172.3	49.8	False
c3	Peter	male	175.4	63.2	True
c4	Jack	male	180.9	77.8	True
c5	Alex	male	169.4	61.6	True

columns=['name','sex','weight','health'] # 忽略了身高这一列
df2 = pd.DataFrame(df1,columns=columns)

	name	sex		weight	health
c1	Lily	female	51.5	True
c2	Amy		female	49.8	False
c3	Peter	male	63.2	True
c4	Jack	male	77.8	True
c5	Alex	male	61.6	True
```

<font color='7fb801'>**如何给行索引命名?**</font>

`df.index.name = 'hello'`

**自测**

- 怎么生成Series(1)
- 怎么生成DataFrame(1)
- df中选择性生成列(1)
- 怎么设置行/列索引(2)

# 2 数据输入输出

pandas可以读取各种各样数据格式的文件，如CSV、Excel、HTML等。**主要掌握读取CSV文件即可**。

官方文档：[IO tools:pandas文件输入输出](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html)

## 2.1 CSV文件的存储

默认会保存行列索引

[`pandas.DataFrame.to_csv()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html?highlight=to_csv#pandas.DataFrame.to_csv)

[`pandas.Series.to_csv()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_csv.html?highlight=to_csv#pandas.Series.to_csv)

这里就只介绍第一个了。

<font color=f05b72>**sep**</font> : 字符串

`sep=','`：默认为逗号分割。

<font color=f05b72>**na_rep**</font> : 字符串

`na_rep=''`：填充空缺值，默认不填充。

<font color=f05b72>**float_format**</font> : 字符串

`float_format=None`：默认不对浮点数格式化。
`float_format='%.2f'`：浮点数格式化为小数点后两位。

<font color=f05b72>**columns**</font> : 序列

填列表，列表元素为数字或字符串。
要保存哪几列。

<font color=f05b72>**header**</font> : 布尔\列表\字符串，默认True

`header=True`：默认保存列索引。
`header=False`：**不保存列索引。**
如果填列表，修改当前的列索引，用自己自定义的列索引并储存。长度要和列数一致。

<font color=f05b72>**index**</font> : 布尔，默认True

`index=True`：默认保存行索引。
是否保存行索引，感觉上一般不保存。

<font color=f05b72>**date_format**</font> : 字符串，默认无

(暂时保留个位置，目前还用不到。)
Format string for datetime objects.

```python
df.to_csv(path,
          sep=',', # 分隔符
          float_format='%.2f', # 浮点数格式化
          columns=None, # 默认保存所有列
          header=False, # 不保存列索引
          index=False # 不保存行索引
         )
```

**自测**

- 空缺值填充(1)
- 浮点数格式化(1)
- 选择性保存列(1)
- 是否保存行/列索引(2)

## 2.2 CSV文件读取

[pandas.read_csv参数详解(中文版)](https://www.cnblogs.com/datablog/p/6127000.html)

这里只列出了个人觉得比较常用的几个参数，具体参数及作用查看链接。

[`pandas.read_csv()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html#pandas.read_csv)

```python
import pandas as pd
pd.read_csv( "//path/table.csv",
            sep=',', # 以逗号分隔数据
            header=0, # 以第0行为列名
            names=None, # 不自定义列名
            index_col=0, # 以第0列为行索引
            usecols=[1,3,5], # 只读取第1,3,5列
            skiprows=2, # 跳过两行（不读取第1第2行）
            nrows=10, # 只读取前10行
)
```

<font color=f05b72>**sep**</font> : str

`sep=','`：默认为逗号分割。

<font color='f05b72'>**header** </font>: int or list of ints

`header='infer'`：默认第一行是列索引。
`header=None`：没有列索引，会读取全部行，且自动生成[0-N]的列索引。
`header=3`：就是以第3行为列索引，且DataFrame从第五行开始。
`header=[0,3]`：以第0,3行为列索引（多级标题），数据从第3行开始。

<font color='f05b72'>**names**</font> : array-like, optional

传一个等同于数据列数的列表，会读取全部行，然后按照这个列表给列索引赋值。

<font color='f05b72'>**index_col** </font>: int or sequence or False

`index_col=None`：默认自动生成[0-N]的行索引。
`index_col=0`：第0列作为行索引。

<font color='f05b72'>**usecols** </font>: array-like, optional

默认读取全部列，可以自己设定读取那几列。
`usecols=[1,5,8]`：读取第1,5,8列。
`usecols=['aplle','pear','banana']`：读取对应列名的列。
顺序是固定的，根据源文件的排列顺序。

<font color='f05b72'>**skiprows** </font>: list-like or integer, optional

`skiprows=2`：跳过两行（不读取第1第2行）。
需要忽略的行数（从文件开始处算起），或需要跳过的行号列表（从0开始）。

<font color='f05b72'>**nrows**</font> : 整型

`nrows=None`：默认读取所有行。
`nrows=10`：只读取前10行，不包括列索引行。
需要读取的行数（从文件头开始算起）。

**自测**

- 列索引的处理（2）
- 行索引的设置/选择**索引列**（1）
- 列的选择性读取（1）
- 行的跳过与数量设定（2）

## 2.3 excel文件读取

[`pd.read_excel(PATH, sheet_name=''`)](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-excel-reader)

# 3 操作数据

## 了解数据

`df.shape` 
`df.head()` 
`df.info()` 
`df.describe()` 

## 数据列的操作

| 方法                                                         | 说明         |
| ------------------------------------------------------------ | ------------ |
| [`df.loc[2]`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html?highlight=loc#pandas.DataFrame.loc) | 查看一行     |
| `df.loc[:,'Age']` `df['Age']`                                | 查看一列     |
| `df['Age'][2]`                                               | 查看某个数据 |
| [`df.drop(2)`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html?highlight=drop#pandas.DataFrame.drop) | 删除一行     |
| `df.drop(['Name'],axis=1)`                                   | 删除一列     |
| [`df.reindex(columns=[])`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reindex.html?highlight=reindex#pandas.DataFrame.reindex) | 重排列索引   |
| `df.reindex(index=[])`                                       | 重排行索引   |
|                                                              |              |
|                                                              |              |

增加一行

增加一列


移动列

移动行



更改列索引名称

`df.rename(columns={'old1':'new1', 'old2':'new2')`

更改行索引名称

`df.index.name='index name'`

排序
`df.sort_index(axis=0,ascending=True)`对行索引排序，升序
`df.sort_values('Age')`对指定行或列排序
`df.sort_values('Age', axis=0, ascending=True)`对一列数据升序

## DataFrame的属性

把df转成2维ndarray数组

`df.values`

查看行索引

`df.index`
`df.index[6]` 查看第6个行索引名称

查看列索引

`df.columns` 
`df.columns[6]` 查看第4个列索引名称

[pandas随机获取DataFrame中的数据](https://blog.csdn.net/weixin_41789707/article/details/80930274)

`df.sample(5)`

选出指定数据类型的数据



## 数据统计分析

| 基本统计分析方法                                    | 说明                            |
| --------------------------------------------------- | ------------------------------- |
| `.sum()`                                            | 计算数据的总和，按0轴计算，下同 |
| `.count()`                                          | 非NaN值的数量                   |
| `.mean()` `.median()`                               | 计算数据的算术均值，算术中位数  |
| `.var()` `.std()`                                   | 计算数据的方差、标准差          |
| `.min()` `.max()`                                   | 计算数据的最小最大值            |
| `.describe()`<font color='orange'>**(常用)**</font> | 对0轴（各列）的统计汇总         |



| 仅适用于Series类型的方法 | 说明                                       |
| ------------------------ | ------------------------------------------ |
| `.argmin()` `.argmax()`  | 计算最大值、最小值所在位置的**自动**索引   |
| `.idxmin()` `.idxmax()`  | 计算最大值、最小值所在位置的**自定义**索引 |



| 累积统计分析 | 说明                                 |
| ------------ | ------------------------------------ |
| `.cumsum()`  | 依次给出前n项和，大小等同于DataFrame |
| `.cumprod()` | 依次给出前n项乘积                    |
| `.cummax()`  | 依次给出前n项的最大值                |
| `.cummin()`  | 依次给出前n项的最小值                |



| 滚动计算方法                 | 说明                    |
| ---------------------------- | ----------------------- |
| `.rolling(w).sum()`          | 依次计算相邻w个元素之和 |
| `.rolling(w).mean()`         | 算术平均值              |
| `.rolling(w).var()`          | 方差                    |
| `.rolling(w).std()`          | 标准差                  |
| `.rolling(w).min()` `.max()` | 最小值，最大值          |



| 相关分析        | 说明                                               |
| --------------- | -------------------------------------------------- |
| `.cov(Series)`  | 计算协方差矩阵                                     |
| `.corr(Series)` | 计算相关系数矩阵，Pearson、Spearman、Kendall等系数 |

## Index类型的相关操作

| 方法                 | 说明                               |
| -------------------- | ---------------------------------- |
| `.insert(loc,e)`     | 在loc位置增加一个元素e             |
| `.delete(loc)`       | 删除loc位置处的元素                |
| `.append(idx)`       | 连接另一个Index对象，产生新的Index |
| `.diff(idx)`         | 计算差集，产生新的Index            |
| `.intersection(idx)` | 计算交集                           |
| `.union(idx)`        | 计算并集                           |

## 施工中













字体颜色快捷区

</font>

<font color='224b8f'>**琉璃绀：表示强调**</font>

<font color='224b8f'>

<font color='orange'>**橙色：表示重要**</font>

<font color='orange'>

<font color='f05b72'>**蔷薇色：醒目**</font>

<font color='f05b72'>

<font color='7fb801'>**若緑：疑惑**</font>

<font color='7fb801'>

[Typora-Emoji参考链接](https://blog.todaycoder.cn/2018/11/18/Typora-Emoji/)

```python

```





























