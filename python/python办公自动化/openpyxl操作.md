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

## 案例

### 创建折线图

使用 `openpyxl` 可以相对容易地创建 Excel 折线图。你可以通过对数据列应用图表对象并设置其属性来实现。下面是一个基础的例子：

1. **读取数据**
2. **创建新工作表**
3. **创建折线图对象**
4. **设置图表的数据范围**
5. **设置图表标题和轴标签**
6. **将图表添加到工作表**
7. **保存工作簿**

以下是代码实现：

```python
from openpyxl import Workbook, load_workbook
from openpyxl.chart import LineChart, Reference

# 1. 读取数据
wb = load_workbook('example.xlsx')
data_ws = wb['data']  # 假设数据在名为"data"的工作表中

# 2. 创建新工作表
figure_ws = wb.create_sheet('figure')  # 创建名为"figure"的工作表

# 3. 创建折线图对象
chart = LineChart()

# 4. 设置图表的数据范围
data = Reference(data_ws, min_col=1, min_row=1, max_col=2, max_row=10000)  # 假设数据在A1:B10
chart.add_data(data, titles_from_data=True)
chart.set_categories(Reference(data_ws, min_col=1, min_row=2, max_row=10000))  # 设置x轴的数据范围

# 5. 设置图表标题和轴标签
chart.title = "My Line Chart"
chart.style = 13  # 设置图表样式，可选
chart.x_axis.title = 'X-axis label'
chart.y_axis.title = 'Y-axis label'

# 6. 将图表添加到工作表
figure_ws.add_chart(chart, "A1")  # 将图表添加到 figure 工作表的 A1 单元格

# 7. 保存工作簿
wb.save("example_with_chart.xlsx")
```

这样，你就在 `figure` 工作表的 A1 单元格里添加了一个基于 `data` 工作表 A1:B10 范围内数据的折线图。

注意：以上代码仅适用于 `.xlsx` 格式的工作簿，如果你需要保存宏，请记得使用 `.xlsm` 格式并在加载工作簿时设置 `keep_vba=True`。

这个例子比较基础，`openpyxl` 提供了更多高级的图表设置，但这应该能满足你的基础需求。有其他问题，随时问我。

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

