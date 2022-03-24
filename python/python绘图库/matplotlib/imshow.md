

范围的映射

用`ax.imshow`的`extent`参数。

```python
fig, ax = plt.subplots()
ax.imshow(z, extent=[1, 258, 50, 500])
ax.axis('auto')
```

