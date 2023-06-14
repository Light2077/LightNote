import re

import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.formula.api import ols
from helper.ols_helper import get_ols_formula, show_summary_in_streamlit

# 构造数据
df = pd.DataFrame(np.random.randn(20, 4), columns=list("abcd"))
formula = get_ols_formula(df.columns[-1], df.columns[:-1])

# 构建模型
model = ols(formula, data=df).fit()
summary = model.summary()

show_summary_in_streamlit(summary)
