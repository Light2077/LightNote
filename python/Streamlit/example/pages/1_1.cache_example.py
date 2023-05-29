import time

import pandas as pd
import streamlit as st


st.code(
    """
import time

import pandas as pd
import streamlit as st


@st.cache_data  # 👈 Add the caching decorator
def load_data():
    time.sleep(3)
    df = pd.DataFrame([[1, 2, 3], [3, 4, 5]])
    return df


df = load_data()
st.dataframe(df)

st.button("Rerun")

"""
)


# @st.cache_data  # 👈 Add the caching decorator
def load_data():
    time.sleep(5)
    df = pd.DataFrame([[1, 2, 3], [3, 4, 5]])
    return df


df = load_data()
st.dataframe(df)

st.button("Rerun")
