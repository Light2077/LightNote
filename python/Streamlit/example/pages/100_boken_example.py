import bokeh
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show
import streamlit as st

st.subheader("bokeh 散点图示例")
df = pd.DataFrame({"apple": [1, 3, 5, 2, 6], "banana": [2, 4, 6, 3, 3]})
source = ColumnDataSource(data=df)

p = figure()
p.circle(x="index", y="apple", source=source, size=15, color="navy", alpha=0.5)
p.triangle(x="index", y="banana", source=source, size=15, color="gold", alpha=0.8)

tooltip = [("apple", "@apple"), ("banana", "@banana")]
hover = HoverTool(tooltips=tooltip)
p.add_tools(hover)

st.bokeh_chart(p, use_container_width=True)


st.subheader("回调测试")
from plot_helper import selectable_scatter_plot

df = pd.DataFrame(np.random.randn(10, 5), columns=list("ABCDE"))
selectable_scatter_plot(df)
# 假设你的DataFrame是df，并且它有5个特征 A, B, C, D, E
# df = pd.DataFrame(...)  # 您的原始DataFrame
