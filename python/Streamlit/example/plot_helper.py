import bokeh
import pandas as pd
from bokeh.models import Select, ColumnDataSource, HoverTool, CustomJS
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.io import curdoc
import streamlit as st


def predict_compare_plot(y_true, y_pred):
    df = pd.DataFrame({"y_pred": y_pred, "y_true": y_true})
    source = ColumnDataSource(data=df)

    p = figure(width=400, height=200)
    p.circle(x="index", y="y_pred", source=source, size=15, color="navy", alpha=0.5)
    p.triangle(x="index", y="y_true", source=source, size=15, color="gold", alpha=0.8)

    tooltip = [("预测值", "@y_pred"), ("真实值", "@y_true")]
    hover = HoverTool(tooltips=tooltip)
    p.add_tools(hover)

    st.bokeh_chart(p, use_container_width=True)


def scatter_plot(df, width=400, height=400):
    source = ColumnDataSource(df)
    xlabel, ylabel = df.columns[0], df.columns[-1]

    p = figure(width=width, height=height)
    p.circle(x=xlabel, y=ylabel, source=source, size=15, color="navy", alpha=0.5)
    tooltip = [(f"{xlabel}", f"@{xlabel}"), (f"{ylabel}", f"@{ylabel}")]
    hover = HoverTool(tooltips=tooltip)
    p.add_tools(hover)

    st.bokeh_chart(p, use_container_width=True)


def selectable_scatter_plot(df):
    cols = df.columns
    source = ColumnDataSource(data=df)

    # 创建初始散点图（这里假设初始状态为 A-B）
    p = figure(width=400, height=400)
    circles = p.circle("A", "B", source=source, size=15, color="navy", alpha=0.5)
    # 创建两个选择器，用于选择散点图的x和y
    select_x = Select(title="x", value=cols[0], options=cols.tolist())
    select_y = Select(title="y", value=cols[1], options=cols.tolist())

    # 当选择器的值发生改变时，调用回调函数
    # select.on_change('value', update)
    callback_x = CustomJS(
        args=dict(circles=circles, source=source, select=select_x),
        code="""
        var f = select.value;
        circles.glyph.x.field = f;
        source.change.emit();
    """,
    )
    callback_y = CustomJS(
        args=dict(circles=circles, source=source, select=select_y),
        code="""
        var f = select.value;
        circles.glyph.y.field = f;
        source.change.emit();
    """,
    )

    select_x.js_on_change("value", callback_x)
    select_y.js_on_change("value", callback_y)
    # 将散点图和选择器组合在一起并显示
    layout = column(select_x, select_y, p)
    curdoc().add_root(layout)
    st.bokeh_chart(layout, use_container_width=True)
