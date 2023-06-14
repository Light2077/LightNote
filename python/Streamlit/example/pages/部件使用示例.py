import streamlit as st

options = ["apple", "banana", "cat", "dog"]

option = st.selectbox("select a kind of fruit / animal", options=options, index=3)

"You selected: ", option

st.subheader("多选框")

options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"],
)

for option in options:
    st.write(option)
st.write("You selected:", options)

# 选择滑条
start_color, end_color = st.select_slider(
    "Select a range of color wavelength",
    options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
    value=("red", "blue"),
)
st.write("You selected wavelengths between", start_color, "and", end_color)
