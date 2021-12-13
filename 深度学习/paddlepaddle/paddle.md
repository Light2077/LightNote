## [项目2-2 【手写数字识别】之快速入门](https://aistudio.baidu.com/aistudio/projectdetail/307929)

##### [Q1](# A1)

深度学习模型的标准结构，或者说是流程（5个）

##### [Q2](# A2)

给定一个数据集`trainset`如何对其进行batch打包？

##### [Q3](# A3)

定义模型的时候，类继承自谁？

##### [Q4](# A4)

飞桨动态图环境的施法前摇（必须的一系列操作）？（hint 4个操作）

##### [Q5](# A5)

如何将数据转为飞桨动态图格式？

##### [Q6](# A6)

如何计算样本的平均损失？

##### [Q7](# A7)

后向传播，更新参数的过程怎么做（3个操作）？

##### [Q8](# A8)

如何保存模型？

##### [Q9](# A9)

如何加载训练好的模型的参数并用来预测？

## [项目2-3 【手写数字识别】之数据处理](https://aistudio.baidu.com/aistudio/projectdetail/308940)

##### [Q10](# A10)

如何自己写一个数据读取和预处理函数，主要思考设计思想？

##### [Q11](# A11)

异步数据读取的优点，以及如何实现(多了3行代码)

##### [Q12](# A12)

卷积和池化怎么导入和使用

##### [Q13](# A13)

四种优化算法

##### [Q13](# A13)

在cpu或gpu上训练怎么设置

##### [Q14](# A14)

如何给所有参数添加正则化

##### [Q15](# A15)

如何用tensorboard可视化，tb_paddle

##### [Q16](# A16)

恢复训练，保存和恢复模型及优化器的参数

#####  [Q17](# A17)

embedding怎么用

##### [A1](# Q1)

- 准备数据：读取，数据预处理
- 设计模型：网络结构
- 配置模型参数：优化器，学习率，深度等
- 模型训练：训练过程
- 模型保存读取测试

##### [A2](# Q2)

`trainset = paddle.batch(trainset, batch_size=8)`

##### [A3](# Q3)

`paddle.dygraph.layer`

##### [A4](# Q4)

创建模型，定义训练模式，数据读取函数，优化器

```python
with fluid.dygraph.guard():
    model = MyModel('model_name')
    model.train()  # 启动训练模式
    train_loader = ...  # 数据读取函数
    optimizer = fluid.optimizer.SGDOptimizer(learning_rate=0.001)  # 定义优化器
```

##### [A5](# Q5)

`data = fluid.dygraph.to_variable(data)`

##### [A6](# Q6)

```python
loss = fluid.layers.square_error_cost(predict, label)
avg_loss = fluid.layers.mean(loss)
```

##### [A7](# Q7)

损失函数后向传播，优化器根据损失函数更新参数，模型清除梯度

```python
avg_loss.backward()
optimizer.minimize(avg_loss)
model.clear_gradients()
```

##### [A8](# Q8)

`fluid.save_dygraph(model.state_dict(), 'model_name')`

##### [A9](# Q9)

注意model始终需要事先把输入数据转换成动态图的变量

```python
with fluid.dygraph.guard():
    model = MyModel('model_name')
    params_file_path = 'trained_model'
    model_dict, _ = fluid.load_dygraph("mnist")
    model.load_dict(model_dict)
    model.eval()
    # 中间读取要用来预测的数据
    result = model(...)  # 定义优化器
```

## [项目2-3 【手写数字识别】之数据处理](https://aistudio.baidu.com/aistudio/projectdetail/308940)

##### [A10](# Q10)

主要掌握思想，针对任务的不同，需要读取不同的数据。
定义一个datagenerator 返回的是特征和标签。善用异常处理Exception和校验assert

```python
#数据处理部分的展开代码
# 定义数据集读取器
def load_data(mode='train'):

    # 数据文件
    datafile = './work/mnist.json.gz'
    print('loading mnist dataset from {} ......'.format(datafile))
    data = json.load(gzip.open(datafile))
    # 读取到的数据可以直接区分训练集，验证集，测试集
    train_set, val_set, eval_set = data

    # 数据集相关参数，图片高度IMG_ROWS, 图片宽度IMG_COLS
    IMG_ROWS = 28
    IMG_COLS = 28
    # 获得数据
    if mode == 'train':
        imgs = train_set[0]
        labels = train_set[1]
    elif mode == 'valid':
        imgs = val_set[0]
        labels = val_set[1]
    elif mode == 'eval':
        imgs = eval_set[0]
        labels = eval_set[1]
    else:
        raise Exception("mode can only be one of ['train', 'valid', 'eval']")

    imgs_length = len(imgs)

    assert len(imgs) == len(labels), \
          "length of train_imgs({}) should be the same as train_labels({})".format(
                  len(imgs), len(labels))

    index_list = list(range(imgs_length))

    # 读入数据时用到的batchsize
    BATCHSIZE = 100

    # 定义数据生成器
    def data_generator():
        if mode == 'train':
            # 训练模式下，将训练数据打乱
            random.shuffle(index_list)
        imgs_list = []
        labels_list = []
        
        for i in index_list:
            img = np.reshape(imgs[i], [1, IMG_ROWS, IMG_COLS]).astype('float32')
            label = np.reshape(labels[i], [1]).astype('float32')
            imgs_list.append(img) 
            labels_list.append(label)
            if len(imgs_list) == BATCHSIZE:
                # 产生一个batch的数据并返回
                yield np.array(imgs_list), np.array(labels_list)
                # 清空数据读取列表
                imgs_list = []
                labels_list = []

        # 如果剩余数据的数目小于BATCHSIZE，
        # 则剩余数据一起构成一个大小为len(imgs_list)的mini-batch
        if len(imgs_list) > 0:
            yield np.array(imgs_list), np.array(labels_list)
    return data_generator
```

##### [A11](# Q11)

首先要指定把数据放到cpu还是gpu，然后创建一个备用生成器，把以及定义好的生成器装进去

- 同步数据读取：每当模型需要数据的时候，运行数据读取函数获得当前批次的数据。在读取数据期间，模型一直在等待数据读取结束，获得数据后才会进行计算。
- 异步数据读取：数据读取和模型训练过程异步进行，读取到的数据先放入缓存区。模型训练完一个批次后，不用等待数据读取过程，直接从缓存区获得下一批次数据进行训练。

`fluid.io.DataLoader.from_generator(capacity=5, return_list=True)`详解

创建一个DataLoader对象用于加载Python生成器产生的数据。数据会由Python线程预先读取，并异步送入一个队列中。fluid.io.DataLoader.from_generator参数名称、参数含义、默认值如下：

参数名和默认值如下：

- feed_list=None,
- capacity=None,
- use_double_buffer=True,
- iterable=True,
- return_list=False

参数含义如下：

- feed_list        仅在paddle静态图中使用，动态图中设置为None，本教程默认使用动态图的建模方式。
- capacity        表示在DataLoader中维护的队列容量，如果读取数据的速度很快，建议设置为更大的值。
- use_double_buffer   是一个布尔型的参数，设置为True时Dataloader会预先异步读取下一个batch的数据放到缓存区。
- iterable          表示创建的Dataloader对象是否是可迭代的，一般设置为True。
- return_list        在动态图下需要设置为True。

```python
# 定义数据读取后存放的位置，CPU或者GPU，这里使用CPU
# place = fluid.CUDAPlace(0) 时，数据读到GPU上
place = fluid.CPUPlace()
with fluid.dygraph.guard(place):
    # 声明数据加载函数，使用训练模式
    train_loader = load_data(mode='train')
    # 定义DataLoader对象用于加载Python生成器产生的数据
    data_loader = fluid.io.DataLoader.from_generator(capacity=5, return_list=True)
    # 设置数据生成器
    data_loader.set_batch_generator(train_loader, places=place)
    # 迭代的读取数据并打印数据的形状
    for i, data in enumerate(data_loader):
        image_data, label_data = data
        print(i, image_data.shape, label_data.shape)
        if i>=5:
            break
```

##### [A12](# Q12)

```python
from paddle.fluid.dygraph.nn import Conv2D, Pool2D, FC
self.conv1 = Conv2D(name_scope, num_filters=20, filter_size=5, stride=1, padding=2, act='relu')
self.pool1 = Pool2D(name_scope, pool_size=2, pool_stride=2, pool_type='max')
```

##### [A13](# Q13)

```python
optimizer = fluid.optimizer.SGDOptimizer(learning_rate=0.01)
optimizer = fluid.optimizer.MomentumOptimizer(learning_rate=0.01)
optimizer = fluid.optimizer.AdagradOptimizer(learning_rate=0.01)
optimizer = fluid.optimizer.AdamOptimizer(learning_rate=0.01)
```

##### [A14](# Q14)

`optimizer = fluid.optimizer.AdamOptimizer(learning_rate=0.01, regularization=fluid.regularizer.L2Decay(regularization_coeff=0.1))`

[A15](# Q15)

使用tb-paddle可视化分析

如果期望使用更加专业的作图工具，可以尝试tb-paddle。tb-paddle能够有效地展示飞桨框架在运行过程中的计算图、各种指标随着时间的变化趋势以及训练中使用到的数据信息。tb-paddle的使用也并不复杂，可分为如下四个主要步骤。

１.　步骤1：引入tb_paddle库，定义作图数据存储位置（供第3步使用），本案例的路径是“log/data”。
```python
from tb_paddle import SummaryWriter
data_writer = SummaryWriter(logdir="log/data")
```
２.　步骤2：在训练过程中插入作图语句。当每100个batch训练完成后，将当前损失作为一个新增的数据点(scalar_x和loss的映射对)存储到第一步设置的文件中。使用变量scalar_x记录下已经训练的批次数，作为作图的X轴坐标。

```python
data_writer.add_scalar("train/loss", avg_loss.numpy(), scalar_x)
data_writer.add_scalar("train/accuracy", avg_acc.numpy(), scalar_x)
scalar_x = scalar_x + 100
```

```python
#引入Tensorboard库，并设定保存作图数据的文件位置
from tb_paddle import SummaryWriter
data_writer = SummaryWriter(logdir="log/data")

with fluid.dygraph.guard(place):
    model = MNIST("mnist")
    model.train() 
    
    #四种优化算法的设置方案，可以逐一尝试效果
    optimizer = fluid.optimizer.SGDOptimizer(learning_rate=0.01)
    
    EPOCH_NUM = 10
    iter = 0
    for epoch_id in range(EPOCH_NUM):
        for batch_id, data in enumerate(train_loader()):
            #准备数据，变得更加简洁
            image_data, label_data = data
            image = fluid.dygraph.to_variable(image_data)
            label = fluid.dygraph.to_variable(label_data)
            
            #前向计算的过程，同时拿到模型输出值和分类准确率
            predict, avg_acc = model(image, label)

            #计算损失，取一个批次样本损失的平均值
            loss = fluid.layers.cross_entropy(predict, label)
            avg_loss = fluid.layers.mean(loss)
            
            #每训练了100批次的数据，打印下当前Loss的情况
            if batch_id % 100 == 0:
                print("epoch: {}, batch: {}, loss is: {}, acc is {}".format(epoch_id, batch_id, avg_loss.numpy(), avg_acc.numpy()))
                data_writer.add_scalar("train/loss", avg_loss.numpy(), iter)
                data_writer.add_scalar("train/accuracy", avg_acc.numpy(), iter)
                iter = iter + 100

            #后向传播，更新参数的过程
            avg_loss.backward()
            optimizer.minimize(avg_loss)
            model.clear_gradients()

    #保存模型参数
    fluid.save_dygraph(model.state_dict(), 'mnist')
```

最后使用`$ tensorboard --logdir log/data`查看

##### [A16](# Q16)

先保存

```python
fluid.save_dygraph(model.state_dict(), './checkpoint/mnist_epoch{}'.format(epoch_id))
fluid.save_dygraph(optimizer.state_dict(), './checkpoint/mnist_epoch{}'.format(epoch_id))
```

再读取

```python
with fluid.dygraph.guard(place):
    # 加载模型参数到模型中
    params_dict, opt_dict = fluid.load_dygraph(params_path)  # 注意此处
    model = MNIST("mnist")
    model.load_dict(params_dict)  # 注意此处
    EPOCH_NUM = 5
    BATCH_SIZE = 100
    # 定义学习率，并加载优化器参数到模型中
    total_steps = (int(60000//BATCH_SIZE) + 1) * EPOCH_NUM
    lr = fluid.dygraph.PolynomialDecay(0.01, total_steps, 0.001)
    
    # 使用Adam优化器
    optimizer = fluid.optimizer.AdamOptimizer(learning_rate=lr)
    optimizer.set_dict(opt_dict)  # 注意此处
```

##### [A17](# Q17)

```python
self.embedding = Embedding(
    self.full_name(),
    size=[self.vocab_size, self.embedding_size],
    dtype='float32',
    param_attr=fluid.ParamAttr(
        name='embedding_para',
        initializer=fluid.initializer.UniformInitializer(
            low=-init_scale, high=init_scale)))
```

##### [A18](# Q18)

``