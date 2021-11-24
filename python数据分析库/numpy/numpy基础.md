# Numpy基本介绍

Python开源的科学计算工具包

高级的数值编程工具

- 强大的N维数组对象：ndarray
- 对数组结构数据进行运算（不用遍历循环）
- 随机数、线性代数、傅里叶变换等功能



Numpy要学什么？

- 基础数据结构
- 通用函数
- 索引及切片
- 随机数
- 数据的输入输出

参考网站：

- numpy中文网：https://www.numpy.org.cn/
- numpy官方网站：https://numpy.org/doc/stable/

# Numpy数组创建

NumPy数组是一个多维数组对象，称为ndarray。其由两部分组成：
① 实际的数据
② 描述这些数据的元数据

常用的数组属性如下

| 数组属性 | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| ndim     | 输出数组维度的个数（轴数），或者说“秩”，维度的数量也称rank   |
| shape    | 数组的维度，对于n行m列的数组，shape为（n，m）                |
| size     | 数组的元素总数，对于n行m列的数组，元素总数为n*m              |
| dtype    | 数组中元素的类型，类似type()（注意了，type()是函数，.dtype是方法） |
| itemsize | 数组中每个元素的字节大小，int32类型字节为4，float64的字节为8 |
| data     | 包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。 |

```python
import numpy as np
# 生成一个数组
a = np.array([1,2,3,4,5,6,7])

print(a)          # [1,2,3,4,5,6,7]
print(a.ndim)     # 1
print(a.shape)    # (7,)
print(a.size)     # 7
print(a.dtype)    # int32
print(a.itemsize) # 4
print(a.data)     # <memory at 0x0000000005927108>
```

## [numpy.arange()](https://numpy.org/doc/stable/reference/generated/numpy.arange.html?highlight=arange#numpy.arange)

```python
numpy.arange([start, ]stop, [step, ]dtype=None, *, like=None)
```

给定间隔内返回均匀间隔的值

```python
import numpy as np
print(np.arange(5))  # [0 1 2 3 4]
print(np.arange(5.0))  # [0. 1. 2. 3. 4.]
print(np.arange(4, 10))  # [4 5 6 7 8 9]
print(np.arange(4.0, 10, 2))  # [4. 6. 8.]
```

## [numpy.linspace()](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html?highlight=linspace#numpy.linspace)

按照设定数均匀切分指定间隔

```python
numpy.linspace(start, stop, num=50, endpoint=True, 
               retstep=False, dtype=None, axis=0)
```

- endpoint: 是否包含stop，默认生成的数组最后一个数就是stop
- retstep：用于查看步长，如果为True，则返回（样本，步长），其中步长是样本之间的间距。

```python
import numpy as np

np.linspace(2.0, 3.0, num=5)
# array([2.  , 2.25, 2.5 , 2.75, 3.  ])

np.linspace(2.0, 3.0, num=5, endpoint=False)
# array([2. , 2.2, 2.4, 2.6, 2.8])

a, step = np.linspace(2.0, 3.0, num=5, retstep=True)
print('array:', array, 'step:', step)
# array: [2.   2.25 2.5  2.75 3.  ] step: 0.25
```

## [numpy.zeros()](https://numpy.org/doc/stable/reference/generated/numpy.zeros.html)

```python
numpy.zeros(shape, dtype=float, order='C', *, like=None)
```

返回全0数组

- dtype：数据类型，默认numpy.float64
- order：是否在存储器中以C或Fortran连续（按行或列方式）存储多维数据。

```python
import numpy as np
np.zeros(5)
# [0. 0. 0. 0. 0.]  默认是float64

np.zeros((2, 2), dtype=np.int)
# [[0 0]
#  [0 0]]
```

## [numpy.zeros_like()](https://numpy.org/doc/stable/reference/generated/numpy.zeros_like.html)

```python
numpy.zeros_like(a, dtype=None, order='K', subok=True, shape=None)
```

返回与给定数组具有相同形状和类型的全零数组。

```python
import numpy as np
a = np.array([[1, 2, 3],
              [4, 5, 6]])

np.zeros_like(a)
# [[0 0 0]
#  [0 0 0]]
```

## [numpy.ones()](https://numpy.org/doc/stable/reference/generated/numpy.ones.html)

```python
numpy.ones(shape, dtype=None, order='C', *, like=None)
```

返回全0数组，类似`numpy.zeros()`

```python
import numpy as np

np.ones(5)
# [1. 1. 1. 1. 1.]  默认是float64

np.ones((2, 2), dtype=np.int)
# [[1 1]
#  [1 1]]
```

## [numpy.ones_like()](https://numpy.org/doc/stable/reference/generated/numpy.ones_like.html)

```python
numpy.ones_like(a, dtype=None, order='K', subok=True, shape=None)
```

返回与给定数组具有相同形状和类型的全零数组。

```python
import numpy as np
a = np.array([[1, 2, 3],
              [4, 5, 6]])

np.ones_like(a)
# [[1 1 1]
#  [1 1 1]]
```

## [numpy.eye()](https://numpy.org/doc/stable/reference/generated/numpy.eye.html)

```python
numpy.eye(N, M=None, k=0, dtype=<class 'float'>, order='C', *, like=None)
```

返回一个二维单位阵

- N：矩阵行数
- M：矩阵列数，默认和行数相同
- k：0（默认）表示主对角线，正值表示上对角线，负值表示下对角线

```python
np.eye(2, dtype=int)
# array([[1, 0],
#        [0, 1]])

np.eye(3, k=1)
# array([[0.,  1.,  0.],
#        [0.,  0.,  1.],
#        [0.,  0.,  0.]])

np.eye(2, 3)
# array([[1., 0., 0.],
#        [0., 1., 0.]])
```

## dtype设置

| 数据类型             | 说明                                             |
| -------------------- | ------------------------------------------------ |
| bool                 | 用一个字节存储的布尔类型（True或False）          |
| inti                 | 由所在平台决定其大小的整数（一般为int32或int64） |
| int8 ~ int64         | 整形                                             |
| uint8 ~ uint64       | 无符号整形                                       |
| float16 ~ float64    | 浮点数                                           |
| complex64            | 复数，分别用两个32位浮点数表示实部和虚部         |
| complex128 / complex | 复数，分别用两个64位浮点数表示实部和虚部         |

> 2 ** 32大约为42亿
>
> 因此有符号整形范围大概在负21亿到正21亿之间

# Numpy通用函数

- 数组改变
  - 转置：[numpy.ndarray.T](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html)
  - 重塑：[numpy.reshape](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html)
  - [numpy.resize](https://numpy.org/doc/stable/reference/generated/numpy.resize.html)
  - 排序：[numpy.sort](https://numpy.org/doc/stable/reference/generated/numpy.sort.html)
- 数组复制
  - [numpy.copy](https://numpy.org/doc/stable/reference/generated/numpy.copy.html)
- 数组类型转换
  - [numpy.ndarray.astype](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html)
- :star:数组堆叠
  - [numpy.hstack](https://numpy.org/doc/stable/reference/generated/numpy.hstack.html)
  - [numpy.vstack](https://numpy.org/doc/stable/reference/generated/numpy.vstack.html)
  - [numpy.stack](https://numpy.org/doc/stable/reference/generated/numpy.stack.html)
- 数组拆分
  - [numpy.hsplit](https://numpy.org/doc/stable/reference/generated/numpy.hsplit.html)
  - [numpy.vsplit](https://numpy.org/doc/stable/reference/generated/numpy.vsplit.html)
  - [numpy.split](https://numpy.org/doc/stable/reference/generated/numpy.split.html)
- 数组简单运算
  - 加减乘除，幂运算（均为点对点运算）
- 矩阵运算
- 数组统计计算
  - 求和：[numpy.sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html)
  - 均值：[numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)
  - 最大值：[numpy.max](https://numpy.org/doc/stable/reference/generated/numpy.max.html)
  - 最小值：[numpy.min](https://numpy.org/doc/stable/reference/generated/numpy.min.html)
  - 标准差：[numpy.std](https://numpy.org/doc/stable/reference/generated/numpy.std.html)
  - 方差：[numpy.var](https://numpy.org/doc/stable/reference/generated/numpy.sum.html)

## 数组改变

### [numpy.ndarray.T](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html)

```python

```



```python

```

### [numpy.reshape](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html)

```python

```



```python

```

## 数组拼接

vstack，hstack与stack的差异

hstack——横向连接

vstack——纵向连接

hstack连接一维数组时不改变数组维度

hstack, vstack连接二维矩阵时不改变数组维度

```python
import numpy as np
# hstack 连接一维数组不改变维度（仍是1维数组）
a = np.array([1, 1, 1])
b = np.array([2, 2, 2])
np.hstack([a, b])  # 同np.r_[a, b]
```

```
array([1, 1, 1, 2, 2, 2])
```



```python
# vstack 连接一维数组使维度+1
a = np.array([1, 1, 1])
b = np.array([2, 2, 2])
np.vstack([a, b])  # 同np.c_[a, b]
```

```python
array([[1, 1, 1],
       [2, 2, 2]])
```



```python
# hstack 和 vstack连接二维数组不改变维度
a
```



### numpy.stack

```python

```

# Numpy索引及切片

## 基本索引

### 一维数组

```python
import numpy as np

a = np.array([0, 1, 2, 3, 4, 5, 6])
print(a[1])  # 1
print(a[2:5])  # [2 3 4]
```

### 二维数组

```python
import numpy as np
a = np.array([[0, 1,  2,  3],
              [4, 5,  6,  7],
              [8, 9, 10, 11]])
print(a[1])  # [4 5 6 7]
print(a[1][2])  # 6

print(a[1:3])
# [[ 4  5  6  7]
#  [ 8  9 10 11]]

print(a[1,2])  # 6
print(a[:2, 2:])
# [[2 3]
#  [6 7]]
```

### 三维数组

```python
import numpy as np
a = np.array([[[0, 1],
               [2, 3]],

              [[4, 5],
               [6, 7]]])

print(a[0])
# [[0 1]
#  [2 3]]

print(a[0][1])
# [2 3]

print(a[0][1][1])
# 3
```

## 布尔索引

```python
import numpy as np
a = np.array([[0, 1,  2,  3],
              [4, 5,  6,  7],
              [8, 9, 10, 11]])

row = [False, True, True]
col = [True, False, False, True]

print(a[row, :])
# [[ 4  5  6  7]
#  [ 8  9 10 11]]

print(a[:, col])
# [[ 0  3]
#  [ 4  7]
#  [ 8 11]]

# 元素级别的布尔索引
m = ar > 5
print(m)
# [[False False False False]
#  [False False  True  True]
#  [ True  True  True  True]]

print(a[m])
# [ 6  7  8  9 10 11]
# pandas判断方式原理就来自于此
```

## 数组值更改

更改切片值，会影响原数组的值

```python
import numpy as np
a = np.array([0, 0, 0, 0, 0])
a[0] = 2
print(a) #  [2 0 0 0 0]

a[1:4] = 3
print(a)  # [2 3 3 3 0]
```

# Numpy随机数

## [numpy.random.rand](https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html)

0到1之间的均匀分布

```python
# numpy.random.rand(d0, d1, ..., dn)

a = np.random.rand()
print(a)  # 0.08662996124854716

b = np.random.rand(4)
print(b)
# [0.56127236 0.61652471 0.96384302 0.57430429]

c = np.random.rand(2, 3)
print(c)  
# [[0.37116085 0.45214524 0.20185025]
#  [0.56930512 0.19509597 0.58370402]]
```

## [numpy.random.randn](https://numpy.org/doc/stable/reference/random/generated/numpy.random.randn.html)

标准正态分布，均值为0，标准差为1

```python
a = np.random.randn()
# 同rand
```

## [numpy.random.randint](https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html)

```python
random.randint(low, high=None, size=None, dtype=int)
```

返回随机整数数组，返回的数组**不包括**`high`

```python
# 返回[0, 2) 的整数
print(np.random.randint(2))
# 1

# 一维随机整数
print(np.random.randint(2), size=4)
# [0 0 0 1]

# 二维随机整数
print(np.random.randint(1, 4), size=(2, 3))
# [[3 2 3]
#  [3 1 3]]
```

## [numpy.random.uniform](https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html)

```python
random.uniform(low=0.0, high=1.0, size=None)
```

指定范围的均匀分布

```python
import numpy as np
np.random.uniform(1, 3, size=(2, 3))
# array([[2.0550718 , 2.11168362, 1.78924032],
#        [1.833848  , 1.50211867, 2.61027538]])
```

## [numpy.random.normal](https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html)

```python
random.normal(loc=0.0, scale=1.0, size=None)
```

指定均值和标准差的正态分布
$$
p(x)=\frac{1}{\sqrt{2\pi \sigma^2}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$

```python
import numpy as np
np.random.normal(1, 3, size=(2, 3))  # 均值为1， 方差为3
# array([[ 2.26646449, -0.9124344 , -1.25082677],
#        [ 4.93236361,  2.94895804,  5.42090783]])
```



# Numpy输入输出

## [np.save](https://numpy.org/doc/stable/reference/generated/numpy.save.html) / [np.load](https://numpy.org/doc/stable/reference/generated/numpy.load.html)

这个是按照numpy特有的格式保存的，无法用文本文件读取

```python
import numpy
a = np.arange(4)

# 保存
np.save('a.npy', a)

# 读取
b = np.load('a.npy')

print(a)  # [0 1 2 3]
print(b)  # [0 1 2 3]
```

## [np.savetxt](https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html) / [np.loadtxt](https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html)

这个可能用得比较多，从文本文件读取或保存数组

```python
numpy.savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)

numpy.loadtxt(fname, dtype=<class 'float'>, comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0, encoding='bytes', max_rows=None, *, like=None)
```

主要的参数：

- fmt：保存的格式，`%.4f`保存4位小数点
- delimiter：分隔符

```python
import numpy
a = np.array([[0, 1,  2,  3],
              [4, 5,  6,  7],
              [8, 9, 10, 11]])

# 保存
np.savetxt('a.csv', a, delimiter=',')

# 读取
b = np.loadtxt('a.csv', delimiter=',')
```

