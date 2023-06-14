from bokeh.plotting import figure, show
import numpy as np
import pandas as pd
from bokeh.models import Band, ColumnDataSource
from datetime import datetime, timedelta

# 示例数据
data = [1, 3, 5, 6, 7, 8, 6, 5, 4, 3, 2, 5, 6, 7, 8, 7, 5, 4, 2, 4, 4, 65, 9, 7, 7, 8]
# 时间序列的起始时间
start_time = datetime.now()

# 时间间隔
time_delta = timedelta(hours=1)


# 滑窗处理数据
window_size = 5  # 窗口大小

x = []  # x 坐标
y_min = []  # 窗口内最小值
y_max = []  # 窗口内最大值

for i in range(len(data) - window_size + 1):
    window_data = data[i : i + window_size]
    window_start_time = start_time + (i * time_delta)
    x.append(window_start_time)
    y_min.append(np.min(window_data))
    y_max.append(np.max(window_data))


# 创建绘图对象
p = figure(
    title="Time Series with Sliding Window",
    x_axis_type="datetime",
    x_axis_label="Time",
    y_axis_label="Value",
)

s1 = ColumnDataSource(pd.DataFrame({"x": x, "y_min": y_min, "y_max": y_max}))

band = Band(
    base="x",
    lower="y_min",
    upper="y_max",
    fill_alpha=0.3,
    source=s1,
    fill_color="gray",
    line_color="black",
)
p.add_layout(band)

# 显示图形
show(p)
