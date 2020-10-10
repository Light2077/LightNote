# new

记录新知，留待整理进总的仓库。



pickle真是太好用了

```python
import pickle

# 保存
with open('filename.pickle', 'wb') as f:
    pickle.dump(<anything>, f)
    
# 加载
with open('filename.pickle', 'rb') as f:
    name = pickle.load(f)
```



json：

- 字典转为字符串：`json.dumps(dict)`
- 字符串转字典：`json.loads(str)`
- 字典写入json文件：`json.dump(dict)`
- 读json文件转成字典：`json.load(json)`



numpy

打乱一个数组

随机取数组中的5个元素

矩阵分解运算的标准库：

- 如何求对角线元素和：`np.trace`
- 如何计算行列式：`np.linalg.det()`
- 如何计算特征值和特征向量：`np.linalg.eig()`
- 如何计算方阵的逆：`np.linalg.inv()`

图片如何垂直翻转：`image[::-1, :, :]`

图片如何水平翻转：`image[:, ::-1, :]`

如何裁剪：`image[H1:H2, :, :]`

如何调整亮度：`image = image * 0.5` 注意如果调大亮度需要裁剪 `np.clip(image, a_min=None, a_max=255.)`

压缩图像：`image[::2, ::2, :]`