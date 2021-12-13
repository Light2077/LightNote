# LSTM

[`tf.keras.layers.LSTM()`](https://tensorflow.google.cn/api_docs/python/tf/keras/layers/LSTM)

```python
inputs = tf.random.normal([32, 10, 8])
lstm = tf.keras.layers.LSTM(4, return_sequences=True, return_state=True)
whole_seq_output, final_memory_state, final_carry_state = lstm(inputs)
print(whole_seq_output.shape)
# (32, 10, 4)

print(final_memory_state.shape)
# (32, 4)

print(final_carry_state.shape)
# (32, 4)
```

[`tf.keras.layers.Bidirectional()`](https://tensorflow.google.cn/api_docs/python/tf/keras/layers/Bidirectional)

```python
lstm = tf.keras.layers.LSTM(4, return_sequences=True)
bilstm = tf.keras.layers.Bidirectional(lstm)

x = tf.random.normal([32, 10, 8])
y = bilstm(x)
print(y.shape)
```

