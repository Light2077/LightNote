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

![img](images/textcnn1.png)

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



令$\mathbf{x}_i \in \mathbf{R}^k$表示一句话中的第$i$个词，该词的词向量维度为$k$。则整句话可以表示为：
$$
\mathbf{x}_{1:n}=\mathbf{x}_1 \oplus \mathbf{x}_2 \oplus ... \oplus \mathbf{x}_n
$$
textcnn的卷积运算
$$
c_i=f(\mathbf{w} \cdot \mathbf{x}_{i:i+h-1}+b)
$$
$\mathbf{w} \in \mathbf{R}^{hk}$

对整个句子进行卷积运算后，得到新的特征图$\mathbf{c}$
$$
\mathbf{c} = [c_1, c_2, ...,c_{n-h+1}]
$$
$\mathbf{c} \in \mathbf{R}^{n-h+1}$是一个一维向量

然后在该特征向量上应用最大池化操作[49]，提取特征向量中的最大值

$\hat{c}=\text{max}\{\mathbf{c}\}$

TextCNN使用多个滤波器(具有不同窗口大小)以获得多个特性，这些特征形成倒数第二层，并传递给完全连接的softmax层，该层的输出是标签上的概率分布。

最后一层的输入
$$
\mathbf{z}=[\hat{c}_1,...\hat{c}_m]
$$
原本的最后一层
$$
y=\mathbf{w} \cdot \mathbf{z} + b
$$
采用的dropout正则化后的模型输出层为:
$$
y=\mathbf{w} \cdot (\mathbf{z} \odot \mathbf{r}) + b
$$
$\mathbf{r} \in \mathbf{R}^m$

在测试阶段，会把最后一层的权重变为：$\hat{\mathbf{w}}=p\mathbf{w}$，这样做的意义是什么？

# 代码

```python
class TextCNN(tf.keras.Model):
    """
    可以考虑的优化的点：
    - filters 改成可以调的，跟kernel_sizes一样可以变化
    -
    """

    def __init__(self, seq_max_len, vocab_size, embedding_dim, output_dim,
                 kernel_sizes, filters=2, embedding_matrix=None):
        super(TextCNN, self).__init__()
        self.seq_max_len = seq_max_len
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim

        if embedding_matrix is None:
            self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        else:
            self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                                       weights=[embedding_matrix], trainable=True)

        self.kernel_sizes = kernel_sizes  # exm: [2, 3, 4]
        self.filters = filters
        self.conv1d = [tf.keras.layers.Conv1D(filters=self.filters, kernel_size=k, strides=1)
                       for k in self.kernel_sizes]
        # max_len-k+1 是卷积层后词向量剩下的长度
        # max_len-k+1 这是为了池化层直接取到剩下的词向量的长度
        self.maxpool1d = [tf.keras.layers.MaxPool1D(seq_max_len - k + 1) for k in self.kernel_sizes]

        self.x_flatten = tf.keras.layers.Flatten()
        # 输出层
        self.dense = tf.keras.layers.Dense(output_dim)

    def call(self, x):
        # input shape (batch_size, max_seq_len)
        # embedding shape (batch_size, max_seq_len, embedding_size)
        x = self.embedding(x)
        pool_output = []
        for conv, pool in zip(self.conv1d, self.maxpool1d):
            c = conv(x)  # (batch_size, max_len-kernel_size+1, filters)
            p = pool(c)  # (batch_size, 1, filters)
            pool_output.append(p)

        # (batch_size, 1, n*filters)
        pool_output = tf.concat(pool_output, axis=2)
        # pool_output = tf.squeeze(pool_output)
        # (batch_size, n * filters)
        pool_output = self.x_flatten(pool_output)

        # (batch_size, output_dim)
        y = self.dense(pool_output)
        return y
```

