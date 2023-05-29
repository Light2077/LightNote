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
