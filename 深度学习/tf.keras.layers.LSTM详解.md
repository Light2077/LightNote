https://tensorflow.google.cn/api_docs/python/tf/keras/layers/LSTM?hl=zh_cn

## 返回最后时刻的输出


```python
import tensorflow as tf
lstm = tf.keras.layers.LSTM(units=16)
x = tf.random.normal((4, 10, 2))
hidden = lstm(x)
```

输入：`(batch_size, seq_len, emb_dim)`

默认输出：`(batch_size, hidden_units)`

## return_sequences

如果`return_sequences=True`，则返回每一时刻的输出

输出：`(batch_size, seq_len, hidden_units)`

```python
import tensorflow as tf
lstm = tf.keras.layers.LSTM(units=16, return_sequences=True)
x = tf.random.normal((4, 10, 2))
output_sequences = lstm(x)
```

## return_state

```python
import tensorflow as tf
lstm = tf.keras.layers.LSTM(units=16, return_state=True)
x = tf.random.normal((4, 10, 2))
hidden1, hidden2, cell = lstm(x)
print(tf.reduce_sum(hidden1 - hidden2))
```

hidden1 和 hidden2 完全相同，同时还返回了细胞状态cell



## 二者结合

```python
import tensorflow as tf
lstm = tf.keras.layers.LSTM(units=16, return_sequences=True, return_state=True)
x = tf.random.normal((4, 10, 2))
output_sequences, hidden, cell = lstm(x)
print(output_sequences.shape)
print(hidden.shape)
print(cell.shape)
"""
(4, 10, 16)
(4, 16)
(4, 16)
"""
```

