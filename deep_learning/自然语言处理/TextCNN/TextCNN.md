# 前言

卷积神经网络（Convolutional Neural Network）

三个重要的思想：

- 稀疏交互：不是每个输出单元都与输入单元交互
- 参数共享：多个函数参数相同
- 等变表示：平移不变性

什么是卷积运算：

离散形式：
$$
(f*g)(n)=\sum_{r=-\infty}^{\infty}f(\tau)g(n-\tau)
$$
连续形式：
$$
(f*g)(n)=\int_{r=-\infty}^{\infty}f(\tau)g(n-\tau)
$$
卷积的计算方法：比较简单，就是加权求和。

神经网络的局限性：

- 参数量会非常庞大
- 容易过拟合
- 难以发现区域的关联性

# TextCNN网络结构

![img](img/textcnn1.png)

```
x            (batch_size, seq_len)
x_emb        (batch_size, seq_len, emb_dim)
conv1        (batch_size, seq_len-k+1, n_filters) * n_kernels
max_pooling  (batch_size, 1, n_filters) * n_kernels
concat       (batch_size, n_kernels * n_filters)
predict      (batch_size, n_classes)
```

词向量的设计：

- 随机初始化，训练中更新词向量
- 预训练词向量，word2vec、glove，训练中不微调
- 预训练词向量，且在训练中微调。

句子长短不一情况：

- 截断和补齐

超参数：

- batch_size：一个批次的大小
- seq_len：句子的长度
- emb_dim：词向量长度
- n_kernels：卷积核的种类数(2、3、4、...)
- n_filters：一种卷积核有多少个
- filter_size：卷积核的大小
- n_classes：类别数

结论：

- 预训练的word2vec或glove效果好于onehot
- 卷积核大小：有较大影响1~10，句子越长，可以选用越大的卷积核。
- 卷积核的数量：有较大影响 100~600，一般可食用dropout(0-0.5)
- 选ReLu和tanh作为激活函数
- 使用1-max pooling
- 当增加的feature map导致性能降低时，可以使用大于0.5的dropout
- 使用交叉验证，评估模型性能

论文地址：

- https://arxiv.org/pdf/1408.5882.pdf
- https://arxiv.org/pdf/1510.03820.pdf

