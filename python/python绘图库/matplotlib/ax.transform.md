transform的作用就是把数据点映射到像素点上。

```python
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(3,3))
ax.plot(range(5))
plt.show()

print('像素边界:', ax.bbox.bounds)
print('数据点映射:', ax.transData.transform((2, 2)))
print('坐标轴映射:', ax.transAxes.transform((0.5, 0.5)))
```

通过transform，使得绘制的图像自动适配

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import BboxTransform, Bbox


fig, ax = plt.subplots(figsize=(7,8))
ax.imshow(np.random.randn(30, 50), extent=(0, 1000, -2, 3))
ax.axis('auto')
transform = BboxTransform(
    Bbox.from_extents(0, 0, 2, 2), 
    ax.bbox,
)
rect = plt.Rectangle((0.5, 0.5), 1, 1, ec='r', fc='None', transform=transform)
ax.add_patch(rect)
plt.show()
```

获取逆变换的transform

```python
transData_r = ax.transData.inverted()
# 输入像素点，转换为数据
transData_r.transform([100, 100])
```

