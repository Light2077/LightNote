https://tf.wiki/zh_hans/basic/tools.html?highlight=tensorboard#tensorboard



## 保存训练过程中的损失信息

```python
summary_writer = tf.summary.create_file_writer('./tensorboard')
# 开始模型训练
for batch_index in range(num_batches):
    # ...（训练代码，当前batch的损失值放入变量loss中）
    with summary_writer.as_default():                               # 希望使用的记录器
        tf.summary.scalar("loss", loss, step=batch_index)
        tf.summary.scalar("MyScalar", my_scalar, step=batch_index)  # 还可以添加其他自定义的变量
```



在项目终端：

```
tensorboard --logdir=./tensorboard
```

## 查看Graph和Profile信息

如果版本大于等于tf2.3，需要提前安装

```
pip install -U tensorboadr -plugin-profile
```



```python
# 训练开始前 开启Trace，可以记录图结构和profile信息
tf.summary.trace_on(graph=True, profiler=True)

# 训练中
for batch, (x, y) in enumerate(dataset):
    pass

# 训练结束后
with summary_writer.as_default():
    tf.summary.trace_export(name="model_trace", step=0, profiler_outdir=log_dir)    # 保存Trace信息到文件
```



```python
from tensorboard.backend.event_processing import event_accumulator
 
#加载日志数据
ea=event_accumulator.EventAccumulator('events.out.tfevents.1550994567.vvd-Inspiron-7557') 
ea.Reload()
print(ea.scalars.Keys())
 
val_psnr=ea.scalars.Items('val_psnr')
print(len(val_psnr))
print([(i.step,i.value) for i in val_psnr])
```

输出



```
['val_loss', 'val_psnr', 'loss', 'psnr', 'lr']
29
[(0, 33.70820617675781), (1, 34.52505874633789), (2, 34.26629638671875), (3, 35.47195053100586), (4, 35.45940017700195), (5, 35.336708068847656), (6, 35.467647552490234), (7, 35.919857025146484), (8, 35.29727554321289), (9, 35.63655471801758), (10, 36.219871520996094), (11, 36.178646087646484), (12, 35.93777847290039), (13, 35.587406158447266), (14, 36.198944091796875), (15, 36.241966247558594), (16, 36.379913330078125), (17, 36.28306198120117), (18, 36.03053665161133), (19, 36.20806121826172), (20, 36.21710968017578), (21, 36.42262268066406), (22, 36.00306701660156), (23, 36.4374885559082), (24, 36.163787841796875), (25, 36.53673553466797), (26, 35.99557113647461), (27, 36.96220016479492), (28, 36.63676452636719)]
```

