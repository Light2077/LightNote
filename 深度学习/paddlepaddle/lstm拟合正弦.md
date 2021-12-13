https://aistudio.baidu.com/bdcpu3/user/135522/1841170/notebooks/1841170.ipynb

```python
import paddle
import numpy as np
import matplotlib.pyplot as plt

class LSTM(paddle.nn.Layer):
    def __init__(self, input_size=1, hidden_size=16):
        super().__init__()
        self.rnn = paddle.nn.LSTM(input_size=input_size, hidden_size=hidden_size,  num_layers=1)
        self.linear = paddle.nn.Linear(hidden_size, 1)

    def forward(self, inputs):
        y, (hidden, cell) = self.rnn(inputs)
        # hidden = paddle.mean(y, axis=1)
        output = self.linear(hidden)
        output = paddle.squeeze(output)
        return output
```

测试lstm输入输出

```python
# 测试LSTM模型

model = LSTM()
# 一批4个样本长度为10
input_size = 1  # 输入维度 单变量预测的话这个就是1 
seq_len = 4  # 用多少个数据预测后一个数据
x = paddle.randn((4, seq_len, input_size))
rnn = paddle.nn.LSTM(input_size=input_size, hidden_size=4)

# x shape (batch_size, seq_len, input_size)
model.forward(x)
```





自己写的dataloader

```python


class DataLoader:
    def __init__(self, data, num_features=1, num_labels=1, batch_size=8):
        """
        num_features : 用多少个数据点来预测
        num_labels : 预测多少个后面的数据点
        """
        self.data = data
        self.num_features = num_features
        self.num_labels = num_labels
        self.batch_size = batch_size

        x = []
        y = []
        for i in range(0, len(data) - num_features - num_labels + 1):
            x.append(data[i:i+num_features])
            y.append(data[i+num_features:i+num_features+num_labels])
        self.x = np.vstack(x).reshape(-1, self.num_features, 1)
        # self.y = np.vstack(y).reshape(-1, self.num_labels, 1)
        self.y = np.vstack(y)
        
        self.num_samples = len(x)
    


    def __iter__(self):
        for i in range(0, self.num_samples, self.batch_size):
            batch_x = self.x[i:i+self.batch_size]
            batch_y = self.y[i:i+self.batch_size]

            batch_x = paddle.to_tensor(batch_x, dtype='float32')
            batch_y = paddle.to_tensor(batch_y, dtype='float32')
            yield batch_x, batch_y 

```

建议用paddle官方的方案

https://www.paddlepaddle.org.cn/documentation/docs/zh/guides/02_paddle2.0_develop/02_data_load_cn.html

```python
import paddle

BATCH_SIZE = 16
BATCH_NUM = 20


class MyDataset(paddle.io.Dataset):
    """
    步骤一：继承paddle.io.Dataset类
    """
    def __init__(self, data, num_features=1, num_labels=1):
        """
        步骤二：实现构造函数，定义数据集大小

        data: numpy.Array 1维数组
        """
        super(MyDataset, self).__init__()
        self.data = data
        self.num_features = num_features
        self.num_labels = num_labels

        x = []
        y = []
        for i in range(0, len(data) - num_features - num_labels + 1):
            x.append(data[i:i+num_features])
            y.append(data[i+num_features:i+num_features+num_labels])
        self.x = np.vstack(x).reshape(-1, self.num_features, 1)
        # self.y = np.vstack(y).reshape(-1, self.num_labels, 1)
        self.y = np.vstack(y)
        self.x = np.array(self.x, dtype="float32")
        self.y = np.array(self.y, dtype="float32")

        self.num_samples = len(x)

    def __getitem__(self, index):
        """
        步骤三：实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据，对应的标签）
        """
        data = self.x[index]
        label = self.y[index]

        return data, label

    def __len__(self):
        """
        步骤四：实现__len__方法，返回数据集总数目
        """
        return self.num_samples


```

数据集生成

```python
num_samples = 1000  # 数据个数
data = np.linspace(-10, 10, num_samples)
data = np.sin(data)
```

构造数据集

```python
dataset = MyDataset(data, num_features=10)
train_loader = paddle.io.DataLoader(custom_dataset, batch_size=BATCH_SIZE, shuffle=False)
```

测试

```python
for x, y in train_loader():
    print(x.shape, y.shape)
    break
```



训练代码

```python
# 训练代码
model = LSTM()
loss_fn = paddle.nn.MSELoss(reduction='mean')
optimizer = paddle.optimizer.SGD(learning_rate=0.01,
                                 parameters=model.parameters())

for epoch in range(10):
    for batch, (batch_x, batch_y) in enumerate(train_loader()):
        y_pred = model(batch_x)
        
        # loss = F.mse_loss(y_pred, batch_y, reduction='mean')
        loss = loss_fn(y_pred, batch_y)
        loss.backward()
        optimizer.step()
        optimizer.clear_grad()
    print("epoch {} loss {:.4f}".format(epoch, float(loss)))
```

评估结果

```python
test_x = data[:-1].reshape(-1, 1, 1)  # 特征
test_y = data[1:]
test_x = paddle.to_tensor(test_x, dtype="float32")
y_pred = model(test_x).numpy().ravel()
plt.plot(test_y)
plt.plot(y_pred)
plt.show()
```

