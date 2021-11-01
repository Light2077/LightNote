如图，要想获取seaborn绘制的密度曲线（下图的蓝线）的具体数值

```python
import numpy as np
import seaborn as sns

x = np.random.randn(100)
sns.kdeplot(x)
```

![获取kde曲线1](img/获取kde曲线1.png)

首先要接收kdeplot()的返回值，返回的是一个[`matplotlib.axes.Axes`](https://matplotlib.org/stable/api/axes_api.html#matplotlib.axes.Axes)对象

```python
ax = sns.kdeplot(x)
```

然后调用`get_children()`方法，返回一个列表，里面是这张图里的各个部件

```python
ax.get_children()
```

```
[<matplotlib.lines.Line2D at 0x2ac91765dc8>,
 <matplotlib.spines.Spine at 0x2ac91741108>,
 <matplotlib.spines.Spine at 0x2ac91741608>,
 <matplotlib.spines.Spine at 0x2ac917418c8>,
 <matplotlib.spines.Spine at 0x2ac91970948>,
 <matplotlib.axis.XAxis at 0x2ac91500f88>,
 <matplotlib.axis.YAxis at 0x2ac917419c8>,
 Text(0.5, 1.0, ''),
 Text(0.0, 1.0, ''),
 Text(1.0, 1.0, ''),
 <matplotlib.patches.Rectangle at 0x2ac91737308>]
```

获取其中第一个对象[`matplotlib.lines.Line2D`](https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html?highlight=line2d#matplotlib.lines.Line2D)，并调用其`get_ydata()`方法就获取了密度曲线的具体数值了

```python
line = ax.get_children()[0]
y = line.get_ydata()
```

PS：此外也可以调用`get_xdata()`得到的值就是一开始使用的`x`