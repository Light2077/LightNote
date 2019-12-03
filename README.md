# LightNote

Lightnote 是一本笔记，记录Light在学习过程中遇到的问题和解决方案。



## Numpy

`neg, pos = np.bincount(array)`

`np.clip(a,a_min,a_max)` 小于`a_min`的数据变成`a_min`,大于`a_max`的数据变成`a_max`



## Jupyter

- 如何设置默认启动位置：[修改配置文件 jupyter_notebook_config.py](https://www.cnblogs.com/xxtalhr/p/10841241.html)([补充](https://blog.csdn.net/qq_42711359/article/details/98305578))

- 如何使用conda的其他环境(增加其他kernel)：`conda install nb_conda_kernels`

- 如何更换主题



## Anaconda

- 更新Anaconda：`conda update conda`

- 更新所有包：`codna update --all`

- 创建新环境：`conda create -n tf2 python=3.7`

- 加速包的下载安装：[清华镜像站使用](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)



## Pycharm

修改变量名：`shift F6`



## TensorFlow

- [Tensorflow2.0官网教程](https://tensorflow.google.cn/tutorials/)
- [简单粗暴 TensorFlow 2.0](https://tf.wiki/)([本地](E:\GitHub\tensorflow-handbook\docs\index.html))
- ~~keras.metrics 占用内存5个G~~ 其实应该是[GPU增长问题](https://tensorflow.google.cn/guide/gpu#limiting_gpu_memory_growth)
- [样本不平衡]( https://tensorflow.google.cn/tutorials/structured_data/imbalanced_data?hl=en )
- 使用history获取每个epoch的loss
- 正则化项[`tf.keras.regularizers.l2(0.01)`]( https://tensorflow.google.cn/guide/keras/overview?hl=en#configure_the_layers )

## Markdown

- [公式对齐](https://blog.csdn.net/bendanban/article/details/77336206)

## 其他

- 绘图：[draw.io](https://draw.io)