import streamlit as st

left_column, right_column = st.columns([3, 1])
# You can use a column just like st.sidebar:
left_column.write("x" * 300)

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    st.write("x" * 100)
