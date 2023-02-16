绘制圆柱体

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义圆柱体的高度
height = 5

# 定义圆柱体的半径
radius = 1

# 圆柱体顶部的圆心坐标
center = [0, 0, height/2]

# 圆柱体底部的圆心坐标
center_bottom = [0, 0, -height/2]

# 生成等分的角度
theta = np.linspace(0, 2 * np.pi, 100)

# 计算x、y坐标
x = center[0] + radius * np.cos(theta)
y = center[1] + radius * np.sin(theta)
z = np.zeros_like(x) + center[2]

# 生成顶面图形
x_top = np.concatenate([x, x])
y_top = np.concatenate([y, y])
z_top = np.concatenate([z, z + height])

# 生成侧面图形
x_side = np.concatenate([x, x])
y_side = np.concatenate([y, y])
z_side = np.concatenate([z, z + height])

# 生成底面图形
x_bottom = center_bottom[0] + radius * np.cos(theta)
y_bottom = center_bottom[1] + radius * np.sin(theta)
z_bottom = np.zeros_like(x_bottom) + center_bottom[2]

# 创建图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制顶面图形
ax.plot(x_top, y_top, z_top, 'b')

# 绘制侧面图形
ax.plot(x_side, y_side, z_side, 'g')

# 绘制底面图形
ax.plot(x_bottom, y_bottom, z_bottom, 'r')

# 设置图形属性
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

```

