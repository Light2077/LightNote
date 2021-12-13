## 导包

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
```

**加载图片**

```python
image = load_sample_image("flower.jpg")
plt.imshow(image)
```

![](./img/flower.png)

**图片归一化**

```python
# 图片归一化 0 - 255 -> 0 - 1
image = np.array(image, dtype=np.float64) / 255
```

**把图片拉成1维**

```python
# 宽 高 深（颜色通道数）
w, h, d = image.shape
image_array = np.reshape(image, (w * h, d))
image_array.shape  # (273280, 3)
```

**构建训练集并训练kmeans模型**

这里没有使用所有的数据

```python
# 构建训练集（采样）
image_array_sample = shuffle(image_array, random_state=0)[:1000]
# 找出10个颜色中心
kmeans = KMeans(n_clusters=10, random_state=0).fit(image_array_sample)
```

**像素归类并重建图像**

```python
# 把所有的像素归类（和哪个颜色接近就归到那一类）
labels = kmeans.predict(image_array)

# 重建图像
# cluster_centers_ 的个数取决于 n_clusters
new_image = kmeans.cluster_centers_[labels].reshape([w, h, d])
plt.imshow(new_image)
```

![](./img/flower2.png)