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

### 像素点转为数值

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import BboxTransform, Bbox


def plot(rects):
    # 采样率是
    # 10000
    fig, ax = plt.subplots(figsize=(3, 3))
    # 0-150通道 10秒
    ax.imshow(np.random.randn(976, 140), extent=(0, 140, 10, 0))
    ax.axis('auto')
    transform = BboxTransform(
        Bbox.from_extents(0, 976, 140, 0), 
        ax.bbox,
    )
    for left, bottom, width, height in rects:
        print(left, bottom, width, height)
        rect = plt.Rectangle((left, bottom), width, height, ec='r', fc='None', transform=transform)
        ax.add_patch(rect)
    plt.show()
    return ax, transform
```

```python
# 异常检测结果

# 帧起始和结束
frame_start = 200
frame_end = 500
channel_start = 100
channel_end = 120

frame_diff = frame_end - frame_start
channel_diff = channel_end - channel_start

rects = [(channel_start, frame_end, channel_diff, frame_diff)]
ax, transform = plot(rects)
transform_r = transform.inverted()
```

```python
# 中间过程会得到这个矩形框的具体像素位置
left, bottom = transform.transform([channel_start, frame_end])
right, top = transform.transform([channel_end, frame_start])

width = right - left
height = top - bottom
print(left, right, bottom, top)
print(width, height)
```

```python
# 左 下 右 上
print('ax.bbox.bounds:', ax.bbox.bounds)
print('自定义:', Bbox.from_extents(0, 10000, 140, 0).bounds)
```

```python
# 最终要根据这个框的像素位置还原到时间点。时间: 0-100000, 通道: 0-140
# 小的数向下取整，大的数向上取整
transform2 = BboxTransform(
    ax.bbox,
    Bbox.from_extents(0, 100000, 140, 0), 
)
```

```python
channel_start, point_start = transform2.transform([left, top])
channel_end, point_end = transform2.transform([right, bottom])
print(channel_start, channel_end, point_start, point_end)
```

