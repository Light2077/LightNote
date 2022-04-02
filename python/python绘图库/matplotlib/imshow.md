

范围的映射

用`ax.imshow`的`extent`参数。

```python
fig, ax = plt.subplots()
ax.imshow(z, extent=[1, 258, 50, 500])
ax.axis('auto')
```



imshow倒转y轴

https://stackoverflow.com/questions/14320159/matplotlib-imshow-data-rotated

设置imshow的属性`origin='lower'`
