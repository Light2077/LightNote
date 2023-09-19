当然，`openpyxl` 是一个 Python 库，用于读取和写入 Excel 2010 xlsx/xlsm/xltx/xltm 文件。它相对来说比较全面和强大，支持样式、图片、公式等多种 Excel 功能。

### 安装
首先确保你已经安装了 `openpyxl`，如果没有安装，你可以使用以下命令进行安装：
```bash
pip install openpyxl
```

### 读取 Excel 文件
你可以使用 `openpyxl.load_workbook()` 方法加载一个现有的 Excel 文件。
```python
from openpyxl import load_workbook

# 加载一个 Excel 文件
wb = load_workbook("example.xlsx")

# 获取所有工作表名
print(wb.sheetnames)

# 获取当前工作表
ws = wb.active
```

### 读取单元格数据
```python
# 通过单元格坐标读取数据
print(ws['A1'].value)

# 或者
print(ws.cell(row=1, column=1).value)
```

### 写入 Excel 文件
```python
# 修改单元格的值
ws['A1'] = 'hello'

# 或者
ws.cell(row=1, column=1, value='hello')
```

### 添加新的工作表
```python
ws2 = wb.create_sheet("NewSheet")
ws2['A1'] = "New Data"
```

### 保存 Excel 文件
```python
wb.save("modified_example.xlsx")
```

### 保留宏
如果你的工作簿包含宏，你需要以 `.xlsm` 格式保存，并在打开时指明它包含宏：
```python
wb = load_workbook("example.xlsm", keep_vba=True)
wb.save("modified_example.xlsm")
```

这只是 `openpyxl` 的基础功能。实际上，你还可以使用它来做很多高级操作，如添加过滤器、插入图表、设置样式等。

希望这能帮助你入门 `openpyxl`！有其他问题，随时问我。

### openpyxl 图像的定制

使用`openpyxl`库进行这种高级的图表定制可能有些限制，不过你可以尝试以下方法：

1. **指定线条粗细与颜色**  
    在你创建的 `Series` 对象上，可以尝试修改 `graphicalProperties` 属性。
    ```python
    series.graphicalProperties.line.width = 25000  # 2.5pt，注意单位是EMU（English Metric Unit）
    series.graphicalProperties.line.solidFill = "FF0000"  # 红色
    ```

2. **设置图例**  
    可以在 `ScatterChart` 对象上使用 `legend` 属性。
    ```python
    chart.legend = None  # 隐藏图例
    # 或
    chart.has_legend = True
    chart.legend.position = "b"  # 底部
    ```

3. **修改x,y轴范围**  
    可以通过修改 `x_axis` 和 `y_axis` 的 `min` 和 `max` 属性。
    ```python
    chart.x_axis.min = 0
    chart.x_axis.max = 10
    chart.y_axis.min = -1
    chart.y_axis.max = 1
    ```

4. **调整图的尺寸**  
    `openpyxl` 中使用 `width` 和 `height` 属性来设置图的尺寸。
    ```python
    chart.width = 15  # 单位为英寸
    chart.height = 7.5  # 单位为英寸
    ```

5. **设置图像外边框线**  
    我认为 `openpyxl` 不支持设置图像外边框线的功能。这通常是在Excel中手动设置的。

下面是一个简单的完整示例：

```python
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = 'data'

for i in range(1, 11):
    ws.append([i, i*i])

chart = ScatterChart()
chart.title = "Scatter Chart Example"
chart.x_axis.title = 'X Axis'
chart.y_axis.title = 'Y Axis'

chart.x_axis.min = 0
chart.x_axis.max = 10
chart.y_axis.min = 0
chart.y_axis.max = 100

chart.width = 15
chart.height = 10

chart.legend = None

xvalues = Reference(ws, min_col=1, min_row=1, max_row=10)
yvalues = Reference(ws, min_col=2, min_row=1, max_row=10)

series = Series(yvalues, xvalues, title="First Series")
series.graphicalProperties.line.width = 25000  # Width in EMUs
series.graphicalProperties.line.solidFill = "FF0000"  # Red color

chart.series.append(series)

ws = wb.create_sheet(title='chart')
ws.add_chart(chart, "A1")

wb.save("scatter_chart_advanced.xlsx")
```

这个例子演示了如何调整部分高级属性，你可以根据需要进行修改。需要注意的是，由于`openpyxl`库的局限性，有些高级的图表特性可能无法实现。

## 案例

### 散点图

[一分钟学会用Python的第三方库openpyxl画真散点图_互联网集市 (qyyshop.com)](https://www.qyyshop.com/info/423066.html)

```python
"""
__author__ = '伴月雎'
__time__ = '2021/4/21 19:15'
"""
from openpyxl import Workbook
from openpyxl.chart import (
    ScatterChart,
    Reference,
    Series,
)

wb = Workbook()
ws = wb.active
rows = [
    ['Size', 'Batch 1', 'Batch 2'],
    [2, 40, 30],
    [3, 40, 25],
    [4, 50, 30],
    [5, 30, 25],
    [6, 25, 35],
    [7, 20, 40],
]
for row in rows:
    ws.append(row)

chart = ScatterChart()
chart.title = "Scatter Chart"
chart.style = 10
chart.x_axis.title = 'Size'
chart.y_axis.title = 'Percentage'

xvalues = Reference(ws, min_col=1, min_row=2, max_row=7)
for i in range(2, 4):
    values = Reference(ws, min_col=i, min_row=1, max_row=7)
    series = Series(values, xvalues, title_from_data=True)
    chart.series.append(series)
# 第一条散点
s1 = chart.series[0]
# 散点标记类型  'auto', 'dash', 'triangle', 'square', 'picture', 'circle', 'dot', 'plus', 'star', 'diamond', 'x'
s1.marker.symbol = "circle"
s1.marker.graphicalProperties.solidFill = "0000FF"  # Marker filling 设定标记填充的颜色
s1.marker.graphicalProperties.line.solidFill = "0000FF"  # Marker outline 标记轮廓的颜色
s1.graphicalProperties.line.noFill = True  # 关闭连线填充

# 第二条带连线的散点
s2 = chart.series[1]
s2.marker.symbol = "circle"
s2.graphicalProperties.solidFill = "FF0000"
s2.marker.graphicalProperties.line.solidFill = "FF0000"
s2.graphicalProperties.dashStyle = "dash"
s2.graphicalProperties.line.width = 1000  # width in EMUs

ws.add_chart(chart, "A10")
wb.save("scatter.xlsx")
```



### 创建折线图

假设现在需要构建一个excel表，包含两个sheet，第一个sheet命名为`data`，有两列数据，第一列列名为`x`是横坐标，第二列列名为`y`是纵坐标。

第二个sheet命名为`plot`，用前一个sheet的数据绘制带平滑线的散点图。

其中，第一个sheet的数据由如下的代码产生

```python
import numpy as np
import pandas as pd

x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({
    'x': x,
    'y': y
})

```

完整代码如下

```python
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.chart import ScatterChart, Reference, Series

# 生成数据
x = np.linspace(0, 10, 100)
y = np.sin(x)
df = pd.DataFrame({
    'x': x,
    'y': y
})

# 创建一个Excel工作簿和一个名为'data'的工作表
wb = Workbook()
ws1 = wb.active
ws1.title = "data"

# 将数据填入'data'工作表
for index, col in enumerate(df.columns):
    col_letter = get_column_letter(index + 1)
    ws1[f"{col_letter}1"] = col
    for row, value in enumerate(df[col]):
        ws1[f"{col_letter}{row + 2}"] = value

# 创建一个新的工作表用于绘图，并命名为'plot'
ws2 = wb.create_sheet(title='plot')

# 创建一个散点图对象
chart = ScatterChart()
chart.title = "Scatter Chart with Smooth Lines"
chart.x_axis.title = 'x'
chart.y_axis.title = 'y'

# 设置数据范围
xvalues = Reference(ws1, min_col=1, min_row=2, max_row=101)
yvalues = Reference(ws1, min_col=2, min_row=2, max_row=101)

# 创建系列并添加到图表中
series = Series(yvalues, xvalues, title_from_data=True)
chart.series.append(series)

# 将图表添加到'plot'工作表
ws2.add_chart(chart, "A1")

# 保存工作簿
wb.save("data_plot.xlsx")

```



### 在excel中插入图片

在 `openpyxl` 中，你可以使用 `openpyxl.drawing.image.Image` 类来将图片插入到工作表。下面是一个简单的例子，演示如何将一张图片插入到名为 `figure` 的工作表中：

1. 首先，确保你有一张图片文件，比如 `example.png`。
2. 接着，使用以下代码将图片插入到 Excel 工作簿的 `figure` 工作表。

```python
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

# 1. 加载现有的 Excel 工作簿
wb = load_workbook('example.xlsx')
if "figure" not in wb"
    figure_ws = wb.create_sheet('figure')
# 2. 获取 figure 工作表
figure_ws = wb['figure']

# 3. 创建一个 Image 对象
img = Image('example.png')

# 4. 设置图片的位置
img.anchor = 'A1'

# 5. 将图片添加到工作表
figure_ws.add_image(img)

# 6. 保存工作簿
wb.save('example_with_image.xlsx')
```

这样，图片 `example.png` 就会被插入到 `figure` 工作表的 'A1' 单元格位置。

你可以通过修改 `img.anchor` 的值来改变图片的起始位置。例如，设置为 'B5' 会让图片从 'B5' 单元格开始。

这应该满足你插入图片到特定工作表的需求。有其他问题，请随时问我。

### 调整sheet顺序，设置活动的sheet

```python
from openpyxl import load_workbook

# 1. 加载 Excel 工作簿
wb = load_workbook('example.xlsx')

# 2. 获取所有工作表名称
sheetnames = wb.sheetnames  # 假设现在是 ['A', 'B', 'C']

# 3. 重新排序工作表
wb._sheets = [wb[sheetname] for sheetname in reversed(sheetnames)]  # 变为 ['C', 'B', 'A']

# 或者使用 reorder_sheets 方法
# wb.reorder_sheets(['C', 'B', 'A'])

# 4. 设置 'A' 为当前活动的工作表
wb.active = wb['A']

# 5. 保存工作簿
wb.save('example_reordered.xlsx')

```

