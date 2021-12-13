### 如何设置坐标轴位置

```python
ax.spines['right'].set_position(('axes', 1.15))
```

### 如何绑定刻度标签与坐标轴

```python
ax.yaxis.set_ticks_position('right')
```

### 隐藏坐标轴边框

```python
ax.spines['top'].set_visi
```

### 设置刻度标签到坐标轴的距离

刻度线的各种设置

https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html?highlight=matplotlib%20axes%20axes%20tick_params#matplotlib.axes.Axes.tick_params

```python
ax.yaxis.set_tick_params(pad=10)
```

