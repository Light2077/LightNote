import cv2
import numpy as np

# 读取图片
image = cv2.imread('image.jpg')

# 获取图片的宽和高
(h, w) = image.shape[:2]

# 计算最短边的长度
min_size = min(h, w)

# 计算圆心坐标
center_x = int(w / 2)
center_y = int(h / 2)

# 计算边框宽度
border_size = int(min_size * 0.05)

# 创建一个形状和大小和原图一样的图像，用于存储裁剪后的图像
mask = np.zeros((h, w), dtype=np.uint8)

# 填充圆形
cv2.circle(mask, (center_x, center_y), int(min_size / 2), (255, 255, 255), thickness=-1)

# 利用掩膜进行裁剪
masked_image = cv2.bitwise_and(image, image, mask=mask)

# 创建一个形状和大小和原图一样的图像，用于存储结果图像
result_image = np.zeros((h, w, 3), dtype=np.uint8)

# 将裁剪后的图像拷贝到结果图像中
result_image[center_y - int(min_size / 2):center_y + int(min_size / 2), center_x - int(min_size / 2):center_x + int(min_size / 2)] = masked_image[center_y - int(min_size / 2):center_y + int(min_size / 2), center_x - int(min_size / 2):center_x + int(min_size / 2)]

# 将结果图像转换为RGB格式
result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

# 在结果图像上画一个金色的圆形边框
cv2.circle(result_image, (center_x, center_y), int(min_size / 2) + border_size, (212, 175, 55), thickness=border_size
