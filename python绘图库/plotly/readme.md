# plotly

https://plotly.com/python/

plotly 是交互式的绘图工具包

通过plotly可以绘制放在网页上的图表，讲道理要比matplotlib更好地展示给用户。

## 安装

pip安装

```
pip install plotly==4.14.3
```

conda安装

```
conda install -c plotly plotly=4.14.3
```



>版本4以前，plotly有离线和在线之分，版本4以后，只有离线

测试是否安装成功

```python
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
fig.write_html('first_figure.html', auto_open=True)
```

运行成功的话会弹出一个网页

## Plotly chart in Dash

[Dash](https://plotly.com/dash/) 是使用Plotly图形在Python中构建分析应用程序的最佳方法。 要在下面运行该应用，请运行pip install dash，单击“下载”以获取代码，然后运行pythonapp.py。

开始使用[Dash官方文档](https://dash.plotly.com/installation)，并了解如何使用Dash Enterprise轻松设置样式并部署此类应用。

```python
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Color:"),
    dcc.Dropdown(
        id="dropdown",
        options=[
            {'label': x, 'value': x}
            for x in ['Gold', 'MediumTurquoise', 'LightGreen']
        ],
        value='Gold',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    [Input("dropdown", "value")])
def display_color(color):
    fig = go.Figure(
        data=go.Bar(y=[2, 3, 1], marker_color=color))
    return fig

app.run_server(debug=True)
```



类似于flask，部署了一个应用

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "__main__" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```



## Jupyter Notebook Support

需要安装前置插件

pip安装

```
pip install "notebook>=5.3" "ipywidgets>=7.5"
```

测试

```python
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
fig.show()
```

### Where to next?

通过三个方式来学习

1. 例子：
   - [basic charts](https://plotly.com/python/basic-charts/)
   - [statistical charts](https://plotly.com/python/statistical-charts/)
   - [scientific charts](https://plotly.com/python/scientific-charts/)
   - [financial charts](https://plotly.com/python/financial-charts/)
   - [maps](https://plotly.com/python/maps/)
   - [3-dimensional charts](https://plotly.com/python/3d-charts/)
2. 基本原理 ：
   - [the structure of figures](https://plotly.com/python/figure-structure/)
   - [how to create and update figures](https://plotly.com/python/creating-and-updating-figures/)
   - [how to display figures](https://plotly.com/python/renderers/), [how to theme figures with templates](https://plotly.com/python/templates/)
   - [how to export figures to various formats](https://plotly.com/python/static-image-export/) 
   - [Plotly Express, the high-level API](https://plotly.com/python/plotly-express/)
3. 文档
   - [Python API reference](https://plotly.com/python-api-reference)  
   - [Figure Reference](https://plotly.com/python/reference)



要想通过python构建网页应用，可以查看 [*Dash User Guide*](https://dash.plotly.com/).

官方论坛： [Plotly Community Forum](http://community.plotly.com/) 

