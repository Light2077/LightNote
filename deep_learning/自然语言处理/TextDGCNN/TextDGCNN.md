# TextDGCNN

## 门机制

假设要处理的词向量序列为
$$
X=[x_1,x_2...,x_n]
$$
一维卷积操作加个门
$$
Z=f_1(X) \odot \sigma (f_2(X))
$$

## 空洞卷积机制

[(2016)**Wavenet**: A generative model for raw audio](https://arxiv.org/abs/1609.03499)

[(2015)Multi-Scale Context Aggregation by Dilated Convolutions](https://arxiv.org/abs/1511.07122)

## 注意力层

$$
\mathbf{z} = \sum_{i=1}^n \alpha_i \mathbf{x}_i
$$

$\alpha_i$为注意力权重
$$
\alpha_i = \text{softmax}(\mathbf{v}^T\text{tanh}(W\mathbf{x}_i+b))
$$
