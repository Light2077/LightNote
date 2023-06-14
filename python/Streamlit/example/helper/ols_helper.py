import re

import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.formula.api import ols


def get_ols_formula(label, features):
    feature_formula = " + ".join(features)
    formula = f"{label} ~ {feature_formula}"
    return formula


def get_ols_summary_note(summary):
    summary_note = summary.extra_txt
    summary_note = re.sub("\n", " ", summary_note)
    notes = re.findall(r"(?<=\[\d\]).*?(?=\[|$)", summary_note, flags=re.S)
    return [n.strip() for n in notes]


def show_summary_in_streamlit(summary):
    st.subheader("回归建模结果")
    for table in summary.tables:
        title = table.title
        table.title = ""
        st.markdown(table.as_html(), unsafe_allow_html=True)
        st.markdown("---")

    st.subheader("💡注意")
    notes = get_ols_summary_note(summary)
    for n in notes:
        st.write("-", n)


if __name__ == "__main__":
    # 构造数据
    df = pd.DataFrame(np.random.randn(20, 4), columns=list("abcd"))
    formula = get_ols_formula(df.columns[-1], df.columns[:-1])
    # st.write(formula)

    # 构建模型
    model = ols(formula, data=df).fit()
    summary = model.summary()
