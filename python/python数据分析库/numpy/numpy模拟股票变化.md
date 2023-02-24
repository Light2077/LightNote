```python
np.random.seed(11)
# seed(3) 狂欢之后跌到谷底 clip(0.9995, 1.0005)
# seed(9) 先苦后甜 clip(0.9997002, 1.0003)
# seed(9) 疯狂的变化(0.9992009, 1.0008)
# seed(11) 疯狂

fig, ax = plt.subplots(figsize=(12, 3))
y_init = 10
y = np.random.normal(scale=5, size=60 * 60 * 24 * 360) / 100 + 1
y = np.clip(y, 0.9990005, 1.001)
y = y_init * y.cumprod()

plt.plot(y[::40])
```

