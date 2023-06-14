import streamlit as st

st.subheader("分栏示例")
left_column, right_column = st.columns([3, 1])
# You can use a column just like st.sidebar:
left_column.write("x" * 300)

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    st.write("x" * 100)

st.subheader("选项卡示例")
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


st.subheader("提示示例")
st.info("This is a purely informational message", icon="💡")
st.warning("This is a warning", icon="⚠️")
st.error("This is an error", icon="🚨")
st.success("This is a success message!", icon="✅")

e = RuntimeError("This is an exception of type RuntimeError")
st.exception(e)

import time

time.sleep(2)
st.snow()
