# 简介

prophet

facebook的时间序列预测工具

https://facebook.github.io/prophet/docs/quick_start.html

# 安装

安装是个大麻烦，最好用anaconda安装，而且需要重新建立一个虚拟环境，这是最简便的方法了，否则可能会遭遇各种错误（我没能解决）

创建新环境

```
conda create -n prophet python=3.7
```

安装prophet

```
conda install -c conda-forge prophet
```

# 原理

https://blog.csdn.net/a358463121/article/details/70194279



[Prophet（预言者）facebook时序预测----论文总结以及调参思路](https://blog.csdn.net/h4565445654/article/details/78398089)


$$
g(t)=\frac{C}{1+exp(-k(t-b))}
$$
b表示曲线的中点

# 使用

```python
import pandas as pd
from prophet import Prophet
```

预测前需要将DataFrame的格式转换成两列

- ds：时间戳，年月日或年月日 时分秒
- y：目标值

# Saturting Forecasts

>saturate
>
>verb  /ˈsætʃəreɪt/
>
>to fill something/somebody completely with something so that it is impossible or [useless](https://www.oxfordlearnersdictionaries.com/definition/english/useless#useless_sng_1) to add any more

Saturting Forecasts，饱和预测。比如人口数量，随着增长通常会达到一个瓶颈难以继续增长。

https://facebook.github.io/prophet/docs/saturating_forecasts.html#forecasting-growth

# 趋势变化点

[Trend Changepoints     ](http://facebook.github.io/prophet/docs/trend_changepoints.html)

时间序列的趋势可能会发生突然的变化，Prophet会自动地检测趋势变化点，也可以手动控制趋势变化点的选择。

Prophet 通过首先指定大量允许速率变化的潜在变化点来检测变化点。 然后它对速率变化的幅度进行稀疏先验（相当于 L1  正则化）——这实质上意味着 Prophet 有大量可能发生速率变化的地方，但会尽可能少地使用它们。 考虑快速入门中的佩顿曼宁预测。  默认情况下，Prophet 指定了 25 个潜在的变化点，它们统一放置在时间序列的前 80% 中。 此图中的垂直线表示放置潜在变化点的位置



用序列的80%推断变化点。

changepoint_range=0.8



## 调整趋势变化灵活度

如果趋势变化过拟合了（太灵活了），或欠拟合，可以调整稀疏先验（sparse prior）的强度。默认情况下`changepoint_prior_scale=0.05`

增大这个数值会趋势变化得更加灵活

```python
m = Prophet(changepoint_prior_scale=0.5)
forecast = m.fit(df).predict(future)
fig = m.plot(forecast)
```

## 指定趋势变化点位置

```python
m = Prophet(changepoints=['2014-01-01'])
forecast = m.fit(df).predict(future)
fig = m.plot(forecast)
```

# 季节、假期与回归器

## 节假日建模与特殊事件



https://facebook.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html

# 乘性季节性

https://facebook.github.io/prophet/docs/multiplicative_seasonality.html

越来越高（低）

# 不确定间隔

趋势的不确定性、季节性估计的不确定性和额外的观测噪声。



**趋势变化的不确定性**

不确定间隔默认是80%

```python
# Python
forecast = Prophet(interval_width=0.95).fit(df).predict(future)

```



季节性不确定

默认为0，采用MCMC采样

```python
# Python
m = Prophet(mcmc_samples=300)
forecast = m.fit(df).predict(future)
```

# 异常点

y异常值处理，可以把异常点

