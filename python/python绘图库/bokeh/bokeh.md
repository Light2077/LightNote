官网🌏：[Bokeh documentation — Bokeh 3.1.1 Documentation](https://docs.bokeh.org/en/latest/index.html)

入门指南📕：[First steps 1: Creating a line chart — Bokeh 3.1.1 Documentation](https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_1.html)

# 安装

```
pip install bokeh
```



## 第一幅图

创建`demo.py` 填入以下内容

```python
from bokeh.plotting import figure, show

# prepare some data
x = [1, 2, 3, 4, 5]
y1 = [6, 7, 2, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [4, 5, 5, 7, 2]

# create a new plot with a title and axis labels
p = figure(title="Multiple line example", x_axis_label="x", y_axis_label="y")

# add multiple renderers
p.line(x, y1, legend_label="Temp.", color="blue", line_width=2)
p.line(x, y2, legend_label="Rate", color="red", line_width=2)
p.line(x, y3, legend_label="Objects", color="green", line_width=2)

# show the results
show(p)
```

运行

```
python demo.py
```

会生成一个`demo.html`

<img src="images/第一幅图.png" alt="第一幅图" style="zoom:50%;" />

## 在notebook中使用

只需要加入下面的代码即可

```python
from bokeh.plotting import output_notebook
output_notebook()
```

# 基本图表的绘制

## 散点图

### 基本散点图

[Scatter plots — Bokeh 3.1.1 Documentation](https://docs.bokeh.org/en/latest/docs/user_guide/basic/scatters.html)

```python
# 在notbook中展示
from bokeh.plotting import figure, show, output_notebook
output_notebook()

p = figure(width=400, height=400)

# add a circle renderer with a size, color, and alpha
p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

# show the results
show(p)
```

<img src="images/bokeh_散点图.png" alt="image-20230511161557060" style="zoom:67%;" />

### 散点样式

选择不同风格的散点

```python
p.circle()  # 圆形
p.square()  # 正方形
```

可以参考这个图

![image-20230511161906067](images/bokeh_散点样式.png)

用下划线连接两种风格，比如想创建圆里有个十字

```python
p.circle_cross()
```

## 折线图

[Lines and curves — Bokeh 3.1.1 Documentation](https://docs.bokeh.org/en/latest/docs/user_guide/basic/lines.html)

可以绘制

- 简单折线图
- 阶梯线图
- 多折线图
- 带缺失值的折线图
- 堆积折线图（Stacked lines）
- 与散点图结合绘图
- 特殊的图形
  - 线段 segment()，各个独立的线段，传入线段的起始点和结束点
  - 射线 ray()，传入射线的起始点、角度、长度
  - 圆弧 arc()，传入圆弧的圆心、半径、开始角度、结束角度

> **glyph** 是 Bokeh 中的一个术语，表示绘图中的基本几何图形元素。它们用于绘制不同类型的图形，如线段、射线、弧线等。



# 数据源

[Data sources — Bokeh 3.1.1 Documentation](https://docs.bokeh.org/en/latest/docs/user_guide/basic/data.html)